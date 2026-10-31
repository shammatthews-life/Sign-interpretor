# Phase H28: Initial Forensic Audit

**Project:** ISL Accessibility Translator — Sign-interpretor  
**Repository:** `d:\sign interpretor`  
**Branch:** `r1-articulation-coverage-and-report`  
**Starting Commit:** `314dd0e`  
**Date:** October 31, 2026  

---

## 1. Baseline Verification

Before initiating any modifications, the local Git tree and historical deliverables were audited:
- **Git Branch:** `r1-articulation-coverage-and-report`
- **HEAD Commit:** `314dd0e` (`feat(isl): complete unique-word vocabulary generation and integration (H27)`)
- **Working Tree Condition:** Clean (0 uncommitted modifications, 0 unstaged files).
- **Playable Sign Library:** 566 Schema 2.0.0 signs registered in `signs/manifest.json`.
- **Target Transcript:** `runtime/youtube/MXKkXXYUxBc/transcript.json` (2,366 segments, 23,258 tokens).

---

## 2. Forensic Findings on Reported Discrepancies

### Issue A: 23,256 vs 23,258 Tokens (RESOLVED)
- **Root Cause:** A single non-ASCII character `ü` (U+00FC) in Segment #1274 (`"His name is Hans Rüsling."`) caused regex word boundary failures in `extract_h27_vocab_inventories.py`, dropping `R` and `sling` (2 tokens).
- **Resolution:** Independently reconciled to exactly **23,258 tokens**. Fully documented in `docs/h28_accounting_reconciliation.md` and `data/h28_accounting_reconciliation.json`.

### Issue B: 10,898 Glosses vs 10,762 Dispatches (RESOLVED)
- **Root Cause:** Exactly 136 glosses produced by multi-word phrase rules (`GOING_TO`: 85, `MUST`: 21, `ALL`: 16, `AGAIN`: 9, `FOR`: 3, `AND`: 1, `ALSO`: 1) lacked entries in `this.motionCatalog` and were filtered before dispatch.
- **Resolution:** Trace ledger constructed linking each gloss to its exact source phrase and linguistic explanation.

### Issue C: Linguistic Review Audit (IN PROGRESS)
- 10,308 tokens remain marked `IMPLEMENTATION_PENDING_LINGUISTIC_REVIEW`.
- Workstream C establishes authentic ISLRTC citation verification, evidence tiers, and native Deaf reviewer packaging.
