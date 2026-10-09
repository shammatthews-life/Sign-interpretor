"""Repeatable CPU/GPU faster-whisper benchmark against local WAV fixtures."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import wave
from time import perf_counter, sleep
from pathlib import Path
from statistics import mean
from typing import Optional
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from asr.generate_benchmark_audio import ensure_fixtures
from asr.streaming_asr import FasterWhisperBackend


def get_vram_usage_mib() -> Optional[float]:
    """Query current GPU VRAM utilization via nvidia-smi if available."""
    try:
        out = subprocess.check_output(
            ["nvidia-smi", "--query-gpu=memory.used", "--format=csv,nounits,noheader"],
            text=True,
            timeout=2.0,
        )
        return float(out.strip().splitlines()[0])
    except Exception:
        return None


def read_wav_mono_float(path: Path) -> tuple[np.ndarray, int]:
    with wave.open(str(path), "rb") as reader:
        if reader.getsampwidth() != 2:
            raise ValueError(f"{path.name}: only 16-bit PCM WAV is supported")
        channels, rate = reader.getnchannels(), reader.getframerate()
        raw = np.frombuffer(reader.readframes(reader.getnframes()), dtype="<i2").astype(np.float32) / 32768.0
    if channels > 1:
        raw = raw.reshape(-1, channels).mean(axis=1)
    if rate == 16000:
        return raw, rate
    output = np.interp(
        np.linspace(0, len(raw) - 1, round(len(raw) * 16000 / rate)),
        np.arange(len(raw)),
        raw,
    ).astype(np.float32)
    return output, 16000


def wer(reference: str, hypothesis: str) -> float:
    ref = reference.lower().replace(".", "").replace(",", "").replace("!", "").replace("?", "").split()
    hyp = hypothesis.lower().replace(".", "").replace(",", "").replace("!", "").replace("?", "").split()
    table = list(range(len(hyp) + 1))
    for i, token in enumerate(ref, 1):
        next_row = [i]
        for j, predicted in enumerate(hyp, 1):
            next_row.append(min(table[j] + 1, next_row[j - 1] + 1, table[j - 1] + (token != predicted)))
        table = next_row
    return table[-1] / max(1, len(ref))


def benchmark(
    model: str,
    fixtures: dict[str, tuple[Path, str]],
    paced: bool,
    *,
    device: str = "cpu",
    compute_type: str = "int8",
    minimum_decode_ms: int = 1000,
    decode_hop_ms: int = 750,
    rolling_window_ms: int = 15000,
    async_worker: bool = False,
) -> dict:
    initial_vram = get_vram_usage_mib() if device == "cuda" else None

    backend = FasterWhisperBackend(
        model,
        device=device,
        compute_type=compute_type,
        minimum_decode_ms=minimum_decode_ms,
        decode_hop_ms=decode_hop_ms,
        rolling_window_ms=rolling_window_ms,
        async_worker=async_worker,
    )
    load_started = perf_counter()
    backend.start()
    load_ms = (perf_counter() - load_started) * 1000

    peak_vram = get_vram_usage_mib() if device == "cuda" else None

    results = []
    all_decode_values = []
    for name, (path, reference) in fixtures.items():
        samples, rate = read_wav_mono_float(path)
        assert rate == 16000
        backend.reset()
        backend.start()
        first_partial = None
        started = perf_counter() * 1000
        for index in range(0, len(samples), 1600):
            chunk = samples[index : index + 1600]
            events = backend.accept_audio_chunk(
                chunk,
                audio_start_ms=index * 1000 / 16000,
                audio_end_ms=(index + len(chunk)) * 1000 / 16000,
            )
            all_decode_values.extend(event.compute_ms for event in events)
            if events and first_partial is None:
                first_partial = events[0]
            if paced:
                sleep(len(chunk) / 16000)

        finals = backend.flush()
        all_decode_values.extend(event.compute_ms for event in finals)
        final = finals[-1] if finals else (backend.events[-1] if backend.events else None)
        text = final.text if final else ""

        current_vram = get_vram_usage_mib() if device == "cuda" else None
        if current_vram and (peak_vram is None or current_vram > peak_vram):
            peak_vram = current_vram

        audio_dur_ms = len(samples) * 1000 / 16000
        final_latency = (final.emitted_at_ms - started) if final else None
        kept_up = (final_latency is not None) and (final_latency <= audio_dur_ms + 1000)

        results.append({
            "fixture": name,
            "reference": reference,
            "hypothesis": text,
            "wer": wer(reference, text),
            "audio_duration_ms": audio_dur_ms,
            "first_partial_latency_ms": (first_partial.emitted_at_ms - started) if first_partial else None,
            "final_latency_ms": final_latency,
            "final_compute_ms": final.compute_ms if final else None,
            "final_rtf": final.rtf if final else None,
            "stale_windows_dropped": backend.stale_windows_dropped,
            "kept_up_with_audio": kept_up,
        })

    backend.stop()

    decode_values = all_decode_values if all_decode_values else [0.0]
    total_audio_ms = sum(result["audio_duration_ms"] for result in results)
    total_decode_ms = sum(decode_values)

    return {
        "model": model,
        "device": device,
        "compute_type": compute_type,
        "minimum_decode_ms": minimum_decode_ms,
        "decode_hop_ms": decode_hop_ms,
        "rolling_window_ms": rolling_window_ms,
        "async_worker": async_worker,
        "model_load_ms": load_ms,
        "vram_peak_mib": peak_vram,
        "results": results,
        "average_wer": mean(result["wer"] for result in results),
        "average_decode_ms": mean(decode_values),
        "worst_decode_ms": max(decode_values),
        "total_decode_compute_ms": total_decode_ms,
        "aggregate_rtf": total_decode_ms / max(1.0, total_audio_ms),
        "can_keep_up": (total_decode_ms / max(1.0, total_audio_ms)) < 0.8,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ASR Benchmark Suite")
    parser.add_argument("--models", nargs="+", default=["tiny.en"])
    parser.add_argument("--devices", nargs="+", default=["cpu", "cuda"])
    parser.add_argument("--compute-types", nargs="+", default=None)
    parser.add_argument("--output", default="tools/asr/benchmark_results.json")
    parser.add_argument("--paced", action="store_true", help="Feed chunks at real-time cadence for latency measurements.")
    parser.add_argument("--async-worker", action="store_true", help="Use asynchronous worker thread.")
    parser.add_argument("--min-decode-ms", type=int, default=1000)
    parser.add_argument("--decode-hop-ms", type=int, default=750)
    parser.add_argument("--rolling-window-ms", type=int, default=15000)

    args = parser.parse_args()
    fixtures = ensure_fixtures(Path(__file__).resolve().parent / "benchmark_audio")

    benchmarks = []
    for model in args.models:
        for device in args.devices:
            # Select appropriate default compute type if not specified
            compute_types = args.compute_types
            if not compute_types:
                compute_types = ["float16"] if device == "cuda" else ["int8"]
            for ct in compute_types:
                print(f"--> Benchmarking {model} on {device} ({ct})...", flush=True)
                b = benchmark(
                    model,
                    fixtures,
                    args.paced,
                    device=device,
                    compute_type=ct,
                    minimum_decode_ms=args.min_decode_ms,
                    decode_hop_ms=args.decode_hop_ms,
                    rolling_window_ms=args.rolling_window_ms,
                    async_worker=args.async_worker,
                )
                benchmarks.append(b)
                print(f"    Avg decode: {b['average_decode_ms']:.1f}ms | Worst: {b['worst_decode_ms']:.1f}ms | RTF: {b['aggregate_rtf']:.3f} | WER: {b['average_wer'] * 100:.1f}%")

    report = {"paced_input": args.paced, "benchmarks": benchmarks}
    Path(args.output).write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"\nWrote results to {args.output}")
