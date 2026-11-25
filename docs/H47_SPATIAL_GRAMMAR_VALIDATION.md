# H47 Spatial Grammar Validation

- **Cross-Cue Referent Persistence (`H47-DEF-02`):** `EnglishToISLTranslator.createDiscourseContext()` + `translate_segments.mjs` now persist `locusByReferent` (`LOCUS_LEFT` = `-10°`, `LOCUS_RIGHT` = `+10°`) across consecutive segments.
- **Verified Multi-Sentence Test:** In `"The teacher explained the plan."` -> `"Then she helped the teacher."`, `teacher` retained `LOCUS_LEFT` (`persisted=true`) while `she` received `LOCUS_RIGHT`.
- **Boundary:** Spatial locus conventions and directional verb arcs (`help`, `give`, `tell`, `show`, `ask`, `teach`, `bring`) remain `PENDING_DEAF_COMMUNITY_REVIEW` (`TRIAL-04` in `eval_protocol_pack.json`).
