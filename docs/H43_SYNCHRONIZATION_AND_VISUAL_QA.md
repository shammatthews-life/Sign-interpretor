# H43 — Synchronization & Real-Chrome Visual QA Report (WS6)

**Status:** VERIFIED IN REAL GOOGLE CHROME + DIRECT3D 11 + NVENC  
**Addresses Defects:** `DEF-H43-001`, `DEF-H43-003`, `DEF-H43-010`, `DEF-H43-011`, `DEF-H43-012`

---

## 1. Visual Verification Summary (`tools/run_h43_real_browser_visual_audit.mjs`)
Real Chrome `158.0.8127.88` was launched with the unpacked extension (`extension/`) loaded on CDP port `9225`, Direct3D 11 GPU acceleration enabled, and backend daemon `http://localhost:8000` serving `Avatar_Boy_Gun_AetherShadow.fbx` and `/signs/bundle.json` (`627` signs).

### Visual Audit Across Three Real YouTube Videos
| Video Key | Video ID | Domain | Ad Cleared (`.ad-showing === false`) | Full Body Engaged | Active Signs Observed | Right Arm Z Span | Screencast Frames | NVENC MP4 (`h264_nvenc`) |
|---|---|---|---|---|---|---:|---:|---:|
| `video_a` | `MXKkXXYUxBc` | Public Speaking Tutorial | Yes (attempt 1) | Yes (`viewMode: "full"`) | `11` (`this`, `speech`, `learn`, `you`, `confused`, `nervous`, `bring`, `few`, `more`, `beautiful`, `speaker`) | **111.7°** | 514 | `9,568,024` bytes (`42.83s`) |
| `video_b` | `y8tFSuOMAqQ` | Conversational Vlogging | Yes (attempt 1) | Yes (`viewMode: "full"`) | `10` (`summer`, `here`, `time`, `start`, `movie`, `your`, `video`, `maybe`, `you`, `good`) | **74.6°** | 546 | `10,686,918` bytes |
| `video_c` | `xrwz9IxpMJg` | IIT/NPTEL Robotics (Indian-EN) | Yes (attempt 1) | Yes (`viewMode: "full"`) | `10` (`let`, `course`, `robot`, `first`, `topic`, `before`, `now`, `we`, `follow`, `what`) | **67.6°** | 658 | `9,316,000` bytes |

---

## 2. Independent Visual Inspection Findings & DPI Crop Calibration
- **Live 3D Avatar Confirmed Rendering on YouTube:** Direct inspection of `artifacts/h43/contact_sheets/video_{a,b,c}/h43_video_{a,b,c}_contact_sheet.png` confirms all 12 frames per video display the ad-free YouTube player alongside the live head-to-toe 3D Aether character inside `#isl-floating-avatar-surface` with dynamic HUD labels (`Signing: SPEECH (full)`, `Signing: HERE (full)`, `Signing: COURSE (full)`).
- **DPI Crop Calibration Catch:** Initial anatomical cropping used raw CSS coordinates (`x=702, y=162, w=320, h=382`) against physical PNG captures (`1583x713` at `devicePixelRatio=1.25`). Visual inspection via `read_file` caught the leftward offset immediately; multiplying live DOM bounding rects by `window.devicePixelRatio` centered `full_body_surface.png`, `hands_torso_zone.png`, and `face_head_zone.png` accurately across all 3 videos (confirmed via re-inspection).
- **Camera Framing Calibration (`embed.js`):** Smoke screenshot inspection caught an over-tight `PerspectiveCamera` FOV (`34°`), corrected to `45°` matching `tools/avatar_viewer/index.html` and `AvatarCameraView.mjs`.
