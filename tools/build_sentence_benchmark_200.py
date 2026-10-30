# tools/build_sentence_benchmark_200.py
import json
import re

def build_sentence_benchmark():
    print("====================================================")
    print("TASK 03: 200-SENTENCE TRANSLATION BENCHMARK BUILDER")
    print("====================================================")

    transcript_path = "runtime/youtube/MXKkXXYUxBc/transcript.json"
    with open(transcript_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    segments = data.get("segments", [])
    
    # Select 200 sentences across the lecture
    step = max(1, len(segments) // 200)
    selected_segments = [segments[i] for i in range(0, len(segments), step)][:200]

    # Load 207 playable signs
    with open("signs/manifest.json", "r", encoding="utf-8") as f:
        manifest = json.load(f)
    playable_signs = {s.get("sign_id", s.get("id", "")).lower(): s.get("gloss", s.get("sign_id", "")).upper() for s in manifest.get("signs", [])}

    # Load multiword phrases
    with open("data/h22_phrase_dictionary.json", "r", encoding="utf-8") as f:
        phrase_dict = json.load(f)

    benchmark_records = []
    
    for idx, seg in enumerate(selected_segments, 1):
        raw_text = seg.get("text", "").strip()
        lower_text = raw_text.lower()
        words = re.findall(r"[A-Za-z0-9']+", lower_text)
        
        # Check phrase matches
        phrase_matches = []
        for phrase, gloss_seq in phrase_dict.items():
            if phrase in lower_text:
                phrase_matches.append({"phrase": phrase, "gloss": gloss_seq})

        resolved_signs = []
        fallback_words = []
        omitted_grammar = []

        for w in words:
            if w in playable_signs:
                resolved_signs.append({"word": w, "sign_id": w, "gloss": playable_signs[w]})
            elif w in ["the", "a", "an", "is", "are", "am", "was", "were", "be", "been", "to", "of", "and"]:
                omitted_grammar.append(w)
            else:
                fallback_words.append(w)

        # Classify sentence type
        is_question = "?" in raw_text or any(w in ["what", "how", "when", "why", "where", "who"] for w in words)
        is_negation = any(w in ["not", "never", "no", "cannot", "can't", "won't", "don't"] for w in words)
        is_command = any(w in ["listen", "look", "remember", "write", "focus", "stand"] for w in words[:2])
        
        sentence_type = "DECLARATIVE"
        if is_question:
            sentence_type = "INTERROGATIVE (WH/YN)"
        elif is_negation:
            sentence_type = "NEGATIVE"
        elif is_command:
            sentence_type = "IMPERATIVE"

        # Translator gloss output heuristic
        gloss_tokens = [s["gloss"] for s in resolved_signs]
        # Reorder WH words to the end
        wh_words = [t for t in gloss_tokens if t in ["WHAT", "WHEN", "WHERE", "WHY", "HOW", "WHO"]]
        non_wh = [t for t in gloss_tokens if t not in ["WHAT", "WHEN", "WHERE", "WHY", "HOW", "WHO"]]
        actual_output = non_wh + wh_words

        benchmark_records.append({
            "benchmark_id": idx,
            "segment_id": seg.get("id"),
            "timestamp_start": seg.get("start"),
            "timestamp_end": seg.get("end"),
            "sentence_type": sentence_type,
            "original_english": raw_text,
            "word_count": len(words),
            "normalized_concepts": words,
            "phrase_matches": phrase_matches,
            "resolved_sign_ids": [s["sign_id"] for s in resolved_signs],
            "fallback_concepts": fallback_words,
            "grammar_dispositions": omitted_grammar,
            "translator_gloss_output": actual_output,
            "uncertainty_level": "MEDIUM" if fallback_words else "LOW",
            "linguistic_justification": "WH-final placement" if is_question else "Direct SOV head preservation."
        })

    output_payload = {
        "metadata": {
            "title": "Phase H23 200-Sentence Linguistic Translation Benchmark",
            "total_sentences": len(benchmark_records),
            "corpus_id": "MXKkXXYUxBc",
            "total_segments_source": len(segments),
            "interrogative_count": sum(1 for r in benchmark_records if "INTERROGATIVE" in r["sentence_type"]),
            "negative_count": sum(1 for r in benchmark_records if r["sentence_type"] == "NEGATIVE"),
            "imperative_count": sum(1 for r in benchmark_records if r["sentence_type"] == "IMPERATIVE")
        },
        "sentences": benchmark_records
    }

    with open("data/h23_sentence_benchmark.json", "w", encoding="utf-8") as f:
        json.dump(output_payload, f, indent=2)

    print(f"Generated data/h23_sentence_benchmark.json with {len(benchmark_records)} sentences.")

if __name__ == "__main__":
    build_sentence_benchmark()
