# H43 — ASR & Audio Intelligence Research and Engineering (WS1)

**Status:** COMPLETE (`RTX 4050 CUDA float16`)  
**Addresses Defects:** `DEF-H43-004`

---

## 1. Elimination of Circular Ground Truth (`DEF-H43-004`)
In `H42`, `artifacts/h42/translation/h42_video_b_locked_benchmark.json` was copied from ASR output, producing a misleading `0.00% WER` self-comparison while errors such as `"future films"` (instead of `"feature films"`) and `"seen by scene"` (instead of `"scene by scene"`) went undetected.

In H43 (`tools/asr/build_h43_references.py`), all 5 evaluation videos (`0:00–2:00` windows) use independent human references (`artifacts/h43/benchmark/h43_multi_domain_references.json`):
- **`xrwz9IxpMJg`** (IIT/NPTEL Indian English Robotics, 213 words): **Official human VTT subtitles** (`subs_xrwz9IxpMJg.en-LUU0EuDKgKo.vtt`)
- **`aircAruvnKk`** (3Blue1Brown Neural Networks, 381 words): **Official human VTT subtitles** (`subs_aircAruvnKk.en.vtt`)
- **`D9Ihs241zeg`** (Chimamanda Adichie TED Storytelling, 290 words): **Official human VTT subtitles** (`subs_D9Ihs241zeg.en.vtt`)
- **`MXKkXXYUxBc`** (Locked Video A Public Speaking, 275 words): Human-audited revision fixing `"I've I've gathered"` stutter and `"audience attention"` -> `"audience's attention"`
- **`y8tFSuOMAqQ`** (Locked Video B Vlogging, 539 words): Human-audited revision verified against captions fixing `"future films"` -> `"feature films"`, `"seen by scene"` -> `"scene by scene"`, `"over-arching"` -> `"overarching"`, `"I'm talking I'll talk"` -> `"I'll talk"`

---

## 2. Multi-Domain GPU ASR & Audio Preprocessing Experiments (`tools/asr/benchmark_h43_asr.py`)
Executed 30 experiments (6 Faster-Whisper + audio preprocessing configurations × 5 videos) on **NVIDIA GeForce RTX 4050 Laptop GPU (`cuda`, `float16`)**:

| Config | Model | Beam | Audio Filter | Mean WER | Mean RTF | Video A | Video B | Video C (IIT IN-EN) | Video D (3B1B STEM) | Video E (TED) |
|---|---|---:|---|---:|---:|---:|---:|---:|---:|---:|
| `tiny.en_b1_raw` | `tiny.en` | 1 | `raw_16k` | 5.66% | 0.0754 | 6.18% | 5.38% | 8.92% | 3.67% | 4.14% |
| `base.en_b1_raw` | `base.en` | 1 | `raw_16k` | 3.64% | 0.0548 | 4.36% | 2.04% | 6.57% | 3.15% | 2.07% |
| `base.en_b5_raw` | `base.en` | 5 | `raw_16k` | 4.34% | 0.0664 | 5.09% | 3.90% | 8.45% | 1.84% | 2.41% |
| `base.en_b5_norm` | `base.en` | 5 | `highpass=80 + loudnorm` | 4.31% | 0.0370 | 5.45% | 3.34% | 7.04% | 2.62% | 3.10% |
| `small.en_b5_raw` | `small.en` | 5 | `raw_16k` | 4.32% | 0.0902 | 7.27% | 4.08% | 4.69% | 3.15% | 2.41% |
| **`small.en_b5_norm`** | **`small.en`** | **5** | **`highpass=80 + loudnorm`** | **3.63%** | **0.0739** | **4.36%** | **2.97%** | **4.23%** | 3.15% | 3.45% |

**Key Engineering Findings:**
1. **`small.en_b5_norm` achieved the best overall accuracy (`3.63%` mean WER)** at `RTF = 0.0739` (~13.5x faster than real-time on RTX 4050 CUDA `float16`).
2. **Accent Robustness:** On IIT/NPTEL Indian English (`xrwz9IxpMJg`), upgrading `tiny.en` -> `small.en` with FFmpeg `highpass=f=80 + loudnorm` **reduced WER from `8.92%` down to `4.23%`** (a **52.6% relative error reduction**).
3. **Production Confidence Propagation (`youtube_ingest.py`, `translate_segments.mjs`):**
   - Upgraded `transcribe_audio_file()` to `beam_size=5` and emitted per-segment `avg_logprob`, `no_speech_prob`, and calibrated acoustic confidence `exp(avg_logprob) * (1 - min(0.95, no_speech_prob))`.
   - Updated `translate_segments.mjs` to forward `asrContext` to `EnglishToISLTranslator.translate()` so low-confidence segments (`< 0.55`) automatically flag `TRANSLATION_UNCERTAIN`.
   - Added `SemanticUnderstandingEngine.js` and `ISLFingerspelling.js` to `_translation_implementation_hash()`.
