# H44 Semantic Engine (`ISL_ISR_3.0`) & Translator Engineering Diary

## Architecture Upgrades
- **Semantic Parser (`SemanticUnderstandingEngine.js`, schema `ISL_ISR_3.0`):**
  1. **Nominal Coordination Guard:** `_rightSideHasClausePredicate()` stops `'and'`/`'or'` from fracturing coordinated object phrases like `"mindset and confidence"` (`A07`) and `"a pen and a paper"` (`A22`), preserving single-clause SOV ordering.
  2. **Approximator MWE Preservation:** `"or so"` advances past both tokens (`B21`) so clause segmentation never splits on `'so'` to leave dangling `OR`.
  3. **Matrix WH vs. Nominal Pseudo-Cleft & Embedded Questions:** Discriminates `is_matrix_wh_question` so `"What you're about to watch is..."` (`A05`) preserves leading `WHAT`, whereas matrix questions and `"of what is my story"` (`B25`) isolate `MY STORY WHAT` with `BROW_FURROW_WH`.
  4. **Contrastive Idiom & Conditional Negation:** `"show not tell"` (`B31`) sets `idiomatic_negation_consumed` and excludes the contrastive formula before negative polarity scanning; `unless` (`C16`) activates conditional negative polarity (`IF ... NOT`) + `BROW_RAISE_CONDITIONAL_TOPIC`.
  5. **Contextual Sense Disambiguation (`contextualOverrides`):** Disambiguates `right` (`GOOD`/`TRUE`/omit), `shot` (`PICTURE` vs `TRY`), `rest of` (`REMAINING`), `just` (`ONLY`/omit), `exactly` (`CLEAR`/`TRUE`), `left` (quantifier `hours left -> REMAINING` vs spatial `LEFT` vs `LEAVE`), and `too -> ALSO`.
  6. **Normalized NMM Aggregation:** Maps clause-level NMM annotations (`BROW_FURROW_WH`, `BROW_RAISE_YN`, `BROW_RAISE_CONDITIONAL_TOPIC`, `HEADSHAKE_NEGATION`) into standardized `NMM-*` markers in [EnglishToISLTranslator.js](file:///d:/sign%20interpretor/tools/avatar_viewer/EnglishToISLTranslator.js).

## Translator Fixes & Verification
- Fixed `gonna -> will` (`B04`), added `'s` possessive stripping (`audience's -> AUDIENCE` in `A18`), restricted auto-fronting `timeGlosses` (removing generic `'TIME'` so `B01` keeps `SUMMER` first), halted SOV object sweeps at subordinator `'THAT'` (`B18`), removed `'MY'`/`'YOUR'` from `subjects` so SOV reorders possessive NPs cleanly (`C26`), eliminated `50` duplicate lexicon key collisions, and synced all modules to `extension/viewer/engine/`.
- Verified via `87/87` tests in `npm.cmd test` (including new H44 regressions in [EnglishToISLTranslator.test.mjs](file:///d:/sign%20interpretor/tools/avatar_viewer/EnglishToISLTranslator.test.mjs)) and `78/78` in `test_h44_semantic_completeness.mjs`.
