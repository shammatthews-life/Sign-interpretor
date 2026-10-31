"""Local HTTP-facing bridge with explicit GPU-required production execution."""
from __future__ import annotations

import base64
from time import perf_counter
from typing import Any
import numpy as np

from .gpu_execution import ExecutionMode, resolve_execution_configuration
from .streaming_asr import FasterWhisperBackend, StreamingASRBackend


class LocalASRService:
    def __init__(self, backend_factory=FasterWhisperBackend) -> None:
        self.backend_factory = backend_factory
        self.backend: StreamingASRBackend | None = None
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
        if self.backend is None:
            resolved = resolve_execution_configuration(
                execution_mode,
                device=device,
                device_index=device_index,
                compute_type=compute_type,
            )
            device = resolved["device"]
            compute_type = resolved["compute_type"]
            device_index = resolved["device_index"]
            self.execution_mode = execution_mode
            self.device_index = device_index
            self.fallback_reason = resolved["fallback_reason"]

            self.backend = self.backend_factory(
                model,
                device=device,
                compute_type=compute_type,
                device_index=device_index if device_index is not None else 0,
                execution_mode=execution_mode,
                async_worker=async_worker,
                minimum_decode_ms=minimum_decode_ms,
                decode_hop_ms=decode_hop_ms,
                rolling_window_ms=rolling_window_ms,
            )
        self.backend.start()
        return self.status()

    def accept(self, payload: dict[str, Any]) -> dict[str, Any]:
        if self.backend is None:
            raise RuntimeError("ASR has not been started.")
        samples = np.frombuffer(base64.b64decode(payload["samples_base64"]), dtype="<f4")
        if self.stream_started_at_ms is None:
            self.stream_started_at_ms = perf_counter() * 1000
        start, end = float(payload["audio_start_ms"]), float(payload["audio_end_ms"])
        events = self.backend.accept_audio_chunk(samples, audio_start_ms=start, audio_end_ms=end)
        self.audio_duration_ms += len(samples) * 1000 / 16000
        self._record(events)
        return {"events": [event.report() for event in events], "status": self.status()}

    def control(self, action: str) -> dict[str, Any]:
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
        elif action == "reset":
            self.backend.reset()
            self.audio_duration_ms = 0.0
            self.first_partial_latency_ms = self.final_latency_ms = self.last_rtf = self.stream_started_at_ms = None
            self.last_partial = self.last_final = ""
        else:
            raise ValueError(f"Unknown ASR action: {action}")
        return self.status()

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
        }
