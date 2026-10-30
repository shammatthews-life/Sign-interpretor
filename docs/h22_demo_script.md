# Phase H22: Five-Minute Live Demonstration Script for College Mentor

**Project:** Indian Sign Language (ISL) Real-Time Accessibility Translator  
**Date:** October 31, 2026  
**Audience:** College Project Evaluator / Final-Year Mentor  
**Presenter:** Project Developer  
**Deliverable File:** `docs/h22_demo_script.md`  

---

## Demonstration Schedule (5 Minutes Total)

### Minute 1: Introduction & Architecture Walkthrough (0:00 – 1:00)
- **Action:** Open Chrome with the unpacked extension loaded. Show the YouTube video page (`https://www.youtube.com/watch?v=MXKkXXYUxBc`).
- **Talking Points:**
  - *"Welcome, Professor. Today I am demonstrating our Indian Sign Language Accessibility Translator. Our system operates as a Chrome Manifest V3 extension paired with a high-performance 3D WebGL avatar named Aether, running locally at 60 FPS."*
  - *"We have mapped all 23,258 spoken tokens from this 2.5-hour lecture with 100.0% accounting and zero silent token loss."*
  - *"Our library contains 207 authentic signs referencing the Government of India's ISLRTC official dictionary."*

---

### Minute 2: Fully Supported Sign Playback (1:00 – 2:00)
- **Action:** Start video playback at $t = 14.0\text{ s}$ ("and bring you a few steps closer to being more confident, more clear").
- **Talking Points:**
  - *"Observe how Aether immediately recognizes high-frequency signs like 'you', 'step', and 'confident'. Note the smooth transitions from neutral rest and accurate two-handed coordination."*

---

### Minute 3: Honest Fallback Subtitle & Grammar Omission (2:00 – 3:00)
- **Action:** Play segment containing specialized jargon or unsupported terms (e.g., $t = 118.0\text{ s}$, mentioning "SQL Server QUIK" or proper nouns).
- **Talking Points:**
  - *"Notice our ethical accessibility standard: when an unsupported word occurs, Aether smoothly holds neutral rest rather than inventing a misleading gesture. Simultaneously, a clear subtitle pill appears directly below him stating 'ISL translation not available in this translator' showing the exact English text."*

---

### Minute 4: Two-Handed Fingerspelling & Multiword Phrases (3:00 – 4:00)
- **Action:** Demonstrate fingerspelling for proper nouns ("DAVID", "TED") and multiword compound translation ("take a look at", "facial expressions").
- **Talking Points:**
  - *"Unlike American Sign Language, ISL uses a two-handed manual alphabet where vowels point to specific fingers of the non-dominant hand. For educational phrases like 'have a look at', our system recognizes the entire compound and executes the single semantic sign for 'LOOK'."*

---

### Minute 5: Interactive Video Controls & Error Recovery (4:00 – 5:00)
- **Action:**
  1. Pause the video $\rightarrow$ avatar pauses immediately.
  2. Seek forward by 60 seconds $\rightarrow$ avatar queue purges instantly (`RESET_AVATAR`), eliminating ghost gestures, and repositions seamlessly.
  3. Increase playback speed to 1.5x $\rightarrow$ avatar animation accelerates proportionally.
- **Concluding Statement:**
  - *"Our system achieves 84.69% communicative coverage across the entire 2.5-hour lecture while rigorously preserving linguistic integrity. Thank you, and I look forward to your questions."*

---
