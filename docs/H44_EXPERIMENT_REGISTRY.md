# H44 Experiment & Verification Registry

## 1. RTX 4050 CUDA ASR Ablations ([h44_ab_asr_experiments.json](file:///d:/sign%20interpretor/artifacts/h44/asr/h44_ab_asr_experiments.json))
| Experiment Config | Video A WER (%) | Video B WER (%) (Interior `<120s`) | Mean WER (%) | Mean RTF | Decision |
| :--- | ---: | ---: | ---: | ---: | :--- |
| `base.en_b1_raw` | `1.37%` (`4/291`) | `1.75%` (`10/571`) | `1.56%` | `0.1239` | Superseded (missed `nervous`, `excellent`) |
| `small.en_b5_raw` | `4.81%` (`14/291`) | `3.33%` (`19/571`) | `4.07%` | `0.1461` | High unconditioned hallucination delta on raw track |
| `small.en_b5_norm` | **`0.69%`** (`2/291`) | `3.15%` (`0.36%` interior) | `1.92%` | **`0.0501`** | **ADOPTED (`highpass=80 + loudnorm` in `youtube_ingest.py`)** |
| `small.en_b5_denoise` | `1.03%` (`3/291`) | `3.85%` (`22/571`) | `2.44%` | `0.0680` | Rejected (`afftdn` smeared fricatives/plurals) |
| `small.en_b5_novad_norm` | `0.69%` (`2/291`) | `3.15%` (`18/571`) | `1.92%` | `0.0674` | Parity with slightly slower RTF |

## 2. Translation, Sign & Pipeline Experiment Suite
| Suite / Validator | Command | Outcome | Scope |
| :--- | :--- | :--- | :--- |
| Sign Manifest Sync & Validator | `npm.cmd run validate:signs` | **635 / 635 valid** | Full `signs/*.json` unique-trajectory check |
| Core Unit & Extension Suite | `npm.cmd test` | **87 / 87 PASS** | Extension SW, synchronizer, camera, player, scheduler, translator |
| H44 Independent Semantic Suite | `node tools/test_h44_semantic_completeness.mjs` | **60/60 (459/459 slots) + 78/78 (100%)** | Non-circular meaning preservation + expanded 78-case suite |
| H43 44-Case + 5-Domain Suite | `node tools/test_h43_multi_domain_evaluation.mjs` | **44/44 + 5 videos evaluated** | Locked A/B `100%`; held-out C/D/E `74.75%–86.82%` |
| Python Pipeline Validators | `validate_h23_job_lifecycle.py`, `validate_h33_4_job_recovery.py`, `validate_sign_library.py` | **ALL PASS** | Job idempotency, durability recovery, sign schema |
| Real Chrome Extension E2E | `node tools/run_h44_real_chrome_e2e.mjs` | **PASS (A & B)** | Chrome `158` + port `8000` CUDA + NVENC capture + 7 transport checks |
| Secret Audit | `node tools/security_audit.mjs` | **CLEAN (0 secrets)** | Full workspace secret/credential hygiene |
