# H43 — Independent Baseline & Forensic Audit Report (Phase 0)

**Milestone:** H43 — Independent Forensic Validation, Multi-Domain ISL Translation Intelligence & Autonomous Accuracy Engineering Campaign  
**Date:** 2026-11-25  
**Auditor:** Antigravity Autonomous Engineering System  
**Scope:** Independent verification of Repository State, H42 Artifacts, ASR Benchmarks, Semantic Engine, ISL Grammar, Sign Library, Tests, and Real-Browser Visual QA.

---

## 1. Executive Summary of Forensic Verification

An independent, code-level and visual-evidence audit of H42 reveals a stark divergence between H42's reported metrics (`65.60%` direct coverage, `100.0%` meaningful coverage, `0.00%` Video B WER, `596` playable signs, `PASS` real-browser Full Body recordings) and the ground-truth behavior of the live pipeline.

While H42's unit tests (`76/76`), manifest validator (`596` JSON files), dual-benchmark script (`27/27` assertions), and edge-case tests (`8/8`) pass as written, **those checks mask critical defects across every stage of the pipeline**:

1. **Avatar Never Rendered in Real Chrome YouTube Sessions:** Visual inspection of H42 (and H41/H38/H35_1) browser screenshots proves `#isl-aether-iframe` stayed at `about:blank`. No 3D avatar appeared in the viewport, no translation job was initiated, Video A captured a Coursera ad, Video B stayed paused at `0:02`, and anatomical crops captured YouTube's ad sidebar.
2. **46 New Signs Fail at Runtime (`NOT_PRELOADED`):** `tools/avatar_viewer/index.html` only preloads a hardcoded list of 550 signs, and `SignLibrary.getPlayable()` throws `NOT_PRELOADED` for any sign not in `this.cache`. All 46 signs added across H37–H42 (including H42's 6 signs) cannot play in the live viewer.
3. **Self-Generated ASR Reference (`0.00% WER` Illusion):** `h42_video_b_locked_benchmark.json` is an exact copy of `faster-whisper base.en` output (`transcript.json`), producing circular `0.00%` WER while hiding real recognition errors (`"future films"` instead of `"feature films"`, `"seen by scene"` instead of `"scene by scene"`).
4. **Dead Semantic Engine & Meaning-Reversing Omissions:** `SemanticUnderstandingEngine.js` computes an `isr` object that `EnglishToISLTranslator.js` never reads during translation. Meanwhile, H42 achieved `0 unknown terms` by omitting meaning-critical words (`without`, `because`, `but`, `out`, `up`, `down`) as `GRAMMAR_OMISSION` (e.g., turning *"without completely overcomplicating"* into `ALL CONFUSED`) and inserting erroneous lexicon mappings (`evening -> MORNING`, `eight -> ONE`, `nine -> ONE`, `third -> ONE`, `wind -> TREE`, `yesterday -> TIME`).
5. **133 Duplicate Sign Trajectories in 596-Sign Library:** Out of 596 JSON sign files, only 463 have unique joint rotations; 133 signs share byte-identical animations across 14 template clusters (including 64 distinct words sharing one identical arm motion), yet all 596 carry `"organization": "ISLRTC"` provenance.

---

## 2. Repository & Runtime State Verification

- **Git Branch & HEAD:** `main` at `70f4bd1` (`feat(h41): video translation accuracy engine, ISL SOV syntax, 590 signs & visual audit`).
- **Working Tree Changes (Preserved):**
  - Modified tracked files: `signs/manifest.json`, `tools/avatar_viewer/EnglishToISLTranslator.js`.
  - Untracked H42 deliverables: `signs/{advice,food,future,summer,tired,together}.json`, `tools/asr/benchmark_h42_asr.py`, `tools/audit_video_b_vocabulary.mjs`, `tools/avatar_viewer/SemanticUnderstandingEngine.js`, `tools/avatar_viewer/scan_video_b.mjs`, `tools/run_h42_dual_visual_audit.mjs`, `tools/test_h42_dual_benchmark_evaluation.mjs`, `tools/test_h42_expanded_linguistic_suite.mjs`, `artifacts/h42/`, and `docs/H42_*.md`.
- **Hardware & Compute Environment Verified:**
  - GPU: NVIDIA GeForce RTX 4050 Laptop GPU (`6141 MiB` total VRAM, `5719 MiB` free, driver `610.91`).
  - CUDA (`ctranslate2`): 1 CUDA device detected.
  - FFmpeg NVENC: `ffmpeg-win-x86_64-v7.1.exe` supports `h264_nvenc`, `hevc_nvenc`, `av1_nvenc`.
  - Local Server: `tools/run_avatar_viewer.py` running on `127.0.0.1:8000` (`task-3080`).

---

## 3. Re-Run & Verification of H42 Claims vs. Forensic Reality

### 3.1 ASR & Reference Transcript Forensics (`WS1`)
- **Verified Claims:** `tools/asr/benchmark_h42_asr.py` did run on CUDA `float16` across 10 configurations and confirmed `vad_filter=True` prevents 32-token silence hallucination on Video A (`11.76%` $\to$ `2.57%` WER).
- **Hidden Flaw 1 (Circular Ground Truth):** Comparing `artifacts/h42/benchmark/h42_video_b_locked_benchmark.json` against `runtime/youtube/y8tFSuOMAqQ/transcript.json` and `h42_asr_experiment_results.json` confirms `video_b_ref === base.en_beam1` (both `full_text` and all 31 segment strings match `100%`). Video A `base.en` segments 0–2 also match `h42_video_a_locked_benchmark.json` verbatim. Thus `0.00% WER` on Video B is an artifact of comparing a model against its own output.
- **Hidden Flaw 2 (Real ASR Errors in Locked Transcript):** Visual caption / context inspection already reveals ASR transcription mistakes in `h42_video_b_locked_benchmark.json`:
  - Segment B16: `"future films"` (actual speech: `"feature films"`) — propagates directly into an erroneous fronted `FUTURE` sign.
  - Segment B25: `"seen by scene"` (actual speech: `"scene by scene"`) — propagates into `SEE`.
  - Segment B2: `"maybe you even gone out"` (dropped `'ve` / `have`).
- **Hidden Flaw 3 (Inconsistent Segment Counts):** Cached `runtime/youtube/MXKkXXYUxBc/transcript.json` has `30` segments in `0:00-2:00`, while `h42_video_a_locked_benchmark.json` has `29` segments.

### 3.2 Semantic Engine & Translation Forensics (`WS2` / `WS3`)
- **Dead ISR Integration:** `EnglishToISLTranslator.js` line 1908 calls `this.semanticEngine.parseUtterance(source_text)` and appends a trace line + `intermediate_semantic_representation: isr` in the return payload, **but zero translation rules read `isr`**.
- **Unresolved Tokens in `SemanticUnderstandingEngine.contextualLexicon`:** Defines glosses `TOO_MUCH`, `CREATE`, `DOCUMENTARY`, `PERSON`, `FILM`, `SUPPORT` that do not exist in `signs/` or `EnglishToISLTranslator.motionCatalog`.
- **Lexicon Targets Missing from Disk/Catalog:**
  - `hello -> GREETING` (missing in `motionCatalog` & `signs/`).
  - `himself -> HE`, `herself -> SHE` (missing in `motionCatalog` & `signs/`).
- **Severe Lexical Mistranslations Found in `EnglishToISLTranslator.lexicon` (1,667 entries):**
  - `['evening', 'MORNING']` (line 1107 — exact opposite; broke Video B Seg 22 `"rest of the evening"` $\to$ `REST MORNING`).
  - `['eight', 'ONE']`, `['nine', 'ONE']`, `['third', 'ONE']` (lines 1104–1106 — corrupts numbers into `ONE`).
  - `['wind', 'TREE']` (line 1102).
  - `['yesterday', 'TIME']` (despite `signs/yesterday.json` existing in catalog!).
  - `['back', 'PAST']` (corrupts `"back of your mind"` $\to$ `PAST`).
  - `['right', 'TRUE']` (corrupts spatial/discourse `"right"`).
  - `['get', 'HAVE']`, `['getting', 'HAVE']`, `['gotten', 'HAVE']` (causes false aspectual `FINISH` in B27).
  - `['kind', 'SAME']`, `['things', 'ALL']`, `['something', 'ONE']`.
- **Meaning-Destroying "Grammar Omissions":**
  - Adding `without`, `because`, `but`, `out`, `down`, `up` to `auxiliaries` silently deletes critical semantic operators while inflating `meaningful_coverage_pct` to `100%`. Example (B7): *"without completely overcomplicating"* $\to$ `ALL CONFUSED` (opposite meaning).
- **Syntax & Scope Defects in Locked Video Outputs:**
  - **Cross-clause negation bleeding (B3, B20):** `NOT` from Clause 1 is moved after an affirmative Clause 2 (B20: *"I don't know what I'm up to today, but I do know..."* $\to$ `... I KNOW THAT HOUR DO NOT`).
  - **Double negation leakage (B13):** *"isn't that you don't know"* $\to$ `... YOU NOT KNOW THAT NOT`.
  - **Bogus `FINISH` aspect trigger (B27):** *"getting because it looks cool"* (`getting -> HAVE` + `looks -> LOOK`) $\to$ `COOL LOOK FINISH`.
  - **Fingerspelling dropped from playback (`A10`, `A11`, `A16`, `A17`):** `DAVID`, `JP`, `PHILLIPS`, `TEDX`, `ORACLE`, `GOOGLE`, `DISNEY` appear in `fingerspelled_terms` only; `gloss_sequence` and `sign_ids` contain zero fingerspelling cues, so the avatar omits every proper name.

### 3.3 Sign Library & Viewer Preload Forensics (`WS4`)
- **Total Files Validated:** 596 JSON files in `signs/`, matching `signs/manifest.json`.
- **Rotation Duplication Discovery:**
  - Unique rotation-only trajectories: **463 / 596** (133 duplicates).
  - Unique rotation + finger-curl trajectories: **491 / 596**.
  - **14 duplicate rotation clusters**, led by a **64-sign cluster** (`action`, `attention`, `bad`, `body`, `build`, `camera`, `challenge`, `change`, `class`, `clean`, `clear`, `dark`, `different`, `easy`, `fast`, `fear`, `finish`, `gesture`, `great`, `happy`, `hard`, `heart`, `hold`, `important`, `lesson`, `level`, `light`, `mean`, `meet`, `minute`, `move`, `music`, `number`, `open`, `pace`, `picture`, `practice`, `presentation`, `problem`, `public`, `put`, `read`, `ready`, `remember`, `same`, `school`, `screen`, `share`, `skill`, `slow`, `small`, `stage`, `stand`, `story`, `system`, `teacher`, `today`, `tree`, `try`, `video`, `week`, `world`, `write`, `year`) + clusters of `20`, `14`, `11`, `11`, `9`, and smaller pairs (`two`/`three`/`five`, `twenty`/`thirty`, `fourth`/`fifth`, `road`/`street`, `during`/`while`).
- **Blanket Metadata Provenance:** All 596 files declare `"organization": "ISLRTC"`, even when motions are identical developer templates (`action` == `bad` == `camera` == `happy`).
- **Motion Unit Mismatch (Radians vs Degrees — `DEF-H43-011`):** `SignAnimationPlayer.js:66,278` converts all `rotations` and `finger_curls` using `Math.PI / 180` (assuming degrees). However, **401 / 596 signs (67.3%)** store `rotations` in radians (`maxRot < 5`, e.g., `0.4`–`1.6`), resulting in `< 1.6°` micro-twitches instead of visible arm trajectories; **323 / 596 signs (54.2%)** store normalized `finger_curls` (`0..1.5` instead of `0..85°`).
- **Bimanual Finger Curl Drop (`DEF-H43-012`):** `SignAnimationPlayer.js:280` looks up `this.handRig[domSide]`, which is `undefined` when `dominant_hand === 'both'`, silently dropping `finger_curls` across **324 bimanual signs**.
- **Live Viewer Preload Cutoff (46 Signs Unplayable at Runtime):** `tools/avatar_viewer/index.html` line 1075 hardcodes 550 sign IDs in `signLibrary.preload([...])`. `SignLibrary.getPlayable()` throws `NOT_PRELOADED` for any uncached sign. All 46 signs added in H37, H38, H41, and H42 fail at runtime in the live viewer.

### 3.4 Real-Browser Visual QA, Synchronization & Recording Forensics (`WS5` / `WS6`)
Independent CDP probing and visual inspection of `artifacts/h42/` images and MP4s revealed:
- **MP4 Encoding Verified, Content Invalid:**
  - `h42_video_a_recording.mp4`: `10.88s`, 272 frames, `1584x714`, `h264_nvenc` (NVENC verified, duration only ~11s, not continuous 120s).
  - `h42_video_b_recording.mp4`: `3.76s`, 94 frames, `1584x714`, `h264_nvenc`.
- **Iframe Blocked on YouTube (`isl-aether-iframe` Blank):** CDP `Page.getFrameTree` confirms `isl-aether-iframe` remains at `url: "about:blank"` inside YouTube (`https://www.youtube.com/watch?...`), while `overlay.js` hides `#isl-aether-fallback`. A direct fetch/PNA test from YouTube context hung indefinitely due to Chrome's cross-scheme / Local Network Access gating between `https://www.youtube.com` and `http://localhost:8000`, AND `overlay.css` emitted `Unsafe attempt to load URL chrome-extension://.../content/overlay.css`.
- **Direct Viewer Load Latency:** Even in a standalone tab (`http://localhost:8000/tools/avatar_viewer/index.html?embed=1`), initial load takes **~10.5 seconds** due to Three.js CDN + 550 sequential batch fetches + 2.8 MB FBX parsing.
- **Ad & Clock Failures in Audit Script:**
  - `video_a/segment_010/frame_mid.png` shows a Coursera Sponsored Ad (`0:01 / 0:10`).
  - `video_b/segment_011/frame_mid.png` shows the video paused at `0:02 / 12:01` (Segment 0 captions) because `h42_dual_benchmark_results.json` omitted `start`/`end`/`duration`, causing every seek to go to `0s`.
  - No YouTube translation job was ever triggered in `run_h42_dual_visual_audit.mjs`.
  - `h42_dual_avatar_full_body.png` cropped `350x560` at `(910, 80)`, capturing YouTube's **Coursera ad recommendation card** instead of the avatar.

---

## 4. H43 Reproducible Baseline Target

H43 establishes an honest, decoupled baseline moving forward:
- **Code Tests Passing (Existing Technical Baseline):** 76/76 unit tests, 8/8 edge-case tests, 596/596 JSON schema valid.
- **Verified Distinct Motion Assets:** 463 unique rotation patterns (not 596 distinct signs).
- **Verified Live Viewer Preload:** 550 signs (46 missing from preload).
- **Verified Real-Browser YouTube Avatar Visibility:** **FAIL (0% visible in embedded YouTube overlay)** prior to H43 remediation.
- **Verified Independent ASR Reference:** **0 independently human-verified references** prior to H43.
- **Deaf-Community Validation:** `PENDING_DEAF_COMMUNITY_REVIEW`.
