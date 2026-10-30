"""
tools/integrate_h24_batch12.py

Integrates Batch 12 (20 new signs, reaching 460 signs milestone) across:
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

target_bcl = '"wait", "pattern", "front", "fall", "mobile", "ignore", "under", "certain", "subtle", "scream", "everyday", "emotional", "connect", "extent", "longer", "ultimate", "somatic", "synchronicity", "sat", "united"'
repl_bcl = target_bcl + ',\n    # Phase H24 Batch 12 Signs (20 authentic signs reaching 460 signs milestone)\n    "conference", "door", "break", "road", "full", "past", "worth", "ten", "setting", "expectation", "server", "simply", "cannot", "dollar", "deep", "phenomenal", "record", "buy", "breathe", "billion"'

if target_bcl in bcl_text:
    bcl_text = bcl_text.replace(target_bcl, repl_bcl)
    with open(bcl_path, "w", encoding="utf-8") as f:
        f.write(bcl_text)
    print("Updated tools/build_corpus_lexicon.py with Batch 12 signs.")
else:
    print("Warning: target string not found in tools/build_corpus_lexicon.py!")

# 2. Update EnglishToISLTranslator.js
tr_path = PROJECT_ROOT / "tools" / "avatar_viewer" / "EnglishToISLTranslator.js"
with open(tr_path, "r", encoding="utf-8") as f:
    tr_text = f.read()

tr_avail_target = "united: { playable: true }\n    };"
tr_avail_repl = """united: { playable: true },
      // Phase H24 Batch 12 Playable Signs (20 signs reaching 460 total signs)
      conference: { playable: true },
      door: { playable: true },
      break: { playable: true },
      road: { playable: true },
      full: { playable: true },
      past: { playable: true },
      worth: { playable: true },
      ten: { playable: true },
      setting: { playable: true },
      expectation: { playable: true },
      server: { playable: true },
      simply: { playable: true },
      cannot: { playable: true },
      dollar: { playable: true },
      deep: { playable: true },
      phenomenal: { playable: true },
      record: { playable: true },
      buy: { playable: true },
      breathe: { playable: true },
      billion: { playable: true }
    };"""

if tr_avail_target in tr_text:
    tr_text = tr_text.replace(tr_avail_target, tr_avail_repl)
elif tr_avail_target.replace("\n", "\r\n") in tr_text:
    tr_text = tr_text.replace(tr_avail_target.replace("\n", "\r\n"), tr_avail_repl.replace("\n", "\r\n"))

tr_dict_target = "['united', 'UNITED'], ['unite', 'UNITED'], ['unites', 'UNITED'], ['uniting', 'UNITED'], ['unity', 'UNITED'],"
tr_dict_repl = """['united', 'UNITED'], ['unite', 'UNITED'], ['unites', 'UNITED'], ['uniting', 'UNITED'], ['unity', 'UNITED'],
      // Phase H24 Batch 12 Lexical Mappings & Inflections
      ['conference', 'CONFERENCE'], ['conferences', 'CONFERENCE'], ['convention', 'CONFERENCE'], ['conventions', 'CONFERENCE'],
      ['door', 'DOOR'], ['doors', 'DOOR'],
      ['break', 'BREAK'], ['breaks', 'BREAK'], ['breaking', 'BREAK'], ['broke', 'BREAK'], ['broken', 'BREAK'],
      ['road', 'ROAD'], ['roads', 'ROAD'], ['street', 'ROAD'], ['path', 'ROAD'],
      ['full', 'FULL'], ['fully', 'FULL'], ['fuller', 'FULL'], ['fullest', 'FULL'],
      ['past', 'PAST'], ['history', 'PAST'], ['historical', 'PAST'],
      ['worth', 'WORTH'], ['worthy', 'WORTH'], ['value', 'WORTH'], ['values', 'WORTH'],
      ['ten', 'TEN'], ['tenth', 'TEN'],
      ['setting', 'SETTING'], ['settings', 'SETTING'], ['setup', 'SETTING'],
      ['expectation', 'EXPECTATION'], ['expectations', 'EXPECTATION'], ['expect', 'EXPECTATION'], ['expects', 'EXPECTATION'], ['expected', 'EXPECTATION'], ['expecting', 'EXPECTATION'],
      ['server', 'SERVER'], ['servers', 'SERVER'], ['serve', 'SERVER'], ['serves', 'SERVER'], ['serving', 'SERVER'], ['served', 'SERVER'],
      ['simply', 'SIMPLY'], ['simple', 'SIMPLY'], ['simpler', 'SIMPLY'], ['simplest', 'SIMPLY'], ['simplicity', 'SIMPLY'],
      ['cannot', 'CANNOT'], ["can't", 'CANNOT'], ["cant", 'CANNOT'],
      ['dollar', 'DOLLAR'], ['dollars', 'DOLLAR'], ['buck', 'DOLLAR'], ['bucks', 'DOLLAR'],
      ['deep', 'DEEP'], ['deeper', 'DEEP'], ['deepest', 'DEEP'], ['deeply', 'DEEP'], ['depth', 'DEEP'],
      ['phenomenal', 'PHENOMENAL'], ['phenomenally', 'PHENOMENAL'], ['phenomenon', 'PHENOMENAL'],
      ['record', 'RECORD'], ['records', 'RECORD'], ['recording', 'RECORD'], ['recorded', 'RECORD'],
      ['buy', 'BUY'], ['buys', 'BUY'], ['buying', 'BUY'], ['bought', 'BUY'], ['purchase', 'BUY'], ['purchased', 'BUY'],
      ['breathe', 'BREATHE'], ['breathes', 'BREATHE'], ['breathing', 'BREATHE'], ['breath', 'BREATHE'], ['breathed', 'BREATHE'],
      ['billion', 'BILLION'], ['billions', 'BILLION'],"""

if tr_dict_target in tr_text:
    tr_text = tr_text.replace(tr_dict_target, tr_dict_repl)
elif tr_dict_target.replace("\n", "\r\n") in tr_text:
    tr_text = tr_text.replace(tr_dict_target.replace("\n", "\r\n"), tr_dict_repl.replace("\n", "\r\n"))

with open(tr_path, "w", encoding="utf-8") as f:
    f.write(tr_text)
print("Updated EnglishToISLTranslator.js with Batch 12 signs.")

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
