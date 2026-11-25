# H47 NMM & Spatial Adversarial Tests

Executed in [test_h47_comprehension_and_discourse.mjs](file:///d:/sign%20interpretor/tools/test_h47_comprehension_and_discourse.mjs) and [test_h46_comprehension_and_spatial_audit.mjs](file:///d:/sign%20interpretor/tools/test_h46_comprehension_and_spatial_audit.mjs):

1. **Identical Manual Sign (`help`), Varying NMM:** Neutral vs `NMM-NEG-HEADSHAKE` (`-0.1554 rad` yaw) vs `NMM-YESNO-BROW-RAISE` (`-0.0856 rad` pitch) vs `NMM-WH-BROW-FURROW` (`+0.1011 rad` pitch) -> **`PASS`**.
2. **Constituent-Scoped NMM:** `"Today the team did not finish the video."` scopes `NMM-NEG-HEADSHAKE` to predicate/negation tokens while leaving opening `today` unscoped (`[]`) -> **`PASS`**.
3. **Cross-Cue Spatial Persistence:** `"The teacher explained the plan."` -> `"Then she helped the teacher."` retains `teacher=LOCUS_LEFT` (`persisted=true`) and assigns `she=LOCUS_RIGHT` -> **`PASS`**.
