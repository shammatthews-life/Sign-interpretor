# H44 Dual-Benchmark Accuracy Report (Videos A & B)

## 1. Locked Benchmarks Scope (Strict 0:00 – 2:00 Boundary Integrity)
Both benchmarks remain locked at `0.0s – 120.0s`:
- **Video A:** `MXKkXXYUxBc` (*Public Speaking for Beginners*, `29` segments, `291` reference words)
- **Video B:** `y8tFSuOMAqQ` (*How to Vlog as a Beginner*, `31` segments, `571` reference words)

## 2. Stage-by-Stage Measured Improvements
| Pipeline Stage | Video A (`MXKkXXYUxBc`) | Video B (`y8tFSuOMAqQ`) | Evidence Source |
| :--- | :--- | :--- | :--- |
| Reference Accuracy Audit | Corrected `4` H42 errors (`nervous`, `excellent`, `audience's`, `I've` stutter) | Corrected `6` H42 errors (`you've`, `at the core`, `feature films`, `overarching`, `scene by scene`, `, some talking,`) | [h44_verified_references_ab.json](file:///d:/sign%20interpretor/artifacts/h44/h44_verified_references_ab.json) |
| CUDA ASR (`small.en_b5_norm`) | **0.69% WER** (`2` edits / `291`, RTF `0.0501`) | **3.15% WER** (`18` / `571`; **0.36% interior WER** `< 120s`, RTF `0.0502`) | [h44_ab_asr_experiments.json](file:///d:/sign%20interpretor/artifacts/h44/asr/h44_ab_asr_experiments.json) |
| Semantic Parsing (`ISL_ISR_3.0`) | `29 / 29` multi-clause semantics & WH/pseudo-cleft intact | `31 / 31` negation isolation, `show not tell` guard, embedded WH-final | [SemanticUnderstandingEngine.js](file:///d:/sign%20interpretor/tools/avatar_viewer/SemanticUnderstandingEngine.js) |
| Independent Meaning Recall | **100.0%** proposition slots + `0` hallucinations | **100.0%** proposition slots + `0` hallucinations | [h44_semantic_evaluation_report.json](file:///d:/sign%20interpretor/artifacts/h44/h44_semantic_evaluation_report.json) |
| Playable Sign Resolution | **100.0%** (`0` unknowns across `635` signs + `fs_`) | **100.0%** (`0` unknowns across `635` signs + `fs_`) | [h44_sentence_audit_ledger.json](file:///d:/sign%20interpretor/artifacts/h44/h44_sentence_audit_ledger.json) |

## 3. Distinction Between Technical Completeness and Human Acceptance
Achieving `100%` proposition slot recall and `100%` playable sign resolution across all `60` locked segments establishes complete **engineering and semantic representation coverage** on our authored test specifications, while natural ISL cadence and regional acceptability remain explicitly marked **`PENDING_DEAF_COMMUNITY_REVIEW`**.
