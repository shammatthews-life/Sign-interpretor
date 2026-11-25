"""tools/asr/benchmark_h42_asr.py

Milestone H42 Workstream 1: ASR, Audio Pipeline & Transcription Intelligence
Comparative experimental evaluation of Faster-Whisper configurations across Benchmark Video A and Video B.
"""
from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path
from typing import Any, Dict, List

import numpy as np
import ctranslate2
from faster_whisper import WhisperModel

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "tools"))

from asr.gpu_execution import resolve_execution_configuration

VIDEO_A_AUDIO = PROJECT_ROOT / "runtime" / "youtube" / "MXKkXXYUxBc" / "audio_16k.wav"
VIDEO_B_AUDIO = PROJECT_ROOT / "runtime" / "youtube" / "y8tFSuOMAqQ" / "audio_16k.wav"

OUTPUT_JSON = PROJECT_ROOT / "artifacts" / "h42" / "asr" / "h42_asr_experiment_results.json"
OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)


def calculate_wer(ref_tokens: List[str], hyp_tokens: List[str]) -> Dict[str, Any]:
    """Levenshtein word error rate calculation."""
    d = np.zeros((len(ref_tokens) + 1, len(hyp_tokens) + 1), dtype=np.uint32)
    for i in range(len(ref_tokens) + 1):
        d[i][0] = i
    for j in range(len(hyp_tokens) + 1):
        d[0][j] = j

    for i in range(1, len(ref_tokens) + 1):
        for j in range(1, len(hyp_tokens) + 1):
            if ref_tokens[i - 1].lower() == hyp_tokens[j - 1].lower():
                d[i][j] = d[i - 1][j - 1]
            else:
                substitution = d[i - 1][j - 1] + 1
                insertion = d[i][j - 1] + 1
                deletion = d[i - 1][j] + 1
                d[i][j] = min(substitution, insertion, deletion)

    wer = d[len(ref_tokens)][len(hyp_tokens)] / max(1, len(ref_tokens))
    return {
        "wer_pct": round(float(wer) * 100, 2),
        "ref_word_count": len(ref_tokens),
        "hyp_word_count": len(hyp_tokens),
        "edit_distance": int(d[len(ref_tokens)][len(hyp_tokens)]),
    }


def run_experiment(
    model_size: str,
    beam_size: int,
    vad_filter: bool,
    audio_path: Path,
    video_id: str,
    target_duration_s: float = 120.0,
) -> Dict[str, Any]:
    """Execute single ASR inference run and record telemetry."""
    print(f"\n--- Testing [{video_id}] Model: {model_size}, Beam: {beam_size}, VAD: {vad_filter} ---")
    
    exec_cfg = resolve_execution_configuration("GPU_PREFERRED", device_index=0)
    device = exec_cfg["device"]
    compute_type = exec_cfg["compute_type"]

    t0_load = time.perf_counter()
    model = WhisperModel(
        model_size,
        device=device,
        compute_type=compute_type,
        device_index=exec_cfg.get("device_index", 0)
    )
    load_time_s = time.perf_counter() - t0_load

    t0_infer = time.perf_counter()
    segments_generator, info = model.transcribe(
        str(audio_path),
        language="en",
        beam_size=beam_size,
        vad_filter=vad_filter,
        condition_on_previous_text=False,
    )

    collected_segments = []
    full_text_words = []
    for s in segments_generator:
        if s.start >= target_duration_s:
            break
        text = s.text.strip()
        if text:
            clamped_end = min(target_duration_s, s.end)
            collected_segments.append({
                "start": round(s.start, 2),
                "end": round(clamped_end, 2),
                "duration": round(clamped_end - s.start, 2),
                "text": text,
                "words": text.split(),
            })
            full_text_words.extend(text.split())

    infer_time_s = time.perf_counter() - t0_infer
    rtf = infer_time_s / target_duration_s

    print(f"  Duration: {target_duration_s:.1f}s | Infer: {infer_time_s:.2f}s | RTF: {rtf:.4f} | Device: {device} ({compute_type})")
    print(f"  Segments: {len(collected_segments)} | Word Count: {len(full_text_words)}")

    return {
        "video_id": video_id,
        "model_size": model_size,
        "beam_size": beam_size,
        "vad_filter": vad_filter,
        "device": device,
        "compute_type": compute_type,
        "load_time_s": round(load_time_s, 2),
        "infer_time_s": round(infer_time_s, 2),
        "rtf": round(rtf, 4),
        "segment_count": len(collected_segments),
        "word_count": len(full_text_words),
        "full_text": " ".join(full_text_words),
        "segments": collected_segments,
    }


def main():
    print("===========================================================================")
    print("H42 WORKSTREAM 1: ASR & SPEECH CONTEXT INTELLIGENCE EXPERIMENTATION")
    print("Backend: Faster-Whisper (ctranslate2 CUDA float16 on NVIDIA RTX 4050)")
    print("===========================================================================")

    configs = [
        {"model_size": "tiny.en", "beam_size": 1, "vad_filter": True},
        {"model_size": "tiny.en", "beam_size": 5, "vad_filter": True},
        {"model_size": "base.en", "beam_size": 1, "vad_filter": True},
        {"model_size": "base.en", "beam_size": 5, "vad_filter": True},
        {"model_size": "base.en", "beam_size": 5, "vad_filter": False},
    ]

    results = {
        "milestone": "H42",
        "workstream": "WS1_ASR_AND_AUDIO_PIPELINE",
        "created_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "cuda_devices": ctranslate2.get_cuda_device_count(),
        "experiments": [],
    }

    # Reference transcripts for 0:00 - 2:00
    video_a_ref_path = PROJECT_ROOT / "artifacts" / "h42" / "benchmark" / "h42_video_a_locked_benchmark.json"
    with open(video_a_ref_path, "r", encoding="utf-8") as f:
        video_a_bench = json.load(f)
    video_a_ref_words = [w for s in video_a_bench["segments"] for w in s["source_text"].split()]

    video_b_ref_path = PROJECT_ROOT / "artifacts" / "h42" / "benchmark" / "h42_video_b_locked_benchmark.json"
    with open(video_b_ref_path, "r", encoding="utf-8") as f:
        video_b_bench = json.load(f)
    video_b_ref_words = [w for s in video_b_bench["segments"] for w in s["source_text"].split()]

    for cfg in configs:
        # Run on Video A
        res_a = run_experiment(
            model_size=cfg["model_size"],
            beam_size=cfg["beam_size"],
            vad_filter=cfg["vad_filter"],
            audio_path=VIDEO_A_AUDIO,
            video_id="MXKkXXYUxBc",
        )
        wer_a = calculate_wer(video_a_ref_words, res_a["full_text"].split())
        res_a["wer_metrics"] = wer_a
        results["experiments"].append(res_a)

        # Run on Video B
        res_b = run_experiment(
            model_size=cfg["model_size"],
            beam_size=cfg["beam_size"],
            vad_filter=cfg["vad_filter"],
            audio_path=VIDEO_B_AUDIO,
            video_id="y8tFSuOMAqQ",
        )
        wer_b = calculate_wer(video_b_ref_words, res_b["full_text"].split())
        res_b["wer_metrics"] = wer_b
        results["experiments"].append(res_b)

    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print(f"\nSaved ASR experimental results to: {OUTPUT_JSON}")
    print("\n===========================================================================")
    print("  ASR COMPARATIVE SUMMARY")
    print("===========================================================================")
    print(f"{'Video':<12} | {'Model':<8} | {'Beam':<5} | {'VAD':<5} | {'RTF':<8} | {'WER (%)':<8} | {'Word Count'}")
    print("-" * 72)
    for exp in results["experiments"]:
        v = exp["video_id"]
        m = exp["model_size"]
        b = exp["beam_size"]
        vad = "YES" if exp["vad_filter"] else "NO"
        rtf = exp["rtf"]
        wer = exp["wer_metrics"]["wer_pct"]
        cnt = exp["word_count"]
        print(f"{v:<12} | {m:<8} | {b:<5} | {vad:<5} | {rtf:<8.4f} | {wer:<8.2f} | {cnt}")


if __name__ == "__main__":
    main()
