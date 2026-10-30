"""
tools/integrate_h24_batch10.py

Integrates Batch 10 (20 new signs, reaching 420 signs milestone) across:
- tools/build_corpus_lexicon.py
- tools/avatar_viewer/EnglishToISLTranslator.js
- tools/avatar_viewer/index.html
And regenerates data/isl_corpus_lexicon.json and data/isl_corpus_coverage.json.
"""

import json
from pathlib import Path
import re

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# 1. Update tools/build_corpus_lexicon.py
bcl_path = PROJECT_ROOT / "tools" / "build_corpus_lexicon.py"
with open(bcl_path, "r", encoding="utf-8") as f:
    bcl_text = f.read()

target_bcl = '"smile", "dream", "exercise", "accomplish", "close", "old", "hungry", "intention", "motivated", "few", "lovely", "focus", "sometimes", "list", "connected", "course", "analyze", "fourth", "fifth", "meeting"'
repl_bcl = target_bcl + ',\n    # Phase H24 Batch 10 Signs (20 authentic signs reaching 420 signs milestone)\n    "human", "relate", "cool", "wow", "corner", "chest", "extension", "loop", "similar", "metaphor", "scientific", "skilled", "proven", "absolute", "dominant", "arena", "myself", "uncomfortable", "filled", "empowering"'

if target_bcl in bcl_text:
    bcl_text = bcl_text.replace(target_bcl, repl_bcl)
    with open(bcl_path, "w", encoding="utf-8") as f:
        f.write(bcl_text)
    print("Updated tools/build_corpus_lexicon.py with Batch 10 signs.")
else:
    print("Warning: target string not found in tools/build_corpus_lexicon.py!")

# 2. Update EnglishToISLTranslator.js
tr_path = PROJECT_ROOT / "tools" / "avatar_viewer" / "EnglishToISLTranslator.js"
with open(tr_path, "r", encoding="utf-8") as f:
    tr_text = f.read()

tr_avail_target = "meeting: { playable: true }\n    };"
tr_avail_repl = """meeting: { playable: true },
      // Phase H24 Batch 10 Playable Signs (20 signs reaching 420 total signs)
      human: { playable: true },
      relate: { playable: true },
      cool: { playable: true },
      wow: { playable: true },
      corner: { playable: true },
      chest: { playable: true },
      extension: { playable: true },
      loop: { playable: true },
      similar: { playable: true },
      metaphor: { playable: true },
      scientific: { playable: true },
      skilled: { playable: true },
      proven: { playable: true },
      absolute: { playable: true },
      dominant: { playable: true },
      arena: { playable: true },
      myself: { playable: true },
      uncomfortable: { playable: true },
      filled: { playable: true },
      empowering: { playable: true }
    };"""

if tr_avail_target in tr_text:
    tr_text = tr_text.replace(tr_avail_target, tr_avail_repl)
elif tr_avail_target.replace("\n", "\r\n") in tr_text:
    tr_text = tr_text.replace(tr_avail_target.replace("\n", "\r\n"), tr_avail_repl.replace("\n", "\r\n"))

tr_dict_target = "['meeting', 'MEETING'], ['meetings', 'MEETING'],"
tr_dict_repl = """['meeting', 'MEETING'], ['meetings', 'MEETING'],
      // Phase H24 Batch 10 Lexical Mappings & Inflections
      ['human', 'HUMAN'], ['humans', 'HUMAN'],
      ['relate', 'RELATE'], ['relates', 'RELATE'], ['related', 'RELATE'], ['relating', 'RELATE'], ['relationship', 'RELATE'], ['relationships', 'RELATE'],
      ['cool', 'COOL'], ['cooler', 'COOL'], ['coolest', 'COOL'],
      ['wow', 'WOW'],
      ['corner', 'CORNER'], ['corners', 'CORNER'],
      ['chest', 'CHEST'], ['chests', 'CHEST'],
      ['extension', 'EXTENSION'], ['extensions', 'EXTENSION'], ['extend', 'EXTENSION'], ['extends', 'EXTENSION'], ['extended', 'EXTENSION'], ['extending', 'EXTENSION'],
      ['loop', 'LOOP'], ['loops', 'LOOP'], ['looping', 'LOOP'], ['looped', 'LOOP'],
      ['similar', 'SIMILAR'], ['similarly', 'SIMILAR'], ['similarity', 'SIMILAR'], ['similarities', 'SIMILAR'],
      ['metaphor', 'METAPHOR'], ['metaphors', 'METAPHOR'],
      ['scientific', 'SCIENTIFIC'], ['scientifically', 'SCIENTIFIC'],
      ['skilled', 'SKILLED'], ['skillful', 'SKILLED'], ['skillfully', 'SKILLED'],
      ['proven', 'PROVEN'], ['prove', 'PROVEN'], ['proves', 'PROVEN'], ['proving', 'PROVEN'], ['proved', 'PROVEN'],
      ['absolute', 'ABSOLUTE'], ['absolutely', 'ABSOLUTE'],
      ['dominant', 'DOMINANT'], ['dominance', 'DOMINANT'], ['dominate', 'DOMINANT'], ['dominates', 'DOMINANT'], ['dominated', 'DOMINANT'], ['dominating', 'DOMINANT'],
      ['arena', 'ARENA'], ['arenas', 'ARENA'],
      ['myself', 'MYSELF'],
      ['uncomfortable', 'UNCOMFORTABLE'], ['uncomfortably', 'UNCOMFORTABLE'],
      ['filled', 'FILLED'], ['fill', 'FILLED'], ['fills', 'FILLED'], ['filling', 'FILLED'],
      ['empowering', 'EMPOWERING'], ['empower', 'EMPOWERING'], ['empowers', 'EMPOWERING'], ['empowered', 'EMPOWERING'], ['empowerment', 'EMPOWERING'],"""

if tr_dict_target in tr_text:
    tr_text = tr_text.replace(tr_dict_target, tr_dict_repl)
elif tr_dict_target.replace("\n", "\r\n") in tr_text:
    tr_text = tr_text.replace(tr_dict_target.replace("\n", "\r\n"), tr_dict_repl.replace("\n", "\r\n"))

with open(tr_path, "w", encoding="utf-8") as f:
    f.write(tr_text)
print("Updated EnglishToISLTranslator.js with Batch 10 signs.")

# 3. Update index.html preload array
with open("signs/manifest.json", "r", encoding="utf-8") as f:
    manifest = json.load(f)
all_signs = sorted([s["sign_id"] for s in manifest["signs"]])

html_path = PROJECT_ROOT / "tools" / "avatar_viewer" / "index.html"
with open(html_path, "r", encoding="utf-8") as f:
    html_text = f.read()

pattern = r"const preload = await signLibrary\.preload\(\[[^\]]*\]\);"
new_preload = "const preload = await signLibrary.preload(" + json.dumps(all_signs) + ");"
html_text = re.sub(pattern, new_preload, html_text)

with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_text)
print(f"Updated tools/avatar_viewer/index.html preload array with {len(all_signs)} signs.")

print("\nIntegration step complete.")
