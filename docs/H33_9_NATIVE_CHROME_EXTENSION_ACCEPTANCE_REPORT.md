# H33.9 — Native Chrome Extension Acceptance Report

## Status

**Partially accepted.** Native Chrome installation, YouTube content-script execution, Aether rendering, floating-avatar controls, and sequential manual playback were verified. Cue-driven translation, video synchronization, and production ASR remain unverified or blocked.

## 1. Installation diagnosis

The current unpacked extension is registered and enabled by native Chrome; its ID was read from Chrome's extension registry, not assumed:

- Chrome: `Chrome/156.0.8078.76`
- Extension ID: `pdabldggmjpcildkjlpcfmgdemecpaha`
- Registry state: `ENABLED`
- Loaded source: `D:\sign interpretor\extension` (matches the project extension directory)
- Manifest version: 3
- Service worker registration: confirmed
- Service-worker target: observed after extension reload; it later went idle as expected for Manifest V3.
- Chrome-reported loading errors: none

The manifest diagnostic found valid JSON and structure, no invalid match patterns, no path traversal, and no missing referenced scripts, stylesheets, popup, icons, or web-accessible resource groups. The exact historical Chrome load error from the earlier unregistered session was not retained, so its original cause cannot be stated reliably.

The blank viewer after a YouTube refresh was traced to service-worker wake behavior, not a current manifest blocker. On a fresh Manifest V3 worker, `GET_STATE` previously returned the bridge's initial in-memory state without checking the local runtime. The content script consequently hid the viewer even when the local server was available. `GET_STATE` now performs a coalesced health probe, rate-limits repeated unavailable probes for five seconds, and returns its response asynchronously. The installation callback uses the same probe path.

## 2. Changes in this phase

- `extension/background/service-worker.js`
  - Probe the local runtime when `GET_STATE` wakes a worker with no known runtime connection.
  - Coalesce concurrent probes and limit repeated offline probes.
  - Share the health-check path with the installation callback and surface unexpected probe errors.
- `extension/background/service-worker.test.mjs`
  - Cover concurrent probe coalescing and repeated offline-probe rate limiting.
- `docs/H33_9_NATIVE_CHROME_EXTENSION_ACCEPTANCE_REPORT.md`
  - Record the native-browser evidence and remaining blockers.

Other H32/H33 worktree modifications were preserved. No commit was created.

## 3. Native Chrome and YouTube evidence

The project extension was reloaded using its actual control in `chrome://extensions`, and the existing YouTube watch tab was refreshed. The Chrome diagnostic then confirmed:

- Content script initialized in the extension's isolated world.
- Overlay mounted and visible.
- Viewer iframe loaded at `http://localhost:8000/tools/avatar_viewer/index.html?embed=1`.
- The YouTube video element was present, `readyState = 4`, and not paused.
- Chrome reported no extension loading errors or diagnostic inspection errors.
- During an 8-second native page reload observation, no console errors or uncaught exceptions were captured from the extension isolated world or Aether iframe.

The tested page was `https://www.youtube.com/watch?v=aqz-KE-bpKQ` (Big Buck Bunny). This is actual native Chrome extension execution, not an embedded preview or manually injected overlay.

The real close/reopen interaction was also exercised using browser input:

- Closing the panel left the avatar visible at its prior position.
- The edge handle reopened the panel and hid itself.
- Avatar/panel overlap was 0 px² at the tested viewport.
- The avatar stayed at approximately `(481, 222)` CSS px while the panel occupied the right edge.

At the tested ~1021 px viewport, the 220 px panel was about 21.5% of the width, slightly above the requested 15–20% range. This phase did not redesign the UI.

## 4. Aether runtime

The live iframe contained the actual viewer runtime:

- Three.js canvas present and rendering.
- WebGL context active (not lost); renderer reported 7,343 frames and 41,373 triangles.
- FBX model loaded with 10 meshes and 243 bones.
- `SignScheduler` and `SignLibrary` initialized.
- 550 sign definitions loaded; 0 failed.
- HELLO, GOOD, MORNING, and WATER all resolved to playable motion definitions.
- Viewer tab visibility was `visible` during playback.

## 5. Real extension-originated sequential playback

The sequence was triggered by clicking the real overlay controls in the YouTube tab. The commands passed through Chrome runtime messaging, the service worker, the content script, the Aether iframe, and the scheduler. No `page.addScriptTag`, manually constructed `postMessage`, or direct scheduler enqueue was used.

Two repetitions were observed. In the first, scheduler polling showed `HELLO → GOOD → MORNING → WATER → idle`, with no interruption or duplicate; the queue ended empty. The extension service worker's session ledger retained `accepted`, `playback_start`, and `playback_end` for every sign in both runs.

| Sign | Event ID (second run) | Accepted | Started (viewer ms) | Completed (viewer ms) | Duration |
|---|---|---|---:|---:|---:|
| HELLO | `isl-59645f70-5dd4-4bac-986b-6c5c80c005e1` | Yes | 373,412.0 | 375,408.4 | 1,996.4 ms |
| GOOD | `isl-edc2bdea-22ea-4901-8292-c6dd8a702499` | Yes | 375,408.9 | 377,113.0 | 1,704.1 ms |
| MORNING | `isl-82b64dde-ae7a-4c25-b56d-af7628b82b42` | Yes | 377,113.2 | 378,915.0 | 1,801.8 ms |
| WATER | `isl-9910586a-7f91-4e91-8d37-d98a06b44f24` | Yes | 378,915.4 | 380,417.9 | 1,502.5 ms |

During the first run, sampled involved-bone rotations moved from rest by maxima of 1.883 rad (HELLO), 1.326 rad (GOOD), 1.187 rad (MORNING), and 1.658 rad (WATER). These are measured component deltas from approximately 70 ms polling, not a linguistic or visual-quality assessment.

These were manual avatar-control commands: `jobId` and `cueId` were null. They prove extension-to-avatar sequential playback, **not** translated YouTube cue playback or synchronization to speech.

## 6. Backend, dependencies, and ASR

The local `/asr/status` POST returned HTTP 200, but the worker was `stopped`; it reported model `base.en`, `device=cuda`, `compute_type=float16`, and `execution_mode=GPU_REQUIRED`. No ASR model was started and no video audio was processed.

The read-only full-video resource preflight was run for 8,979 seconds:

- Available system RAM: **1.31 GiB**; required minimum: **6 GiB** — blocked.
- Free disk: **68.19 GiB**; required minimum: **10 GiB** — passed.
- Free CUDA memory: **5,920 MiB**; required minimum: **2,048 MiB** — passed.
- Result: `BLOCKED`; `full_video_run_permitted=false`.

The safety threshold was not bypassed. Cached `base.en` and `tiny.en` model directories exist, but neither was loaded. The project `.venv` contains `faster-whisper`, `ctranslate2`, PyAV, and `yt-dlp`; the project's FFmpeg resolver found the bundled `imageio-ffmpeg` executable. The listener observed on port 8000 runs under the system Python, where `faster-whisper` and `yt-dlp` were not importable. ASR startup was deliberately not attempted because the memory gate failed; the listener's ASR-start behavior under that interpreter therefore remains unverified.

As a bounded diagnostic, `tools/validate_phase_f2_asr.py` passed its synthetic streaming, chunk validation, failure-recovery, and resource-preflight checks using a fake model; it does not download/load a model or claim real transcription. Full-video ASR remains blocked.

## 7. Tests

- `node --test`: **133 passed, 0 failed**.
- `node --test extension\background\service-worker.test.mjs`: **7 passed, 0 failed**.
- `node --test tools\diagnostics\chrome_extension_diagnostic.test.mjs`: **5 passed, 0 failed**.
- `python tools\validate_phase_f2_asr.py` (project `.venv`): passed; the injected worker errors printed by failure-recovery tests were expected test cases.
- `node --check` on the changed service-worker files: passed.
- `git diff --check` on the changed service-worker files: passed.
- Native Chrome extension diagnostic: installed, enabled, manifest-valid, service worker registered, YouTube content script executed, viewer iframe loaded, backend status reachable.
- Resource preflight: intentionally returned `BLOCKED` (exit code 2) because available RAM was below the required minimum.

## 8. Synchronization and remaining blockers

- No cue start/end timestamps were involved in the manual sign sequence; YouTube-to-avatar timing error in milliseconds was **not measured**.
- Full YouTube speech processing and translated cue delivery were not verified.
- Pause/resume, seeking, speed changes, SPA video switching, and multi-tab isolation were not re-tested in this native-browser run. Existing automated tests do not substitute for those manual acceptance checks.
- WATER is technically playable, but its linguistic validation remains pending. The motion asset is not evidence that WATER is a correct ISL translation.
- Full-video ASR remains blocked by insufficient available RAM. Do not report it as successful.
- The ASR startup path under the currently listening system-Python process remains unverified; use the project environment and satisfy the preflight before attempting ASR.

## 9. Follow-up: half-body framing, transparency, and GPU

The viewer now applies the half-body camera preset when it starts in embedded mode. In native Chrome on YouTube, the loaded FBX contained 10 meshes and 278 bones; the WebGL canvas was 400 × 650 device pixels, requested an alpha context, and reported `getClearAlpha() = 0`. Sampled empty canvas pixels were `[0, 0, 0, 0]`; the embedded page and body backgrounds were transparent, and the floor grid was hidden.

After launching the isolated Chrome test profile with the unpacked extension from `D:\sign interpretor\extension` and opening the YouTube watch page, the live floating viewport's computed background image and shadow were `none`, its border was absent, and a native Chrome screenshot visibly showed the YouTube page behind the avatar. The head and torso were in frame using the half-body preset.

The HELLO control was clicked through native Chrome input on the real extension UI. At 480 ms, playback was active and tracked arm-bone quaternion components had changed (right upper arm: 0.465; forearm: 0.444; hand: 0.151). The sign then completed; the scheduler was idle with an empty queue and no active cue. This validates one manual sign animation, not translation or cue synchronization.

Windows has `GpuPreference=2;` set for `C:\Program Files\Google\Chrome\Application\chrome.exe`. After restarting the isolated native Chrome test profile, the actual YouTube Aether iframe reported `ANGLE (NVIDIA, NVIDIA GeForce RTX 4050 Laptop GPU..., Direct3D11)`. The user's separate primary Chrome profile was left open.

Focused camera and service-worker tests after the framing change: **10 passed, 0 failed**. The isolated test Chrome was restarted; the primary Chrome profile was not.

## 10. Repository state and next milestone

- Branch: `audit/h33-5-end-to-end-playback`
- Repository HEAD: `56925e65ef50e504aebfb05274260516777ddb24`
- No commit was created. Existing H32/H33 changes remain in the worktree.

Recommended next milestone: **H33.10 — Cue-Driven YouTube Playback and Safe ASR Runtime Activation**. First run the viewer/backend with the project `.venv`, satisfy the 6 GiB preflight, then verify actual cue IDs, YouTube timing error, pause/resume, seek, playback-rate changes, and multi-tab isolation. Keep WATER marked linguistically pending until reviewed.
