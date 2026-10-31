"""Replaceable buffered streaming-ASR interfaces and faster-whisper adapter.

Phase F2.5 enhancements:
- CUDA / GPU acceleration support with automatic DLL discovery on Windows
- Decoupled asynchronous ASR worker thread preventing audio ingestion blocking
- Stale-window policy: collapses accumulated intermediate hops into the newest valid window
- Diagnostic metrics: worker state, queue size, backlog, RTF, and latency tracking
"""
from __future__ import annotations

import os
import sys
import tempfile
import threading
from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict
from time import perf_counter
from typing import Callable, Iterable, Optional

import numpy as np

from .gpu_execution import (
    ExecutionMode,
    get_shared_whisper_model,
    resolve_execution_configuration,
    verify_nvidia_cuda,
)


@dataclass
class TranscriptEvent:
    kind: str  # PARTIAL_TRANSCRIPT | FINAL_TRANSCRIPT
    text: str
    audio_start_ms: float
    audio_end_ms: float
    asr_started_at_ms: float
    asr_finished_at_ms: float
    emitted_at_ms: float
    confidence: Optional[float] = None
    backlog_dropped: int = 0

    @property
    def audio_duration_ms(self) -> float:
        return self.audio_end_ms - self.audio_start_ms

    @property
    def compute_ms(self) -> float:
        return self.asr_finished_at_ms - self.asr_started_at_ms

    @property
    def rtf(self) -> float:
        return self.compute_ms / max(1.0, self.audio_duration_ms)

    def report(self) -> dict:
        data = asdict(self)
        data.update(audio_duration_ms=self.audio_duration_ms, compute_ms=self.compute_ms, rtf=self.rtf)
        return data


class FlushResult(list[TranscriptEvent]):
    """List-compatible flush result with an explicit completion outcome."""

    def __init__(self, events=(), *, status: str = "COMPLETED", error: Optional[str] = None) -> None:
        super().__init__(events)
        self.status = status
        self.error = error


class StreamingASRBackend(ABC):
    """Backend contract; callers never depend on WhisperModel internals."""

    @abstractmethod
    def start(self) -> None: ...
    @abstractmethod
    def accept_audio_chunk(self, samples: np.ndarray, *, audio_start_ms: float, audio_end_ms: float) -> list[TranscriptEvent]: ...
    @abstractmethod
    def pause(self) -> None: ...
    @abstractmethod
    def resume(self) -> None: ...
    @abstractmethod
    def flush(self) -> list[TranscriptEvent]: ...
    @abstractmethod
    def stop(self) -> None: ...
    @abstractmethod
    def reset(self) -> None: ...


class TranscriptStabilizer:
    """Suppresses unchanged partials while retaining semantically final events."""

    def __init__(self) -> None:
        self.last_partial = ""
        self.last_final = ""

    @staticmethod
    def normalize(text: str) -> str:
        return " ".join(text.strip().split())

    def partial(self, text: str) -> Optional[str]:
        text = self.normalize(text)
        if not text or text == self.last_partial or text == self.last_final:
            return None
        self.last_partial = text
        return text

    def final(self, text: str) -> Optional[str]:
        text = self.normalize(text)
        if not text or text == self.last_final:
            return None
        self.last_final = text
        self.last_partial = text
        return text

    def reset(self) -> None:
        self.last_partial = self.last_final = ""


class FasterWhisperBackend(StreamingASRBackend):
    """CPU/GPU configurable faster-whisper adapter with bounded rolling buffer

    Supports both synchronous processing (async_worker=False) for batch benchmarks
    and asynchronous threaded execution (async_worker=True) for real-time streaming.
    Under asynchronous execution, audio ingestion is decoupled from Whisper inference:
    the worker decodes the newest rolling window when ready, collapsing any stale intermediate
    triggers into the current window to prevent backlog accumulation.
    """
    MAX_STREAM_DURATION_MS = 15 * 60 * 1000
    MAX_IMPLICIT_SILENCE_GAP_MS = 5000

    def __init__(
        self,
        model_name: str = "tiny.en",
        *,
        device: str = "cpu",
        compute_type: str = "int8",
        sample_rate: int = 16000,
        minimum_decode_ms: int = 1000,
        decode_hop_ms: int = 750,
        rolling_window_ms: int = 4000,
        model_factory: Optional[Callable[..., object]] = None,
        on_event: Optional[Callable[[TranscriptEvent], None]] = None,
        async_worker: bool = False,
        device_index: int = 0,
        execution_mode: ExecutionMode | None = None,
    ) -> None:
        self.model_name = model_name
        self.device = device
        self.compute_type = compute_type
        self.device_index = device_index
        self.execution_mode = execution_mode
        self.sample_rate = sample_rate
        self.minimum_decode_ms = minimum_decode_ms
        self.decode_hop_ms = decode_hop_ms
        self.rolling_window_ms = rolling_window_ms
        self.model_factory = model_factory
        self.on_event = on_event
        self.async_worker = async_worker

        self.model = None
        self.state = "stopped"
        self._worker_state = "IDLE"
        self.samples = np.empty(0, dtype=np.float32)
        self.buffer_start_ms: Optional[float] = None
        self.buffer_end_ms: Optional[float] = None
        self.stream_start_ms: Optional[float] = None
        self._stream_sample_count = 0
        self._flush_cursor_samples = 0
        self._audio_spool = tempfile.TemporaryFile(mode="w+b")
        self.last_decode_end_ms: Optional[float] = None
        self.last_decode_ms: Optional[float] = None
        self.last_rtf: Optional[float] = None

        self.stabilizer = TranscriptStabilizer()
        self.events: list[TranscriptEvent] = []
        self._completed_events: list[TranscriptEvent] = []
        self._pending_decode_count = 0
        self._stale_windows_dropped = 0

        # Thread synchronization for async_worker
        self._lock = threading.Lock()
        self._worker_trigger = threading.Event()
        self._stop_event = threading.Event()
        self._flush_requested = threading.Event()
        self._flush_completed = threading.Event()
        self._worker_thread: Optional[threading.Thread] = None
        self._lifecycle_lock = threading.RLock()
        self._inference_lock = threading.Lock()
        self._flush_in_progress = False
        self._flush_result_events: list[TranscriptEvent] = []
        self._flush_error: Optional[str] = None
        self._last_inference_succeeded = False
        self.last_error: Optional[str] = None

    @property
    def worker_state(self) -> str:
        if self.state != "running":
            return "STOPPED"
        return self._worker_state

    @property
    def queue_size(self) -> int:
        with self._lock:
            return round(len(self.samples) / max(1, self.sample_rate * 0.1))

    @property
    def backlog(self) -> int:
        with self._lock:
            return self._pending_decode_count

    @property
    def stale_windows_dropped(self) -> int:
        with self._lock:
            return self._stale_windows_dropped

    def start(self) -> None:
        with self._lifecycle_lock:
            if self.async_worker and self._worker_thread and self._worker_thread.is_alive():
                raise RuntimeError("The previous ASR worker is still stopping; retry after it exits.")
            if self.state == "running":
                return
            if self.state == "paused":
                raise RuntimeError("ASR is paused; call resume() instead of start().")

            if self.execution_mode is not None:
                resolved = resolve_execution_configuration(
                    self.execution_mode,
                    device=self.device,
                    device_index=self.device_index,
                    compute_type=self.compute_type,
                )
                self.device = resolved["device"]
                self.compute_type = resolved["compute_type"]
                self.device_index = resolved["device_index"] or 0
            elif self.device == "cuda":
                verify_nvidia_cuda(self.device_index, self.compute_type)

            if self.model is None:
                model_options: dict[str, object] = {
                    "device": self.device,
                    "compute_type": self.compute_type,
                }
                if self.device == "cuda":
                    model_options["device_index"] = self.device_index
                if self.model_factory:
                    self.model = self.model_factory(self.model_name, **model_options)
                else:
                    self.model, self._inference_lock = get_shared_whisper_model(
                        self.model_name,
                        device=self.device,
                        compute_type=self.compute_type,
                        device_index=self.device_index if self.device == "cuda" else None,
                    )

            self.state = "running"
            self._worker_state = "IDLE"
            self.last_error = None

            if self.async_worker:
                self._worker_thread = None
                self._stop_event.clear()
                self._worker_trigger.clear()
                self._flush_requested.clear()
                self._flush_completed.clear()
                self._worker_thread = threading.Thread(
                    target=self._worker_loop, daemon=True, name="ASRWorkerThread"
                )
                self._worker_thread.start()

    def pause(self) -> None:
        with self._lock:
            if self.state == "running":
                self.state = "paused"

    def resume(self) -> None:
        with self._lock:
            if self.state == "paused":
                self.state = "running"

    def stop(self) -> None:
        with self._lifecycle_lock:
            with self._lock:
                self.state = "stopped"
                self._worker_state = "STOPPED"
            if self.async_worker and self._worker_thread and self._worker_thread.is_alive():
                self._stop_event.set()
                self._worker_trigger.set()
                self._worker_thread.join(timeout=5.0)
                if self._worker_thread.is_alive():
                    raise TimeoutError("ASR worker did not stop within 5 seconds; session reset is incomplete.")
                self._worker_thread = None
            with self._inference_lock:
                with self._lock:
                    self._reset_utterance_locked()
                    self._completed_events.clear()
                    self._flush_in_progress = False
                    self._flush_requested.clear()
                    self._flush_completed.clear()

    def reset(self) -> None:
        with self._lifecycle_lock:
            self.stop()
            with self._lock:
                self._reset_utterance_locked()
                self.last_decode_end_ms = None
                self.last_decode_ms = self.last_rtf = None
                self.events = []
                self._completed_events.clear()
                self._stale_windows_dropped = 0
                self._worker_state = "IDLE"
                self.last_error = None

    def accept_audio_chunk(self, samples: np.ndarray, *, audio_start_ms: float, audio_end_ms: float) -> list[TranscriptEvent]:
        if self.state != "running":
            return []
        data = np.asarray(samples, dtype=np.float32).reshape(-1)
        if not len(data):
            return []
        if not np.isfinite(data).all():
            raise ValueError("Audio samples must all be finite.")
        if not np.isfinite(audio_start_ms) or not np.isfinite(audio_end_ms) or audio_start_ms < 0 or audio_end_ms <= audio_start_ms:
            raise ValueError("Audio timestamps must be finite, non-negative, and increasing.")
        expected_duration_ms = len(data) * 1000 / self.sample_rate
        if abs((audio_end_ms - audio_start_ms) - expected_duration_ms) > max(2.0, 1000 / self.sample_rate):
            raise ValueError("Audio timestamps do not match the sample count and configured sample rate.")

        with self._lock:
            if self.state != "running":
                return []
            if self._flush_in_progress:
                raise RuntimeError("Cannot accept audio while a flush is in progress.")
            if self.buffer_end_ms is not None:
                gap_ms = audio_start_ms - self.buffer_end_ms
                tolerance_ms = max(2.0, 1000 / self.sample_rate)
                if gap_ms < -tolerance_ms:
                    raise ValueError("Audio chunk overlaps previously accepted audio or is out of order.")
                if gap_ms > tolerance_ms:
                    if gap_ms > self.MAX_IMPLICIT_SILENCE_GAP_MS:
                        raise ValueError("Audio timeline gap exceeds 5 seconds; flush the current utterance before resuming.")
                    gap_samples = round(gap_ms * self.sample_rate / 1000)
                    if (self._stream_sample_count + gap_samples + len(data)) * 1000 / self.sample_rate > self.MAX_STREAM_DURATION_MS:
                        raise BufferError("ASR utterance reached its 15-minute limit; flush before sending more audio.")
                    silence = np.zeros(gap_samples, dtype="<f4")
                    self._audio_spool.seek(0, os.SEEK_END)
                    self._audio_spool.write(silence.tobytes())
                    self._stream_sample_count += gap_samples
                    self.samples = np.concatenate((self.samples, silence))
            if (self._stream_sample_count + len(data)) * 1000 / self.sample_rate > self.MAX_STREAM_DURATION_MS:
                raise BufferError("ASR utterance reached its 15-minute limit; flush before sending more audio.")
            if self.buffer_start_ms is None:
                self.buffer_start_ms = audio_start_ms
                self.stream_start_ms = audio_start_ms
            self._audio_spool.seek(0, os.SEEK_END)
            self._audio_spool.write(np.asarray(data, dtype="<f4").tobytes())
            self._stream_sample_count += len(data)
            self.buffer_end_ms = audio_end_ms
            self.samples = np.concatenate((self.samples, data))
            self._trim_window()

            duration_ms = len(self.samples) * 1000 / self.sample_rate
            due = self.last_decode_end_ms is None or (audio_end_ms - self.last_decode_end_ms >= self.decode_hop_ms)
            should_decode = duration_ms >= self.minimum_decode_ms and due

            if self.async_worker:
                if should_decode:
                    if self._worker_state == "DECODING":
                        # Stale window policy: decode request arrived while worker is busy;
                        # track accumulated backlog but do not spawn queued decodes
                        self._pending_decode_count += 1
                    else:
                        self._worker_trigger.set()
                # Return any events produced by the background worker since last call
                returned = list(self._completed_events)
                self._completed_events.clear()
                return returned
            else:
                # Synchronous execution mode (for deterministic unit tests & batch benchmarks)
                if should_decode:
                    return self._decode(final=False)
                return []

    def flush(self) -> FlushResult:
        if self.state != "running":
            return FlushResult()

        if self.async_worker:
            with self._lock:
                if self._stream_sample_count == 0:
                    return FlushResult()
                if self._flush_in_progress:
                    if not self._flush_completed.is_set():
                        raise RuntimeError("An ASR flush is already in progress.")
                else:
                    self._flush_in_progress = True
                    self._flush_error = None
                    self._flush_result_events.clear()
                    self._flush_completed.clear()
                    self._flush_requested.set()
                    self._worker_trigger.set()

            # Wait for background worker to finalize the flush
            if not self._flush_completed.wait(timeout=5.0):
                self.last_error = "ASR worker did not complete flush within 5 seconds."
                raise TimeoutError("ASR worker did not complete flush within 5 seconds.")

            with self._lock:
                returned = list(self._completed_events) + list(self._flush_result_events)
                self._completed_events.clear()
                status = "FAILED_RETRYABLE" if self._flush_error else "COMPLETED"
                error = self._flush_error
                self._flush_result_events.clear()
                self._flush_in_progress = False
                self._flush_completed.clear()
                if status == "COMPLETED":
                    self._reset_utterance_locked()
                return FlushResult(returned, status=status, error=error)
        else:
            with self._lock:
                if not self._stream_sample_count:
                    return FlushResult()
                if self._flush_in_progress:
                    raise RuntimeError("An ASR flush is already in progress.")
                self._flush_in_progress = True
                self._flush_cursor_samples = min(self._flush_cursor_samples, self._stream_sample_count)

            events: list[TranscriptEvent] = []
            error = None
            while True:
                try:
                    with self._lock:
                        window_samples, start_ms, end_ms = self._next_flush_window_locked()
                except OSError as exc:
                    error = str(exc)
                    break
                if window_samples is None:
                    break
                event = self._run_transcribe(window_samples, start_ms=start_ms, end_ms=end_ms, final=True)
                if not self._last_inference_succeeded:
                    error = self.last_error or "ASR final transcription failed."
                    break
                with self._lock:
                    self._flush_cursor_samples += len(window_samples)
                if event:
                    events.append(event)
                    self.events.append(event)
                    self.last_decode_ms = event.compute_ms
                    self.last_rtf = event.rtf
                    if self.on_event:
                        try:
                            self.on_event(event)
                        except Exception as exc:
                            self.last_error = f"ASR event callback failed: {type(exc).__name__}: {exc}"
                            print(f"[ASR Worker Error] {self.last_error}", file=sys.stderr)

            with self._lock:
                self._flush_in_progress = False
                if error is None:
                    self._reset_utterance_locked()
                return FlushResult(events, status="FAILED_RETRYABLE" if error else "COMPLETED", error=error)

    def _reset_utterance_locked(self) -> None:
        """Keep the running model, but start fresh audio and transcript state."""
        self.samples = np.empty(0, dtype=np.float32)
        self.buffer_start_ms = self.buffer_end_ms = self.last_decode_end_ms = None
        self.stream_start_ms = None
        self._stream_sample_count = 0
        self._flush_cursor_samples = 0
        self._audio_spool.close()
        self._audio_spool = tempfile.TemporaryFile(mode="w+b")
        self._pending_decode_count = 0
        self.stabilizer.reset()

    def _next_flush_window_locked(self):
        if self._flush_cursor_samples >= self._stream_sample_count or self.stream_start_ms is None:
            return None, None, None
        maximum_samples = max(1, round(self.sample_rate * self.rolling_window_ms / 1000))
        count = min(maximum_samples, self._stream_sample_count - self._flush_cursor_samples)
        self._audio_spool.flush()
        self._audio_spool.seek(self._flush_cursor_samples * 4)
        raw = self._audio_spool.read(count * 4)
        if len(raw) != count * 4:
            raise OSError("ASR audio spool is incomplete; finalization can be retried.")
        start_ms = self.stream_start_ms + self._flush_cursor_samples * 1000 / self.sample_rate
        end_ms = start_ms + count * 1000 / self.sample_rate
        return np.frombuffer(raw, dtype="<f4").copy(), start_ms, end_ms

    def _trim_window(self) -> None:
        maximum_samples = round(self.sample_rate * self.rolling_window_ms / 1000)
        if len(self.samples) <= maximum_samples:
            return
        drop = len(self.samples) - maximum_samples
        self.samples = self.samples[drop:]
        if self.buffer_end_ms is not None:
            self.buffer_start_ms = self.buffer_end_ms - len(self.samples) * 1000 / self.sample_rate

    def _worker_loop(self) -> None:
        """Background thread executing asynchronous non-blocking Whisper decodes."""
        while not self._stop_event.is_set():
            triggered = self._worker_trigger.wait(timeout=0.05)
            if self._stop_event.is_set():
                break

            with self._lock:
                is_flush = self._flush_requested.is_set()
                if not is_flush and not triggered:
                    continue
                if self.state != "running" and not is_flush:
                    self._worker_trigger.clear()
                    continue

                if is_flush:
                    try:
                        window_samples, window_start_ms, window_end_ms = self._next_flush_window_locked()
                    except OSError as exc:
                        self._flush_error = str(exc)
                        self._flush_requested.clear()
                        self._flush_completed.set()
                        self._worker_trigger.clear()
                        continue
                    if window_samples is None:
                        self._flush_requested.clear()
                        self._flush_completed.set()
                        self._worker_trigger.clear()
                        continue
                    dropped = 0
                else:
                    if len(self.samples) == 0:
                        self._worker_trigger.clear()
                        continue
                    # Partial decodes use the newest rolling window. Finalization
                    # reads every sample from the disk-backed utterance spool.
                    window_samples = self.samples.copy()
                    window_start_ms = self.buffer_start_ms
                    window_end_ms = self.buffer_end_ms
                    dropped = self._pending_decode_count
                    self._stale_windows_dropped += dropped
                    self._pending_decode_count = 0
                self._worker_trigger.clear()
                self._worker_state = "DECODING"
                is_final = is_flush

            # Decode executed OUTSIDE the lock so audio ingestion never blocks
            event = self._run_transcribe(
                window_samples,
                start_ms=window_start_ms,
                end_ms=window_end_ms,
                final=is_final,
                backlog_dropped=dropped,
            )

            callback = None
            with self._lock:
                self._worker_state = "IDLE"
                if self._last_inference_succeeded or not is_flush:
                    self.last_decode_end_ms = window_end_ms
                if event:
                    if is_flush:
                        self._flush_result_events.append(event)
                    else:
                        self._completed_events.append(event)
                    self.events.append(event)
                    self.last_decode_ms = event.compute_ms
                    self.last_rtf = event.rtf
                    callback = self.on_event

                if is_flush:
                    if not self._last_inference_succeeded:
                        self._flush_error = self.last_error or "ASR final transcription failed."
                        self._flush_requested.clear()
                        self._flush_completed.set()
                    else:
                        self._flush_cursor_samples += len(window_samples)
                        if self._flush_cursor_samples >= self._stream_sample_count:
                            self._flush_requested.clear()
                            self._flush_completed.set()
                        else:
                            self._worker_trigger.set()
                else:
                    # If new audio accumulated during this decode crossing the hop threshold,
                    # trigger immediately on the next freshest window
                    duration_ms = len(self.samples) * 1000 / self.sample_rate
                    due = self.buffer_end_ms is not None and (self.buffer_end_ms - window_end_ms >= self.decode_hop_ms)
                    if duration_ms >= self.minimum_decode_ms and due:
                        self._worker_trigger.set()
            if event and callback:
                try:
                    callback(event)
                except Exception as exc:
                    self.last_error = f"ASR event callback failed: {type(exc).__name__}: {exc}"
                    print(f"[ASR Worker Error] {self.last_error}", file=sys.stderr)

    def _run_transcribe(
        self,
        samples: np.ndarray,
        *,
        start_ms: Optional[float],
        end_ms: Optional[float],
        final: bool,
        backlog_dropped: int = 0,
    ) -> Optional[TranscriptEvent]:
        if not self.model or start_ms is None or end_ms is None or not len(samples):
            self._last_inference_succeeded = False
            return None

        self._last_inference_succeeded = False
        try:
            started = perf_counter() * 1000
            with self._inference_lock:
                segments, _info = self.model.transcribe(
                    samples,
                    language="en",
                    beam_size=1,
                    condition_on_previous_text=False,
                    vad_filter=False,
                    without_timestamps=False,
                )
                segments = list(segments)
                text = " ".join(getattr(segment, "text", "") for segment in segments).strip()
                confidence_values = [getattr(segment, "avg_logprob", None) for segment in segments]
                confidence_values = [val for val in confidence_values if val is not None]
                stable = self.stabilizer.normalize(text) if final else self.stabilizer.partial(text)
            self._last_inference_succeeded = True
            self.last_error = None
            finished = perf_counter() * 1000
        except Exception as exc:
            self.last_error = f"ASR transcription failed: {type(exc).__name__}: {exc}"
            print(f"[ASR Worker Error] {self.last_error}", file=sys.stderr)
            return None

        if stable is None:
            return None

        event = TranscriptEvent(
            kind="FINAL_TRANSCRIPT" if final else "PARTIAL_TRANSCRIPT",
            text=stable,
            audio_start_ms=start_ms,
            audio_end_ms=end_ms,
            asr_started_at_ms=started,
            asr_finished_at_ms=finished,
            emitted_at_ms=perf_counter() * 1000,
            confidence=sum(confidence_values) / len(confidence_values) if confidence_values else None,
            backlog_dropped=backlog_dropped,
        )
        if os.environ.get("SIGN_SPEECH_DIAGNOSTICS") == "1":
            print(f"[ASR] {event.kind} character_count={len(stable)}", file=sys.stderr)
        return event

    def _decode(self, *, final: bool) -> list[TranscriptEvent]:
        """Synchronous decoding helper for non-threaded mode."""
        if not self.model or self.buffer_start_ms is None or self.buffer_end_ms is None:
            return []

        samples = self.samples.copy()
        start_ms, end_ms = self.buffer_start_ms, self.buffer_end_ms
        event = self._run_transcribe(samples, start_ms=start_ms, end_ms=end_ms, final=final)
        self.last_decode_end_ms = end_ms
        if event is None:
            return []
        self.last_decode_ms = event.compute_ms
        self.last_rtf = event.rtf
        self.events.append(event)
        if self.on_event:
            try:
                self.on_event(event)
            except Exception as exc:
                self.last_error = f"ASR event callback failed: {type(exc).__name__}: {exc}"
                print(f"[ASR Worker Error] {self.last_error}", file=sys.stderr)
        return [event]
