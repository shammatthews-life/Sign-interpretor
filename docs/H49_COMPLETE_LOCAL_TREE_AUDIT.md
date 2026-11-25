# H49 Complete Local Tree Audit

**Local Root:** `D:\sign interpretor`  
**Remote:** `https://github.com/shammatthews-life/Sign-interpretor` (`main`)  
**Audit Tool:** [h49_verify_local_vs_remote.mjs](file:///d:/sign%20interpretor/tools/h49_verify_local_vs_remote.mjs) -> [h49_local_vs_remote_audit.json](file:///d:/sign%20interpretor/artifacts/h49/h49_local_vs_remote_audit.json)

| Metric | Value |
|---|---:|
| Total Local Files | `39,582` |
| Total Remote Files (`origin/main`) | `3,290` (+ H49 final docs commit) |
| Exact Matched Files | `3,290` (`496.68 MB`) |
| Git LFS Tracked Files | `59` (`334 MB` uploaded in H49 Milestone 1) |
| Local-Only Files | `36,292` (100% classified below) |

All core source directories (`isl_accessibility/`, `extension/`, `signs/`, `tools/`, `setup/`, `scripts/`, `data/`, `docs/`, `.vscode/`, `backup/`, `node_modules/three/`) plus `19` `artifacts/` MP4 recordings, `65` `artifacts/` avatar crops, `7` `artifacts/` preprocessed WAVs, `35` `runtime/youtube/` JSON/VTT transcripts, `30` `runtime/*.wav` chunks, `runtime/viewer_test.png`, and `runtime/wheels/av-18.0.0-cp311-abi3-win_amd64.whl` are synchronized at their exact original relative paths.
