#!/usr/bin/env python3
"""Verify a real Faster-Whisper inference on NVIDIA CUDA and save raw evidence."""
from __future__ import annotations

import argparse
import ctypes
import hashlib
import importlib.metadata
import json
import os
import subprocess
import sys
import threading
import time
import wave
from ctypes import wintypes
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from tools.asr.gpu_execution import verify_nvidia_cuda

DEFAULT_AUDIO = PROJECT_ROOT / "runtime" / "youtube" / "MXKkXXYUxBc" / "audio_16k.wav"
DEFAULT_REPORT = PROJECT_ROOT / "data" / "h33_nvidia_gpu_verification.json"
DEFAULT_TELEMETRY = PROJECT_ROOT / "data" / "h33_nvidia_gpu_telemetry.json"
EXPECTED_GPU = "NVIDIA GeForce RTX 4050 Laptop GPU"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--audio", type=Path, default=DEFAULT_AUDIO)
    parser.add_argument("--model", default="base.en")
    parser.add_argument("--device-index", type=int, default=0)
    parser.add_argument("--compute-type", default="float16")
    parser.add_argument("--sample-seconds", type=float, default=5.0)
    parser.add_argument("--repetitions", type=int, default=10)
    parser.add_argument("--sample-interval-ms", type=int, default=200)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--telemetry", type=Path, default=DEFAULT_TELEMETRY)
    return parser.parse_args()


def resolve_cached_model(model_name: str) -> Path:
    candidate = Path(model_name)
    required_files = ("config.json", "model.bin", "tokenizer.json", "vocabulary.txt")
    if candidate.is_dir() and all((candidate / name).is_file() for name in required_files):
        return candidate.resolve()

    try:
        from huggingface_hub import constants
    except ImportError as exc:
        raise RuntimeError(
            "huggingface_hub is required to locate the cached Faster-Whisper model."
        ) from exc

    model_cache = Path(constants.HF_HUB_CACHE) / f"models--Systran--faster-whisper-{model_name}"
    ref_file = model_cache / "refs" / "main"
    if not ref_file.is_file():
        raise FileNotFoundError(
            f"Model {model_name!r} is not present in the local Hugging Face cache at "
            f"{model_cache}. This diagnostic does not download model weights."
        )
    snapshot = model_cache / "snapshots" / ref_file.read_text(encoding="utf-8").strip()
    missing = [name for name in required_files if not (snapshot / name).is_file()]
    if missing:
        raise FileNotFoundError(
            f"The cached model snapshot is incomplete: missing {', '.join(missing)} "
            f"under {snapshot}."
        )
    return snapshot


def read_audio_prefix(path: Path, duration_s: float):
    import numpy as np

    if duration_s <= 0:
        raise ValueError("--sample-seconds must be greater than zero.")
    with wave.open(str(path), "rb") as source:
        if (
            source.getnchannels() != 1
            or source.getsampwidth() != 2
            or source.getframerate() != 16000
            or source.getcomptype() != "NONE"
        ):
            raise ValueError("Diagnostic input must be mono, 16 kHz, uncompressed PCM16 WAV.")
        frame_count = min(source.getnframes(), round(duration_s * source.getframerate()))
        if frame_count == 0:
            raise ValueError("Diagnostic audio contains no frames.")
        samples = np.frombuffer(source.readframes(frame_count), dtype="<i2")
    return samples.astype(np.float32) / 32768.0, frame_count / 16000.0


def query_gpu() -> dict[str, Any]:
    result = subprocess.run(
        [
            "nvidia-smi",
            "--query-gpu=index,name,driver_version,utilization.gpu,memory.used,memory.total,temperature.gpu",
            "--format=csv,noheader,nounits",
        ],
        check=True,
        capture_output=True,
        text=True,
        timeout=5,
    )
    fields = [part.strip() for part in result.stdout.splitlines()[0].split(",", 6)]
    if len(fields) != 7:
        raise RuntimeError(f"Unexpected nvidia-smi GPU telemetry: {result.stdout!r}")
    return {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "device_index": int(fields[0]),
        "gpu_name": fields[1],
        "driver_version": fields[2],
        "utilization_gpu_pct": _float_or_none(fields[3]),
        "memory_used_mb": _float_or_none(fields[4]),
        "memory_total_mb": _float_or_none(fields[5]),
        "temperature_c": _float_or_none(fields[6]),
    }


def query_compute_processes() -> dict[str, Any]:
    try:
        result = subprocess.run(
            [
                "nvidia-smi",
                "--query-compute-apps=pid,process_name,used_memory",
                "--format=csv,noheader,nounits",
            ],
            check=True,
            capture_output=True,
            text=True,
            timeout=5,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        return {"available": False, "error": str(exc), "processes": []}

    processes = []
    for line in result.stdout.splitlines():
        fields = [part.strip() for part in line.split(",", 2)]
        if len(fields) == 3:
            processes.append(
                {
                    "pid": int(fields[0]) if fields[0].isdigit() else None,
                    "process_name": fields[1],
                    "memory_used_mb": _float_or_none(fields[2]),
                }
            )
    return {"available": True, "processes": processes}


def query_memory() -> dict[str, Any]:
    data: dict[str, Any] = {"process": None, "system": None}
    try:
        class PROCESS_MEMORY_COUNTERS_EX(ctypes.Structure):
            _fields_ = [
                ("cb", ctypes.c_ulong),
                ("PageFaultCount", ctypes.c_ulong),
                ("PeakWorkingSetSize", ctypes.c_size_t),
                ("WorkingSetSize", ctypes.c_size_t),
                ("QuotaPeakPagedPoolUsage", ctypes.c_size_t),
                ("QuotaPagedPoolUsage", ctypes.c_size_t),
                ("QuotaPeakNonPagedPoolUsage", ctypes.c_size_t),
                ("QuotaNonPagedPoolUsage", ctypes.c_size_t),
                ("PagefileUsage", ctypes.c_size_t),
                ("PeakPagefileUsage", ctypes.c_size_t),
                ("PrivateUsage", ctypes.c_size_t),
            ]

        counters = PROCESS_MEMORY_COUNTERS_EX()
        counters.cb = ctypes.sizeof(counters)
        kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
        psapi = ctypes.WinDLL("psapi", use_last_error=True)
        kernel32.GetCurrentProcess.restype = wintypes.HANDLE
        psapi.GetProcessMemoryInfo.argtypes = [
            wintypes.HANDLE,
            ctypes.POINTER(PROCESS_MEMORY_COUNTERS_EX),
            wintypes.DWORD,
        ]
        psapi.GetProcessMemoryInfo.restype = wintypes.BOOL
        handle = kernel32.GetCurrentProcess()
        if not psapi.GetProcessMemoryInfo(handle, ctypes.byref(counters), counters.cb):
            raise ctypes.WinError(ctypes.get_last_error())
        data["process"] = {
            "pid": os.getpid(),
            "working_set_mb": round(counters.WorkingSetSize / 1024**2, 2),
            "peak_working_set_mb": round(counters.PeakWorkingSetSize / 1024**2, 2),
            "private_memory_mb": round(counters.PrivateUsage / 1024**2, 2),
        }
    except (AttributeError, OSError) as exc:
        data["process_error"] = str(exc)

    try:
        class MEMORYSTATUSEX(ctypes.Structure):
            _fields_ = [
                ("dwLength", ctypes.c_ulong),
                ("dwMemoryLoad", ctypes.c_ulong),
                ("ullTotalPhys", ctypes.c_ulonglong),
                ("ullAvailPhys", ctypes.c_ulonglong),
                ("ullTotalPageFile", ctypes.c_ulonglong),
                ("ullAvailPageFile", ctypes.c_ulonglong),
                ("ullTotalVirtual", ctypes.c_ulonglong),
                ("ullAvailVirtual", ctypes.c_ulonglong),
                ("ullAvailExtendedVirtual", ctypes.c_ulonglong),
            ]

        status = MEMORYSTATUSEX()
        status.dwLength = ctypes.sizeof(status)
        kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
        kernel32.GlobalMemoryStatusEx.argtypes = [ctypes.POINTER(MEMORYSTATUSEX)]
        kernel32.GlobalMemoryStatusEx.restype = wintypes.BOOL
        if not kernel32.GlobalMemoryStatusEx(ctypes.byref(status)):
            raise ctypes.WinError(ctypes.get_last_error())
        data["system"] = {
            "total_ram_gib": round(status.ullTotalPhys / 1024**3, 2),
            "available_ram_gib": round(status.ullAvailPhys / 1024**3, 2),
            "used_percent": status.dwMemoryLoad,
        }
    except (AttributeError, OSError) as exc:
        data["system_error"] = str(exc)
    return data


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(4 * 1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _float_or_none(value: str) -> float | None:
    try:
        return float(value)
    except ValueError:
        return None


def main() -> int:
    args = parse_args()
    report: dict[str, Any] = {
        "schema_version": 1,
        "phase": "H33",
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": "NOT RUN",
        "gpu_environment": {"status": "NOT RUN"},
        "model": {"status": "NOT RUN"},
        "inference": {"status": "NOT RUN"},
        "errors": [],
    }
    telemetry: dict[str, Any] = {
        "schema_version": 1,
        "phase": "H33",
        "created_at_utc": report["created_at_utc"],
        "gpu_samples_during_inference": [],
        "compute_process_samples_during_inference": [],
        "memory_samples": [],
    }
    sampler_thread: threading.Thread | None = None
    stop_sampler = threading.Event()
    stage = "nvidia_gpu_preflight"

    def sample_inference() -> None:
        interval = max(0.05, args.sample_interval_ms / 1000)
        while not stop_sampler.is_set():
            try:
                telemetry["gpu_samples_during_inference"].append(query_gpu())
            except (OSError, subprocess.SubprocessError, RuntimeError) as exc:
                telemetry.setdefault("sampling_errors", []).append(str(exc))
            telemetry["compute_process_samples_during_inference"].append(
                query_compute_processes()
            )
            telemetry["memory_samples"].append(
                {"timestamp_utc": datetime.now(timezone.utc).isoformat(), **query_memory()}
            )
            stop_sampler.wait(interval)

    try:
        if not args.audio.is_file():
            raise FileNotFoundError(f"Audio input does not exist: {args.audio}")
        if args.repetitions < 1:
            raise ValueError("--repetitions must be at least one.")

        stage = "nvidia_gpu_preflight"
        gpu_info = verify_nvidia_cuda(
            args.device_index, args.compute_type, expected_gpu_name=EXPECTED_GPU
        )
        report["gpu_environment"] = {"status": "PASS", **gpu_info}
        report["host_pid"] = os.getpid()
        report["package_versions"] = {
            "ctranslate2": importlib.metadata.version("ctranslate2"),
            "faster_whisper": importlib.metadata.version("faster-whisper"),
        }
        report["source_audio"] = {
            "path": str(args.audio.resolve()),
            "sha256": sha256_file(args.audio),
        }
        telemetry["gpu_before_model_load"] = query_gpu()
        telemetry["memory_before_model_load"] = query_memory()

        stage = "cached_model_resolution"
        model_path = resolve_cached_model(args.model)
        report["model"]["resolved_path"] = str(model_path)

        stage = "cuda_model_load"
        from faster_whisper import WhisperModel

        load_started = time.perf_counter()
        model = WhisperModel(
            str(model_path),
            device="cuda",
            device_index=args.device_index,
            compute_type=args.compute_type,
        )
        load_duration_ms = (time.perf_counter() - load_started) * 1000
        report["model"].update(
            {
                "status": "PASS",
                "name": args.model,
                "device": "cuda",
                "device_index": args.device_index,
                "compute_type": args.compute_type,
                "load_duration_ms": round(load_duration_ms, 2),
            }
        )
        telemetry["gpu_after_model_load"] = query_gpu()
        telemetry["memory_after_model_load"] = query_memory()

        stage = "load_audio_prefix"
        audio, audio_duration_s = read_audio_prefix(args.audio, args.sample_seconds)
        report["inference"].update(
            {
                "audio_duration_s": round(audio_duration_s, 3),
                "sample_rate_hz": 16000,
                "warmup_duration_ms": None,
                "repetitions": args.repetitions,
                "observations": [],
            }
        )

        stage = "cuda_warmup_inference"
        warmup_audio = audio[: min(len(audio), 16000)]
        warmup_started = time.perf_counter()
        warmup_segments, _ = model.transcribe(
            warmup_audio,
            language="en",
            beam_size=1,
            vad_filter=False,
            condition_on_previous_text=False,
        )
        list(warmup_segments)
        report["inference"]["warmup_duration_ms"] = round(
            (time.perf_counter() - warmup_started) * 1000, 2
        )
        telemetry["gpu_before_inference"] = query_gpu()
        telemetry["memory_before_inference"] = query_memory()

        stage = "actual_cuda_inference"
        sampler_thread = threading.Thread(target=sample_inference, daemon=True)
        sampler_thread.start()
        observations = []
        for iteration in range(args.repetitions):
            started = time.perf_counter()
            segments, info = model.transcribe(
                audio,
                language="en",
                beam_size=1,
                vad_filter=False,
                condition_on_previous_text=False,
            )
            segment_list = list(segments)
            duration_ms = (time.perf_counter() - started) * 1000
            observations.append(
                {
                    "iteration": iteration + 1,
                    "duration_ms": round(duration_ms, 2),
                    "segment_count": len(segment_list),
                    "text": " ".join(segment.text.strip() for segment in segment_list).strip(),
                    "detected_language": getattr(info, "language", None),
                }
            )
        stop_sampler.set()
        sampler_thread.join(timeout=10)
        if sampler_thread.is_alive():
            raise TimeoutError("NVIDIA telemetry sampler did not stop.")
        report["inference"]["observations"] = observations
        report["inference"]["actual_cuda_inference_succeeded"] = True
        telemetry["gpu_after_inference"] = query_gpu()
        telemetry["memory_after_inference"] = query_memory()
        report["inference"]["status"] = "PASS"
        report["status"] = "PASS"
    except Exception as exc:
        report["status"] = "FAIL"
        report["failed_stage"] = stage
        report["errors"].append(f"{type(exc).__name__}: {exc}")
        report["inference"]["actual_cuda_inference_succeeded"] = False
        report["inference"]["status"] = "FAIL" if stage == "actual_cuda_inference" else "NOT RUN"
    finally:
        stop_sampler.set()
        if sampler_thread is not None and sampler_thread.is_alive():
            sampler_thread.join(timeout=10)
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.telemetry.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        args.telemetry.write_text(json.dumps(telemetry, indent=2) + "\n", encoding="utf-8")

    print(json.dumps({"status": report["status"], "report": str(args.report), "errors": report["errors"]}, indent=2))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
