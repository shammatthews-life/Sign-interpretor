# H45 Semantic Preservation & Anti-Circular Evaluation Report

## 1. Exposing H44's Blind Spot
H44's 459-slot bag-of-concepts evaluator scored `100%` while passing `27` real semantic failures (`B14` collapsed double negation, `B15`/`ADV04` inverted negation scope, `B25` affirmative `"instead of stressing"`, `B04` `GOOD YOUR VIDEO`, `B20`/`B21`/`B24` spurious `DO`, plus wrong-but-playable substitutions like `probably->THINK`, `view->SEE`, `talks->SAY`, `things->MATTER`).

## 2. H45 Strict Relational, Role, Scope & Adversarial Evaluation
Implemented [test_h45_relational_semantics.mjs](file:///d:/sign%20interpretor/tools/test_h45_relational_semantics.mjs) against [h45_relational_and_adversarial_suite.json](file:///d:/sign%20interpretor/artifacts/h45/h45_relational_and_adversarial_suite.json) (`33` strict relational & adversarial checks enforcing per-clause negation counts, `A < B` role/scope order, forbidden wrong-sense glosses, NMM propagation, and ellipsis):
- **Pre-H45 Baseline (`1df82e4`):** **`6 / 33 (18.18%)`**
- **Post-H45 `ISL_ISR_4.0` + `647`-Sign Library:** **`33 / 33 (100%)`**
- **Updated H44 Proposition & 78-Case Suites (after purging stale H44 expectations that enforced old bugs):** `60 / 60` (`461 / 461` slots) + `78 / 78 (100%)`.
- **H43 44-Case Challenge Suite (after fixing `NEG_01` `maxCount: 2` & `OPR_02` `EVERYONE`):** **`44 / 44 (100%)`**.
- **Held-Out Generalization Videos (`test_h43_multi_domain_evaluation.mjs`):** `xrwz9IxpMJg` `86.82%` (`17` UNK), `aircAruvnKk` `75.98%` (`61` UNK), `D9Ihs241zeg` `74.88%` (`51` UNK).
- **Human Review Status:** `PENDING_DEAF_COMMUNITY_REVIEW`.
