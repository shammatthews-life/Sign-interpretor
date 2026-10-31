"""Read-only resource check before running a full local YouTube inference."""
from __future__ import annotations

import argparse
import ctypes
import json
import math
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent


class _MemoryStatus(ctypes.Structure):
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


def _available_memory_bytes() -> int:
    if os.name == "nt":
        status = _MemoryStatus()
        status.dwLength = ctypes.sizeof(status)
        if not ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(status)):
            raise OSError("GlobalMemoryStatusEx failed.")
        return int(status.ullAvailPhys)
    if hasattr(os, "sysconf"):
        return int(os.sysconf("SC_AVPHYS_PAGES") * os.sysconf("SC_PAGE_SIZE"))
    raise OSError("Available system memory cannot be measured on this platform.")


def _cuda_memory() -> dict:
    executable = shutil.which("nvidia-smi")
    if not executable:
        return {"available": False, "error": "nvidia-smi was not found on PATH."}
    try:
        result = subprocess.run(
            [
                executable,
                "--query-gpu=memory.free,memory.total",
                "--format=csv,noheader,nounits",
            ],
            capture_output=True,
            text=True,
            check=True,
            timeout=10,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        return {"available": False, "error": f"{type(exc).__name__}: {exc}"}
    devices = []
    for line in result.stdout.splitlines():
        values = [value.strip() for value in line.split(",")]
        if len(values) != 2 or not all(value.isdigit() for value in values):
            return {"available": False, "error": "nvidia-smi returned an unrecognized memory record."}
        devices.append({"free_mib": int(values[0]), "total_mib": int(values[1])})
    if not devices:
        return {"available": False, "error": "nvidia-smi did not report a CUDA device."}
    return {"available": True, "devices": devices}


def run_preflight(
    *,
    audio_seconds: float,
    output_dir: Path,
    minimum_available_memory_gib: float = 6.0,
    minimum_free_disk_gib: float = 10.0,
    minimum_free_vram_gib: float = 2.0,
) -> dict:
    started_at = time.time()
    available_memory = _available_memory_bytes()
    disk = shutil.disk_usage(output_dir if output_dir.exists() else PROJECT_ROOT)
    cuda = _cuda_memory()
    required_disk = max(
        minimum_free_disk_gib,
        audio_seconds * 16_000 * 2 * 3 / (1024 ** 3),
    )
    selected_device = None
    if cuda["available"]:
        selected_device = max(cuda["devices"], key=lambda item: item["free_mib"])
    checks = {
        "system_memory": available_memory >= minimum_available_memory_gib * 1024 ** 3,
        "free_disk": disk.free >= required_disk * 1024 ** 3,
        "cuda_device": selected_device is not None,
        "cuda_free_memory": selected_device is not None and selected_device["free_mib"] >= minimum_free_vram_gib * 1024,
    }
    return {
        "status": "SAFE" if all(checks.values()) else "BLOCKED",
        "created_at_unix": started_at,
        "audio_seconds": audio_seconds,
        "output_dir": str(output_dir),
        "measurements": {
            "available_system_memory_gib": round(available_memory / 1024 ** 3, 3),
            "free_disk_gib": round(disk.free / 1024 ** 3, 3),
            "required_free_disk_gib": round(required_disk, 3),
            "cuda": cuda,
            "selected_cuda_device": selected_device,
        },
        "thresholds": {
            "minimum_available_memory_gib": minimum_available_memory_gib,
            "minimum_free_disk_gib": minimum_free_disk_gib,
            "minimum_free_vram_gib": minimum_free_vram_gib,
        },
        "checks": checks,
        "full_video_run_permitted": all(checks.values()),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--audio-seconds", type=float, required=True, help="Expected audio duration in seconds.")
    parser.add_argument("--output-dir", type=Path, default=PROJECT_ROOT / "runtime" / "youtube")
    parser.add_argument("--minimum-available-memory-gib", type=float, default=6.0)
    parser.add_argument("--minimum-free-disk-gib", type=float, default=10.0)
    parser.add_argument("--minimum-free-vram-gib", type=float, default=2.0)
    parser.add_argument("--json-out", type=Path)
    args = parser.parse_args()
    values = (
        args.audio_seconds,
        args.minimum_available_memory_gib,
        args.minimum_free_disk_gib,
        args.minimum_free_vram_gib,
    )
    if any(not math.isfinite(value) or value <= 0 for value in values):
        parser.error("Audio duration and resource thresholds must be positive.")
    report = run_preflight(
        audio_seconds=args.audio_seconds,
        output_dir=args.output_dir,
        minimum_available_memory_gib=args.minimum_available_memory_gib,
        minimum_free_disk_gib=args.minimum_free_disk_gib,
        minimum_free_vram_gib=args.minimum_free_vram_gib,
    )
    encoded = json.dumps(report, indent=2)
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(encoded + "\n", encoding="utf-8")
    print(encoded)
    return 0 if report["status"] == "SAFE" else 2


if __name__ == "__main__":
    sys.exit(main())
