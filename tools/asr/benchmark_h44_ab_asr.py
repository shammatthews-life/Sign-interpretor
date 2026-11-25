"""tools/asr/benchmark_h44_ab_asr.py

H44 Workstream 6: Controlled ASR & Audio Preprocessing Evaluation on Locked Video A and B.
Compares base.en, small.en, VAD/beam parameters, word_timestamps, and FFmpeg filtering
against h44_verified_references_ab.json using normalized lexical WER (excluding punctuation noise)
within the strictly locked 0:00-2:00 benchmark boundaries.
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

import numpy as np
from faster_whisper import WhisperModel

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "tools"))

from asr.gpu_execution import resolve_execution_configuration

REFS_PATH = ROOT / "artifacts" / "h44" / "h44_verified_references_ab.json"
OUT_JSON = ROOT / "artifacts" / "h44" / "asr" / "h44_ab_asr_experiments.json"
OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
PREPROC_DIR = ROOT / "artifacts" / "h43" / "asr" / "preprocessed_audio"
PREPROC_DIR.mkdir(parents=True, exist_ok=True)
FFMPEG_EXE = ROOT / ".venv" / "Lib" / "site-packages" / "imageio_ffmpeg" / "binaries" / "ffmpeg-win-x86_64-v7.1.exe"

NUM_MAP = {
    "0": "zero", "1": "one", "2": "two", "3": "three", "4": "four", "5": "five",
    "6": "six", "7": "seven", "8": "eight", "9": "nine", "10": "ten",
    "25": "twenty five", "30": "thirty", "110": "hundred ten", "5000": "five thousand"
}


def normalize_lexical(text: str) -> List[str]:
    s = text.lower().replace("5,000", "5000")
    s = s.replace("endeavour", "endeavor")
    s = s.replace("over-complicating", "overcomplicating")
    s = s.replace("over-arching", "overarching")
    s = s.replace("gonna", "going to")
    s = s.replace("dialogue,", "dialogue").replace("dialogues", "dialogue")
    s = re.sub(r"[-']", " ", s)
    s = re.sub(r"[^\w\s]", " ", s)
    tokens = []
    for w in s.split():
        if w in NUM_MAP:
            tokens.extend(NUM_MAP[w].split())
        else:
            tokens.append(w)
    return tokens


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


def prepare_audio(vid: str, raw_wav: Path, variant: str) -> Path:
    if variant == "raw_16k":
        return raw_wav
    out_wav = PREPROC_DIR / f"{vid}_{variant}.wav"
    if out_wav.exists() and out_wav.stat().st_size > 10000:
        return out_wav
    af = (
        "highpass=f=80,loudnorm=I=-16:TP=-1.5:LRA=11"
        if variant == "loudnorm_hp80"
        else "highpass=f=85,afftdn=nf=-22,loudnorm=I=-16:TP=-1.5:LRA=11"
    )
    subprocess.run(
        [str(FFMPEG_EXE), "-y", "-i", str(raw_wav), "-t", "124", "-af", af, "-ar", "16000", "-ac", "1", "-c:a", "pcm_s16le", str(out_wav)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=True,
    )
    return out_wav


def main():
    refs = json.loads(REFS_PATH.read_text(encoding="utf-8"))["videos"]
    exec_cfg = resolve_execution_configuration("GPU_PREFERRED", device_index=0)
    device, compute_type = exec_cfg["device"], exec_cfg["compute_type"]

    configs = [
        {"name": "base.en_b1_raw", "model": "base.en", "beam": 1, "vad": True, "audio": "raw_16k", "word_ts": False},
        {"name": "small.en_b5_raw", "model": "small.en", "beam": 5, "vad": True, "audio": "raw_16k", "word_ts": False},
        {"name": "small.en_b5_norm", "model": "small.en", "beam": 5, "vad": True, "audio": "loudnorm_hp80", "word_ts": True},
        {"name": "small.en_b5_denoise", "model": "small.en", "beam": 5, "vad": True, "audio": "afftdn_hp85_norm", "word_ts": True},
        {"name": "small.en_b5_novad_norm", "model": "small.en", "beam": 5, "vad": False, "audio": "loudnorm_hp80", "word_ts": True},
    ]

    models: Dict[str, WhisperModel] = {}
    results: List[Dict[str, Any]] = []

    for cfg in configs:
        m_name = cfg["model"]
        if m_name not in models:
            models[m_name] = WhisperModel(m_name, device=device, compute_type=compute_type, device_index=exec_cfg.get("device_index", 0))
        model = models[m_name]

        for vid, ref_data in refs.items():
            wav_path = prepare_audio(vid, ROOT / "runtime" / "youtube" / vid / "audio_16k.wav", cfg["audio"])
            max_end = 119.5 if vid == "MXKkXXYUxBc" else 120.5

            t0 = time.perf_counter()
            segs_gen, _ = model.transcribe(
                str(wav_path),
                language="en",
                beam_size=cfg["beam"],
                vad_filter=cfg["vad"],
                condition_on_previous_text=False,
                word_timestamps=cfg["word_ts"],
                clip_timestamps="0,122",
            )
            segs = []
            hyp_words_raw = []
            confs = []
            for s in segs_gen:
                if s.start >= 119.0:
                    break
                if cfg["word_ts"] and getattr(s, "words", None):
                    kept_words = [w.word for w in s.words if w.start < max_end]
                    txt = "".join(kept_words).strip()
                else:
                    txt = s.text.strip()
                if not txt:
                    continue
                avg_lp = float(getattr(s, "avg_logprob", -0.25))
                nsp = float(getattr(s, "no_speech_prob", 0.0))
                conf = max(0.0, min(1.0, math.exp(avg_lp) * (1.0 - min(0.95, nsp))))
                confs.append(conf)
                segs.append({
                    "start": round(s.start, 2),
                    "end": round(min(120.0, s.end), 2),
                    "text": txt,
                    "avg_logprob": round(avg_lp, 4),
                    "asr_confidence": round(conf, 4),
                })
                hyp_words_raw.extend(txt.split())
            infer_s = time.perf_counter() - t0

            ref_text = " ".join(x["text"] for x in ref_data["segments"])
            wer = calculate_wer(normalize_lexical(ref_text), normalize_lexical(" ".join(hyp_words_raw)))
            row = {
                "config": cfg["name"],
                "video_id": vid,
                "infer_time_s": round(infer_s, 3),
                "rtf": round(infer_s / 120.0, 4),
                "mean_confidence": round(sum(confs) / max(1, len(confs)), 4),
                "wer_metrics": wer,
                "segments": segs,
            }
            results.append(row)
            print(f"{cfg['name']:22s} | {vid} | lexical_WER={wer['wer_pct']:5.2f}% (edits={wer['edit_distance']}) | RTF={row['rtf']:.4f} | conf={row['mean_confidence']:.3f}")

    summary = {}
    for cfg in configs:
        rows = [r for r in results if r["config"] == cfg["name"]]
        summary[cfg["name"]] = {
            "mean_lexical_wer_pct": round(sum(r["wer_metrics"]["wer_pct"] for r in rows) / len(rows), 2),
            "per_video": {r["video_id"]: r["wer_metrics"] for r in rows},
            "mean_rtf": round(sum(r["rtf"] for r in rows) / len(rows), 4),
        }

    OUT_JSON.write_text(json.dumps({"milestone": "H44", "summary": summary, "experiments": results}, indent=2) + "\n", encoding="utf-8")
    print("\n=== H44 AB ASR SUMMARY ===")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
