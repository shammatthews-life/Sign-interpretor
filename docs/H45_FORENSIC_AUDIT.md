# H45 Forensic Audit of H44 Evaluation & Wrong-But-Playable Defects

## 1. Why H44's `100% (459/459)` Evaluation Was Overly Permissive
Auditing H44's proposition evaluator ([test_h44_semantic_completeness.mjs](file:///d:/sign%20interpretor/tools/test_h44_semantic_completeness.mjs)) revealed three circular/permissive blind spots:
1. **Unbounded Slot Matching (`Set.has`):** Checking whether concepts existed anywhere in `gloss_sequence` missed when a concept appeared inside the wrong syntactic role (e.g., `B04` `"GOOD YOUR VIDEO FEEL NOT"` fronting `GOOD` ahead of `"YOUR VIDEO"`), or when a lexical sign ALREADY existed on disk (`perspective.json`, `happen.json`, `speech.json`, `presentation.json`, `maybe.json`) yet H44 emitted a distorted substitute (`view -> SEE`, `going on -> GO`, `talks -> SAY`, `delivered -> GIVE`, `probably -> THINK`).
2. **Negation Presence vs. Clause Negation Count & Scope:** Checking `glosses.includes('NOT')` passed `B14` (`"See the problem isn't that you don't know that"` -> `SEE PROBLEM THAT YOU KNOW THAT NOT`), even though **one of two independent negations was dropped**, reversing truth value. Similarly, `B15` (`"don't know how to find ... to tell"`) and `B21` (`"don't know what I'm up to"`) allowed `NOT` to float past embedded clauses (`... TELL NOT`, `... I DO NOT`), and `ADV04` (`"I didn't say you failed the speech"`) inverted matrix negation into subordinate negation (`I SAY YOU FAIL SPEECH NOT`).
3. **Vocabulary Compression Masking Wrong-But-Playable Errors:** The `lexicon` compressed nuanced tokens into wrong playable signs purely for coverage: `things -> MATTER`, `something -> ONE`, `still -> CONTINUOUS`, `always -> CONTINUOUS`, `again -> MORE`, `some -> FEW`, `gotten -> GET`, `talks -> SAY`, `view -> SEE`, `probably -> THINK`, `do + know -> DO KNOW`.

## 2. Specific Defect Categories Uncovered in Phase 0
| Category | Affected Segments / Tests | Concrete Failure Observed |
| :--- | :--- | :--- |
| Multi-clause Negation Drop | `B14` | `isn't that you don't know` collapsed to single trailing `NOT` |
| Negation Scope Drift Past Embedded Clauses | `B15`, `B21`, `ADV04` | Matrix `don't know` / `didn't say` negated subordinate `TELL` / `DO` / `FAIL` |
| Contrastive Replacement Missing Negation | `B25` | `instead of stressing yourself` -> affirmative `INSTEAD NERVOUS YOU` |
| Spurious Emphatic / Elliptical `DO` | `B13`, `B20`, `B21`, `B24`, `ADV12` | `do know` / `you do too` emitted physical verb `DO` (`WORK`) |
| Wrong-But-Playable Noun/Verb Senses | `A06`, `A12`, `A28`, `B04`, `B06`, `B07`, `B19`, `B26`, `B27`, `B31` | `view->SEE`, `talks->SAY`, `delivered->GIVE`, `probably->THINK`, `things->MATTER`, `going on->GO`, `gotten->GET` |
| Comparative & Morphological Gaps | `B06`, `ADV06`, `ADV07`, `ADV02` | `easier` lost `MORE`; `loves`, `clearer`, `stayed`, `rained`, `home` dropped |
| SOV Noun/Verb Ambiguity | `ADV01` | Nominal `the coach` / `the beginner` (`COACHING` / `LEARN`) triggered verb lock blocking OV reordering |
