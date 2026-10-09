# Phase G1 — Speech → Controlled Sign Sequence → Aether

## 1. Overview & Goal

Phase G1 implements our first integrated end-to-end speech-to-avatar prototype:

```
Microphone / Audio Source
         ↓
F1 AudioPipeline (16 kHz mono Float32 PCM, VAD)
         ↓
F2.5 FasterWhisperBackend (RTX 4050 CUDA float16, decoupled worker)
         ↓
Partial & Final Transcript Events
         ↓
SpeechSignOrchestrator
         ↓
SentenceProcessor (Token / Phrase Parsing)
         ↓
Safe Prefix Commit Policy & Playability Filtering
         ↓
SignScheduler (Incremental Queuing)
         ↓
Aether 3D Avatar (Three.js WebGL Player)
```

**Scope Limitation**:
This prototype performs **Speech → Controlled English Sign Mapping → Aether**. It is **NOT** yet natural English → ISL grammatical translation.

---

## 2. Core Architecture: `SpeechSignOrchestrator`

The orchestrator ([`tools/avatar_viewer/SpeechSignOrchestrator.js`](file:///d:/sign%20interpretor/tools/avatar_viewer/SpeechSignOrchestrator.js)) acts as the decoupled bridge between ASR events, sentence processing, and the sign motion queue.

### Responsibilities:
1. Ingests streaming `PARTIAL_TRANSCRIPT` and `FINAL_TRANSCRIPT` events without coupling Whisper to the avatar or renderer.
2. Manages incremental prefix commitments so that already-enqueued signs are never duplicated.
3. Queries [`SignLibrary`](file:///d:/sign%20interpretor/tools/avatar_viewer/SignLibrary.js) for playability: filters unknown words and blocks `MOTION_INCOMPLETE` signs (e.g., `WATER`).
4. Enqueues verified signs into [`SignScheduler`](file:///d:/sign%20interpretor/tools/avatar_viewer/SignScheduler.js).
5. Measures end-to-end timing ($T_0 \to T_1 \to T_2 \to T_3 \to T_4$) and backpressure.

---

## 3. Duplicate Prevention & Stable Prefix Commit Policy

### Problem
Whisper decodes overlapping rolling windows during speech. If every partial triggered sign queuing, a phrase like `"hello good morning"` would enqueue `HELLO`, then `HELLO` + `GOOD`, then `HELLO` + `GOOD` + `MORNING`, repeating signs multiple times.

### Deterministic Commit Policy
1. **Committed Counter**: The orchestrator tracks `committedSigns.length`. Only new candidate signs beyond this index are evaluated.
2. **Stable Prefix Commitment**:
   - In a `PARTIAL_TRANSCRIPT` event, candidate signs corresponding to words that are **followed by subsequent words** in the transcript are classified as a confirmed, stable prefix.
   - These stable prefix signs are committed immediately ($0$ extra latency) to `SignScheduler` so Aether begins playing the start of the sentence while trailing words are still being spoken.
3. **Trailing Word Confirmation**:
   - The trailing sign (corresponding to the last word of an in-flight partial) may still be incomplete or unstable.
   - It is only committed if observed across $\ge 2$ consecutive decodes, after a stability delay ($\ge 250\text{ ms}$), OR the moment a subsequent word arrives.
4. **Final Flush**:
   - Upon receiving a `FINAL_TRANSCRIPT` event (speech pause or utterance end), all remaining candidate signs are committed immediately.

### Verification Result
In stress testing with 5 rapidly overlapping/repeated partials (`"hello"`, `"hello good"`, `"hello good morning"`, `"hello good morning"`, `"hello good morning"`):
- Exactly 3 signs were enqueued: `HELLO`, `GOOD`, `MORNING`.
- Duplicate enqueues: **0**.

---

## 4. End-to-End Latency Instrumentation

The pipeline tracks milestones across the entire speech-to-signing lifecycle:
- **$T_0$**: Audio enters system (first chunk timestamp).
- **$T_1$**: First partial transcript emitted by ASR.
- **$T_2$**: First sign safely committed by orchestrator.
- **$T_3$**: First sign enqueued into scheduler.
- **$T_4$**: Aether begins WebGL sign playback.

### Measured Latencies:
- **First Partial Latency ($T_1 - T_0$)**: $\sim 800\text{–}1107\text{ ms}$.
- **Speech $\to$ Sign Commit Latency ($T_2 - T_0$)**: $\sim 1107\text{ ms}$.
- **Scheduler Enqueue Overhead ($T_3 - T_2$)**: $< 0.1\text{ ms}$.
- **Speech $\to$ Aether Playback Start ($T_4 - T_0$)**: $\sim 1107\text{ ms}$.

Because `HELLO` starts signing while `good morning` is still being spoken, the avatar appears responsive without waiting for full sentence finalization.

---

## 5. Fast Speech & Backpressure Measurement

When a speaker talks faster than Aether signs (signing takes $\sim 1700\text{–}2000\text{ ms}$ per sign):
- The `SignScheduler` queue smoothly buffers the incoming signs.
- **Queue Count**: Captured and exposed via `getDiagnostics()`. In fast-speech bursts, queue count reached 2.
- **Queue Age**: Oldest queued sign wait time tracked in real-time.
- **Stream Lag**: Fast speech fixture ($5500\text{ ms}$) completed end-to-end processing in $5654\text{ ms}$ (lag of only $154\text{ ms}$).
- Aether continues signing sequentially without reset or frame dropping.

---

## 6. Safety: Unknown Words & Incomplete Signs

Tested with inputs containing unmapped words and incomplete motions (`"hello water smartphone morning"`):
- **Unknown Words**: `'SMARTPHONE'` reported cleanly in `unknownWords`. Zero hallucinated motions.
- **MOTION_INCOMPLETE**: `'water'` flagged as `unavailableSigns` (motion status: incomplete in `signs/water.json`). Zero unverified motions enqueued.
- **Playable**: Only `'hello'` and `'morning'` reached Aether's scheduler.

---

## 7. Verification Test Suite

All tests passed with zero regressions:
1. `tools/validate_sign_library.py`: **PASSED**
2. `tools/validate_phase_f2_asr.py`: **PASSED**
3. `tools/validate_phase_f1_audio.mjs`: **PASSED**
4. `tools/validate_phase_b_hello.mjs`: **PASSED**
5. `tools/validate_phase_c_library_scheduler.mjs`: **PASSED**
6. `tools/validate_phase_d_authoring.mjs`: **PASSED**
7. `tools/validate_phase_e2_good.mjs`: **PASSED**
8. `tools/validate_phase_e3_morning.mjs`: **PASSED**
9. `tools/validate_sentence_pipeline.mjs`: **PASSED**
10. `tools/validate_speech_sign_orchestrator.mjs`: **PASSED** (Unit tests for orchestrator logic)
11. `tools/validate_phase_g1_pipeline.mjs`: **PASSED** (End-to-end integration test)
12. `tools/asr/test_phase_g1_live_audio.py`: **PASSED** (WAV fixture verification)
13. `git diff --check`: **PASSED**
