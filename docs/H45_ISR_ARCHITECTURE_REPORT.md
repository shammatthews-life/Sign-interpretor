# H45 ISR 4.0 & Translation Architecture Report

Upgraded [SemanticUnderstandingEngine.js](file:///d:/sign%20interpretor/tools/avatar_viewer/SemanticUnderstandingEngine.js) (`ISL_ISR_4.0`) and [EnglishToISLTranslator.js](file:///d:/sign%20interpretor/tools/avatar_viewer/EnglishToISLTranslator.js) (synced to [extension/viewer/engine/](file:///d:/sign%20interpretor/extension/viewer/engine/EnglishToISLTranslator.js)):
1. **Multi-Clause Complement & WH-Boundary Segmentation:** Splits `that`-complements under negated/reporting matrices (`B14`), zero-`that` finite complements (`ADV04`, `ADV05`), and WH-complements under negated cognitive verbs (`B21`).
2. **Negation Anchoring & Contrastive Replacement:** Supports `negation_anchor: 'MATRIX_VERB'` (`B15`) and `is_contrastive_instead_of` (`B25`), preventing clause-end scope drift.
3. **Emphatic / Elliptical `DO` & NMM Propagation:** Detects `do + cognitive/lexical verb` (`HEAD_NOD_EMPHATIC` -> `NMM-EMPHATIC-NOD`) while omitting spurious action verb `DO`; resolves VP ellipsis `you do too` (`B13`).
4. **SOV Determiner Shielding & Predicate Pairing:** Prevents `"the beginner"` (`LEARN`) from locking SOV reordering (`ADV01`), and keeps perception predicates paired (`FEEL GOOD`, `B04`).
5. **Expanded `motionCatalog` & Contextual Overrides:** Supports all `647` validated signs with context-aware disambiguation (`view`, `talks`, `deliver`, `still`, `always`, `straight`, `get/gotten + comparative`).
