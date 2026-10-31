"""Focused unit tests for Phase F2 buffered ASR adapter (no model download needed)."""
from __future__ import annotations

import sys
from pathlib import Path
import base64
import concurrent.futures
import json
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
    return {"metadata": {}, "audio_path": str(audio)}

def fake_transcribe(_audio, _output, **kwargs):
    transcribe_calls.append(kwargs)
    return {
        "model": "base.en",
        "device": "cuda",
        "device_index": 0,
        "compute_type": "float16",
        "execution_mode": "GPU_REQUIRED",
        "transcription_time_s": 0.1,
        "rtf": 0.1,
    }

with tempfile.TemporaryDirectory() as temp_dir:
    transcript_dir = Path(temp_dir) / "transcript-cache"
    transcript_dir.mkdir()
    transcript_json = transcript_dir / "transcript.json"
    transcript_txt = transcript_dir / "transcript.txt"
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
            Path(temp_dir) / "unused.wav",
            transcript_dir,
            execution_mode="GPU_REQUIRED",
        )
        cache_hit_stages = []
        cached_again = youtube_ingest.transcribe_audio_file(
            Path(temp_dir) / "unused.wav",
            transcript_dir,
            execution_mode="GPU_REQUIRED",
            on_progress=lambda stage, _progress: cache_hit_stages.append(stage),
        )
    assert transcribed["device"] == "cuda" and transcribed["full_text"] == "fresh cuda result"
    assert cached_again == transcribed and cache_hit_stages == ["TRANSCRIBE_CACHE_HIT"]
    assert len(cache_model_instances) == 1 and cache_model_instances[0].transcribe_calls == 1

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
    assert first_job == repeated_job, "Duplicate active YouTube requests created conflicting jobs."
    assert DeferredThread.starts == 1, "Duplicate active YouTube requests created multiple workers."

from run_avatar_viewer import QuietSimpleHTTPRequestHandler
class OriginProbe:
    def __init__(self, origin):
        self.headers = {"Origin": origin} if origin is not None else {}
        self.server = SimpleNamespace(server_port=8000)

assert QuietSimpleHTTPRequestHandler._origin_is_allowed(OriginProbe("http://localhost:8000"))
assert QuietSimpleHTTPRequestHandler._origin_is_allowed(OriginProbe("chrome-extension://" + "a" * 32))
assert not QuietSimpleHTTPRequestHandler._origin_is_allowed(OriginProbe("http://attacker.example"))
assert not QuietSimpleHTTPRequestHandler._origin_is_allowed(OriginProbe("http://localhost:8001"))
assert QuietSimpleHTTPRequestHandler._origin_is_allowed(OriginProbe(None))

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
