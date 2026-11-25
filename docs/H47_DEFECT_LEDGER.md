# H47 Defect Ledger

| ID | Severity | Component | Description | Status |
|---|---|---|---|---|
| `H47-DEF-01` | **CRITICAL** | Evaluation & Standards | Missing `ISO/IEC 20071-24` accessibility mapping and runnable Deaf-centred comprehension evaluation protocol/kit. | **OPEN (Phase 0)** |
| `H47-DEF-02` | **HIGH** | `EnglishToISLTranslator.js` / `translate_segments.mjs` | Stateless per-segment `spatial_plan` resets referent loci across consecutive cues. | **OPEN (Phase 0)** |
| `H47-DEF-03` | **HIGH** | `EnglishToISLTranslator.js` / `timeline-synchronizer.js` | NMMs applied uniformly to all signs in a cue instead of scoped to predicate/negation/WH constituents. | **OPEN (Phase 0)** |
| `H47-DEF-04` | **MEDIUM** | `EnglishToISLTranslator.js` | Polysemy collisions (`left` depart vs direction, `right` correct vs direction, `sign up` vs `sign`). | **OPEN (Phase 0)** |
| `H47-DEF-05` | **HIGH** | `tools/run_h46_real_chrome_e2e.mjs` -> H47 E2E | Live Chrome `sampleEmbedPose` omits `Bip001_Head` & `Bip001_Spine1` telemetry. | **OPEN (Phase 0)** |
| `H47-DEF-06` | **MEDIUM** | `signs/*.json` & `SignScheduler.js` | Missing anatomical/feature-cluster trajectory audit across all `647` signs & `2.2x` tempo readability check. | **OPEN (Phase 0)** |
| `H47-DEF-07` | **GOVERNANCE** | Linguistic Acceptance | Deaf ISL user comprehension and native linguistic acceptance remain unverified. | **PENDING_DEAF_COMMUNITY_REVIEW** |
