# H45 Deep ISL Linguistic Research & Grammatical Provenance

Grounded in **ISLRTC** (*SignLearn* / Official ISL Dictionary), **Aboh, Pfau & Zeshan (2005)**, **Zeshan & Sinha**, and comparative sign-linguistics (kept strictly distinct from direct ISL attestation):

1. **Multi-Clause Negation & Scope Boundaries (`B14`, `B15`, `B21`, `ADV04`):**
   - In ISL, negation relies on clause-final manual `NOT` co-occurring with `HEADSHAKE_NEGATION` (`Zeshan & Sinha`), whose scope is bounded by syntactic clause domain.
   - Collapsing `"The problem isn't that you don't know that"` (`B14`) into one `NOT` inverted truth value; `ISL_ISR_4.0` splits complement `that`-clauses and zero-`that` reporting complements (`"I didn't say | you failed"`, `ADV04`) so each negated predicate keeps its own scoped `NOT`.
   - When matrix negation embeds an infinitive (`"don't know how to find ... to tell"`, `B15`), `negation_anchor: 'MATRIX_VERB'` anchors `NOT` at `KNOW` (`YOU KNOW NOT HOW ...`) rather than letting `NOT` float across the embedded infinitive.
2. **Emphatic & Elliptical `do` (`B13`, `B20`, `B21`, `B24`):**
   - ISL does not realize English emphatic *do* as an independent action verb; instead it marks affirmation via intensified motion and emphatic head nod (`NMM-EMPHATIC-NOD`), while VP ellipsis (`you do too`) resolves to its lexical antecedent (`KNOW`).
3. **Contrastive Replacement `"instead of X"` (`B25`):**
   - Rendered via contrastive spatial/negative framing (`YOU NERVOUS NOT | BEFORE YOU START RECORD ...`) rather than affirmative `INSTEAD NERVOUS YOU`.
4. **Inchoative Comparatives & SOV Determiner Guards (`B06`, `ADV01`, `ADV07`):**
   - Comparative adjectives (`easier`, `better`, `clearer`) expand to `MORE + ADJ`, paired with inchoative `BECOME` for `"get/gotten + ADJ"`.
   - Determiner-marked nouns (`"the beginner"`) are shielded from verb-matching inside `_restructureClauseGloss` so SOV object fronting works reliably (`YESTERDAY COACHING LEARN HELP`).
5. **Honest Provenance:** All structural rules and 647 parametric signs remain `PENDING_DEAF_COMMUNITY_REVIEW`.
