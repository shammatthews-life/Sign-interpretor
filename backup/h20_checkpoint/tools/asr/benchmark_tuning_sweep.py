"""Tuning sweep for Task 6 (first-partial latency) and Task 7/8/9 streaming verification."""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from tools.asr.benchmark_faster_whisper import benchmark, ensure_fixtures, wer
from tools.asr.streaming_asr import FasterWhisperBackend

fixtures = ensure_fixtures(Path("tools/asr/benchmark_audio"))

# Tuning configurations to evaluate for Task 6
configs = [
    {
        "name": "Config 1 (F2 Baseline)",
        "min_decode_ms": 1000,
        "decode_hop_ms": 750,
        "rolling_window_ms": 4000,
    },
    {
        "name": "Config 2 (Aggressive Low-Latency)",
        "min_decode_ms": 500,
        "decode_hop_ms": 350,
        "rolling_window_ms": 3000,
    },
    {
        "name": "Config 3 (Balanced Low-Latency)",
        "min_decode_ms": 750,
        "decode_hop_ms": 500,
        "rolling_window_ms": 3500,
    },
]

sweep_results = []
for cfg in configs:
    print(f"--> Sweeping {cfg['name']} (min={cfg['min_decode_ms']}ms, hop={cfg['decode_hop_ms']}ms, win={cfg['rolling_window_ms']}ms)...", flush=True)
    res = benchmark(
        "tiny.en",
        fixtures,
        paced=True,
        device="cuda",
        compute_type="float16",
        minimum_decode_ms=cfg["min_decode_ms"],
        decode_hop_ms=cfg["decode_hop_ms"],
        rolling_window_ms=cfg["rolling_window_ms"],
        async_worker=True,
    )
    res["config_name"] = cfg["name"]
    first_partial_latencies = [r["first_partial_latency_ms"] for r in res["results"] if r["first_partial_latency_ms"] is not None]
    avg_fp_lat = sum(first_partial_latencies) / len(first_partial_latencies) if first_partial_latencies else None
    res["average_first_partial_latency_ms"] = avg_fp_lat
    sweep_results.append(res)
    print(f"    Avg First Partial Latency: {avg_fp_lat:.0f}ms | Avg Decode: {res['average_decode_ms']:.1f}ms | Worst: {res['worst_decode_ms']:.1f}ms | WER: {res['average_wer']*100:.1f}%", flush=True)

out_file = Path("tools/asr/benchmark_tuning_sweep.json")
out_file.write_text(json.dumps({"sweep": sweep_results}, indent=2), encoding="utf-8")
print(f"Tuning sweep results written to {out_file}")
