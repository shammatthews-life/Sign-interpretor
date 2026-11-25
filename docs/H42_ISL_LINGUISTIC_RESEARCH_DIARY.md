# H42 — Workstream 3: Advanced ISL Linguistic Research, Grammar & Translation Naturalness Diary

**Workstream:** WS3 (Advanced ISL Linguistic Research, Grammar and Translation Naturalness)  
**Lead:** ISL Linguistic Research Agent  
**Benchmarks:** Video A (`MXKkXXYUxBc`, 0:00–2:00, 272 words) & Video B (`y8tFSuOMAqQ`, 0:00–2:00, 539 words)

---

## 1. Research Monograph & Grammatical Foundation

Workstream 3 investigated core sign language syntax based on Indian Sign Language Research and Training Centre (ISLRTC) specifications and academic literature (Zeshan 2000, 2003; Bhattacharya et al. 2017):

### Linguistic Principles:
1. **Constituent Ordering in Complex Sentences:**
   - In simple clauses, ISL follows canonical Subject-Object-Verb (SOV) order.
   - In complex sentences containing conditional or causal relationships, the subordinate clause functions as the **Topical Frame** and precedes the main assertion:
     $$\text{Sentence} \to [\text{Condition/Reason Topic}]_{\text{raised\_eyebrows}} + [\text{Consequent Main Clause}]_{\text{neutral}}$$
   - In Video B Seg 29 (*"if it's a scene I'll have to build a little bit more around it"*), the conditional dependent clause precedes the main clause `MORE BUILD NEED`.
2. **Modal Auxiliary vs Lexical Possession Disambiguation (`DEF-H42-005`):**
   - English "have to have a story" (Video B Seg 12) combines modal necessity ("have to") with lexical possession ("have a story").
   - In natural ISL, modal necessity is signed via `NEED` or `MUST`, while possession is signed via `HAVE`. Translating both as `HAVE HAVE` is ungrammatical. The authentic ISL translation is `STORY YOU NEED HAVE`, correctly fronting object `STORY` before the modal-verb complex.
3. **Aspectual Completion vs Possession:**
   - Auxiliary "have" in present perfect ("I've learned through years...") is an aspectual completion marker `FINISH`, placed immediately following the verb (`LEARN FINISH`).
4. **Discourse Opener Priority:**
   - Conversational vocatives and discourse openers (`ALRIGHT`, `HEY`, `HELLO`, `WELCOME`) establish mutual visual engagement before any proposition begins, retaining position 0 while temporal markers (`TODAY`, `TOMORROW`, `NOW`, `SUMMER`, `FUTURE`) front to position 1.
5. **Clause-Scoped Negation:**
   - In ISL, negation particles (`NOT`) scope to the boundary of their enclosing clause rather than floating across the utterance.

---

## 2. Independent Grammar Audit & Verification

We authored and executed two independent evaluation suites to verify linguistic authenticity:
1. `tools/test_h42_dual_benchmark_evaluation.mjs` (27 total invariants verified across Video A and Video B):
   - **Video A (17 Invariants):**
     - Invariant 0: Public Speaking compound (`PUBLIC SPEECH`).
     - Invariant 1: Complement ordering & lexical disambiguation (`CONFUSED` before `OVERCOME`).
     - Invariant 2: Intensifier reduplication (`VERY MORE`).
     - Invariant 3: Interrogative relative clause protection (no interrogative `WHAT` at end).
     - Invariant 4: Broadcast studio compound (`RECORD ROOM`).
     - Invariant 5: Begin/start SOV (`START` clause-final).
     - Invariant 6: Superlative and terminal aspect (`MOST`, `FINISH` clause-final).
     - Invariant 7: Cardinal numeral composition (`HUNDRED TEN`).
     - Invariant 8: Discourse greeting protection & clause negation (`HEY` at 0, `NOT` before `MY NAME`).
     - Invariant 9: Quantifier & superlative (`MOST SEE`).
     - Invariant 10: Aspectual completion (`STUDY FINISH`).
     - Invariant 11: Enterprise entity & practice finish (`COMPANY`, `PRACTICE FINISH`).
     - Invariant 12: Cardinal numeral (`THIRTY`).
     - Invariant 13: Cardinal numeral composition (`TWENTY FIVE`).
     - Invariant 14: Pen and paper SOV (`PEN` before `HAVE`).
     - Invariant 15: Expressive idiom (`ENJOY`).
     - Invariant 16: Geopolitical entity (`SWEDEN COUNTRY`).
   - **Video B (10 Invariants):**
     - Invariant B0: Summer opening & recording initiation (`SUMMER`, `RECORD`).
     - Invariant B1: Vlogging activity & documenting life (`START`, `VIDEO`, `MOVIE`, `LIFE`).
     - Invariant B2: Advisory sharing & trial/error practice (`ADVICE`, `PRACTICE FAIL LEARN`).
     - Invariant B3: Loosely defined short film (`VIDEO`, `SIMPLE SMALL MOVIE`).
     - Invariant B4: Fatigue state (`TIRED`) & story is king superlative (`STORY MOST IMPORTANT`).
     - Invariant B5: Modal obligation (`STORY NEED HAVE`).
     - Invariant B6: Future films & scene resolution (`FUTURE`, `PICTURE`).
     - Invariant B7: Bimanual synthesis (`COMBINATION JOIN`).
     - Invariant B8: Physiological hunger & nourishment (`HUNGRY`, `FOOD`).
     - Invariant B9: Professional maxim (`SHOW MORE SAY LESS`).
2. `tools/test_h42_expanded_linguistic_suite.mjs` (8/8 passing):
   - Multi-clause coordination argument isolation.
   - Modal necessity vs possession ("have to have").
   - Aspectual completion (`FINISH`) following lexical verb.
   - Temporal marker fronting with conversational opener retention (`HELLO TOMORROW...`).
   - WH-question word finality (`... WHAT`) with non-manual marker.
   - Yes/No question non-manual marker generation without invented manual sign.
   - Natural ISL function word omission (`just`, `because`, `of`, `the`).
   - Authentic Schema 2.0.0 signs produce playable sign IDs.
