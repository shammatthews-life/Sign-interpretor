# H46 ASR Research, Meaning-Critical Error Audit & Ablation

**Benchmark Videos (0:00–2:00 Locked):**
- Video A: `MXKkXXYUxBc` (29 verified segments `A01–A29`)
- Video B: `y8tFSuOMAqQ` (31 verified segments `B01–B31`)

---

## 1. Reproduced RTX 4050 CUDA ASR Ablation (`small.en`, `float16`, `beam_size=5`)

From [h45_asr_ablation.json](file:///d:/sign%20interpretor/artifacts/h45/asr/h45_asr_ablation.json) against [h44_verified_references_ab.json](file:///d:/sign%20interpretor/artifacts/h44/h44_verified_references_ab.json):

| Config | Video A WER (%) | Video B WER (%) | Mean WER (%) | Mean RTF | Decision |
|---|---:|---:|---:|---:|---|
| `base.en_b5_norm` (`vad min_silence=350ms`) | `9.62%` | `2.63%` | `6.12%` | `0.0560` | Rejected (clips intro boundaries) |
| `small.en_b5_norm` (`vad min_silence=350ms`) | `8.59%` | **`2.28%`** | `5.43%` | `0.0761` | Rejected (`350ms` VAD hurts A) |
| `small.en_b5_norm_prompt` (`min_silence=350ms`) | `8.59%` | `2.28%` | `5.43%` | `0.0771` | Prompt did not outperform unprompted |
| **Production Default (`youtube_ingest.py`)** (`small.en`, default Silero VAD, `highpass=80+loudnorm`) | **`0.69%`** | `3.15%` (`0.36%` interior) | **`1.92%`** | **`0.0501`** | **Retained as optimal** |

---

## 2. Meaning-Critical Error Audit (Negations, Numerals, Proper Names)

- **Video A (`0.69%` WER):** Zero dropped negations, zero corrupted numerals, zero corrupted core nouns.
- **Video B (`3.15%` total WER, `0.36%` interior WER):** Remaining edge boundary differences occur at the `2:00` lock boundary (`B31` tail), with zero negation inversions or number corruptions in `B01–B30`.
- **Conclusion:** Further ASR hyperparameter tuning on `small.en` is unnecessary and risks overfitting; H46 focuses on semantic, spatial, NMM, and visual signing fidelity downstream of ASR.
