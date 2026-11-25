# H47 Comprehension-Oriented Benchmark Architecture

H47 separates evaluation into **8 distinct layers** so technical execution is never conflated with human comprehension:

| Layer | What It Measures | H47 Verification Tool / Status |
|---|---|---|
| 1. Technical Execution | Runtime, Chrome extension lifecycle, WebGL/CUDA, `88/88` unit tests | `npm.cmd test` + `run_h47_real_chrome_e2e.mjs` |
| 2. Linguistic Representation | ISL SOV order, `spatial_plan`, scoped NMMs, discourse continuity | `test_h47_comprehension_and_discourse.mjs` |
| 3. Sign Selection | Context-sensitive disambiguation (`right`, `left`, `sign up`, `back`) | `test_h47_comprehension_and_discourse.mjs` |
| 4. Motion Representation | Anatomical joint bounds, feature diversity, `0` rotation dupes | `h47_audit_trajectory_quality.mjs` + `validate:signs` |
| 5. Semantic Preservation | Proposition slots (`461/461`), polarity, relational/role preservation (`33/33`) | `test_h44_semantic_completeness.mjs` + `test_h45_relational_semantics.mjs` |
| 6. Visual Readability | Live Chrome framing (`400x478`), head/spine NMM telemetry, contact sheets & crops | `run_h47_real_chrome_e2e.mjs` + visual inspection |
| 7. User Comprehension | Blind meaning reconstruction + distractor MC + confidence ratings | `eval_protocol_pack.json` (`PENDING_DEAF_COMMUNITY_REVIEW`) |
| 8. Human Linguistic Acceptance | Native Deaf ISL signer acceptability & naturalness sign-off | `PENDING_DEAF_COMMUNITY_REVIEW` |
