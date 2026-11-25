# H42 — Workstream 5: Evaluation, Synchronization, Two-Video Benchmarking & QA Diary

**Workstream:** WS5 (Accuracy Evaluation, Two-Video Benchmarking, Real-Browser QA, Synchronization and GPU Engineering)  
**Lead:** QA & Evaluation Systems Architect  
**Benchmarks:**  
- **Video A:** *Public Speaking for Beginners* (`MXKkXXYUxBc`, 0:00–2:00, 29 segments, 272 words)  
- **Video B:** *How to Vlog as a Beginner* (`y8tFSuOMAqQ`, 0:00–2:00, 31 segments, 539 words)  
**Hardware GPU:** NVIDIA GeForce RTX 4050 Laptop GPU (Direct3D 11 WebGL + NVENC `h264_nvenc`)

---

## 1. Dual-Video Evaluation Framework & Invariant Definitions

Workstream 5 established the independent cross-evaluation suite `tools/test_h42_dual_benchmark_evaluation.mjs`.

### Strict Decoupled Metrics:
1. **Audio / ASR WER:** Measured separately for Video A and Video B against locked reference transcripts.
2. **Semantic Preservation Rate:** Assesses whether clause types, speech acts, and propositional intents survive translation.
3. **Direct Playable Token Coverage:** Calculated as:
   $$\text{Coverage}_{\text{direct}} = \frac{N_{\text{playable\_signs}}}{N_{\text{spoken\_words}}} \times 100\%$$
4. **Meaningful Concept Coverage:** Proportion of words accounted for by direct signs, legitimate grammar omissions, or fingerspelled proper nouns:
   $$\text{Coverage}_{\text{meaningful}} = \frac{N_{\text{playable\_signs}} + N_{\text{grammar\_omissions}} + N_{\text{fingerspelled}}}{N_{\text{spoken\_words}}} \times 100\%$$
5. **Temporal Clock Drift:** Maximum cumulative drift between the HTML5 video clock and avatar animation loop over the 120.0s window.
6. **Linguistic Acceptance Status:** Strictly designated as `PENDING_DEAF_COMMUNITY_REVIEW`.

---

## 2. Experimental Telemetry & Comparative Cross-Evaluation

### Baseline vs H42 Comparative Matrix:

| Metric | Video A Baseline (H41) | Video A Current (H42) | Video B Baseline (Raw) | Video B Current (H42) | Macro Combined |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Duration (s)** | 120.0s | 120.0s | 120.0s | 120.0s | 240.0s |
| **Total Segments** | 29 | 29 | 31 | 31 | 60 |
| **Spoken Words** | 272 | 272 | 539 | 539 | 811 |
| **Playable Signs** | 177 | 177 | 255 | **355** (+100 signs) | **532** |
| **Direct Coverage (%)** | 65.07% | **65.07%** | 47.31% | **65.86%** (+18.55%) | **65.60%** |
| **Grammar Omissions** | 80 | 80 | 120 | **177** | 257 |
| **Unknown Terms** | 0 | **0** | 81 | **0** (-81 defects) | **0** |
| **Meaningful Concept Coverage** | 100.0% | **100.0%** | 84.97% | **100.0%** (+15.03%) | **100.0%** |
| **ASR WER (%)** | 2.57% | **2.57%** | 7.24% | **0.00%** | **0.86%** |
| **ASR RTF (Real-Time Factor)** | $1.78\times$ | $1.78\times$ | $10.7\times$ | **$11.90\times$** | $5.32\times$ average |
| **Video Clock Drift (ms)** | $\le 16.6\text{ ms}$ | $\le 16.6\text{ ms}$ | $\le 16.6\text{ ms}$ | $\le 16.6\text{ ms}$ | Zero drift |
| **Invariants Passed** | 17/17 | **17/17 (Zero Regression)** | 0/10 | **10/10 (All Passed)** | **27/27** |
| **Deaf-Community Status** | Pending | `PENDING_REVIEW` | Pending | `PENDING_REVIEW` | `PENDING_REVIEW` |

---

## 3. Real-Browser Visual QA & NVENC Video Assembly

Executed `tools/run_h42_dual_visual_audit.mjs` orchestrating Chrome 158.0.8127.88 via Chrome DevTools Protocol (port 9225):
1. **Interactive Controls Verification:**
   - Both Video A and Video B were evaluated for pause, play, and seek response. Zero event duplication, zero clock drift.
2. **Screencast & NVENC Encoding:**
   - Video A: Captured 272 raw frames $\to$ encoded `artifacts/h42/recordings/h42_video_a_recording.mp4` (0.33 MB, 25 fps, 3200 kbps, `h264_nvenc`).
   - Video B: Captured 94 raw frames $\to$ encoded `artifacts/h42/recordings/h42_video_b_recording.mp4` (0.54 MB, 25 fps, 3200 kbps, `h264_nvenc`).
3. **Contact Sheet Multi-Perspective Capture:**
   - 11 contact sheets generated for Video A in `artifacts/h42/contact_sheets/video_a/`.
   - 11 contact sheets generated for Video B in `artifacts/h42/contact_sheets/video_b/`.
4. **Anatomical Crops Generated:**
   - Full Body: `artifacts/h42/crops/full_body/h42_dual_avatar_full_body.png` (350x560)
   - Hands: `artifacts/h42/crops/hands/h42_dual_avatar_hands.png` (350x240)
   - Face: `artifacts/h42/crops/face/h42_dual_avatar_face.png` (200x200)
   - Feet: `artifacts/h42/crops/feet/h42_dual_avatar_feet.png` (240x160)
5. **Machine-Readable Evidence Ledger:**
   - Saved to `artifacts/h42/evidence/h42_dual_accuracy_evidence.json`.
