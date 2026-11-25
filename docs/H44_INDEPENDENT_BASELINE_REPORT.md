# H44 Independent Baseline & GitHub Recovery Report

## 1. Phase 0 GitHub Baseline Recovery
Prior to H44 modifications, this workspace underwent a complete local-to-remote GitHub reconciliation:
- `.gitignore` was audited and tightened (excluding `*.wav`, `artifacts/**/preprocessed_audio/`, and `artifacts/**/tmp_*` scratch artifacts).
- `node tools/security_audit.mjs` executed cleanly with `[PASS] Security Audit Clean: Zero credentials, tokens, or private secrets found!`.
- `660` verified H42/H43 baseline files were committed and pushed to `origin/main`, creating verified starting anchor commit **`77b2f959327a33714d2e6a98d6e2de4157179809`**.

## 2. Independent Forensic Verification of Locked Benchmark Texts (`0:00–2:00`)
Keeping both locked Video A (`MXKkXXYUxBc`, `29` segments) and Video B (`y8tFSuOMAqQ`, `31` segments) windows strictly locked to `0.0s – 120.0s`, H44 independently audited H42's benchmark JSON strings ([h42_video_a_locked_benchmark.json](file:///d:/sign%20interpretor/artifacts/h42/benchmark/h42_video_a_locked_benchmark.json) & [h42_video_b_locked_benchmark.json](file:///d:/sign%20interpretor/artifacts/h42/benchmark/h42_video_b_locked_benchmark.json)) against YouTube `en-orig`/`en` transcripts and multi-model CUDA Faster-Whisper inference ([h44_ab_asr_experiments.json](file:///d:/sign%20interpretor/artifacts/h44/asr/h44_ab_asr_experiments.json)):

- **10 substantive transcription errors** (12 total diffs including punctuation/spacing) were uncovered inside H42's benchmark references (`nervous` omitted in `A02`; `excellence` -> `excellent` in `A10`; missing `'s` on `audience's` in `A18`/`A19`; stutter `I've I've` in `A20`; omitted `you've` in `B03`; `that the core` -> `at the core` in `B11`; `feature films` fix in `B17`; `overarching` in `B19`; `scene by scene` normalization in `B26`; omitted `, some talking,` in `B30`).
- Corrected benchmark ground truth is versioned in [h44_verified_references_ab.json](file:///d:/sign%20interpretor/artifacts/h44/h44_verified_references_ab.json).

## 3. CUDA ASR Baseline vs. H44 Optimized `small.en` Config
Tested on NVIDIA GeForce RTX 4050 (`float16` CUDA via `faster-whisper`) across all 5 ablation configs (`tools/asr/benchmark_h44_ab_asr.py`):
- **`base.en_b1_raw`:** `1.37%` WER (A), `1.75%` WER (B), `1.56%` mean WER, `0.1239` mean RTF.
- **`small.en_b5_norm` (`highpass=80,loudnorm=I=-16:TP=-1.5:LRA=11`):** **`0.69%` WER on Video A** (`2` edits / `291` words, catching both `nervous` and `excellent`) and **`3.15%` WER on Video B** (`18` edits / `571` words; **`0.36%` interior WER** inside `[0, 120s)` — `16` edits solely from segment `B31` crossing the `120.0–122.7s` boundary) at **`0.0501` RTF** (~20x real-time).
- Runtime pipeline default updated in [youtube_ingest.py](file:///d:/sign%20interpretor/tools/youtube_pipeline/youtube_ingest.py) (`model_name="small.en"`, FFmpeg `highpass=f=80,loudnorm` conditioning).
