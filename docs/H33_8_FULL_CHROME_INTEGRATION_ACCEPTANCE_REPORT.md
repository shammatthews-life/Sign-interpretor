# H33.8 - Full Chrome Integration Acceptance Report

## Status

**Partially verified; production acceptance is blocked.** The compact overlay and the embedded Aether viewer were exercised locally. The project extension was not registered in Chrome, so no real YouTube-to-extension-to-backend acceptance is claimed.

## 1. Implemented changes

- Made the expanded Details panel a bounded, scrollable region so its long diagnostic content cannot push the avatar controls outside the viewport.
- Reduced the Details panel allowance on short displays and the avatar placeholder height when detached, keeping Half/Full, Move, and Dock controls visible.
- Hid the redundant detached note on short displays.
- Kept a single Aether iframe while docking, floating, collapsing, and reopening the sidebar.
- Added a regression test that verifies the detached-state class is applied and removed with the floating state.

## 2. Files changed for this phase

- `extension/content/overlay.css`
- `extension/content/overlay.js`
- `extension/content/overlay.test.mjs`
- `docs/H33_8_FULL_CHROME_INTEGRATION_ACCEPTANCE_REPORT.md`

The worktree already contained unrelated H32/H33 edits before this phase. They were preserved. No commit was created.

## 3. Automated tests

Ran the focused Node test suite covering the overlay, service worker, playback protocol, cue manifest, timeline synchronizer, sign scheduler, speech orchestrator, pending viewer queue, rig correction, live speech session, and avatar camera:

- **57 passed, 0 failed**
- `node --check extension/content/overlay.js`: passed
- `git diff --check` on the two edited overlay source files: passed

The scheduler test intentionally logs a simulated player-load error while verifying that playback advances; the test passed.

## 4. Compact UI and avatar preview results

These are measurements from a local browser preview, not from an installed extension or a YouTube page.

| Viewport | Panel width | Viewport share | Main controls visible | Collapse/reopen |
|---|---:|---:|---|---|
| 1920 x 1080 | 280 px | 14.6% | Pass | Pass |
| 1366 x 768 | 220 px | 16.1% | Pass | Pass |
| 1280 x 720 | 220 px | 17.2% | Pass | Pass |
| 390 x 844 | 220 px | 56.4% | Pass | Pass |

Subpixel layout rounding was under 1 CSS pixel at the right edge. The narrow viewport necessarily exceeds the requested 15-20% share because the panel keeps a 220 px minimum for its controls.

At 876 x 500, the previously clipped Dock control and the Half/Full/Move controls were within the viewport both docked and floating. The floating avatar remained within the viewport. The details content scrolls independently.

At 1280 x 720, pointer interactions verified Half/Full camera framing, drag and viewport clamping, collapse/reopen while floating, click-through to an underlying page button with drag mode off, and docking. The iframe element and loaded Aether rig remained the same throughout.

## 5. Embedded viewer playback evidence

The preview used valid, uniquely identified `ISL_AETHER_COMMAND` messages from the expected local parent window and origin to the embedded viewer. They passed the viewer's message gate and exercised acknowledgement handling, the scheduler, and real Aether animation, but bypassed Chrome's content script and service worker. Incorrect-origin and incorrect-window rejection were not browser-tested in this phase.

| Sign | Accepted | Playback start (viewer ms) | Declared duration | Playback end (viewer ms) | Measured duration |
|---|---|---:|---:|---:|---:|
| HELLO | Yes | 1,382,922 | 2,000 ms | 1,384,924 | 2,002 ms |
| GOOD | Yes | 1,382,924 | 1,700 ms | 1,384,629 | 1,705 ms |
| MORNING | Yes | 1,384,629 | 1,800 ms | 1,386,431 | 1,802 ms |
| WATER | Yes | 1,386,431 | 1,500 ms | 1,387,933 | 1,502 ms |
| THANK YOU | No | - | - | - | Rejected: `NOT_PRELOADED` |

The four available signs completed once and in order. Each next sign started at the prior sign's completion timestamp (or within 1 ms); the scheduler ended idle with an empty queue. The viewer returned `accepted` acknowledgements for the four playable signs and a `rejected` acknowledgement for THANK YOU. The rejected sign did not block the queue.

HELLO's right-upper-arm quaternion changed during playback, confirming actual model motion rather than message acceptance alone. Replaying a completed event ID returned an acknowledgement without adding lifecycle events; reusing that ID for a different sign was rejected as `EVENT_ID_CONFLICT`.

These timings are measured inside the viewer using its performance clock. They are **not** YouTube synchronization error measurements. `signs/water.json` is playable but its linguistic validation status is `IMPLEMENTATION_PENDING_LINGUISTIC_REVIEW`; its motion should not be treated as linguistically accepted.

## 6. Video synchronization

No YouTube current-time, cue-boundary, or real playback timing error was measured. Automated timeline tests passed for pause/resume, seeking, playback rate, and repeated occurrences, but those tests do not establish synchronization on a real video.

## 7. Actual Chrome and YouTube integration

**Blocked / not verified.**

- An isolated native Chrome 156.0.8078.76 session was opened at `chrome://extensions` with Developer Mode enabled.
- Load unpacked was attempted for `D:\sign interpretor\extension`, but the project did not appear in the extension list. No project service worker or content-script injection was observed.
- The extension ID seen in that session, `fignfifoniblkonapihmkfakmlgkbkcf`, belongs to Google's Network Speech component and is not the project extension ID.
- The local viewer server was started with that non-project ID. It must not be used as evidence of project-origin authorization.
- No actual YouTube watch page was tested for video playback, translation, pause/resume, seeking, playback speed, or multi-tab isolation.

**Required user action to unblock:** In native Chrome, open `chrome://extensions`, enable Developer Mode, choose **Load unpacked**, and select the `D:\sign interpretor\extension` folder itself (the folder containing `manifest.json`). Once Chrome displays the project extension card, provide its generated extension ID and any load error shown. Restart the local viewer with that project ID before attempting the YouTube workflow.

## 8. RAM and ASR status

The local `/asr/status` endpoint reported `stopped`, model `base.en`, device `cuda`, `float16`, `GPU_REQUIRED`, and zero audio received. No full-video ASR was run. The previously measured available RAM was 2.572 GiB against a 6 GiB preflight minimum; the safety check was not bypassed.

## 9. Known limitations and blockers

- Actual Chrome extension registration and the complete YouTube workflow remain unverified.
- Full-video ASR and real-video cue synchronization remain unverified.
- `THANK YOU` has no preloaded sign asset and is rejected as unavailable. A reviewed asset or explicit unavailable-sign presentation is still required for that word.
- WATER has a playable asset, but its linguistic review is pending.
- The preview harness does not execute the project's real Chrome content-script/service-worker chain. Its successful viewer messages are not Chrome integration evidence.
- The user-visible unavailable-sign fallback was not visually verified on YouTube.

## 10. Repository state and next step

- Branch: `audit/h33-5-end-to-end-playback`
- HEAD before this phase's changes: `56925e65ef50e504aebfb05274260516777ddb24`
- No commit was created; the worktree contains pre-existing H32/H33 changes.

Next, load the unpacked extension in Chrome, provide its generated ID, and rerun the acceptance workflow on a real YouTube watch page with the local backend available. Do not mark H33.8 production-accepted until that test and the resource-constrained ASR path have evidence.
