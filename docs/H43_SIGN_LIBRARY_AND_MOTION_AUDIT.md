# H43 — Sign Library & Motion Quality Audit (WS4)

**Status:** COMPLETE (`PENDING_DEAF_COMMUNITY_REVIEW` for linguistic articulation acceptance)  
**Addresses Defects:** `DEF-H43-002`, `DEF-H43-008`, `DEF-H43-009`, `DEF-H43-011`, `DEF-H43-012`

---

## 1. Independent Baseline Defects Uncovered
1. **Radian vs Degree Unit Mismatch (`DEF-H43-011`):** `SignAnimationPlayer.js` multiplies keyframe `rotations` by `Math.PI / 180.0` (expecting degrees) and calls `THREE.MathUtils.degToRad(curlDeg)` on `finger_curls`. Forensic inspection across the 596 H42 `signs/*.json` files revealed:
   - **401 / 596** sign files stored bone rotations in **radians** (`maxRot < 5`), resulting in near-zero joint rotation (`~0.8°` instead of `~46°`) during playback!
   - **323 / 596** sign files stored `finger_curls` normalized to `0..1.5` instead of degrees (`~1°` instead of `60°–80°`).
2. **Bimanual `finger_curls` Silently Ignored (`DEF-H43-012`):** `SignAnimationPlayer.js:271-296` looked up `this.handRig[domSide]`. Because `HandRig` only has `left` and `right` keys, **324** `dominant_hand: "both"` signs never curled either hand unless every individual phalanx bone was explicitly keyframed.
3. **550-Sign Preload Cutoff (`DEF-H43-002`):** `tools/avatar_viewer/index.html` preloaded only a static 550-ID array, causing `SignLibrary.getPlayable()` to throw `NOT_PRELOADED` for newer H37–H42 vocabulary even when `.json` files existed on disk.
4. **Dynamic Fingerspelling Never Synthesized by `SignLibrary` (`DEF-H43-008`):** `ISLFingerspelling.js` exposed `composeFingerspellingMotion(word)`, but `SignLibrary.loadSign()` and `SignLibrary.getPlayable()` did not invoke it for `fs_<word>` IDs, causing HTTP 404 or `NOT_PRELOADED`.
5. **122 Signs Shared Duplicate Keyframes Across 21 Template Clusters (`DEF-H43-009`):** A 51-sign cluster (`action`, `video`, `picture`, `happy`, `bad`, `easy`, `hard`, `teacher`, `school`, `story`, `today`, `different`, `important`, `small`, etc.) and 20 smaller clusters (`hear/imagine/tell/true/understand`, `brain/eat/eye/flower/mind/phone/sound/wrong`, `clear/finish/great/open/public/world`, `read/write`, `first/second`, `minute/year`, etc.) shared byte-for-byte identical keyframes while carrying misleading per-sign gloss notes.

---

## 2. Engineering Fixes Implemented
1. **`tools/avatar_viewer/SignAnimationPlayer.js`:**
   - Updated `applyFrame()` to iterate over `targetSides = domSide === 'both' ? ['left', 'right'] : [domSide]`.
   - Added support for both flat `{ thumb, index, middle, ring, pinky }` and per-hand `{ left: {...}, right: {...} }` `finger_curls` dictionaries, guarding non-finite values with `Number.isFinite()`.
   - Added unit tests in `tools/avatar_viewer/SignAnimationPlayer.test.mjs` verifying degree-to-radian conversion, bimanual `dominant_hand: 'both'` finger curling, and per-hand curl dictionaries.
2. **`tools/avatar_viewer/SignLibrary.js`:**
   - Added `preloadBundle(bundleUrl, manifestUrl)` loading all signs via a single `GET /signs/bundle.json` request (falling back cleanly to array or map `manifest.signs`), plus `fs_<word>` synthesis via `ISLFingerspelling.js` (`composeFingerspellingMotion`) in both `loadSign()` and `getPlayable()`.
   - Added verification tests in `tools/avatar_viewer/SignLibrary.test.mjs`.
3. **`tools/h43_fix_sign_units_and_curate.mjs`:**
   - Converted all **401** radian-scale sign files to calibrated degrees (`* 180 / Math.PI`, clamped `[-175, 175]`) and **323** normalized `finger_curls` to degrees (`* 80`, clamped `[0, 120]`).
   - Replaced all **105** non-canonical duplicate cluster entries and upgraded core benchmark signs with distinct ISLRTC-grounded parametric `Bip001_*` articulations (`provenance_tier: "h43_linguistic_articulation_parametric"`, `motion_distinctness: "unique_trajectory"`).
   - Authored **27** missing grammatical, ordinal/temporal, and multi-domain signs: `without`, `because`, `but`, `or`, `why`, `if`, `already`, `maybe`, `also`, `evening`, `eight`, `nine`, `third`, `back`, `feature`, `film`, `scene`, `robot`, `network`, `pixel`, `digit`, `layer`, `neuron`, `weight`, `single`, `african`, `africa`.
4. **`tools/sync_and_validate_signs_manifest.mjs`:**
   - Preserves honest `provenance_tier`, `motion_distinctness`, and `validation_status` (`IMPLEMENTATION_PENDING_LINGUISTIC_REVIEW`) across all 623 signs in `signs/manifest.json`.

---

## 3. Post-Fix Verification Metrics
- **Total Valid Playable Signs:** `627` (up from `596`; added 27 grammatical/domain signs + `he`, `she`, `get`, `wind`)
- **Radian-Scale Signs (`maxRot < 5°`) Remaining:** `0`
- **Normalized Small `finger_curls` (`<= 1.55`) Remaining:** `0`
- **Maximum Joint Rotation Angle Across Library:** `108°` (all within safe kinematic range)
- **Duplicate Trajectory Clusters Remaining:** `0` (`627 / 627` unique keyframe trajectories)
- **Manifest & Python Backend Schema Validation:** `627 / 627` pass both `npm.cmd run validate:signs` and `tools/run_avatar_viewer.py` `validate_sign_definition()` (after adding missing `return_to_neutral` and `transition_hints` to 4 legacy signs `better.json`, `ok.json`, `throw.json`, `usually.json`).
