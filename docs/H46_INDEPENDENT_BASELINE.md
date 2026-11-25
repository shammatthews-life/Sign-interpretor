# H46 Independent Baseline Report (Pre-Fix Phase 0)

**Baseline Git Commit:** `749a6eedfbdb453ba5a0a3cb64a7d2d4a03dce15` (`origin/main` == `LOCAL_HEAD`)  
**Audit Date:** 2026-11-25  
**Scope:** Independent reproduction of H45 metrics, engine sync audit, NMM/spatial transport audit, sign-library visual uniqueness audit, and initial failing H46 baseline.

---

## 1. Reproduced H45 Engineering & Test Metrics

| Check | Command | Observed Result |
|---|---|---|
| Unit Test Suite | `npm.cmd test` | `88 / 88 PASS` |
| Sign Library Schema Validator | `npm.cmd run validate:signs` | `647 / 647` valid |
| Strict Relational Semantics | `node tools/test_h45_relational_semantics.mjs --strict` | `33 / 33 (100%)` |
| Semantic Completeness | `node tools/test_h44_semantic_completeness.mjs` | `60 / 60 (461 / 461 slots)` + `78 / 78 (100%)` |
| Multi-Domain Benchmark | `node tools/test_h43_multi_domain_evaluation.mjs` | `44 / 44`; A `100%`, B `100%`, `xrwz9IxpMJg` `86.82%` (`17` unk), `aircAruvnKk` `75.98%` (`61` unk), `D9Ihs241zeg` `74.88%` (`51` unk) |
| Security Audit | `node tools/security_audit.mjs` | `[PASS] Security Audit Clean` |

---

## 2. Independent Forensic Findings (Why H45 Is Not Yet Visually Complete ISL)

1. **Zero End-to-End NMM & Spatial Grammar Rendering (`0` Transport Matches):**
   - `EnglishToISLTranslator.js` outputs `non_manual_markers` in JSON, but probing `tools/youtube_pipeline/translate_segments.mjs`, `extension/shared/youtube-cue-manifest.js`, `extension/content/timeline-synchronizer.js`, and `extension/viewer/embed.js` returned **0 matches** for `non_manual|nmm|spatial|locus|role_shift`.
   - Consequently, the 3D avatar in Chrome receives **no** non-manual cues (`NMM-NEG-HEADSHAKE`, `NMM-WH-BROW-FURROW`, `NMM-YESNO-BROW-RAISE`, `NMM-EMPHATIC-NOD`, `NMM-COND-BROW-RAISE`) and **no** spatial referent locus, role-shift, or directional verb inflection vectors.

2. **33 Exact Rotation-Duplicate Signs (`13` Duplicate Groups across `46` Sign Files):**
   - Independent hash comparison of `motion.keyframes[].rotations` across all `647` JSON files in `signs/` confirmed **13 exact rotation-duplicate groups** (`33` redundant duplicate files):
     - `action <=> hold <=> minute`
     - `add <=> keep <=> long <=> new <=> next <=> off <=> room <=> slide <=> team`
     - `already <=> video`
     - `ask <=> first <=> life <=> question <=> show <=> win`
     - `base <=> board <=> communication`
     - `beautiful <=> eat <=> tell`
     - `catch <=> left <=> other <=> pick <=> seven <=> should <=> six`
     - `chest <=> myself`
     - `evening <=> read`
     - `fifth <=> fourth`
     - `five <=> three <=> two`
     - `open <=> scene`
     - `thirty <=> twenty`
   - High-frequency Video A/B pairs (`beautiful<=>tell`, `base<=>communication`, `five<=>two/three`, `thirty<=>twenty`, `already<=>video`, `open<=>scene`, `ask<=>show/life/first`, `action<=>hold/minute`, `add<=>new/next/room`, `catch<=>other`) render **identically** on the 3D skeleton.

3. **Zero-Curl & Static-Head Sign Counts:**
   - `94 / 647` sign JSON files have zero non-zero `finger_curls` across all keyframes.
   - `421 / 647` sign JSON files have zero `Bip001_Head` motion in keyframes (making runtime procedural NMM actuation essential).

4. **Engine File Sync Status:**
   - `EnglishToISLTranslator.js`, `SemanticUnderstandingEngine.js`, and `SignScheduler.js` hashes match between `tools/avatar_viewer/` and `extension/viewer/engine/`.
   - `SignAnimationPlayer.js` differs only on line 13 (`import * as THREE from 'three'` vs `'../../vendor/three/three.module.min.js'`).

5. **Open H45 Issues Preserved:**
   - Video A post-seek YouTube buffering spinner in Chrome E2E (`readyState >= 3` was checked only at `t = 3.0s`).
   - Linguistic validation remains `PENDING_DEAF_COMMUNITY_REVIEW`.
