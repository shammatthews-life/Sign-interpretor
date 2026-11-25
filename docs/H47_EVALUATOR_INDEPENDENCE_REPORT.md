# H47 Evaluator Independence Report

1. **Non-Circularity Principle:** Automated evaluators in H47 (`test_h47_comprehension_and_discourse.mjs`, `h47_audit_trajectory_quality.mjs`, `test_h45_relational_semantics.mjs --strict`) check independent semantic, syntactic, polysemy, discourse-locus, and 3D kinematic invariants rather than circularly matching translator-internal strings.
2. **Locked Benchmark Separation:** Videos A (`MXKkXXYUxBc`) and B (`y8tFSuOMAqQ`) remain strictly separated from the new `h47_generalization_benchmark.json` development/adversarial/generalization suites.
3. **Human Ground Truth Boundary:** Automated evaluators cannot replace Deaf human comprehension testing; all human metrics remain `PENDING_DEAF_COMMUNITY_REVIEW`.
