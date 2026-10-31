"""Focused unit tests for Phase F2 buffered ASR adapter (no model download needed)."""
from __future__ import annotations

import sys
from pathlib import Path
import base64
import concurrent.futures
import json
import os
import numpy as np
import threading
import tempfile
import time
from types import SimpleNamespace
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
from asr.streaming_asr import FasterWhisperBackend, TranscriptEvent, TranscriptStabilizer
from asr.asr_service import LocalASRService
from asr import gpu_execution
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
try:
    FasterWhisperBackend(
        model_name="must-not-load",
        device="cpu",
        execution_mode="GPU_REQUIRED",
        model_factory=lambda *_args, **_kwargs: (_ for _ in ()).throw(AssertionError("CPU model factory was called")),
    ).start()
except CudaExecutionError:
    pass
else:
    raise AssertionError("A direct FasterWhisperBackend must enforce GPU_REQUIRED against CPU selection.")
try:
    resolve_execution_configuration("CPU_TEST_ONLY", device_index=-1)
except ValueError:
    pass
else:
    raise AssertionError("Negative device indexes must be rejected.")


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

for lifecycle_state in ("paused", "stopped"):
    race_backend = FasterWhisperBackend(
        model_name=f"accept-{lifecycle_state}-race",
        model_factory=model_factory,
        minimum_decode_ms=1000,
    )
    race_backend.start()
    original_asarray = np.asarray

    def transition_before_append(samples, *args, **kwargs):
        with race_backend._lock:
            race_backend.state = lifecycle_state
        return original_asarray(samples, *args, **kwargs)

    with patch("asr.streaming_asr.np.asarray", side_effect=transition_before_append):
        raced_events = race_backend.accept_audio_chunk(
            np.zeros(16000, dtype=np.float32),
            audio_start_ms=0,
            audio_end_ms=1000,
        )
    assert raced_events == [] and race_backend._stream_sample_count == 0, (
        f"Audio was accepted after the backend transitioned to {lifecycle_state}."
    )
    race_backend.stop()

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

class FailSecondWindowModel:
    def __init__(self):
        self.calls = 0
    def transcribe(self, _audio, **_kwargs):
        self.calls += 1
        if self.calls == 2:
            raise RuntimeError("injected finalization failure")
        return [Segment(f" window {self.calls}")], object()

retry_model = FailSecondWindowModel()
retry_backend = FasterWhisperBackend(
    model_name="flush-retry",
    model_factory=lambda *_args, **_kwargs: retry_model,
    minimum_decode_ms=20_000,
    rolling_window_ms=4000,
)
retry_backend.start()
retry_backend.accept_audio_chunk(
    np.zeros(160_000, dtype=np.float32),
    audio_start_ms=1000,
    audio_end_ms=11_000,
)
failed_flush = retry_backend.flush()
assert failed_flush.status == "FAILED_RETRYABLE" and len(failed_flush) == 1, "Flush failure did not report completed-window progress."
assert retry_backend._flush_cursor_samples == 64_000 and retry_backend._stream_sample_count == 160_000, "Failed flush discarded unfinalized audio or replayed a completed window."
retried_flush = retry_backend.flush()
assert retried_flush.status == "COMPLETED" and [event.text for event in retried_flush] == ["window 3", "window 4"], "Retry did not resume at the failed window."
all_final_windows = failed_flush + retried_flush
assert [(event.audio_start_ms, event.audio_end_ms) for event in all_final_windows] == [
    (1000, 5000), (5000, 9000), (9000, 11000)
], "Long utterance finalization lost, overlapped, or duplicated an audio interval."
assert len(retry_backend.samples) == 0 and retry_backend._stream_sample_count == 0, "Successful retry did not release spooled utterance audio."
retry_backend.stop()

async_retry_model = FailSecondWindowModel()
async_retry_backend = FasterWhisperBackend(
    model_name="async-flush-retry",
    model_factory=lambda *_args, **_kwargs: async_retry_model,
    minimum_decode_ms=20_000,
    rolling_window_ms=4000,
    async_worker=True,
)
async_retry_backend.start()
async_retry_backend.accept_audio_chunk(
    np.zeros(160_000, dtype=np.float32),
    audio_start_ms=0,
    audio_end_ms=10_000,
)
async_failed_flush = async_retry_backend.flush()
assert async_failed_flush.status == "FAILED_RETRYABLE" and len(async_failed_flush) == 1
async_success_flush = async_retry_backend.flush()
assert async_success_flush.status == "COMPLETED" and len(async_success_flush) == 2
assert len(async_retry_backend.events) == 3, "Async flush retry emitted a duplicate final event."
async_retry_backend.stop()

class SlowFirstDecodeModel:
    def __init__(self):
        self.calls = 0
        self.decode_started = threading.Event()
        self.release_decode = threading.Event()
    def transcribe(self, _audio, **_kwargs):
        self.calls += 1
        if self.calls == 1:
            self.decode_started.set()
            if not self.release_decode.wait(timeout=4):
                raise TimeoutError("test did not release its slow fake inference")
        return [Segment(f" slow window {self.calls}")], object()

slow_model = SlowFirstDecodeModel()
slow_backend = FasterWhisperBackend(
    model_name="slow-backpressure",
    model_factory=lambda *_args, **_kwargs: slow_model,
    minimum_decode_ms=1000,
    rolling_window_ms=4000,
    async_worker=True,
)
slow_backend.start()
for index in range(10):
    slow_backend.accept_audio_chunk(
        np.zeros(16_000, dtype=np.float32),
        audio_start_ms=index * 1000,
        audio_end_ms=(index + 1) * 1000,
    )
    if index == 0:
        assert slow_model.decode_started.wait(timeout=3), "Slow inference did not start."
assert len(slow_backend.samples) <= 64_000, "Slow inference allowed the in-memory rolling window to grow without bound."
assert slow_backend._stream_sample_count == 160_000, "Slow inference dropped accepted samples from the disk-backed stream."
with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
    flush_future = executor.submit(slow_backend.flush)
    deadline = time.monotonic() + 2
    while not slow_backend._flush_in_progress and time.monotonic() < deadline:
        time.sleep(0.005)
    slow_model.release_decode.set()
    slow_flush = flush_future.result(timeout=6)
assert slow_flush.status == "COMPLETED"
slow_final_intervals = [
    (event.audio_start_ms, event.audio_end_ms)
    for event in slow_flush
    if event.kind == "FINAL_TRANSCRIPT"
]
assert slow_final_intervals == [
    (0, 4000), (4000, 8000), (8000, 10_000)
], f"Backpressure during slow inference lost or duplicated final audio intervals: {slow_final_intervals}"
slow_backend.stop()

timeline_backend = FasterWhisperBackend(
    model_name="timeline-check",
    model_factory=lambda *_args, **_kwargs: ShortUtteranceModel(),
    minimum_decode_ms=1000,
)
timeline_backend.start()
try:
    timeline_backend.accept_audio_chunk(np.zeros(1600, dtype=np.float32), audio_start_ms=0, audio_end_ms=200)
except ValueError:
    pass
else:
    raise AssertionError("Mismatched audio duration/sample count was accepted.")
timeline_backend.accept_audio_chunk(np.zeros(1600, dtype=np.float32), audio_start_ms=0, audio_end_ms=100)
timeline_backend.accept_audio_chunk(np.zeros(1600, dtype=np.float32), audio_start_ms=300, audio_end_ms=400)
assert timeline_backend._stream_sample_count == 6400, "A short silence gap was not represented in the audio timeline."
timeline_backend._audio_spool.flush()
timeline_backend._audio_spool.seek(1600 * 4)
assert not np.frombuffer(timeline_backend._audio_spool.read(3200 * 4), dtype="<f4").any(), "Inserted silence was not zero-filled."
try:
    timeline_backend.accept_audio_chunk(np.zeros(1600, dtype=np.float32), audio_start_ms=350, audio_end_ms=450)
except ValueError:
    pass
else:
    raise AssertionError("Overlapping audio timestamps were accepted.")
try:
    timeline_backend.accept_audio_chunk(np.zeros(1600, dtype=np.float32), audio_start_ms=6400, audio_end_ms=6500)
except ValueError:
    pass
else:
    raise AssertionError("An excessive audio timeline gap was accepted.")
assert timeline_backend._stream_sample_count == 6400, "Rejected audio changed the accepted stream."
timeline_backend.stop()

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
flush_backend.stream_start_ms = 0
flush_backend._stream_sample_count = 1
flush_backend._audio_spool.write(np.ones(1, dtype="<f4").tobytes())
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
    def __init__(self, *_args, **_kwargs):
        self.state = "stopped"; self.model_name = "fake"; self.device = "cpu"; self.compute_type = "int8"
        self.flush_calls = 0; self.start_calls = 0
    def start(self): self.start_calls += 1; self.state = "running"
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
chunk_payload = {
    "samples_base64": base64.b64encode(raw).decode(),
    "audio_start_ms": 100,
    "audio_end_ms": 200,
    "chunk_id": 0,
}
service.accept(chunk_payload)
duration_before_chunk_error = service.audio_duration_ms
try:
    service.accept({**chunk_payload, "audio_start_ms": 200, "audio_end_ms": 300, "chunk_id": 2})
except ValueError:
    pass
else:
    raise AssertionError("Out-of-order chunk_id was accepted.")
assert service.audio_duration_ms == duration_before_chunk_error, "Rejected chunk_id changed audio accounting."
service.accept({**chunk_payload, "audio_start_ms": 200, "audio_end_ms": 300, "chunk_id": 1})

def assert_rejected_audio(payload):
    duration_before = service.audio_duration_ms
    try:
        service.accept(payload)
    except (ValueError, TypeError, RuntimeError):
        pass
    else:
        raise AssertionError(f"Malformed audio payload was accepted: {payload!r}")
    assert service.audio_duration_ms == duration_before, "Rejected payload changed audio accounting."

assert_rejected_audio({"samples_base64": "%%%", "audio_start_ms": 100, "audio_end_ms": 200})
assert_rejected_audio({"samples_base64": base64.b64encode(b"abc").decode(), "audio_start_ms": 100, "audio_end_ms": 200})
assert_rejected_audio({"samples_base64": base64.b64encode(np.array([np.nan], dtype="<f4").tobytes()).decode(), "audio_start_ms": 100, "audio_end_ms": 200})
assert_rejected_audio({"samples_base64": base64.b64encode(np.array([2.0], dtype="<f4").tobytes()).decode(), "audio_start_ms": 100, "audio_end_ms": 200})
assert_rejected_audio({"samples_base64": base64.b64encode(raw).decode(), "audio_start_ms": float("nan"), "audio_end_ms": 200})
assert_rejected_audio({"samples_base64": base64.b64encode(raw).decode(), "audio_start_ms": 200, "audio_end_ms": 200})
assert_rejected_audio([])
service.control("pause")
assert_rejected_audio({"samples_base64": base64.b64encode(raw).decode(), "audio_start_ms": 100, "audio_end_ms": 200})
service.control("resume")

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

service_start_count = service.backend.start_calls
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
    starts = list(executor.map(
        lambda _index: service.start(model="fake", execution_mode="CPU_TEST_ONLY"),
        range(16),
    ))
assert all(start["state"] == "running" for start in starts)
assert service.backend.start_calls == service_start_count, "Concurrent idempotent starts restarted the backend."
try:
    service.start(model="different", execution_mode="CPU_TEST_ONLY")
except RuntimeError:
    pass
else:
    raise AssertionError("A running service must reject silent model/execution reconfiguration.")
assert service.control("stop")["audio_duration_ms"] == 0, "Stopping ASR retained prior stream accounting."
assert service.start(model="fake", execution_mode="CPU_TEST_ONLY")["state"] == "running"
response = service.accept({"samples_base64": base64.b64encode(raw).decode(), "audio_start_ms": 0, "audio_end_ms": 100})
assert response["status"]["audio_duration_ms"] == 100, "Restart after stop retained stale stream data."

class RecoverableModel:
    def __init__(self):
        self.calls = 0
        self.call_events = [threading.Event(), threading.Event(), threading.Event()]
    def transcribe(self, _audio, **_kwargs):
        self.calls += 1
        self.call_events[min(self.calls - 1, 2)].set()
        if self.calls == 1:
            raise RuntimeError("injected inference failure")
        return [Segment(f" recovered {self.calls}")], object()

recoverable_model = RecoverableModel()
worker_backend_ref = []
def failing_callback(_event):
    worker_backend_ref[0].queue_size
    raise RuntimeError("injected callback failure")

worker_backend = FasterWhisperBackend(
    model_name="failure-injection",
    model_factory=lambda *_args, **_kwargs: recoverable_model,
    minimum_decode_ms=1000,
    decode_hop_ms=100,
    async_worker=True,
    on_event=failing_callback,
)
worker_backend_ref.append(worker_backend)
worker_backend.start()
for index in range(3):
    worker_backend.accept_audio_chunk(
        np.zeros(16000, dtype=np.float32),
        audio_start_ms=index * 1000,
        audio_end_ms=(index + 1) * 1000,
    )
    assert recoverable_model.call_events[index].wait(timeout=3), "ASR worker stopped after an injected failure."
    deadline = time.monotonic() + 3
    while worker_backend.worker_state != "IDLE" and time.monotonic() < deadline:
        time.sleep(0.01)
    assert worker_backend.worker_state == "IDLE", "ASR worker did not return to IDLE after inference."
    assert worker_backend._worker_thread and worker_backend._worker_thread.is_alive(), "ASR worker thread exited unexpectedly."
    assert worker_backend.queue_size >= 0, "ASR callback-safe status query failed."
    if index == 0:
        assert "transcription failed" in worker_backend.last_error, "Inference failure was not exposed in backend status."
assert "callback failed" in worker_backend.last_error, "Callback failure was not exposed in backend status."
assert recoverable_model.calls == 3, "ASR worker did not recover and process later windows."
worker_backend.stop()

created_shared_models = []
def shared_model_factory(*_args, **_kwargs):
    model = object()
    created_shared_models.append(model)
    return model
old_model_cache = gpu_execution._model_cache.copy()
gpu_execution._model_cache.clear()
try:
    with patch.dict(sys.modules, {"faster_whisper": SimpleNamespace(WhisperModel=shared_model_factory)}):
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
            shared = list(executor.map(
                lambda _index: gpu_execution.get_shared_whisper_model(
                    "concurrent-test", device="cpu", compute_type="int8"
                ),
                range(16),
            ))
finally:
    gpu_execution._model_cache.clear()
    gpu_execution._model_cache.update(old_model_cache)
assert len({id(model) for model, _lock in shared}) == 1, "Concurrent jobs created duplicate shared model instances."
assert all(lock is shared[0][1] for _model, lock in shared), "Shared model callers did not share its inference lock."
assert len(created_shared_models) == 1, "Shared model cache constructed duplicate model instances."

from youtube_pipeline import youtube_ingest

cache_config = {
    "device": "cuda",
    "device_index": 0,
    "compute_type": "float16",
    "fallback_reason": None,
}
cached_pipeline_result = {
    "status": "READY",
    "transcript": {
        "model": "base.en",
        "device": "cpu",
        "device_index": None,
        "compute_type": "int8",
        "execution_mode": "CPU_TEST_ONLY",
    },
}
transcribe_calls = []
def fake_download(_url, output_dir, **_kwargs):
    audio = Path(output_dir) / "fake.wav"
    audio.write_bytes(b"test-audio-content")
    return {
        "metadata": {
            "video_id": "abcdefghijk",
            "audio_sha256": youtube_ingest._sha256_file(audio),
        },
        "audio_path": str(audio),
    }

def fake_transcribe(_audio, _output, **kwargs):
    transcribe_calls.append(kwargs)
    return {
        "model": "base.en",
        "device": "cuda",
        "device_index": 0,
        "compute_type": "float16",
        "execution_mode": "GPU_REQUIRED",
        "segments": [],
        "full_text": "fresh cuda result",
        "transcription_time_s": 0.1,
        "rtf": 0.1,
    }

with tempfile.TemporaryDirectory() as temp_dir:
    transcript_dir = Path(temp_dir) / "transcript-cache"
    transcript_dir.mkdir()
    transcript_json = transcript_dir / "transcript.json"
    transcript_txt = transcript_dir / "transcript.txt"
    audio_file = Path(temp_dir) / "unused.wav"
    audio_file.write_bytes(b"stable audio bytes")
    transcript_json.write_text(json.dumps({
        "model": "base.en",
        "device": "cpu",
        "device_index": None,
        "compute_type": "int8",
        "execution_mode": "CPU_TEST_ONLY",
        "segments": [],
        "full_text": "old cpu cache",
    }), encoding="utf-8")
    transcript_txt.write_text("old cpu cache\n", encoding="utf-8")
    cache_model_instances = []
    class CachedTranscriptModel:
        def __init__(self, *_args, **_kwargs):
            self.transcribe_calls = 0
            cache_model_instances.append(self)
        def transcribe(self, *_args, **_kwargs):
            self.transcribe_calls += 1
            return (
                [SimpleNamespace(text=" fresh cuda result", start=0.0, end=1.0, avg_logprob=-0.2)],
                SimpleNamespace(duration=1.0, language="en"),
            )

    with patch.object(youtube_ingest, "resolve_execution_configuration", return_value=cache_config), \
         patch.dict(sys.modules, {"faster_whisper": SimpleNamespace(WhisperModel=CachedTranscriptModel)}):
        transcribed = youtube_ingest.transcribe_audio_file(
            audio_file,
            transcript_dir,
            execution_mode="GPU_REQUIRED",
        )
        cache_hit_stages = []
        cached_again = youtube_ingest.transcribe_audio_file(
            audio_file,
            transcript_dir,
            execution_mode="GPU_REQUIRED",
            on_progress=lambda stage, _progress: cache_hit_stages.append(stage),
        )
    assert transcribed["device"] == "cuda" and transcribed["full_text"] == "fresh cuda result"
    assert cached_again == transcribed and cache_hit_stages == ["TRANSCRIBE_CACHE_HIT"]
    assert len(cache_model_instances) == 1 and cache_model_instances[0].transcribe_calls == 1
    audio_file.write_bytes(b"changed audio bytes")
    changed_audio = youtube_ingest.transcribe_audio_file(
        audio_file,
        transcript_dir,
        execution_mode="GPU_REQUIRED",
    )
    assert changed_audio["full_text"] == transcribed["full_text"] and changed_audio["audio_sha256"] != transcribed["audio_sha256"]
    assert cache_model_instances[0].transcribe_calls == 2, "Changed audio incorrectly reused a stale transcript cache."

translation_calls = []
def fake_translation_bridge(*_args, **_kwargs):
    translation_calls.append(True)
    return SimpleNamespace(stdout="[]", stderr="")

translation_input = {"segments": [{"start": 0.0, "end": 1.0, "text": "hello"}]}
with tempfile.TemporaryDirectory() as temp_dir:
    translation_dir = Path(temp_dir)
    with patch.object(youtube_ingest, "_translation_implementation_hash", return_value="sign-catalog-v1"), \
         patch.object(youtube_ingest.subprocess, "run", side_effect=fake_translation_bridge):
        youtube_ingest.segment_and_translate(translation_input, translation_dir)
        youtube_ingest.segment_and_translate(translation_input, translation_dir)
    assert len(translation_calls) == 1, "Identical translation input did not hit its content-addressed cache."
    with patch.object(youtube_ingest, "_translation_implementation_hash", return_value="sign-catalog-v2"), \
         patch.object(youtube_ingest.subprocess, "run", side_effect=fake_translation_bridge):
        youtube_ingest.segment_and_translate(translation_input, translation_dir)
    assert len(translation_calls) == 2, "Changed sign catalog identity reused a stale translation cache."
    changed_translation_input = {"segments": [{"start": 0.0, "end": 1.0, "text": "good morning"}]}
    with patch.object(youtube_ingest, "_translation_implementation_hash", return_value="sign-catalog-v2"), \
         patch.object(youtube_ingest.subprocess, "run", side_effect=fake_translation_bridge):
        youtube_ingest.segment_and_translate(changed_translation_input, translation_dir)
    assert len(translation_calls) == 3, "Changed transcript input reused a stale translation cache."

with tempfile.TemporaryDirectory() as temp_dir:
    video_dir = Path(temp_dir) / "abcdefghijk"
    video_dir.mkdir()
    (video_dir / "pipeline_result.json").write_text(
        json.dumps(cached_pipeline_result),
        encoding="utf-8",
    )
    with patch.object(youtube_ingest, "resolve_execution_configuration", return_value=cache_config), \
         patch.object(youtube_ingest, "download_youtube_audio", side_effect=fake_download), \
         patch.object(youtube_ingest, "transcribe_audio_file", side_effect=fake_transcribe), \
         patch.object(youtube_ingest, "segment_and_translate", return_value={}):
        result = youtube_ingest.process_youtube_video(
            "https://www.youtube.com/watch?v=abcdefghijk",
            output_base_dir=Path(temp_dir),
        )
    assert len(transcribe_calls) == 1, "Pipeline cache with CPU provenance bypassed GPU_REQUIRED transcription."
    assert result["transcript"]["device"] == "cuda", "Mismatched pipeline cache was not replaced."

class DeferredThread:
    starts = 0
    def __init__(self, **_kwargs): pass
    def start(self): type(self).starts += 1

with tempfile.TemporaryDirectory() as temp_dir:
    manager = youtube_ingest.YouTubeJobManager(output_base_dir=Path(temp_dir))
    with patch.object(youtube_ingest.threading, "Thread", DeferredThread):
        first_job = manager.submit_job("https://www.youtube.com/watch?v=abcdefghijk")
        repeated_job = manager.submit_job("https://youtu.be/abcdefghijk", force=True)
        second_job = manager.submit_job("https://www.youtube.com/watch?v=123456789ab")
    assert first_job == repeated_job, "Duplicate active YouTube requests created conflicting jobs."
    assert DeferredThread.starts == 2, "Duplicate active YouTube requests created multiple workers."
    try:
        manager.submit_job("https://www.youtube.com/watch?v=ZYXWVUTSRQP")
    except RuntimeError:
        pass
    else:
        raise AssertionError("YouTube job manager exceeded its active-worker limit.")
    manager.JOB_HISTORY_LIMIT = 2
    with manager._lock:
        manager.jobs["old-completed"] = {"stage": "READY", "finished_at": 1, "started_at": 0}
        manager.jobs["newer-completed"] = {"stage": "ERROR", "finished_at": 2, "started_at": 1}
        manager.jobs["newest-completed"] = {"stage": "READY", "finished_at": 3, "started_at": 2}
        manager._prune_jobs_locked()
    assert "old-completed" not in manager.jobs and "newest-completed" in manager.jobs
    assert first_job in manager.jobs and second_job in manager.jobs, "Job pruning removed active job state."

class ImmediateThread:
    def __init__(self, *, target, args, **_kwargs):
        self.target, self.args = target, args
    def start(self):
        self.target(*self.args)

with tempfile.TemporaryDirectory() as temp_dir:
    manager = youtube_ingest.YouTubeJobManager(output_base_dir=Path(temp_dir))
    result_payload = {"status": "READY", "metadata": {"title": "durable job result"}}
    with patch.object(youtube_ingest.threading, "Thread", ImmediateThread), \
         patch.object(youtube_ingest, "process_youtube_video", return_value=result_payload):
        job_id = manager.submit_job("https://www.youtube.com/watch?v=abcdefghijk")
    assert manager.jobs[job_id]["result"] is None, "Completed job retained the full result in memory."
    assert manager.get_status(job_id)["title"] == "durable job result"
    assert manager.get_result(job_id) == result_payload, "Completed job result was not recoverable from disk."
    manager.JOB_HISTORY_LIMIT = 0
    with manager._lock:
        manager._prune_jobs_locked()
    assert manager.get_status(job_id) is None
    assert manager.get_result(job_id) == result_payload, "Pruned job result was not retrievable from its durable artifact."

from run_avatar_viewer import (
    PROJECT_ROOT as VIEWER_PROJECT_ROOT,
    QuietSimpleHTTPRequestHandler,
    save_sign_definition,
    validate_sign_definition,
)
class OriginProbe:
    _request_host_is_local = QuietSimpleHTTPRequestHandler._request_host_is_local

    def __init__(self, origin):
        self.headers = {"Origin": origin} if origin is not None else {}
        self.headers["Host"] = "localhost:8000"
        self.server = SimpleNamespace(server_port=8000)

assert QuietSimpleHTTPRequestHandler._origin_is_allowed(OriginProbe("http://localhost:8000"))
with patch.dict(os.environ, {"SIGN_ALLOWED_EXTENSION_ID": "a" * 32}):
    assert QuietSimpleHTTPRequestHandler._origin_is_allowed(OriginProbe("chrome-extension://" + "a" * 32))
    assert not QuietSimpleHTTPRequestHandler._origin_is_allowed(OriginProbe("chrome-extension://" + "b" * 32))
assert not QuietSimpleHTTPRequestHandler._origin_is_allowed(OriginProbe("http://attacker.example"))
assert not QuietSimpleHTTPRequestHandler._origin_is_allowed(OriginProbe("http://localhost:8001"))
assert QuietSimpleHTTPRequestHandler._origin_is_allowed(OriginProbe(None))
host_spoof = OriginProbe(None)
host_spoof.headers["Host"] = "attacker.example:8000"
assert not QuietSimpleHTTPRequestHandler._origin_is_allowed(host_spoof), "A hostile Host header bypassed loopback request validation."

from io import BytesIO
response_headers = object.__new__(QuietSimpleHTTPRequestHandler)
response_headers._headers_buffer = []
response_headers.wfile = BytesIO()
response_headers.request_version = "HTTP/1.1"
QuietSimpleHTTPRequestHandler.end_headers(response_headers)
assert b"Access-Control-Allow-Origin" not in response_headers.wfile.getvalue()

class BodyProbe:
    _read_body = QuietSimpleHTTPRequestHandler._read_body
    def __init__(self, body):
        from io import BytesIO
        self.headers = {"Content-Length": str(len(body))}
        self.rfile = BytesIO(body)

large_sign_body = json.dumps({"sign_id": "large_sign", "payload": "x" * 20_000}).encode()
parsed_large_sign = QuietSimpleHTTPRequestHandler._read_json_body(BodyProbe(large_sign_body), 1_048_576)
assert parsed_large_sign["sign_id"] == "large_sign", "The sign authoring API rejected valid large sign definitions."

valid_sign = json.loads((VIEWER_PROJECT_ROOT / "signs" / "add.json").read_text(encoding="utf-8"))
validate_sign_definition(valid_sign)
playable_sign_count = 0
for existing_sign_path in sorted((VIEWER_PROJECT_ROOT / "signs").glob("*.json")):
    if existing_sign_path.name == "manifest.json":
        continue
    existing_definition = json.loads(existing_sign_path.read_text(encoding="utf-8"))
    if existing_definition.get("motion", {}).get("status") != "playable":
        continue
    validate_sign_definition(existing_definition)
    playable_sign_count += 1
assert playable_sign_count > 0, "No existing playable sign definitions were validated."
with tempfile.TemporaryDirectory() as temp_dir:
    sign_definition = json.loads(json.dumps(valid_sign))
    sign_definition["sign_id"] = "h33_test_sign"
    saved_sign = save_sign_definition(Path(temp_dir), sign_definition)
    original_saved_text = saved_sign.read_text(encoding="utf-8")
    try:
        save_sign_definition(Path(temp_dir), sign_definition)
    except FileExistsError:
        pass
    else:
        raise AssertionError("Saving an existing sign silently overwrote it.")
    assert saved_sign.read_text(encoding="utf-8") == original_saved_text, "Rejected overwrite changed the existing sign."
    sign_definition["metadata"]["display_name"] = "Updated test sign"
    save_sign_definition(Path(temp_dir), sign_definition, allow_overwrite=True)
    assert json.loads(saved_sign.read_text(encoding="utf-8"))["metadata"]["display_name"] == "Updated test sign"
invalid_sign = json.loads(json.dumps(valid_sign))
invalid_sign["motion"]["keyframes"][0]["rotations"]["Bip001_R_Hand"]["x"] = float("nan")
try:
    validate_sign_definition(invalid_sign)
except ValueError:
    pass
else:
    raise AssertionError("Sign schema accepted a non-finite pose value.")

print("PASS: GPU_REQUIRED backend rejects direct CPU selection and invalid CUDA indexes.")
print("PASS: concurrent service starts are idempotent and reject incompatible reconfiguration.")
print("PASS: malformed, non-finite, oversized-amplitude, and invalid-timestamp audio is rejected without accounting changes.")
print("PASS: asynchronous inference and callback failures remain visible while the worker recovers.")
print("PASS: concurrent ASR callers share one model and serialized inference lock.")
print("PASS: transcript cache provenance enforces GPU mode and reuses matching CUDA results.")
print("PASS: stale YouTube pipeline cache cannot bypass requested GPU execution provenance.")
print("PASS: duplicate active YouTube jobs reuse a single worker without corrupting shared output paths.")
print("PASS: local viewer rejects remote origins and permits only local runtime or extension callers.")
print("PASS: local sign authoring retains the supported large JSON payload size.")
print("PASS: ASR backend lifecycle loads once, resets cleanly, and restarts without stale transcript state")
print("PASS: buffered audio windows emit stabilized partial/final transcript events")
print("PASS: short buffered utterances finalize on flush and repeated finals are not suppressed across utterance boundaries")
print("PASS: duplicate suppression and event timing/RTF reporting work")
print("PASS: local F1-to-ASR service bridge accepts canonical float32 chunks and starts a fresh session after reset")
print("PASS: ASR service flush returns finalized events exactly once with updated status")
print("PASS: ASR finalization retries resume from the first failed chunk without losing or duplicating intervals")
print("PASS: ASR timeline validation rejects sample-duration mismatches and discontinuous chunks")
print("PASS: exact extension origin and local Host checks reject untrusted browser callers")
print("PASS: sign authoring validates motion schema and saves atomically without implicit overwrite")
import resource_preflight
with patch.object(resource_preflight, "_available_memory_bytes", return_value=8 * 1024 ** 3), \
     patch.object(resource_preflight, "_cuda_memory", return_value={"available": True, "devices": [{"free_mib": 4096, "total_mib": 6144}]}), \
     patch.object(resource_preflight.shutil, "disk_usage", return_value=SimpleNamespace(free=20 * 1024 ** 3)):
    assert resource_preflight.run_preflight(audio_seconds=3600, output_dir=Path("."))["status"] == "SAFE"
with patch.object(resource_preflight, "_available_memory_bytes", return_value=1 * 1024 ** 3), \
     patch.object(resource_preflight, "_cuda_memory", return_value={"available": True, "devices": [{"free_mib": 4096, "total_mib": 6144}]}), \
     patch.object(resource_preflight.shutil, "disk_usage", return_value=SimpleNamespace(free=20 * 1024 ** 3)):
    assert resource_preflight.run_preflight(audio_seconds=3600, output_dir=Path("."))["status"] == "BLOCKED"
print("PASS: read-only resource preflight enforces memory, disk, and CUDA thresholds.")
