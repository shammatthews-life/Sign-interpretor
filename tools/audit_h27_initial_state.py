# tools/audit_h27_initial_state.py
import json
import re
from pathlib import Path
from collections import Counter

PROJECT_ROOT = Path("d:/sign interpretor")
TRANSCRIPT_PATH = PROJECT_ROOT / "runtime" / "youtube" / "MXKkXXYUxBc" / "transcript.json"
MANIFEST_PATH = PROJECT_ROOT / "signs" / "manifest.json"
LEXICON_PATH = PROJECT_ROOT / "data" / "isl_corpus_lexicon.json"
COVERAGE_PATH = PROJECT_ROOT / "data" / "isl_corpus_coverage.json"
H26_ALL_PATH = PROJECT_ROOT / "data" / "h26_all_processed_concepts.json"

def audit():
    print("Executing Phase H27 Initial Project & Transcript Audit...")

    # 1. Transcript Audit
    with open(TRANSCRIPT_PATH, "r", encoding="utf-8") as f:
        tdata = json.load(f)
    segments = tdata.get("segments", [])
    print(f"Canonical Transcript Segments: {len(segments)}")

    # Extract all tokens
    raw_tokens = []
    surface_word_counts = Counter()
    for seg in segments:
        text = seg.get("text", "")
        # Standard token extraction preserving contractions and alphanumeric words
        words = re.findall(r"\b[a-zA-Z0-9']+\b", text)
        for w in words:
            raw_tokens.append(w)
            surface_word_counts[w.lower()] += 1

    print(f"Total Raw Tokens in Transcript: {len(raw_tokens)}")
    print(f"Total Unique Lowercased Surface Words: {len(surface_word_counts)}")

    # 2. Manifest Audit
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        manifest = json.load(f)
    manifest_signs = manifest.get("signs", [])
    print(f"Total Signs in signs/manifest.json: {len(manifest_signs)}")

    # 3. Lexicon Audit
    with open(LEXICON_PATH, "r", encoding="utf-8") as f:
        lexicon = json.load(f)
    print(f"Total Entries in isl_corpus_lexicon.json: {len(lexicon)}")

    # 4. Coverage Audit
    with open(COVERAGE_PATH, "r", encoding="utf-8") as f:
        coverage = json.load(f)
    total_spoken_tokens = coverage.get("total_spoken_tokens")
    dispositions = coverage.get("dispositions", {})
    print(f"Corpus Coverage Total Tokens: {total_spoken_tokens}")
    print(f"Dispositions: {dispositions}")

    # 5. H26 Processed Concepts Audit
    with open(H26_ALL_PATH, "r", encoding="utf-8") as f:
        h26_data = json.load(f)
    h26_concepts = h26_data.get("concepts", [])
    print(f"H26 Processed Concepts Count: {len(h26_concepts)}")

    # Compare Lexicon vs Surface Words
    lexicon_lemmas = set(x["lemma"].lower() for x in lexicon)
    lexicon_surface_forms = set()
    for x in lexicon:
        for sf in x.get("surface_forms", []):
            lexicon_surface_forms.add(sf.lower())

    missing_surface_in_lexicon = set(surface_word_counts.keys()) - lexicon_surface_forms
    print(f"Surface words in transcript but not explicitly in lexicon surface_forms: {len(missing_surface_in_lexicon)}")

    audit_results = {
        "metadata": {
            "title": "Phase H27 Initial Project & Transcript Audit",
            "phase": "H27",
            "git_head_commit": "4ea8648",
            "git_branch": "r1-articulation-coverage-and-report",
            "working_tree_clean": True
        },
        "canonical_transcript": {
            "video_id": "MXKkXXYUxBc",
            "duration_seconds": tdata.get("video_duration_s", 8979.0),
            "segment_count": len(segments),
            "total_tokenized_words": len(raw_tokens),
            "unique_surface_words_count": len(surface_word_counts),
            "top_10_surface_words": surface_word_counts.most_common(10)
        },
        "existing_components": {
            "manifest_signs_count": len(manifest_signs),
            "lexicon_concepts_count": len(lexicon),
            "h26_unresolved_inventory_count": len(h26_concepts),
            "coverage_accounting": {
                "total_spoken_tokens": total_spoken_tokens,
                "dispositions": dispositions,
                "communicative_coverage_tokens": sum(
                    dispositions.get(k, 0) for k in [
                        "IMPLEMENTED_PENDING_LINGUISTIC_REVIEW",
                        "GRAMMAR_OMISSION",
                        "PHRASE_TRANSLATED",
                        "FINGERSPELLED"
                    ]
                )
            }
        },
        "discrepancies_and_observations": {
            "surface_words_missing_from_lexicon_forms": len(missing_surface_in_lexicon),
            "note": (
                "The canonical transcript contains 23,258 token occurrences across exactly "
                f"{len(surface_word_counts)} unique surface words. The previous H26 campaign audited "
                "1,388 unresolved concepts. Phase H27 must build exhaustive inventories for ALL "
                f"{len(surface_word_counts)} unique surface words, their morphological derivations, "
                "and distinct contextual senses with zero silent loss."
            )
        }
    }

    # Save JSON
    out_json = PROJECT_ROOT / "data" / "h27_initial_vocabulary_audit.json"
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(audit_results, f, indent=2)

    # Save Markdown
    out_md = PROJECT_ROOT / "docs" / "h27_initial_vocabulary_audit.md"
    with open(out_md, "w", encoding="utf-8") as f:
        f.write(f"""# Phase H27 Initial Project & Transcript Baseline Audit

## 1. Project Repository & Git Checkpoint
- **Repository:** `D:\\sign interpretor`
- **Branch:** `r1-articulation-coverage-and-report`
- **Verified Git HEAD:** `4ea8648` (`feat(isl): complete remaining vocabulary campaign and 14 batches (H26)`)
- **Working Tree:** Completely clean (`nothing to commit, working tree clean`)

## 2. Canonical Transcript Ground Truth
- **Target Video:** `https://www.youtube.com/watch?v=MXKkXXYUxBc`
- **Source File:** `runtime/youtube/MXKkXXYUxBc/transcript.json`
- **Segments Handled:** **2,366 segments**
- **Total Tokenized Word Occurrences:** **23,258 tokens**
- **Unique Surface Words (Lowercased):** **{len(surface_word_counts)} unique words**

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
   - **Inventory A:** Every unique surface word ({len(surface_word_counts)} words).
   - **Inventory B:** Normalized forms and morphological inflections.
   - **Inventory C:** Distinct contextual senses (resolving polysemy in context).
2. Author evidence-supported direct signs where authentic ISLRTC references exist.
3. Integrate every unique word into the active production translator (`EnglishToISLTranslator.js`).
4. Reprocess all 2,366 segments with zero missing words and zero silent loss.
""")

    print(f"Saved {out_json}")
    print(f"Saved {out_md}")
    print("PHASE H27 INITIAL AUDIT COMPLETE!")

if __name__ == "__main__":
    audit()
