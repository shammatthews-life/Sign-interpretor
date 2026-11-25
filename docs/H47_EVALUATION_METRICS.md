# H47 Evaluation Metrics Specification

- **Technical Metrics (Automated):** Unit test pass rate (`88/88`), sign schema validity (`647/647`), rotation uniqueness (`0` dupes), proposition slot recall (`461/461`), strict relational pass rate (`33/33`), live Chrome head/spine NMM deltas (`rad`).
- **Comprehension Metrics (Human-Ready Protocol, Currently Unmeasured = `PENDING_DEAF_COMMUNITY_REVIEW`):**
  - **Meaning Reconstruction Accuracy:** % of core event + agent/patient + polarity propositions reconstructed accurately from blind avatar viewing.
  - **Distractor-Controlled MC Accuracy:** Target selection rate adjusted by Confidence (1–5) to separate true comprehension from guessing.
  - **Minimal-Pair Discrimination (`d'` / accuracy):** Ability to distinguish Affirmative vs Negation vs Y/N vs WH and Left-to-Right vs Right-to-Left spatial loci.
  - **Subjective Readability & Naturalness:** 5-point Likert distributions + qualitative defect tags.
