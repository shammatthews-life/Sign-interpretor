# H46 Defect Ledger (Final Status)

| ID | Severity | Component | Defect Description | Final Status | Verification Evidence |
|---|---|---|---|---|---|
| `H46-DEF-01` | **CRITICAL** | `translate_segments.mjs` / `youtube-cue-manifest.js` / `timeline-synchronizer.js` / `content-script.js` / `embed.js` / `SignScheduler.js` | `non_manual_markers` dropped before reaching 3D avatar. | **FIXED & VERIFIED** | `test_h46_comprehension_and_spatial_audit.mjs` (`MANIFEST_NMM_SPATIAL_TRANSPORT: PASS`) + `npm test` (`88/88`) |
| `H46-DEF-02` | **CRITICAL** | `SignAnimationPlayer.js` | `applyFrame()` lacked procedural NMM actuation on `Bip001_Head` / `Bip001_Spine1`. | **FIXED & VERIFIED** | `PLAYER_3D_NMM_AND_SPATIAL_ACTUATION`: `negHeadDelta=0.0699 rad`, `whHeadPitchDelta=0.1011 rad` |
| `H46-DEF-03` | **CRITICAL** | `EnglishToISLTranslator.js` & `SignAnimationPlayer.js` | No `spatial_plan` (referent loci, role shifts, directional verbs) emitted or rendered. | **FIXED & VERIFIED** | `TRANSLATOR_SPATIAL_PLAN` (`locus=3, dir=2`) + `spatialSpineDelta=0.1556 rad` |
| `H46-DEF-04` | **HIGH** | `signs/*.json` | `13` exact rotation-duplicate groups (`33` excess signs) across `647` signs. | **FIXED & VERIFIED** | `h46_repair_duplicate_signs.mjs` -> `SIGN_ROTATION_UNIQUENESS: 0` duplicate groups / `647` signs |
| `H46-DEF-05` | **MEDIUM** | `signs/*.json` | `33` duplicate signs lacked distinct `finger_curls`. | **FIXED & VERIFIED** | All `33` repaired signs now include explicit ISLRTC-aligned `finger_curls` |
| `H46-DEF-06` | **HIGH** | `tools/run_h46_real_chrome_e2e.mjs` | Video A post-seek YouTube buffering spinner in Chrome. | **FIXED & VERIFIED** | `waitForVideoBuffered()` after `seek_forward` & `seek_back`; clean 12-frame Chrome contact sheets on A & B |
| `H46-DEF-07` | **GOVERNANCE** | Linguistic Validation | All ISL rules, spatial conventions, and repaired sign trajectories remain unreviewed by Deaf ISL linguists. | **PENDING_DEAF_COMMUNITY_REVIEW** | Honest governance boundary preserved |
