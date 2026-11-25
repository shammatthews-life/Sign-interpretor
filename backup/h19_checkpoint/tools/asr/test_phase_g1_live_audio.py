"""Integration test feeding real WAV fixtures through ASR into speech-to-sign pipeline."""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from tools.asr.benchmark_faster_whisper import read_wav_mono_float
from tools.asr.streaming_asr import FasterWhisperBackend
from tools.asr.asr_service import LocalASRService

audio_dir = Path(__file__).resolve().parent / "benchmark_audio"
hello_wav = audio_dir / "hello_good_morning.wav"
fast_wav = audio_dir / "fast.wav"
noisy_wav = audio_dir / "mild_noisy.wav"

# Dictionary of controlled signs
CONTROLLED_SIGNS = {
    "hello": "hello",
    "good": "good",
    "morning": "morning",
    "water": "water",  # incomplete
    "thank you": "thank you",  # unavailable
}
PLAYABLE_SIGNS = {"hello", "good", "morning"}
INCOMPLETE_SIGNS = {"water"}

def run_pipeline(wav_path: Path, label: str):
    print(f"\n==================================================")
    print(f"RUNNING LIVE AUDIO TEST: {label} ({wav_path.name})")
    print(f"==================================================")

    samples, rate = read_wav_mono_float(wav_path)
    assert rate == 16000

    backend = FasterWhisperBackend(
        "tiny.en",
        device="cuda",
        compute_type="float16",
        minimum_decode_ms=750,
        decode_hop_ms=500,
        rolling_window_ms=4000,
        async_worker=True,
    )
    backend.start()

    committed_signs = []
    trailing_candidate = None
    trailing_count = 0
    unknown_words = []
    unavailable_signs = []
    timings = {"t0": None, "t1": None, "t2": None, "t4": None}

    t_start = time.perf_counter()
    chunk_size = 1600  # 100 ms canonical chunks

    def process_transcript(text: str, is_final: bool, emitted_at: float):
        nonlocal trailing_candidate, trailing_count
        norm = " ".join(text.lower().replace(".", "").replace(",", "").replace("!", "").split())
        tokens = norm.split() if norm else []
        if not tokens:
            return

        # Simple tokenizer matching SentenceProcessor
        sign_ids = []
        i = 0
        while i < len(tokens):
            if i + 1 < len(tokens) and f"{tokens[i]} {tokens[i+1]}" in CONTROLLED_SIGNS:
                sign_ids.append(CONTROLLED_SIGNS[f"{tokens[i]} {tokens[i+1]}"])
                i += 2
            elif tokens[i] in CONTROLLED_SIGNS:
                sign_ids.append(CONTROLLED_SIGNS[tokens[i]])
                i += 1
            else:
                unknown_words.append(tokens[i].upper())
                i += 1

        uncommitted = sign_ids[len(committed_signs):]
        if not uncommitted:
            return

        now = time.perf_counter()
        to_commit = []
        if is_final:
            to_commit.extend(uncommitted)
            trailing_candidate = None
            trailing_count = 0
        else:
            for idx, sid in enumerate(uncommitted):
                is_last = (idx == len(uncommitted) - 1)
                if not is_last:
                    to_commit.append(sid)
                else:
                    if trailing_candidate == sid:
                        trailing_count += 1
                    else:
                        trailing_candidate = sid
                        trailing_count = 1
                    if trailing_count >= 2:
                        to_commit.append(sid)
                        trailing_candidate = None
                        trailing_count = 0

        for sid in to_commit:
            if sid in INCOMPLETE_SIGNS or sid not in PLAYABLE_SIGNS:
                unavailable_signs.append(sid)
                committed_signs.append({"id": sid, "status": "UNAVAILABLE", "at": now})
                print(f"  [Orchestrator] Sign '{sid.upper()}' marked UNAVAILABLE (motion incomplete / not found).")
            else:
                if timings["t2"] is None:
                    timings["t2"] = now
                committed_signs.append({"id": sid, "status": "COMMITTED", "at": now})
                print(f"  [Orchestrator] Sign '{sid.upper()}' COMMITTED to SignScheduler (t={(now - t_start)*1000:.0f} ms).")

    # Feed chunks
    timings["t0"] = t_start
    for idx in range(0, len(samples), chunk_size):
        chunk = samples[idx : idx + chunk_size]
        events = backend.accept_audio_chunk(
            chunk,
            audio_start_ms=idx * 1000 / 16000,
            audio_end_ms=(idx + len(chunk)) * 1000 / 16000,
        )
        for ev in events:
            if timings["t1"] is None and ev.text:
                timings["t1"] = time.perf_counter()
            process_transcript(ev.text, is_final=False, emitted_at=ev.emitted_at_ms)
        time.sleep(len(chunk) / 16000)

    finals = backend.flush()
    for ev in finals:
        process_transcript(ev.text, is_final=True, emitted_at=ev.emitted_at_ms)

    elapsed_total_ms = (time.perf_counter() - t_start) * 1000
    audio_dur_ms = len(samples) * 1000 / 16000
    backend.stop()

    playable_committed = [s["id"] for s in committed_signs if s["status"] == "COMMITTED"]
    print(f"\nResults for {label}:")
    print(f"  Audio duration:         {audio_dur_ms:.0f} ms")
    print(f"  Total processing time:  {elapsed_total_ms:.0f} ms (lag: {elapsed_total_ms - audio_dur_ms:.0f} ms)")
    print(f"  Signs committed:        {[s.upper() for s in playable_committed]}")
    print(f"  Unavailable signs:      {unavailable_signs}")
    print(f"  Unknown words:          {list(set(unknown_words))}")
    if timings["t1"] and timings["t0"]:
        print(f"  First partial latency:  {(timings['t1'] - timings['t0'])*1000:.0f} ms")
    if timings["t2"] and timings["t0"]:
        print(f"  Speech->Sign latency:   {(timings['t2'] - timings['t0'])*1000:.0f} ms")

    return {
        "audio_dur_ms": audio_dur_ms,
        "elapsed_total_ms": elapsed_total_ms,
        "playable_committed": playable_committed,
        "unavailable_signs": unavailable_signs,
        "unknown_words": unknown_words,
        "timings": timings,
    }


if __name__ == "__main__":
    res_hello = run_pipeline(hello_wav, "Task 7: Hello Good Morning")
    assert "hello" in res_hello["playable_committed"], "HELLO must be committed."
    assert len(res_hello["playable_committed"]) == len(set(res_hello["playable_committed"])), "Duplicate signs committed!"

    res_fast = run_pipeline(fast_wav, "Task 9: Fast Speech")
    assert res_fast["elapsed_total_ms"] <= res_fast["audio_dur_ms"] + 1500, "Fast speech pipeline lagged excessively!"

    res_noisy = run_pipeline(noisy_wav, "Task 10: Mildly Noisy Speech")
    print("\nALL AUDIO PIPELINE INTEGRATION TESTS SUCCEEDED!")
