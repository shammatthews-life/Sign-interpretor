import json

with open("data/h29_remaining_fallback_inventory.json", "r", encoding="utf-8") as f:
    d = json.load(f)

items = d["fallback_concepts"]
candidates = []
for it in items:
    lemma = it["lemma"].lower()
    if not any(c.isdigit() for c in lemma) and it["frequency"] in {4, 5}:
        candidates.append((lemma, it["frequency"]))

print("Candidates freq 4-5:", candidates[:50])
