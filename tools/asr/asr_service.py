"""Local HTTP-facing bridge with explicit GPU-required production execution."""
from __future__ import annotations

import base64
import binascii
import math
import threading
from time import perf_counter
from typing import Any
import numpy as np

from .gpu_execution import ExecutionMode, resolve_execution_configuration
from .streaming_asr import FasterWhisperBackend, StreamingASRBackend


class LocalASRService:
    MAX_AUDIO_CHUNK_BYTES = 2 * 1024 * 1024

    def __init__(self, backend_factory=FasterWhisperBackend) -> None:
        self.backend_factory = backend_factory
        self.backend: StreamingASRBackend | None = None
        self._lock = threading.RLock()
        self._backend_configuration: tuple[Any, ...] | None = None
        self.audio_duration_ms = 0.0
        self.first_partial_latency_ms = None
        self.final_latency_ms = None
        self.last_partial = ""
        self.last_final = ""
        self.last_rtf = None
        self.stream_started_at_ms = None
        self.execution_mode: ExecutionMode = "GPU_REQUIRED"
        self.device_index: int | None = 0
        self.fallback_reason: str | None = None

    def start(
        self,
        *,
        model: str = "base.en",
        device: str | None = None,
        compute_type: str | None = None,
        execution_mode: ExecutionMode = "GPU_REQUIRED",
        device_index: int = 0,
        async_worker: bool = True,
        minimum_decode_ms: int = 1000,
        decode_hop_ms: int = 750,
        rolling_window_ms: int = 4000,
    ) -> dict[str, Any]:
        with self._lock:
            if not isinstance(model, str) or not model.strip():
                raise ValueError("ASR model must be a non-empty string.")
            model = model.strip()
            if not isinstance(async_worker, bool):
                raise ValueError("async_worker must be a boolean.")
            for name, value in (
                ("minimum_decode_ms", minimum_decode_ms),
                ("decode_hop_ms", decode_hop_ms),
                ("rolling_window_ms", rolling_window_ms),
            ):
                if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
                    raise ValueError(f"{name} must be a positive integer.")
            if rolling_window_ms < minimum_decode_ms:
                raise ValueError("rolling_window_ms must be at least minimum_decode_ms.")
            resolved = resolve_execution_configuration(
                execution_mode,
                device=device,
                device_index=device_index,
                compute_type=compute_type,
            )
            device = resolved["device"]
            compute_type = resolved["compute_type"]
            resolved_device_index = resolved["device_index"]
            configuration = (
                model,
                device,
                compute_type,
                resolved_device_index,
                execution_mode,
                async_worker,
                minimum_decode_ms,
                decode_hop_ms,
                rolling_window_ms,
            )
            if self._backend_configuration is not None and configuration != self._backend_configuration:
                raise RuntimeError(
                    "ASR is already configured with a different model or execution mode; "
                    "restart the local runtime before changing its configuration."
                )

            if self.backend is None:
                candidate = self.backend_factory(
                    model,
                    device=device,
                    compute_type=compute_type,
                    device_index=resolved_device_index if resolved_device_index is not None else 0,
                    execution_mode=execution_mode,
                    async_worker=async_worker,
                    minimum_decode_ms=minimum_decode_ms,
                    decode_hop_ms=decode_hop_ms,
                    rolling_window_ms=rolling_window_ms,
                )
                candidate.start()
                self.backend = candidate
                self._backend_configuration = configuration
            elif self.backend.state != "running":
                self.backend.start()

            self.execution_mode = execution_mode
            self.device_index = resolved_device_index
            self.fallback_reason = resolved["fallback_reason"]

            return self.status()

    def accept(self, payload: dict[str, Any]) -> dict[str, Any]:
        with self._lock:
            if self.backend is None:
                raise RuntimeError("ASR has not been started.")
            if self.backend.state != "running":
                raise RuntimeError(f"ASR cannot accept audio while its state is {self.backend.state!r}.")
            if not isinstance(payload, dict):
                raise ValueError("ASR chunk payload must be a JSON object.")

            encoded = payload.get("samples_base64")
            if not isinstance(encoded, str) or not encoded:
                raise ValueError("samples_base64 must be a non-empty base64 string.")
            if len(encoded) > self.MAX_AUDIO_CHUNK_BYTES * 4 // 3 + 4:
                raise ValueError("Audio chunk exceeds the maximum supported size.")
            try:
                raw = base64.b64decode(encoded, validate=True)
            except (ValueError, binascii.Error) as exc:
                raise ValueError("samples_base64 must contain valid base64 data.") from exc
            if not raw or len(raw) > self.MAX_AUDIO_CHUNK_BYTES or len(raw) % 4:
                raise ValueError("Audio chunk must contain a non-empty float32 sample array within the size limit.")

            start_value, end_value = payload.get("audio_start_ms"), payload.get("audio_end_ms")
            if (
                isinstance(start_value, bool)
                or isinstance(end_value, bool)
                or not isinstance(start_value, (int, float))
                or not isinstance(end_value, (int, float))
            ):
                raise ValueError("Audio timestamps must be numeric.")
            try:
                start, end = float(start_value), float(end_value)
            except OverflowError as exc:
                raise ValueError("Audio timestamps must be finite numeric values.") from exc
            if not math.isfinite(start) or not math.isfinite(end) or start < 0 or end <= start:
                raise ValueError("Audio timestamps must be finite, non-negative, and increasing.")

            samples = np.frombuffer(raw, dtype="<f4")
            if not np.isfinite(samples).all():
                raise ValueError("Audio samples must all be finite.")
            if np.max(np.abs(samples)) > 1.5:
                raise ValueError("Audio samples exceed the accepted normalized amplitude range [-1.5, 1.5].")

            if self.stream_started_at_ms is None:
                self.stream_started_at_ms = perf_counter() * 1000
            events = self.backend.accept_audio_chunk(samples, audio_start_ms=start, audio_end_ms=end)
            sample_rate = getattr(self.backend, "sample_rate", 16000)
            self.audio_duration_ms += len(samples) * 1000 / sample_rate
            self._record(events)
            return {"events": [event.report() for event in events], "status": self.status()}

    def control(self, action: str) -> dict[str, Any]:
        with self._lock:
            if self.backend is None:
                return self.status()
            if action == "pause":
                self.backend.pause()
            elif action == "resume":
                self.backend.resume()
            elif action == "flush":
                events = self.backend.flush()
                self._record(events)
                return {"events": [event.report() for event in events], "status": self.status()}
            elif action == "stop":
                self.backend.stop()
                self._reset_stream_state()
            elif action == "reset":
                self.backend.reset()
                self._reset_stream_state()
            else:
                raise ValueError(f"Unknown ASR action: {action}")
            return self.status()

    def _reset_stream_state(self) -> None:
        self.audio_duration_ms = 0.0
        self.first_partial_latency_ms = None
        self.final_latency_ms = None
        self.last_rtf = None
        self.stream_started_at_ms = None
        self.last_partial = ""
        self.last_final = ""

    def _record(self, events) -> None:
        for event in events:
            # Browser and server clocks differ; use the server's first accepted
            # chunk receipt as the local latency reference.
            latency = event.emitted_at_ms - (self.stream_started_at_ms or event.emitted_at_ms)
            self.last_rtf = event.rtf
            if event.kind == "PARTIAL_TRANSCRIPT":
                self.last_partial = event.text
                if self.first_partial_latency_ms is None:
                    self.first_partial_latency_ms = latency
            else:
                self.last_final = event.text
                self.final_latency_ms = latency

    def status(self) -> dict[str, Any]:
        with self._lock:
            backend = self.backend
            worker_state = getattr(backend, "worker_state", "IDLE" if backend and backend.state == "running" else "STOPPED")
            queue_size = getattr(backend, "queue_size", 0)
            backlog = getattr(backend, "backlog", 0)
            last_decode_ms = getattr(backend, "last_decode_ms", None)
            return {
                "state": backend.state if backend else "stopped",
                "worker_state": worker_state,
                "model": getattr(backend, "model_name", "base.en"),
                "device": getattr(
                    backend,
                    "device",
                    "cuda" if self.execution_mode == "GPU_REQUIRED" else "cpu",
                ),
                "compute_type": getattr(
                    backend,
                    "compute_type",
                    "float16" if self.execution_mode != "CPU_TEST_ONLY" else "int8",
                ),
                "execution_mode": self.execution_mode,
                "device_index": self.device_index,
                "fallback_reason": self.fallback_reason,
                "audio_duration_ms": self.audio_duration_ms,
                "audio_received_sec": round(self.audio_duration_ms / 1000.0, 2),
                "asr_queue": queue_size,
                "backlog": backlog,
                "partial": self.last_partial,
                "final": self.last_final,
                "first_partial_latency_ms": self.first_partial_latency_ms,
                "final_latency_ms": self.final_latency_ms,
                "last_decode_ms": last_decode_ms,
                "rtf": self.last_rtf,
                "last_error": getattr(backend, "last_error", None),
            }
