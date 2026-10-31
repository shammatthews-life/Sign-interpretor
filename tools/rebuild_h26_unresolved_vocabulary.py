# tools/rebuild_h26_unresolved_vocabulary.py
import json
import csv
import re
from pathlib import Path
from collections import defaultdict

PROJECT_ROOT = Path("d:/sign interpretor")

def pos_heuristic(word):
    w = word.lower()
    if w.endswith("ly"):
        return "ADVERB"
    if w.endswith("ing") or w.endswith("ed") or w.endswith("ize") or w.endswith("ate"):
        return "VERB"
    if w.endswith("tion") or w.endswith("ment") or w.endswith("ness") or w.endswith("ity") or w.endswith("er") or w.endswith("or"):
        return "NOUN"
    if w.endswith("ful") or w.endswith("ous") or w.endswith("able") or w.endswith("ive") or w.endswith("al"):
        return "ADJECTIVE"
    return "NOUN / UNCLASSIFIED"

def rebuild_unresolved():
    print("Rebuilding Complete Unresolved Vocabulary Inventory...")

    lexicon_path = PROJECT_ROOT / "data" / "isl_corpus_lexicon.json"
    with open(lexicon_path, "r", encoding="utf-8") as f:
        lexicon = json.load(f)

    transcript_path = PROJECT_ROOT / "runtime" / "youtube" / "MXKkXXYUxBc" / "transcript.json"
    with open(transcript_path, "r", encoding="utf-8") as f:
        transcript_data = json.load(f)
    segments = transcript_data.get("segments", [])

    # Identify all unresolved entries in current lexicon
    unresolved_entries = []
    for item in lexicon:
        strat = item.get("translation_strategy", "")
        fallback_req = item.get("fallback_required", False)
        rev_status = item.get("linguistic_review_status", "")

        # Unresolved if strategy is SUBTITLE_FALLBACK or DICTIONARY_VERIFIED_PENDING_MOTION
        if strat == "SUBTITLE_FALLBACK" or fallback_req or "PENDING_MOTION" in rev_status:
            unresolved_entries.append(item)

    print(f"Total unique unresolved concepts identified: {len(unresolved_entries)}")
    total_tokens = sum(x.get("frequency", 0) for x in unresolved_entries)
    print(f"Total token occurrences across unresolved concepts: {total_tokens}")

    # Build segment mapping from canonical transcript
    # Segment IDs where each lemma appears
    lemma_segments = defaultdict(list)
    for seg_idx, seg in enumerate(segments):
        seg_id = seg.get("segment_id", seg_idx + 1)
        text = seg.get("text", "")
        tokens = re.findall(r"\b[a-zA-Z0-9']+\b", text.lower())
        for tok in set(tokens):
            lemma_segments[tok].append(seg_id)

    # Enrich unresolved entries
    enriched_list = []
    for entry in unresolved_entries:
        lemma = entry.get("lemma", "").lower()
        freq = entry.get("frequency", 0)
        surface_forms = entry.get("surface_forms", [lemma])

        # Find segment IDs
        seg_ids = set()
        for sf in surface_forms:
            seg_ids.update(lemma_segments.get(sf.lower(), []))
        seg_ids_list = sorted(list(seg_ids))

        # Priority calculation
        if freq >= 5:
            priority = "HIGH (P1 - Core Video Vocabulary)"
        elif freq >= 2:
            priority = "MEDIUM (P2 - Secondary Lexicon)"
        else:
            priority = "LOW (P3 - Hapax / Long Tail)"

        pos = pos_heuristic(lemma)
        cat = entry.get("semantic_category") or "General Discourse"

        enriched_rec = {
            "concept_id": lemma,
            "lemma": lemma,
            "surface_words": surface_forms,
            "frequency": freq,
            "example_sentence": entry.get("example_sentences", [""])[0] if entry.get("example_sentences") else "",
            "segment_ids": seg_ids_list[:10],
            "total_segments_count": len(seg_ids_list),
            "semantic_category": cat,
            "part_of_speech": pos,
            "existing_sign_mapping": None,
            "phrase_availability": False,
            "dictionary_evidence": entry.get("dictionary_entry") if entry.get("dictionary_match") else None,
            "current_disposition": entry.get("translation_strategy", "SUBTITLE_FALLBACK"),
            "research_priority": priority
        }
        enriched_list.append(enriched_rec)

    # Sort descending by frequency, then alphabetically by lemma
    enriched_list.sort(key=lambda x: (-x["frequency"], x["lemma"]))

    # 1. Save CSV
    csv_path = PROJECT_ROOT / "data" / "h26_complete_unresolved_vocabulary.csv"
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "rank", "lemma", "frequency", "research_priority", "part_of_speech",
            "semantic_category", "surface_words", "example_sentence", "segments_count"
        ])
        for rank, item in enumerate(enriched_list, 1):
            writer.writerow([
                rank,
                item["lemma"],
                item["frequency"],
                item["research_priority"],
                item["part_of_speech"],
                item["semantic_category"],
                "; ".join(item["surface_words"]),
                item["example_sentence"],
                item["total_segments_count"]
            ])

    # 2. Save JSON
    json_path = PROJECT_ROOT / "data" / "h26_complete_unresolved_vocabulary.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({
            "metadata": {
                "title": "H26 Complete Unresolved Vocabulary Inventory",
                "phase": "H26",
                "total_unresolved_concepts": len(enriched_list),
                "total_unresolved_tokens": total_tokens,
                "frequency_bands": {
                    "high_p1_gte_5": sum(1 for x in enriched_list if x["frequency"] >= 5),
                    "medium_p2_2_to_4": sum(1 for x in enriched_list if 2 <= x["frequency"] < 5),
                    "low_p3_eq_1": sum(1 for x in enriched_list if x["frequency"] == 1)
                }
            },
            "concepts": enriched_list
        }, f, indent=2)

    # 3. Frequency Matrix
    freq_matrix = defaultdict(lambda: {"concept_count": 0, "token_sum": 0, "sample_lemmas": []})
    for item in enriched_list:
        fr = item["frequency"]
        freq_matrix[fr]["concept_count"] += 1
        freq_matrix[fr]["token_sum"] += fr
        if len(freq_matrix[fr]["sample_lemmas"]) < 8:
            freq_matrix[fr]["sample_lemmas"].append(item["lemma"])

    matrix_sorted = {str(k): freq_matrix[k] for k in sorted(freq_matrix.keys(), reverse=True)}

    matrix_path = PROJECT_ROOT / "data" / "h26_unresolved_frequency_matrix.json"
    with open(matrix_path, "w", encoding="utf-8") as f:
        json.dump({
            "total_unresolved_concepts": len(enriched_list),
            "total_unresolved_tokens": total_tokens,
            "frequency_distribution": matrix_sorted
        }, f, indent=2)

    print(f"Generated {csv_path}")
    print(f"Generated {json_path}")
    print(f"Generated {matrix_path}")
    print("TASK 04 REBUILD COMPLETE!")

if __name__ == "__main__":
    rebuild_unresolved()
