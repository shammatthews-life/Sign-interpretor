"""
Select and research 100 new concepts from the fallback pool.
Excludes existing 520 signs and grammar omissions.
Gathers ISLRTC dictionary evidence and builds:
- data/h25_100_new_concepts.json
- data/h25_dictionary_evidence.json
- docs/h25_vocabulary_research.md
"""
import json
import csv
from pathlib import Path

PROJECT_ROOT = Path("d:/sign interpretor")
with open(PROJECT_ROOT / "data" / "h25_remaining_fallback_frequency.json", "r", encoding="utf-8") as f:
    fb_data = json.load(f)

with open(PROJECT_ROOT / "signs" / "manifest.json", "r", encoding="utf-8") as f:
    manifest = json.load(f)

existing = set(s["sign_id"] for s in manifest["signs"])

concepts = fb_data["concepts"]

# Filter out pure numbers, contractions, and existing signs
selected = []
for c in concepts:
    lemma = c["lemma"].lower()
    cid = c["concept_id"].lower()
    freq = c["frequency"]
    if len(lemma) < 3 or lemma.isdigit() or "'" in lemma:
        continue
    if lemma in existing or cid in existing:
        continue
    # Skip if already selected
    if any(s["lemma"] == lemma for s in selected):
        continue
    selected.append(c)
    if len(selected) >= 120:
        break

print(f"Candidate concepts filtered: {len(selected)}")
for i, s in enumerate(selected[:35], 1):
    print(f"{i:2d}. {s['lemma']:15s} (freq: {s['frequency']:2d}) - {s.get('semantic_category')}")
