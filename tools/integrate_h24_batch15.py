"""
tools/integrate_h24_batch15.py

Integrates Batch 15 (20 new signs, reaching 520 signs total) across:
- tools/build_corpus_lexicon.py
- tools/avatar_viewer/EnglishToISLTranslator.js
- tools/avatar_viewer/index.html
- tools/test_aether_h24_motions.mjs
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

target_bcl = '"test", "village", "street", "cloak", "average", "dry", "attract", "grab", "send", "behavior", "effect", "belief", "failure", "gray", "nowhere", "burden", "observant", "kid", "set", "result"'
repl_bcl = target_bcl + ',\n    # Phase H24 Batch 15 Signs (20 authentic signs reaching 520 signs milestone)\n    "may", "hey", "boom", "sweden", "everything", "somebody", "anyone", "anything", "nothing", "until", "weird", "along", "quarter", "tumble", "fill", "danger", "conductor", "lie", "luxury", "turbo"'

if target_bcl in bcl_text:
    bcl_text = bcl_text.replace(target_bcl, repl_bcl)
    with open(bcl_path, "w", encoding="utf-8") as f:
        f.write(bcl_text)
    print("Updated tools/build_corpus_lexicon.py with Batch 15 signs.")
else:
    print("Warning: target string not found in tools/build_corpus_lexicon.py!")

# 2. Update EnglishToISLTranslator.js
tr_path = PROJECT_ROOT / "tools" / "avatar_viewer" / "EnglishToISLTranslator.js"
with open(tr_path, "r", encoding="utf-8") as f:
    tr_text = f.read()

tr_avail_target = "result: { playable: true }\n    };"
tr_avail_repl = """result: { playable: true },
      // Phase H24 Batch 15 Playable Signs (20 signs reaching 520 total signs)
      may: { playable: true },
      hey: { playable: true },
      boom: { playable: true },
      sweden: { playable: true },
      everything: { playable: true },
      somebody: { playable: true },
      anyone: { playable: true },
      anything: { playable: true },
      nothing: { playable: true },
      until: { playable: true },
      weird: { playable: true },
      along: { playable: true },
      quarter: { playable: true },
      tumble: { playable: true },
      fill: { playable: true },
      danger: { playable: true },
      conductor: { playable: true },
      lie: { playable: true },
      luxury: { playable: true },
      turbo: { playable: true }
    };"""

if tr_avail_target in tr_text:
    tr_text = tr_text.replace(tr_avail_target, tr_avail_repl)
elif tr_avail_target.replace("\n", "\r\n") in tr_text:
    tr_text = tr_text.replace(tr_avail_target.replace("\n", "\r\n"), tr_avail_repl.replace("\n", "\r\n"))

tr_dict_target = "['result', 'RESULT'], ['results', 'RESULT'], ['resulted', 'RESULT'], ['resulting', 'RESULT'],"
tr_dict_repl = """['result', 'RESULT'], ['results', 'RESULT'], ['resulted', 'RESULT'], ['resulting', 'RESULT'],
      // Phase H24 Batch 15 Lexical Mappings & Inflections
      ['may', 'MAY'], ['might', 'MAY'],
      ['hey', 'HEY'], ['hi', 'HEY'], ['hello', 'GREETING'],
      ['boom', 'BOOM'], ['booming', 'BOOM'],
      ['sweden', 'SWEDEN'], ['swedish', 'SWEDEN'],
      ['everything', 'EVERYTHING'],
      ['somebody', 'SOMEBODY'], ['someone', 'SOMEBODY'],
      ['anyone', 'ANYONE'], ['anybody', 'ANYONE'],
      ['anything', 'ANYTHING'],
      ['nothing', 'NOTHING'],
      ['until', 'UNTIL'], ['till', 'UNTIL'],
      ['weird', 'WEIRD'], ['weirdest', 'WEIRD'], ['odd', 'WEIRD'],
      ['along', 'ALONG'],
      ['quarter', 'QUARTER'], ['quarters', 'QUARTER'],
      ['tumble', 'TUMBLE'], ['tumbles', 'TUMBLE'], ['tumbling', 'TUMBLE'], ['tumbled', 'TUMBLE'],
      ['fill', 'FILL'], ['fills', 'FILL'], ['filling', 'FILL'], ['filled', 'FILL'],
      ['danger', 'DANGER'], ['dangerous', 'DANGER'],
      ['conductor', 'CONDUCTOR'], ['conductors', 'CONDUCTOR'],
      ['lie', 'LIE'], ['lies', 'LIE'], ['lying', 'LIE'], ['lied', 'LIE'],
      ['luxury', 'LUXURY'], ['luxurious', 'LUXURY'],
      ['turbo', 'TURBO'],"""

if tr_dict_target in tr_text:
    tr_text = tr_text.replace(tr_dict_target, tr_dict_repl)
elif tr_dict_target.replace("\n", "\r\n") in tr_text:
    tr_text = tr_text.replace(tr_dict_target.replace("\n", "\r\n"), tr_dict_repl.replace("\n", "\r\n"))

with open(tr_path, "w", encoding="utf-8") as f:
    f.write(tr_text)
print("Updated EnglishToISLTranslator.js with Batch 15 signs.")

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

# 4. Update test_aether_h24_motions.mjs
mjs_path = PROJECT_ROOT / "tools" / "test_aether_h24_motions.mjs"
with open(mjs_path, "r", encoding="utf-8") as f:
    mjs_text = f.read()

target_mjs = "'test', 'village', 'street', 'cloak', 'average', 'dry', 'attract', 'grab', 'send', 'behavior', 'effect', 'belief', 'failure', 'gray', 'nowhere', 'burden', 'observant', 'kid', 'set', 'result'"
repl_mjs = target_mjs + ",\n  // Batch 15 (20)\n  'may', 'hey', 'boom', 'sweden', 'everything', 'somebody', 'anyone', 'anything', 'nothing', 'until', 'weird', 'along', 'quarter', 'tumble', 'fill', 'danger', 'conductor', 'lie', 'luxury', 'turbo'"

if target_mjs in mjs_text:
    mjs_text = mjs_text.replace(target_mjs, repl_mjs)
    with open(mjs_path, "w", encoding="utf-8") as f:
        f.write(mjs_text)
    print("Updated tools/test_aether_h24_motions.mjs with Batch 15 signs.")

# 5. Rebuild Corpus Lexicon
print("\nRebuilding corpus lexicon...")
res = subprocess.run(["python", "tools/build_corpus_lexicon.py"], capture_output=True, text=True, cwd=str(PROJECT_ROOT))
print(res.stdout)
if res.stderr:
    print(res.stderr)
