# H47 Translation Error Analysis

| Error Category | Pre-H47 Example | Post-H47 Resolution | Status |
|---|---|---|---|
| Polysemy collision | `"Look at your right hand"` -> `TRUE HAND` | Mapped `"right hand"` -> `SIDE HAND` | **Fixed** |
| Phrasal verb drop | `"Sign up for the class"` -> `CLASS` | Mapped `"sign up"` -> `JOIN` | **Fixed** |
| Adverb gap | `"explained clearly"` dropped `clearly` | Mapped `"clearly"` -> `CLEAR` | **Fixed** |
| Cue-wide NMM over-application | `NMM-NEG-HEADSHAKE` on opening `today` | Scoped via `nmm_scopes` to negative predicate/particle | **Fixed** |
| Cross-cue referent drift | `teacher` locus reset per segment | Persistent `discourseContext` across segments | **Fixed** |
| Unverified Deaf comprehension | No blind comprehension test pack | `eval_protocol_pack.json` ready | **PENDING_DEAF_COMMUNITY_REVIEW** |
