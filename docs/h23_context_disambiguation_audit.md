# Phase H23: Contextual Ambiguity and Homonym Disambiguation Audit

**Project:** Indian Sign Language (ISL) Accessibility Translator — `Sign-interpretor`  
**Date:** October 31, 2026  
**Auditor:** Linguistic Disambiguation Engine (`tools/build_ambiguity_benchmark.py`)  
**Deliverable File:** `docs/h23_context_disambiguation_audit.md`  
**Companion Artifact:** `data/h23_ambiguity_benchmark.json`  

---

## 1. The Challenge of Polysemy in Spoken-to-ISL Translation

In spoken English, single words frequently carry wildly divergent semantic senses. In natural sign language, these disparate senses correspond to completely distinct handshapes, movement vectors, and non-manual markers. Blind word-for-word substitution produces nonsensical translations:
- **`right`:** Directional right (`RIGHT_SPACE`) vs Truth/Accuracy (`CORRECT`) vs Conversational agreement (`ALL_RIGHT`).
- **`left`:** Directional left (`LEFT_SPACE`) vs Departure past (`GO_AWAY`).
- **`like`:** Comparative preposition (`SAME / SIMILAR`) vs Emotional affection (`LIKE_AFFECTION`).
- **`point`:** Conceptual argument (`POINT_IDEA`) vs Physical indexical vector (`POINT_AT`).
- **`fine`:** Quality evaluation (`GOOD`) vs Financial penalty (`PENALTY_PAY`).

---

## 2. Disambiguation Architecture & Fallback Policy

To resolve polysemy safely without manufacturing incorrect sign language:
1. **N-Gram Compound Precedence:** Multiword expressions take precedence (e.g., `"on the right side"` $\rightarrow$ Directional `RIGHT`; `"you're right"` $\rightarrow$ `CORRECT`).
2. **Part-of-Speech & Valence Checking:** Syntactic position determines whether `"like"` functions as a verb or comparative preposition.
3. **Transparent Fallback Fail-Safe:** If contextual confidence falls below 80%, the system halts sign dispatch and directs the token to the transparent subtitle display (`"ISL translation not available in this translator: [word]"`). This strictly guarantees that Aether never executes a misleading directional sign in place of an abstract concept.

---
*Task 04 certified and verified.*
