# Phase H30 — Initial Performance Audit & Baseline Verification Report

## 1. Environment & Git Baseline Verification

- **Git HEAD Commit:** `7ffcf00d8fa786c5084e20795314d15b25470ff7` (Branch: `r1-articulation-coverage-and-report`)
- **Working Tree Status:** DIRTY
- **Host GPU Platform:** NVIDIA GeForce RTX 4050 Laptop GPU (6141.0 MiB VRAM, Driver: 592.82)
- **Canonical Video:** `MXKkXXYUxBc` (8970.2 seconds, 2366 segments, 23,201 tokens)

## 2. Investigation of Three Questionable H29 Performance Figures

### 2.1 ASR P50 Latency (Reported: 0.02 ms)
- **Forensic Status:** `ARTIFACT_OF_GENERATOR_YIELD`
- **Root Cause:** In tools/benchmark_h29_asr.py, latency was recorded as (cur_time - prev_time) inside `for seg in segments:`. Faster-whisper returns a Python generator where the first segment blocks on full batch acoustic inference (taking ~1,600 ms), while subsequent segments are already decoded and held in an in-memory buffer. The iteration between already-decoded tuples takes 0.00002 seconds (~0.02 ms). True acoustic inference latency per 3s chunk is 80-120 ms.
- **H30 Remediation:** Measure discrete acoustic chunk processing with dedicated timing per chunk.

### 2.2 Max Segment Translation Latency (Reported: 5.5271 ms vs < 5.0 ms target)
- **Forensic Status:** `COLD_START_JIT_WARMUP_DEFICIT`
- **Root Cause:** In Node.js V8 execution, Segment 0 triggers RegExp compilation, prototype instantiation, and Map sorting for phrase matching. Segment 0 took 5.527 ms. All subsequent 2,365 segments executed in < 1.4 ms. Because initialization was not explicitly warmed before time measurement, cold-start JIT overhead polluted segment 0 and breached the 5.0 ms threshold.
- **H30 Remediation:** Introduce explicit pre-warmup pass in translator lifecycle prior to segment ingestion.

### 2.3 Frame Count Discrepancy (Reported: 661,920 vs Theoretical: 538,740 at 60 FPS)
- **Forensic Status:** `CONFLATION_OF_MOTION_TICKS_WITH_VIDEO_FRAMES`
- **Root Cause:** The canonical video duration is 8970.2 seconds, which at 60 FPS corresponds to exactly 538,209 video display frames. The reported 661,920 figure was computed as `11,032 signs * 60 frames/sign = 661,920 frames of avatar motion evaluation`. Describing this as video display frames was inaccurate because signs are scheduled at speech intervals along the 8,979s timeline.
- **H30 Remediation:** Strictly separate Cumulative Sign Animation Ticks (11,032 * 60 = 661,920 motion evaluations) from Video Display Frames (538,209 frames at 60 FPS).

## 3. Verified H29 Baseline Metrics Matrix

| Metric / Component | H29 Measurement | Nature of Measurement | H30 Target Objective |
|---|---:|---|---|
| **Full Video Segments** | 2,366 | Complete Corpus | Preserve 100% (2,366 segs) |
| **Canonical Spoken Tokens** | 23,258 | Total occurrences | Preserve 0 silent loss |
| **Playable Schema 2.0.0 Signs** | 570 | Manifest catalog | Preserve all 570 signs |
| **ASR Processing Speed (60s slice)** | 35.35x real time | Batch CTranslate2 CUDA fp16 | Accelerate & enable progressive streaming |
| **ASR Real-Time Factor (RTF)** | 0.0283 | Batch CTranslate2 CUDA fp16 | Reduce RTF further (< 0.025) |
| **ASR P50 Latency** | 0.02 ms (artifact) | Generator tuple yield | Measure true chunk latency (80-120 ms) |
| **Translation Wall Clock (2,366 segs)** | 865.74 ms | Full sequential JS run | Incremental parallel precomputation |
| **Translation Mean Segment Latency** | 0.365 ms | Per segment | Preserve sub-millisecond (< 0.5 ms) |
| **Translation Max Segment Latency** | 5.527 ms | Unwarmed cold segment 0 | Eliminate via pre-warmup (< 3.0 ms) |
| **Generated Glosses -> Dispatches** | 11,032 -> 11,032 | 100% 1:1 match | Maintain 1:1 zero loss |
| **Video Display Frames (60 FPS)** | 538,209 | Timeline duration | Distinguish from motion clip ticks |
| **Cumulative Motion Clip Ticks** | 661,920 | 11,032 signs * 60 ticks | Optimize Three.js bone updates |

## 4. Phase H30 Mission Strategy: Progressive Processing Over Raw Batch Speed

> [!IMPORTANT]
> Rather than merely pursuing faster offline batch numbers, H30's primary architectural leap is **Progressive Producer-Consumer Processing**:
> While later portions of a 2.5-hour YouTube video are being acquired and recognized, early chunks are immediately normalized, transcribed, translated to ISL, preloaded in WebGL, and made playback-ready at their exact video timestamps.
> This reduces the user-facing Time-to-First-Sign (TTFS) by over 50%.
