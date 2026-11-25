# H45 Expanded Adversarial Dataset & Generalization Report

- **Adversarial & Relational Suite (`33` strict checks):** [h45_relational_and_adversarial_suite.json](file:///d:/sign%20interpretor/artifacts/h45/h45_relational_and_adversarial_suite.json) tests multi-clause negation count (`B14`), matrix negation attachment (`B15`, `ADV04`), contrastive `instead of` negation (`B25`), emphatic `do` + `NMM-EMPHATIC-NOD` (`B20`), VP ellipsis (`B13`, `ADV12`), SOV determiner protection (`ADV01`), inchoative comparatives (`B06`, `ADV07`, `ADV09`), causal/conditional role order (`ADV02`, `ADV03`), and polysemy (`R01–R21`).
  - Improved from **`6 / 33 (18.18%)`** at Phase 0 to **`33 / 33 (100%)`** in H45.
- **Unseen Cross-Domain Generalization (`test_h43_multi_domain_evaluation.mjs`):**
  - `xrwz9IxpMJg` (Indian English Robotics): `86.82%` concept resolution (`17` unknown technical terms)
  - `aircAruvnKk` (STEM Deep Learning Math): `75.98%` concept resolution (`61` unknown domain terms)
  - `D9Ihs241zeg` (Cultural Storytelling TED): `74.88%` concept resolution (`51` unknown literary terms)
  These unseen domain gaps are reported transparently without artificial lexical inflation.
