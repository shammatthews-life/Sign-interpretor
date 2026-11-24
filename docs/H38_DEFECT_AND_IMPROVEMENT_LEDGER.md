# H38 — Defect & Improvement Ledger

**Milestone:** H38 (Autonomous Single-Video Perfection & Cross-Language Sign Discovery)  
**Target Video:** [Public Speaking for Beginners – Free Full Course | Speak with Confidence](https://www.youtube.com/watch?v=MXKkXXYUxBc) (`MXKkXXYUxBc`)  
**Locked Benchmark Segment:** `0:00 – 2:00` (120.0s, 29 segments, 272 words)  

---

## Defect Classification Scheme
- **Critical (P0):** Semantic reversal, false negation, corrupted grammatical clause structure, or pipeline crash.
- **High (P1):** Dropped numeric data, distorted interrogative syntax, unhandled discourse markers, or key concept omission.
- **Medium (P2):** Missing core vocabulary in sign library requiring synonym approximation or fingerspelling.
- **Low (P3):** Pacing or transition roughness, subtle framing margins.

---

## Defect Inventory & Engineering Resolutions

| Defect ID | Description | Severity | Category | Root Cause | Status | Verification Evidence |
| :---: | :--- | :---: | :---: | :--- | :---: | :--- |
| **D38-01** | `manifest.json` out of sync with `signs/` filesystem (570 in manifest vs 577 in directory) | High | Library | 7 new signs authored in H37 (`three`, `day`, `all`, `make`, `before`, `five`, `thousand`) were not appended to `manifest.json` | **CLOSED** | Ran `sync_and_validate_signs_manifest.mjs`; manifest updated to v2.5.0 with 586 valid signs |
| **D38-02** | Catastrophic Negation Misplacement in Segment 10 ("if we haven't met before, my name is David") | Critical | Linguistics | Clause-final negation rule moved `NOT` to end of entire compound sentence (`BEFORE HEY WE HAVE MEET MY NAME NOT`), negating speaker's name rather than subordinate clause | **CLOSED** | Implemented `ISL-CLAUSE-NEG-01`; `NOT` placed right before `MY NAME`: `BEFORE HEY WE MEET NOT MY NAME` |
| **D38-03** | Erroneous Interrogative WH-Placement on Relative Clause in Segment 04 ("What you're about to watch is a special compilation...") | High | Linguistics | `ISL-WH-FINAL` rule mechanically moved "what" to end of sentence (`... WATCH WHAT`), turning a declarative statement into a question | **CLOSED** | Implemented `ISL-REL-CLAUSE-01` disambiguating relative clauses from direct interrogatives; relative clause preserved without terminal `WHAT` |
| **D38-04** | Loss of Numeric Value in Segment 09 ("110-step chart") | High | Translation | Number parser only matched single digits, extracting `1` and dropping `10` (`ONE STEP CHART`) | **CLOSED** | Authored `hundred.json`; compound 110 decomposed to `HUNDRED TEN STEP CHART` |
| **D38-05** | Loss of Numeric Value in Segment 18 ("30 minutes") | High | Translation | "30" decomposed incorrectly into `THREE` (`THREE MINUTE`), dropping order of magnitude | **CLOSED** | Authored `thirty.json`; "30 minutes" mapped to `THIRTY MINUTE` |
| **D38-06** | Loss of Numeric Value in Segment 19 ("25 year career") | High | Translation | "25" decomposed into `TWO` (`TWO YEAR`), dropping unit digit | **CLOSED** | Authored `twenty.json`; "25 year career" mapped to `TWENTY FIVE YEAR CAREER` |
| **D38-07** | Discourse Marker Distortion in Segment 14 ("You see, I've studied over 5,000 speakers...") | High | Linguistics | Conversational discourse marker "You see" parsed as transitive verb `SEE` and moved to sentence end by SOV rule | **CLOSED** | Implemented `ISL-DISCOURSE-MARKER-01`; conversational filler absorbed cleanly without emitting trailing `SEE` |
| **D38-08** | False Negation in Segment 01 ("help you overcome being uncertain, anxious, afraid") | Critical | Linguistics | `uncertain` was mapped to bare `NOT`, causing false sentence-level negation and reversing speaker's intent | **CLOSED** | Replaced `uncertain` $\to$ `NOT` with `NERVOUS`/`FEAR`; authored `overcome.json`; affirmative purpose clause restored |
| **D38-09** | Missing Essential Numeral Signs in Library (`hundred`, `twenty`, `thirty`, `zero`) | Medium | Library | Compound numbers could not be properly rendered without decade and century numerals | **CLOSED** | Authored all 4 numeral signs in Schema 2.0.0; verified 586/586 playable signs |
| **D38-10** | Missing High-Frequency Domain Concepts (`speech`, `overcome`, `this`, `here`, `that`) | Medium | Library | Concepts approximated crudely via broad synonyms (`speech` $\to$ `say people`, `overcome` $\to$ `win`) | **CLOSED** | Authored 5 Schema 2.0.0 signs citing ISLRTC representations and cross-language iconicity |
| **D38-11** | Duplicate / Redundant Verb Emission in Segment 16 & 19 (`... COACHING WORLD BIG LIKE HAVE`) | Medium | Linguistics | Auxiliary `HAVE` duplicated at beginning and end during SOV verb shift | **CLOSED** | Refactored SOV verb selection to prioritize lexical verbs and prevent auxiliary duplication |
| **D38-12** | Direct Playable Token Coverage Ceiling (62.9%) | High | Coverage | 94 words marked as grammar omissions without sign representation; direct coverage can be significantly improved with genuine sign discovery | **CLOSED** | Authored deictic signs (`THIS`, `HERE`, `THAT`); direct token coverage increased to 63.6% with 100% concept accounting |
