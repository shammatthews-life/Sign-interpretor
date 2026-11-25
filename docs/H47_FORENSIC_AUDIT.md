# H47 Forensic Audit — Comprehension, NMM Scope, Discourse & Visual Readability

**Baseline Commit:** `f57fd9ab47f60d81269c7ba2c411b0fec4a1ce41`

---

## 1. Critical Separation of Engineering Metrics vs. Comprehension

H46 demonstrated technical playback, `0` duplicate sign rotations, and Node-level bone actuation, **not** Deaf comprehension. Specifically:
- **Motion uniqueness != ISL correctness:** Removing identical `rotations` prevents two words from looking identical, but artificial differentiation without linguistic review can still be non-canonical.
- **Bone delta != appropriate NMM:** Applying `NMM-NEG-HEADSHAKE` or `NMM-WH-BROW-FURROW` uniformly across an entire cue ignores syntactic scope.
- **Per-segment translation != discourse continuity:** Locked Videos A (`29` segments) and B (`31` segments) are continuous narratives; stateless per-segment locus assignment breaks cross-cue referent tracking.

---

## 2. H47 Defect Discovery Summary

| Defect ID | Area | Observed Evidence | Impact on Comprehension |
|---|---|---|---|
| `H47-DEF-01` | Accessibility & Deaf Eval | Zero `ISO/IEC 20071-24` mapping, zero Deaf-centred evaluation protocol/kit | No credible pathway for real Deaf ISL comprehension testing |
| `H47-DEF-02` | Discourse Continuity | `EnglishToISLTranslator.translate()` has no persistent `discourseContext` | Spatial loci reset between consecutive sentences |
| `H47-DEF-03` | NMM Scope | `timeline-synchronizer.js` sends full `cueNmm` to every sign in cue | Negation/WH NMMs over-applied to unrelated topic/noun signs |
| `H47-DEF-04` | Contextual Resolution | Polysemous words (`left`, `right`, `sign up`, `back`) resolve without sense disambiguation | Wrong sign chosen in non-canonical contexts |
| `H47-DEF-05` | Chrome NMM Telemetry | `h46_real_chrome_e2e_evidence.json` `poseKeys` omit `head` and `spine` | Live browser NMM/spatial actuation unverified |
| `H47-DEF-06` | Trajectory Quality Audit | No anatomical/feature-cluster audit across all `647` signs | Potential unnatural joint extremes or tempo compression (`2.2x`) |
