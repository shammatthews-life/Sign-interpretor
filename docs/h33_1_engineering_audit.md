# H33.1 Independent Engineering Audit

## Executive status

**Engineering fixes and focused verification: PASS. Product release acceptance: BLOCKED.**

The H33 commit `cea02cdc0e44afaa8e8518233f8e2342aed3599f` contains the production CUDA changes, diagnostic, validators, reports, and evidence described by its commit. Its Git tree contains all 38 files in the commit summary; the claim that only two documentation files were committed is not supported by the repository.

H33.1 closes source-level defects in CUDA enforcement, model lifecycle/concurrency, streaming input validation, worker error visibility, transcript-cache provenance, duplicate YouTube jobs, and the local viewer's network boundary. A bounded production-service CUDA smoke test passed. This does **not** complete the 8,979-second canonical video, full-corpus accuracy, product TTFS, occurrence reconciliation, long-session reliability, or interactive Chrome acceptance.

## Changes and tests

| Area | Finding | Change and verification |
|---|---|---|
| CUDA enforcement | A direct `FasterWhisperBackend(execution_mode="GPU_REQUIRED", device="cpu")` could verify the GPU and still instantiate a CPU model. | The backend now resolves and enforces the requested mode/device/index before model creation. A failure-injection test confirms the CPU factory is never called. |
| Model duplication | Streaming and YouTube paths could independently construct GPU models; concurrent inference was not serialized. | Production paths share one model and inference lock per model/device/index/compute-type configuration. Concurrent fake-model tests confirm one construction and one shared lock. |
| Service lifecycle | Concurrent `start()` calls could race; repeated starts could start the backend again; reconfiguration could silently retain the old model; stop/restart could retain stale stream state. | Service starts are serialized and idempotent for identical configuration; incompatible reconfiguration fails explicitly; stop/reset clears stream state. Concurrent-start and restart tests pass. |
| Audio input | Base64 decoding accepted malformed input; byte length, timestamps, NaN/Inf, and sample amplitudes were not validated. | The service validates payload shape, strict base64, float32 alignment, a 2 MiB decoded limit, finite timestamps/samples, increasing non-negative timestamps, and normalized amplitude bounds. Rejected chunks do not affect accounting. |
| Worker failures | Inference failures were printed and converted to empty output; callback exceptions could escape the worker. | Backend status exposes `last_error`; callbacks run outside the backend lock; inference and callback failure injection confirms recovery and continued processing. |
| Cached results | Cached YouTube transcripts and full pipeline results could be returned without matching requested execution provenance. | Cache hits now require matching model/device/index/compute type/execution mode. A mismatched CPU cache cannot bypass a GPU-required run. |
| Concurrent YouTube requests | Repeated active requests for the same video could race while writing shared output paths. | Active same-video submissions reuse the existing job ID and worker; the regression test confirms one worker. Different videos remain concurrent; shared inference is serialized. |
| Local API boundary | The viewer listened on all interfaces and emitted wildcard CORS headers. Diagnostics writes had no body-size limit. | The viewer now binds to loopback, emits no wildcard CORS permissions, rejects non-local write origins, bounds diagnostics bodies, and permits sign definitions up to 1 MiB (existing tracked signs reach 322 KB). |

Focused regression command:

```powershell
python tools\validate_phase_f2_asr.py
```

Result: **16 PASS assertions** covering the defects and existing streaming behavior. Python compilation also passed for the five changed production modules.

The production smoke used the repository `.venv` and a one-second all-zero float32 chunk; it was a path/lifecycle smoke test, not a quality or throughput benchmark:

- `GPU_REQUIRED`, `base.en`, CUDA device 0, float16
- CTranslate2 4.8.2; Faster-Whisper 1.1.1; Python 3.12.10
- Finalization returned one event; `last_error` was null; stop left state `stopped`
- GPU was idle at 48 °C with 5,920 MiB free after the process exited

## Regression gates

| Gate | Result | Interpretation |
|---|---|---|
| H32 project validator | **PASS — 51/51** | Existing artifacts and corpus invariants validate. This is not a fresh full-video transcription. |
| H31 project validator | **PASS — 48/48** | Existing evidence validates; interactive Chrome acceptance remains unperformed. |
| H30 project validator | **PASS — exit 0** | The validator completed successfully. Its regenerated timing files were restored to their original committed values. |
| H33 evidence validator | **BLOCKED — 43 PASS, 0 FAIL, 8 BLOCKED, 2 MANUAL** | This is the intended honest outcome: GPU milestone evidence exists, but required end-to-end product acceptance is incomplete. |

The H32 and H30 validators regenerate machine-measured timing artifacts. Those incidental changes were restored; the pre-existing H32 worktree edits were not reverted or staged.

## Repository and publication-history audit

The initial H33 source audit confirmed `cea02cdc` against the fetched `origin/r1-articulation-coverage-and-report` base (`2608ba357c70e030d4ad9063d988fb09a22d150d`). After committing H33.1 as `692da3f28984f23fb8f2faac8c965388578b6836`, the complete unpublished range is 49 commits ahead of that base; the current origin has no `audit/h33-gpu-enforcement` ref.

- Rescanned all 49 unpublished commits: 1,930 unique Git objects and 1,640 text blobs. No matches were found for private-key headers, common GitHub/AWS/Google/Slack token formats, or long secret/password assignments.
- No `.env`, private-key, model-weight, audio/video, FBX, GLB/GLTF, OBJ/MTL, or Blender assets were found in that range.
- The tracked PNGs are 32×32 placeholders (104–105 bytes) plus small extension icons; they are not avatar models or textures.
- The history includes short ASR/test phrase fields and lexical/context datasets. No full transcript or media file was found by this inventory; the scan does not establish licensing for every corpus entry.
- The ten pre-existing H32 edits remain unstaged. H33.1 changes are confined to its ASR/runtime sources, focused validator, and this report/evidence.

This report/evidence metadata update is separate from the scanned commit range and must be scanned as staged content before its commit. The secret scan is a bounded pattern-based review, not a guarantee against every possible secret format. Push only to the dedicated audit branch and never force-push.

## Release blockers and manual work

The following are **not claimed as complete**:

- Full 8,979-second canonical ASR/video run and full-corpus WER/CER: **BLOCKED / NOT RUN**. The H32 300-second canonical slice and extrapolation are not full-run evidence.
- Product TTFS, occurrence-level transcript-to-sign accounting, and long-session fault/memory testing: **NOT RUN**.
- Installed Chrome/YouTube acceptance and hands-on sign playback: **MANUAL**.
- Native ISL linguistic review: **NOT RUN**; existing classifications remain implementation-pending-review.
- The extension manifest still includes `<all_urls>` content-script/resource matches. This is left unchanged to avoid narrowing the advertised general web-overlay behavior without product approval; verify that broad site access is intentional.

Low available RAM during the audit (about 2.17 GiB) was an additional reason not to start an unbounded full-video or long-session run.
