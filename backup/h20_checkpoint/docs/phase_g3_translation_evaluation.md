# Phase G3: Translation evaluation and stress testing

## Evaluation method

`tools/validate_phase_g3_translation.mjs` runs a deterministic 40-sentence corpus in `tools/fixtures/g3_translation_corpus.json`. It records each source sentence, normalized text, transformation trace, gloss, playable IDs, unknown terms, unavailable motions, categorical translator status, evaluation category, and timing. It deliberately does not calculate BLEU/ROUGE because no authoritative ISL reference translation corpus is part of this project.

Evaluation labels describe the behavior of this limited system, not the correctness of a natural ISL translation:

- `SUPPORTED`: direct controlled lexical/phrase mapping.
- `HEURISTIC`: an explicitly tagged project transformation was applied.
- `UNCERTAIN`: the result is deliberately incomplete or lacks sufficient linguistic evidence.
- `FAILURE`: no resolvable gloss was produced.

The evaluator writes machine-readable and readable reports to `docs/g3_translation_evaluation_report.json` and `.md`.

## Traceable rules

| Rule ID | Source/reason | Input pattern | Transformation | Confidence |
| --- | --- | --- | --- | --- |
| G2-PHRASE-01 | Lexical phrase handling; project lexicon | `good morning`, `thank you` | Resolve the longest phrase before individual tokens | Supported only for listed lexicon entries |
| G2-SVO-01 | Project-controlled prototype; not a universal ISL claim | exactly subject + object + controlled verb | Produce controlled SOV-style gloss | Project heuristic |
| G3-RULE-PRONOUN-01 | Corrects a measured controlled-grammar gap (`I help you`) | two pronouns plus `HELP`/`NEED` | Treat the later pronoun as controlled object and retain S-O-V output | Project heuristic |
| G3-RULE-QUESTION-01 | ISL question research documents manual and non-manual components | English yes/no or WH question cue | Preserve a `YES_NO_QUESTION` or `WH_QUESTION` non-manual requirement; do not invent a manual sign | Source-supported marking, construction remains uncertain |
| G3-RULE-NEGATION-01 | ISL negation research documents lexical and non-manual components | English `not` | Retain `NOT` plus `NEGATION` non-manual requirement; do not claim a placement rule | Source-supported preservation, construction remains uncertain |
| G3-LEXICAL-01 | Evaluation coverage improvement; no grammar claim | `tomorrow`, `how`, `not` | Resolve as lexical concepts; no time-fronting or WH-order rewrite | Lexical/project catalog; motion unavailable |

## Targeted improvements

The harness compares a baseline configuration with the three G3 additions disabled against the current rule backend. The changes are intentionally narrow:

1. Pronoun-object recognition fixes the measured `I help you` controlled-pattern gap.
2. Question classification separates yes/no from WH requirements while retaining non-manual requirements rather than manufacturing motion.
3. Negation and small high-frequency lexical preservation (`not`, `how`, `tomorrow`) prevent those concepts from being silently treated as unknown; no speculative word-order rule was added.

Time ordering, generalized negation placement, topicalization, and broad function-word deletion remain open review items. They are not converted into rules merely because the corpus exposes them.

## Backend boundary

`TranslationBackend` defines `translate(text)`, `translate_partial(text)`, and `reset()`. `RuleBasedISLTranslator` is the current concrete implementation; `EnglishToISLTranslator` remains as a compatibility name for G2/G1. A later `MLTranslationBackend` or `HybridTranslationBackend` can return the same representation and categorical status before scheduler filtering. The backend does not own Aether or the sign scheduler.

## Live and latency policy

The live pipeline remains ASR → `SpeechSignOrchestrator` → rule backend → `SignScheduler` → Aether. The UI now shows raw ASR text (existing partial/final fields), gloss, resolved playable IDs, unknown/unavailable concepts, current sign, and queue. Translation's own stage timing is present in each representation; G1 timing continues to report first transcript, commit, and Aether start. The translator is synchronous and its compute time is measured independently of ASR.
