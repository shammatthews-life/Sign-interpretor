"""
tools/patch_multiword_phrases.py

Phase H22 Coordinator: Integrates Worker B's researched multiword phrases
into tools/build_corpus_lexicon.py and tools/avatar_viewer/EnglishToISLTranslator.js.
Ensures longest-match precedence and full accounting reproducibility.
"""

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
BUILD_PATH = PROJECT_ROOT / "tools" / "build_corpus_lexicon.py"
TRANS_PATH = PROJECT_ROOT / "tools" / "avatar_viewer" / "EnglishToISLTranslator.js"

# Load H22 mined phrases
with open(PROJECT_ROOT / "data" / "h22_phrase_integration_report.json", "r", encoding="utf-8") as f:
    report = json.load(f)

# High-yield multiword expressions to integrate:
# Curated phrases from H21/H22 research where target glosses exist in our 207-sign library
HIGH_YIELD_PHRASES = [
    ("i'm going to show", ["I", "GOING_TO", "SHOW"], "Future intentional demonstration construct"),
    ("going to show you", ["GOING_TO", "SHOW", "YOU"], "Future interpersonal demonstration compound"),
    ("i'm going to give", ["I", "GOING_TO", "GIVE"], "Future interpersonal transfer construct"),
    ("going to give you", ["GOING_TO", "GIVE", "YOU"], "Future transfer to interlocutor"),
    ("want to show you", ["WANT", "SHOW", "YOU"], "Volitional demonstration construct"),
    ("want to give you", ["WANT", "GIVE", "YOU"], "Volitional transfer construct"),
    ("as you can see", ["YOU", "CAN", "SEE"], "Deictic visual perceptual discourse formula"),
    ("the reason why", ["REASON"], "Explanatory causal discourse particle"),
    ("give you an example", ["GIVE", "YOU", "EXAMPLE"], "Pedagogical exemplification compound"),
    ("take a look", ["LOOK"], "Directional gaze construct"),
    ("take a look at", ["LOOK"], "Directional gaze construct"),
    ("pay attention to", ["ATTENTION"], "Pedagogical focus directive"),
    ("step by step", ["STEP", "STEP"], "Sequential procedural discourse idiom"),
    ("first of all", ["FIRST"], "Initial procedural ordering formula"),
    ("let me know", ["TELL", "ME"], "Interpersonal communicative request"),
    ("make sure that", ["TRUE"], "Epistemic verification formula"),
    ("listen to this", ["HEAR"], "Auditory attention directive"),
    ("in other words", ["MEAN"], "Reformulative discourse marker"),
    ("on the stage", ["STAGE"], "Spatial lecture locator"),
    ("in the classroom", ["CLASS"], "Institutional spatial locator"),
    ("public speaking challenge", ["SAY", "PEOPLE", "CHALLENGE"], "Lecture theme tripartite compound"),
    ("great job", ["GREAT", "WORK"], "Positive evaluation formula"),
    ("talk to you", ["SAY", "YOU"], "Interpersonal communication predicate"),
    ("look like", ["SAME"], "Comparative visual similarity construct")
]

# 1. Update tools/build_corpus_lexicon.py
with open(BUILD_PATH, "r", encoding="utf-8") as f:
    build_code = f.read()

phrase_insert_str = "\n    # Phase H22 High-Yield Multiword Educational Expressions\n"
for p, glosses, desc in HIGH_YIELD_PHRASES:
    if f'"{p}"' not in build_code and f"'{p}'" not in build_code:
        gloss_str = "[" + ", ".join(f'"{g}"' for g in glosses) + "]"
        phrase_insert_str += f'    ("{p}", {gloss_str}, "{desc}"),\n'

# Insert after ("high level", ["HIGH", "LEVEL"], "Broad overview conceptual compound"),
anchor = '("high level", ["HIGH", "LEVEL"], "Broad overview conceptual compound"),'
if anchor in build_code and '"step by step"' not in build_code:
    build_code = build_code.replace(anchor, anchor + phrase_insert_str, 1)
    with open(BUILD_PATH, "w", encoding="utf-8") as f:
        f.write(build_code)
    print("Patched tools/build_corpus_lexicon.py with Phase H22 phrases.")
else:
    print("build_corpus_lexicon.py already contains H22 phrases or anchor missing.")

# 2. Update tools/avatar_viewer/EnglishToISLTranslator.js
with open(TRANS_PATH, "r", encoding="utf-8") as f:
    trans_code = f.read()

trans_phrase_additions = "\n      // Phase H22 Curated High-Yield Multiword Phrases\n"
for p, glosses, desc in HIGH_YIELD_PHRASES:
    if f"['{p}'," not in trans_code and f'["{p}",' not in trans_code:
        gloss_str = "[" + ", ".join(f"'{g}'" for g in glosses) + "]"
        trans_phrase_additions += f"      ['{p}', {gloss_str}],\n"

trans_anchor = "['as well as', ['AND', 'ALSO']],"
if trans_anchor in trans_code and "'step by step'" not in trans_code:
    trans_code = trans_code.replace(trans_anchor, trans_anchor + trans_phrase_additions, 1)
    with open(TRANS_PATH, "w", encoding="utf-8") as f:
        f.write(trans_code)
    print("Patched EnglishToISLTranslator.js with Phase H22 phrases.")
else:
    print("EnglishToISLTranslator.js already contains H22 phrases or anchor missing.")
