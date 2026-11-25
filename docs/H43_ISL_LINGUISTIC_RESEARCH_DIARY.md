# H43 — ISL Linguistic Research & Translation Diary (WS3)

**Status:** COMPLETE (`PENDING_DEAF_COMMUNITY_REVIEW`)  
**Addresses Defects:** `DEF-H43-006`, `DEF-H43-007`, `DEF-H43-008`

---

## 1. Lexicon Repairs (`DEF-H43-007`)
Independently audited all 1,667 `lexicon` mappings in `tools/avatar_viewer/EnglishToISLTranslator.js` against `motionCatalog` and `signs/*.json`:
- Fixed 3 broken catalog references where lexicon targets did not exist on disk: `hello -> HELLO` (was `GREETING`), `himself -> HE`, `herself -> SHE` (plus authored `he.json` and `she.json`).
- Fixed semantic collisions and placeholder substitutions:
  - `evening`: `MORNING` -> `EVENING` (`signs/evening.json`)
  - `eight`: `ONE` -> `EIGHT` (`signs/eight.json`)
  - `nine`: `ONE` -> `NINE` (`signs/nine.json`)
  - `third`: `ONE` -> `THIRD` (`signs/third.json`)
  - `yesterday`: `TIME` -> `YESTERDAY`
  - `wind`: `TREE` -> `WIND` (`signs/wind.json`)
  - `back`: `PAST` -> `BACK` (`signs/back.json`)
  - `get/getting/gotten`: `HAVE` -> `GET` (`signs/get.json`)
  - `film/films`: `RECORD/MOVIE` -> `FILM` (`signs/film.json`)
  - `scene/scenes`: `PICTURE` -> `SCENE` (`signs/scene.json`)
  - `maybe`: `GUESS` -> `MAYBE` (`signs/maybe.json`)
  - `also`: `MORE` -> `ALSO` (`signs/also.json`)
  - `kind`: `SAME` -> `GOOD`
  - `right`: removed static blanket `TRUE`, delegated to clause context.

---

## 2. Elimination of Meaning-Reversing Omissions (`DEF-H43-006`)
Removed `without`, `because`, `but`, `or`, `if` from the English function-word omission set (`auxiliaries`), authored dedicated ISL signs (`without.json`, `because.json`, `but.json`, `or.json`, `why.json`, `if.json`, `already.json`), and verified retention in `gloss_sequence` and `sign_ids`.

---

## 3. Clause-Scoped ISL Restructuring & Playable Fingerspelling (`DEF-H43-008`)
Refactored `EnglishToISLTranslator.translate()` to process every ISR clause (`_restructureClauseGloss`) independently:
1. **Clause-Local Temporal Fronting:** Fronts temporal markers (`TODAY`, `TOMORROW`, `YESTERDAY`, `EVENING`, `BEFORE`, `FUTURE`) to the head of their own clause (after conversational openers `HEY`/`HELLO`/`WELCOME` or discourse connectors), while preserving greetings such as `"GOOD MORNING"`.
2. **Clause-Local SOV / OV Reordering:** Orders subject-object-verb within clause boundaries so objects/modifiers do not migrate across conjunctions.
3. **Clause-Isolated Negation (`NOT`):** Collapses auxiliary-induced duplicate negations (`doesn't` -> single `NOT`) and anchors `NOT` strictly to the end of its enclosing clause (`B3`, `B13`, `B20`).
4. **Playable Proper-Noun & Acronym Fingerspelling (`fs_<word>`):** Proper nouns (`David`, `JP`, `Phillips`, `TEDx`, `Oracle`, `Google`, `Disney`, `Chimamanda`, `Adichie`, `Nigeria`) and domain acronyms (`IIT`, `NPTEL`, `MIT`, `AI`, `GPU`, `RGB`, `CNN`, `LSTM`) emit `FS_<WORD>` glosses and playable `fs_<word>` IDs resolved directly by `SignLibrary` via `ISLFingerspelling.js`, while unknown non-proper words remain honest `unknown_terms` without fabrication.
5. **Verification:** Verified in `tools/avatar_viewer/EnglishToISLTranslator.test.mjs`; linguistic acceptability remains `PENDING_DEAF_COMMUNITY_REVIEW`.
