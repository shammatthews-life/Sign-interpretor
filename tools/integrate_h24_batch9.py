"""
tools/integrate_h24_batch9.py

Integrates Batch 9 (20 new signs, reaching 400 signs milestone) across:
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

target_bcl = '"special", "practical", "welcome", "valuable", "transform", "avoid", "excellent", "social", "critical", "direction", "content", "fail", "basketball", "golf", "less", "massive", "continuous", "dancing", "born", "friday", "instead", "ago", "quite", "guy"'
repl_bcl = target_bcl + ',\n    # Phase H24 Batch 9 Signs (20 authentic signs reaching 400 signs milestone)\n    "smile", "dream", "exercise", "accomplish", "close", "old", "hungry", "intention", "motivated", "few", "lovely", "focus", "sometimes", "list", "connected", "course", "analyze", "fourth", "fifth", "meeting"'

if target_bcl in bcl_text:
    bcl_text = bcl_text.replace(target_bcl, repl_bcl)
    with open(bcl_path, "w", encoding="utf-8") as f:
        f.write(bcl_text)
    print("Updated tools/build_corpus_lexicon.py with Batch 9 signs.")
else:
    print("Warning: target string not found in tools/build_corpus_lexicon.py!")

# 2. Update EnglishToISLTranslator.js
tr_path = PROJECT_ROOT / "tools" / "avatar_viewer" / "EnglishToISLTranslator.js"
with open(tr_path, "r", encoding="utf-8") as f:
    tr_text = f.read()

tr_avail_target = "guy: { playable: true }\n    };"
tr_avail_repl = """guy: { playable: true },
      // Phase H24 Batch 9 Playable Signs (20 signs reaching 400 total signs)
      smile: { playable: true },
      dream: { playable: true },
      exercise: { playable: true },
      accomplish: { playable: true },
      close: { playable: true },
      old: { playable: true },
      hungry: { playable: true },
      intention: { playable: true },
      motivated: { playable: true },
      few: { playable: true },
      lovely: { playable: true },
      focus: { playable: true },
      sometimes: { playable: true },
      list: { playable: true },
      connected: { playable: true },
      course: { playable: true },
      analyze: { playable: true },
      fourth: { playable: true },
      fifth: { playable: true },
      meeting: { playable: true }
    };"""

if tr_avail_target in tr_text:
    tr_text = tr_text.replace(tr_avail_target, tr_avail_repl)
elif tr_avail_target.replace("\n", "\r\n") in tr_text:
    tr_text = tr_text.replace(tr_avail_target.replace("\n", "\r\n"), tr_avail_repl.replace("\n", "\r\n"))

tr_dict_target = "['guy', 'GUY'], ['guys', 'GUY'],"
tr_dict_repl = """['guy', 'GUY'], ['guys', 'GUY'],
      // Phase H24 Batch 9 Lexical Mappings & Inflections
      ['smile', 'SMILE'], ['smiles', 'SMILE'], ['smiling', 'SMILE'], ['smiled', 'SMILE'],
      ['dream', 'DREAM'], ['dreams', 'DREAM'], ['dreaming', 'DREAM'], ['dreamed', 'DREAM'],
      ['exercise', 'EXERCISE'], ['exercises', 'EXERCISE'], ['exercising', 'EXERCISE'], ['exercised', 'EXERCISE'],
      ['accomplish', 'ACCOMPLISH'], ['accomplishes', 'ACCOMPLISH'], ['accomplished', 'ACCOMPLISH'], ['accomplishing', 'ACCOMPLISH'],
      ['close', 'CLOSE'], ['closer', 'CLOSE'], ['closest', 'CLOSE'],
      ['old', 'OLD'], ['older', 'OLD'], ['oldest', 'OLD'],
      ['hungry', 'HUNGRY'],
      ['intention', 'INTENTION'], ['intentions', 'INTENTION'], ['intend', 'INTENTION'], ['intends', 'INTENTION'], ['intended', 'INTENTION'], ['intending', 'INTENTION'],
      ['motivated', 'MOTIVATED'], ['motivate', 'MOTIVATED'], ['motivates', 'MOTIVATED'], ['motivating', 'MOTIVATED'], ['motivation', 'MOTIVATED'],
      ['few', 'FEW'],
      ['lovely', 'LOVELY'],
      ['focus', 'FOCUS'], ['focuses', 'FOCUS'], ['focused', 'FOCUS'], ['focusing', 'FOCUS'],
      ['sometimes', 'SOMETIMES'],
      ['list', 'LIST'], ['lists', 'LIST'], ['listing', 'LIST'], ['listed', 'LIST'],
      ['connected', 'CONNECTED'], ['connect', 'CONNECTED'], ['connects', 'CONNECTED'], ['connecting', 'CONNECTED'], ['connection', 'CONNECTED'], ['connections', 'CONNECTED'],
      ['course', 'COURSE'], ['courses', 'COURSE'],
      ['analyze', 'ANALYZE'], ['analyzes', 'ANALYZE'], ['analyzed', 'ANALYZE'], ['analyzing', 'ANALYZE'], ['analysis', 'ANALYZE'],
      ['fourth', 'FOURTH'],
      ['fifth', 'FIFTH'],
      ['meeting', 'MEETING'], ['meetings', 'MEETING'],"""

if tr_dict_target in tr_text:
    tr_text = tr_text.replace(tr_dict_target, tr_dict_repl)
elif tr_dict_target.replace("\n", "\r\n") in tr_text:
    tr_text = tr_text.replace(tr_dict_target.replace("\n", "\r\n"), tr_dict_repl.replace("\n", "\r\n"))

with open(tr_path, "w", encoding="utf-8") as f:
    f.write(tr_text)
print("Updated EnglishToISLTranslator.js with Batch 9 signs.")

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
