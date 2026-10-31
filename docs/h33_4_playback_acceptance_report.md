# H33.4 Playback, Translation Accounting, and Acceptance

## Result

The playback path now keeps ordinary video cue transitions separate from explicit playback cancellation. Each sign occurrence has a stable event identity; Aether bounds queued work, validates sign availability, reports acceptance/rejection, and emits accepted/start/end/cancelled lifecycle events. The content script retries the same event identity until an acknowledgement arrives, bounds pending and in-flight work, and reports delivery failures instead of treating `postMessage` as proof of playback. Expired cue backlog is discarded while the sign already moving and independent manual playback are preserved.

The iframe accepts commands only from its parent window and an allowed YouTube or loopback origin. Timeline synchronization evaluates cues on install, uses video-frame callbacks when supported with `timeupdate` fallback, follows replacement video elements, and handles seek, buffering, playback, end, rate, and pause events.

## Source-word dispositions

The canonical cached result contains 2,366 transcript and translation segments. [h33_4_word_accounting.json](../data/h33_4_word_accounting.json) records every source token occurrence exactly once, with its source segment, character offsets, exclusive disposition, and supporting translation/trace evidence. Its independent validator reproduces the source tokenizer and all disposition totals.

| Disposition | Occurrences |
|---|---:|
| Playable sign | 58 |
| Sign unavailable in the playable library | 1,883 |
| Unknown to the local translation catalog | 18,957 |
| Omitted under an explicit project heuristic trace | 2,261 |
| Phrase represented / fingerspelled | 0 |
| Source mismatch shown as transcript fallback | 5 |
| Missing translation | 0 |
| Ambiguous; requires review | 49 |
| **Total source-token occurrences** | **23,213** |

This is not a claim that the vocabulary was exhaustively researched on the internet or that all translations are linguistically valid. The local translation result contains substantial unknown vocabulary; the product must keep showing unavailable-word messages and the original transcript rather than inventing signs. The 49 ambiguous tokens and 88 unmatched translation claims remain explicit review items. The one encoding/source mismatch remains a transcript fallback.

Historical totals are not silently forced to match: H27's extractor and inventory reproduce 23,256 under its ASCII word-boundary expression; H22 records 23,258 and its ASCII-fragment tokenizer reproduces that number. The new Unicode-token inventory is 23,213: it preserves internal hyphens as part of a word (44 occurrences) and the non-ASCII proper-name token as one token rather than ASCII fragments. Both cached transcript inputs were independently checked against each other. The ledger records source hashes and each historical count.

## Verification

- Node regression tests for cue construction, timeline synchronization, queue capacity, acknowledgement identities, cancellation, and cue-aware backlog: **16 passed**.
- Per-token accounting validator: **PASS**, 23,213 unique occurrence IDs and 23,213 exclusive dispositions.
- Real `hello` sign asset through the animation engine: **PASS**; measured bone rotation was 2.1293 radians and neutral reset error was 0 radians.
- Embedded browser viewer smoke test: **PASS**; a WebGL canvas rendered, accepted consecutive sign occurrences, rejected an unavailable sign with `NOT_PRELOADED`, ignored a mismatched parent origin, and emitted ordered playback lifecycle events. Evidence: [h33_4_browser_acceptance.json](../data/h33_4_browser_acceptance.json).
- Supplemental cross-origin iframe check: trusted-parent lifecycle messages were delivered across `127.0.0.1` and `localhost`; a command retried during library startup and was later accepted with `playback_start`, an expired queued cue was cancelled without a start event, and an unavailable sign was rejected. Playback completion of the later active cue was not captured in this supplemental check; consecutive playback is covered by the separate embedded-viewer smoke test.
- The existing H33 CUDA diagnostic records a fresh five-second Faster-Whisper `base.en` FP16 inference on the RTX 4050 with active `nvidia-smi` telemetry. This is short-sample GPU evidence, not a full-video run.
- Full-video ASR remains **BLOCKED** by the refreshed preflight: 2.572 GiB free system memory against a 6 GiB minimum. The full video was not run.
- Interactive Chrome acceptance of the unpacked extension on YouTube remains **MANUAL ACCEPTANCE REQUIRED**. The embedded viewer smoke test is not a substitute for testing the installed extension.
- Linguistic validation by an ISL reviewer was not performed.

## Reproducible checks

```powershell
node --test tools/avatar_viewer/SignScheduler.test.mjs extension/shared/youtube-cue-manifest.test.mjs extension/content/timeline-synchronizer.test.mjs
node tools/validate_h33_4_avatar_motion.mjs
.\.venv\Scripts\python.exe tools\build_h33_4_word_accounting.py
.\.venv\Scripts\python.exe tools\validate_h33_4_word_accounting.py
.\.venv\Scripts\python.exe tools\validate_h33_4_job_recovery.py
```
