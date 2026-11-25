# H44 Real-Chrome End-to-End Evidence Report

## 1. Execution Method (Genuine Runtime Pipeline)
Verified inside real Google Chrome `158.0.8127.88` with unpacked `extension/` loaded via CDP port `9226` connected to the local runtime server on `http://127.0.0.1:8000` (`small.en` CUDA ASR + `635`-sign `/signs/bundle.json`) — **with zero manual postMessage shortcuts**:
1. Cleared YouTube ads honestly (`ad_clear.cleared === true` for both videos).
2. Engaged Full Body camera mode (`#btn-avatar-full` + `AetherEmbed.setViewMode('full')`).
3. Connected extension popup (`popup.html`) to runtime and submitted `https://www.youtube.com/watch?v=...` -> `#btn-youtube-process` -> `service-worker.js` -> `POST /youtube/process` -> `YOUTUBE_CUES_READY` -> `YouTubeTimelineSynchronizer.setCueManifest(...)`.

## 2. Measured Browser Telemetry (`h44_real_chrome_e2e_evidence.json`)
| Metric | Video A (`MXKkXXYUxBc`) | Video B (`y8tFSuOMAqQ`) |
| :--- | :--- | :--- |
| Ad Clearance Attempts | `7` (cleared `true`) | `1` (cleared `true`) |
| Loaded Signs in Aether WebGL | `635` | `635` |
| Pipeline Segments Delivered | `2090` (`SUPPORTED 733`) | `278` (`SUPPORTED 131`) |
| Observed Distinct Active Signs Across 12 Phases | `11` (`public`, `new`, `people`, `goal`, `many`, `speaker`, `find`, `true`, `what`, `confused`, `nervous`) | `12` (`summer`, `that`, `you`, `first`, `know`, `tired`, `story`, `most`, `people`, `problem`, `i`, `advice`) |
| Non-Neutral Pose Phases | `12 / 12` | `12 / 12` |
| Transport Pause / Resume Verified | `true` / `true` | `true` / `true` |
| Playback Speed `1.5x` / `0.5x` Verified | `true` / `true` | `true` / `true` |
| Forward Seek & Backward Seek Verified | `true` / `true` | `true` / `true` |
| Half-Body <-> Full-Body Toggle Verified | `true` (restored `full`) | `true` (restored `full`) |
| Screencast Frames -> NVENC MP4 | `793` frames ([h44_video_a_recording.mp4](file:///d:/sign%20interpretor/artifacts/h44/recordings/h44_video_a_recording.mp4)) | `788` frames ([h44_video_b_recording.mp4](file:///d:/sign%20interpretor/artifacts/h44/recordings/h44_video_b_recording.mp4)) |

## 3. Visual Inspection Confirmation
Visual inspection of [h44_video_a_contact_sheet.png](file:///d:/sign%20interpretor/artifacts/h44/contact_sheets/video_a/h44_video_a_contact_sheet.png), [h44_video_a_avatar_crops_sheet.png](file:///d:/sign%20interpretor/artifacts/h44/contact_sheets/video_a/h44_video_a_avatar_crops_sheet.png), [h44_video_b_contact_sheet.png](file:///d:/sign%20interpretor/artifacts/h44/contact_sheets/video_b/h44_video_b_contact_sheet.png), [h44_video_b_avatar_crops_sheet.png](file:///d:/sign%20interpretor/artifacts/h44/contact_sheets/video_b/h44_video_b_avatar_crops_sheet.png), `04_seek_forward.png`, and `11_half_body_toggle.png` confirmed crisp head-to-toe Full Body framing, active two-handed & single-handed trajectories (`PUBLIC`, `NEW`, `MANY`, `CONFUSED`, `THAT`, `KNOW`, `I`, `MATTER`), synchronized YouTube captions beneath the speaker, and responsive Half Body toggle.

Full telemetry: [h44_real_chrome_e2e_evidence.json](file:///d:/sign%20interpretor/artifacts/h44/evidence/h44_real_chrome_e2e_evidence.json).
