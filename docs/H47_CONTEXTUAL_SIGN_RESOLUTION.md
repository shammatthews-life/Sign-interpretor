# H47 Contextual Sign Resolution Report

- **Polysemy Defects Discovered & Fixed (`H47-DEF-04`):**
  1. `"Look at your right hand"` previously mapped `"right"` -> `TRUE` (`YOUR TRUE HAND LOOK`); fixed via contextual multiword entries (`"right hand"` -> `SIDE HAND`, `"right side"` -> `SIDE`, `"turn right"` -> `TURN SIDE`).
  2. `"Sign up for the class"` previously dropped `"sign up"` (`CLASS`); fixed via `["sign up", ["JOIN"]]`.
  3. `"clearly"` was unmapped; added `["clearly", "CLEAR"]`.
- **Verification:** `8/8` on [h47_generalization_benchmark.json](file:///d:/sign%20interpretor/artifacts/h47/h47_generalization_benchmark.json) with zero regressions on locked Videos A & B (`60/60`, `461/461` slots).
