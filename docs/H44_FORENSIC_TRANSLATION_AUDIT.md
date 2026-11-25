# H44 Forensic Translation & Benchmark Audit

## 1. Forensic Audit of H42/H43 "Locked" Benchmark References
Prior to touching translation rules, H44 independently cross-checked the locked `0:00–2:00` benchmark transcripts ([h42_video_a_locked_benchmark.json](file:///d:/sign%20interpretor/artifacts/h42/benchmark/h42_video_a_locked_benchmark.json) and [h42_video_b_locked_benchmark.json](file:///d:/sign%20interpretor/artifacts/h42/benchmark/h42_video_b_locked_benchmark.json)) against official YouTube manual/original tracks (`en-orig` / `en`) and CUDA multi-model Whisper inference ([h44_ab_asr_experiments.json](file:///d:/sign%20interpretor/artifacts/h44/asr/h44_ab_asr_experiments.json)). While keeping both `0:00–120.0s` windows locked, this forensic pass exposed **10 substantive reference errors** (and 12 total string diffs including punctuation) baked into H42's ground truth:

| Segment | Prior H42 String | Forensic Finding | Verified Spoken Reference ([h44_verified_references_ab.json](file:///d:/sign%20interpretor/artifacts/h44/h44_verified_references_ab.json)) |
| :--- | :--- | :--- | :--- |
| `A02` | `being uncertain, anxious, afraid` | Omitted spoken word **`nervous`** | `It's to help you overcome being uncertain, nervous, anxious, afraid,` |
| `A10` | `chart of excellence communication` | ASR noun substitution **`excellence`** | `from the 110-step chart of excellent communication.` |
| `A19` / `A18` boundary | `audience attention` | Dropped genitive possessive **`audience's`** | `when it comes to capturing an audience's attention.` |
| `A20` | `I've I've studied / gathered` | Retained ASR stutter boundary artifact | Removed stutter + normalized contraction |
| `B03` | `maybe you even gone out` | Omitted auxiliary **`you've`** | `or maybe you've even gone out and filmed some scenes...` |
| `B11` | `that the core` | Corrupted preposition **`at`** -> `that` | `that at the core of all this` |
| `B17` | Truncated / altered `feature films` | Corrected full phrasing | Preserved both `short films` and `feature films` |
| `B19` | Distorted `overarching` | Restored spoken word | Restored `overarching` |
| `B26` | `scene by scene` spacing/hyphen diff | Normalized consistently | Normalized `scene by scene` |
| `B30` | Omitted `, some talking,` | Dropped spoken appositive clause | `I'll also capture some dialogue, some talking,` |

## 2. Forensic Failure Modes Discovered in the H43 Translator & Semantic Engine
Even with exact references, auditing all 60 segments revealed critical translation failures that slipped past H43's earlier 44-case suite:

1. **WH-Question vs. Nominal Pseudo-Cleft Conflation (`A05`):**
   `"What you're about to watch is a live coaching"` began with `What`, triggering blind `WH-final` movement and scrambling meaning (`WHAT` pushed to clause end). Fixed via `ISL_ISR_3.0` discriminating `is_matrix_wh_question` vs nominal free-relatives ([SemanticUnderstandingEngine.js](file:///d:/sign%20interpretor/tools/avatar_viewer/SemanticUnderstandingEngine.js)).
2. **Embedded Quoted Direct Questions Missed WH-Final Rule (`B25`):**
   `"before you start shooting of what is my story"` kept `WHAT` before `MY STORY` because `of` merged both clauses. Splitting embedded direct `of <WH> is/are` cleanly yields `MY STORY WHAT`.
3. **Coordinated Noun Phrase Splitting (`A07`, `A22`):**
   Clause boundary logic split `"mindset and confidence"` and `"a pen and a paper"` on `and`, breaking unified SOV object phrases. Guarding coordinated nouns when the right side lacks a finite predicate preserves SOV objects intact.
4. **Subordinator SOV Bleeding (`B18`):**
   `"You need a compilation of scenes that when stitched together..."` dragged `NEED` past `THAT` into the subordinate relative clause. Stopping SOV object accumulation at `THAT` keeps `YOU COMBINATION SCENE NEED`.
5. **Contrastive Idiom False Negation (`B31`):**
   `"show not tell"` is a contrastive rhetorical formula, not clause polarity negation; H43 appended trailing `NOT` (`SHOW ... NOT`), flipping polarity. `ISL_ISR_3.0` isolates `idiomatic_negation_consumed` and prevents false `NOT` insertion (`SHOW MORE SAY LESS`).
6. **Contraction Mis-Expansion (`B04`):**
   `gonna` mapped to `go` (`I GO SAY`) rather than future auxiliary `will`. Fixed in `CONTRACTION_PATTERNS` ([EnglishToISLTranslator.js](file:///d:/sign%20interpretor/tools/avatar_viewer/EnglishToISLTranslator.js)).
7. **Generic Noun False Temporal Fronting (`B01`):**
   `timeGlosses` contained literal noun `TIME`, fronting `TIME` in `"best time to go out"` ahead of `"SUMMER HERE"`. Restricting auto-fronting to true temporal deictics (`TODAY`, `TOMORROW`, `NOW`, `SUMMER`, `FUTURE`, `YESTERDAY`, `PAST`, `BEFORE`, `NEXT`) restored `SUMMER HERE ...`.
8. **Silent Polysemy, Collisions & Unplayable Idioms (`A12`, `A15`, `A18`, `B03`, `B21`, `B23`, `B30`):**
   - `50` duplicate keys inside `lexicon` entries (`simple`, `afraid`, `sat`, `speech`, `particular`, `things`, `definitely`, `too`, etc.) silently shadowed intended glosses until purged and unified.
   - `"or so"` (`B21`) split on `so` leaving dangling `OR`; now preserved as unified `AROUND` (`around.json`).
   - `"best known"` (`A12`), `"just a"` (`B10`/`B28`), `"rest of"` (`B23`), and `"most viewed"`/`"many"` (`A13`/`A29`/`B06`) now resolve to 5 newly authored parametric ISLRTC signs (`famous`, `only`, `around`, `remaining`, `many`), lifting the library from `627` to `632` validated signs.
   - `"in the back of your mind"` (`B03`) previously dropped unplayable `INSIDE`; now maps cleanly to playable `YOUR MIND DEEP`, and `"capture some dialogue"` (`B30`) maps to `COMMUNICATION RECORD` instead of physical `HOLD`.
   - Genitive possessive `'s` (`A18` `"audience's"`) now strips `'s` before lexicon lookup so `AUDIENCE` resolves instead of `UNK`.

## 3. Forensic Honesty Boundary
All 60 segments now resolve with `0` unknown terms and `0` unavailable signs across `555` playable sign occurrences, verified programmatically in [h44_sentence_audit_ledger.json](file:///d:/sign%20interpretor/artifacts/h44/h44_sentence_audit_ledger.json). Linguistic naturalness and regional ISL acceptability remain explicitly marked `PENDING_DEAF_COMMUNITY_REVIEW`.
