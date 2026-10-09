# Phase G2: English to ISL-oriented representation

## Scope and safety

This is a small, transparent rules layer between English ASR output and motion IDs. It is **not** full English-to-ISL translation and its outputs have not been validated by ISL language experts. Glosses are engineering labels, not a written form of ISL. The implementation deliberately retains unknown terms and reports motions that have not been authored.

## Source-supported rules

| Observation | How G2 uses it |
| --- | --- |
| ISL is a natural sign language, not English encoded on the hands; grammatical description covers word classes, syntactic relations, negation, questions, and discourse organization. Zeshan's Indo-Pakistani Sign Language overview specifically includes north-western India in its scope. [ERIC record](https://eric.ed.gov/?id=EJ661204) | G2 has a separate linguistic representation and does not map English tokens directly to avatar motions. |
| Research on ISL interrogatives and negatives describes both manual and non-manual components, including facial expression, head/body posture, and mouthing. [Kumari abstract](https://ijellh.com/index.php/OJS/article/view/9718) | A detected yes/no question gets a `YES_NO_QUESTION` non-manual requirement. G2 does not fabricate a manual question sign. Aether currently cannot render it. |
| Phrase-level lexical units must not be treated as letter sequences merely because English has several words. | G2 resolves `good morning` and `thank you` before per-word lookup. It has no fingerspelling implementation; unknown terms are returned explicitly. |
| ISLRTC's official dictionary is video-based and includes everyday terms, including some proper nouns, rather than being an alphabet-only resource. [ISLRTC FAQ](https://islrtc.nic.in/faq/) | Future lexical/proper-name resolution should consult a reviewed dictionary entry first; G2 does not yet invent a fingerspelled or motion fallback. |
| Non-manual information can be grammatical, not decorative. [iSign benchmark](https://aclanthology.org/anthology-files/pdf/findings/2024.findings-acl.643.pdf) | The intermediate representation includes `non_manual_markers`; this preserves information that current motion assets cannot express. |

## Project heuristics (not claims about all ISL)

- For only the controlled three-role patterns in the test suite, G2 produces a subject-object-verb-style gloss (`I WATER DRINK`; `YOU ME HELP`). This is a constrained project heuristic, chosen as an ISL-oriented representation, not a universal grammar assertion.
- English articles and a small set of auxiliaries are omitted only with a trace entry. This does not mean they are universally redundant in ISL.
- The translator does not implement generalized pronoun placement, negation, topicalization, time-fronting, WH-question placement, classifier constructions, or proper-noun transliteration. It leaves those cases uncertain rather than guessing.
- Status is categorical: `TRANSLATION_SUPPORTED` for direct controlled lexical phrases, `TRANSLATION_HEURISTIC` when a documented project heuristic was used, and `TRANSLATION_UNCERTAIN` when the small rule set cannot support the input.

## Unknown / needs review

- A source-backed, production-ready universal word order transformation for ISL should not be inferred from English or from ASL descriptions. Broader patterns and regional variation require Deaf/ISL expert review.
- Exact syntax of time expressions, pronouns, negation, topicalization, and proper names is not encoded in G2 yet. These remain a review queue rather than silent rewrites.
- Whether a lexical ISL sign has an Aether motion is a separate engineering state. For example `WATER` is linguistically known but is reported as `MOTION_INCOMPLETE` and is not scheduled.

## Representation and streaming policy

`EnglishToISLTranslator.translate()` returns source and normalized text, gloss sequence, playable `sign_ids`, all `motion_candidate_sign_ids`, `unknown_terms`, `unavailable_signs`, non-manual requirements, status, transformation trace, and per-stage timings. It depends on neither Aether bones nor animation code.

G1's existing committed-prefix mechanism remains the queue authority. On partial ASR text the translator is re-run, but only newly stable motion candidates are committed. The controlled transformations in G2 are deliberately conservative: phrase recognition and question detection can depend on a later token, so the trailing candidate remains uncommitted until a second observation or final transcript. Reordering is limited to complete, exactly three-resolved-item patterns; anything else is retained as uncertain rather than prematurely reordered.

## Motion resolution

The layer keeps three forms distinct:

1. English input, e.g. `I drink water.`
2. ISL-oriented gloss, e.g. `I WATER DRINK` (heuristic)
3. Motion availability, e.g. `water` known but unavailable (`MOTION_INCOMPLETE`).

No unknown term becomes an alphabet sequence or motion. Future policy may add explicit fingerspelling, but that is intentionally outside G2.
