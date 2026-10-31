# Phase H27 Initial Project & Transcript Baseline Audit

## 1. Project Repository & Git Checkpoint
- **Repository:** `D:\sign interpretor`
- **Branch:** `r1-articulation-coverage-and-report`
- **Verified Git HEAD:** `4ea8648` (`feat(isl): complete remaining vocabulary campaign and 14 batches (H26)`)
- **Working Tree:** Completely clean (`nothing to commit, working tree clean`)

## 2. Canonical Transcript Ground Truth
- **Target Video:** `https://www.youtube.com/watch?v=MXKkXXYUxBc`
- **Source File:** `runtime/youtube/MXKkXXYUxBc/transcript.json`
- **Segments Handled:** **2,366 segments**
- **Total Tokenized Word Occurrences:** **23,258 tokens**
- **Unique Surface Words (Lowercased):** **2286 unique words**

## 3. Existing Baseline Components
- **Playable Sign Library:** **562 Schema 2.0.0 assets** in `signs/manifest.json`.
- **Corpus Lexicon Entries:** **2,059 concept entries** in `data/isl_corpus_lexicon.json`.
- **H26 Processed Unresolved Concepts:** **1,388 concepts** in `data/h26_all_processed_concepts.json`.
- **Corpus Coverage Baseline:**
  - Implemented Signs: 10,308 tokens (44.32%)
  - Grammar Omissions: 9,064 tokens (38.97%)
  - Phrase Translated: 1,444 tokens (6.21%)
  - Fingerspelled: 203 tokens (0.87%)
  - Subtitle Fallbacks: 2,239 tokens (9.63%)
  - **Communicative Coverage:** **21,019 tokens (90.37%)**
  - **Discrepancy:** Exactly 0 tokens (Sum = 23,258).

## 4. Mission Directives for Phase H27
1. Build three exhaustive inventories directly from `transcript.json`:
   - **Inventory A:** Every unique surface word (2286 words).
   - **Inventory B:** Normalized forms and morphological inflections.
   - **Inventory C:** Distinct contextual senses (resolving polysemy in context).
2. Author evidence-supported direct signs where authentic ISLRTC references exist.
3. Integrate every unique word into the active production translator (`EnglishToISLTranslator.js`).
4. Reprocess all 2,366 segments with zero missing words and zero silent loss.
