# Phase F2.5 ASR Acceleration & Non-Blocking Streaming

## 1. Overview & Problem Statement

In Phase F2, the baseline streaming ASR used CPU + int8 running synchronously. Because Whisper decodes took 800–1000+ ms per decode, audio ingestion and repeated overlapping decodes blocked each other. On fast speech, the synchronous worker fell up to 18 seconds behind wall-clock time.

Phase F2.5 resolves this by:
1. Inspecting and enabling GPU acceleration on the NVIDIA RTX 4050 Laptop GPU (6141 MiB VRAM).
2. Benchmarking CPU vs. GPU configurations across all canonical F2 fixtures.
3. Implementing a decoupled asynchronous worker thread for non-blocking audio ingestion.
4. Designing and enforcing a bounded stale-window decode policy.
5. Tuning first-partial latency parameters while preserving transcript stability.
6. Expanding diagnostic telemetry.

---

## 2. GPU Inspection & Runtime Discovery

### Hardware & Driver State
- **GPU**: NVIDIA GeForce RTX 4050 Laptop GPU (6141 MiB total VRAM)
- **NVIDIA Driver**: 592.82 (CUDA Version: 13.1)
- **Python**: 3.12.10
- **CTranslate2**: 4.8.2
- **faster-whisper**: 1.1.1

### Critical Dependency Resolution
- Inspection revealed that CTranslate2 4.8.2 on Windows bundles `cudnn64_9.dll` and `ctranslate2.dll`, but was built against CUDA 12 and requires `cublas64_12.dll` and `cublasLt64_12.dll`.
- These DLLs were located on the system and placed directly in the `ctranslate2` package directory alongside automatic runtime discovery in `tools/asr/streaming_asr.py:ensure_cuda_support()`.
- Verified GPU execution: native CTranslate2 on CUDA device 0 with `float16` and `int8_float16`.

---

## 3. CPU vs. GPU Benchmark (Task 3)

Benchmark performed against the 5 canonical F2 audio fixtures (`short.wav`, `normal.wav`, `fast.wav`, `pause_rich.wav`, `mild_noisy.wav`) under paced real-time audio input:

The WAV fixtures are generated locally by `tools/asr/generate_benchmark_audio.py`
and are not distributed in this repository because they derive from an
upstream recording. Review the upstream source terms before generating them;
the fixture directory is ignored by Git.

| Model | Device | Compute Type | Load Time | Avg Decode | Worst Decode | RTF | Avg WER | Peak VRAM | Keeps Up? |
|---|---|---|---|---|---|---|---|---|---|
| **tiny.en** | CPU | int8 | 1992 ms | 880.5 ms | 6573.4 ms | 0.942 | 14.8% | N/A (CPU) | ❌ Falls behind |
| **tiny.en** | GPU (CUDA) | float16 | 1954 ms | 204.7 ms | 1410.7 ms | 0.237 | 17.5% | 227 MiB | ✅ Yes |
| **tiny.en** | GPU (CUDA) | int8_float16 | 948 ms | 299.3 ms | 3064.4 ms | 0.333 | 16.6% | 203 MiB | ✅ Yes |
| **base.en** | GPU (CUDA) | float16 | 1108 ms | 160.7 ms | 296.4 ms | 0.193 | 11.2% | 275 MiB | ✅ Yes |

### Analysis
- **Speedup**: `tiny.en` on CUDA `float16` yields a **4.3x reduction** in average decode time (204.7 ms vs. 880.5 ms) and a **4.7x reduction** in worst decode time (1410 ms vs. 6573 ms).
- **VRAM footprint**: Memory usage is minimal (227 MiB for `tiny.en`, 275 MiB for `base.en`), using less than 5% of the RTX 4050's 6141 MiB capacity.
- **base.en superiority**: On GPU, `base.en` (`float16`) outperforms `tiny.en` across all metrics:
  - Average decode: 160.7 ms
  - Worst decode: 296.4 ms
  - Aggregate RTF: 0.193
  - WER: 11.2% (vs 14.8% on tiny.en)
- `int8_float16` on GPU provided no latency advantage over `float16` because small Whisper models on Ada Lovelace tensor cores run faster with native FP16 than INT8 dequantization overhead.

---

## 4. Asynchronous ASR Worker & Stale-Window Policy (Tasks 4 & 5)

### Worker Architecture
```
Audio Ingestion Thread (HTTP / Mic / File)
             ↓
        accept_audio_chunk()  [< 0.2 ms non-blocking]
             ↓
        Audio Rolling Buffer (thread-safe lock)
             ↓  (Event trigger when hop due & duration >= minimum)
        ASR Worker Thread (_worker_loop)
             ↓  (Runs Whisper transcribe outside buffer lock)
        Transcript Stabilizer
             ↓
        Output Event Queue / on_event callback
```

### Stale-Window Policy
When audio arrives faster than the worker or when a decode takes longer than a hop:
1. Audio ingestion never blocks: incoming 100 ms chunks append to the rolling buffer immediately (< 0.2 ms).
2. Decode triggers arriving while the worker is state `DECODING` increment `backlog` count rather than queuing redundant decode tasks.
3. When the worker becomes `IDLE`, it **never replays stale intermediate snapshots**. Instead, it snapshots only the **single newest valid rolling window** (`samples[-window_size:]`).
4. Overlap context (up to `rolling_window_ms`) is preserved inside the window so the transcript stabilizer maintains smooth context.
5. In fast speech testing, the stale-window policy successfully dropped 35 obsolete intermediate decode slices while keeping total stream lag to only 167 ms (vs. 18,500 ms lag on CPU).

---

## 5. First-Partial Latency Tuning (Task 6)

Evaluated under paced real-time input on GPU (`float16`):

| Configuration | Min Speech | Decode Hop | Rolling Window | Avg First Partial Latency | Avg Decode | Aggregate RTF |
|---|---|---|---|---|---|---|
| **Config 1 (Baseline)** | 1000 ms | 750 ms | 4000 ms | 1071 ms | 175.0 ms | 0.22 |
| **Config 3 (Balanced)** | 750 ms | 500 ms | 3500 ms | 850 ms | 210.6 ms | 0.26 |
| **Config 2 (Aggressive)** | 500 ms | 350 ms | 3000 ms | 561 ms | 192.3 ms | 0.29 |

**Selection**:
- For live conversational interaction, **Config 3** (750 ms minimum speech, 500 ms hop, 3500 ms window) achieves sub-second first-partial response (~850 ms) while preserving strong context and stability.
- On GPU, even Config 1 first-partial latency dropped from 1400–1600 ms down to 1071 ms.

---

## 6. Finalization & Live Tests (Tasks 7, 8, 9, 10)

1. **Task 7 ("Hello good morning")**:
   - Streamed 1884 ms audio in 100 ms canonical chunks.
   - First partial: `'Hello, good morning.'` at 800 ms.
   - Final event: `'Hello, good morning.'` upon flush.
   - No duplicate partial events emitted.
2. **Task 8 (Fast Speech)**:
   - 5500 ms fast speech audio finished in 5667 ms (lag: 167 ms).
   - Ingestion per chunk averaged 0.167 ms (max 1.1 ms).
   - Stale-window policy dropped 35 obsolete hops, keeping queue clean.
3. **Task 9 (Mildly Noisy Audio)**:
   - GPU float16 achieved 4.5% WER on `mild_noisy.wav` with 143.7 ms average decode.
4. **Task 10 (Diagnostics Telemetry)**:
   - Expanded ASR panel in `tools/avatar_viewer/index.html` and `LocalASRService` to expose:
     - `Device`: CPU / GPU (CUDA float16)
     - `Model`: tiny.en / base.en
     - `Worker state`: IDLE / DECODING
     - `Audio received`: X.XX sec
     - `ASR queue`: X chunks
     - `Backlog`: X stale hops dropped
     - `Current partial`: text
     - `Last final`: text
     - `First partial latency`: X ms
     - `Decode latency`: X ms
     - `RTF`: X.XXX
