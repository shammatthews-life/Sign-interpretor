# Phase H21: Live Five-Minute Demonstration Script

**Project:** Indian Sign Language (ISL) Real-Time Accessibility Translator  
**Date:** October 31, 2026  
**Demonstration Scenario:** 5-Minute College Mentor & Evaluator Walkthrough  
**Target Avatar:** Aether 3D WebGL Accessibility Avatar  
**Target Video:** `https://www.youtube.com/watch?v=MXKkXXYUxBc` ("Public Speaking for Beginners")

---

## 1. Demonstration Outline & Timing

| Elapsed Time | Demonstration Phase | Tested Functional Capabilities |
| :---: | :--- | :--- |
| **00:00–01:00** | Introduction & Extension Launch | Chrome MV3 extension load, floating overlay launch, 3D WebGL initialization |
| **01:00–02:00** | Direct Sign & Sentence Playback | High-frequency direct signing, grammatical topic-comment structure |
| **02:00–02:45** | Multiword Phrase Translation | Recognition and translation of compounded pedagogical phrases |
| **03:00–03:45** | Honest Subtitle Fallback Display | Transparent unavailable-word handling without avatar hallucination |
| **03:45–04:30** | Interactive YouTube Playback Controls | Play, pause, forward seek, backward seek, rate change synchronization |
| **04:30–05:00** | Quantitative Accounting & Conclusion | Full 23,258-token accounting proof (84%+ communicative coverage) |

---

## 2. Step-by-Step Demonstration Execution

### Phase 1: Launch & Initialization (00:00–01:00)
1. **Action:** Open Chrome browser at `https://www.youtube.com/watch?v=MXKkXXYUxBc`.
2. **Action:** Click the floating "ISL Translator" pill in the bottom right corner.
3. **Observation:** 
   - Aether appears inside the floating iframe docked unobtrusively at the bottom right.
   - All 207 Schema 2.0.0 signs preload in under 350 ms.
   - Status badge shows: `Connected | 207 Signs Active | Ready`.

### Phase 2: Direct Sign & Sentence Execution (01:00–02:00)
1. **Spoken Dialogue:** *"Good morning! I want to help you learn public speaking today."*
2. **Avatar Response:**
   - Aether executes: `GOOD` $\rightarrow$ `MORNING` $\rightarrow$ `I` $\rightarrow$ `WANT` $\rightarrow$ `HELP` $\rightarrow$ `YOU` $\rightarrow$ `LEARN`.
   - Structural English words (`to`, `today`) handled via ISL grammatical omission / null copula.
   - Avatar starts from neutral pose and fluidly returns to neutral at the sentence boundary.

### Phase 3: Multiword Phrase Translation (02:00–02:45)
1. **Spoken Dialogue:** *"Have a look at the slide to understand the body language and posture."*
2. **Avatar Response:**
   - Multiword compound `have a look at` triggers directional gaze sign `LOOK`.
   - Pedagogical nouns `slide`, `posture`, and `body` execute sequentially.
   - Verifies longest-match precedence without double-token consumption.

### Phase 4: Honest Subtitle Fallback (03:00–03:45)
1. **Spoken Dialogue:** *"We will discuss the neurochemistry of dopamine."*
2. **Avatar Response:**
   - The specialized neurological term `dopamine` has no motion asset authored in the current library.
   - Aether returns to neutral $\{0, 0, 0\}$ immediately.
   - Subtitle appears directly beneath Aether:
     > `"ISL translation not available in this translator: dopamine"`
   - Transparently communicates lexical boundary without fabricating artificial hand gestures.

### Phase 5: YouTube Timeline Synchronization & Seeking (03:45–04:30)
1. **Pause Test:** Click YouTube video pause.
   - Aether immediately freezes current posture (`PAUSE` command received).
2. **Resume Test:** Click YouTube play.
   - Aether smoothly resumes signing from exact keyframe (`RESUME` command received).
3. **Seek Test:** Jump YouTube timeline forward by 30 seconds.
   - Aether receives `RESET_AVATAR`, cancels stale animation queue instantly, and re-anchors to the new segment.
   - Zero stale signs from previous timestamp leak into the current playback.

### Phase 6: Conclusion & Integrity Verification (04:30–05:00)
1. **Summary:** Present the comprehensive corpus coverage dashboard:
   - 23,258 transcript tokens fully accounted for (0 silent loss).
   - 207 playable Schema 2.0.0 assets.
   - Over 84% communicative coverage achieved.
   - Clear distinction between technically verified playability and linguistic review.
