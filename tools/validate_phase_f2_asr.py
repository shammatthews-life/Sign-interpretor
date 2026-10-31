"""Focused unit tests for Phase F2 buffered ASR adapter (no model download needed)."""
from __future__ import annotations

import sys
from pathlib import Path
import base64
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from asr.streaming_asr import FasterWhisperBackend, TranscriptEvent, TranscriptStabilizer
from asr.asr_service import LocalASRService
from asr.gpu_execution import CudaExecutionError, resolve_execution_configuration

cpu_test_config = resolve_execution_configuration("CPU_TEST_ONLY")
assert cpu_test_config["device"] == "cpu" and cpu_test_config["compute_type"] == "int8"
preferred_cpu_config = resolve_execution_configuration("GPU_PREFERRED", device="cpu")
assert preferred_cpu_config["device"] == "cpu" and preferred_cpu_config["fallback_reason"]
default_service = LocalASRService()
assert default_service.status()["device"] == "cuda"
assert default_service.status()["execution_mode"] == "GPU_REQUIRED"
try:
    resolve_execution_configuration("GPU_REQUIRED", device="cpu")
except CudaExecutionError:
    pass
else:
    raise AssertionError("GPU_REQUIRED must reject CPU selection rather than silently fall back.")


class Segment:
    def __init__(self, text: str, avg_logprob: float = -0.2) -> None:
        self.text, self.avg_logprob = text, avg_logprob


class FakeWhisperModel:
    def __init__(self) -> None:
        self.calls = 0

    def transcribe(self, _audio, **_kwargs):
        self.calls += 1
        texts = [" hello", " hello good", " hello good", " hello good morning"]
        return [Segment(texts[min(self.calls - 1, len(texts) - 1)])], object()


created = []
def model_factory(_name, **_kwargs):
    model = FakeWhisperModel(); created.append(model); return model


backend = FasterWhisperBackend(
    model_name="fake", model_factory=model_factory, minimum_decode_ms=1000,
    decode_hop_ms=750, rolling_window_ms=4000,
)
backend.start()
backend.start()
assert len(created) == 1, "Model must load exactly once and be reused."

events = backend.accept_audio_chunk(np.zeros(16000, dtype=np.float32), audio_start_ms=0, audio_end_ms=1000)
assert [event.kind for event in events] == ["PARTIAL_TRANSCRIPT"] and events[0].text == "hello", "First buffered partial failed."
events = backend.accept_audio_chunk(np.zeros(12000, dtype=np.float32), audio_start_ms=1000, audio_end_ms=1750)
assert [event.text for event in events] == ["hello good"], "Second partial failed."
events = backend.accept_audio_chunk(np.zeros(12000, dtype=np.float32), audio_start_ms=1750, audio_end_ms=2500)
assert not events, "Repeated transcript should be suppressed."
events = backend.flush()
assert [event.kind for event in events] == ["FINAL_TRANSCRIPT"] and events[0].text == "hello good morning", "Final event failed."
report = backend.events[-1].report()
assert report["audio_duration_ms"] > 0 and report["compute_ms"] >= 0 and report["rtf"] >= 0, "Timing/RTF report failed."

backend.pause(); assert backend.accept_audio_chunk(np.zeros(16000), audio_start_ms=2500, audio_end_ms=3500) == [], "Paused backend accepted audio."
backend.resume(); backend.reset()
assert backend.state == "stopped" and len(backend.samples) == 0 and not backend.events, "Reset left stale audio or events."
backend.start()
events = backend.accept_audio_chunk(np.zeros(16000, dtype=np.float32), audio_start_ms=0, audio_end_ms=1000)
assert backend.state == "running" and [event.kind for event in events] == ["PARTIAL_TRANSCRIPT"], "Backend did not restart with a fresh transcript session."

class ShortUtteranceModel:
    def transcribe(self, _audio, **_kwargs):
        return [Segment(" hello")], object()

short_backend = FasterWhisperBackend(
    model_name="short-test",
    model_factory=lambda *_args, **_kwargs: ShortUtteranceModel(),
    minimum_decode_ms=1000,
)
short_backend.start()
short_audio = np.zeros(3200, dtype=np.float32)  # 200 ms, below the partial decode minimum.
assert short_backend.accept_audio_chunk(short_audio, audio_start_ms=0, audio_end_ms=200) == [], "Short utterance should wait for finalization, not be partially decoded."
events = short_backend.flush()
assert [event.kind for event in events] == ["FINAL_TRANSCRIPT"] and events[0].text == "hello", "Explicit flush must finalize audio shorter than the decode minimum."
assert len(short_backend.samples) == 0, "Flush must clear the completed utterance audio."
assert short_backend.accept_audio_chunk(short_audio, audio_start_ms=500, audio_end_ms=700) == [], "Fresh short utterance should wait for finalization."
events = short_backend.flush()
assert [event.kind for event in events] == ["FINAL_TRANSCRIPT"] and events[0].text == "hello", "A fresh utterance must be allowed to repeat the same final transcript."
short_backend.stop()

class StuckWorker:
    def is_alive(self): return True
    def join(self, timeout=None): self.join_timeout = timeout

worker_backend = FasterWhisperBackend(model_name="fake", model_factory=model_factory, async_worker=True)
worker_backend._worker_thread = StuckWorker()
try:
    worker_backend.stop()
except TimeoutError:
    pass
else:
    raise AssertionError("A still-running ASR worker must not be reported as stopped.")
assert worker_backend._worker_thread.join_timeout == 5.0, "ASR worker shutdown must be bounded."
try:
    worker_backend.start()
except RuntimeError:
    pass
else:
    raise AssertionError("A fresh ASR worker must not start while the previous worker is alive.")
worker_backend._worker_thread = None

class FlushTimeoutEvent:
    def clear(self): pass
    def wait(self, timeout=None): return False

flush_backend = FasterWhisperBackend(model_name="fake", model_factory=model_factory, async_worker=True)
flush_backend.state = "running"
flush_backend.samples = np.ones(1, dtype=np.float32)
flush_backend._flush_completed = FlushTimeoutEvent()
try:
    flush_backend.flush()
except TimeoutError:
    pass
else:
    raise AssertionError("An incomplete asynchronous ASR flush must be reported.")

stabilizer = TranscriptStabilizer()
assert stabilizer.partial(" hello ") == "hello"
assert stabilizer.partial("hello") is None
assert stabilizer.final("hello") == "hello"
assert stabilizer.final("hello") is None

class ServiceBackend:
    def __init__(self, *_args, **_kwargs): self.state = "stopped"; self.model_name = "fake"; self.device = "cpu"; self.compute_type = "int8"; self.flush_calls = 0
    def start(self): self.state = "running"
    def accept_audio_chunk(self, _samples, **_kwargs): return []
    def pause(self): self.state = "paused"
    def resume(self): self.state = "running"
    def flush(self):
        self.flush_calls += 1
        return [TranscriptEvent("FINAL_TRANSCRIPT", "hello", 0, 100, 1, 2, 3)]
    def stop(self): self.state = "stopped"
    def reset(self): self.state = "stopped"

service = LocalASRService(ServiceBackend)
assert service.start(model="fake", execution_mode="CPU_TEST_ONLY")["state"] == "running"
raw = np.zeros(1600, dtype="<f4").tobytes()
response = service.accept({"samples_base64": base64.b64encode(raw).decode(), "audio_start_ms": 0, "audio_end_ms": 100})
assert response["status"]["audio_duration_ms"] == 100, "F1-to-ASR service bridge did not account for canonical chunk."
record_calls = 0
record_events = service._record
def count_record(events):
    global record_calls
    record_calls += 1
    record_events(events)
service._record = count_record
flush_response = service.control("flush")
assert len(flush_response["events"]) == 1 and flush_response["events"][0]["text"] == "hello", "ASR flush did not return its finalized transcript."
assert flush_response["status"]["final"] == "hello", "ASR flush status was not updated from its finalized transcript."
assert service.backend.flush_calls == 1, "ASR flush event was requested or recorded more than once."
assert record_calls == 1, "ASR flush event was recorded more than once."
assert service.control("pause")["state"] == "paused"
assert service.control("reset")["audio_duration_ms"] == 0
assert service.start(model="fake", execution_mode="CPU_TEST_ONLY")["state"] == "running", "ASR service did not restart after reset."
response = service.accept({"samples_base64": base64.b64encode(raw).decode(), "audio_start_ms": 0, "audio_end_ms": 100})
assert response["status"]["audio_duration_ms"] == 100, "Restart retained stale ASR audio duration."

print("PASS: ASR backend lifecycle loads once, resets cleanly, and restarts without stale transcript state")
print("PASS: buffered audio windows emit stabilized partial/final transcript events")
print("PASS: short buffered utterances finalize on flush and repeated finals are not suppressed across utterance boundaries")
print("PASS: duplicate suppression and event timing/RTF reporting work")
print("PASS: local F1-to-ASR service bridge accepts canonical float32 chunks and starts a fresh session after reset")
print("PASS: ASR service flush returns finalized events exactly once with updated status")
