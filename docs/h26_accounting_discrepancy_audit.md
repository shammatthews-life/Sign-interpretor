# Phase H26 Audit: Resolution of the H25 14-Token Discrepancy

## Executive Summary
This document provides the definitive mathematical and structural audit resolving the apparent 14-token difference noted between the initial Phase H25 fallback research pool (reported as 1,398 unique concepts and 2,260 token occurrences) and the final canonical corpus accounting (reported as 2,246 subtitle fallback tokens).

**Conclusion:** Neither value was fabricated or erroneous. The 14-token variance is completely accounted for by two concrete, chronological facts in the H25 pipeline:
1. **13 tokens** were converted from `SUBTITLE_FALLBACK` into `IMPLEMENTED_PENDING_LINGUISTIC_REVIEW` when 30 new signs were authored during Phase H25 Task 05 and integrated into the lexicon.
2. **1 token** (`tomorrow`, frequency: 1) was categorized in the final accounting as `DICTIONARY_REFERENCE_AVAILABLE_BUT_MOTION_PENDING` (a distinct disposition), whereas the initial Task 03 survey lumped it into the broad un-signable research pool.

$$13\text{ (newly implemented tokens)} + 1\text{ (pending motion token)} = 14\text{ tokens reconciled}$$

---

## 1. Timeline of Events in Phase H25

### Step 1: Task 03 Baseline Audit (Pre-Authoring State)
- At the start of Phase H25, Worker A executed [`tools/audit_h25_fallback_pool.py`](../tools/audit_h25_fallback_pool.py) against the pre-H25 corpus lexicon.
- This initial audit counted all tokens requiring fallback or lacking playable sign assets:
  - Total fallback concepts: **1,398 concepts**
  - Total token occurrences: **2,260 tokens** (comprising 2,259 subtitle fallbacks + 1 dictionary reference pending motion).
- This was exported to [`data/h25_remaining_fallback_frequency.json`](../data/h25_remaining_fallback_frequency.json).

### Step 2: Task 05 New Sign Authoring & Integration
- In Task 05, Worker A authored 30 new Schema 2.0.0 sign assets in `signs/`:
  `fix`, `realize`, `notice`, `limit`, `substance`, `cover`, `risk`, `safe`, `guide`, `memory`, `join`, `explain`, `complex`, `nature`, `weather`, `plant`, `animal`, `mountain`, `river`, `ocean`, `bridge`, `market`, `cost`, `rich`, `weak`, `heavy`, `shadow`, `mirror`, `window`, `wall`.
- Out of these 30 concepts, 10 had direct spoken occurrences in the canonical lecture transcript:
  - `mirror`: 2 tokens
  - `notice`: 2 tokens
  - `market`: 2 tokens
  - `substance`: 1 token
  - `animal`: 1 token
  - `complex`: 1 token
  - `memory`: 1 token
  - `explain`: 1 token
  - `cover`: 1 token
  - `cost`: 1 token
  - **Total Converted Tokens:** **13 tokens** (spanning 10 unique concepts).

### Step 3: Task 07 Final Lexicon Rebuild & Accounting
- In Task 07, [`tools/build_corpus_lexicon.py`](../tools/build_corpus_lexicon.py) was executed to produce the updated master lexicon.
- Because those 10 concepts were now playable signs in `signs/manifest.json`, their disposition transitioned from `SUBTITLE_FALLBACK` to `IMPLEMENTED_PENDING_LINGUISTIC_REVIEW`:
  $$\text{New Fallback Pool} = 2,260 - 13 = 2,247\text{ tokens}$$
- The 2,247 unresolved tokens were partitioned into mutually exclusive categories in [`data/isl_corpus_coverage.json`](../data/isl_corpus_coverage.json):
  - `SUBTITLE_FALLBACK`: **2,246 tokens**
  - `DICTIONARY_REFERENCE_AVAILABLE_BUT_MOTION_PENDING`: **1 token** (`tomorrow`)
  - **Sum:** **2,247 tokens**

---

## 2. Mathematical Reconciliation Table

| Metric | Task 03 Audit | Task 07 Rebuild | Difference | Resolution Explanation |
| :--- | :---: | :---: | :---: | :--- |
| **Total Canonical Tokens** | 23,258 | 23,258 | 0 | Strict mathematical invariant preserved. |
| **Playable Sign Tokens** | 10,287 | 10,300 | +13 | 10 newly authored concepts converted to signs. |
| **Combined Unresolved Tokens** | 2,260 | 2,247 | -13 | Tokens absorbed by newly authored signs. |
| **Subtitle Fallback Only** | 2,259 | 2,246 | -13 | Directly reflects the +13 playable sign absorption. |
| **Dictionary Reference Pending** | 1 | 1 | 0 | `tomorrow` (isolated in final accounting). |
| **Apparent Discrepancy** | **2,260** | **2,246** | **14** | **Reconciled: 13 implemented + 1 isolated pending.** |

---

## 3. Machine-Readable Audit Output
The full concept-level record mapping every reconciled token is stored in:
[`data/h26_h25_discrepancy_resolution.json`](../data/h26_h25_discrepancy_resolution.json).

**Confirmed Invariant for Phase H26:**
The current baseline active fallback inventory consists of:
- **1,388 concepts** strictly categorized as `SUBTITLE_FALLBACK` (**2,246 tokens**).
- **1 concept** strictly categorized as `DICTIONARY_REFERENCE_AVAILABLE_BUT_MOTION_PENDING` (**1 token**: `tomorrow`).
- **Total Unresolved Baseline Inventory:** **1,389 concepts** (**2,247 tokens**).
