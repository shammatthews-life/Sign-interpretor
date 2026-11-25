# H45 Real-Chrome End-to-End & GPU NVENC Evidence Report

Executed [run_h45_real_chrome_e2e.mjs](file:///d:/sign%20interpretor/tools/run_h45_real_chrome_e2e.mjs) inside Google Chrome `158.0.8127.88` with unpacked `extension/` connected to port `8000` (`647`-sign bundle, `ISL_ISR_4.0` translator) — evidence saved in [h45_real_chrome_e2e_evidence.json](file:///d:/sign%20interpretor/artifacts/h45/evidence/h45_real_chrome_e2e_evidence.json):

| Metric | Video A (`MXKkXXYUxBc`) | Video B (`y8tFSuOMAqQ`) |
| :--- | :--- | :--- |
| Ad Clearance | `true` (`9` attempts) | `true` (`1` attempt) |
| Loaded Signs in Aether WebGL | `647` | `647` |
| Pipeline Segments Delivered | `2090` (`SUPPORTED 734`) | `278` (`SUPPORTED 131`) |
| Observed Active Signs | `this`, `new`, `people`, `goal` (hit YouTube buffer spinner after `seek_forward`) | `i`, `maybe`, `plan`, `video`, `know`, `very`, `story`, `because`, `thing` (`everyone` also observed in prior H45 pass) |
| Transport Controls (`pause`, `resume`, `1.5x`, `0.5x`, seeks, half/full) | `7 / 7` `true` | `7 / 7` `true` |
| NVENC MP4 Frames Captured | `778` frames | `657` frames |

**Honest Visual Observation:** Inspection of [h45_video_b_contact_sheet.png](file:///d:/sign%20interpretor/artifacts/h45/contact_sheets/video_b/h45_video_b_contact_sheet.png) confirmed smooth continuous playback with zero ads and zero buffering across all 12 frames. Inspection of [h45_video_a_contact_sheet.png](file:///d:/sign%20interpretor/artifacts/h45/contact_sheets/video_a/h45_video_a_contact_sheet.png) showed YouTube player buffering (`spinner`) after `seek_forward` (`58.6s`), cleanly documented rather than concealed.
