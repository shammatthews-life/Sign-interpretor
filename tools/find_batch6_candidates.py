import json

with open("data/isl_corpus_lexicon.json", "r", encoding="utf-8") as f:
    data = json.load(f)

fallback = [item for item in data if item.get("fallback_required") == True and not item.get("lemma", "").isdigit()]
fallback.sort(key=lambda x: x.get("frequency", 0), reverse=True)

print(f"Remaining non-numeric fallback concepts: {len(fallback)}")
print("Next 50 candidate words by frequency (51-100):")
for i, item in enumerate(fallback[50:100], 51):
    lemma = item.get("lemma")
    freq = item.get("frequency")
    sem = item.get("semantic_category", "")
    print(f"{i:2d}. {lemma:<16} freq={freq:<2} sem={sem}")
