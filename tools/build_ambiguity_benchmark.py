# tools/build_ambiguity_benchmark.py
import json
import re

def build_ambiguity_benchmark():
    print("====================================================")
    print("TASK 04: CONTEXTUAL AMBIGUITY & HOMONYM STRESS TEST")
    print("====================================================")

    transcript_path = "runtime/youtube/MXKkXXYUxBc/transcript.json"
    with open(transcript_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    segments = data.get("segments", [])
    
    target_homonyms = [
        "right", "left", "like", "well", "kind", "light", "change", "point", 
        "mean", "fine", "close", "present", "make", "get", "take", "run", 
        "turn", "play", "sound", "over"
    ]

    ambiguity_catalog = []

    for term in target_homonyms:
        matches = []
        pattern = re.compile(rf"\b{term}\b", re.IGNORECASE)
        for seg in segments:
            text = seg.get("text", "")
            if pattern.search(text):
                matches.append({
                    "segment_id": seg.get("id"),
                    "timestamp": seg.get("start"),
                    "sentence": text.strip()
                })
                if len(matches) >= 3:
                    break

        # Define ISL semantic senses
        senses = {
            "right": [
                {"sense": "DIRECTION", "isl_gloss": "RIGHT (spatial index)", "example": "look to your right"},
                {"sense": "CORRECT", "isl_gloss": "CORRECT / TRUE", "example": "that is right"},
                {"sense": "DISCOURSE_MARKER", "isl_gloss": "ALL-RIGHT / AGREE", "example": "right, let us begin"}
            ],
            "left": [
                {"sense": "DIRECTION", "isl_gloss": "LEFT (spatial index)", "example": "on the left side"},
                {"sense": "DEPARTURE_PAST", "isl_gloss": "GO-AWAY / FINISH", "example": "he left the room"}
            ],
            "like": [
                {"sense": "SIMILARITY_PREPOSITION", "isl_gloss": "SAME / SIMILAR", "example": "sounds like a bell"},
                {"sense": "AFFECTION_VERB", "isl_gloss": "LIKE (chest clasp)", "example": "I like this topic"}
            ],
            "point": [
                {"sense": "ARGUMENT_NOUN", "isl_gloss": "POINT / IDEA", "example": "make a good point"},
                {"sense": "DEICTIC_VERB", "isl_gloss": "POINT-AT (index gesture)", "example": "point at the screen"}
            ],
            "well": [
                {"sense": "DISCOURSE_FILLER", "isl_gloss": "OMITTED_OR_PAUSE", "example": "well, let us see"},
                {"sense": "HEALTH_ADVERB", "isl_gloss": "GOOD / HEALTHY", "example": "he did very well"}
            ]
        }

        term_senses = senses.get(term, [
            {"sense": "PRIMARY_LEXICAL", "isl_gloss": term.upper(), "example": f"standard usage of {term}"},
            {"sense": "SECONDARY_METAPHORICAL", "isl_gloss": "SUBTITLE_FALLBACK", "example": f"idiomatic context of {term}"}
        ])

        ambiguity_catalog.append({
            "homonym": term,
            "total_occurrences_found": len(matches),
            "senses_documented": term_senses,
            "transcript_contexts": matches,
            "disambiguation_strategy": "CONTEXTUAL_N_GRAM_AND_POS",
            "fallback_policy": "If disambiguation confidence < 80%, fallback to subtitle display to prevent misleading gestures."
        })

    output_payload = {
        "metadata": {
            "title": "Phase H23 Contextual Ambiguity and Homonym Disambiguation Benchmark",
            "total_homonyms_evaluated": len(ambiguity_catalog)
        },
        "ambiguity_cases": ambiguity_catalog
    }

    with open("data/h23_ambiguity_benchmark.json", "w", encoding="utf-8") as f:
        json.dump(output_payload, f, indent=2)

    print(f"Generated data/h23_ambiguity_benchmark.json across {len(ambiguity_catalog)} homonyms.")

if __name__ == "__main__":
    build_ambiguity_benchmark()
