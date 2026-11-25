"""
tools/patch_build_corpus_lexicon.py

Clean patch for tools/build_corpus_lexicon.py for Phase H21.
"""

from pathlib import Path

BUILD_PATH = Path(__file__).resolve().parent / "build_corpus_lexicon.py"

with open(BUILD_PATH, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add 25 signs to PLAYABLE_SIGNS
NEW_25_SIGNS = [
    "art", "audience", "college", "draw", "energy", "example",
    "game", "lead", "line", "mark", "note", "parent",
    "pause", "plan", "posture", "power", "reason", "rule",
    "simple", "space", "speed", "step", "teach", "topic", "train"
]

target_anchor = '"fine", "somewhere"'
new_signs_str = ',\n    # Phase H21 High-Impact Lexical Signs\n    ' + ', '.join(f'"{s}"' for s in NEW_25_SIGNS)

if target_anchor in content and '"teach"' not in content:
    content = content.replace(target_anchor, target_anchor + new_signs_str, 1)
    print("Added 25 signs to PLAYABLE_SIGNS.")

# 2. Add H21 inflections inside LEMMA_MAP
inflections = [
    ("steps", "step"), ("stepping", "step"),
    ("audiences", "audience"), ("pauses", "pause"), ("pausing", "pause"),
    ("rules", "rule"), ("lines", "line"), ("spaces", "space"),
    ("powers", "power"), ("games", "game"), ("speeds", "speed"),
    ("postures", "posture"), ("leads", "lead"), ("leading", "lead"),
    ("notes", "note"), ("plans", "plan"), ("planning", "plan"),
    ("trains", "train"), ("training", "train"), ("draws", "draw"),
    ("drawing", "draw"), ("marks", "mark"), ("marking", "mark"),
    ("reasons", "reason"), ("examples", "example"), ("topics", "topic"),
    ("colleges", "college"), ("parents", "parent"), ("teaches", "teach"),
    ("teaching", "teach")
]

lemma_additions = "    # Phase H21 Inflection Mappings\n"
for infl, base in inflections:
    lemma_additions += f'    "{infl}": "{base}",\n'

lemma_anchor = '"don\'t": "not", "can\'t": "not"'
if lemma_anchor in content and '"teaches": "teach"' not in content:
    content = content.replace(lemma_anchor, lemma_additions + "    " + lemma_anchor, 1)
    print("Added H21 inflections inside LEMMA_MAP.")

# 3. Ensure token in PLAYABLE_SIGNS takes precedence before LEMMA_MAP lookup
check_anchor = "            # Determine lemma\n            lemma = LEMMA_MAP.get(token, token)"
replacement_check = """            # Determine lemma (playable signs take precedence)
            if token in PLAYABLE_SIGNS:
                lemma = token
            else:
                lemma = LEMMA_MAP.get(token, token)"""

if check_anchor in content:
    content = content.replace(check_anchor, replacement_check, 1)
    print("Updated lemma determination logic to prioritize PLAYABLE_SIGNS.")

with open(BUILD_PATH, "w", encoding="utf-8") as f:
    f.write(content)

print("Patch applied successfully.")
