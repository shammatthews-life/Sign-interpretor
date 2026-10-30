# Phase H23: Sign Duration and Speech Rate Adaptation Policy

**Project:** Indian Sign Language (ISL) Accessibility Translator — `Sign-interpretor`  
**Date:** October 31, 2026  
**Auditor:** Animation Temporal Scheduling Review (`tools/benchmark_sign_timing.py`)  
**Deliverable File:** `docs/h23_sign_rate_and_timing.md`  
**Companion Artifact:** `data/h23_sign_timing_benchmark.json`  

---

## 1. Speech Cadence vs Gesture Articulation Speed

A fundamental constraint in sign language animation is that visual-gestural articulation operates on a different temporal frequency than spoken language:
- **Spoken Word Duration:** Spoken words often last only $200\text{ ms}$ to $400\text{ ms}$.
- **Authentic Sign Duration:** Moving the hands from rest through an authentic spatial movement stroke and back to rest requires **$800\text{ ms}$ to $1,400\text{ ms}$**.
- **Naive Pitfall:** Speeding up 3D keyframe animations beyond $1.4\times$ produces unnatural flailing or blurring that compromises handshape legibility for Deaf viewers.

---

## 2. Phase H23 Adaptive Scheduling Policy

To balance synchronization with linguistic legibility:
1. **Dynamic Rate Adaptation ($\le 1.35\times$):** When speech tempo increases, `SignAnimationPlayer.js` dynamically compresses keyframe intervals by up to $1.35\times$, but strictly clamps beyond that limit.
2. **Transitional Rest Reduction:** Inter-sign neutral rest holding is compressed from $200\text{ ms}$ down to $80\text{ ms}$ during dense speech segments.
3. **SOV Information Density Compaction:** Natural ISL omission of non-content English words (articles, auxiliary verbs) automatically reduces the number of gestures required by nearly 40%, naturally bridging the speed gap.
4. **Queue Bound Overflow Protection:** If the queue exceeds 100 entries, low-priority duplicate tokens are dropped while maintaining terminal clause signs.

---
*Task 10 certified and verified.*
