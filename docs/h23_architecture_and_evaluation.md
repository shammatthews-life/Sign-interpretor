# Phase H23: System Architecture, Theory, and Evaluation Thesis

**Project:** Indian Sign Language (ISL) Real-Time Accessibility Translator  
**Degree Track:** Final-Year Engineering Project Defense & Evaluation  
**Deliverable File:** `docs/h23_architecture_and_evaluation.md`  

---

## 1. Abstract
Automated accessibility tools for Deaf and Hard-of-Hearing individuals frequently rely on closed captions or text-based subtitles. However, for pre-lingually Deaf individuals in India, Indian Sign Language (ISL) is their primary visual-gestural mother tongue, possessing syntactic structures fundamentally distinct from written English. This project presents an end-to-end accessibility architecture that bridges spoken YouTube lecture audio to natural 3D Indian Sign Language synthesis. Operating via a Manifest V3 browser extension and a Three.js WebGL avatar ("Aether"), the system performs Subject-Object-Verb (SOV) grammatical reordering, WH-interrogative topicalization, multiword idiomatic compound recognition, and two-handed ISL fingerspelling. Across a canonical 2.5-hour lecture video (23,258 spoken tokens), the system achieves 84.69% communicative coverage (19,698 tokens) across 207 Schema 2.0.0 signs while preserving a transparent, non-hallucinating subtitle fallback for unverified concepts.

---

## 2. Problem Statement & Objectives
- **Problem Statement:** Standard YouTube automatic speech recognition generates English captions that reflect linear English grammar (Subject-Verb-Object), introducing substantial cognitive reading barriers for native Deaf signers whose language uses Subject-Object-Verb (SOV) spatial grammar.
- **Objectives:**
  1. Parse continuous YouTube audio into timestamped segments locally.
  2. Transform English grammatical syntax into authentic ISL gloss sequences.
  3. Render 3D skeletal animations on avatar Aether at 60 FPS without body mesh clipping.
  4. Implement an ethical fallback mechanism that refuses to invent gestures for unverified terms.
  5. Synchronize visual signing with video playback, including pause, resume, seek, and variable speed scaling.

---

## 3. Comprehensive Mentor Defense Q&A Preparation

### Q1: Why translate to ISL rather than ASL or BSL?
*Answer:* Indian Sign Language is the official visual-gestural language of India's Deaf community, recognized under the Rights of Persons with Disabilities Act (2016). ISL is linguistically distinct from American Sign Language (ASL)—for example, ISL uses a two-handed manual alphabet where vowels point to specific fingers of the non-dominant hand, and follows SOV word order. Using ASL would impose an alien foreign language on Indian Deaf viewers.

### Q2: How does the system handle words that don't have an authored sign?
*Answer:* Rather than hallucinating arbitrary gestures or freezing, the system employs an "Honest Subtitle Fallback": the avatar smoothly returns to neutral rest while a high-contrast subtitle pill displays `"ISL translation not available in this translator: [word]"` for 2,500 ms. This guarantees transparent, ethical accessibility.

### Q3: What is the purpose of the 207 Schema 2.0.0 JSON files?
*Answer:* Each JSON file encapsulates a high-precision skeletal animation clip conforming to our Schema 2.0.0 standard. It stores timestamped joint rotation Euler angles and finger curl percentages across Aether's 243-bone rig, guaranteeing strictly increasing timestamps and a `{ x: 0, y: 0, z: 0 }` neutral return.

### Q4: How is video synchronization maintained when the user seeks or pauses?
*Answer:* `ISLTimelineSynchronizer` listens to HTML5 `<video>` events (`timeupdate`, `seeked`, `ratechange`). Seeking immediately fires `RESET_AVATAR`, purging the 100-event queue in under 10 ms to eliminate ghost gestures, recalculating the segment index via binary search, and resuming signing from the new timestamp.

### Q5: Has the system received formal certification from Deaf native signers?
*Answer:* In accordance with scientific integrity, all 207 assets are cataloged as `IMPLEMENTATION_PENDING_LINGUISTIC_REVIEW`. They are mechanically verified and cite official ISLRTC dictionary entries, but we provide an external Deaf Reviewer Evaluation Package (`docs/h23_external_reviewer_package.md`) for formal certification prior to clinical deployment.

---
*Architecture and defense documentation complete.*
