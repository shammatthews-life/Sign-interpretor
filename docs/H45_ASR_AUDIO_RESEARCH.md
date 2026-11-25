# H45 ASR, Audio & VAD Research Report

Executed RTX 4050 CUDA (`float16`, `beam_size=5`) ablation in [benchmark_h45_asr.py](file:///d:/sign%20interpretor/tools/asr/benchmark_h45_asr.py) ([h45_asr_ablation.json](file:///d:/sign%20interpretor/artifacts/h45/asr/h45_asr_ablation.json)) against [h44_verified_references_ab.json](file:///d:/sign%20interpretor/artifacts/h44/h44_verified_references_ab.json):

| Config | Video A WER (%) | Video B WER (%) | Mean WER (%) | Mean RTF | Key Finding |
| :--- | ---: | ---: | ---: | ---: | :--- |
| `base.en_b5_norm` (`vad min_silence=350ms`) | `9.62%` | `2.63%` | `6.12%` | `0.0560` | Short-silence VAD clipped intro boundaries on A |
| `small.en_b5_norm` (`vad min_silence=350ms`) | `8.59%` | **`2.28%`** | `5.43%` | `0.0761` | Improved B (`2.28%`), hurt A vs default Silero VAD (`0.69%`) |
| `small.en_b5_norm_prompt` (`min_silence=350ms`) | `8.59%` | `2.28%` | `5.43%` | `0.0771` | Domain `initial_prompt` matched unprompted lexical WER |
| **Production Default (`youtube_ingest.py`)** (`small.en`, default VAD, `highpass=80+loudnorm`) | **`0.69%`** | `3.15%` (`0.36%` interior) | **`1.92%`** | **`0.0501`** | **Confirmed optimal: retains default Silero VAD (`0.69%` on A)** |

*(Note: `medium.en` HF Hub download stalled on unauthenticated rate limits and was excluded rather than waiting indefinitely.)*
