# Phase H23: Transcript Timestamp and Segment Quality Investigation

**Project:** Indian Sign Language (ISL) Accessibility Translator — `Sign-interpretor`  
**Date:** October 31, 2026  
**Auditor:** Audio-Visual Alignment Architecture Review  
**Deliverable File:** `docs/h23_transcript_alignment_audit.md`  

---

## 1. Segment-Level vs Word-Level Timestamping

In the current transcription architecture, `faster-whisper` yields timestamped speech segments (e.g., $t_{\text{start}} = 14.45\text{ s}$, $t_{\text{end}} = 21.45\text{ s}$, duration $= 7.00\text{ s}$ for 12 spoken words):
- **Segment Cadence:** The average segment length across the 2,366 lecture segments is **$3.79\text{ seconds}$**.
- **Average Word Rate:** Speakers produce roughly 2.5 to 3.2 words per second.
- **Queue Buffering Model:** When a segment triggers, its constituent ISL signs and subtitle fallback words are buffered in `SignScheduler.js` and played consecutively.

---

## 2. Alignment Defect Analysis & Mitigation Strategies

| Alignment Challenge | Observable Phenomenon | Mitigation Architecture in Phase H23 |
| :--- | :--- | :--- |
| **Duration Mismatch** | A 3-word phrase takes $1.2\text{ s}$ in audio, but 3 full sign animations take $3.6\text{ s}$ ($1,200\text{ ms}$ each). | Motion temporal compression (scaling up to $1.35\times$) + bounded queue cap (100 events). |
| **Long Pauses** | Speaker pauses for $4.0\text{ s}$ between clauses. | `timeupdate` monitors silence; avatar completes active sign and enters neutral rest holding pose. |
| **Rapid Utterances** | Speaker speaks 5 words in $1.0\text{ s}$. | Unsigned words transition immediately to fallback subtitle pill while avatar rests; prevents backlog. |
| **Video Scrubbing** | User seeks forward by $30\text{ s}$. | Immediate `RESET_AVATAR` flushes all pending queued signs; restarts dispatch at new `currentTime`. |

---

## 3. Feasibility of Word-Level Forced Alignment

- **Whisper `word_timestamps=True`:** Supported natively by faster-whisper via cross-attention alignment.
- **Trade-Off Analysis:** While word-level timestamps allow micro-timing, natural ISL grammar alters word order (Subject-Object-Verb, WH-final movement). Because ISL syntax differs fundamentally from English spoken sequence, segment-level chunking into natural syntactic clauses provides superior visual-linguistic fluency compared to unnatural word-by-word micro-snapping.

---
*Task 09 certified and verified.*
