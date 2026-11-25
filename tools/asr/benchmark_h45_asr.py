"""tools/asr/benchmark_h45_asr.py

H45 Workstream 6: RTX 4050 CUDA ASR Ablation (small.en vs medium.en vs domain initial_prompt)
against independently verified references in h44_verified_references_ab.json.
"""
from __future__ import annotations

import json
import math
import time
from pathlib import Path
from typing import Any, Dict, List

from faster_whisper import WhisperModel

import sys
ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "tools"))

from asr.benchmark_h44_ab_asr import calculate_wer, normalize_lexical, REFS_PATH, PREPROC_DIR
from asr.gpu_execution import resolve_execution_configuration

OUT_JSON = ROOT / "artifacts" / "h45" / "asr" / "h45_asr_ablation.json"
OUT_JSON.parent.mkdir(parents=True, exist_ok=True)


def run_config(model_size: str, name: str, initial_prompt: str | None = None) -> Dict[str, Any]:
    resolved = resolve_execution_configuration(execution_mode="GPU_REQUIRED")
    model = WhisperModel(
        model_size,
        device=resolved["device"],
        device_index=resolved["device_index"],
        compute_type=resolved["compute_type"],
    )
    refs = json.loads(REFS_PATH.read_text(encoding="utf-8"))
    per_video = {}

    for vid in ("MXKkXXYUxBc", "y8tFSuOMAqQ"):
        wav_path = PREPROC_DIR / f"{vid}_loudnorm_hp80.wav"
        ref_full = " ".join(seg["text"] for seg in refs["videos"][vid]["segments"])
        ref_words = normalize_lexical(ref_full)

        t0 = time.perf_counter()
        segs_gen, _ = model.transcribe(
            str(wav_path),
            language="en",
            beam_size=5,
            condition_on_previous_text=False,
            vad_filter=True,
            vad_parameters={"min_silence_duration_ms": 350},
            word_timestamps=True,
            initial_prompt=initial_prompt,
        )
        segs = []
        hyp_parts = []
        for s in segs_gen:
            txt = s.text.strip()
            if txt:
                avg_lp = float(getattr(s, "avg_logprob", -0.25))
                no_sp = float(getattr(s, "no_speech_prob", 0.0))
                conf = max(0.0, min(1.0, math.exp(avg_lp) * (1.0 - min(0.95, no_sp))))
                segs.append({"start": round(s.start, 2), "end": round(s.end, 2), "text": txt, "asr_confidence": round(conf, 4)})
                hyp_parts.append(txt)
        dt = time.perf_counter() - t0
        hyp_words = normalize_lexical(" ".join(hyp_parts))
        wer = calculate_wer(ref_words, hyp_words)
        per_video[vid] = {
            "wer_pct": wer["wer_pct"],
            "edit_distance": wer["edit_distance"],
            "ref_words": wer["ref_words"],
            "hyp_words": wer["hyp_words"],
            "infer_time_s": round(dt, 3),
            "rtf": round(dt / 120.0, 4),
            "segment_count": len(segs),
            "segments": segs,
        }

    mean_wer = round(sum(v["wer_pct"] for v in per_video.values()) / 2.0, 2)
    mean_rtf = round(sum(v["rtf"] for v in per_video.values()) / 2.0, 4)
    return {"config": name, "model": model_size, "initial_prompt": bool(initial_prompt), "mean_wer_pct": mean_wer, "mean_rtf": mean_rtf, "per_video": per_video}


def main() -> None:
    experiments: List[Dict[str, Any]] = []
    for cfg in [
        ("base.en", "base.en_b5_norm", None),
        ("small.en", "small.en_b5_norm", None),
        ("small.en", "small.en_b5_norm_prompt", "Public speaking, TEDx, Oracle, Google, Disney, David JP Phillips, vlogging, overarching story, dialogue."),
    ]:
        print(f"Running {cfg[1]} ({cfg[0]}) on RTX 4050 CUDA...")
        res = run_config(*cfg)
        experiments.append(res)
        print(f"  -> mean_wer={res['mean_wer_pct']}%, mean_rtf={res['mean_rtf']} | A={res['per_video']['MXKkXXYUxBc']['wer_pct']}%, B={res['per_video']['y8tFSuOMAqQ']['wer_pct']}%")

    payload = {"milestone": "H45", "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "experiments": experiments}
    OUT_JSON.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"Saved H45 ASR ablation to {OUT_JSON}")


if __name__ == "__main__":
    main()
