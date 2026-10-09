# H8 YouTube Extension Test Report

## Outcome

**H8 integration implementation: PASS in the local browser/runtime harness.**
The strict installed-extension-on-YouTube verification remains outstanding:
the integrated browser does not have this unpacked Chrome extension installed.
The popup UI, real backend API, service-worker message handler, content script,
and Aether iframe were therefore exercised at their real boundaries with a
Chrome messaging shim, and that distinction is not reported as an installed
extension session.

No ASR, translation, sign library, scheduler, Aether model, or sign motion was
replaced or fabricated.

## Video run

- URL entered: `https://youtu.be/y8tFSuOMAqQ`
- Video: `How to Vlog as a Beginner (without overthinking it)`
- Video ID: `y8tFSuOMAqQ`
- Audio duration: 721.835 s
- ASR: `base.en`, CUDA, float16
- Timestamped transcript segments: 256
- Resolved concept occurrences: 242
- Playable occurrences: 3 (`good`)
- Unavailable concept occurrences: 239
- Unknown-term occurrences: 2,442

The backend returned the cached H7 `pipeline_result.json`; no YouTube
redownload occurred. The separate H7 fresh decode benchmark remains 28.599 s
ASR time, 0.135 s translation time, and RTF 0.0396. The H8 API cache-hit time
is not presented as a fresh ASR benchmark.

## Verification evidence

| Requirement | Result |
|---|---|
| Extension manifest/resources and popup URL controls | PASS |
| URL validation, including malformed and non-YouTube URL rejection | PASS |
| `POST /youtube/process` returns HTTP 202 and unique job ID | PASS |
| Invalid API URL returns HTTP 400; unknown job returns HTTP 404 | PASS |
| Job status polling and READY result retrieval | PASS |
| Cached real transcript has 256 valid `start` / `end` / `text` segments | PASS |
| Existing G2/G3 translation result reaches popup and overlay | PASS |
| Playable/unavailable concepts explicitly separated | PASS |
| Backend/offline, malformed response, timeout and job-error handling | PASS (deterministic tests) |
| Service-worker `YOUTUBE_PROCESS` handler against live localhost API | PASS |
| Worker emitted `PLAY_SIGN good`, `QUEUE_SIGN good`, `QUEUE_SIGN good` | PASS |
| Content-script command relay to actual embedded Aether viewer | PASS (browser messaging shim) |
| Aether had 243 bones; scheduler observed current `good`, queued two `good` | PASS |
| Overlay lifecycle / duplicate mount / YouTube SPA guards | PASS |
| Installed Chrome extension popup on an actual YouTube tab | NOT RUN |

The popup page was opened in the local browser, the real video URL was entered,
and the actual popup JavaScript displayed its real cached API result. A
browser-side Chrome messaging shim supplied the extension API boundary because
the extension was not installed in that browser. Separately, the actual
service-worker script was run in a Node VM with Chrome tab/message stubs while
its RuntimeBridge called the real local `/youtube/*` endpoints. The actual
content script was loaded in the browser, received versioned Aether commands,
and forwarded them to the real embedded Aether viewer and SignScheduler.

## H8 deterministic checks

`node tools/validate_phase_h8_extension_youtube.mjs` passed:

1. Manifest and extension loading
2. YouTube URL validation
3. Asynchronous process/job creation contract
4. Status and result polling
5. Transcript payload shape
6. Translation payload shape
7. Playable-sign output
8. Unavailable-concept output
9. Invalid input, offline, malformed response, timeout, and job-error handling
10. Aether command types
11. Overlay lifecycle
12. Duplicate mount prevention
13. YouTube SPA resilience
14. Aether command relay contract

`node tools/validate_phase_h8_extension_youtube.mjs --runtime` passed against
the local server and cached real video. It additionally verified the worker
creates a separate job and emits three Aether commands for the three real
playable occurrences.

## H1–H7 regression

- H7 existing cached-video pipeline runner: **PASS** (cache hit; CUDA/float16,
  256 segments, 3 playable and 239 unavailable occurrences)
- H6 extension shell: **PASS**
- H5 evidence intake: **PASS**
- H4 authoring evidence gate: **PASS**
- H3 candidate evidence states: **PASS**
- H2 coverage/evidence gate: **PASS**
- H1 prioritization: **PASS**
- G3 translation validation: **PASS**
- G2 translation validation: **PASS**
- G1 speech-to-Aether pipeline validation: **PASS**
- Sign-library schema validation: **PASS** (13 entries; 13 visual assets
  remain missing, as expected by the existing evidence gate)
- `git diff --check`: **PASS**

Existing sign-motion definitions were not modified. This result establishes
the H8 local integration harness, not broad sign availability or complete
YouTube-to-ISL translation. Final confirmation in a Chrome session with the
unpacked extension installed and active on YouTube remains a manual release
check.
