# H45 Experiment Registry

| Experiment | Tool / Script | Pre-H45 Baseline | H45 Result | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Error Mining (A & B) | `tools/h45_error_miner.mjs` | `24/60` segments flagged | `17/60` info-only (0 scope/DO/GO/GET bugs) | `h45_error_mining_report.json` |
| Strict Relational & Adversarial Suite | `tools/test_h45_relational_semantics.mjs --strict` | `6/33 (18.18%)` | **`33/33 (100%)`** | Enforces negation count, role/scope order, NMM, ellipsis |
| Sign Library Validation | `npm.cmd run validate:signs` | `635` valid | **`647 / 647` valid** | +12 ISLRTC-researched signs |
| Unit & Extension Suite | `npm.cmd test` | `87 / 87 PASS` | **`88 / 88 PASS`** | Added `H45 ISR 4.0` unit test |
| H44 Semantic & Challenge Suites | `tools/test_h44_semantic_completeness.mjs` | `60/60 + 78/78` (stale slots) | **`60/60 (461/461) + 78/78`** | Updated stale H44 expectations that enforced old bugs |
| H43 Challenge & 5-Domain | `tools/test_h43_multi_domain_evaluation.mjs` | `42/44` under H45 (stale `NEG_01`/`OPR_02`) | **`44/44 + 5 videos`** | Purged `NEG_01` single-NOT bug |
| CUDA ASR Ablation | `tools/asr/benchmark_h45_asr.py` | `0.69%` A / `3.15%` B (`small.en` default VAD) | `8.59%` A / `2.28%` B (`min_silence=350ms`) | Confirmed default Silero VAD (`0.69%` A) superior |
| Real Chrome Extension E2E | `tools/run_h45_real_chrome_e2e.mjs` | `635` signs | **`647` signs, B clean, A buffered post-seek** | `h45_real_chrome_e2e_evidence.json` |
| Security Audit | `tools/security_audit.mjs` | `0` secrets | **`0` secrets** | Clean |
