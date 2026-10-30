# tools/mine_multiword_phrases.py
import json
import re
import csv
from collections import Counter

def mine_transcript_phrases():
    transcript_path = "runtime/youtube/MXKkXXYUxBc/transcript.json"
    with open(transcript_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    segments = data.get("segments", [])
    
    # Pre-existing phrases in translator
    existing_phrases = set()
    with open("tools/avatar_viewer/EnglishToISLTranslator.js", "r", encoding="utf-8") as f:
        js_content = f.read()
        m = re.findall(r"['\"]([^'\"]+)['\"]\s*:", js_content)
        for term in m:
            if " " in term:
                existing_phrases.add(term.lower().strip())

    # Build sentences and n-grams
    sentences = []
    phrase_contexts = {}
    ngram_counter = Counter()

    for seg in segments:
        text = seg.get("text", "").lower()
        clean = re.sub(r"[^a-z0-9'\s]", " ", text)
        words = clean.split()
        if not words:
            continue
        
        sentences.append((words, seg.get("text", "")))

        # 2-grams, 3-grams, 4-grams
        for n in [2, 3, 4]:
            for i in range(len(words) - n + 1):
                gram = " ".join(words[i:i+n])
                # Skip if already exists or trivial stopword combinations
                if gram not in existing_phrases:
                    ngram_counter[gram] += 1
                    if gram not in phrase_contexts:
                        phrase_contexts[gram] = []
                    if len(phrase_contexts[gram]) < 3:
                        phrase_contexts[gram].append({
                            "segment_id": seg.get("id"),
                            "timestamp": seg.get("start"),
                            "sentence": seg.get("text")
                        })

    # Filter meaningful candidates with count >= 2
    candidates = []
    for gram, cnt in ngram_counter.most_common():
        if cnt >= 2:
            # Basic heuristic: contains at least one content word (len >= 3)
            words = gram.split()
            if any(len(w) >= 3 and w not in ["the", "and", "that", "this", "with"] for w in words):
                candidates.append({
                    "phrase": gram,
                    "word_count": len(words),
                    "frequency": cnt,
                    "sample_context": phrase_contexts[gram][0]["sentence"] if phrase_contexts[gram] else ""
                })

    top_250 = candidates[:250]

    # 1. CSV
    with open("data/h22_phrase_frequency.csv", "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["rank", "phrase", "word_count", "frequency", "sample_context"])
        for idx, c in enumerate(top_250, 1):
            writer.writerow([idx, c["phrase"], c["word_count"], c["frequency"], c["sample_context"]])

    # 2. Candidates JSON
    with open("data/h22_phrase_candidates.json", "w", encoding="utf-8") as f:
        json.dump({
            "total_candidates_mined": len(top_250),
            "candidates": top_250
        }, f, indent=2)

    # 3. Contexts JSON
    contexts_export = {c["phrase"]: phrase_contexts.get(c["phrase"], []) for c in top_250}
    with open("data/h22_phrase_contexts.json", "w", encoding="utf-8") as f:
        json.dump(contexts_export, f, indent=2)

    print(f"Mined {len(top_250)} multiword phrase candidates.")
    print("Generated data/h22_phrase_frequency.csv, data/h22_phrase_candidates.json, data/h22_phrase_contexts.json.")

if __name__ == "__main__":
    mine_transcript_phrases()
