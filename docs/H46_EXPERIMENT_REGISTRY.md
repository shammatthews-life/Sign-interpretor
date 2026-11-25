# H46 Experiment Registry

| Experiment ID | Hypothesis / Change | Metric | Result | Commit |
|---|---|---|---|---|
| `EXP-H46-00` | Pre-fix H46 baseline audit | `test_h46_comprehension_and_spatial_audit.mjs` | `0 / 4 PASS` (honest pre-fix baseline) | `694755e` |
| `EXP-H46-01` | Refactor 33 exact rotation-duplicate signs + curls | `SIGN_ROTATION_UNIQUENESS` + `validate:signs` | `0 / 647` duplicates, `647 / 647` valid | `a0dccab` |
| `EXP-H46-02` | End-to-end NMM + `spatial_plan` + 3D skeletal overlays | `test_h46_comprehension_and_spatial_audit.mjs` | `5 / 5 PASS` (`negHeadDelta=0.0699 rad`, `spatialSpineDelta=0.1556 rad`, `whHeadPitchDelta=0.1011 rad`) | `a0dccab` |
| `EXP-H46-03` | Post-seek `waitForVideoBuffered()` in Chrome 158 E2E | `run_h46_real_chrome_e2e.mjs` on A & B | `12` phases A (`11` signs), `12` phases B (`12` signs), zero buffering stalls | Final H46 |
