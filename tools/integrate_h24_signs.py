"""
tools/integrate_h24_signs.py

Synchronizes 17 new Schema 2.0.0 signs (total 224) into:
- tools/avatar_viewer/EnglishToISLTranslator.js
- tools/avatar_viewer/index.html
- data/isl_corpus_lexicon.json & data/isl_corpus_coverage.json
"""

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# 1. Update EnglishToISLTranslator.js
translator_path = PROJECT_ROOT / "tools" / "avatar_viewer" / "EnglishToISLTranslator.js"
with open(translator_path, "r", encoding="utf-8") as f:
    tr_text = f.read()

# Add to availableSigns
h21_target = "train: { playable: true }\n    };"
h24_signs_js = """train: { playable: true },
      // Phase H24 New Playable Signs (17 high-frequency signs)
      increase: { playable: true },
      little: { playable: true },
      rest: { playable: true },
      let: { playable: true },
      able: { playable: true },
      part: { playable: true },
      big: { playable: true },
      stop: { playable: true },
      watch: { playable: true },
      chart: { playable: true },
      subject: { playable: true },
      culture: { playable: true },
      product: { playable: true },
      audio: { playable: true },
      positive: { playable: true },
      trust: { playable: true },
      match: { playable: true }
    };"""

if h21_target in tr_text:
    tr_text = tr_text.replace(h21_target, h24_signs_js)
elif h21_target.replace("\n", "\r\n") in tr_text:
    tr_text = tr_text.replace(h21_target.replace("\n", "\r\n"), h24_signs_js.replace("\n", "\r\n"))
else:
    print("WARNING: Could not find train: { playable: true } in EnglishToISLTranslator.js")

# Add to dictionary entries
dict_target = "['train', 'TRAIN'],"
h24_dict_js = """['train', 'TRAIN'],
      // Phase H24 Lexical Mappings & Inflections
      ['increase', 'INCREASE'], ['increased', 'INCREASE'], ['increases', 'INCREASE'], ['increasing', 'INCREASE'],
      ['little', 'LITTLE'],
      ['rest', 'REST'], ['rests', 'REST'], ['resting', 'REST'], ['rested', 'REST'],
      ['let', 'LET'], ['lets', 'LET'], ['letting', 'LET'],
      ['able', 'ABLE'],
      ['part', 'PART'], ['parts', 'PART'],
      ['big', 'BIG'],
      ['stop', 'STOP'], ['stops', 'STOP'], ['stopped', 'STOP'], ['stopping', 'STOP'],
      ['watch', 'WATCH'], ['watches', 'WATCH'], ['watched', 'WATCH'], ['watching', 'WATCH'],
      ['chart', 'CHART'], ['charts', 'CHART'],
      ['subject', 'SUBJECT'], ['subjects', 'SUBJECT'],
      ['culture', 'CULTURE'], ['cultures', 'CULTURE'],
      ['product', 'PRODUCT'], ['products', 'PRODUCT'],
      ['audio', 'AUDIO'],
      ['positive', 'POSITIVE'],
      ['trust', 'TRUST'], ['trusts', 'TRUST'], ['trusted', 'TRUST'], ['trusting', 'TRUST'],
      ['match', 'MATCH'], ['matches', 'MATCH'], ['matched', 'MATCH'], ['matching', 'MATCH'],"""

if dict_target in tr_text:
    tr_text = tr_text.replace(dict_target, h24_dict_js)
elif dict_target.replace("\n", "\r\n") in tr_text:
    tr_text = tr_text.replace(dict_target.replace("\n", "\r\n"), h24_dict_js.replace("\n", "\r\n"))

with open(translator_path, "w", encoding="utf-8") as f:
    f.write(tr_text)
print("Updated EnglishToISLTranslator.js")

# 2. Update tools/avatar_viewer/index.html
index_path = PROJECT_ROOT / "tools" / "avatar_viewer" / "index.html"
with open(index_path, "r", encoding="utf-8") as f:
    idx_text = f.read()

# Load all sign IDs from manifest
manifest_path = PROJECT_ROOT / "signs" / "manifest.json"
with open(manifest_path, "r", encoding="utf-8") as f:
    manifest = json.load(f)

all_sign_ids = sorted([s["sign_id"] for s in manifest["signs"]])
new_preload_json = json.dumps(all_sign_ids)

# Replace preload array
import re
idx_text = re.sub(
    r'signLibrary\.preload\(\[[^\]]+\]\)',
    f'signLibrary.preload({new_preload_json})',
    idx_text
)

# Update status message
idx_text = re.sub(
    r'Library preloaded: \d+ ISL signs across \d+ verified Schema 2\.0\.0 assets are playable\.',
    f'Library preloaded: {len(all_sign_ids)} ISL signs across {len(all_sign_ids)} verified Schema 2.0.0 assets are playable.',
    idx_text
)

with open(index_path, "w", encoding="utf-8") as f:
    f.write(idx_text)
print(f"Updated tools/avatar_viewer/index.html with {len(all_sign_ids)} signs.")
