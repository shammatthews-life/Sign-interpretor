# Phase H28: Translation Quality Benchmark Report

**Project:** ISL Accessibility Translator — Sign-interpretor  
**Repository:** `d:\sign interpretor`  
**Phase:** H28  
**Benchmark Scope:** 42 Structured Sentences across 11 Linguistic Categories

---

## 1. Benchmark Structure & Design

The translation quality benchmark evaluates the translator across 11 critical linguistic dimensions:
1. **Simple Declarative Sentences:** Basic SOV reordering (`I WATER DRINK`).
2. **Questions:** WH-Final syntax (`YOU WANT WHAT`, `YOU KNOW HOW`).
3. **Negation:** Headshake and NOT-Final ordering (`I WATER WANT NOT`).
4. **Multi-Clause Sentences:** Conditional and temporal clauses.
5. **Pronoun Variations:** Directional pronouns and spatial indexing.
6. **Possessives:** Argument possessive markers.
7. **Temporal References:** Past and future aspectual signs (`TOMORROW`, `TIME`).
8. **Idioms & Collocations:** Multi-token phrase priority (`OVER AND OVER AGAIN`).
9. **Proper Nouns & Technical Terms:** Accurate routing to fingerspelling.
10. **Contextual Polysemy:** Correct sense selection for ambiguous words (`right`, `like`, `light`).
11. **Honest Fallbacks:** Explicit subtitle pill trigger for abstract concepts.

---

## 2. Benchmark Execution Harness

The automated benchmark runner is implemented in [`tools/test_h28_translation_quality.mjs`](../tools/test_h28_translation_quality.mjs).
