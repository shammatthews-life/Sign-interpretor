"""
tools/integrate_h24_batch14.py

Integrates Batch 14 (20 new signs, reaching landmark 500 signs milestone) across:
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

target_bcl = '"laugh", "soul", "meal", "follow", "fair", "statistics", "nose", "self", "angel", "math", "insane", "goosebumps", "pointless", "misunderstand", "tilt", "spend", "perceive", "upon", "fan", "decide"'
repl_bcl = target_bcl + ',\n    # Phase H24 Batch 14 Signs (20 authentic signs reaching landmark 500 signs milestone)\n    "test", "village", "street", "cloak", "average", "dry", "attract", "grab", "send", "behavior", "effect", "belief", "failure", "gray", "nowhere", "burden", "observant", "kid", "set", "result"'

if target_bcl in bcl_text:
    bcl_text = bcl_text.replace(target_bcl, repl_bcl)
    with open(bcl_path, "w", encoding="utf-8") as f:
        f.write(bcl_text)
    print("Updated tools/build_corpus_lexicon.py with Batch 14 signs.")
else:
    print("Warning: target string not found in tools/build_corpus_lexicon.py!")

# 2. Update EnglishToISLTranslator.js
tr_path = PROJECT_ROOT / "tools" / "avatar_viewer" / "EnglishToISLTranslator.js"
with open(tr_path, "r", encoding="utf-8") as f:
    tr_text = f.read()

tr_avail_target = "decide: { playable: true }\n    };"
tr_avail_repl = """decide: { playable: true },
      // Phase H24 Batch 14 Playable Signs (20 signs reaching 500 total signs)
      test: { playable: true },
      village: { playable: true },
      street: { playable: true },
      cloak: { playable: true },
      average: { playable: true },
      dry: { playable: true },
      attract: { playable: true },
      grab: { playable: true },
      send: { playable: true },
      behavior: { playable: true },
      effect: { playable: true },
      belief: { playable: true },
      failure: { playable: true },
      gray: { playable: true },
      nowhere: { playable: true },
      burden: { playable: true },
      observant: { playable: true },
      kid: { playable: true },
      set: { playable: true },
      result: { playable: true }
    };"""

if tr_avail_target in tr_text:
    tr_text = tr_text.replace(tr_avail_target, tr_avail_repl)
elif tr_avail_target.replace("\n", "\r\n") in tr_text:
    tr_text = tr_text.replace(tr_avail_target.replace("\n", "\r\n"), tr_avail_repl.replace("\n", "\r\n"))

tr_dict_target = "['decide', 'DECIDE'], ['decides', 'DECIDE'], ['decided', 'DECIDE'], ['deciding', 'DECIDE'],"
tr_dict_repl = """['decide', 'DECIDE'], ['decides', 'DECIDE'], ['decided', 'DECIDE'], ['deciding', 'DECIDE'],
      // Phase H24 Batch 14 Lexical Mappings & Inflections
      ['test', 'TEST'], ['tests', 'TEST'], ['tested', 'TEST'], ['testing', 'TEST'],
      ['village', 'VILLAGE'], ['villages', 'VILLAGE'],
      ['street', 'STREET'], ['streets', 'STREET'],
      ['cloak', 'CLOAK'], ['cloaks', 'CLOAK'], ['mantle', 'CLOAK'],
      ['average', 'AVERAGE'], ['averages', 'AVERAGE'], ['averaged', 'AVERAGE'],
      ['dry', 'DRY'], ['dryer', 'DRY'], ['drying', 'DRY'], ['dried', 'DRY'],
      ['attract', 'ATTRACT'], ['attracts', 'ATTRACT'], ['attracted', 'ATTRACT'], ['attracting', 'ATTRACT'], ['attraction', 'ATTRACT'],
      ['grab', 'GRAB'], ['grabs', 'GRAB'], ['grabbed', 'GRAB'], ['grabbing', 'GRAB'],
      ['send', 'SEND'], ['sends', 'SEND'], ['sending', 'SEND'], ['sent', 'SEND'],
      ['behavior', 'BEHAVIOR'], ['behaviors', 'BEHAVIOR'], ['behavioral', 'BEHAVIOR'],
      ['effect', 'EFFECT'], ['effects', 'EFFECT'], ['effective', 'EFFECT'],
      ['belief', 'BELIEF'], ['beliefs', 'BELIEF'],
      ['failure', 'FAILURE'], ['failures', 'FAILURE'],
      ['gray', 'GRAY'], ['grey', 'GRAY'], ['grayscale', 'GRAY'],
      ['nowhere', 'NOWHERE'],
      ['burden', 'BURDEN'], ['burdens', 'BURDEN'], ['liability', 'BURDEN'],
      ['observant', 'OBSERVANT'], ['observance', 'OBSERVANT'],
      ['kid', 'KID'], ['kidding', 'KID'], ['kids', 'KID'], ['kidded', 'KID'],
      ['set', 'SET'], ['sets', 'SET'], ['setting', 'SET'], ['setup', 'SET'],
      ['result', 'RESULT'], ['results', 'RESULT'], ['resulted', 'RESULT'], ['resulting', 'RESULT'],"""

if tr_dict_target in tr_text:
    tr_text = tr_text.replace(tr_dict_target, tr_dict_repl)
elif tr_dict_target.replace("\n", "\r\n") in tr_text:
    tr_text = tr_text.replace(tr_dict_target.replace("\n", "\r\n"), tr_dict_repl.replace("\n", "\r\n"))

with open(tr_path, "w", encoding="utf-8") as f:
    f.write(tr_text)
print("Updated EnglishToISLTranslator.js with Batch 14 signs.")

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
