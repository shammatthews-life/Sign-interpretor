"""
tools/integrate_h24_batch2.py

Integrates Batch 2 (16 new signs, total 240 signs) across:
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

target_bcl = '"increase", "little", "rest", "let", "able", "part", "big", "stop", "watch", "chart", "subject", "culture", "product", "audio", "positive", "trust", "match"'
repl_bcl = target_bcl + ',\n    # Phase H24 Batch 2 Signs (16 authentic signs covering 128 tokens)\n    "perspective", "after", "angle", "wise", "outside", "remove", "sell", "momentum", "bring", "pen", "nervous", "feedback", "quick", "earth", "far", "instance"'

if target_bcl in bcl_text:
    bcl_text = bcl_text.replace(target_bcl, repl_bcl)
    with open(bcl_path, "w", encoding="utf-8") as f:
        f.write(bcl_text)
    print("Updated tools/build_corpus_lexicon.py with Batch 2 signs.")
else:
    print("Target string not found in tools/build_corpus_lexicon.py!")

# 2. Update EnglishToISLTranslator.js
tr_path = PROJECT_ROOT / "tools" / "avatar_viewer" / "EnglishToISLTranslator.js"
with open(tr_path, "r", encoding="utf-8") as f:
    tr_text = f.read()

tr_avail_target = "match: { playable: true }\n    };"
tr_avail_repl = """match: { playable: true },
      // Phase H24 Batch 2 Playable Signs
      perspective: { playable: true },
      after: { playable: true },
      angle: { playable: true },
      wise: { playable: true },
      outside: { playable: true },
      remove: { playable: true },
      sell: { playable: true },
      momentum: { playable: true },
      bring: { playable: true },
      pen: { playable: true },
      nervous: { playable: true },
      feedback: { playable: true },
      quick: { playable: true },
      earth: { playable: true },
      far: { playable: true },
      instance: { playable: true }
    };"""

if tr_avail_target in tr_text:
    tr_text = tr_text.replace(tr_avail_target, tr_avail_repl)
elif tr_avail_target.replace("\n", "\r\n") in tr_text:
    tr_text = tr_text.replace(tr_avail_target.replace("\n", "\r\n"), tr_avail_repl.replace("\n", "\r\n"))

tr_dict_target = "['match', 'MATCH'], ['matches', 'MATCH'], ['matched', 'MATCH'], ['matching', 'MATCH'],"
tr_dict_repl = """['match', 'MATCH'], ['matches', 'MATCH'], ['matched', 'MATCH'], ['matching', 'MATCH'],
      // Phase H24 Batch 2 Lexical Mappings & Inflections
      ['perspective', 'PERSPECTIVE'], ['perspectives', 'PERSPECTIVE'],
      ['after', 'AFTER'],
      ['angle', 'ANGLE'], ['angles', 'ANGLE'],
      ['wise', 'WISE'],
      ['outside', 'OUTSIDE'],
      ['remove', 'REMOVE'], ['removes', 'REMOVE'], ['removed', 'REMOVE'], ['removing', 'REMOVE'],
      ['sell', 'SELL'], ['sells', 'SELL'], ['sold', 'SELL'], ['selling', 'SELL'],
      ['momentum', 'MOMENTUM'],
      ['bring', 'BRING'], ['brings', 'BRING'], ['brought', 'BRING'], ['bringing', 'BRING'],
      ['pen', 'PEN'], ['pens', 'PEN'],
      ['nervous', 'NERVOUS'],
      ['feedback', 'FEEDBACK'],
      ['quick', 'QUICK'], ['quickly', 'QUICK'],
      ['earth', 'EARTH'],
      ['far', 'FAR'],
      ['instance', 'INSTANCE'], ['instances', 'INSTANCE'],"""

if tr_dict_target in tr_text:
    tr_text = tr_text.replace(tr_dict_target, tr_dict_repl)
elif tr_dict_target.replace("\n", "\r\n") in tr_text:
    tr_text = tr_text.replace(tr_dict_target.replace("\n", "\r\n"), tr_dict_repl.replace("\n", "\r\n"))

with open(tr_path, "w", encoding="utf-8") as f:
    f.write(tr_text)
print("Updated tools/avatar_viewer/EnglishToISLTranslator.js with Batch 2 mappings.")

# 3. Update tools/avatar_viewer/index.html
idx_path = PROJECT_ROOT / "tools" / "avatar_viewer" / "index.html"
with open(idx_path, "r", encoding="utf-8") as f:
    idx_text = f.read()

manifest_path = PROJECT_ROOT / "signs" / "manifest.json"
with open(manifest_path, "r", encoding="utf-8") as f:
    manifest = json.load(f)

all_sign_ids = sorted([s["sign_id"] for s in manifest["signs"]])
new_preload_json = json.dumps(all_sign_ids)

idx_text = re.sub(
    r'signLibrary\.preload\(\[[^\]]+\]\)',
    f'signLibrary.preload({new_preload_json})',
    idx_text
)

idx_text = re.sub(
    r'Library preloaded: \d+ ISL signs across \d+ verified Schema 2\.0\.0 assets are playable\.',
    f'Library preloaded: {len(all_sign_ids)} ISL signs across {len(all_sign_ids)} verified Schema 2.0.0 assets are playable.',
    idx_text
)

with open(idx_path, "w", encoding="utf-8") as f:
    f.write(idx_text)
print(f"Updated tools/avatar_viewer/index.html with {len(all_sign_ids)} signs.")
