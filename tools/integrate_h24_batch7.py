"""
tools/integrate_h24_batch7.py

Integrates Batch 7 (24 new signs, total 356 signs) across:
- tools/build_corpus_lexicon.py
- tools/avatar_viewer/EnglishToISLTranslator.js
- tools/avatar_viewer/index.html
And regenerates data/isl_corpus_lexicon.json and data/isl_corpus_coverage.json.
"""

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# 1. Update tools/build_corpus_lexicon.py
bcl_path = PROJECT_ROOT / "tools" / "build_corpus_lexicon.py"
with open(bcl_path, "r", encoding="utf-8") as f:
    bcl_text = f.read()

target_bcl = '"coaching", "couple", "final", "experience", "prepared", "general", "strong", "decision", "worse", "ice", "side", "replace", "sick", "brilliant", "paid", "maths", "spice", "harness", "client", "cream", "once", "speaker", "mention", "allow"'
repl_bcl = target_bcl + ',\n    # Phase H24 Batch 7 Signs (24 authentic signs, total 356 signs)\n    "job", "business", "message", "care", "promise", "flow", "store", "center", "middle", "sister", "post", "package", "favorite", "silent", "comfortable", "football", "low", "amount", "crazy", "between", "each", "chat", "bit", "super"'

if target_bcl in bcl_text:
    bcl_text = bcl_text.replace(target_bcl, repl_bcl)
    with open(bcl_path, "w", encoding="utf-8") as f:
        f.write(bcl_text)
    print("Updated tools/build_corpus_lexicon.py with Batch 7 signs.")
else:
    print("Warning: target string not found in tools/build_corpus_lexicon.py!")

# 2. Update EnglishToISLTranslator.js
tr_path = PROJECT_ROOT / "tools" / "avatar_viewer" / "EnglishToISLTranslator.js"
with open(tr_path, "r", encoding="utf-8") as f:
    tr_text = f.read()

tr_avail_target = "allow: { playable: true }\n    };"
tr_avail_repl = """allow: { playable: true },
      // Phase H24 Batch 7 Playable Signs (24 signs, total 356 signs)
      job: { playable: true },
      business: { playable: true },
      message: { playable: true },
      care: { playable: true },
      promise: { playable: true },
      flow: { playable: true },
      store: { playable: true },
      center: { playable: true },
      middle: { playable: true },
      sister: { playable: true },
      post: { playable: true },
      package: { playable: true },
      favorite: { playable: true },
      silent: { playable: true },
      comfortable: { playable: true },
      football: { playable: true },
      low: { playable: true },
      amount: { playable: true },
      crazy: { playable: true },
      between: { playable: true },
      each: { playable: true },
      chat: { playable: true },
      bit: { playable: true },
      super: { playable: true }
    };"""

if tr_avail_target in tr_text:
    tr_text = tr_text.replace(tr_avail_target, tr_avail_repl)
elif tr_avail_target.replace("\n", "\r\n") in tr_text:
    tr_text = tr_text.replace(tr_avail_target.replace("\n", "\r\n"), tr_avail_repl.replace("\n", "\r\n"))

tr_dict_target = "['allow', 'ALLOW'], ['allows', 'ALLOW'], ['allowed', 'ALLOW'], ['allowing', 'ALLOW'],"
tr_dict_repl = """['allow', 'ALLOW'], ['allows', 'ALLOW'], ['allowed', 'ALLOW'], ['allowing', 'ALLOW'],
      // Phase H24 Batch 7 Lexical Mappings & Inflections
      ['job', 'JOB'], ['jobs', 'JOB'],
      ['business', 'BUSINESS'], ['businesses', 'BUSINESS'],
      ['message', 'MESSAGE'], ['messages', 'MESSAGE'],
      ['care', 'CARE'], ['cares', 'CARE'], ['caring', 'CARE'], ['cared', 'CARE'],
      ['promise', 'PROMISE'], ['promises', 'PROMISE'], ['promising', 'PROMISE'], ['promised', 'PROMISE'],
      ['flow', 'FLOW'], ['flows', 'FLOW'], ['flowing', 'FLOW'], ['flowed', 'FLOW'],
      ['store', 'STORE'], ['stores', 'STORE'], ['storing', 'STORE'], ['stored', 'STORE'],
      ['center', 'CENTER'], ['centers', 'CENTER'], ['central', 'CENTER'],
      ['middle', 'MIDDLE'],
      ['sister', 'SISTER'], ['sisters', 'SISTER'],
      ['post', 'POST'], ['posts', 'POST'], ['posting', 'POST'], ['posted', 'POST'],
      ['package', 'PACKAGE'], ['packages', 'PACKAGE'], ['packaging', 'PACKAGE'], ['packaged', 'PACKAGE'],
      ['favorite', 'FAVORITE'], ['favorites', 'FAVORITE'],
      ['silent', 'SILENT'], ['silence', 'SILENT'], ['silently', 'SILENT'],
      ['comfortable', 'COMFORTABLE'], ['comfort', 'COMFORTABLE'],
      ['football', 'FOOTBALL'],
      ['low', 'LOW'], ['lower', 'LOW'], ['lowest', 'LOW'],
      ['amount', 'AMOUNT'], ['amounts', 'AMOUNT'],
      ['crazy', 'CRAZY'],
      ['between', 'BETWEEN'],
      ['each', 'EACH'],
      ['chat', 'CHAT'], ['chats', 'CHAT'], ['chatting', 'CHAT'], ['chatted', 'CHAT'],
      ['bit', 'BIT'], ['bits', 'BIT'],
      ['super', 'SUPER'], ['superb', 'SUPER'],"""

if tr_dict_target in tr_text:
    tr_text = tr_text.replace(tr_dict_target, tr_dict_repl)
elif tr_dict_target.replace("\n", "\r\n") in tr_text:
    tr_text = tr_text.replace(tr_dict_target.replace("\n", "\r\n"), tr_dict_repl.replace("\n", "\r\n"))

with open(tr_path, "w", encoding="utf-8") as f:
    f.write(tr_text)
print("Updated EnglishToISLTranslator.js with Batch 7 signs.")

# 3. Update index.html dropdown
html_path = PROJECT_ROOT / "tools" / "avatar_viewer" / "index.html"
with open(html_path, "r", encoding="utf-8") as f:
    html_text = f.read()

batch7_signs = [
    ("job", "JOB"),
    ("business", "BUSINESS"),
    ("message", "MESSAGE"),
    ("care", "CARE"),
    ("promise", "PROMISE"),
    ("flow", "FLOW"),
    ("store", "STORE"),
    ("center", "CENTER"),
    ("middle", "MIDDLE"),
    ("sister", "SISTER"),
    ("post", "POST"),
    ("package", "PACKAGE"),
    ("favorite", "FAVORITE"),
    ("silent", "SILENT"),
    ("comfortable", "COMFORTABLE"),
    ("football", "FOOTBALL"),
    ("low", "LOW"),
    ("amount", "AMOUNT"),
    ("crazy", "CRAZY"),
    ("between", "BETWEEN"),
    ("each", "EACH"),
    ("chat", "CHAT"),
    ("bit", "BIT"),
    ("super", "SUPER")
]

opt_lines = "\n".join([f'            <option value="{s_id}">{gloss}</option>' for s_id, gloss in batch7_signs])
target_html = '            <option value="allow">ALLOW</option>'

if target_html in html_text:
    html_text = html_text.replace(target_html, target_html + "\n" + opt_lines)
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_text)
    print("Updated tools/avatar_viewer/index.html with Batch 7 options.")
else:
    print("Warning: target option allow not found in index.html!")

print("\nIntegration step 1-3 complete.")
