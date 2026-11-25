# H43 — Semantic Understanding Engineering Diary (WS2)

**Status:** COMPLETE (`PENDING_DEAF_COMMUNITY_REVIEW`)  
**Addresses Defects:** `DEF-H43-005`

---

## 1. Root Defect Identified in Baseline (`H42`)
Forensic inspection of `tools/avatar_viewer/EnglishToISLTranslator.js` revealed that although `this.semanticEngine.parseUtterance(source_text)` was called on line 1908, its returned `isr` object was logged only as a diagnostic summary string and **never consumed by any translation or restructuring step**. Consequently:
- Negation particles used a single global `gloss.indexOf('NOT')` hack that bled across subordinate/coordinate clause boundaries (`B3`, `B20`) or doubled up on negative auxiliaries (`B13`).
- Aspectual `FINISH` triggered naively whenever `'HAVE' + VERB` co-occurred globally, misclassifying `get -> HAVE` and `"getting"` (`B27`) as completed events.
- Contextual senses (`right`, `back`, `shot`, `film`, `scene`) were flattened statically in the lexicon regardless of neighboring words.
- Repeated ASR stutters (`"I've I've gathered"`) produced duplicated `I` / `HAVE` sequences.

---

## 2. ISR-Driven Architecture Implemented
Updated `tools/avatar_viewer/SemanticUnderstandingEngine.js` (`ISL_ISR_2.0`):
1. **Contraction-Aware Clause Segmentation (`segmentClauses`):**
   - Preserves apostrophes inside negative/modal contractions (`don't`, `haven't`, `isn't`, `I've`) while tokenizing terminal punctuation (`.,!?;:`).
   - Splits on coordinating/subordinating conjunctions (`and`, `but`, `so`, `because`, `or`, `if`, `when`, `while`, `although`, `though`, `since`, `unless`) while keeping coordinated pairs (`"pen and paper"`) and trailing clause adverbs (`"met before,"`) intact.
   - Splits comma-separated independent clauses cleanly only when followed by a subject/conjunction starter, leaving comma-separated noun lists (`"short films, feature films, documentaries"`) intact.
2. **True Perfective Aspect Detection (`parseClauseUnit`):**
   - `PERFECTIVE_COMPLETED` triggers **strictly** on `(have | has | had | 've | haven't | hasn't | hadn't)` followed optionally by an adverb and a recognized past participle (`met`, `gathered`, `learned`, `coached`, `-ed`/`-en`), explicitly rejecting `"have to <V>"` (deontic obligation), possessive `"have <NP>"`, and `"get/getting"`.
3. **Contextual Sense Disambiguation (`contextual_overrides`):**
   - `right` after `feel/look/seem/sound` -> `GOOD`; before `here/now/away` -> omitted intensifier; otherwise `TRUE`.
   - `shot` in media/film contexts (`vlog`, `film`, `camera`, `scene`, `movie`) -> `PICTURE`, otherwise `TRY`.
4. **ASR Uncertainty Propagation (`asr_confidence`, `avg_logprob`):**
   - Consumes optional `asrContext` per segment so low-confidence acoustic predictions propagate directly into `TRANSLATION_UNCERTAIN` status.
