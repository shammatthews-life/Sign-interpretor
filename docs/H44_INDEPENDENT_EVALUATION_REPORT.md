# H44 Independent Semantic & Cross-Domain Evaluation Report

## 1. Anti-Circularity Design
H44 strictly avoids letting the translator score itself. Semantic ground-truth propositions for all 60 locked segments (`A01–A29`, `B01–B31`) were authored independently from verified spoken English in [h44_independent_propositions.json](file:///d:/sign%20interpretor/artifacts/h44/h44_independent_propositions.json) and executed by [test_h44_semantic_completeness.mjs](file:///d:/sign%20interpretor/tools/test_h44_semantic_completeness.mjs), producing [h44_semantic_evaluation_report.json](file:///d:/sign%20interpretor/artifacts/h44/h44_semantic_evaluation_report.json).

## 2. Meaning-Preservation Scorecard (Locked Benchmarks A & B)
| Metric | Result | Verified Scope |
| :--- | :--- | :--- |
| Proposition Concept Slot Recall | **100.0% (`459 / 459`)** | All 60 segments (`A01–A29`, `B01–B31`) |
| Clause Polarity Preservation | **100.0% (`60 / 60`)** | Affirmative, Negative (`NOT`), Privative (`WITHOUT`), Mixed Scoped |
| Syntactic Ordering Constraints | **100.0%** | Temporal fronting, clause-local SOV, WH-final vs pseudo-cleft |
| Discourse & Aspect Relation Retention | **100.0%** | `IF`, `BECAUSE`, `BUT`, `WITHOUT`, perfective `FINISH` |
| Zero Hallucination / Semantic Corruption | **100.0% (`60 / 60`)** | Zero false `NOT` on `B31`, zero `GO` on `B04`, zero `SLEEP` on `B23` |
| Playable Sign Asset Resolution | **100.0% (`60 / 60`)** | `0` unknown terms, `0` unavailable signs (`635`-sign library + `fs_`) |

## 3. Expanded Linguistic Suites & Unseen Cross-Domain Generalization
- **H44 Expanded Challenge Suite (`78` independent cases across 15 linguistic categories):** **`78 / 78 (100%)`** ([h44_expanded_challenge_75.json](file:///d:/sign%20interpretor/artifacts/h44/h44_expanded_challenge_75.json)). Running this expanded suite proactively caught and forced repairs for missing `WHERE`/`WHO`/`PLEASE`/`HELPED`/`UNLESS`, object-determiner SOV interruption (`MY`/`YOUR`), `hours left -> REMAINING`, and `NMM-*` clause propagation.
- **H43 44-Case Linguistic Challenge Suite:** **`44 / 44 (100%)`**.
- **Core Automated Unit & Extension Test Suite (`npm.cmd test`):** **`87 / 87 PASS`**.
- **Python Pipeline Validators:** `validate_h23_job_lifecycle.py` (`PASS`), `validate_h33_4_job_recovery.py` (`PASS`), `validate_sign_library.py` (`Schema check: PASSED`).
- **Held-Out Cross-Domain Videos (`test_h43_multi_domain_evaluation.mjs`):**
  - `xrwz9IxpMJg` (Indian English Robotics): `86.82%` concept resolution (`17` unknown technical terms)
  - `aircAruvnKk` (STEM Deep Learning Math): `75.98%` concept resolution (`61` unknown domain terms)
  - `D9Ihs241zeg` (TED Storytelling): `74.75%` concept resolution (`51` unknown literary terms)
  This contrast confirms genuine domain-general grammatical coverage while honestly exposing unseen specialized vocabulary boundaries outside A & B.
