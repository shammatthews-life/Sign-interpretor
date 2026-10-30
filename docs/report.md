# ISL Accessibility Translator — Project Understanding & Continuation Report

**Date:** October 30, 2026  
**Local Time:** 20:05 IST  
**Git Branch:** `r1-articulation-coverage-and-report` (7 commits ahead of `origin/r1-articulation-coverage-and-report`)  
**Latest Commits:**
- `dbd4cd0` docs(stt): record fresh YouTube pipeline evidence
- `fb7b040` docs(stt): prioritize YouTube workflow evidence
- `e83cba9` fix(stt): return finalized transcript events on flush
- `4007233` fix(stt): handle single and repeated utterances
- `97217bb` fix(stt): harden microphone capture lifecycle

---

## A. What the Project Is

The **ISL Accessibility Translator** (`Sign-interpretor`) is a specialized web accessibility application implemented as a Google Chrome browser extension (Manifest V3) paired with a local Python 3.12 runtime. Its sole purpose is to convert the spoken audio of YouTube videos into Indian Sign Language (ISL) gloss sequences and display them in real time via an animated 3D humanoid avatar named **Aether**.

The project is intentionally focused on **YouTube video translation only**. It is not a live microphone speech-to-sign app, an arbitrary whole-OS audio capturer, a general website translator, or a sign-to-text recognition tool.

---

## B. Final Product Experience

When a Deaf or hard-of-hearing user opens a YouTube video:
1. The original YouTube video continues playing unobstructed in the main video player.
2. An ISL accessibility overlay appears as a non-intrusive floating panel docked at the **bottom-right corner** of the viewing area.
3. The user can toggle or minimize the panel, inspect transcript and sign status diagnostics, or adjust settings.
4. As dialogue occurs in the video, the audio is processed into timestamped transcript segments, transformed into ISL grammatical gloss sequences, filtered through an evidence-gated sign library, and sequentially executed by the Aether avatar.
5. In the mature vision, the avatar signs in temporal synchronization with the speaker on the video timeline, responding seamlessly to play, pause, seek, and playback rate adjustments.
6. If a spoken concept has no linguistically verified or playable sign, the system transparently identifies it as unavailable rather than fabricating arbitrary hand movements.

---

## C. Current Architecture

The end-to-end data flow operates through a decoupled, modular pipeline:

```
YouTube Video URL
       ↓
Chrome Extension (Popup / Content Script)
       ↓
Local Backend Runtime API (FastAPI / HTTP localhost:8000)
       ↓
yt-dlp (Permitted audio extraction, background job queue)
       ↓
FFmpeg Normalization (Mono 16 kHz PCM WAV)
       ↓
faster-whisper ASR (base.en, CUDA float16 batch inference)
       ↓
Timestamped Transcript Segments ([start, end, text])
       ↓
EnglishToISLTranslator (G2/G3 rule-based linguistic transformation)
       ↓
Signability & Evidence Validation (SignLibrary schema 2.0.0 checks)
       ↓
SignScheduler (Queueing, neutral-pose blending, state tracking)
       ↓
SignAnimationPlayer (Keyframe interpolation, easing, bone transforms)
       ↓
Aether 3D Avatar (Three.js WebGL rendering inside isolated iframe)
       ↓
Floating Bottom-Right YouTube Accessibility Overlay (Shadow DOM)
```

---

## D. Completed Implementation & Key Files

### 1. Browser Extension (`extension/`)
- `extension/manifest.json`: Manifest V3 configuration, permissions (`storage`, `activeTab`, `host_permissions` for localhost and YouTube).
- `extension/popup/` (`popup.html`, `popup.js`, `popup.css`): URL entry, connection status, job submission, and diagnostics.
- `extension/content/` (`content-script.js`, `overlay.js`, `overlay.css`): Shadow DOM isolated overlay injection, SPA navigation resilience, iframe avatar host, and drag/minimize handling.
- `extension/background/` (`service-worker.js`, `runtime-bridge.js`): Background coordinator connecting extension events to local HTTP API endpoints (`/youtube/process`, `/youtube/status`, `/youtube/result`).
- `extension/shared/` (`message-contract.js`, `demo-data.js`): Strict typed message contracts and deterministic demo scenarios.

### 2. Local Python Development Runtime (`tools/`)
- `tools/run_avatar_viewer.py`: Development server hosting avatar viewer assets and YouTube REST endpoints on port 8000.
- `tools/youtube_pipeline/youtube_ingest.py`: YouTube URL validation (11-char regex), yt-dlp audio download, FFmpeg 16 kHz WAV conversion, faster-whisper execution, cached job storage in `runtime/youtube/<video_id>/`.
- `tools/youtube_pipeline/run_test_video.py`: Standalone CLI pipeline runner for testing YouTube processing.
- `tools/asr/` (`streaming_asr.py`, `asr_service.py`): ASR service with CUDA verification and speech transcription lifecycle handling.

### 3. Avatar Viewer & Sign Motion Engine (`tools/avatar_viewer/`)
- `tools/avatar_viewer/index.html`: Three.js runtime hosting the local `Avatar_Boy_Gun_AetherShadow` FBX model.
- `tools/avatar_viewer/SignAnimationPlayer.js`: Keyframe-based animation playback, bone transform application, and easing.
- `tools/avatar_viewer/SignLibrary.js`: Schema 2.0.0 validation, asset loading, and playable motion gating.
- `tools/avatar_viewer/SignScheduler.js`: Queue management, neutral pose transitions, concurrency prevention, and lifecycle events.
- `tools/avatar_viewer/SpeechSignOrchestrator.js`: Transcript-to-translation-to-animation bridge.
- `tools/avatar_viewer/EnglishToISLTranslator.js` & `TranslationBackend.js`: Normalization, phrase lookup, negation/question detection, and candidate sign ID resolution.
- `tools/avatar_viewer/NonFiniteHelperBoneCorrection.mjs`: Mathematical rotation fix for non-finite helper bones (`PRIVATE_Grenade_Point`) preserving rest-pose integrity.

### 4. Authored Sign Library (`signs/`)
- Authoring format: Schema 2.0.0 JSON separating linguistic metadata, keyframes, bone transforms, and review status.
- Current authored assets:
  - `signs/hello.json`: 7 keyframes, 2000 ms, authored temple greeting motion (lexical ISL, not fingerspelling).
  - `signs/good.json`: Playable motion, pending linguistic sign-off.
  - `signs/morning.json`: Playable motion, pending linguistic sign-off.
  - `signs/water.json`: Marked `MOTION_INCOMPLETE` (not playable).

---

## E. Research Foundation

### 1. Published Literature
- **Base Paper — Patra et al. (IJCAI 2026):** *"A Gloss-driven Indian Sign Language Production System Using Learned Pose Representations"*. Proposes Sign-Pose-VQ-VAE decomposing ISL into body, left-hand, and right-hand discrete codebooks with co-articulation. Serves as our long-term conceptual benchmark for ISL generation.
- **Prior Baseline — Zuo et al. (ECCV 2024):** *"A Simple Baseline for Spoken Language to Sign Language Translation with 3D Avatars (Spoken2Sign)"*. Demonstrates end-to-end spoken text to 3D avatar animation using gloss dictionaries and sign connectors.
- **T2S-GPT — Yin et al. (ACL 2024):** Autoregressive vector-quantized sign production; reference for motion tokenization and duration modeling.
- **Additional Survey References (2024–2026):** Li (2025; editable JSON intermediate representation), Ma et al. (2024; attentional hand focus), Xie et al. (2024; latent motion transformer), G2P-DDM (2024; diffusion pose generation), Walsh et al. (2024; lexical selection and reordering), Nayak et al. (2025; ISL Odia translation), Taşyürek et al. (2026; articulator disentanglement), Kha et al. (2026; temporal diffusion).

### 2. Separation of Implementations vs. Proposed Research
- **Current Implemented Baseline:**
  - Speech Recognition: `faster-whisper base.en` (CUDA float16).
  - Linguistic Processing: `EnglishToISLTranslator.js` (G2/G3 rule-based lexicon and phrase mapper).
  - Motion Engine: Schema 2.0.0 JSON keyframes on FBX skeleton via Three.js.
- **Proposed Future Model Candidates:**
  - Speech Recognition: `Whisper large-v3-turbo` (to be independently benchmarked on WER, CER, RTF, latency against `base.en`).
  - Text/Gloss Processing: `Qwen3-4B` (to be benchmarked against rule-based translation for semantic preservation and gloss structure).
  - Research Layer: **SASA-ISL** (*Signability-Aware Semantic Adaptation for Indian Sign Language*), an intended constraint-verification layer validating candidate glosses against evidence quality, temporal video duration, and signability before execution.

---

## F. Current Verified Test Evidence

### What Actually Passed (Real Evidence)
1. **Fresh YouTube Backend Pipeline Test (Oct 21, 2026):**
   - Video URL: `https://www.youtube.com/watch?v=EvbhKINYrPg`
   - Job ID: `yt_EvbhKINYrPg_a05755a17692` reached `READY`.
   - Extracted 599.725 s mono 16 kHz WAV audio in 9.922 s.
   - Batch ASR inference: 35.328 s on CUDA float16, producing 130 timestamped segments.
   - Sample reference comparison: Opening dialogue matched 26/26 words against YouTube captions.
   - Translation breakdown: 156 concept occurrences (61 playable: 28 `good`, 22 `morning`, 11 `hello`; 95 unavailable; 314 unknown terms).
2. **Deterministic & Harness Verification:**
   - `tools/validate_phase_h8_extension_youtube.mjs`: 14/14 checks passed (URL validation, API contract, status polling, relay contracts).
   - `tools/validate_phase_r1_articulation.mjs` and `NonFiniteHelperBoneCorrection.test.mjs`: 5/5 unit tests passed; zero non-finite rest components.

---

## G. Current Blockers

1. **Extension-to-Avatar End-to-End Verification Gap:** The full loop from user click in the unpacked Chrome extension popup on `youtube.com` -> service worker -> local runtime -> overlay content script -> embedded iframe -> `SignScheduler` -> physical Aether animation has only passed in mocked harnesses, not in an installed Google Chrome instance.
2. **Vocabulary Coverage:** Only 3 greeting motions (`hello`, `good`, `morning`) are currently marked playable. 95+ concept occurrences in typical videos are reported unavailable.
3. **Linguistic Review Status:** `good` and `morning` are technically playable but pending certified ISL interpreter review. `water` is incomplete.
4. **Video Timeline Synchronization:** Current playback queues signs immediately upon translation completion rather than synchronizing sign dispatch to the video player's `currentTime`, play/pause events, or seek operations.

---

## H. Fresh Test Run & Vocabulary Collection Video: MXKkXXYUxBc

**Target Video:** `https://youtu.be/MXKkXXYUxBc`  
**Title:** *Public Speaking for Beginners - Free Full Course | Speak with Confidence*  
**Duration:** 8,979 seconds (~2 hours, 29 minutes, 39 seconds)

### 1. Ingestion & ASR Execution Results
- **Audio Extraction:** Downloaded 110.60 MiB audio stream via `yt-dlp`; converted by `FFmpeg` to mono 16 kHz PCM WAV.
- **ASR Model:** `faster-whisper base.en` on CUDA with `float16`.
- **Transcription Duration:** 241.826 seconds (~4.03 minutes; Real-Time Factor: **0.0269**).
- **Segment Count:** 2,366 timestamped segments.
- **Total Word Count:** 23,049 words.

### 2. Translation & Concept Availability Breakdown
- **Total Concept Occurrences:** 1,943 occurrences
- **Playable Sign Occurrences:** 63 occurrences (3.24%)
  - `good`: 57 occurrences
  - `morning`: 3 occurrences
  - `hello`: 3 occurrences
- **Unavailable Concept Occurrences:** 1,880 occurrences (96.76%)
  - `you`: 1,000 occurrences
  - `i`: 580 occurrences
  - `how`: 94 occurrences
  - `not`: 93 occurrences
  - `me`: 92 occurrences
  - `need`: 10 occurrences
  - `help`: 6 occurrences
  - `thank_you`: 3 occurrences
  - `tomorrow`: 1 occurrence
  - `drink`: 1 occurrence
- **Unknown Term Occurrences:** 19,048 occurrences (words not yet present in the translator lexicon/phrase tables).

---

## I. Corpus Frequency Analysis & Targeted Vocabulary Priority

Analyzing the 23,049 words in `MXKkXXYUxBc` highlights that spoken instruction heavily concentrates on a compact set of high-utility functional terms. Authoring and verifying this vocabulary will yield exponential coverage gains:

### 1. People / Pronouns & Deictics (Total Occurrences: 2,661)
- `you`: **1,003**
- `your`: 271
- `i`: **580**
- `my`: 144
- `me`: 92
- `we`: 127
- `they`: 123
- `them`: 84
- `he` / `she`: 129
- `people`: 93

### 2. Common Action Verbs (Total Occurrences: 1,323)
- `have`: 201
- `do`: 198
- `go` / `going`: 240
- `want`: **118**
- `look`: 110
- `give`: 73
- `see`: 71
- `know`: 70
- `say`: 44
- `take`: 32
- `feel`: 23
- `come`: 20
- `need`: 10
- `help`: 6

### 3. Interrogatives / Questions (Total Occurrences: 565)
- `what`: **158**
- `when`: 133
- `how`: **94**
- `which`: 60
- `why`: 46
- `who`: 45
- `where`: 29

### 4. Negation & Core Modifiers (Total Occurrences: 1,168)
- `not`: **93**
- `no`: 42
- `yes`: 31
- `now`: 92
- `more`: 84
- `all`: 73
- `one`: 142
- `good`: 57 (Currently playable)
- `bad`: 14

### Immediate Priority Vocabulary Target (High-Leverage Set)
By authoring, validating, and adding just seven high-frequency signs to the library, coverage in this video alone expands from **63** to **over 2,200 playable occurrences**:
1. **`YOU`** (1,003 occurrences) — Index-finger deictic pointing forward.
2. **`I` / `ME`** (672 occurrences) — Index-finger deictic pointing to chest.
3. **`WHAT`** (158 occurrences) — Open hands palm-up with side-to-side questioning motion.
4. **`GO`** (129 occurrences) — Directional forward hand movement.
5. **`WANT`** (118 occurrences) — Claw-hand pulling toward torso.
6. **`NOT`** (93 occurrences) — Flat-hand or index negation wave with non-manual headshake.
7. **`HOW`** (94 occurrences) — Curved fingers rotating outward.

---

## J. Live Browser & Animation Verification (Google Chrome CDP)

To close the real-browser verification gap, the Three.js avatar viewer runtime was launched and inspected directly inside Google Chrome (`Version 156.0.8078.76`) via Chrome DevTools Protocol (CDP):

1. **Viewer Runtime Initialization:**
   - Server active on `http://localhost:8000`.
   - WebGL Three.js canvas rendered cleanly.
   - FBX model `Avatar_Boy_Gun_AetherShadow` successfully parsed.
   - Total skeleton bones resolved: **243 bones**.
2. **Helper Bone Rotations (`R1`):**
   - Helper bone correction status: **`PASS`**.
   - Identity rotations applied to `PRIVATE_Grenade_Point` and `PRIVATE_Grenade_Point_Low` prior to rest-pose snapshot; non-finite components = 0.
3. **In-Browser Sign Playback & Scheduler Check:**
   - Sequential test enqueued: `['good', 'morning', 'hello']`.
   - Initial dispatch: `currentId: "good"`, `queue: ["morning", "hello"]`, `playerIsPlaying: true`.
   - Mid-playback state: `currentId: "morning"`, `queueRemaining: ["hello"]`, `playerIsPlaying: true`.
   - Result: Successful sequential keyframe interpolation, per-segment easing, and neutral-pose transitions observed without runtime errors in the Chrome browser environment.

---

## K. Phase H9 Vocabulary Roadmap & Mathematical Audit

A comprehensive development plan was established in [`docs/h9_isl_vocabulary_roadmap.md`](h9_isl_vocabulary_roadmap.md).

### 1. Mathematical Audit & Reconciled Discrepancies
- **Standalone `you` (1,000) vs. Raw token `you` (1,003):** 3 occurrences of `you` belong to the 2-word phrase `"thank you"`, which mapped to `THANK_YOU`, leaving exactly 1,000 standalone `you` occurrences.
- **Case Distinction vs. ISL Deictics:** English separates `I` (580) and `ME` (92); in ISL, both use identical index-finger deictic pointing to the center chest. Possessive `MY` (144) uses an open flat hand on the chest and must remain distinct.
- **Locomotion `GO` vs. Intention `"GOING TO"`:** In the transcript, `"going to"` appears 85 times (40 as `"i'm going to"`). In ISL, this expresses immediate intention/future (`FUTURE`/`PLAN`), not physical walking (`GO`).

### 2. Top 15 Priority Concepts & Implementation Batches
- **Batch 1 (5 High-Leverage Deictics & Questions):** `YOU` (1,003), `I`/`ME` (672), `WHAT` (158), `HOW` (94), `NOT` (93).  
  *Estimated video coverage increase: ~2,020 occurrences (reaching >90% concept coverage of recognized terms).*
- **Batch 2 (Core Action Verbs):** `GO` (129), `WANT` (118), `HAVE` (201), `LOOK/SEE` (181), `DO` (198).
- **Batch 3 (Quantifiers & Discourse):** `ONE` (142), `WHEN` (133), `PEOPLE` (93), `NOW` (92), `MORE` (84).

All 15 concepts have documented references in the official ISLRTC video dictionary.

---

## L. IDE Environment Fix

Resolved the VS Code/IDE Python extension path warning (`${workspaceFolder}/.venv/Scripts/python.exe` resolution failure) by updating `.vscode/settings.json` with escaped Windows path delimiters (`${workspaceFolder}\\.venv\\Scripts\\python.exe`).

---

## M. Phase H10 Real Extension-to-Aether E2E Acceptance Evidence

**Execution Date:** October 30, 2026  
**Test Video:** `https://www.youtube.com/watch?v=EvbhKINYrPg` (English greeting dialogue, 600 s)  
**Job ID:** `yt_EvbhKINYrPg_8086cee7a18d`

### 1. Browser Architecture & Execution Findings
- **Google Chrome CLI Limitation Discovered:**  
  Official branded Google Chrome on Windows explicitly blocks `--load-extension` via CLI (`chrome\browser\extensions\extension_service.cc:423: WARNING: --load-extension is not allowed in Google Chrome, ignoring.`).  
  For Chrome, the unpacked extension must be loaded via the standard UI (`chrome://extensions` $\to$ *Developer mode* $\to$ *Load unpacked*).
- **Chromium Live E2E Verification (Microsoft Edge Engine):**  
  The unpacked extension was loaded directly into the Chromium engine with CDP automation, demonstrating the complete live browser pipeline without mocks.

### 2. Verified Workflow & Message Flow Chain
1. **Extension Service Worker (`gonglknbkaolppemaahmcfpclnegikbd`):**
   - Active at `background/service-worker.js`.
   - Connected to local development runtime at `http://localhost:8000` (`runtimeAvailable: true`).
2. **YouTube Tab Integration:**
   - Opened `https://www.youtube.com/watch?v=EvbhKINYrPg`.
   - Content script injected; Shadow DOM overlay `#isl-accessibility-overlay-root` mounted.
   - Fixed module-level scoping for `flushAetherCommands` and `bindAetherFrame` in `content-script.js`.
   - Embedded `#isl-aether-iframe` pointed to `http://localhost:8000/tools/avatar_viewer/index.html?embed=1` (`iframeHidden: false`).
3. **Popup Submission & Processing:**
   - Opened actual extension popup UI (`popup/popup.html`).
   - Populated `#youtube-url` with `https://www.youtube.com/watch?v=EvbhKINYrPg` and triggered `#btn-youtube-process`.
   - Service worker dispatched `YOUTUBE_PROCESS`, queried local backend, polled job `yt_EvbhKINYrPg_8086cee7a18d` to `READY`.
   - Popup UI rendered completed state: `video 600 s · audio 599.7 s`.
4. **Command Relay & Avatar Execution:**
   - Service worker identified 61 playable occurrences (`GOOD`, `MORNING`, `HELLO`) and dispatched `PLAY_SIGN` / `QUEUE_SIGN` messages to the tab.
   - Content script forwarded commands to the iframe via `postMessage`.
   - Aether `SignScheduler` enqueued and animated the signs through Three.js; unavailable concepts (`HOW`, `YOU`, `NOT`, `I`, `NEED`, `THANK_YOU`, `TOMORROW`) were reported with zero fabricated gestures.

---

## N. Long-Running Execution Profile & Batch 1 Vocabulary Implementation

### 1. Long-Running Process Identification
- In the active development session, the background task:
  `.\venv\Scripts\python.exe tools\run_avatar_viewer.py --port 8000 --no-browser`
  is the **local development HTTP server daemon**. It is not stuck; it actively serves Three.js FBX assets, sign definitions, and development REST endpoints to the Chrome extension.

### 2. Execution-Time & Benchmarking Profile
- **Long Lecture (`MXKkXXYUxBc`, 2 hrs 29 mins 39 secs / 8,979 s audio):**
  - Audio extraction & normalization (yt-dlp + FFmpeg): ~73 s (110.60 MiB stream $\to$ mono 16 kHz WAV).
  - Speech Recognition (`faster-whisper base.en` on CUDA `float16`): 241.826 s (~4.03 minutes).
  - Real-Time Factor (RTF): **0.0269** (processes 1 minute of video audio in ~1.6 seconds of GPU compute).
  - Linguistic translation across all 2,366 segments: **0.615 seconds**.
- **Dialogue Test (`EvbhKINYrPg`, 10 mins / 600 s audio):**
  - Audio extraction: 9.922 s | ASR: 35.328 s | Translation: 0.135 s.
- **Cache Hits:**
  - Repeated extension queries on processed videos resolve in under **50 ms**.

### 3. Vocabulary Scaling Strategy (23k Words vs. Core ISL Lexicon)
- **Zipf's Law & Communicative Density:** A 23,049-word transcript does NOT require 23,000 separate animations. Spoken natural language concentrates communicative density in a compact core.
- **ISL Linguistic Integrity:** Natural Indian Sign Language has a core lexicon of ~2,500–5,000 signs. Technical terminology (e.g. `dopamine`) and proper names are communicated via two-handed ISL fingerspelling, not fabricated gestures.
- **Strict Accessibility Guardrail:** Silently substituting ASL or international gestures when an ISL sign is absent confuses Deaf Indian users and violates ISLRTC standards. Signs must be authentically authored according to ISL evidence or transparently reported as unavailable/pending review.

### 4. Batch 1 Implementation & Measured Coverage Jump
Authored Schema 2.0.0 signs with precise finger-curl articulation and wrist orientations:
- [`signs/you.json`](signs/you.json): Dominant index-finger point (`index: 0, thumb/middle/ring/pinky: 60–75° curl`), 1200 ms.
- [`signs/i.json`](signs/i.json): Dominant index-finger deictic to chest center, 1200 ms.
- [`signs/what.json`](signs/what.json): Two-handed open palms-up questioning oscillation, 1500 ms.
- [`signs/not.json`](signs/not.json): Flat-hand horizontal wave with coordinated headshake, 1400 ms.
- [`signs/water.json`](signs/water.json): W/3-finger chin contact motion, 1500 ms.

### 5. Measured Video Coverage Gain on `MXKkXXYUxBc`
Reprocessing the full 2,366 transcript segments through `EnglishToISLTranslator`:
- **Before Batch 1 (Baseline):** 63 playable occurrences (`good`: 57, `morning`: 3, `hello`: 3).
- **After Batch 1 Implementation:** **1,986 playable occurrences** (an increase of **+1,923 playable occurrences**).
  - `you`: 1,000 occurrences
  - `i`: 580 occurrences
  - `what`: 158 occurrences
  - `not`: 93 occurrences
  - `me`: 92 occurrences
  - `good`: 57 occurrences
  - `morning`: 3 occurrences
  - `hello`: 3 occurrences
- **Unavailable Occurrences Reduced:** Dropped from **1,880 down to only 115** occurrences (94.5% concept resolution).
---
---

## O. Phase H12 Full 23,049-Word Corpus Audit & ISL Expansion Plan

A complete audit of all 23,256 spoken words and 2,366 segments in `MXKkXXYUxBc` was conducted and documented in [`docs/h12_corpus_vocabulary_audit.md`](h12_corpus_vocabulary_audit.md).

### 1. Corpus Statistics
- **Total Spoken Tokens:** 23,256
- **Unique Surface Words:** 2,286
- **Unique Normalized Lemmas:** 1,981
- **Top 100 Lemmas:** Cover **15,158 tokens (65.18%)** of the entire lecture.
- **Top 250 Lemmas:** Cover **18,495 tokens (79.53%)**.
- **Top 500 Lemmas:** Cover **20,562 tokens (88.42%)**.

### 2. Multi-Denominator Coverage Truth
- **Total ASR Tokens:** 23,256 words recognized.
- **Spoken Word Playable Coverage:** **2,089 / 23,256 tokens (8.98%)** are directly signed by our playable library.
- **Structural Function Words:** **5,029 / 23,256 tokens (21.62%)** are English function words (`be`, `the`, `a`, `to`, `of`, `in`, `and`) that are naturally omitted or spatially indexed in ISL grammar.
- **Combined Communicative Coverage:** **7,118 / 23,256 tokens (30.61%)** are structurally or lexically accounted for.
- **Unresolved Spoken Tokens:** 16,138 tokens (69.39%), prioritizable through the Top 100 lemma list.

### 3. Reconciled Batch 1 & Authoring Status
Original Batch 1 priority list is now 100% authored, playable, and Schema 2.0.0 validated:
- `YOU` ([`signs/you.json`](signs/you.json)): 1,003 occurrences
- `I` / `ME` ([`signs/i.json`](signs/i.json)): 672 occurrences
- `WHAT` ([`signs/what.json`](signs/what.json)): 158 occurrences
- `HOW` ([`signs/how.json`](signs/how.json)): 94 occurrences (authored in H12)
- `NOT` ([`signs/not.json`](signs/not.json)): 93 occurrences
- `WATER` ([`signs/water.json`](signs/water.json)): authored in H11

---
---

## P. Phase H13 Evidence-Based ISL Motion Authoring & Unavailable-Word Subtitle System

Documented in detail in [`docs/h13_motion_authoring_and_subtitle_fallback.md`](h13_motion_authoring_and_subtitle_fallback.md).

### 1. Batch 2 Authoring (Schema 2.0.0)
Authored and integrated 6 priority ISL motions from the `MXKkXXYUxBc` lecture corpus:
- [`signs/your.json`](signs/your.json): 275 occurrences. Possessive pronoun; flat B-handshape facing addressee (1200 ms).
- [`signs/my.json`](signs/my.json): 144 occurrences. Possessive pronoun; flat B-handshape resting on center chest (1200 ms).
- [`signs/have.json`](signs/have.json): 257 occurrences. Two-handed possessive verb; curved cupped hands contacting torso (1400 ms).
- [`signs/want.json`](signs/want.json): 129 occurrences. Two-handed volitional verb; open claw hands pulling toward torso (1400 ms).
- [`signs/look.json`](signs/look.json): 151 occurrences. Directional visual verb; V-handshape pointing toward visual target (1300 ms).
- [`signs/see.json`](signs/see.json): 97 occurrences. Visual perception verb; V-handshape moving forward along line of sight (1300 ms).

All authored motions are classified as `IMPLEMENTATION_PENDING_LINGUISTIC_REVIEW` to maintain scientific integrity until certified by native Deaf ISL signers.

### 2. Unavailable-Word Subtitle Fallback System
Implemented a fallback UI directly below the Aether avatar canvas in `#isl-accessibility-overlay-root`:
- **Header:** `"ISL translation not available in this translator"`.
- **Text Rendering:** Safe `textContent` display of the exact spoken English word/phrase from the transcript segment.
- **Playback Behavior:** When an unavailable concept is encountered, Aether resets to neutral and the subtitle appears. When the next playable sign starts, the subtitle is automatically dismissed.
- **Natural Grammar Omission:** English auxiliary verbs and articles (`is`, `are`, `be`, `the`, `a`, `to`, `of`) omitted by natural ISL syntax are classified under `GRAMMAR_OMISSION` and bypass the unavailable warning display.

### 3. Measured Corpus Impact on `MXKkXXYUxBc`
- **Playable Sign Library:** Expanded from 9 to **15 signs**.
- **Playable Tokens in Lecture:** Increased from 2,089 to **3,142 spoken words (13.51%)** (+1,053 tokens).
- **Combined Communicative Coverage:** Expanded from 7,118 to **8,171 spoken words (35.14%)**.
- **Validation:** 100% pass on [`tools/validate_phase_h13_motion_and_subtitle.mjs`](../tools/validate_phase_h13_motion_and_subtitle.mjs) with zero regressions across all previous test suites.

---
---

## Q. Phase H14 Visual & Extension Integration Verification

Documented in detail in [`docs/h14_visual_and_extension_verification.md`](h14_visual_and_extension_verification.md).

### 1. Verification of the 15-Sign Library
All 15 authored motions (`hello`, `good`, `morning`, `water`, `you`, `i`, `what`, `not`, `how`, `your`, `my`, `have`, `want`, `look`, `see`) were verified for:
- Finger articulation curls (`thumb`, `index`, `middle`, `ring`, `pinky`).
- Two-handed coordination across symmetrical Left and Right rigs (`WHAT`, `HOW`, `HAVE`, `WANT`, `MORNING`).
- Exact terminal keyframe return to anatomical neutral `{ x: 0, y: 0, z: 0 }`.

### 2. Extension Subtitle & Reading Persistence
- Implemented a 2500 ms minimum persistence timer on the unavailable subtitle fallback to ensure human readability.
- Clear cancellation triggers when a subsequent playable sign starts.
- Safe `textContent` sanitization blocks transcript script injection.

### 3. Review Status Distinction & Mixed-Sentence Support
- In `#isl-overlay-container`, active signs display a dedicated `[PENDING REVIEW]` or `[VERIFIED]` badge.
- Added deterministic scenario `mixed_sentence` (`"I want your dopamine"`) demonstrating interleaving between playable signs and unavailable word fallbacks.
- Verified by [`tools/validate_phase_h14_visual_and_extension.mjs`](../tools/validate_phase_h14_visual_and_extension.mjs) (PASS 1 through 7).
