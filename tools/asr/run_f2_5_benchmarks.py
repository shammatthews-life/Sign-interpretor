"""Execute the Phase F2.5 comprehensive benchmarks comparing CPU vs GPU configurations."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from tools.asr.benchmark_faster_whisper import benchmark, ensure_fixtures

fixtures = ensure_fixtures(Path("tools/asr/benchmark_audio"))

configs = [
    ("tiny.en", "cpu", "int8"),
    ("tiny.en", "cuda", "float16"),
    ("tiny.en", "cuda", "int8_float16"),
    ("base.en", "cuda", "float16"),
]

benchmarks = []
for model, device, ct in configs:
    print(f"--> Benchmarking {model} on {device} ({ct})...", flush=True)
    res = benchmark(model, fixtures, paced=True, device=device, compute_type=ct)
    benchmarks.append(res)
    avg_d = res["average_decode_ms"]
    worst_d = res["worst_decode_ms"]
    rtf = res["aggregate_rtf"]
    wer_pct = res["average_wer"] * 100
    vram = res.get("vram_peak_mib")
    load_ms = res["model_load_ms"]
    print(f"    Load: {load_ms:.0f}ms | Avg: {avg_d:.1f}ms | Worst: {worst_d:.1f}ms | RTF: {rtf:.3f} | WER: {wer_pct:.1f}% | VRAM: {vram} MiB", flush=True)

output_path = Path("tools/asr/benchmark_phase_f2_5.json")
output_path.write_text(json.dumps({"benchmarks": benchmarks}, indent=2), encoding="utf-8")
print(f"\nAll F2.5 benchmarks completed and saved to {output_path}")
