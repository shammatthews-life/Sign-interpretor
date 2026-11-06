# Avatar Interaction and Playback QA Report

## Scope and disposition

This report covers the movable avatar, overlay close/reopen behavior, YouTube
click-through, and the extension-to-Aether playback path. It does not claim
acceptance of the full translation-to-animation pipeline.

The worktree was on `audit/h33-5-end-to-end-playback`. No commit was created.
Pre-existing H32/H33 changes were left intact.

## Changes under test

- Removed extension code that changed YouTube's `#primary` margin and root
  attributes when the sidebar was shown or hidden.
- Kept avatar dragging bounded by the viewport rather than by the sidebar.
- Updated overlay regression coverage for viewport dragging, pointer identity,
  panel reopening, and unchanged host-page layout.
- Retained click-through behavior: the floating surface and iframe do not
  consume pointer events; only the enabled drag grip does.

## Three review passes

### Pass 1 - Code and focused regression review

- Found host-page reflow coupled to sidebar visibility and drag bounds that
  prevented placing the avatar over the sidebar.
- Removed the host-page mutation and allowed a dragged avatar anywhere within
  the viewport.
- Focused overlay tests: **8 passed, 0 failed**.
- JavaScript syntax checks and `git diff --check` passed. Git emitted only its
  existing LF-to-CRLF working-copy warning.

### Pass 2 - Native Chrome interaction review

The unpacked extension was reloaded through Chrome's extension manager so the
test used the edited extension source, not an injected overlay.

- Chrome: `156.0.8078.76`.
- Extension ID: `pdabldggmjpcildkjlpcfmgdemecpaha`.
- Extension directory: `D:\sign interpretor\extension`.
- The real YouTube tab contained the extension host, open Shadow DOM, and
  visible avatar iframe.
- Close hid the panel and exposed its reopen handle; clicking the handle
  restored the panel while leaving the avatar visible.
- With Move avatar enabled, a native pointer drag moved the avatar from
  approximately `(946, 230)` to `(360, 248)` in a `1536 x 776` CSS-pixel
  viewport.
- The YouTube primary container's inline margin stayed empty, and
  `data-isl-sidebar-active` stayed absent.
- Clicking the YouTube video at `(520, 500)`, underneath the floating avatar,
  paused and resumed playback. Hit testing identified the underlying video.

### Pass 3 - Playback and full regression review

- The embedded viewer ran in the actual extension iframe at
  `http://localhost:8000/tools/avatar_viewer/index.html?embed=1`.
- The viewer exposed one WebGL canvas, 243 bones, and 550 loaded sign-library
  entries. Its context used alpha transparency and `clearAlpha` was `0`.
- Chrome reported `ANGLE (NVIDIA, NVIDIA GeForce RTX 4050 Laptop GPU ...)` as
  the WebGL renderer. The source requests `high-performance`; the reported
  context attributes nevertheless included `powerPreference: low-power`, so
  no Chrome-rendering performance improvement is claimed.
- Separately, a short offline ASR smoke test exercised the project's actual
  `FasterWhisperBackend` in `GPU_REQUIRED` mode with `tiny.en` and `float16`.
  The input was 5.38 seconds of locally synthesized speech, not video audio.
  The model loaded in 0.87 s and inference took 0.63 s. `nvidia-smi` reported
  177 MiB VRAM after load and 227 MiB with 24% GPU utilization after inference.
  This proves CUDA execution for a small diagnostic; it is not a full-video
  benchmark or a performance comparison against CPU.
- A HELLO command clicked in the extension UI produced live Aether playback.
  The maximum observed rotation delta was `0.8851` radians across the right
  clavicle, upper arm, forearm, and hand. Playback returned to idle.
- A second native extension-UI run queued HELLO, GOOD, MORNING, and WATER.
  Each occurrence produced `accepted`, `playback_start`, and `playback_end`
  lifecycle events in order. The final scheduler was idle with an empty queue.
- The complete Node test suite passed **75/75** on each of three runs.

## Native playback event log

Times below are the Aether lifecycle event timestamps (`atMs`), not YouTube
cue synchronization measurements.

| Sign | Event ID | Start (ms) | Completion (ms) | Elapsed (ms) |
|---|---|---:|---:|---:|
| HELLO | `isl-1489773f-0f08-461d-8bfb-d7cad1be9019` | 481827.8 | 483823.1 | 1995.3 |
| GOOD | `isl-556782ba-a88c-480f-9419-628e4db288da` | 483823.3 | 485529.7 | 1706.4 |
| MORNING | `isl-86a747a0-b57a-44d4-9ba2-a1926c107cf2` | 485530.2 | 487332.3 | 1802.1 |
| WATER | `isl-26da715b-b0ee-4482-a115-fe799c7bcab3` | 487332.6 | 488835.6 | 1503.0 |

Each listed event also had an `accepted` lifecycle event before playback. The
final viewer state was `active: null`, `queue: []`, and `playing: false`.

## Test results

| Test | Result |
|---|---:|
| `extension/content/overlay.test.mjs` | 8 passed, 0 failed |
| Extension, avatar-viewer, and diagnostic Node tests | 75 passed, 0 failed x 3 |
| `node --check` for overlay implementation and tests | Passed |
| `git diff --check` for relevant overlay files | Passed; line-ending warning only |
| Native Chrome panel close/reopen | Passed |
| Native Chrome avatar drag and YouTube click-through | Passed |
| Native Chrome HELLO playback and bone transform observation | Passed |
| Native Chrome HELLO/GOOD/MORNING/WATER completion order | Passed |
| Automated unavailable-sign and unsupported-word handling | Passed |
| Project streaming ASR on synthetic speech, RTX 4050 CUDA float16 | Passed |

## Blockers and limitations

- The selected YouTube page is a copyrighted 3.5-hour television compilation.
  No captions or transcript text were downloaded or reproduced, and no
  word-by-word inventory or new signs were generated from it.
- The page reached `readyState: 4` and exposed a duration of `12391.061` seconds.
  It was left paused at approximately `227.3` seconds. No audio extraction,
  ASR, backend translation, or full-video processing was run.
- At the final resource check, available RAM was about 2.97 GiB, still below the
  previously established 6 GiB full-video preflight floor. The short cached
  `tiny.en` GPU diagnostic does not override that safety limit; no full-video
  job was started.
- WATER's technical motion played, but its linguistic validation remains
  pending. Playback is not proof of ISL accuracy.
- Native bone-transform measurements were captured for HELLO only. The other
  three signs completed through the real extension queue, but their individual
  bone deltas were not measured. A later measurement attempt occurred after
  Chrome hid the tab; its animation frame did not advance, and the test queue
  was cleared through the extension's Reset control (programmatically
  activating the actual button, without sending a direct Aether message).
- The native sequence used the four sign shortcuts available in the extension
  UI. `THANK YOU` was covered by the automated scheduler test, not by the
  native Chrome sequence.
- No screen recording was captured. The motion evidence is from live bone
  rotations and lifecycle events.
- Full video translation coverage, missing-word fallback on that video,
  backend health, ASR resource recovery, and linguistic review remain
  unverified.

## Files changed for this task

- `extension/content/overlay.js`
- `extension/content/overlay.css`
- `extension/content/overlay.test.mjs`
- `docs/avatar_interaction_qa_report.md`
- `docs/avatar_interaction_user_review.md`
