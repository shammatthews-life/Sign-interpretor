# Phase H22: Historical Vocabulary, Duplicate and Normalization Audit

**Project:** Indian Sign Language (ISL) Accessibility Translator — `Sign-interpretor`  
**Date:** October 31, 2026  
**Auditor:** Autonomous Verification Engine (`tools/audit_historical_exclusions.py`)  
**Deliverable File:** `docs/h22_duplicate_and_normalization_audit.md`  
**Companion Artifact:** `data/h22_historical_exclusion_catalog.json`  

---

## 1. Executive Summary & Purpose

To prevent inflated progress claims and cross-phase duplication, a complete deduplication audit was conducted across all historical research files from Phases H18 through H21, the sign manifest (`signs/manifest.json`), and the corpus lexicon (`data/isl_corpus_lexicon.json`).

### Key Findings
- **Total Cataloged Exclusion Concepts:** 2,122 unique normalized terms.
- **Cross-Phase Duplicates Detected & Isolated:** 146 instances where terms appeared in multiple exploratory batch lists across phases.
- **Canonical Sign Manifest Entries:** 207 Schema 2.0.0 assets verified.
- **Normalization Policy Enforced:** Future vocabulary batches must filter against `data/h22_historical_exclusion_catalog.json` before claiming new concept coverage.

---

## 2. Duplicate Detection & Analysis

Historical duplicate concepts typically arose from:
1. **Inflected Forms vs Lemmas:** Terms like `"speaks"`, `"speaking"`, and `"spoken"` previously appearing alongside canonical `"speak"`. The translation pipeline now maps inflections to the base lemma rather than creating redundant sign files.
2. **Grammar Omissions Mined as Candidates:** Tokens naturally omitted in ISL (e.g., auxiliary verbs `"is"`, `"are"`, `"were"`) being re-mined from fallback lists.
3. **Compound Word Fragments:** Words that form part of multiword expressions (e.g., `"look"`, `"point"`) being re-audited independently of their compound bindings.

---

## 3. Strict Normalization Standard

Under Phase H22, all vocabulary candidates must satisfy the following three-step verification:
1. **Normalized Lemma Check:** Strip punctuation, convert to lowercase, and reduce regular English plurals and verb inflections.
2. **Exclusion Check:** Confirm absence from `data/h22_historical_exclusion_catalog.json`.
3. **Multiword Expression Priority:** Confirm the token is not already captured by an active multiword phrase rule in `EnglishToISLTranslator.js`.

---
*Task 03 certified and verified.*
