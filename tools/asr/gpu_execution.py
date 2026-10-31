"""Strict NVIDIA CUDA validation and explicit ASR execution-mode selection."""
from __future__ import annotations

import shutil
import subprocess
from typing import Literal

ExecutionMode = Literal["GPU_REQUIRED", "GPU_PREFERRED", "CPU_TEST_ONLY"]


class CudaExecutionError(RuntimeError):
    """Raised when a required NVIDIA CUDA execution environment is unavailable."""


def verify_nvidia_cuda(
    device_index: int = 0,
    compute_type: str = "float16",
    expected_gpu_name: str = "NVIDIA GeForce RTX 4050 Laptop GPU",
) -> dict:
    nvidia_smi = shutil.which("nvidia-smi")
    if not nvidia_smi:
        raise CudaExecutionError(
            "nvidia-smi was not found. Install/update the NVIDIA driver and ensure "
            "its directory is on PATH; GPU_REQUIRED mode will not fall back to CPU."
        )

    try:
        result = subprocess.run(
            [
                nvidia_smi,
                "--query-gpu=index,name,driver_version,utilization.gpu,memory.used,memory.total,temperature.gpu",
                "--format=csv,noheader,nounits",
            ],
            check=True,
            capture_output=True,
            text=True,
            timeout=10,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        raise CudaExecutionError(f"Unable to query NVIDIA GPU with nvidia-smi: {exc}") from exc

    selected = None
    for line in result.stdout.splitlines():
        fields = [field.strip() for field in line.split(",", 6)]
        if len(fields) == 7 and fields[0].isdigit() and int(fields[0]) == device_index:
            selected = fields
            break
    if selected is None:
        raise CudaExecutionError(
            f"nvidia-smi did not report GPU index {device_index}; CUDA device selection "
            "cannot be verified."
        )

    gpu_name = selected[1]
    if gpu_name.casefold() != expected_gpu_name.casefold():
        raise CudaExecutionError(
            f"GPU index {device_index} is {gpu_name!r}, expected "
            f"{expected_gpu_name!r}; refusing to select an unverified device."
        )

    try:
        import ctranslate2

        cuda_device_count = ctranslate2.get_cuda_device_count()
        supported_compute_types = sorted(
            ctranslate2.get_supported_compute_types("cuda", device_index)
        )
    except Exception as exc:
        raise CudaExecutionError(
            "CTranslate2 could not enumerate CUDA devices. Verify compatible NVIDIA "
            f"CUDA/cuBLAS/cuDNN runtime libraries. Details: {exc}"
        ) from exc

    if cuda_device_count <= device_index:
        raise CudaExecutionError(
            f"CTranslate2 reports {cuda_device_count} CUDA device(s); device index "
            f"{device_index} is unavailable."
        )
    if compute_type not in supported_compute_types:
        raise CudaExecutionError(
            f"CTranslate2 device {device_index} does not support compute type "
            f"{compute_type!r}. Supported: {', '.join(supported_compute_types)}."
        )

    return {
        "device_index": device_index,
        "gpu_name": gpu_name,
        "driver_version": selected[2],
        "cuda_device_count": cuda_device_count,
        "supported_compute_types": supported_compute_types,
        "selected_compute_type": compute_type,
        "nvidia_smi": nvidia_smi,
        "initial_telemetry": {
            "utilization_gpu_pct": _number_or_none(selected[3]),
            "memory_used_mb": _number_or_none(selected[4]),
            "memory_total_mb": _number_or_none(selected[5]),
            "temperature_c": _number_or_none(selected[6]),
        },
    }


def resolve_execution_configuration(
    execution_mode: ExecutionMode,
    *,
    device: str | None = None,
    device_index: int = 0,
    compute_type: str | None = None,
) -> dict:
    if execution_mode not in ("GPU_REQUIRED", "GPU_PREFERRED", "CPU_TEST_ONLY"):
        raise ValueError(f"Unknown ASR execution mode: {execution_mode!r}.")

    if execution_mode == "CPU_TEST_ONLY":
        if device not in (None, "cpu"):
            raise ValueError("CPU_TEST_ONLY mode accepts only device='cpu'.")
        return {
            "device": "cpu",
            "device_index": None,
            "compute_type": compute_type or "int8",
            "fallback_reason": None,
            "gpu": None,
        }

    if execution_mode == "GPU_REQUIRED":
        if device not in (None, "cuda"):
            raise CudaExecutionError(
                "GPU_REQUIRED mode cannot select a non-CUDA device. Choose "
                "CPU_TEST_ONLY explicitly for CPU-only tests."
            )
        if device_index != 0:
            raise CudaExecutionError("GPU_REQUIRED mode is pinned to NVIDIA GPU index 0.")
        selected_compute_type = compute_type or "float16"
        gpu = verify_nvidia_cuda(device_index, selected_compute_type)
        return {
            "device": "cuda",
            "device_index": device_index,
            "compute_type": selected_compute_type,
            "fallback_reason": None,
            "gpu": gpu,
        }

    if device == "cpu":
        return {
            "device": "cpu",
            "device_index": None,
            "compute_type": compute_type or "int8",
            "fallback_reason": "CPU explicitly requested in GPU_PREFERRED mode.",
            "gpu": None,
        }

    selected_compute_type = compute_type or "float16"
    try:
        gpu = verify_nvidia_cuda(device_index, selected_compute_type)
    except CudaExecutionError as exc:
        if device == "cuda":
            raise
        return {
            "device": "cpu",
            "device_index": None,
            "compute_type": "int8",
            "fallback_reason": str(exc),
            "gpu": None,
        }
    return {
        "device": "cuda",
        "device_index": device_index,
        "compute_type": selected_compute_type,
        "fallback_reason": None,
        "gpu": gpu,
    }


def _number_or_none(value: str) -> float | None:
    try:
        return float(value)
    except ValueError:
        return None
