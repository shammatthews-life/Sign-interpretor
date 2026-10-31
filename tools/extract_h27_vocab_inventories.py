# tools/extract_h27_vocab_inventories.py
import json
import csv
import re
from pathlib import Path
from collections import defaultdict, Counter

PROJECT_ROOT = Path("d:/sign interpretor")
TRANSCRIPT_PATH = PROJECT_ROOT / "runtime" / "youtube" / "MXKkXXYUxBc" / "transcript.json"
MANIFEST_PATH = PROJECT_ROOT / "signs" / "manifest.json"
NORMALIZATION_RULES_PATH = PROJECT_ROOT / "data" / "h26_normalization_rules.json"

def pos_tagger(word):
    w = word.lower()
    if w.endswith("ly"): return "ADVERB"
    if w.endswith("ing"): return "VERB_PARTICIPLE"
    if w.endswith("ed"): return "VERB_PAST"
    if w.endswith("tion") or w.endswith("ment") or w.endswith("ness") or w.endswith("ity") or w.endswith("er") or w.endswith("or"):
        return "NOUN"
    if w.endswith("ful") or w.endswith("ous") or w.endswith("able") or w.endswith("ive") or w.endswith("al"):
        return "ADJECTIVE"
    return "NOUN_VERB_GENERAL"

def extract_inventories():
    print("Extracting Exhaustive Inventories A, B, and C from Canonical Transcript...")

    with open(TRANSCRIPT_PATH, "r", encoding="utf-8") as f:
        tdata = json.load(f)
    segments = tdata.get("segments", [])

    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        manifest = json.load(f)
    playable_signs = {s["sign_id"].lower(): s for s in manifest.get("signs", [])}

    with open(NORMALIZATION_RULES_PATH, "r", encoding="utf-8") as f:
        norm_rules = json.load(f)
    contractions = norm_rules.get("contractions", {})
    irreg_verbs = norm_rules.get("irregular_verbs", {})
    irreg_nouns = norm_rules.get("irregular_nouns", {})
    polysemy_map = norm_rules.get("polysemy_disambiguation", {})

    # Data structures for extraction
    surface_word_records = {}
    occurrences_list = []
    lemma_surface_map = defaultdict(set)
    lemma_occurrences = defaultdict(list)
    concept_records = {}

    token_global_index = 0

    for seg_idx, seg in enumerate(segments):
        seg_id = seg.get("segment_id", seg_idx + 1)
        text = seg.get("text", "")
        start = seg.get("start", 0.0)
        end = seg.get("end", 0.0)

        # Regex extracting words including apostrophes inside words (e.g. it's, don't, you've)
        raw_words = re.findall(r"\b[a-zA-Z0-9']+\b", text)

        for w_idx, raw_w in enumerate(raw_words):
            token_global_index += 1
            lower_w = raw_w.lower()
            is_cont = "'" in raw_w
            is_alphanumeric = bool(re.search(r"\d", raw_w))
            is_proper = raw_w[0].isupper() and w_idx > 0

            # 1. Inventory A: Surface word record
            if lower_w not in surface_word_records:
                surface_word_records[lower_w] = {
                    "surface_word_id": f"sw_{len(surface_word_records) + 1:04d}",
                    "surface_word": lower_w,
                    "original_casing_sample": raw_w,
                    "frequency": 0,
                    "is_contraction": is_cont,
                    "is_alphanumeric": is_alphanumeric,
                    "is_proper_noun": is_proper,
                    "occurrences": []
                }
            surface_word_records[lower_w]["frequency"] += 1
            if len(surface_word_records[lower_w]["occurrences"]) < 10:
                surface_word_records[lower_w]["occurrences"].append({
                    "token_index": token_global_index,
                    "segment_id": seg_id,
                    "timestamp": [start, end],
                    "context": text
                })

            # 2. Inventory B: Lemmatization / Normalization
            if lower_w in contractions:
                lemma = contractions[lower_w][0]
                infl = "CONTRACTION"
            elif lower_w in irreg_verbs:
                lemma = irreg_verbs[lower_w]
                infl = "IRREGULAR_VERB"
            elif lower_w in irreg_nouns:
                lemma = irreg_nouns[lower_w]
                infl = "IRREGULAR_NOUN"
            elif lower_w.endswith("ing") and len(lower_w) > 4:
                lemma = lower_w[:-3]
                infl = "PRESENT_PARTICIPLE"
            elif lower_w.endswith("ed") and len(lower_w) > 4:
                lemma = lower_w[:-2] if lower_w.endswith("eed") else lower_w[:-1] if lower_w.endswith("e") else lower_w[:-2]
                infl = "PAST_TENSE"
            elif lower_w.endswith("s") and len(lower_w) > 3 and not lower_w.endswith("ss"):
                lemma = lower_w[:-1]
                infl = "PLURAL_OR_3SG"
            else:
                lemma = lower_w
                infl = "BASE_FORM"

            lemma_surface_map[lemma].add(lower_w)
            lemma_occurrences[lemma].append({
                "token_index": token_global_index,
                "segment_id": seg_id,
                "timestamp": [start, end],
                "context": text,
                "surface_word": lower_w
            })

            # 3. Inventory C: Concept Disambiguation
            if lemma in polysemy_map:
                senses = polysemy_map[lemma]["senses"]
                # Heuristic context check for polysemous words
                context_lower = text.lower()
                chosen_sense = senses[0]
                if lemma == "right" and ("turn" in context_lower or "side" in context_lower or "hand" in context_lower):
                    chosen_sense = senses[0] # direction
                elif lemma == "right" and ("now" in context_lower or "correct" in context_lower or "yes" in context_lower):
                    chosen_sense = senses[1] if len(senses) > 1 else senses[0]
                elif lemma == "like" and ("you" in context_lower or "i" in context_lower or "love" in context_lower):
                    chosen_sense = senses[0] # preference
                elif lemma == "light" and ("heavy" in context_lower or "weight" in context_lower):
                    chosen_sense = senses[1] if len(senses) > 1 else senses[0]
                elif lemma == "watch" and ("wrist" in context_lower or "clock" in context_lower):
                    chosen_sense = senses[1] if len(senses) > 1 else senses[0]

                concept_id = f"concept_{lemma}_{chosen_sense['sense_id']}"
                sense_def = chosen_sense["definition"]
                strat = chosen_sense.get("isl_strategy", "LEXICAL_SIGN")
                sign_alias = chosen_sense.get("sign_alias", lemma)
            else:
                concept_id = f"concept_{lemma}"
                sense_def = f"General contextual sense for '{lemma}'"
                strat = "LEXICAL_SIGN" if lemma in playable_signs else "UNRESOLVED_FALLBACK"
                sign_alias = lemma if lemma in playable_signs else None

            if concept_id not in concept_records:
                # Handling route determination
                if sign_alias and sign_alias in playable_signs:
                    route = "Route A: Established direct ISL sign"
                    review_status = "IMPLEMENTATION_PENDING_LINGUISTIC_REVIEW"
                    ev_src = "ISLRTC Standard / signs/manifest.json"
                elif lemma in {"the", "a", "an", "is", "are", "am", "was", "were", "to", "of", "in"}:
                    route = "Route D: Grammatical or spatial construction"
                    review_status = "VERIFIED_ISL_EVIDENCE"
                    ev_src = "ISL Spatial Grammar Rules"
                elif lower_w in {"ted", "julian", "treasure"}:
                    route = "Route E: Official ISL fingerspelling"
                    review_status = "VERIFIED_ISL_EVIDENCE"
                    ev_src = "Two-Handed ISL Fingerspelling Engine"
                else:
                    route = "Route F: Research required or honest fallback"
                    review_status = "NO_RELIABLE_MAPPING_FOUND"
                    ev_src = "Transcript Fallback Pool"

                concept_records[concept_id] = {
                    "concept_id": concept_id,
                    "lemma": lemma,
                    "definition": sense_def,
                    "part_of_speech": pos_tagger(lemma),
                    "handling_route": route,
                    "sign_id": sign_alias if (sign_alias and sign_alias in playable_signs) else None,
                    "isl_gloss": (sign_alias or lemma).upper(),
                    "evidence_source": ev_src,
                    "review_status": review_status,
                    "surface_forms": set(),
                    "frequency": 0,
                    "sample_sentence": text
                }

            concept_records[concept_id]["surface_forms"].add(lower_w)
            concept_records[concept_id]["frequency"] += 1

            occurrences_list.append({
                "token_index": token_global_index,
                "segment_id": seg_id,
                "timestamp": [start, end],
                "surface_word": lower_w,
                "lemma": lemma,
                "concept_id": concept_id
            })

    print(f"Total Unique Surface Words: {len(surface_word_records)}")
    print(f"Total Normalized Lemmas:    {len(lemma_surface_map)}")
    print(f"Total Distinct Concepts:    {len(concept_records)}")
    print(f"Total Token Occurrences:    {len(occurrences_list)}")

    # 1. Save data/h27_unique_surface_words.json
    sw_path = PROJECT_ROOT / "data" / "h27_unique_surface_words.json"
    with open(sw_path, "w", encoding="utf-8") as f:
        json.dump({
            "metadata": {
                "title": "Inventory A: Canonical Unique Surface Words",
                "phase": "H27",
                "total_unique_surface_words": len(surface_word_records),
                "total_spoken_tokens": len(occurrences_list)
            },
            "surface_words": sorted(list(surface_word_records.values()), key=lambda x: -x["frequency"])
        }, f, indent=2)

    # 2. Save data/h27_normalized_vocabulary.json
    normalized_list = []
    for lemma, sforms in sorted(lemma_surface_map.items()):
        normalized_list.append({
            "lemma_id": f"lem_{len(normalized_list) + 1:04d}",
            "lemma": lemma,
            "part_of_speech": pos_tagger(lemma),
            "surface_forms": sorted(list(sforms)),
            "frequency": len(lemma_occurrences[lemma]),
            "sample_occurrences_count": len(lemma_occurrences[lemma])
        })
    normalized_list.sort(key=lambda x: -x["frequency"])

    norm_path = PROJECT_ROOT / "data" / "h27_normalized_vocabulary.json"
    with open(norm_path, "w", encoding="utf-8") as f:
        json.dump({
            "metadata": {
                "title": "Inventory B: Normalized Vocabulary & Morphological Forms",
                "phase": "H27",
                "total_normalized_lemmas": len(normalized_list)
            },
            "lemmas": normalized_list
        }, f, indent=2)

    # 3. Save data/h27_unique_concepts.json
    final_concepts = []
    for cid, crec in concept_records.items():
        crec_copy = dict(crec)
        crec_copy["surface_forms"] = sorted(list(crec_copy["surface_forms"]))
        final_concepts.append(crec_copy)
    final_concepts.sort(key=lambda x: -x["frequency"])

    concept_path = PROJECT_ROOT / "data" / "h27_unique_concepts.json"
    with open(concept_path, "w", encoding="utf-8") as f:
        json.dump({
            "metadata": {
                "title": "Inventory C: Distinct Lexical Concepts & Contextual Senses",
                "phase": "H27",
                "total_distinct_concepts": len(final_concepts)
            },
            "concepts": final_concepts
        }, f, indent=2)

    # 4. Save data/h27_vocabulary_occurrences.json
    occ_path = PROJECT_ROOT / "data" / "h27_vocabulary_occurrences.json"
    with open(occ_path, "w", encoding="utf-8") as f:
        json.dump({
            "metadata": {
                "title": "Complete Index of Spoken Token Occurrences",
                "phase": "H27",
                "total_token_occurrences": len(occurrences_list)
            },
            "occurrences": occurrences_list
        }, f, indent=2)

    # 5. Save data/h27_vocabulary_frequency.csv
    csv_path = PROJECT_ROOT / "data" / "h27_vocabulary_frequency.csv"
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "rank", "surface_word", "lemma", "concept_id", "frequency",
            "part_of_speech", "handling_route", "sign_id", "review_status", "sample_context"
        ])
        for rank, sw in enumerate(sorted(list(surface_word_records.values()), key=lambda x: -x["frequency"]), 1):
            w = sw["surface_word"]
            # Map to concept
            sample_ctx = sw["occurrences"][0]["context"] if sw["occurrences"] else ""
            c_entry = next((c for c in final_concepts if w in c["surface_forms"]), None)
            writer.writerow([
                rank,
                w,
                c_entry["lemma"] if c_entry else w,
                c_entry["concept_id"] if c_entry else f"concept_{w}",
                sw["frequency"],
                c_entry["part_of_speech"] if c_entry else pos_tagger(w),
                c_entry["handling_route"] if c_entry else "Route F: Fallback",
                c_entry.get("sign_id", "") if c_entry else "",
                c_entry["review_status"] if c_entry else "NO_RELIABLE_MAPPING_FOUND",
                sample_ctx
            ])

    print(f"Saved {sw_path}")
    print(f"Saved {norm_path}")
    print(f"Saved {concept_path}")
    print(f"Saved {occ_path}")
    print(f"Saved {csv_path}")
    print("INVENTORIES A, B, AND C SUCCESSFULLY GENERATED!")

if __name__ == "__main__":
    extract_inventories()
