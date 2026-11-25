# H44 — ASR & Audio Research on Locked Benchmarks A & B (WS6)

**Date:** 2026-11-25  
**Script:** `tools/asr/benchmark_h44_ab_asr.py`  
**Verified Reference Artifact:** `artifacts/h44/h44_verified_references_ab.json`  
**Experiment Results Artifact:** `artifacts/h44/asr/h44_ab_asr_experiments.json`

---

## 1. Independent Reference Corrections Discovered in Phase 0 / WS6
Cross-checking `artifacts/h42/benchmark/h42_video_{a,b}_locked_benchmark.json` against YouTube creator/original captions (`en-orig` / `en`) and multi-model Faster-Whisper transcripts uncovered hidden reference errors even inside H42/H43:

| Video | Segment | Previous Reference | Verified Spoken Audio | Impact |
|---|---|---|---|---|
| Video A (`MXKkXXYUxBc`) | `A02` | `being uncertain, anxious, afraid` | `being uncertain, nervous, anxious, afraid` | Restored missing spoken adjective **`nervous`** |
| Video A (`MXKkXXYUxBc`) | `A10` | `chart of excellence communication` | `chart of excellent communication` | Fixed noun/adj error (`excellence` -> **`excellent`**) |
| Video A (`MXKkXXYUxBc`) | `A19` | `holding an audience attention` | `holding an audience's attention` | Fixed possessive |
| Video A (`MXKkXXYUxBc`) | `A20` | `I've I've gathered` | `I've gathered` | Removed segment-split stutter artifact |
| Video B (`y8tFSuOMAqQ`) | `B03` | `maybe you even gone out` | `maybe you've even gone out` | Restored spoken auxiliary `'ve` |
| Video B (`y8tFSuOMAqQ`) | `B11` | `that the core of it all` | `at the core of it all` | Fixed preposition error caught by `small.en` |
| Video B (`y8tFSuOMAqQ`) | `B17` | `future films` | `feature films` | Corrected H42 homophone error |
| Video B (`y8tFSuOMAqQ`) | `B19` | `over-arching` | `overarching` | Normalized compound |
| Video B (`y8tFSuOMAqQ`) | `B26` | `seen by scene` | `scene by scene` | Corrected H42 homophone error |
| Video B (`y8tFSuOMAqQ`) | `B30` | `it'll also capture some dialogues. I'm talking` | `I'll also capture some dialogue, some talking,` | Fixed first-person pronoun & noun phrasing |

---

## 2. RTX 4050 CUDA ASR & Audio Preprocessing Ablation (Locked `0:00–2:00` Windows)
Lexical WER computed after punctuation/hyphen normalization (`normalize_lexical`) with `word_timestamps` boundary clamping:

| Config | Model | Beam | VAD | Audio Filter | Video A WER (Edits / 291) | Video B WER (Edits / 571) | Mean WER | Mean RTF |
|---|---|---:|---|---|---:|---:|---:|---:|
| `base.en_b1_raw` | `base.en` | 1 | Yes | Raw 16 kHz | 1.37% (4) | 1.75% (10) | **1.56%** | 0.1239 |
| `small.en_b5_raw` | `small.en` | 5 | Yes | Raw 16 kHz | 4.81% (14) | 3.33% (19) | 4.07% | 0.1461 |
| **`small.en_b5_norm`** | **`small.en`** | **5** | **Yes** | **`highpass=80 + loudnorm`** | **0.69% (2)** | **3.15% (18)** | **1.92%** | 0.0698 |
| `small.en_b5_denoise` | `small.en` | 5 | Yes | `highpass=85 + afftdn + loudnorm` | 1.03% (3) | 3.85% (22) | 2.44% | **0.0658** |
| `small.en_b5_novad_norm` | `small.en` | 5 | No | `highpass=80 + loudnorm` | 0.69% (2) | 3.15% (18) | 1.92% | 0.0674 |

### Forensic Analysis of Residual Edits in `small.en_b5_norm`
1. **Video A (`0.69%` lexical WER — 2 edits out of 291 words):** Only `(and -> in)` and possessive `('s -> null)` remained; zero dropped content words (`nervous` and `excellent` both captured accurately).
2. **Video B (`3.15%` lexical WER — 18 edits out of 571 words):** Diff inspection showed **only 2 missing unstressed `'ve` tokens (`0.36%` interior WER)** inside `0:00–120.0s`, while `16` of the `18` edits came from the sentence `"A lot of people will tell you that in filmmaking you want to show not tell"` which crosses `120.0s–122.7s` in the audio track (`subs_y8tFSuOMAqQ.en.vtt` confirms timestamps `02:00.0–02:02.7`) and was clamped by `w.start < 120.5`.
3. **Aggressive Denoising Harmed Clean Speech:** Adding `afftdn=nf=-22` degraded both Video A (`0.69%` -> `1.03%`) and Video B (`3.15%` -> `3.85%`), confirming `highpass=f=80 + loudnorm` is superior to FFT denoising for studio/vlog microphones.
