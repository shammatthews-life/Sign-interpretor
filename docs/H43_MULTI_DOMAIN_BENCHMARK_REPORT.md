# H43 — Multi-Domain Benchmark & Linguistic Evaluation Report (WS5)

**Status:** COMPLETE (`PENDING_DEAF_COMMUNITY_REVIEW` for all linguistic claims)  
**Scripts:** `tools/asr/build_h43_references.py`, `tools/test_h43_multi_domain_evaluation.mjs`  
**Artifacts:** `artifacts/h43/benchmark/h43_multi_domain_references.json`, `artifacts/h43/benchmark/h43_linguistic_challenge_dataset.json`, `artifacts/h43/benchmark/h43_multi_domain_evaluation.json`

---

## 1. Expanded Multi-Domain Evaluation Corpus (`0:00–2:00` Windows)
Retained locked H42 Videos A & B for regression tracking and added 3 distinct real-world domains backed by official creator/human VTT subtitles:

| Video ID | Title / Topic | Domain / Accent | Reference Source | Words |
|---|---|---|---|---:|
| `MXKkXXYUxBc` (A) | Public Speaking for Beginners | Tutorial / Scandinavian-EN | Human-audited caption revision | 272 |
| `y8tFSuOMAqQ` (B) | How to Vlog as a Beginner | Conversational / North-American-EN | Human-audited caption revision | 539 |
| `xrwz9IxpMJg` (C) | IIT/NPTEL Robotics Lecture 01 | Academic STEM / **Indian-English** | Official human VTT subtitles | 213 |
| `aircAruvnKk` (D) | 3Blue1Brown: But what is a neural network? | Technical Math / ML | Official human VTT subtitles | 378 |
| `D9Ihs241zeg` (E) | Chimamanda Ngozi Adichie: Danger of a Single Story | Literary Storytelling / Nigerian-EN | Official human VTT subtitles | 289 |

---

## 2. Multi-Layer Decoupled Scoring Summary
### Layer 1–3: 44-Case Linguistic Challenge Suite (`h43_linguistic_challenge_dataset.json`)
- **Pass Rate:** **44 / 44 (`100.0%`)**
- Categories verified: clause-isolated negation (`6/6`), auxiliary contraction negation without doubling (`5/5`), discourse operators `without/because/but/or/why/if/already/maybe/also` (`8/8`), perfective `FINISH` vs progressive/obligation/possessive (`5/5`), repaired lexicon homographs & ordinals (`8/8`), playable `fs_<word>` fingerspelling & non-fabricated unknowns (`4/4`), ASR stutter deduplication & confidence propagation (`4/4`), multi-domain vocabulary (`4/4`).

### Layer 4: Five-Video Reference & End-to-End `small.en_b5_norm` Results
| Video | Ref Playable Signs (`lex` + `fs`) | Ref Concept Resolution | Ref Unk | E2E `small.en_b5_norm` WER | E2E Playable Signs (`lex` + `fs`) | E2E Concept Res | E2E Disk Playability |
|---|---:|---:|---:|---:|---:|---:|---:|
| `MXKkXXYUxBc` (A) | 185 (`178` + `7`) | 100.00% | 0 | 4.36% | 184 (`177` + `7`) | 97.35% | **100.0%** |
| `y8tFSuOMAqQ` (B) | 371 (`371` + `0`) | 100.00% | 0 | 2.97% | 356 (`356` + `0`) | 99.72% | **100.0%** |
| `xrwz9IxpMJg` (C) | 113 (`113` + `0`) | 86.92% | 17 | 4.23% | 115 (`115` + `0`) | 87.79% | **100.0%** |
| `aircAruvnKk` (D) | 189 (`189` + `0`) | 74.70% | 64 | 3.15% | 189 (`189` + `0`) | 74.41% | **100.0%** |
| `D9Ihs241zeg` (E) | 151 (`148` + `3`) | 74.75% | 51 | 3.45% | 147 (`144` + `3`) | 74.62% | **100.0%** |

*Honesty Note:* Lower concept resolution (`74.7%–86.9%`) on unseen academic ML, robotics, and literary domains reflects genuine uncovered specialized vocabulary (`ginger`, `beer`, `28x28`, `sloppily`, `robota`, `servant`), which is reported honestly under `unknown_terms` rather than hidden via placeholder synonyms. Linguistic naturalness and Deaf-community acceptability across all outputs remain `PENDING_DEAF_COMMUNITY_REVIEW`.
