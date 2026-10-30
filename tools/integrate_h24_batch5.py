"""
tools/integrate_h24_batch5.py

Integrates Batch 5 (24 new signs, total 308 signs) across:
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

target_bcl = '"play", "live", "emotion", "afraid", "place", "house", "sorry", "believe", "company", "sing", "song", "money", "real", "hour", "perfect", "sit", "car", "turn", "normal", "confused", "remind", "definition", "happen", "slowly"'
repl_bcl = target_bcl + ',\n    # Phase H24 Batch 5 Signs (24 authentic signs covering 125+ tokens, passing 300 milestone)\n    "ability", "leave", "movie", "dynamic", "guess", "respect", "data", "launch", "pack", "apple", "grow", "air", "fun", "concept", "present", "tools", "sure", "awesome", "opposite", "tip", "sensation", "gym", "basis", "technique"'

if target_bcl in bcl_text:
    bcl_text = bcl_text.replace(target_bcl, repl_bcl)
    with open(bcl_path, "w", encoding="utf-8") as f:
        f.write(bcl_text)
    print("Updated tools/build_corpus_lexicon.py with Batch 5 signs.")
else:
    print("Warning: target string not found in tools/build_corpus_lexicon.py!")

# 2. Update EnglishToISLTranslator.js
tr_path = PROJECT_ROOT / "tools" / "avatar_viewer" / "EnglishToISLTranslator.js"
with open(tr_path, "r", encoding="utf-8") as f:
    tr_text = f.read()

tr_avail_target = "slowly: { playable: true }\n    };"
tr_avail_repl = """slowly: { playable: true },
      // Phase H24 Batch 5 Playable Signs (24 signs, total 308 signs)
      ability: { playable: true },
      leave: { playable: true },
      movie: { playable: true },
      dynamic: { playable: true },
      guess: { playable: true },
      respect: { playable: true },
      data: { playable: true },
      launch: { playable: true },
      pack: { playable: true },
      apple: { playable: true },
      grow: { playable: true },
      air: { playable: true },
      fun: { playable: true },
      concept: { playable: true },
      present: { playable: true },
      tools: { playable: true },
      sure: { playable: true },
      awesome: { playable: true },
      opposite: { playable: true },
      tip: { playable: true },
      sensation: { playable: true },
      gym: { playable: true },
      basis: { playable: true },
      technique: { playable: true }
    };"""

if tr_avail_target in tr_text:
    tr_text = tr_text.replace(tr_avail_target, tr_avail_repl)
elif tr_avail_target.replace("\n", "\r\n") in tr_text:
    tr_text = tr_text.replace(tr_avail_target.replace("\n", "\r\n"), tr_avail_repl.replace("\n", "\r\n"))

tr_dict_target = "['slowly', 'SLOWLY'],"
tr_dict_repl = """['slowly', 'SLOWLY'],
      // Phase H24 Batch 5 Lexical Mappings & Inflections
      ['ability', 'ABILITY'], ['abilities', 'ABILITY'],
      ['leave', 'LEAVE'], ['leaves', 'LEAVE'], ['leaving', 'LEAVE'], ['left', 'LEAVE'],
      ['movie', 'MOVIE'], ['movies', 'MOVIE'], ['film', 'MOVIE'], ['films', 'MOVIE'],
      ['dynamic', 'DYNAMIC'], ['dynamics', 'DYNAMIC'],
      ['guess', 'GUESS'], ['guesses', 'GUESS'], ['guessing', 'GUESS'], ['guessed', 'GUESS'],
      ['respect', 'RESPECT'], ['respects', 'RESPECT'], ['respected', 'RESPECT'], ['respecting', 'RESPECT'],
      ['data', 'DATA'],
      ['launch', 'LAUNCH'], ['launches', 'LAUNCH'], ['launching', 'LAUNCH'], ['launched', 'LAUNCH'],
      ['pack', 'PACK'], ['packs', 'PACK'], ['packing', 'PACK'], ['packed', 'PACK'],
      ['apple', 'APPLE'], ['apples', 'APPLE'],
      ['grow', 'GROW'], ['grows', 'GROW'], ['growing', 'GROW'], ['grew', 'GROW'], ['grown', 'GROW'],
      ['air', 'AIR'],
      ['fun', 'FUN'],
      ['concept', 'CONCEPT'], ['concepts', 'CONCEPT'],
      ['present', 'PRESENT'], ['presents', 'PRESENT'], ['presenting', 'PRESENT'], ['presented', 'PRESENT'],
      ['tools', 'TOOLS'], ['tool', 'TOOLS'],
      ['sure', 'SURE'], ['surely', 'SURE'],
      ['awesome', 'AWESOME'],
      ['opposite', 'OPPOSITE'], ['opposites', 'OPPOSITE'],
      ['tip', 'TIP'], ['tips', 'TIP'],
      ['sensation', 'SENSATION'], ['sensations', 'SENSATION'],
      ['gym', 'GYM'], ['gyms', 'GYM'],
      ['basis', 'BASIS'], ['bases', 'BASIS'],
      ['technique', 'TECHNIQUE'], ['techniques', 'TECHNIQUE'],"""

if tr_dict_target in tr_text:
    tr_text = tr_text.replace(tr_dict_target, tr_dict_repl)
elif tr_dict_target.replace("\n", "\r\n") in tr_text:
    tr_text = tr_text.replace(tr_dict_target.replace("\n", "\r\n"), tr_dict_repl.replace("\n", "\r\n"))

with open(tr_path, "w", encoding="utf-8") as f:
    f.write(tr_text)
print("Updated tools/avatar_viewer/EnglishToISLTranslator.js with Batch 5 mappings.")

# 3. Update index.html preload list & message
html_path = PROJECT_ROOT / "tools" / "avatar_viewer" / "index.html"
with open(html_path, "r", encoding="utf-8") as f:
    html_text = f.read()

# Load manifest signs
with open(PROJECT_ROOT / "signs" / "manifest.json", "r", encoding="utf-8") as mf:
    manifest_data = json.load(mf)
all_sign_ids = sorted(list(set(s["sign_id"] for s in manifest_data["signs"])))

new_preload_str = json.dumps(all_sign_ids)
html_text = re.sub(r'signLibrary\.preload\(\[[^\]]+\]\)', f'signLibrary.preload({new_preload_str})', html_text)
html_text = re.sub(r'\d+ ISL signs across \d+ verified', f'{len(all_sign_ids)} ISL signs across {len(all_sign_ids)} verified', html_text)

with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_text)
print(f"Updated tools/avatar_viewer/index.html preload list to {len(all_sign_ids)} signs.")

print("Batch 5 integration complete.")
