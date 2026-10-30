"""
tools/integrate_h24_batch8.py

Integrates Batch 8 (24 new signs, total 380 signs) across:
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

target_bcl = '"job", "business", "message", "care", "promise", "flow", "store", "center", "middle", "sister", "post", "package", "favorite", "silent", "comfortable", "football", "low", "amount", "crazy", "between", "each", "chat", "bit", "super"'
repl_bcl = target_bcl + ',\n    # Phase H24 Batch 8 Signs (24 authentic signs, total 380 signs)\n    "special", "practical", "welcome", "valuable", "transform", "avoid", "excellent", "social", "critical", "direction", "content", "fail", "basketball", "golf", "less", "massive", "continuous", "dancing", "born", "friday", "instead", "ago", "quite", "guy"'

if target_bcl in bcl_text:
    bcl_text = bcl_text.replace(target_bcl, repl_bcl)
    with open(bcl_path, "w", encoding="utf-8") as f:
        f.write(bcl_text)
    print("Updated tools/build_corpus_lexicon.py with Batch 8 signs.")
else:
    print("Warning: target string not found in tools/build_corpus_lexicon.py!")

# 2. Update EnglishToISLTranslator.js
tr_path = PROJECT_ROOT / "tools" / "avatar_viewer" / "EnglishToISLTranslator.js"
with open(tr_path, "r", encoding="utf-8") as f:
    tr_text = f.read()

tr_avail_target = "super: { playable: true }\n    };"
tr_avail_repl = """super: { playable: true },
      // Phase H24 Batch 8 Playable Signs (24 signs, total 380 signs)
      special: { playable: true },
      practical: { playable: true },
      welcome: { playable: true },
      valuable: { playable: true },
      transform: { playable: true },
      avoid: { playable: true },
      excellent: { playable: true },
      social: { playable: true },
      critical: { playable: true },
      direction: { playable: true },
      content: { playable: true },
      fail: { playable: true },
      basketball: { playable: true },
      golf: { playable: true },
      less: { playable: true },
      massive: { playable: true },
      continuous: { playable: true },
      dancing: { playable: true },
      born: { playable: true },
      friday: { playable: true },
      instead: { playable: true },
      ago: { playable: true },
      quite: { playable: true },
      guy: { playable: true }
    };"""

if tr_avail_target in tr_text:
    tr_text = tr_text.replace(tr_avail_target, tr_avail_repl)
elif tr_avail_target.replace("\n", "\r\n") in tr_text:
    tr_text = tr_text.replace(tr_avail_target.replace("\n", "\r\n"), tr_avail_repl.replace("\n", "\r\n"))

tr_dict_target = "['super', 'SUPER'], ['superb', 'SUPER'],"
tr_dict_repl = """['super', 'SUPER'], ['superb', 'SUPER'],
      // Phase H24 Batch 8 Lexical Mappings & Inflections
      ['special', 'SPECIAL'], ['specially', 'SPECIAL'],
      ['practical', 'PRACTICAL'], ['practically', 'PRACTICAL'],
      ['welcome', 'WELCOME'], ['welcomes', 'WELCOME'], ['welcomed', 'WELCOME'], ['welcoming', 'WELCOME'],
      ['valuable', 'VALUABLE'], ['value', 'VALUABLE'], ['values', 'VALUABLE'],
      ['transform', 'TRANSFORM'], ['transforms', 'TRANSFORM'], ['transformed', 'TRANSFORM'], ['transforming', 'TRANSFORM'],
      ['avoid', 'AVOID'], ['avoids', 'AVOID'], ['avoided', 'AVOID'], ['avoiding', 'AVOID'],
      ['excellent', 'EXCELLENT'], ['excellently', 'EXCELLENT'],
      ['social', 'SOCIAL'], ['socially', 'SOCIAL'],
      ['critical', 'CRITICAL'], ['critically', 'CRITICAL'],
      ['direction', 'DIRECTION'], ['directions', 'DIRECTION'],
      ['content', 'CONTENT'], ['contents', 'CONTENT'],
      ['fail', 'FAIL'], ['fails', 'FAIL'], ['failed', 'FAIL'], ['failing', 'FAIL'],
      ['basketball', 'BASKETBALL'],
      ['golf', 'GOLF'],
      ['less', 'LESS'], ['lesser', 'LESS'],
      ['massive', 'MASSIVE'], ['massively', 'MASSIVE'],
      ['continuous', 'CONTINUOUS'], ['continuously', 'CONTINUOUS'],
      ['dancing', 'DANCING'], ['dance', 'DANCING'], ['dances', 'DANCING'], ['danced', 'DANCING'],
      ['born', 'BORN'], ['birth', 'BORN'],
      ['friday', 'FRIDAY'], ['fridays', 'FRIDAY'],
      ['instead', 'INSTEAD'],
      ['ago', 'AGO'],
      ['quite', 'QUITE'],
      ['guy', 'GUY'], ['guys', 'GUY'],"""

if tr_dict_target in tr_text:
    tr_text = tr_text.replace(tr_dict_target, tr_dict_repl)
elif tr_dict_target.replace("\n", "\r\n") in tr_text:
    tr_text = tr_text.replace(tr_dict_target.replace("\n", "\r\n"), tr_dict_repl.replace("\n", "\r\n"))

with open(tr_path, "w", encoding="utf-8") as f:
    f.write(tr_text)
print("Updated EnglishToISLTranslator.js with Batch 8 signs.")

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
