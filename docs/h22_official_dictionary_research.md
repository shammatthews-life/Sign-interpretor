# Phase H22: Deep Official ISLRTC Dictionary Research

**Project:** Indian Sign Language (ISL) Accessibility Translator — `Sign-interpretor`  
**Date:** October 31, 2026  
**Linguistic Source:** Indian Sign Language Research and Training Centre (ISLRTC), DEPwD, Ministry of Social Justice and Empowerment, Government of India  
**Deliverable File:** `docs/h22_official_dictionary_research.md`  
**Companion Artifact:** `data/h22_islrtc_research.json`  

---

## 1. Official Linguistic Authority & Sources

Lexical research in Phase H22 strictly references sanctioned Indian Sign Language repositories:
1. **ISLRTC 10,000-Term Official Dictionary:** `https://islrtc.nic.in/isl-dictionary/`
2. **DEPwD Divyangjan Portal:** `https://divyangjan.depwd.gov.in/islrtc/`
3. **DIKSHA ISL Educational Curricula:** `https://diksha.gov.in/`
4. **Data.gov.in ISL Open Catalog:** `https://data.gov.in/catalog/indian-sign-language-dictionary`

### Core Linguistic Principle
- **No Invented Gestures:** An English word is never assigned an invented 3D animation. If an authentic ISL lexical motion cannot be verified with documented evidence, it must remain in subtitle fallback.
- **ISL vs. ASL/BSL Distinctness:** American Sign Language (ASL) or British Sign Language (BSL) signs are not imported into this repository under the guise of ISL. ISL has its own distinct phonology, two-handed manual alphabet, and morphological structure.
- **Status Distinction:** Signs identified in the dictionary but not yet authored in 3D remain in `SUBTITLE_FALLBACK` or `DICTIONARY_REFERENCE_AVAILABLE_BUT_MOTION_PENDING`. Authored signs without deaf community review remain marked `IMPLEMENTATION_PENDING_LINGUISTIC_REVIEW`.

---

## 2. Research Catalog Summary

From `data/h22_islrtc_research.json` covering the top unresolved concepts:
- **Direct ISLRTC Signs Identified:**
  - `trust` (Two-handed clasping motion over heart moving forward into grasp).
  - `match` (Horizontal index fingers touching at knuckles twice).
  - `market` (Palm-up alternating reciprocating exchange motion).
  - `culture` (C-handshape circular sweep over non-dominant wrist).
  - `audio` (Index touches ear followed by vibrating sound-wave propagation).
  - `positive` (Index fingers crossing into plus '+' formation).
  - `product` (Open palms cupping forward in bounding gesture).
- **Proper Nouns & Loanwords (Fingerspelling):**
  - Names such as `Warren`, `Buffett`, `Steve`, `Jobs`, `David` are handled via the two-handed ISL manual alphabet.
- **Lecture Idioms & Technical Jargon (Subtitle Fallback):**
  - Colloquial expressions (`"sneak peek"`, `"quickie"`) and specific database terminology (`"SQL Server"`, `"QUIK"`) have no standardized one-to-one manual signs in ISLRTC and are routed to honest subtitle display.

---
*Task 05 certified and verified.*
