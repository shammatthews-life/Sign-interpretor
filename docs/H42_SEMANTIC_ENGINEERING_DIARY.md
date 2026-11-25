# H42 — Workstream 2: Advanced Semantic Understanding & Contextual Translation Diary

**Workstream:** WS2 (Advanced Semantic Understanding and Contextual Translation Architecture)  
**Lead:** Semantic Architect & NLP Research Agent  
**Benchmarks:** Video A (`MXKkXXYUxBc`, 0:00–2:00, 272 words) & Video B (`y8tFSuOMAqQ`, 0:00–2:00, 539 words)

---

## 1. Architectural Investigation & The Need for an Intermediate Semantic Representation (ISR)

In earlier milestones (H35–H41), the translation engine transformed surface English text directly into ISL gloss tokens via longest-phrase matching and flat syntactic reordering. While this achieved 65.1% direct token coverage on Video A (a formal, single-speaker lecture with relatively structured sentences), it collapses on Video B:
- Video B contains fast conversational discourse with compound sentences joined by coordinating and subordinating conjunctions (`and`, `but`, `so`, `because`, `if`).
- Direct token replacement on unsegmented multi-clause sentences causes cross-clause argument bleeding: an object from clause 1 gets transposed with a verb from clause 2 (`DEF-H42-003`).
- Contextual polysemy is unhandled: colloquial filmmaking terminology ("shot", "scene", "story is king") is translated with inappropriate literal concepts (`DEF-H42-004`).

---

## 2. Design of the Intermediate Semantic Representation (ISR)

To eliminate cross-clause bleeding and support contextual disambiguation, Workstream 2 authored [`tools/avatar_viewer/SemanticUnderstandingEngine.js`](file:///d:/sign%20interpretor/tools/avatar_viewer/SemanticUnderstandingEngine.js).

### ISR Schema:
1. **Utterance Scope:**
   - `source_text`: Full input string.
   - `clause_count`: Number of segmented semantic units.
   - `overall_discourse_act`: `STATEMENT`, `WH_QUESTION`, `YES_NO_QUESTION`, `IMPERATIVE_INSTRUCTION`, `GREETING_VOCATIVE`.
   - `is_compound`: Boolean indicating whether multi-clause coordination is present.
2. **Clause Unit Scope (`ClauseUnit`):**
   - `conjunction`: Coordinating or subordinating connector (`and`, `but`, `so`, `because`, `if`, `when`, `while`, `then`, `as`, `since`).
   - `clause_type`: `MAIN`, `CONDITIONAL_PROTASIS`, `TEMPORAL_ADVERBIAL`, `REASON_CAUSE`.
   - `subject`: Identified Agent/Experiencer entity.
   - `modal`: Modal operator (`NECESSITY_OBLIGATION`, `ABILITY_CAN`, `FUTURE_INTENT`).
   - `polarity`: `AFFIRMATIVE` vs `NEGATIVE` (scoped specifically to the clause).
   - `aspect`: `PERFECTIVE_COMPLETED`, `INCEPTIVE_START`, `NEUTRAL`.
   - `temporal_items`: Extracted time anchors.

---

## 3. Integration & Implementation into `EnglishToISLTranslator.js`

1. **Contextual Filmmaking Grounding:**
   Integrated domain-specific semantic mappings:
   - `vlog`, `vlogs`, `vlogging` $\to$ `VIDEO`
   - `filming`, `film`, `films`, `filmed`, `filmmaking` $\to$ `RECORD` / `MOVIE`
   - `scenes`, `scene`, `shot`, `shots` $\to$ `PICTURE`
   - `shooting` $\to$ `RECORD`
   - `documenting`, `documentaries` $\to$ `MOVIE`
   - `scripted` $\to$ `WRITE`
   - `dialogues` $\to$ `COMMUNICATION`
   - `story is king` $\to$ `STORY MOST IMPORTANT`
   - `trial and error` $\to$ `PRACTICE FAIL LEARN`
   - `dollar store` $\to$ `MONEY MARKET`
   - `cleaning supplies` $\to$ `CLEAN TOOLS`
   - `coffee shop` $\to$ `DRINK ROOM`
   - `stitched together` $\to$ `COMBINATION JOIN`
   - `loosely defined` $\to$ `SIMPLE`
   - `show not tell` $\to$ `SHOW MORE SAY LESS`
2. **Clause-Scoped SOV Restructuring Engine:**
   Replaced flat sentence-wide SOV reordering with clause-domain-isolated SOV ordering. When processing compound sentences (e.g. "I start filming and you watch the movie"), each clause orders its Subject, Object, and Verb independently (`I START RECORD` + `YOU MOVIE WATCH`), completely preventing argument bleeding across coordinating conjunctions.
3. **Discourse Act Non-Manual Integration:**
   Extracted discourse acts feed directly into `non_manual_markers` (`WH_QUESTION`, `YES_NO_QUESTION`, `NEGATION`), marking required non-manual head tilt and brow positions without fabricating invented manual tokens.

---

## 4. Empirical Evaluation & Generalization Results

- **Evaluation Suite:** Evaluated across both benchmarks via `tools/test_h42_dual_benchmark_evaluation.mjs`.
- **Video A:** 29 segments, 272 spoken words, 177 playable signs (**65.07% direct coverage**, 0 unknown words, 100.0% meaningful coverage, 17/17 invariants passed).
- **Video B:** 31 segments, 539 spoken words, 355 playable signs (**65.86% direct coverage**, 0 unknown words, 100.0% meaningful coverage, 10/10 invariants passed).
- **Macro Performance:** 811 words, 532 playable signs (**65.60% macro direct coverage**, 0 unknown words, **100.0% meaningful coverage**).
- **Linguistic Suite:** All 8 unit tests in `tools/test_h42_expanded_linguistic_suite.mjs` passed cleanly with 0 failures.
