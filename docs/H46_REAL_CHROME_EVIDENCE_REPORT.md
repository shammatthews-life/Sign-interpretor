# H46 Real-Chrome E2E Visual & Pipeline Evidence Report

**Harness:** [run_h46_real_chrome_e2e.mjs](file:///d:/sign%20interpretor/tools/run_h46_real_chrome_e2e.mjs) (Chrome `158.0.8127.88`, unpacked `extension/`, local port `8000` runtime with CUDA `small.en`)  
**Evidence JSON:** [h46_real_chrome_e2e_evidence.json](file:///d:/sign%20interpretor/artifacts/h46/evidence/h46_real_chrome_e2e_evidence.json)

## 1. Locked Video Results

| Video | Ads Cleared | Pipeline READY | Avatar Surface | Phases | Distinct Signs Observed |
|---|---|---|---|---:|---|
| Video A (`MXKkXXYUxBc`) | `true` (7 attempts) | `segCount: 2090` | `400x478` (`Full Body` + `Half Body` toggle) | `12` | `11` (`public`, `people`, `goal`, `confused`, `five`, `find`, `true`, `what`, `speaker`, `this`, `close`) |
| Video B (`y8tFSuOMAqQ`) | `true` (1 attempt) | `segCount: 278` | `400x478` (`Full Body` + `Half Body` toggle) | `12` | `12` (`i`, `maybe`, `your`, `write`, `you`, `story`, `because`, `everyone`, `problem`, `that`, `advice`, `want`) |

## 2. Post-Seek Buffering Fix & Visual Inspection

- `waitForVideoBuffered()` was added after `seek_forward` and `seek_back`.
- Direct visual inspection of [h46_video_a_contact_sheet.png](file:///d:/sign%20interpretor/artifacts/h46/contact_sheets/video_a/h46_video_a_contact_sheet.png), [h46_video_a_avatar_crops_sheet.png](file:///d:/sign%20interpretor/artifacts/h46/contact_sheets/video_a/h46_video_a_avatar_crops_sheet.png), [h46_video_b_contact_sheet.png](file:///d:/sign%20interpretor/artifacts/h46/contact_sheets/video_b/h46_video_b_contact_sheet.png), and [h46_video_b_avatar_crops_sheet.png](file:///d:/sign%20interpretor/artifacts/h46/contact_sheets/video_b/h46_video_b_avatar_crops_sheet.png) confirms zero buffering spinners, clean head-to-toe Full Body framing, responsive Half Body toggle on frame 11, and distinct signing poses across both videos.
- NVENC MP4 recordings generated in `artifacts/h46/recordings/` (gitignored).
