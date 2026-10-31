"""
tools/test_h30_incremental_asr.py
Phase H30 Workstream C: Incremental ASR & Early Transcript Finalization.
Simulates real-time streaming audio ingestion with early segment emission.
"""

import os
import sys
import time
import json
import wave
import numpy as np
from faster_whisper import WhisperModel

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(PROJECT_ROOT)

AUDIO_SRC = "runtime/h29_benchmark_60s.wav"
OUTPUT_JSON = "data/h30_incremental_asr_results.json"

class IncrementalASREngine:
    def __init__(self, model):
        self.model = model
        self.finalized_segments = []
        self.high_water_mark_s = 0.0
        self.segment_counter = 0

    def process_incoming_chunk(self, chunk_wav_path, chunk_start_s):
        t0 = time.perf_counter()
        segments, info = self.model.transcribe(
            chunk_wav_path,
            beam_size=1,
            condition_on_previous_text=False,
            vad_filter=True,
            word_timestamps=True
        )
        
        emitted_this_chunk = []
        for s in segments:
            seg_start = chunk_start_s + s.start
            seg_end = chunk_start_s + s.end
            
            # Avoid duplicating segments already finalized past high-water mark
            if seg_end <= self.high_water_mark_s + 0.1:
                continue
                
            text = s.text.strip()
            if not text:
                continue
                
            self.segment_counter += 1
            t_finalized = time.perf_counter()
            finalization_latency_ms = (t_finalized - t0) * 1000
            
            item = {
                "segment_index": self.segment_counter,
                "text": text,
                "start": round(seg_start, 2),
                "end": round(seg_end, 2),
                "words_count": len(text.split()),
                "finalization_latency_ms": round(finalization_latency_ms, 2)
            }
            self.finalized_segments.append(item)
            emitted_this_chunk.append(item)
            self.high_water_mark_s = max(self.high_water_mark_s, seg_end)
            
        return emitted_this_chunk

def main():
    print("=== STARTING PHASE H30 INCREMENTAL ASR & FINALIZATION TEST ===", flush=True)
    
    t0_load = time.perf_counter()
    model = WhisperModel("base.en", device="cuda", compute_type="float16")
    # Warmup
    _ = list(model.transcribe(AUDIO_SRC, beam_size=1, vad_filter=True))
    print(f"Model ready in {round((time.perf_counter() - t0_load)*1000, 2)} ms", flush=True)
    
    engine = IncrementalASREngine(model)
    
    with wave.open(AUDIO_SRC, 'rb') as wf:
        framerate = wf.getframerate()
        nchannels = wf.getnchannels()
        sampwidth = wf.getsampwidth()
        total_frames = wf.getnframes()
        audio_data = wf.readframes(total_frames)
        
    chunk_size_s = 5.0
    chunk_frames = int(chunk_size_s * framerate)
    
    timeline_events = []
    t_pipeline_start = time.perf_counter()
    
    for offset_idx, offset in enumerate(range(0, total_frames, chunk_frames)):
        chunk_bytes = audio_data[offset * sampwidth * nchannels : (offset + chunk_frames) * sampwidth * nchannels]
        if len(chunk_bytes) < framerate * sampwidth * 0.5:
            break
            
        chunk_start_s = offset / framerate
        tmp_path = f"runtime/h30_inc_chunk_{offset_idx}.wav"
        with wave.open(tmp_path, 'wb') as wf_chunk:
            wf_chunk.setnchannels(nchannels)
            wf_chunk.setsampwidth(sampwidth)
            wf_chunk.setframerate(framerate)
            wf_chunk.writeframes(chunk_bytes)
            
        emitted = engine.process_incoming_chunk(tmp_path, chunk_start_s)
        for em in emitted:
            wall_elapsed_ms = (time.perf_counter() - t_pipeline_start) * 1000
            timeline_events.append({
                "segment_index": em["segment_index"],
                "text": em["text"],
                "audio_time_range": f"{em['start']:.2f}s - {em['end']:.2f}s",
                "wall_time_emitted_ms": round(wall_elapsed_ms, 2),
                "processing_lag_ms": round(wall_elapsed_ms - (em["end"] * 1000), 2)
            })
            print(f"[FINALIZED Seg #{em['segment_index']}] [{em['start']:.2f}s - {em['end']:.2f}s] '{em['text']}' (Latency: {em['finalization_latency_ms']} ms)", flush=True)
            
    # Verify invariants: Monotonicity, non-duplication
    starts = [s["start"] for s in engine.finalized_segments]
    assert all(starts[i] <= starts[i+1] for i in range(len(starts)-1)), "Timestamps must be monotonically increasing"
    
    latencies = [s["finalization_latency_ms"] for s in engine.finalized_segments]
    p50_lat = float(np.percentile(latencies, 50)) if latencies else 0.0
    p90_lat = float(np.percentile(latencies, 90)) if latencies else 0.0
    p95_lat = float(np.percentile(latencies, 95)) if latencies else 0.0
    p99_lat = float(np.percentile(latencies, 99)) if latencies else 0.0
    
    out_results = {
        "phase": "H30",
        "audio_source": AUDIO_SRC,
        "streaming_chunk_size_s": chunk_size_s,
        "total_segments_finalized": len(engine.finalized_segments),
        "total_words": sum(s["words_count"] for s in engine.finalized_segments),
        "finalization_latencies_ms": {
            "mean": round(float(np.mean(latencies)), 2),
            "p50": round(p50_lat, 2),
            "p90": round(p90_lat, 2),
            "p95": round(p95_lat, 2),
            "p99": round(p99_lat, 2)
        },
        "timeline_emission_log": timeline_events
    }
    
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(out_results, f, indent=2)
    print(f"\nSaved incremental ASR results to {OUTPUT_JSON}", flush=True)

if __name__ == "__main__":
    main()
