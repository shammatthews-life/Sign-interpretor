# H33.3 YouTube Timeline and Vocabulary Coverage

## Result

YouTube signing now uses a validated, timestamp-preserving cue manifest. The extension requests cues only for the matching video and job, activates signs against the video's half-open time intervals, and acknowledges the manifest fingerprint. Seek, pause/resume, playback-rate changes, video replacement, and repeated sign occurrences are handled by the timeline synchronizer. Stale jobs are rejected.

Each cue retains its source transcript. Unsupported words and unavailable sign concepts are shown as **"Sign not available"** with the original segment text; a source/translation mismatch is withheld rather than presented as a valid translation. The overlay reports occurrence counts and does not claim complete ISL coverage.

## Canonical video audit

The cached result for `MXKkXXYUxBc` was audited without rerunning its 8,979-second ASR workload:

| Measure | Result |
|---|---:|
| Transcript / translation segments | 2,366 / 2,366 |
| Aligned segments | 2,365 |
| Source-text mismatches | 1 |
| Playable sign occurrences | 63 |
| Unavailable-sign occurrences | 1,880 |
| Unknown-term occurrences | 19,044 |
| Distinct unknown terms | 2,264 |
| Distinct unavailable concepts | 10 |
| Mismatch fallback words | 5 |
| Total fallback occurrences | 20,929 |

Segment 1274 (5,037.8-5,041.16 seconds) differs by encoding: the transcript contains `Hans Rüsling.` and the translation source contains `Hans RÃ¼sling.`. The segment is preserved as original-text fallback; its glosses and signs are not played.

**Coverage is incomplete.** Most vocabulary occurrences in this cached video do not have playable signs or resolved translation terms. The fallback communicates those gaps instead of inventing or implying a sign.

## Verification

- Worker delivery, cue-manifest, timeline, and live-ASR Node tests: 21 passed.
- Avatar movement check used the project's playable `hello` sign and the real Three.js avatar rig in the viewer: 4 of 10 involved bones moved at 850 ms; maximum measured rotation delta was 1.9174 radians. At the sign's 2,000 ms neutral endpoint, maximum deviation from the captured rest pose was `9.72e-17` radians.
- The embedded avatar command bridge applied a 1.5x playback-rate update.
- The avatar check verifies animation-engine movement and neutral reset; it is not Chrome-extension visual acceptance or linguistic validation.
- Focused ASR lifecycle race checks passed for audio arriving as the backend transitions to paused or stopped.
- `tools/validate_phase_f2_asr.py` reached its YouTube execution checks but could not complete because the environment lacks `ctranslate2` and compatible CUDA dependencies. No full-video ASR was started.
