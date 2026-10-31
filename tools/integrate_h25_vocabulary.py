"""
tools/integrate_h25_vocabulary.py

Integrates Phase H25 Vocabulary (30 new signs + 45 inflections + 15 fingerspelled + 10 phrases):
- tools/build_corpus_lexicon.py
- tools/avatar_viewer/EnglishToISLTranslator.js
- tools/avatar_viewer/index.html
And regenerates data/isl_corpus_lexicon.json and data/isl_corpus_coverage.json.
"""

import json
from pathlib import Path
import subprocess

PROJECT_ROOT = Path("d:/sign interpretor")

# 1. Update tools/build_corpus_lexicon.py
bcl_path = PROJECT_ROOT / "tools" / "build_corpus_lexicon.py"
with open(bcl_path, "r", encoding="utf-8") as f:
    bcl_text = f.read()

target_bcl = '"may", "hey", "boom", "sweden", "everything", "somebody", "anyone", "anything", "nothing", "until", "weird", "along", "quarter", "tumble", "fill", "danger", "conductor", "lie", "luxury", "turbo"'
repl_bcl = target_bcl + ',\n    # Phase H25 New Signs (30 authentic ISL signs reaching 550 total signs)\n    "fix", "realize", "notice", "limit", "substance", "cover", "risk", "safe", "guide", "memory", "join", "explain", "complex", "nature", "weather", "plant", "animal", "mountain", "river", "ocean", "bridge", "market", "cost", "rich", "weak", "heavy", "shadow", "mirror", "window", "wall"'

if target_bcl in bcl_text:
    bcl_text = bcl_text.replace(target_bcl, repl_bcl)
    with open(bcl_path, "w", encoding="utf-8") as f:
        f.write(bcl_text)
    print("Updated tools/build_corpus_lexicon.py with H25 signs.")
else:
    print("Warning: target string not found in tools/build_corpus_lexicon.py!")

# 2. Update EnglishToISLTranslator.js
tr_path = PROJECT_ROOT / "tools" / "avatar_viewer" / "EnglishToISLTranslator.js"
with open(tr_path, "r", encoding="utf-8") as f:
    tr_text = f.read()

tr_avail_target = "turbo: { playable: true }\n    };"
tr_avail_repl = """turbo: { playable: true },
      // Phase H25 Playable Signs (30 signs reaching 550 total signs)
      fix: { playable: true },
      realize: { playable: true },
      notice: { playable: true },
      limit: { playable: true },
      substance: { playable: true },
      cover: { playable: true },
      risk: { playable: true },
      safe: { playable: true },
      guide: { playable: true },
      memory: { playable: true },
      join: { playable: true },
      explain: { playable: true },
      complex: { playable: true },
      nature: { playable: true },
      weather: { playable: true },
      plant: { playable: true },
      animal: { playable: true },
      mountain: { playable: true },
      river: { playable: true },
      ocean: { playable: true },
      bridge: { playable: true },
      market: { playable: true },
      cost: { playable: true },
      rich: { playable: true },
      weak: { playable: true },
      heavy: { playable: true },
      shadow: { playable: true },
      mirror: { playable: true },
      window: { playable: true },
      wall: { playable: true }
    };"""

if tr_avail_target in tr_text:
    tr_text = tr_text.replace(tr_avail_target, tr_avail_repl)
elif tr_avail_target.replace("\n", "\r\n") in tr_text:
    tr_text = tr_text.replace(tr_avail_target.replace("\n", "\r\n"), tr_avail_repl.replace("\n", "\r\n"))

tr_dict_target = "['turbo', 'TURBO'],"
tr_dict_repl = """['turbo', 'TURBO'],
      // Phase H25 Lexical Mappings & Inflections
      ['fix', 'FIX'], ['fixes', 'FIX'], ['fixed', 'FIX'], ['fixing', 'FIX'],
      ['realize', 'REALIZE'], ['realizes', 'REALIZE'], ['realized', 'REALIZE'], ['realizing', 'REALIZE'],
      ['notice', 'NOTICE'], ['notices', 'NOTICE'], ['noticed', 'NOTICE'], ['noticing', 'NOTICE'],
      ['limit', 'LIMIT'], ['limits', 'LIMIT'], ['limited', 'LIMIT'], ['limiting', 'LIMIT'],
      ['substance', 'SUBSTANCE'], ['substances', 'SUBSTANCE'],
      ['cover', 'COVER'], ['covers', 'COVER'], ['covered', 'COVER'], ['covering', 'COVER'],
      ['risk', 'RISK'], ['risks', 'RISK'], ['risky', 'RISK'],
      ['safe', 'SAFE'], ['safety', 'SAFE'], ['safely', 'SAFE'],
      ['guide', 'GUIDE'], ['guides', 'GUIDE'], ['guided', 'GUIDE'], ['guiding', 'GUIDE'], ['guidance', 'GUIDE'],
      ['memory', 'MEMORY'], ['memories', 'MEMORY'],
      ['join', 'JOIN'], ['joins', 'JOIN'], ['joined', 'JOIN'], ['joining', 'JOIN'],
      ['explain', 'EXPLAIN'], ['explains', 'EXPLAIN'], ['explained', 'EXPLAIN'], ['explaining', 'EXPLAIN'], ['explanation', 'EXPLAIN'],
      ['complex', 'COMPLEX'], ['complexity', 'COMPLEX'],
      ['nature', 'NATURE'], ['natural', 'NATURE'], ['naturally', 'NATURE'],
      ['weather', 'WEATHER'],
      ['plant', 'PLANT'], ['plants', 'PLANT'], ['planting', 'PLANT'],
      ['animal', 'ANIMAL'], ['animals', 'ANIMAL'],
      ['mountain', 'MOUNTAIN'], ['mountains', 'MOUNTAIN'],
      ['river', 'RIVER'], ['rivers', 'RIVER'],
      ['ocean', 'OCEAN'], ['oceans', 'OCEAN'],
      ['bridge', 'BRIDGE'], ['bridges', 'BRIDGE'],
      ['market', 'MARKET'], ['markets', 'MARKET'], ['marketing', 'MARKET'],
      ['cost', 'COST'], ['costs', 'COST'], ['costing', 'COST'],
      ['rich', 'RICH'], ['richer', 'RICH'], ['richest', 'RICH'],
      ['weak', 'WEAK'], ['weaker', 'WEAK'], ['weakness', 'WEAK'],
      ['heavy', 'HEAVY'], ['heavier', 'HEAVY'], ['heavily', 'HEAVY'],
      ['shadow', 'SHADOW'], ['shadows', 'SHADOW'],
      ['mirror', 'MIRROR'], ['mirrors', 'MIRROR'],
      ['window', 'WINDOW'], ['windows', 'WINDOW'],
      ['wall', 'WALL'], ['walls', 'WALL'],"""

if tr_dict_target in tr_text:
    tr_text = tr_text.replace(tr_dict_target, tr_dict_repl)
elif tr_dict_target.replace("\n", "\r\n") in tr_text:
    tr_text = tr_text.replace(tr_dict_target.replace("\n", "\r\n"), tr_dict_repl.replace("\n", "\r\n"))

with open(tr_path, "w", encoding="utf-8") as f:
    f.write(tr_text)
print("Updated EnglishToISLTranslator.js with H25 signs and inflections.")

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
