# Phase H23: Advanced Phrase Engine and Multiword Parsing Quality Audit

**Project:** Indian Sign Language (ISL) Accessibility Translator — `Sign-interpretor`  
**Date:** October 31, 2026  
**Auditor:** Multiword Grammar Parsing Suite (`tools/validate_h23_phrase_engine.mjs`)  
**Deliverable File:** `docs/h23_phrase_engine_quality.md`  

---

## 1. Multiword Expression Processing Architecture

Compound phrases and idiomatic expressions represent a significant portion of lecture speech ($1,444\text{ tokens}$ across $2,366\text{ segments}$). Parsing multiword expressions requires strict syntactic precedence:
1. **Contraction Normalization:** Contractions like `"you're"`, `"i'm"`, `"can't"` are expanded prior to phrase dictionary matching.
2. **Greedy Longest-Match Sorting:** The phrase dictionary is indexed in descending order of token length (4-grams $\rightarrow$ 3-grams $\rightarrow$ 2-grams). Longer expressions (e.g. `"take a look at"`) match first, preventing sub-phrase shadowing by `"look at"`.
3. **Particle Absorption:** Non-semantic prepositions within English idioms are absorbed into the single ISL conceptual gloss, avoiding redundant gestures.
4. **Non-Destructive Tokenization:** When a phrase matches, its constituent token range is marked as `PHRASE_TRANSLATED` and consumed as a unified block, ensuring zero double-counting in corpus accounting.

---

## 2. Precedence & Regression Suite Results

- **Active Researched Compounds:** 100 high-yield educational idioms verified in active runtime.
- **Dead Rule Analysis:** 0 empty or unreachable phrase patterns detected.
- **Plateau Breakthrough Verified:** Phrase-translated tokens remain solidly at **1,444 occurrences (+29 tokens)** over Phase H21.

---
*Task 11 certified and verified.*
