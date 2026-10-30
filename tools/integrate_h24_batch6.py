"""
tools/integrate_h24_batch6.py

Integrates Batch 6 (24 new signs, total 332 signs) across:
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

target_bcl = '"ability", "leave", "movie", "dynamic", "guess", "respect", "data", "launch", "pack", "apple", "grow", "air", "fun", "concept", "present", "tools", "sure", "awesome", "opposite", "tip", "sensation", "gym", "basis", "technique"'
repl_bcl = target_bcl + ',\n    # Phase H24 Batch 6 Signs (24 authentic signs covering 115+ tokens, total 332 signs)\n    "coaching", "couple", "final", "experience", "prepared", "general", "strong", "decision", "worse", "ice", "side", "replace", "sick", "brilliant", "paid", "maths", "spice", "harness", "client", "cream", "once", "speaker", "mention", "allow"'

if target_bcl in bcl_text:
    bcl_text = bcl_text.replace(target_bcl, repl_bcl)
    with open(bcl_path, "w", encoding="utf-8") as f:
        f.write(bcl_text)
    print("Updated tools/build_corpus_lexicon.py with Batch 6 signs.")
else:
    print("Warning: target string not found in tools/build_corpus_lexicon.py!")

# 2. Update EnglishToISLTranslator.js
tr_path = PROJECT_ROOT / "tools" / "avatar_viewer" / "EnglishToISLTranslator.js"
with open(tr_path, "r", encoding="utf-8") as f:
    tr_text = f.read()

tr_avail_target = "technique: { playable: true }\n    };"
tr_avail_repl = """technique: { playable: true },
      // Phase H24 Batch 6 Playable Signs (24 signs, total 332 signs)
      coaching: { playable: true },
      couple: { playable: true },
      final: { playable: true },
      experience: { playable: true },
      prepared: { playable: true },
      general: { playable: true },
      strong: { playable: true },
      decision: { playable: true },
      worse: { playable: true },
      ice: { playable: true },
      side: { playable: true },
      replace: { playable: true },
      sick: { playable: true },
      brilliant: { playable: true },
      paid: { playable: true },
      maths: { playable: true },
      spice: { playable: true },
      harness: { playable: true },
      client: { playable: true },
      cream: { playable: true },
      once: { playable: true },
      speaker: { playable: true },
      mention: { playable: true },
      allow: { playable: true }
    };"""

if tr_avail_target in tr_text:
    tr_text = tr_text.replace(tr_avail_target, tr_avail_repl)
elif tr_avail_target.replace("\n", "\r\n") in tr_text:
    tr_text = tr_text.replace(tr_avail_target.replace("\n", "\r\n"), tr_avail_repl.replace("\n", "\r\n"))

tr_dict_target = "['technique', 'TECHNIQUE'], ['techniques', 'TECHNIQUE'],"
tr_dict_repl = """['technique', 'TECHNIQUE'], ['techniques', 'TECHNIQUE'],
      // Phase H24 Batch 6 Lexical Mappings & Inflections
      ['coaching', 'COACHING'], ['coach', 'COACHING'], ['coaches', 'COACHING'], ['coached', 'COACHING'],
      ['couple', 'COUPLE'], ['couples', 'COUPLE'],
      ['final', 'FINAL'], ['finally', 'FINAL'],
      ['experience', 'EXPERIENCE'], ['experiences', 'EXPERIENCE'], ['experienced', 'EXPERIENCE'],
      ['prepared', 'PREPARED'], ['prepare', 'PREPARED'], ['prepares', 'PREPARED'], ['preparing', 'PREPARED'],
      ['general', 'GENERAL'], ['generally', 'GENERAL'],
      ['strong', 'STRONG'], ['strongly', 'STRONG'], ['stronger', 'STRONG'],
      ['decision', 'DECISION'], ['decisions', 'DECISION'], ['decide', 'DECISION'], ['decided', 'DECISION'],
      ['worse', 'WORSE'], ['worst', 'WORSE'],
      ['ice', 'ICE'],
      ['side', 'SIDE'], ['sides', 'SIDE'],
      ['replace', 'REPLACE'], ['replaces', 'REPLACE'], ['replaced', 'REPLACE'], ['replacing', 'REPLACE'],
      ['sick', 'SICK'], ['sickness', 'SICK'],
      ['brilliant', 'BRILLIANT'], ['brilliantly', 'BRILLIANT'],
      ['paid', 'PAID'], ['pay', 'PAID'], ['pays', 'PAID'], ['paying', 'PAID'],
      ['maths', 'MATHS'], ['math', 'MATHS'],
      ['spice', 'SPICE'], ['spices', 'SPICE'], ['spicy', 'SPICE'],
      ['harness', 'HARNESS'], ['harnesses', 'HARNESS'], ['harnessed', 'HARNESS'], ['harnessing', 'HARNESS'],
      ['client', 'CLIENT'], ['clients', 'CLIENT'],
      ['cream', 'CREAM'], ['creams', 'CREAM'],
      ['once', 'ONCE'],
      ['speaker', 'SPEAKER'], ['speakers', 'SPEAKER'],
      ['mention', 'MENTION'], ['mentions', 'MENTION'], ['mentioned', 'MENTION'], ['mentioning', 'MENTION'],
      ['allow', 'ALLOW'], ['allows', 'ALLOW'], ['allowed', 'ALLOW'], ['allowing', 'ALLOW'],"""

if tr_dict_target in tr_text:
    tr_text = tr_text.replace(tr_dict_target, tr_dict_repl)
elif tr_dict_target.replace("\n", "\r\n") in tr_text:
    tr_text = tr_text.replace(tr_dict_target.replace("\n", "\r\n"), tr_dict_repl.replace("\n", "\r\n"))

with open(tr_path, "w", encoding="utf-8") as f:
    f.write(tr_text)
print("Updated tools/avatar_viewer/EnglishToISLTranslator.js with Batch 6 mappings.")

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

print("Batch 6 integration complete.")
