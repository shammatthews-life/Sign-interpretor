"""
tools/integrate_h24_batch13.py

Integrates Batch 13 (20 new signs, reaching 480 signs milestone) across:
- tools/build_corpus_lexicon.py
- tools/avatar_viewer/EnglishToISLTranslator.js
- tools/avatar_viewer/index.html
And regenerates data/isl_corpus_lexicon.json and data/isl_corpus_coverage.json.
"""

import json
from pathlib import Path
import subprocess

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# 1. Update tools/build_corpus_lexicon.py
bcl_path = PROJECT_ROOT / "tools" / "build_corpus_lexicon.py"
with open(bcl_path, "r", encoding="utf-8") as f:
    bcl_text = f.read()

target_bcl = '"conference", "door", "break", "road", "full", "past", "worth", "ten", "setting", "expectation", "server", "simply", "cannot", "dollar", "deep", "phenomenal", "record", "buy", "breathe", "billion"'
repl_bcl = target_bcl + ',\n    # Phase H24 Batch 13 Signs (20 authentic signs reaching 480 signs milestone)\n    "laugh", "soul", "meal", "follow", "fair", "statistics", "nose", "self", "angel", "math", "insane", "goosebumps", "pointless", "misunderstand", "tilt", "spend", "perceive", "upon", "fan", "decide"'

if target_bcl in bcl_text:
    bcl_text = bcl_text.replace(target_bcl, repl_bcl)
    with open(bcl_path, "w", encoding="utf-8") as f:
        f.write(bcl_text)
    print("Updated tools/build_corpus_lexicon.py with Batch 13 signs.")
else:
    print("Warning: target string not found in tools/build_corpus_lexicon.py!")

# 2. Update EnglishToISLTranslator.js
tr_path = PROJECT_ROOT / "tools" / "avatar_viewer" / "EnglishToISLTranslator.js"
with open(tr_path, "r", encoding="utf-8") as f:
    tr_text = f.read()

tr_avail_target = "billion: { playable: true }\n    };"
tr_avail_repl = """billion: { playable: true },
      // Phase H24 Batch 13 Playable Signs (20 signs reaching 480 total signs)
      laugh: { playable: true },
      soul: { playable: true },
      meal: { playable: true },
      follow: { playable: true },
      fair: { playable: true },
      statistics: { playable: true },
      nose: { playable: true },
      self: { playable: true },
      angel: { playable: true },
      math: { playable: true },
      insane: { playable: true },
      goosebumps: { playable: true },
      pointless: { playable: true },
      misunderstand: { playable: true },
      tilt: { playable: true },
      spend: { playable: true },
      perceive: { playable: true },
      upon: { playable: true },
      fan: { playable: true },
      decide: { playable: true }
    };"""

if tr_avail_target in tr_text:
    tr_text = tr_text.replace(tr_avail_target, tr_avail_repl)
elif tr_avail_target.replace("\n", "\r\n") in tr_text:
    tr_text = tr_text.replace(tr_avail_target.replace("\n", "\r\n"), tr_avail_repl.replace("\n", "\r\n"))

tr_dict_target = "['billion', 'BILLION'], ['billions', 'BILLION'],"
tr_dict_repl = """['billion', 'BILLION'], ['billions', 'BILLION'],
      // Phase H24 Batch 13 Lexical Mappings & Inflections
      ['laugh', 'LAUGH'], ['laughs', 'LAUGH'], ['laughing', 'LAUGH'], ['laughed', 'LAUGH'], ['laughter', 'LAUGH'],
      ['soul', 'SOUL'], ['souls', 'SOUL'],
      ['meal', 'MEAL'], ['meals', 'MEAL'], ['dinner', 'MEAL'], ['lunch', 'MEAL'],
      ['follow', 'FOLLOW'], ['follows', 'FOLLOW'], ['following', 'FOLLOW'], ['followed', 'FOLLOW'],
      ['fair', 'FAIR'], ['fairly', 'FAIR'], ['fairness', 'FAIR'], ['equal', 'FAIR'],
      ['statistics', 'STATISTICS'], ['stats', 'STATISTICS'], ['statistical', 'STATISTICS'],
      ['nose', 'NOSE'], ['noses', 'NOSE'],
      ['self', 'SELF'], ['selves', 'SELF'],
      ['angel', 'ANGEL'], ['angels', 'ANGEL'],
      ['math', 'MATH'], ['mathematics', 'MATH'],
      ['insane', 'INSANE'], ['insanity', 'INSANE'],
      ['goosebumps', 'GOOSEBUMPS'], ['goosebump', 'GOOSEBUMPS'],
      ['pointless', 'POINTLESS'], ['pointlessly', 'POINTLESS'],
      ['misunderstand', 'MISUNDERSTAND'], ['misunderstood', 'MISUNDERSTAND'], ['misunderstanding', 'MISUNDERSTAND'], ['misunderstands', 'MISUNDERSTAND'],
      ['tilt', 'TILT'], ['tilts', 'TILT'], ['tilted', 'TILT'], ['tilting', 'TILT'],
      ['spend', 'SPEND'], ['spends', 'SPEND'], ['spending', 'SPEND'], ['spent', 'SPEND'],
      ['perceive', 'PERCEIVE'], ['perceives', 'PERCEIVE'], ['perceived', 'PERCEIVE'], ['perceiving', 'PERCEIVE'], ['perception', 'PERCEIVE'],
      ['upon', 'UPON'],
      ['fan', 'FAN'], ['fans', 'FAN'],
      ['decide', 'DECIDE'], ['decides', 'DECIDE'], ['decided', 'DECIDE'], ['deciding', 'DECIDE'],"""

if tr_dict_target in tr_text:
    tr_text = tr_text.replace(tr_dict_target, tr_dict_repl)
elif tr_dict_target.replace("\n", "\r\n") in tr_text:
    tr_text = tr_text.replace(tr_dict_target.replace("\n", "\r\n"), tr_dict_repl.replace("\n", "\r\n"))

with open(tr_path, "w", encoding="utf-8") as f:
    f.write(tr_text)
print("Updated EnglishToISLTranslator.js with Batch 13 signs.")

# 3. Update index.html sign preloads
with open(PROJECT_ROOT / "signs" / "manifest.json", "r", encoding="utf-8") as f:
    manifest = json.load(f)

sign_ids = sorted([s["sign_id"] for s in manifest["signs"]])
idx_path = PROJECT_ROOT / "tools" / "avatar_viewer" / "index.html"
with open(idx_path, "r", encoding="utf-8") as f:
    idx_text = f.read()

pos_start = idx_text.find("const preload = await signLibrary.preload(")
if pos_start != -1:
    pos_open = idx_text.find("[", pos_start)
    pos_close = idx_text.find("]", pos_open)
    idx_text = idx_text[:pos_open] + json.dumps(sign_ids) + idx_text[pos_close+1:]
    with open(idx_path, "w", encoding="utf-8") as f:
        f.write(idx_text)
    print(f"Updated tools/avatar_viewer/index.html with {len(sign_ids)} signs.")

# 4. Rebuild Corpus Lexicon
print("\nRebuilding corpus lexicon...")
res = subprocess.run(["python", "tools/build_corpus_lexicon.py"], capture_output=True, text=True, cwd=str(PROJECT_ROOT))
print(res.stdout)
if res.stderr:
    print(res.stderr)
