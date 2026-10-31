import json
import csv
from pathlib import Path
from collections import defaultdict

PROJECT_ROOT = Path("d:/sign interpretor")
LEXICON_PATH = PROJECT_ROOT / "data" / "isl_corpus_lexicon.json"
TRANSCRIPT_PATH = PROJECT_ROOT / "runtime" / "youtube" / "MXKkXXYUxBc" / "transcript.json"
MANIFEST_PATH = PROJECT_ROOT / "signs" / "manifest.json"

with open(LEXICON_PATH, "r", encoding="utf-8") as f:
    lexicon = json.load(f)

with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
    manifest = json.load(f)
playable_ids = {s["sign_id"].lower() for s in manifest.get("signs", [])}

# Extract concepts whose disposition is SUBTITLE_FALLBACK
fallback_records = []
for entry in lexicon:
    strat = entry.get("translation_strategy", "")
    disp = entry.get("disposition", "")
    is_fallback = entry.get("fallback_required", False) or strat == "SUBTITLE_FALLBACK" or disp == "SUBTITLE_FALLBACK"

    if is_fallback:
        lemma = entry.get("lemma", "")
        # Ensure it is genuinely not in playable_ids
        if lemma.lower() in playable_ids:
            continue

        freq = entry.get("frequency", 0)
        sforms = sorted(list(entry.get("surface_forms", [])))
        ex_sentences = entry.get("example_sentences", [])
        timestamps = entry.get("timestamps", [])
        cat = entry.get("semantic_category", "General")

        fallback_records.append({
            "concept_id": entry.get("concept_id", f"concept_{lemma}"),
            "lemma": lemma,
            "frequency": freq,
            "surface_forms": sforms,
            "semantic_category": cat,
            "dictionary_match": entry.get("dictionary_match", False),
            "dictionary_entry": entry.get("dictionary_entry"),
            "dictionary_source": entry.get("dictionary_source"),
            "example_sentences": ex_sentences[:3],
            "timestamps": timestamps[:3],
            "current_runtime_behavior": "SUBTITLE_FALLBACK_PILL",
            "root_cause": "LEXICAL_SIGN_MOTION_NOT_YET_AUTHORED"
        })

# Sort by frequency descending
fallback_records.sort(key=lambda x: -x["frequency"])
total_fallback_tokens = sum(r["frequency"] for r in fallback_records)

print(f"Total distinct fallback concepts: {len(fallback_records)}")
print(f"Total fallback token occurrences: {total_fallback_tokens}")
print("\nTop 25 Fallback Concepts:")
for r in fallback_records[:25]:
    print(f"  {r['lemma'].ljust(15)} : {r['frequency']} occurrences (Category: {r['semantic_category']})")

# Save JSON
with open(PROJECT_ROOT / "data" / "h29_remaining_fallback_inventory.json", "w", encoding="utf-8") as f:
    json.dump({
        "metadata": {
            "title": "Phase H29 Remaining Fallback Inventory",
            "phase": "H29",
            "total_concepts": len(fallback_records),
            "total_tokens": total_fallback_tokens
        },
        "fallback_concepts": fallback_records
    }, f, indent=2)

print("Saved data/h29_remaining_fallback_inventory.json")

# Save CSV
with open(PROJECT_ROOT / "data" / "h29_remaining_fallback_frequency.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([
        "rank", "concept_id", "lemma", "frequency", "semantic_category",
        "surface_forms", "dictionary_match", "dictionary_entry", "sample_sentence"
    ])
    for rank, r in enumerate(fallback_records, 1):
        sample_s = r["example_sentences"][0] if r["example_sentences"] else ""
        writer.writerow([
            rank,
            r["concept_id"],
            r["lemma"],
            r["frequency"],
            r["semantic_category"],
            "; ".join(r["surface_forms"]),
            r["dictionary_match"],
            r.get("dictionary_entry", ""),
            sample_s
        ])

print("Saved data/h29_remaining_fallback_frequency.csv")
