"""
Audit the remaining fallback pool from data/isl_corpus_lexicon.json and runtime/youtube/MXKkXXYUxBc/transcript.json.
Generates:
- data/h25_remaining_fallback_frequency.csv
- data/h25_remaining_fallback_frequency.json
- data/h25_historical_exclusion_catalog.json
"""
import json
import csv
from collections import defaultdict, Counter
from pathlib import Path

PROJECT_ROOT = Path("d:/sign interpretor")
LEXICON_PATH = PROJECT_ROOT / "data" / "isl_corpus_lexicon.json"
TRANSCRIPT_PATH = PROJECT_ROOT / "runtime" / "youtube" / "MXKkXXYUxBc" / "transcript.json"
MANIFEST_PATH = PROJECT_ROOT / "signs" / "manifest.json"

with open(LEXICON_PATH, "r", encoding="utf-8") as f:
    lexicon = json.load(f)

with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
    manifest = json.load(f)

existing_signs = set(s["sign_id"] for s in manifest["signs"])

print(f"Total entries in lexicon: {len(lexicon)}")
print(f"Total signs in manifest: {len(existing_signs)}")

# Filter fallback entries
fallback_entries = [x for x in lexicon if x.get("translation_strategy") == "SUBTITLE_FALLBACK" or x.get("fallback_required") is True]
print(f"Fallback concepts count: {len(fallback_entries)}")

total_fallback_tokens = sum(x["frequency"] for x in fallback_entries)
print(f"Total fallback token occurrences: {total_fallback_tokens}")

# Build frequency rankings
fallback_entries.sort(key=lambda x: -x["frequency"])

# Write CSV
csv_path = PROJECT_ROOT / "data" / "h25_remaining_fallback_frequency.csv"
with open(csv_path, "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["rank", "concept_id", "lemma", "frequency", "semantic_category", "surface_forms", "example"])
    for rank, item in enumerate(fallback_entries, 1):
        writer.writerow([
            rank,
            item.get("concept_id", ""),
            item.get("lemma", ""),
            item.get("frequency", 0),
            item.get("semantic_category", "Uncategorized"),
            ";".join(item.get("surface_forms", [])),
            item.get("example_sentences", [""])[0] if item.get("example_sentences") else ""
        ])

# Write JSON
json_path = PROJECT_ROOT / "data" / "h25_remaining_fallback_frequency.json"
with open(json_path, "w", encoding="utf-8") as f:
    json.dump({
        "total_fallback_concepts": len(fallback_entries),
        "total_fallback_token_occurrences": total_fallback_tokens,
        "concepts": fallback_entries
    }, f, indent=2)

# Build historical exclusion catalog (520 existing signs + grammar omissions + phrases)
exclusion_catalog = {
    "total_excluded_entries": len(existing_signs),
    "existing_playable_signs": sorted(list(existing_signs)),
    "grammar_omissions": [x["lemma"] for x in lexicon if x.get("translation_strategy") == "GRAMMAR_OMISSION"],
    "phrase_translated": [x["lemma"] for x in lexicon if x.get("translation_strategy") == "PHRASE_TRANSLATED"],
    "fingerspelled": [x["lemma"] for x in lexicon if x.get("translation_strategy") == "FINGERSPELLED"]
}

exclusion_path = PROJECT_ROOT / "data" / "h25_historical_exclusion_catalog.json"
with open(exclusion_path, "w", encoding="utf-8") as f:
    json.dump(exclusion_catalog, f, indent=2)

print("TASK 03 AUDIT COMPLETE:")
print(f"  + Generated {csv_path}")
print(f"  + Generated {json_path}")
print(f"  + Generated {exclusion_path}")
