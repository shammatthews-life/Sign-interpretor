# tools/audit_historical_exclusions.py
import json
import glob
import os

def run_historical_audit():
    historical_sources = [
        "data/h19_250_processed_concepts.json",
        "data/h20_250_processed_concepts.json",
        "data/h21_500_processed_concepts.json",
        "data/h22_300_processed_concepts.json"
    ]
    
    all_seen_concepts = set()
    concept_source_map = {}
    duplicates_detected = []
    
    # 1. Process master concept lists
    for src in historical_sources:
        if os.path.exists(src):
            with open(src, "r", encoding="utf-8") as f:
                data = json.load(f)
                items = data.get("concepts", data) if isinstance(data, dict) else data
                if isinstance(items, list):
                    for item in items:
                        term = None
                        if isinstance(item, str):
                            term = item.lower().strip()
                        elif isinstance(item, dict):
                            term = item.get("concept", item.get("lemma", item.get("term", ""))).lower().strip()
                        
                        if term:
                            if term in all_seen_concepts:
                                duplicates_detected.append({
                                    "term": term,
                                    "original_source": concept_source_map[term],
                                    "duplicate_source": src
                                })
                            else:
                                all_seen_concepts.add(term)
                                concept_source_map[term] = src

    # 2. Process sign manifest
    manifest_signs = set()
    with open("signs/manifest.json", "r", encoding="utf-8") as f:
        manifest = json.load(f)
        for s in manifest.get("signs", []):
            sid = s.get("id", "").lower().strip()
            manifest_signs.add(sid)
            all_seen_concepts.add(sid)
            concept_source_map[sid] = "signs/manifest.json"

    # 3. Process lexicon list
    with open("data/isl_corpus_lexicon.json", "r", encoding="utf-8") as f:
        lexicon = json.load(f)
        for entry in lexicon:
            if isinstance(entry, dict):
                lemma = entry.get("lemma", entry.get("concept_id", "")).lower().strip()
                if lemma:
                    all_seen_concepts.add(lemma)
                    if lemma not in concept_source_map:
                        concept_source_map[lemma] = "data/isl_corpus_lexicon.json"

    exclusion_list = sorted(list(all_seen_concepts))

    catalog = {
        "audit_timestamp": "2026-10-31T03:15:00+05:30",
        "total_historical_exclusions": len(exclusion_list),
        "manifest_signs_count": len(manifest_signs),
        "duplicate_occurrences_found": len(duplicates_detected),
        "duplicate_sample": duplicates_detected[:20],
        "historical_exclusion_terms": exclusion_list
    }

    with open("data/h22_historical_exclusion_catalog.json", "w", encoding="utf-8") as f:
        json.dump(catalog, f, indent=2)

    print(f"Historical audit complete.")
    print(f"Total exclusion concepts cataloged: {len(exclusion_list)}")
    print(f"Duplicate cross-phase references detected: {len(duplicates_detected)}")
    print("Generated data/h22_historical_exclusion_catalog.json")

if __name__ == "__main__":
    run_historical_audit()
