# H47 Defect Ledger (Final Status)

| ID | Severity | Component | Description | Final Status | Verification Evidence |
|---|---|---|---|---|---|
| `H47-DEF-01` | **CRITICAL** | Standards & Deaf Eval | Missing `ISO/IEC 20071-24` / `WCAG 1.2.6` mapping and runnable Deaf-centred evaluation kit. | **FIXED & READY** | [H47_ACCESSIBILITY_REQUIREMENTS_MAPPING.md](file:///d:/sign%20interpretor/docs/H47_ACCESSIBILITY_REQUIREMENTS_MAPPING.md) + [eval_protocol_pack.json](file:///d:/sign%20interpretor/artifacts/h47/deaf_eval_kit/eval_protocol_pack.json) |
| `H47-DEF-02` | **HIGH** | `EnglishToISLTranslator.js` / `translate_segments.mjs` | Stateless per-segment `spatial_plan` reset referent loci across cues. | **FIXED & VERIFIED** | `DISCOURSE_LOCUS_PERSISTENCE: PASS` (`teacher1=LOCUS_LEFT, teacher2=LOCUS_LEFT`) |
| `H47-DEF-03` | **HIGH** | `EnglishToISLTranslator.js` / `timeline-synchronizer.js` | Cue-wide NMM broadcast onto unrelated opening nouns. | **FIXED & VERIFIED** | `nmm_scopes` + `NMM_CONSTITUENT_SCOPING: PASS` |
| `H47-DEF-04` | **MEDIUM** | `EnglishToISLTranslator.js` | Polysemy collisions (`right hand` -> `TRUE`, `sign up` dropped, `clearly` dropped). | **FIXED & VERIFIED** | `GENERALIZATION_BENCHMARK: 8/8 PASS` |
| `H47-DEF-05` | **HIGH** | `tools/run_h47_real_chrome_e2e.mjs` | Live Chrome `sampleEmbedPose` omitted `Bip001_Head` & `Bip001_Spine1`. | **FIXED & VERIFIED** | Live Chrome `headSamples` & `spineSamples` captured in `h47_real_chrome_e2e_evidence.json` |
| `H47-DEF-06` | **MEDIUM** | `signs/*.json` | Missing anatomical/feature-cluster trajectory audit across all `647` signs. | **FIXED & VERIFIED** | `h47_audit_trajectory_quality.mjs`: `647` signs, `0` extreme joint warnings |
| `H47-DEF-07` | **GOVERNANCE** | Linguistic Acceptance | Deaf ISL user comprehension and native linguistic acceptance. | **PENDING_DEAF_COMMUNITY_REVIEW** | Honest governance boundary preserved |
