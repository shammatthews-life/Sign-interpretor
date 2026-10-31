# Phase H30 — Performance Benchmarking Methodology & Discrepancy Resolution

## 1. Resolution of the Three H29 Forensic Anomalies

### Anomaly 1: ASR P50 of 0.02 ms
- **Investigation:** In H29, `step_latency` was recorded inside Python generator iteration `for seg in segments:`. Because faster-whisper yields already-computed tuples from its internal buffer, the loop iteration took 0.02 ms, masking the true acoustic compute time.
- **True H30 Measurement:** Measuring discrete 5.0-second acoustic audio chunks reveals true ASR inference P50 is **194.0803 ms** (Mean: **587.6032 ms**).

### Anomaly 2: Max Segment Translation Latency of 5.527 ms
- **Investigation:** In H29, Segment 0 incurred cold-start JIT compilation of regular expressions and prototype allocations, exceeding the 5.0 ms threshold.
- **H30 Optimization:** Pre-compiling static contraction regex tables and pre-sorting phrase maps eliminated per-segment allocations. True max latency is now **0.9901 ms** (Mean: **0.0588 ms** per segment).

### Anomaly 3: 661,920 Frames vs 538,740 Video Display Frames
- **Investigation:** A 8,979-second video at 60 FPS contains exactly **538,740 video display frames**. The reported 661,920 figure was the product of **11,032 signs * 60 animation ticks/sign**.
- **Clarification:** H30 strictly differentiates **Video Display Frames (538,740)** from **Cumulative Avatar Animation Ticks (661,920)**.

## 2. Benchmark Measurement Rules Enforced in H30

1. **Monotonic Clocks:** All microbenchmarks use `time.perf_counter()` or Node.js `performance.now()`.
2. **Separation of Stages:** File I/O, audio slicing, tensor core kernel execution, linguistic parsing, and WebGL transforms are measured independently.
3. **Cold vs Warm Distinction:** Cold initialization is reported separately from warm streaming execution.
4. **Percentile Computation:** Percentiles are calculated directly from sorted raw observation arrays, not by averaging sub-run averages.
