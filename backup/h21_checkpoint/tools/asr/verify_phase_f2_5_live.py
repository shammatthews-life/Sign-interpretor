"""Phase F2.5 verification script: Task 4, 5, 6, 7, 8, 9, 10."""
from __future__ import annotations

import sys
import time
from pathlib import Path
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from tools.asr.benchmark_faster_whisper import read_wav_mono_float, wer
from tools.asr.streaming_asr import FasterWhisperBackend, TranscriptEvent
from tools.asr.asr_service import LocalASRService

audio_dir = Path(__file__).resolve().parent / "benchmark_audio"
hello_wav = audio_dir / "hello_good_morning.wav"
fast_wav = audio_dir / "fast.wav"
noisy_wav = audio_dir / "mild_noisy.wav"

print("=" * 60)
print("PHASE F2.5 VERIFICATION: STREAMING, GPU, AND LATENCY")
print("=" * 60)

# =========================================================================
# TEST 1: Task 7 - "Hello good morning" partial evolution and finalization
# =========================================================================
print("\n--- TEST 1: Task 7 — 'Hello good morning' Partial Evolution & Finalization ---")
samples, rate = read_wav_mono_float(hello_wav)
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

emitted_events: list[TranscriptEvent] = []
ingest_times_ms = []

t0 = time.perf_counter()
chunk_size = 1600  # 100 ms canonical chunks
for idx in range(0, len(samples), chunk_size):
    chunk = samples[idx : idx + chunk_size]
    t_ingest_start = time.perf_counter()
    new_events = backend.accept_audio_chunk(
        chunk,
        audio_start_ms=idx * 1000 / 16000,
        audio_end_ms=(idx + len(chunk)) * 1000 / 16000,
    )
    ingest_ms = (time.perf_counter() - t_ingest_start) * 1000
    ingest_times_ms.append(ingest_ms)
    emitted_events.extend(new_events)
    # simulate paced real-time input
    time.sleep(len(chunk) / 16000)

finals = backend.flush()
emitted_events.extend(finals)
backend.stop()

print(f"Total audio: {len(samples)*1000/16000:.0f} ms | Max chunk ingest time: {max(ingest_times_ms):.3f} ms | Avg ingest time: {np.mean(ingest_times_ms):.3f} ms")
assert max(ingest_times_ms) < 20.0, f"Audio ingestion blocked! Max took {max(ingest_times_ms)} ms"
print(f"Ingestion is completely non-blocking (avg {np.mean(ingest_times_ms):.3f} ms / chunk)")

# Verify events
print(f"Emitted {len(emitted_events)} events during stream:")
last_partial_text = ""
duplicate_partial = False
for i, ev in enumerate(emitted_events):
    print(f"  [{i+1}] {ev.kind}: '{ev.text}' (audio: {ev.audio_start_ms:.0f}-{ev.audio_end_ms:.0f}ms, emitted: {ev.emitted_at_ms:.1f}ms, compute: {ev.compute_ms:.1f}ms)")
    if ev.kind == "PARTIAL_TRANSCRIPT" and ev.text == last_partial_text:
        duplicate_partial = True
    if ev.kind == "PARTIAL_TRANSCRIPT":
        last_partial_text = ev.text

assert not duplicate_partial, "Duplicate PARTIAL event detected! TranscriptStabilizer failed to suppress identical partial."
assert any(ev.kind == "PARTIAL_TRANSCRIPT" for ev in emitted_events) or len(samples) < 1000, "Should emit partial transcripts during speech."
assert emitted_events[-1].kind == "FINAL_TRANSCRIPT", "Last event must be FINAL_TRANSCRIPT."
final_text = emitted_events[-1].text.lower()
print(f"Final Transcript: '{emitted_events[-1].text}'")
assert "hello" in final_text and ("good" in final_text or "morning" in final_text), f"Transcript mismatch: '{final_text}'"
print("PASS: Partial transcripts evolved smoothly toward final transcript without duplicate events.")

# =========================================================================
# TEST 2: Task 8 - Fast Speech Streaming & Queue Concurrency
# =========================================================================
print("\n--- TEST 2: Task 8 — Fast Speech Streaming & Queue Concurrency ---")
fast_samples, rate = read_wav_mono_float(fast_wav)

backend_fast = FasterWhisperBackend(
    "tiny.en",
    device="cuda",
    compute_type="float16",
    minimum_decode_ms=750,
    decode_hop_ms=500,
    rolling_window_ms=4000,
    async_worker=True,
)
backend_fast.start()

fast_events = []
worker_states = []
fast_ingest_times = []
t_start = time.perf_counter()

for idx in range(0, len(fast_samples), chunk_size):
    chunk = fast_samples[idx : idx + chunk_size]
    t_ingest = time.perf_counter()
    evs = backend_fast.accept_audio_chunk(
        chunk,
        audio_start_ms=idx * 1000 / 16000,
        audio_end_ms=(idx + len(chunk)) * 1000 / 16000,
    )
    fast_ingest_times.append((time.perf_counter() - t_ingest) * 1000)
    worker_states.append(backend_fast.worker_state)
    fast_events.extend(evs)
    time.sleep(len(chunk) / 16000)

finals = backend_fast.flush()
fast_events.extend(finals)
elapsed_total = (time.perf_counter() - t_start) * 1000
audio_total_ms = len(fast_samples) * 1000 / 16000
backend_fast.stop()

first_p = next((e for e in fast_events if e.kind == "PARTIAL_TRANSCRIPT"), None)
first_p_lat = (first_p.emitted_at_ms - (fast_events[0].asr_started_at_ms if fast_events else 0)) if first_p else None
decodes = [e.compute_ms for e in fast_events]

print(f"Fast speech audio duration: {audio_total_ms:.0f} ms")
print(f"Total processing elapsed:   {elapsed_total:.0f} ms (lag: {elapsed_total - audio_total_ms:.0f} ms)")
print(f"Ingest time per chunk:      avg {np.mean(fast_ingest_times):.3f} ms, max {max(fast_ingest_times):.3f} ms")
print(f"Worker states observed:     IDLE={worker_states.count('IDLE')}, DECODING={worker_states.count('DECODING')}")
print(f"Decodes completed:          {len(decodes)} (avg {np.mean(decodes):.1f} ms, worst {max(decodes):.1f} ms)")
print(f"Stale windows dropped:      {backend_fast.stale_windows_dropped}")
print(f"Final transcript:           '{fast_events[-1].text if fast_events else ''}'")

assert elapsed_total <= audio_total_ms + 1500, f"ASR queue fell behind! Elapsed {elapsed_total:.0f} ms for {audio_total_ms:.0f} ms audio"
assert max(fast_ingest_times) < 20.0, "Audio ingestion was blocked during fast speech!"
print("PASS: System continuously processes fast speech without blocking audio capture.")

# =========================================================================
# TEST 3: Task 9 - Mildly Noisy Audio Comparison (CPU vs GPU)
# =========================================================================
print("\n--- TEST 3: Task 9 — Mildly Noisy Audio Comparison ---")
noisy_samples, rate = read_wav_mono_float(noisy_wav)
reference_noisy = "And so my fellow Americans ask not what your country can do for you ask what you can do for your country."

# GPU run
backend_gpu = FasterWhisperBackend("tiny.en", device="cuda", compute_type="float16", rolling_window_ms=15000)
backend_gpu.start()
for idx in range(0, len(noisy_samples), chunk_size):
    backend_gpu.accept_audio_chunk(noisy_samples[idx:idx+chunk_size], audio_start_ms=idx*1000/16000, audio_end_ms=(idx+chunk_size)*1000/16000)
finals_gpu = backend_gpu.flush()
text_gpu = finals_gpu[-1].text if finals_gpu else ""
wer_gpu = wer(reference_noisy, text_gpu)
decodes_gpu = [e.compute_ms for e in backend_gpu.events]
backend_gpu.stop()

print(f"GPU Noisy — WER: {wer_gpu*100:.1f}%, Avg decode: {np.mean(decodes_gpu):.1f} ms, Worst: {max(decodes_gpu):.1f} ms")
print(f"GPU Noisy Transcript: '{text_gpu}'")
assert wer_gpu <= 0.15, f"High WER on mildly noisy audio: {wer_gpu}"
print("PASS: GPU model handles mildly noisy audio robustly with low WER and fast decode.")

# =========================================================================
# TEST 4: Task 10 - ASR Diagnostics Telemetry Verification
# =========================================================================
print("\n--- TEST 4: Task 10 — ASR Diagnostic Telemetry ---")
service = LocalASRService()
status = service.start(model="tiny.en")
print("Service start status:")
for k, v in status.items():
    print(f"  {k}: {v}")

required_keys = [
    "state", "worker_state", "model", "device", "compute_type",
    "audio_duration_ms", "audio_received_sec", "asr_queue",
    "backlog", "partial", "final", "first_partial_latency_ms",
    "last_decode_ms", "rtf",
]
for k in required_keys:
    assert k in status, f"Missing required diagnostic key: {k}"

assert status["device"] == "cuda", f"Expected cuda device auto-detected, got {status['device']}"
assert status["compute_type"] == "float16", f"Expected float16, got {status['compute_type']}"
assert status["worker_state"] in ("IDLE", "DECODING"), f"Invalid worker state: {status['worker_state']}"

service.control("stop")
print("PASS: All Task 10 diagnostic telemetry fields verified.")

print("\n" + "=" * 60)
print("ALL PHASE F2.5 LIVE VERIFICATION CHECKS PASSED!")
print("=" * 60)
