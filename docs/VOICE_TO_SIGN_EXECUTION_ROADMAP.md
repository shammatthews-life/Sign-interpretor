# Voice-to-Sign Execution Roadmap

**Deadline:** November 20, 2026 (IST)

**Tracker started:** October 10, 2026 (IST)

**Current milestone:** Phase 1 — R1 Stabilization (October 11–12)

## Milestone status

| Milestone | Planned dates (IST) | Status | Acceptance summary |
|---|---|---|---|
| Phase 1 — R1 Stabilization | Oct 11–12 | REVIEW REQUIRED | Helper correction and automated/runtime checks pass. Complete manual visual review of individual wrist/finger-axis changes before R1 can pass. |
| Phase 2 — Voice to Text | Oct 13–17 | IN PROGRESS — YouTube URL workflow verified through cached runtime result; fresh URL processing and current playback review outstanding | The primary product route is submitted YouTube URL → audio → batch ASR → sign resolution → Aether. Microphone streaming is a separate optional route, not the primary acceptance path. |
| Phase 3 — Text to Sign Pipeline | Oct 18–24 | NOT STARTED | Transcript tokens resolve to an ordered animation queue; unsupported tokens remain visible. |
| Phase 4 — Vocabulary Coverage | Oct 25–31 | NOT STARTED | Coverage has a defined denominator, provenance, validation, and disclosed limitations. |
| Phase 5 — Extension Options and UX | Nov 1–7 | NOT STARTED | Main flow and playback controls operate reliably through the extension. |
| Phase 6 — Integration and Evaluation | Nov 8–14 | NOT STARTED | Fixed end-to-end test set has measured results and recorded failures. |
| Phase 7 — Release Freeze and Demo | Nov 15–20 | NOT STARTED | Reproducible setup, honest documentation, and demonstration are ready by Nov 20. |

## Phase 1 task register

### R1-NAN-01 — Guard and correct imported helper rotations

- **Planned:** October 11–12, 2026
- **Actual:** October 10, 2026
- **Status:** PASS (this task only)
- **Acceptance criteria:**
  - Inspect the loaded candidates and correct only named orphan helper bones after all safety checks pass.
  - Run the correction after loading/rig resolution but before any imported rest-pose snapshot.
  - Preserve position and scale; verify finite resulting transforms.
  - Do not change skinned skeleton references or articulated hand hierarchy.
  - Unit-test eligible, ineligible, missing, and unrelated nodes.
  - Run focused and R1 regression checks.
- **Implementation:** `tools/avatar_viewer/NonFiniteHelperBoneCorrection.mjs` is a strict two-name allowlist for `PRIVATE_Grenade_Point` and `PRIVATE_Grenade_Point_Low`. Runtime checks require a bone, effectively zero X scale, non-finite imported Euler/quaternion rotation, no children, no loaded skinned-mesh skeleton reference, and no ancestry relationship to protected wrist/hand/finger bones. Only the Euler rotation is reset to identity. The viewer runs this before `userData.initialRotation` and `userData.initialPosition` capture, logs issues, exposes its result, and shows PASS or REVIEW REQUIRED in the R1 status.
- **Loaded-model evidence:** Both named FBX nodes were bones, had X scale `0`, non-finite Euler/quaternion and local/world matrices, no children, no skeleton references, and were not ancestors of the resolved articulated bones. Both positions and all scale components remained unchanged. After correction, both rotations were `[0,0,0]`, both quaternions were `[0,0,0,1]`, matrices were finite, and their captured rest rotations were finite. Runtime result: `status: PASS`, both preservation flags true for both nodes, skeleton references preserved, protected hierarchy preserved.
- **Verification:**
  - `node --test tools\avatar_viewer\NonFiniteHelperBoneCorrection.test.mjs` — PASS, 5/5 tests.
  - `node tools\validate_phase_r1_articulation.mjs` — PASS, source guardrails include correction allowlist/safety/order.
  - `window.AetherRig.articulationTest.runAutomatedSuite()` — 98/98 axis checks, 10/10 poses, 4/4 replay speeds, curl precedence PASS, HAC 32/32, zero non-finite rest components, zero replay reset drift.
  - `git diff --check` — PASS.
- **Visual evidence:** A fresh browser run visually inspected separate neutral right- and left-hand focus views. A right open-palm technical pose with wrist/finger-joint position markers was also inspected. Focus actions caused no bone-quaternion changes. Screenshots were inspected in the live browser and were not added to the repository.
- **Files changed for this task:** `tools/avatar_viewer/index.html`, `tools/avatar_viewer/NonFiniteHelperBoneCorrection.mjs`, `tools/avatar_viewer/NonFiniteHelperBoneCorrection.test.mjs`, `tools/validate_phase_r1_articulation.mjs`.

### R1-VIS-02 — Finish individual-axis visual review

- **Planned:** October 11, 2026; complete by October 12, 2026
- **Status:** REVIEW REQUIRED
- **Acceptance criteria:** In the loaded viewer, visually inspect and record right/left wrist and representative finger X/Y/Z isolated-joint changes plus combined technical poses. Ensure each hand remains fully framed and the animation is reset afterward. Do not modify sign data or claim anatomical correctness based on numeric-only results.
- **Actual review:** On October 10, 2026, used the existing isolated-joint selector and hand-camera controls to inspect wrist X/Y/Z and index-base X/Y/Z on both hands. No sign animation or persistent bone pose was changed. The isolated controls reported the selected axis at +30 degrees (0.52360-radian world-orientation change); this is diagnostic and not treated as visual proof. Wrist X/Y/Z rotations on both hands visibly changed hand/wrist orientation. Left wrist Y initially had body occlusion; a runtime-only camera reposition made the hand more visible. Right wrist Z brought the hand close to the torso. Individual left and right index-base X/Y/Z movements were exercised, but the small changes to rendered finger shape/orientation were subtle and could not be distinguished consistently from overlapping fingers, glove/cuff geometry, and proximity to the torso. Therefore, the visual criterion for each isolated finger axis is not established.
- **Reset/evidence:** Reset the articulation controller to its captured rest pose after inspection; the viewer reported time 0 and zero non-finite rest components. Screenshots were visually inspected in the live browser but were not saved to the repository. Neutral bilateral focus and a right open-palm technical pose were inspected previously; these do not replace the unclear isolated finger-axis evidence.
- **Remaining gap:** The 98/98 automated axis checks verify numeric local/world rotation changes, but do not substitute for clear visual confirmation. The existing R1 report also records that individual left-hand axis views were not conclusively confirmed. This time-boxed visual attempt did not resolve that gap. R1 remains REVIEW REQUIRED.
- **Owner decision (October 10, 2026):** Approved proceeding with Phase 2 under the bounded fallback: retain R1 as REVIEW REQUIRED, explicitly disclose the isolated finger-axis visual limitation, and defer any claim of complete per-axis visual verification. This does not waive R1 acceptance criteria or declare R1 passed.
- **Next action:** Begin Phase 2 on its planned dates (October 13–17). Keep the R1 finger-axis visual follow-up open; no speech-recognition implementation was started as part of R1-VIS-02.

## Phase 2 task register

### PH2-STT-01 — Audit and establish the input path

- **Planned:** October 13–17, 2026
- **Actual:** October 10, 2026
- **Status:** PASS (audit and integration plan only; no STT implementation change)
- **Existing live microphone route:** The standalone viewer's `MicrophoneSource` requests browser microphone access with `getUserMedia`. `StreamingAudioPipeline` downmixes/resamples to mono 16 kHz `Float32Array`, frames 100 ms chunks, runs the existing energy VAD, and posts accepted samples as base64 little-endian float32 to local `POST /asr/chunk`. The local `LocalASRService` forwards them to the existing faster-whisper streaming backend. `POST /asr/start` initializes that backend; the viewer displays partial/final transcript text in its G1 panel and forwards transcript events into `SpeechSignOrchestrator`, `SignScheduler`, and the avatar. The pinned dependency is `faster-whisper==1.1.1`; the default live model is `tiny.en`, with automatic local CUDA or CPU selection. The live route uses localhost, so it requires no paid API or API key; first-time model availability may require a model download.
- **Existing extension YouTube route:** The popup requires the user to enter a YouTube URL and sends `YOUTUBE_PROCESS` through the service worker and `RuntimeBridge` to local `POST /youtube/process`. The Python job downloads/extracts the URL's audio with yt-dlp and FFmpeg, converts it to mono 16 kHz PCM WAV, transcribes locally with faster-whisper (default `base.en`), and returns timestamped transcript results. The extension popup and page overlay display the transcript; playable signs are relayed to the active tab. This is URL-based batch processing, not capture of audio currently playing in the tab. The manifest has `activeTab` and YouTube host permissions but no `tabCapture` permission; code inspection found no tab audio capture. The active tab ID is used to route playback commands.
- **Integration plan (updated October 21, 2026):** The product's primary workflow is a user-submitted YouTube URL through the existing popup → `YOUTUBE_PROCESS` → local `/youtube/process` job → audio extraction → faster-whisper batch transcription → existing G2/G3 translator → playable-sign filtering → Aether scheduler. Prioritize this route for Phase 2 acceptance. Microphone streaming remains a separate implemented feature, not a required acceptance source unless explicitly requested. The extension does not capture current-tab/system audio; URL submission must not be described as tab capture.
- **Audit findings for follow-up:** `Start Live Speech` starts the local ASR service and microphone, but `startAudioSource` handles source-start errors internally, after which the caller can still set the overall live status to “Running.” `Stop Live Speech` flushes ASR then pauses the audio pipeline; it does not stop the microphone tracks or stop/reset the ASR backend. Thus clean stop/restart and failure-state criteria are not yet established. The extension overlay's generic transcript state is not wired to the live viewer transcript events; the live transcript is currently visible in the standalone viewer's G1 panel, while the extension receives completed YouTube job results.
- **Environment/runtime observation:** `.venv` reports Python 3.12.10 and installed faster-whisper 1.1.1. A live `POST http://localhost:8000/asr/status` returned `state: stopped`, default model `tiny.en`, CPU/int8, with zero audio received. No live transcription was performed during this audit.
- **Tests run (audit baseline):**
  - `node tools\validate_phase_f1_audio.mjs` — PASS (audio preparation/VAD pipeline; synthetic signal test, not transcription).
  - `.\.venv\Scripts\python.exe tools\validate_phase_f2_asr.py` — PASS (F2 adapter lifecycle and chunk contract using a fake Whisper model; not real recognition).
  - `node tools\validate_phase_g1_pipeline.mjs` — PASS (simulated transcript-event and sign-queue integration; not captured speech).
  - `node tools\validate_speech_sign_orchestrator.mjs` — PASS (orchestrator logic tests; not captured speech).
  - `tools\asr\test_phase_g1_live_audio.py` — NOT RUN; it requires generated local benchmark audio and explicitly selects a CUDA Whisper backend. No actual microphone speech was tested.
- **Acceptance boundary:** The microphone audit/tests concern only the optional streaming route. YouTube workflow acceptance requires an actual URL job, audio extraction (or explicitly identified cache hit), genuine audio ASR with transcript evidence, sign resolution with unsupported items disclosed, and scheduler/avatar playback evidence. Deterministic mocks alone do not establish URL workflow success.
- **Next action:** Continue validating the existing YouTube URL workflow; do not prioritize additional microphone work unless a distinct microphone requirement is approved. Current-tab audio capture is not implemented.

### PH2-STT-02 — Harden live microphone-to-text lifecycle

- **Planned:** October 13–17, 2026
- **Actual implementation/checkpoint:** October 10, 2026
- **Status:** IMPLEMENTATION CHECKPOINT — automated and capture lifecycle checks PASS; end-to-end live acceptance BLOCKED / REVIEW REQUIRED.
- **Implementation:** Reused the standalone viewer's existing microphone, 16 kHz mono float32 pipeline, `/asr/*` endpoints, transcript display, and sign orchestrator. Startup now requires successful microphone capture and ASR startup before reporting RUNNING; partial startup resources are released on failure. Stop prevents further chunk acceptance, releases microphone tracks, awaits in-flight chunks, flushes accepted audio, then calls the existing ASR stop/reset endpoints. Restart creates a fresh source and pipeline. The UI reports startup/recognition errors and permits recovery. The streaming backend now surfaces a timed-out flush, retains a worker that exceeds its bounded five-second stop wait, reports reset failure, and refuses a new worker until the prior worker exits.
- **Automated verification (October 10):**
  - `node --test tools\avatar_viewer\LiveSpeechSession.test.mjs` — PASS, 8/8, including concurrent/double-start protection, microphone and ASR startup failures, cleanup, restart, chunk failure, transcript-event delivery, and microphone setup/permission failures.
  - `node tools\validate_phase_f1_audio.mjs` — PASS; audio/VAD/chunk pipeline checks (synthetic input, not live speech).
  - `.\.venv\Scripts\python.exe tools\validate_phase_f2_asr.py` — PASS; F2 lifecycle, fresh reset/restart, stuck-worker protection, and flush-timeout reporting use fake test doubles and are not recognition evidence.
  - `node tools\validate_phase_g1_pipeline.mjs` — PASS; simulated transcript-to-sign integration, not live speech.
  - `node tools\validate_speech_sign_orchestrator.mjs` — PASS; orchestrator logic only.
  - `git diff --check` — PASS.
- **Browser lifecycle evidence (October 10):** Reloaded the standalone viewer cleanly and verified its initial stop control was disabled. Independently started live capture more than once, including after reload: each session showed `Live Speech Running`, `Microphone Active`, a `live` browser track, and ASR `running`. Stopping showed `Live Speech Stopped`, `Microphone released`, ASR `stopped`, and the captured track's `readyState` became `ended`. A controlled microphone-acquisition rejection showed ERROR rather than RUNNING; automated tests cover permission and setup failure cleanup. No bone rotations, animation poses, sign JSON, or model data were changed by these checks.
- **Live-speech blocker:** No human phrase was spoken during this verification. The microphone was active, but the service audio duration remained 0.00 seconds and the VAD forwarded no chunks. Consequently, there is no evidence of genuine speech reaching faster-whisper, a visible real transcript, transcript-triggered sign scheduling, or a live-speech stop/restart cycle following recognized speech. Fake-model tests and simulated G1 transcript events do not satisfy these criteria.
- **Acceptance decision:** PH2-STT-02 is not PASS. Retain BLOCKED / REVIEW REQUIRED until real speech produces a visible transcript and reaches the existing sign scheduler. No speech-recognition system was duplicated, and the NaN correction, sign data, animation poses, and hand articulation were not changed.
- **Files changed for this checkpoint:** `tools/audio_pipeline/AudioPipeline.js`, `tools/asr/streaming_asr.py`, `tools/avatar_viewer/LiveSpeechSession.mjs`, `tools/avatar_viewer/LiveSpeechSession.test.mjs`, `tools/avatar_viewer/index.html`, `tools/validate_phase_f1_audio.mjs`, `tools/validate_phase_f2_asr.py`, and this roadmap.
- **Next action:** PH2-STT-03 — obtain a repeatable real-microphone phrase test; verify received audio, genuine partial/final transcript display, sign scheduling, clean stop and a fresh restarted session, then record exact evidence. Keep the speech-to-text milestone open until all live criteria pass.

### PH2-STT-03 — Fix single-word and repeated-utterance handling

- **Planned:** October 17, 2026 (IST)
- **Implementation status:** Targeted code changes and automated regression tests PASS; genuine live verification BLOCKED.
- **Confirmed causes:** `LiveSpeechSession` previously sent `/asr/flush` only when Stop was pressed, so a pause between words did not produce a final event. The ASR partial decoder also waits for its configured 1,000 ms minimum, although explicit flush accepts shorter buffered audio. Separately, `SpeechSignOrchestrator` sliced parsed signs using a session-wide committed-sign count; after one finalized `hello`, another utterance with `hello` had no remaining candidate. The ASR final stabilizer retained prior final state until reset, and the existing flush did not clear its rolling audio window. These causes are confirmed by code inspection and new deterministic event/backend fixtures; they were not observed in a live microphone trace because the local service was unavailable.
- **Targeted changes:** The live controller now finalizes after 800 ms of existing VAD-rejected audio following speech; it does not reduce or otherwise alter the VAD energy threshold. Accepted audio waits behind any finalization in progress to preserve utterance order. ASR flush finalizes even below the partial minimum, then clears the current audio window and transcript stabilizer while keeping the running backend/model available for the next utterance. The orchestrator's duplicate offset is now utterance-scoped and resets on a final, so repeated valid words remain eligible while partial/final overlap within one utterance remains suppressed. Unsupported words and unavailable-sign reason codes are surfaced in diagnostics/viewer; unavailable signs are not queued. No audio samples or raw transcript text are written to diagnostic logs. Opt-in metadata-only console tracing is available with `?speechDiagnostics=1`.
- **Sign status checked:** `signs/good.json` reports `motion.status: playable` and `technical_animation_status: TECHNICALLY_PLAYABLE`; it remains `IMPLEMENTATION_PENDING_LINGUISTIC_REVIEW`. The automated test loads the actual file and verifies technical playability without claiming linguistic sign-off.
- **Automated verification:**
  - `node --test tools\avatar_viewer\LiveSpeechSession.test.mjs tools\avatar_viewer\SpeechSignOrchestrator.test.mjs` — PASS, 15/15. Covers isolated/fresh repeated finalized `hello`, partial-to-final de-duplication, VAD-silence flush, actual `good.json` status, ordered phrase signs, unsupported words, and empty/error scheduler behavior.
  - `.\.venv\Scripts\python.exe tools\validate_phase_f2_asr.py` — PASS. Includes a 200 ms mocked backend utterance below the 1,000 ms partial minimum; explicit flush returns a final, clears the utterance, and permits the same final again in a fresh buffer.
  - `node tools\validate_phase_f1_audio.mjs` — PASS; baseline chunking/VAD checks unchanged.
  - `node tools\validate_phase_g1_pipeline.mjs` — PASS; ordered HELLO → GOOD → MORNING integration and partial stability.
  - `node tools\validate_speech_sign_orchestrator.mjs` — PASS; unknown and `MOTION_INCOMPLETE` water status remain non-playable and are explicitly reported.
  - `.\.venv\Scripts\python.exe tools\validate_sign_library.py` — schema checks PASS; expected illustration/image assets remain pending and are outside this task.
- **Bounded live verification:** BLOCKED. `http://localhost:8000/asr/status` timed out, local listener checks found no ASR/viewer process on the expected ports, and no browser page was available to operate. No phrases were spoken or actually transcribed in this run; there is no live animation result to claim. Automated mocked/backend tests are not live recognition evidence.
- **Acceptance decision:** PH2 Voice to Text remains open and is not PASS. The implementation addresses identified pipeline defects, but audio quality, actual one-word recognition, automatic pause-finalization behavior, repeated live playback, and end-to-end device/service operation still need a real speaker, microphone, local ASR service, and viewer.
- **Files changed for this task:** `tools/avatar_viewer/LiveSpeechSession.mjs`, `tools/avatar_viewer/LiveSpeechSession.test.mjs`, `tools/avatar_viewer/SignScheduler.js`, `tools/avatar_viewer/SpeechSignOrchestrator.js`, `tools/avatar_viewer/SpeechSignOrchestrator.test.mjs`, `tools/avatar_viewer/index.html`, `tools/asr/streaming_asr.py`, `tools/validate_phase_f2_asr.py`, `tools/validate_speech_sign_orchestrator.mjs`, and this roadmap.
- **Next action:** Run the four requested spoken cases (`Hello`, separate `Hello`, `Good`, and `Hello, good morning`) with the local ASR service and viewer available. Enable metadata-only diagnostics using `?speechDiagnostics=1`, record only phrases genuinely shown by ASR and their actual sign/animation status, and keep PH2 open until live evidence passes. Preserve R1 as REVIEW REQUIRED and protect the November 20 demonstration deadline.

### PH2-STT-04 — Return finalized ASR events on flush

- **Actual:** October 11, 2026
- **Status:** Targeted fix and automated regression coverage PASS; live microphone verification not performed.
- **Confirmed cause:** `LocalASRService.control("flush")` recorded the backend's finalized events but discarded them from its return value. The `/asr/*` route serializes this return value directly, while `LiveSpeechSession` forwards transcript events only when the response contains `events`; therefore flush-finalized transcripts could not reach the orchestration callback. The live-session callback already used the right forwarding path and needed no duplicate forwarding branch.
- **Fix:** Flush now calls the backend once, records that returned event list once, and returns its event reports together with the resulting current status. Other control actions retain their status-only responses, and the HTTP route preserves the result unchanged. The shared ASR status renderer now updates the G1 ASR state label; ASR and live-session errors update that same label explicitly.
- **Verification:** `.\.venv\Scripts\python.exe tools\validate_phase_f2_asr.py` exercises flush event payload, updated final status, a single backend flush invocation, and existing start/pause/reset/restart behavior. `node --test tools\avatar_viewer\LiveSpeechSession.test.mjs tools\avatar_viewer\SpeechSignOrchestrator.test.mjs` exercises flush-to-session callback delivery, including separate repeated `hello` utterances, plus orchestration and scheduler cases. `node tools\validate_speech_sign_orchestrator.mjs` checks the directly related resolver/scheduler validator.
- **Live verification:** Not performed in this code-change task. Automated events are not evidence of actual microphone recognition or avatar playback; PH2 remains open until real spoken transcript and playback are observed.
- **R1:** Remains REVIEW REQUIRED pending its separate visual sign-off.
- **Next action (superseded October 21):** Validate the primary YouTube URL-to-ISL workflow. This flush fix remains scoped to the optional microphone route; it is not a blocker to YouTube batch processing.

### PH2-STT — Prioritize the YouTube URL-to-ISL workflow

- **Actual:** October 21, 2026
- **Status:** Existing URL/API pipeline verified through a cached real result; fresh download/transcription and current browser playback not performed in this bounded run. Phase 2 remains IN PROGRESS.
- **Entry point and trace:** The popup validates and submits a URL as `YOUTUBE_PROCESS`; the service worker records the active tab and invokes `RuntimeBridge.submitYouTube`; the bridge posts to local `POST /youtube/process`; `YouTubeJobManager` runs `process_youtube_video`; `download_youtube_audio` uses yt-dlp and FFmpeg to produce mono 16 kHz PCM WAV; `transcribe_audio_file` uses faster-whisper (`base.en`); `segment_and_translate` calls the existing Node translator bridge and returns glosses, playable signs, unavailable concepts, and unknown terms. The extension worker relays only playable signs as `PLAY_SIGN` followed by `QUEUE_SIGN` commands to the active tab's embedded Aether viewer and its existing `SignScheduler`. This is explicit URL processing, not tab/system-audio capture.
- **Fixture and real ASR evidence:** Reused the already-present real-video fixture `y8tFSuOMAqQ` (“How to Vlog as a Beginner (without overthinking it)”). Its cached audio is 721.835 s mono/16 kHz PCM. The persisted transcript metadata records `base.en`, CUDA/float16, 256 timestamped segments. Prior H7 evidence in `docs/h7_youtube_test_report.md` records successful audio extraction and a fresh real faster-whisper decode (28.599 s) of this audio; it is not a result newly decoded on October 21. Example persisted transcript words: “Alright, so summer is here and in my opinion that's really the best time to go out, start filming, start vlogging…”. No subtitle/caption accuracy comparison was performed in this run.
- **October 21 runtime submission:** `node tools/validate_phase_h8_extension_youtube.mjs --runtime` submitted `https://youtu.be/y8tFSuOMAqQ` through the live local `/youtube/process` API and extension service-worker boundary. The job reached READY and returned the cached full pipeline result; no YouTube download or ASR inference ran for these job IDs because `pipeline_result.json` already existed. URL acceptance/job IDs, result retrieval and schema, transcript availability, translation output, and worker commands were verified.
- **Stage results:**
  1. URL accepted: PASS; the runtime returned HTTP 202/QUEUED, and the job reached READY.
  2. Audio extraction: cached artifact confirmed present and correctly formatted; extraction was not re-executed during this run. Prior H7 evidence documents the actual extraction.
  3. ASR: cached real transcript returned (256 segments, 721.835 s); no fresh inference this run. Prior H7 evidence documents the real decode. Sample words above are from persisted ASR output; no independent caption ground-truth comparison was done.
  4. Sign resolution: PASS against the existing G2/G3 translator output: 242 concept occurrences resolved; 2,442 unknown-term occurrences remain visible.
  5. Scheduler handoff: runtime test confirmed the actual service-worker logic emitted `PLAY_SIGN good`, then two `QUEUE_SIGN good` commands for the three playable occurrences. 239 concept occurrences are unavailable and were not scheduled.
  6. Avatar playback: not observed in this October 21 run because the integrated browser could not open the local viewer (`chrome-error://chromewebdata/`). Existing H7/H8 reports document a prior browser harness run where the real Aether viewer received those three `good` commands, reported current/queued `good`, and emitted playback lifecycle events; do not misattribute that earlier evidence to today's runtime run. Installed-extension playback on a real YouTube tab remains outstanding.
- **Focused commands (October 21):**
  - `node tools\validate_phase_h8_extension_youtube.mjs` — PASS; deterministic extension/API contract and error-path tests. The expected mocked negative-case log `[ISL Runtime Bridge] YouTube job failed: ASR failed` appeared; the validator completed successfully.
  - `node tools\validate_phase_h8_extension_youtube.mjs --runtime` — PASS; real localhost URL/job/result route against the cached real-video pipeline result; extension worker emitted three expected Aether commands. It does not prove a new download or decode, nor current visual playback.
  - `git diff --check` — PASS (documentation-only update).
- **User-visible error behavior:** Popup and overlay display URL validation/runtime/job errors, including job-stage failures. Unavailable signs and unknown concepts are surfaced instead of fabricated or scheduled.
- **Acceptance decision / blockers:** Do not mark Phase 2 complete based on this cache-backed API run. Repeat with an actual fresh URL download/transcription if required by release acceptance, compare recognized words to a known transcript, and verify current browser/avatar playback completion. The extension must be installed/active for the strict real-YouTube-tab handoff check. Microphone flush/finalization is a separate feature and is not shown to block this batch route.

## Risks and guardrails

- R1 remains **REVIEW REQUIRED** until the unclear isolated finger-axis views are resolved or an explicitly approved fallback is recorded; do not infer a visual PASS from the automated suite.
- The correction deliberately does not change the zero X scale or FBX file. Any missing or ineligible expected candidate produces a visible REVIEW REQUIRED result and is not normalized.
- Keep the prior report edits in `docs/r1_fine_grained_articulation_report.json` and `docs/r1_fine_grained_avatar_articulation.md`; do not overwrite them.
- The Aether model is local-only and excluded from Git. Do not upload it or bundle model-derived assets.
- Do not start Phase 2 until Phase 1 passes or an explicitly approved time-boxed fallback is chosen.

## Next task

**PH2-STT — Complete YouTube URL-to-ISL acceptance**

**Planned:** Phase 2 follow-up (date to be scheduled)

**Prerequisite:** Owner approved the bounded R1 fallback on October 10, 2026; R1 remains REVIEW REQUIRED.

**Concrete next action:** Run a bounded fresh YouTube URL job that does not hit the full-result cache; verify audio extraction, compare genuine ASR words to captions/reference audio, then verify resolved/unavailable concepts and actual Aether sign playback start/completion with the extension installed. Preserve the distinction between URL ingestion and current-tab capture; do not make the optional microphone workflow a Phase 2 gate unless that requirement is separately reinstated.
