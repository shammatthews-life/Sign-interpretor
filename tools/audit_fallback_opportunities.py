import json
from pathlib import Path

PROJECT_ROOT = Path("d:/sign interpretor")
with open(PROJECT_ROOT / "data" / "h29_remaining_fallback_inventory.json", "r", encoding="utf-8") as f:
    fdata = json.load(f)
fallbacks = fdata["fallback_concepts"]

with open(PROJECT_ROOT / "signs" / "manifest.json", "r", encoding="utf-8") as f:
    manifest = json.load(f)
playable_ids = {s["sign_id"].lower() for s in manifest.get("signs", [])}

# Check inflections pointing to playable signs
inflection_recoverable = []
digits_recoverable = []
proper_nouns = []
high_impact_lexical_candidates = []

DIGIT_MAP = {
    "1": "one", "2": "two", "6": "six", "7": "seven", "10": "ten", "billion": "billion"
}

for r in fallbacks:
    lemma = r["lemma"].lower()
    freq = r["frequency"]

    # Check digits
    if lemma in DIGIT_MAP:
        digits_recoverable.append((lemma, DIGIT_MAP[lemma], freq))
        continue

    # Check direct inflection stripping
    candidate_base = None
    if lemma.endswith("s") and lemma[:-1] in playable_ids:
        candidate_base = lemma[:-1]
    elif lemma.endswith("es") and lemma[:-2] in playable_ids:
        candidate_base = lemma[:-2]
    elif lemma.endswith("ing") and lemma[:-3] in playable_ids:
        candidate_base = lemma[:-3]
    elif lemma.endswith("ed") and lemma[:-2] in playable_ids:
        candidate_base = lemma[:-2]
    elif lemma.endswith("ed") and lemma[:-1] in playable_ids:
        candidate_base = lemma[:-1]
    elif lemma.endswith("er") and lemma[:-2] in playable_ids:
        candidate_base = lemma[:-2]
    elif lemma.endswith("er") and lemma[:-1] in playable_ids:
        candidate_base = lemma[:-1]
    elif lemma.endswith("'s") and lemma[:-2] in playable_ids:
        candidate_base = lemma[:-2]
    elif lemma == "won't":
        candidate_base = "will"

    if candidate_base:
        inflection_recoverable.append((lemma, candidate_base, freq))
    elif r["semantic_category"] == "Proper Noun" or lemma in {"lars", "ted", "julian"}:
        proper_nouns.append((lemma, freq))
    elif freq >= 3:
        high_impact_lexical_candidates.append((lemma, freq, r["example_sentences"][:1]))

print(f"Total fallback concepts: {len(fallbacks)}")
print(f"Inflections of existing playable signs: {len(inflection_recoverable)} concepts ({sum(x[2] for x in inflection_recoverable)} tokens)")
print(f"Sample inflections:", inflection_recoverable[:15])
print(f"\nDigits recoverable: {len(digits_recoverable)} concepts ({sum(x[2] for x in digits_recoverable)} tokens)")
print(f"Sample digits:", digits_recoverable)
print(f"\nProper nouns recoverable via fingerspelling: {len(proper_nouns)} concepts ({sum(x[1] for x in proper_nouns)} tokens)")
print(f"\nHigh impact lexical candidates (freq >= 3): {len(high_impact_lexical_candidates)} concepts ({sum(x[1] for x in high_impact_lexical_candidates)} tokens)")
print("Top high impact lexical candidates:")
for item in high_impact_lexical_candidates[:20]:
    print(f"  {item[0].ljust(15)} : freq {item[1]}")
