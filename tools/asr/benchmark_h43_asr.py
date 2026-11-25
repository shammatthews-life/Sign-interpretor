"""tools/asr/benchmark_h43_asr.py

H43 Workstream 1: Multi-Domain Faster-Whisper GPU Benchmark & Audio Preprocessing Ablation.
Evaluates tiny.en, base.en, and small.en across 5 diverse videos (0:00-2:00) on RTX 4050 CUDA,
comparing beam sizes and FFmpeg audio preprocessing against verified human references.
"""
from __future__ import annotations

import json
import math
import re
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Dict, List

import ctranslate2
import numpy as np
from faster_whisper import WhisperModel

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "tools"))

from asr.gpu_execution import resolve_execution_configuration

REFS_PATH = ROOT / "artifacts" / "h43" / "benchmark" / "h43_multi_domain_references.json"
OUT_JSON = ROOT / "artifacts" / "h43" / "asr" / "h43_asr_experiment_results.json"
OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
PREPROC_DIR = ROOT / "artifacts" / "h43" / "asr" / "preprocessed_audio"
PREPROC_DIR.mkdir(parents=True, exist_ok=True)
FFMPEG_EXE = ROOT / ".venv" / "Lib" / "site-packages" / "imageio_ffmpeg" / "binaries" / "ffmpeg-win-x86_64-v7.1.exe"


def normalize_for_wer(text: str) -> List[str]:
    clean = text.lower()
    clean = re.sub(r"[^\w'\s]", " ", clean)
    clean = re.sub(r"\s+", " ", clean).strip()
    return [w for w in clean.split(" ") if w]


def calculate_wer(ref_words: List[str], hyp_words: List[str]) -> Dict[str, Any]:
    n, m = len(ref_words), len(hyp_words)
    d = np.zeros((n + 1, m + 1), dtype=np.uint32)
    for i in range(n + 1):
        d[i][0] = i
    for j in range(m + 1):
        d[0][j] = j
    for i in range(1, n + 1):
        rw = ref_words[i - 1]
        for j in range(1, m + 1):
            if rw == hyp_words[j - 1]:
                d[i][j] = d[i - 1][j - 1]
            else:
                d[i][j] = min(d[i - 1][j - 1] + 1, d[i][j - 1] + 1, d[i - 1][j] + 1)
    wer = d[n][m] / max(1, n)
    return {
        "wer_pct": round(float(wer) * 100.0, 2),
        "ref_words": n,
        "hyp_words": m,
        "edit_distance": int(d[n][m]),
    }


def prepare_audio_variant(video_id: str, raw_wav: Path, variant: str) -> Path:
    if variant == "raw_16k":
        return raw_wav
    out_wav = PREPROC_DIR / f"{video_id}_{variant}.wav"
    if out_wav.exists() and out_wav.stat().st_size > 10000:
        return out_wav
    af = "highpass=f=80,loudnorm=I=-16:TP=-1.5:LRA=11"
    subprocess.run(
        [str(FFMPEG_EXE), "-y", "-i", str(raw_wav), "-t", "125", "-af", af, "-ar", "16000", "-ac", "1", "-c:a", "pcm_s16le", str(out_wav)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=True,
    )
    return out_wav


def main():
    refs = json.loads(REFS_PATH.read_text(encoding="utf-8"))
    exec_cfg = resolve_execution_configuration("GPU_PREFERRED", device_index=0)
    device, compute_type = exec_cfg["device"], exec_cfg["compute_type"]

    model_configs = [
        {"name": "tiny.en_b1_raw", "model": "tiny.en", "beam": 1, "vad": True, "audio": "raw_16k"},
        {"name": "base.en_b1_raw", "model": "base.en", "beam": 1, "vad": True, "audio": "raw_16k"},
        {"name": "base.en_b5_raw", "model": "base.en", "beam": 5, "vad": True, "audio": "raw_16k"},
        {"name": "base.en_b5_norm", "model": "base.en", "beam": 5, "vad": True, "audio": "loudnorm_hp80"},
        {"name": "small.en_b5_raw", "model": "small.en", "beam": 5, "vad": True, "audio": "raw_16k"},
        {"name": "small.en_b5_norm", "model": "small.en", "beam": 5, "vad": True, "audio": "loudnorm_hp80"},
    ]

    loaded_models: Dict[str, WhisperModel] = {}
    experiments: List[Dict[str, Any]] = []

    for cfg in model_configs:
        m_name = cfg["model"]
        if m_name not in loaded_models:
            print(f"[ASR Benchmark] Loading {m_name} on {device} ({compute_type})...")
            loaded_models[m_name] = WhisperModel(
                m_name,
                device=device,
                compute_type=compute_type,
                device_index=exec_cfg.get("device_index", 0),
            )
        model = loaded_models[m_name]

        for vid, ref_data in refs["videos"].items():
            raw_wav = ROOT / "runtime" / "youtube" / vid / "audio_16k.wav"
            wav_path = prepare_audio_variant(vid, raw_wav, cfg["audio"])

            t0 = time.perf_counter()
            segs_gen, info = model.transcribe(
                str(wav_path),
                language="en",
                beam_size=cfg["beam"],
                vad_filter=cfg["vad"],
                condition_on_previous_text=False,
                clip_timestamps="0,122",
            )
            segs = []
            confs = []
            logprobs = []
            words_acc = []
            for s in segs_gen:
                if s.start >= 120.0:
                    break
                txt = s.text.strip()
                if not txt:
                    continue
                avg_lp = float(getattr(s, "avg_logprob", -0.25))
                nsp = float(getattr(s, "no_speech_prob", 0.0))
                conf = max(0.0, min(1.0, math.exp(avg_lp) * (1.0 - min(0.95, nsp))))
                confs.append(conf)
                logprobs.append(avg_lp)
                segs.append({
                    "start": round(s.start, 2),
                    "end": round(min(120.0, s.end), 2),
                    "text": txt,
                    "avg_logprob": round(avg_lp, 4),
                    "no_speech_prob": round(nsp, 4),
                    "asr_confidence": round(conf, 4),
                })
                words_acc.extend(txt.split())
            infer_s = time.perf_counter() - t0
            hyp_text = " ".join(words_acc)

            wer = calculate_wer(normalize_for_wer(ref_data["full_text"]), normalize_for_wer(hyp_text))
            row = {
                "config": cfg["name"],
                "model": m_name,
                "beam_size": cfg["beam"],
                "vad_filter": cfg["vad"],
                "audio_variant": cfg["audio"],
                "video_id": vid,
                "domain": ref_data["domain"],
                "ground_truth_status": ref_data["ground_truth_status"],
                "device": device,
                "compute_type": compute_type,
                "infer_time_s": round(infer_s, 3),
                "rtf": round(infer_s / 120.0, 4),
                "segment_count": len(segs),
                "mean_confidence": round(sum(confs) / max(1, len(confs)), 4),
                "mean_avg_logprob": round(sum(logprobs) / max(1, len(logprobs)), 4),
                "low_confidence_segments": sum(1 for c in confs if c < 0.55),
                "wer_metrics": wer,
                "segments": segs,
            }
            experiments.append(row)
            print(f"  {cfg['name']:18s} | {vid} ({ref_data['domain'][:16]:16s}) | WER={wer['wer_pct']:5.2f}% | RTF={row['rtf']:.4f} | conf={row['mean_confidence']:.3f}")

    # Aggregate mean WER per configuration
    summary_by_config: Dict[str, Any] = {}
    for cfg in model_configs:
        rows = [e for e in experiments if e["config"] == cfg["name"]]
        mean_wer = round(sum(r["wer_metrics"]["wer_pct"] for r in rows) / len(rows), 2)
        mean_rtf = round(sum(r["rtf"] for r in rows) / len(rows), 4)
        summary_by_config[cfg["name"]] = {
            "mean_wer_pct": mean_wer,
            "mean_rtf": mean_rtf,
            "per_video_wer_pct": {r["video_id"]: r["wer_metrics"]["wer_pct"] for r in rows},
        }

    payload = {
        "milestone": "H43",
        "workstream": "WS1_ASR_AND_AUDIO_PIPELINE",
        "cuda_devices": ctranslate2.get_cuda_device_count(),
        "window_seconds": 120.0,
        "summary_by_config": summary_by_config,
        "experiments": experiments,
    }
    OUT_JSON.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("\n=== SUMMARY BY CONFIG ===")
    print(json.dumps(summary_by_config, indent=2))


if __name__ == "__main__":
    main()
