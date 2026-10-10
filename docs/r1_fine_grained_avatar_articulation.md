# R1 — Fine-Grained Avatar Articulation

**Overall status: REVIEW REQUIRED.** The live Aether automated articulation
suite passes, and the two imported helper rotations have been corrected with
position and scale preserved. Isolated finger-axis visual verification remains
inconclusive.

**Scope:** technical rig articulation only. The poses and tests below are not
ISL signs and do not establish linguistic or anatomical correctness.

## Runtime and rig

- Branch: `r1-articulation-coverage-and-report`
- Verified commit: `2608ba357c70e030d4ad9063d988fb09a22d150d`
- Viewer: `http://localhost:8000/tools/avatar_viewer/index.html`
- Local Aether model: `Avatar_Boy_Gun_AetherShadow` FBX and textures
- Runtime bone map: 243 bones
- Hand audit: 34 entries (two forearms, two hand roots, and 30 finger
  segments)
- Both left and right hand chains were present in the runtime map. The
  independent-joint matrix covered thumb, index, middle, ring, and pinky base,
  middle, and tip joints on both sides, plus both hand roots.
- X/Y/Z were independently tested for every one of the 30 finger segments and
  both hand roots. The hand-root X checks include flexion and extension.

The viewer exposes per-bone X/Y/Z authoring controls for the controlled bones.
`SignAuthoringController` captures and serializes rotations relative to the
captured rest pose. The existing sign schema can represent these fine-grained
rotations; no schema change was needed. The current runtime applies explicit
rotations without replacing them with the legacy curl pass, while preserving
the legacy curl fallback on unkeyframed neighboring joints.

## Expanded live browser suite

The suite was run in the actual local Aether viewer using
`window.AetherRig.articulationTest.runAutomatedSuite()`. Results were captured
from the live runtime and are included in
[`r1_fine_grained_articulation_report.json`](r1_fine_grained_articulation_report.json).

| Check | Result |
|---|---:|
| World-orientation axis checks | **98/98 PASS** |
| X axis | 34/34 PASS |
| Y axis | 32/32 PASS |
| Z axis | 32/32 PASS |
| HAC (all tested joints require all axes) | **32/32** |
| Technical poses | **10/10 PASS** |
| Replay rates | **4/4 PASS**, three repeats each |
| Maximum measured replay reset drift | **0 radians** |
| Curl precedence | **PASS** |

Each axis test measured a finite, non-zero world-orientation change. Child
displacement was recorded as diagnostic evidence rather than being the sole
movement criterion. The 34 X checks are 30 finger axes plus two axes for each
hand root (flexion and extension); Y and Z each have 30 finger axes and one
axis check for each hand root.

The HAC numerator is 32 because the test requires all three axes to pass for
each of the 30 finger joints and two hand roots. This is a technical coverage
metric, not an anatomical or ISL accuracy score.

### Technical poses

All ten viewer fixtures passed their automated checks:

1. neutral hand
2. all fingers extended
3. partially curled fingers
4. fist
5. thumb/index isolated
6. open palm
7. wrist flexed
8. wrist extended
9. wrist rotated
10. asymmetric finger test

These are technical test poses, not lexical signs.

### Curl precedence

- Explicit right index-base bone `Bip001_R_Finger1`: expected 20 degrees,
  observed 20 degrees; authored rotation was preserved.
- Unkeyframed neighboring bone `Bip001_R_Finger11`: expected 80 degrees,
  observed 80 degrees; legacy curl fallback remained active.
- Both regression conditions passed; fallback behavior was not removed.

### Replay and reset

At 0.5×, 1.0×, 1.25×, and 1.5×, each repeated three times, the suite observed
the mid-pose, reset successfully, and measured zero reset drift. This
automated result found no rotation accumulation in those runs.

## Non-finite imported rest values — guarded correction verified

The live report initially identified four non-finite rotation components on
two nodes unrelated to the hand joints:

| Runtime node | Parent | Imported X scale | Component | Value |
|---|---|---:|---|---|
| `PRIVATE_Grenade_Point` | `Avatar_Boy_Gun_AetherShadow` | 0 | `rotation.x` | NaN |
| `PRIVATE_Grenade_Point` | `Avatar_Boy_Gun_AetherShadow` | 0 | `rotation.y` | NaN |
| `PRIVATE_Grenade_Point_Low` | `Avatar_Boy_Gun_AetherShadow` | 0 | `rotation.x` | NaN |
| `PRIVATE_Grenade_Point_Low` | `Avatar_Boy_Gun_AetherShadow` | 0 | `rotation.y` | NaN |

The nodes' local quaternions and matrices were also non-finite after loading.
The guarded runtime correction applies only to these two allowlisted,
childless helper bones after verifying their zero X scale, non-finite rotation,
absence from loaded skeleton references, and lack of ancestry over protected
articulated bones. It resets only their rotations to identity before rest-pose
capture. Runtime checks confirmed finite captured rest rotations, preserved
position, scale, skeleton references, and articulated hierarchy. The zero X
scale was not changed. The focused correction tests passed 5/5 and the static
validator passed. This resolves the helper-rotation correction gate without
changing the FBX model.

## Visual verification

The actual rendered avatar was inspected in the browser:

- The right-hand technical fist and open-palm views showed visibly different
  hand poses.
- Neutral close-up framing was usable for both the left and right hand.
- Wrist X/Y/Z controls were exercised on both sides; changes in wrist/hand
  orientation were visible. Left wrist Y initially had body occlusion, which
  a runtime-only camera reposition reduced. Right wrist Z brought the hand
  close to the torso.
- Index-base X/Y/Z controls were exercised on both sides, but rendered finger
  changes were subtle and not consistently distinguishable from overlapping
  fingers and glove/cuff geometry.
- The expanded automated suite independently reports finite world-orientation
  changes for both hands and every covered axis.
- A right open-palm technical pose was inspected; it does not establish clear
  isolated finger-axis movement.

Therefore, visual verification is **PARTIAL**. Numeric transform checks do
not prove every rendered joint moves as intended. The articulation controller
was reset to its captured rest pose afterward. No avatar screenshot was
committed; local browser screenshots were inspected during the session.

## Regression and sign protection

The applicable recorded regressions passed:

- B, C, D, E2, E3, F1, F2
- G1, G2, G3
- H1–H6
- H7 cached-audio pipeline (256 transcript segments; no redownload)
- H8 local runtime harness, including invalid YouTube URL HTTP 400, unknown
  job HTTP 404, cached job completion, and handoff of three playable `good`
  occurrences
- Sentence pipeline and speech/sign orchestrator
- SignLibrary validation (13 dictionary entries; 13 missing visual assets
  remain under the existing evidence gate)
- `git diff --check`

The H8 harness is not evidence of an installed extension session on a live
YouTube tab; that check remains not run.

SHA-256 hashes of `signs/hello.json`, `signs/good.json`,
`signs/morning.json`, and `signs/water.json` were rechecked and are recorded
in the JSON report. They match the unchanged baseline; no lexical sign file
was modified.

## Conclusion and remaining gates

The runtime can represent and replay fine-grained rotations across both hand
chains, and its automated suite passed. R1 remains **REVIEW REQUIRED**, not
complete, until:

1. Clear visual confirmation of isolated finger-axis movement is obtained on
   both hands; numeric-only results are insufficient.
2. The final diff and regression state are rechecked after follow-up work.

No lexical ISL sign was created or changed as part of this articulation test.
