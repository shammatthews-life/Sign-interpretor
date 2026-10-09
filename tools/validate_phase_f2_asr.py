"""Focused unit tests for Phase F2 buffered ASR adapter (no model download needed)."""
from __future__ import annotations

import sys
from pathlib import Path
import base64
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from asr.streaming_asr import FasterWhisperBackend, TranscriptStabilizer
from asr.asr_service import LocalASRService


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

stabilizer = TranscriptStabilizer()
assert stabilizer.partial(" hello ") == "hello"
assert stabilizer.partial("hello") is None
assert stabilizer.final("hello") == "hello"
assert stabilizer.final("hello") is None

class ServiceBackend:
    def __init__(self, *_args, **_kwargs): self.state = "stopped"; self.model_name = "fake"; self.device = "cpu"; self.compute_type = "int8"
    def start(self): self.state = "running"
    def accept_audio_chunk(self, _samples, **_kwargs): return []
    def pause(self): self.state = "paused"
    def resume(self): self.state = "running"
    def flush(self): return []
    def stop(self): self.state = "stopped"
    def reset(self): self.state = "stopped"

service = LocalASRService(ServiceBackend)
assert service.start(model="fake")["state"] == "running"
raw = np.zeros(1600, dtype="<f4").tobytes()
response = service.accept({"samples_base64": base64.b64encode(raw).decode(), "audio_start_ms": 0, "audio_end_ms": 100})
assert response["status"]["audio_duration_ms"] == 100, "F1-to-ASR service bridge did not account for canonical chunk."
assert service.control("pause")["state"] == "paused"
assert service.control("reset")["audio_duration_ms"] == 0

print("PASS: ASR backend lifecycle loads the model once and resets cleanly")
print("PASS: buffered audio windows emit stabilized partial/final transcript events")
print("PASS: duplicate suppression and event timing/RTF reporting work")
print("PASS: local F1-to-ASR service bridge accepts canonical float32 chunks")
