# R1 — Fine-Grained Avatar Articulation

**Status: IN PROGRESS — expanded runtime verification required.**  
**Scope:** technical rig articulation only; this report does not establish that any technical pose is a linguistically correct ISL sign.

## Verified source findings

The published runtime source was inspected on the review branch:

- `SignAnimationPlayer.js` contains a legacy finger-curl fallback that skips bones with explicit rotation entries in either endpoint keyframe.
- `SignAuthoringController.js` captures, applies, validates, and serializes X/Y/Z rotation deltas relative to the captured rest pose.
- `index.html` generates separate X, Y, and Z sliders for every name returned by `controlledNames()`, including the controlled hand/finger chains and arm/hand-root bones.
- `run_avatar_viewer.py` maps URL-validation `ValueError` exceptions in `POST /youtube/process` to HTTP 400. The H8 runtime report records the invalid-URL test passing.
- Existing lexical sign JSON files were hash-checked during the source synchronization and were not modified.

## Previously recorded local runtime evidence

The local agent run log from October 9, 2026 records these results from the version before the expanded all-axis suite in this branch:

| Check | Recorded result |
|---|---|
| Isolated joint checks in the earlier suite | 36/36 passed |
| Technical poses | 10/10 passed |
| Replay speeds | 0.5×, 1.0×, 1.25×, and 1.5× passed; three repeats per speed |
| Mid-pose observation | True |
| Maximum reset drift in those replay checks | 0 |
| Earlier HAC-style unique-joint coverage | 32/32 |
| Non-finite captured rest-pose components | 4 — not yet attributed to exact bones/components in the earlier output |
| Visual checks recorded | Neutral, technical fist, open-palm pose, right index-base isolated test, and right wrist flexion view |

Those results are retained as prior evidence, **not** represented as a run of the expanded suite introduced in this follow-up. Technical poses are diagnostics; they are not ISL signs.

## Changes in this follow-up

1. The R1 isolated-joint matrix now generates independent local X/Y/Z checks for every available finger segment, and X/Y/Z checks for each hand-root joint (plus a negative-X wrist check).
2. Hand Articulation Completeness (HAC) counts an anatomical joint only when **all** of that joint's axis checks pass, rather than counting it after one successful axis.
3. A targeted runtime regression checks that an explicitly authored finger rotation is preserved while the legacy curl fallback still affects a neighbouring, unkeyframed joint.
4. The result captures the exact bone/component/value for each non-finite rest-pose component, rather than reporting only a count.
5. The viewer status reports the axis checks, technical poses, replay speeds, curl-precedence check, HAC, and non-finite rest-component count. Any remaining non-finite rest values keep the overall disposition at **REVIEW REQUIRED**.
6. `tools/validate_phase_r1_articulation.mjs` checks that the important source guardrails are present. It is a static source check; it is not a runtime or visual test.

With the intended rig map (30 finger segments and two hand-root joints), the expanded matrix is expected to expose 98 axis tests. The actual number must be read from the live viewer after the updated branch is checked out.

## Remaining completion gates

- Run `node tools/validate_phase_r1_articulation.mjs` and the full existing regression suite after updating the local checkout.
- Open the current Aether viewer and run `window.AetherRig.articulationTest.runAutomatedSuite()`. Save the resulting `window.AetherRig.articulationTestResults` output with the updated report.
- Inspect the reported non-finite components by exact bone name and component. Determine whether these arise from the imported model/rig or from viewer initialization. Do **not** silently replace them with zero; document and test any normalization change before making it.
- Visually inspect isolated X, Y, and Z movement for each relevant wrist/finger segment with a close-up view. Property changes and descendant displacement are not alone proof of anatomically correct motion.
- Repeat the visual technical-pose checks and replay/reset tests on the updated code.
- Keep lexical sign JSON unchanged unless a generic runtime fix demonstrably requires an edit and before/after hashes are reviewed.

## Acceptance

R1 is **not yet marked complete**. Completion requires the expanded target-runtime suite, reviewed non-finite rest-component details, visual checks of the newly covered axes, successful regressions, and a final report with the actual updated results.

H8's local API/worker harness was recorded as passing, including invalid URL HTTP 400 and cached job processing. A real session with the unpacked Chrome extension installed and active on a live YouTube tab remains unverified in the existing H8 report.
