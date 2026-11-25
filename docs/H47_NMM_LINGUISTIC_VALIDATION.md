# H47 Non-Manual Marker (NMM) Linguistic Validation

- **H46 Defect Fixed in H47 (`H47-DEF-03`):** Previously, `cueNmm` was broadcast to every sign in a cue. H47 added `_buildNmmScopes()` in `EnglishToISLTranslator.js` -> `youtube-cue-manifest.js` -> `timeline-synchronizer.js`, scoping:
  - `NMM-NEG-HEADSHAKE` to negative predicates/particles (`NMM_CONSTITUENT_SCOPING: PASS`, opening noun `today` receives `[]`).
  - `NMM-WH-BROW-FURROW` to the WH constituent/clause.
  - `NMM-COND-BROW-RAISE` to the conditional antecedent (`if`-clause).
- **Minimal-Pair Contrast (`NMM_MINIMAL_PAIR_CONTRAST: PASS`):** On identical manual sign `help`, NMMs produce distinct 3D `Bip001_Head` signatures (`negYawDelta=-0.1554 rad`, `ynPitchDelta=-0.0856 rad`, `whPitchDelta=+0.1011 rad`).
- **Boundary:** Measurable bone deltas do not prove Deaf comprehension; human NMM discrimination is staged in `TRIAL-03` of `eval_protocol_pack.json` (`PENDING_DEAF_COMMUNITY_REVIEW`).
