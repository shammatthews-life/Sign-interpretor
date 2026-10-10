# Voice-to-Sign Execution Roadmap

**Deadline:** November 20, 2026 (IST)

**Tracker started:** October 10, 2026 (IST)

**Current milestone:** Phase 1 — R1 Stabilization (October 11–12)

## Milestone status

| Milestone | Planned dates (IST) | Status | Acceptance summary |
|---|---|---|---|
| Phase 1 — R1 Stabilization | Oct 11–12 | REVIEW REQUIRED | Helper correction and automated/runtime checks pass. Complete manual visual review of individual wrist/finger-axis changes before R1 can pass. |
| Phase 2 — Voice to Text | Oct 13–17 | APPROVED TO START | Owner approved proceeding under the bounded R1 fallback; fresh run captures supported audio, shows transcript, stops cleanly, and reports errors. |
| Phase 3 — Text to Sign Pipeline | Oct 18–24 | NOT STARTED | Transcript tokens resolve to an ordered animation queue; unsupported tokens remain visible. |
| Phase 4 — Vocabulary Coverage | Oct 25–31 | NOT STARTED | Coverage has a defined denominator, provenance, validation, and disclosed limitations. |
| Phase 5 — Extension Options and UX | Nov 1–7 | NOT STARTED | Main flow and playback controls operate reliably through the extension. |
| Phase 6 — Integration and Evaluation | Nov 8–14 | NOT STARTED | Fixed end-to-end test set has measured results and recorded failures. |
| Phase 7 — Release Freeze and Demo | Nov 15–20 | NOT STARTED | Reproducible setup, honest documentation, and demonstration are ready by Nov 20. |

## Phase 1 task register

### R1-NAN-01 — Guard and correct imported helper rotations

- **Planned:** October 11–12, 2026
- **Actual:** October 10, 2026
- **Status:** PASS (this task only)
- **Acceptance criteria:**
  - Inspect the loaded candidates and correct only named orphan helper bones after all safety checks pass.
  - Run the correction after loading/rig resolution but before any imported rest-pose snapshot.
  - Preserve position and scale; verify finite resulting transforms.
  - Do not change skinned skeleton references or articulated hand hierarchy.
  - Unit-test eligible, ineligible, missing, and unrelated nodes.
  - Run focused and R1 regression checks.
- **Implementation:** `tools/avatar_viewer/NonFiniteHelperBoneCorrection.mjs` is a strict two-name allowlist for `PRIVATE_Grenade_Point` and `PRIVATE_Grenade_Point_Low`. Runtime checks require a bone, effectively zero X scale, non-finite imported Euler/quaternion rotation, no children, no loaded skinned-mesh skeleton reference, and no ancestry relationship to protected wrist/hand/finger bones. Only the Euler rotation is reset to identity. The viewer runs this before `userData.initialRotation` and `userData.initialPosition` capture, logs issues, exposes its result, and shows PASS or REVIEW REQUIRED in the R1 status.
- **Loaded-model evidence:** Both named FBX nodes were bones, had X scale `0`, non-finite Euler/quaternion and local/world matrices, no children, no skeleton references, and were not ancestors of the resolved articulated bones. Both positions and all scale components remained unchanged. After correction, both rotations were `[0,0,0]`, both quaternions were `[0,0,0,1]`, matrices were finite, and their captured rest rotations were finite. Runtime result: `status: PASS`, both preservation flags true for both nodes, skeleton references preserved, protected hierarchy preserved.
- **Verification:**
  - `node --test tools\avatar_viewer\NonFiniteHelperBoneCorrection.test.mjs` — PASS, 5/5 tests.
  - `node tools\validate_phase_r1_articulation.mjs` — PASS, source guardrails include correction allowlist/safety/order.
  - `window.AetherRig.articulationTest.runAutomatedSuite()` — 98/98 axis checks, 10/10 poses, 4/4 replay speeds, curl precedence PASS, HAC 32/32, zero non-finite rest components, zero replay reset drift.
  - `git diff --check` — PASS.
- **Visual evidence:** A fresh browser run visually inspected separate neutral right- and left-hand focus views. A right open-palm technical pose with wrist/finger-joint position markers was also inspected. Focus actions caused no bone-quaternion changes. Screenshots were inspected in the live browser and were not added to the repository.
- **Files changed for this task:** `tools/avatar_viewer/index.html`, `tools/avatar_viewer/NonFiniteHelperBoneCorrection.mjs`, `tools/avatar_viewer/NonFiniteHelperBoneCorrection.test.mjs`, `tools/validate_phase_r1_articulation.mjs`.

### R1-VIS-02 — Finish individual-axis visual review

- **Planned:** October 11, 2026; complete by October 12, 2026
- **Status:** REVIEW REQUIRED
- **Acceptance criteria:** In the loaded viewer, visually inspect and record right/left wrist and representative finger X/Y/Z isolated-joint changes plus combined technical poses. Ensure each hand remains fully framed and the animation is reset afterward. Do not modify sign data or claim anatomical correctness based on numeric-only results.
- **Actual review:** On October 10, 2026, used the existing isolated-joint selector and hand-camera controls to inspect wrist X/Y/Z and index-base X/Y/Z on both hands. No sign animation or persistent bone pose was changed. The isolated controls reported the selected axis at +30 degrees (0.52360-radian world-orientation change); this is diagnostic and not treated as visual proof. Wrist X/Y/Z rotations on both hands visibly changed hand/wrist orientation. Left wrist Y initially had body occlusion; a runtime-only camera reposition made the hand more visible. Right wrist Z brought the hand close to the torso. Individual left and right index-base X/Y/Z movements were exercised, but the small changes to rendered finger shape/orientation were subtle and could not be distinguished consistently from overlapping fingers, glove/cuff geometry, and proximity to the torso. Therefore, the visual criterion for each isolated finger axis is not established.
- **Reset/evidence:** Reset the articulation controller to its captured rest pose after inspection; the viewer reported time 0 and zero non-finite rest components. Screenshots were visually inspected in the live browser but were not saved to the repository. Neutral bilateral focus and a right open-palm technical pose were inspected previously; these do not replace the unclear isolated finger-axis evidence.
- **Remaining gap:** The 98/98 automated axis checks verify numeric local/world rotation changes, but do not substitute for clear visual confirmation. The existing R1 report also records that individual left-hand axis views were not conclusively confirmed. This time-boxed visual attempt did not resolve that gap. R1 remains REVIEW REQUIRED.
- **Owner decision (October 10, 2026):** Approved proceeding with Phase 2 under the bounded fallback: retain R1 as REVIEW REQUIRED, explicitly disclose the isolated finger-axis visual limitation, and defer any claim of complete per-axis visual verification. This does not waive R1 acceptance criteria or declare R1 passed.
- **Next action:** Begin Phase 2 on its planned dates (October 13–17). Keep the R1 finger-axis visual follow-up open; no speech-recognition implementation was started as part of R1-VIS-02.

## Risks and guardrails

- R1 remains **REVIEW REQUIRED** until the unclear isolated finger-axis views are resolved or an explicitly approved fallback is recorded; do not infer a visual PASS from the automated suite.
- The correction deliberately does not change the zero X scale or FBX file. Any missing or ineligible expected candidate produces a visible REVIEW REQUIRED result and is not normalized.
- Keep the prior report edits in `docs/r1_fine_grained_articulation_report.json` and `docs/r1_fine_grained_avatar_articulation.md`; do not overwrite them.
- The Aether model is local-only and excluded from Git. Do not upload it or bundle model-derived assets.
- Do not start Phase 2 until Phase 1 passes or an explicitly approved time-boxed fallback is chosen.

## Next task

**Phase 2 — Voice to Text (not started)**

**Planned dates:** October 13–17, 2026 (IST)

**Prerequisite:** Owner approved the bounded R1 fallback on October 10, 2026; R1 remains REVIEW REQUIRED.

**Concrete next action:** Begin the planned Phase 2 work October 13–17 without representing R1 visual verification as complete; retain the finger-axis visual follow-up.
