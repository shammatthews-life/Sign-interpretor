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
import ctypes
import threading
from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict
from time import perf_counter
from typing import Callable, Iterable, Optional

import numpy as np


def ensure_cuda_support() -> bool:
    """Ensure CUDA 12 libraries are discoverable on Windows for CTranslate2."""
    try:
        import ctranslate2
        if ctranslate2.get_cuda_device_count() == 0:
            return False
        candidates = [
            os.path.dirname(ctranslate2.__file__),
            r"C:\Program Files\Blackmagic Design\DaVinci Resolve",
            os.path.join(os.environ.get("CUDA_PATH", ""), "bin"),
        ]
        for p in candidates:
            if os.path.isdir(p):
                try:
                    os.add_dll_directory(p)
                except Exception:
                    pass
                if p not in os.environ.get("PATH", ""):
                    os.environ["PATH"] = p + ";" + os.environ.get("PATH", "")
                for dll in ("cublasLt64_12.dll", "cublas64_12.dll"):
                    dll_path = os.path.join(p, dll)
                    if os.path.exists(dll_path):
                        try:
                            ctypes.CDLL(dll_path)
                        except Exception:
                            pass
        return True
    except Exception:
        return False


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
    ) -> None:
        self.model_name = model_name
        self.device = device
        self.compute_type = compute_type
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
        if self.device == "cuda":
            ensure_cuda_support()

        if self.model is None:
            if self.model_factory:
                self.model = self.model_factory(self.model_name, device=self.device, compute_type=self.compute_type)
            else:
                from faster_whisper import WhisperModel
                self.model = WhisperModel(self.model_name, device=self.device, compute_type=self.compute_type)

        self.state = "running"
        self._worker_state = "IDLE"

        if self.async_worker and (self._worker_thread is None or not self._worker_thread.is_alive()):
            self._stop_event.clear()
            self._worker_trigger.clear()
            self._flush_requested.clear()
            self._flush_completed.clear()
            self._worker_thread = threading.Thread(target=self._worker_loop, daemon=True, name="ASRWorkerThread")
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
        self.state = "stopped"
        self._worker_state = "STOPPED"
        if self.async_worker and self._worker_thread and self._worker_thread.is_alive():
            self._stop_event.set()
            self._worker_trigger.set()
            self._worker_thread.join(timeout=1.0)
            self._worker_thread = None

    def reset(self) -> None:
        self.stop()
        with self._lock:
            self.samples = np.empty(0, dtype=np.float32)
            self.buffer_start_ms = self.buffer_end_ms = self.last_decode_end_ms = None
            self.last_decode_ms = self.last_rtf = None
            self.stabilizer.reset()
            self.events = []
            self._completed_events = []
            self._pending_decode_count = 0
            self._stale_windows_dropped = 0
            self._worker_state = "IDLE"

    def accept_audio_chunk(self, samples: np.ndarray, *, audio_start_ms: float, audio_end_ms: float) -> list[TranscriptEvent]:
        if self.state != "running":
            return []
        data = np.asarray(samples, dtype=np.float32).reshape(-1)
        if not len(data):
            return []

        with self._lock:
            if self.buffer_start_ms is None:
                self.buffer_start_ms = audio_start_ms
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

    def flush(self) -> list[TranscriptEvent]:
        if self.state != "running":
            return []

        if self.async_worker:
            with self._lock:
                if len(self.samples) == 0:
                    return []
                self._flush_completed.clear()
                self._flush_requested.set()
                self._worker_trigger.set()

            # Wait for background worker to finalize the flush
            self._flush_completed.wait(timeout=5.0)

            with self._lock:
                returned = list(self._completed_events)
                self._completed_events.clear()
                return returned
        else:
            with self._lock:
                if not len(self.samples):
                    return []
            return self._decode(final=True)

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

                if len(self.samples) == 0:
                    self._worker_trigger.clear()
                    if is_flush:
                        self._flush_requested.clear()
                        self._flush_completed.set()
                    continue

                # STALE-WINDOW POLICY:
                # Snapshot ONLY the single newest valid rolling window!
                # If multiple hops were triggered while decoding, collapse them
                # into this newest window, preventing stale queues.
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

            with self._lock:
                self._worker_state = "IDLE"
                self.last_decode_end_ms = window_end_ms
                if event:
                    self._completed_events.append(event)
                    self.events.append(event)
                    self.last_decode_ms = event.compute_ms
                    self.last_rtf = event.rtf
                    if self.on_event:
                        self.on_event(event)

                if is_flush:
                    self._flush_requested.clear()
                    self._flush_completed.set()
                else:
                    # If new audio accumulated during this decode crossing the hop threshold,
                    # trigger immediately on the next freshest window
                    duration_ms = len(self.samples) * 1000 / self.sample_rate
                    due = self.buffer_end_ms is not None and (self.buffer_end_ms - window_end_ms >= self.decode_hop_ms)
                    if duration_ms >= self.minimum_decode_ms and due:
                        self._worker_trigger.set()

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
            return None

        started = perf_counter() * 1000
        try:
            segments, _info = self.model.transcribe(
                samples,
                language="en",
                beam_size=1,
                condition_on_previous_text=False,
                vad_filter=False,
                without_timestamps=False,
            )
            segments = list(segments)
        except Exception as exc:
            print(f"[ASR Worker Error] transcribe failed: {exc}", file=sys.stderr)
            return None

        text = " ".join(getattr(segment, "text", "") for segment in segments).strip()
        confidence_values = [getattr(segment, "avg_logprob", None) for segment in segments]
        confidence_values = [val for val in confidence_values if val is not None]
        finished = perf_counter() * 1000

        stable = self.stabilizer.final(text) if final else self.stabilizer.partial(text)
        if stable is None:
            return None

        return TranscriptEvent(
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
            self.on_event(event)
        return [event]
