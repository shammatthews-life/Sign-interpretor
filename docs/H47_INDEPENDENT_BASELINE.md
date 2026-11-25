# H47 Independent Baseline Report (Pre-Fix Phase 0)

**Verified Git Commit:** `f57fd9ab47f60d81269c7ba2c411b0fec4a1ce41` (`origin/main` == `LOCAL_HEAD`)  
**Audit Date:** 2026-11-25  
**Scope:** Independent source-level & runtime forensic verification of H46 before any H47 modifications.

---

## 1. Reproduced H46 Technical Baseline

| Check | Result | What It Proves vs. What It Does NOT Prove |
|---|---|---|
| `npm.cmd test` | `88 / 88 PASS` | Proves JS unit/scheduler/synchronizer logic; does **not** prove Deaf comprehension |
| `npm.cmd run validate:signs` | `647 / 647` valid (`0` exact rotation dupes) | Proves JSON schema & rotation uniqueness; does **not** prove ISLRTC/Deaf linguistic correctness |
| `test_h46_comprehension_and_spatial_audit.mjs` | `5 / 5 PASS` | Proves Node mock-rig bone deltas & `spatial_plan` emission; does **not** prove live Chrome NMM rendering |
| `test_h45_relational_semantics.mjs --strict` | `33 / 33 (100%)` | Proves relational slot & polarity preservation on targeted suite |
| `test_h44_semantic_completeness.mjs` | `60 / 60 (461 / 461 slots)` + `78 / 78 (100%)` | Proves slot recall & order on locked A/B + 78 cases |
| `test_h43_multi_domain_evaluation.mjs` | `44 / 44` | Proves challenge suite + 5-video token coverage |
| `security_audit.mjs` | `[PASS] Security Audit Clean` | Zero secrets exposed |

---

## 2. Independent Forensic Findings (H46 Gaps Uncovered)

1. **Chrome E2E Did Not Sample `Bip001_Head` or `Bip001_Spine1`:**
   - Inspecting `artifacts/h46/evidence/h46_real_chrome_e2e_evidence.json` confirmed `poseKeys` only captured `['currentSign', 'queuedCount', 'viewMode', 'rArm', 'lArm', 'rFore', 'rHand']`. Live Chrome WebGL head/spine NMM actuation was never measured.
2. **Stateless Per-Segment Spatial Loci:**
   - `EnglishToISLTranslator.translate()` resets `locus_assignments` on every call, so referents (`he`, `she`, `teacher`, `team`) do not retain consistent spatial loci across consecutive cues in Videos A & B.
3. **Unscoped Cue-Wide NMM Broadcast:**
   - `timeline-synchronizer.js` broadcasts `cueNmm` identically to every sign in a cue instead of scoping negation (`NMM-NEG-HEADSHAKE`) to negative predicates/particles or `WH` brow-furrow to interrogative scope.
4. **Polysemy / Sense Collisions:**
   - Context-insensitive lexical mapping conflates distinct senses (e.g., `"left"` directional vs past tense of *leave*, `"right"` correct/agree vs lateral direction, `"sign up"` vs *sign*).
5. **Governance Status:**
   - All outputs remain `PENDING_DEAF_COMMUNITY_REVIEW`; no Deaf participant evaluation protocol or kit existed prior to H47.
