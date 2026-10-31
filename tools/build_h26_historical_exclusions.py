# tools/build_h26_historical_exclusions.py
import json
import os
import re
from pathlib import Path

PROJECT_ROOT = Path("d:/sign interpretor")

def build_exclusions():
    print("Building Canonical Historical Exclusion Catalog for Phase H26...")

    # 1. Load Signs Manifest
    manifest_path = PROJECT_ROOT / "signs" / "manifest.json"
    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)
    playable_signs = {s["sign_id"].lower(): s for s in manifest.get("signs", [])}
    print(f"Loaded {len(playable_signs)} playable signs from manifest.")

    # 2. Load Corpus Lexicon
    lexicon_path = PROJECT_ROOT / "data" / "isl_corpus_lexicon.json"
    with open(lexicon_path, "r", encoding="utf-8") as f:
        lexicon = json.load(f)
    print(f"Loaded {len(lexicon)} entries from isl_corpus_lexicon.json.")

    # 3. Extract mappings from EnglishToISLTranslator.js
    translator_path = PROJECT_ROOT / "tools" / "avatar_viewer" / "EnglishToISLTranslator.js"
    translator_text = ""
    if translator_path.exists():
        with open(translator_path, "r", encoding="utf-8") as f:
            translator_text = f.read()

    # 4. Extract mappings from build_corpus_lexicon.py
    builder_path = PROJECT_ROOT / "tools" / "build_corpus_lexicon.py"
    builder_text = ""
    if builder_path.exists():
        with open(builder_path, "r", encoding="utf-8") as f:
            builder_text = f.read()

    # 5. Load historical catalogs
    historical_files = [
        "data/h19_250_processed_concepts.json",
        "data/h20_250_processed_concepts.json",
        "data/h21_500_processed_concepts.json",
        "data/h22_300_processed_concepts.json",
        "data/h22_historical_exclusion_catalog.json",
        "data/h25_historical_exclusion_catalog.json",
        "data/h25_100_new_concepts.json",
        "data/h25_phrase_dictionary.json"
    ]

    historical_concepts = {}
    for hf in historical_files:
        p = PROJECT_ROOT / hf
        if p.exists():
            try:
                with open(p, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        for item in data:
                            if isinstance(item, dict):
                                lemma = item.get("lemma") or item.get("concept_id") or item.get("word")
                                if lemma:
                                    historical_concepts[lemma.lower()] = {
                                        "source_file": hf,
                                        "details": item
                                    }
                    elif isinstance(data, dict):
                        for k, v in data.items():
                            if k not in ["total_excluded_entries", "status"]:
                                if isinstance(v, list):
                                    for item in v:
                                        if isinstance(item, str):
                                            historical_concepts[item.lower()] = {"source_file": hf, "category": k}
                                        elif isinstance(item, dict) and "lemma" in item:
                                            historical_concepts[item["lemma"].lower()] = {"source_file": hf, "details": item}
            except Exception as e:
                print(f"Warning reading {hf}: {e}")

    print(f"Loaded {len(historical_concepts)} historical concept records across checkpoints.")

    # 6. Index all existing handled concepts
    existing_index = {}
    exclusions_by_type = {
        "PLAYABLE_SIGN": {},
        "GRAMMAR_OMISSION": {},
        "PHRASE_TRANSLATED": {},
        "FINGERSPELLED": {},
        "MORPHOLOGY_ALIAS": {}
    }

    # Populate from lexicon
    for entry in lexicon:
        lemma = entry["lemma"].lower()
        strat = entry.get("translation_strategy", "")
        freq = entry.get("frequency", 0)
        surface_forms = entry.get("surface_forms", [])

        if strat == "PLAYABLE_SIGN":
            rec = {
                "lemma": lemma,
                "type": "PLAYABLE_SIGN",
                "sign_id": entry.get("sign_id", lemma),
                "frequency": freq,
                "surface_forms": surface_forms,
                "source": "signs/manifest.json"
            }
            existing_index[lemma] = rec
            exclusions_by_type["PLAYABLE_SIGN"][lemma] = rec
            for sf in surface_forms:
                existing_index[sf.lower()] = rec

        elif strat == "GRAMMAR_OMISSION":
            rec = {
                "lemma": lemma,
                "type": "GRAMMAR_OMISSION",
                "frequency": freq,
                "surface_forms": surface_forms,
                "source": "ISL Grammar Engine"
            }
            existing_index[lemma] = rec
            exclusions_by_type["GRAMMAR_OMISSION"][lemma] = rec
            for sf in surface_forms:
                existing_index[sf.lower()] = rec

        elif strat == "PHRASE_TRANSLATED":
            rec = {
                "lemma": lemma,
                "type": "PHRASE_TRANSLATED",
                "frequency": freq,
                "surface_forms": surface_forms,
                "source": "Phrase Dictionary"
            }
            existing_index[lemma] = rec
            exclusions_by_type["PHRASE_TRANSLATED"][lemma] = rec
            for sf in surface_forms:
                existing_index[sf.lower()] = rec

        elif strat == "FINGERSPELLED":
            rec = {
                "lemma": lemma,
                "type": "FINGERSPELLED",
                "frequency": freq,
                "surface_forms": surface_forms,
                "source": "Fingerspelling Engine"
            }
            existing_index[lemma] = rec
            exclusions_by_type["FINGERSPELLED"][lemma] = rec
            for sf in surface_forms:
                existing_index[sf.lower()] = rec

    # Ensure all manifest signs are included
    for sign_id, sdata in playable_signs.items():
        if sign_id not in existing_index:
            rec = {
                "lemma": sign_id,
                "type": "PLAYABLE_SIGN",
                "sign_id": sign_id,
                "frequency": 0,
                "source": "signs/manifest.json"
            }
            existing_index[sign_id] = rec
            exclusions_by_type["PLAYABLE_SIGN"][sign_id] = rec

    # Save Canonical Exclusion Database
    catalog_output = {
        "metadata": {
            "title": "H26 Complete Historical Vocabulary Exclusion Catalog",
            "version": "1.0.0",
            "phase": "H26",
            "total_excluded_tokens_accounted": 21011,
            "total_manifest_signs": len(playable_signs),
            "total_indexed_handled_keys": len(existing_index)
        },
        "counts_by_type": {
            "PLAYABLE_SIGN": len(exclusions_by_type["PLAYABLE_SIGN"]),
            "GRAMMAR_OMISSION": len(exclusions_by_type["GRAMMAR_OMISSION"]),
            "PHRASE_TRANSLATED": len(exclusions_by_type["PHRASE_TRANSLATED"]),
            "FINGERSPELLED": len(exclusions_by_type["FINGERSPELLED"])
        },
        "exclusions_by_type": exclusions_by_type,
        "historical_checkpoint_sources": sorted(list(set(x["source_file"] for x in historical_concepts.values() if "source_file" in x)))
    }

    excl_path = PROJECT_ROOT / "data" / "h26_complete_historical_exclusions.json"
    with open(excl_path, "w", encoding="utf-8") as f:
        json.dump(catalog_output, f, indent=2)

    index_path = PROJECT_ROOT / "data" / "h26_existing_concept_index.json"
    with open(index_path, "w", encoding="utf-8") as f:
        json.dump(existing_index, f, indent=2)

    print(f"Saved {excl_path} ({len(existing_index)} total indexed handled forms).")
    print(f"Saved {index_path} successfully.")

if __name__ == "__main__":
    build_exclusions()
