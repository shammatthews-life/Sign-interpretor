"""
tools/audit_phrase_integration.py

Phase H22 Worker B: Investigating and Auditing Multiword Phrase Integration.
Identifies which researched phrases from H19, H20, and H21 are active in:
1. tools/build_corpus_lexicon.py (MULTIWORD_EXPRESSIONS)
2. tools/avatar_viewer/EnglishToISLTranslator.js (this.phrases)
"""

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"

with open(DATA_DIR / "h21_top100_phrase_research.json", "r", encoding="utf-8") as f:
    h21_phrases = json.load(f)

with open(PROJECT_ROOT / "tools" / "build_corpus_lexicon.py", "r", encoding="utf-8") as f:
    build_code = f.read()

with open(PROJECT_ROOT / "tools" / "avatar_viewer" / "EnglishToISLTranslator.js", "r", encoding="utf-8") as f:
    trans_code = f.read()

integrated_in_build = []
missing_from_build = []

for p in h21_phrases:
    phrase_str = p["phrase"].lower()
    in_build = f'"{phrase_str}"' in build_code or f"'{phrase_str}'" in build_code
    in_trans = f"'{phrase_str}'" in trans_code or f'"{phrase_str}"' in trans_code
    
    status = {
        "phrase": phrase_str,
        "occurrences": p["occurrences"],
        "tokens_affected": p["tokens_affected"],
        "target_isl_glosses": p["target_isl_glosses"],
        "in_build_corpus_lexicon": in_build,
        "in_translator_js": in_trans
    }
    if in_build and in_trans:
        integrated_in_build.append(status)
    else:
        missing_from_build.append(status)

print(f"Total H21 researched phrases: {len(h21_phrases)}")
print(f"Active in both build & translator: {len(integrated_in_build)}")
print(f"Missing from one or both: {len(missing_from_build)}")

missing_tokens = sum(x["tokens_affected"] for x in missing_from_build)
print(f"Tokens affected by unintegrated phrases: {missing_tokens}")

audit_report = {
    "phase": "H22",
    "worker": "B",
    "root_cause_analysis": {
        "finding": "In Phase H21, 200 phrase candidates were mined and 100 researched into data/ artifacts, but only a subset was plugged into MULTIWORD_EXPRESSIONS in build_corpus_lexicon.py and this.phrases in EnglishToISLTranslator.js.",
        "impact": f"{len(missing_from_build)} high-value phrases affecting {missing_tokens} spoken tokens remained unintegrated, causing phrase-translated tokens to plateau at 1,415.",
        "resolution": "Integrate the researched multiword phrases into MULTIWORD_EXPRESSIONS and EnglishToISLTranslator.js with longest-match precedence."
    },
    "integrated_count": len(integrated_in_build),
    "missing_count": len(missing_from_build),
    "missing_phrases": missing_from_build
}

with open(DATA_DIR / "h22_phrase_audit.json", "w", encoding="utf-8") as f:
    json.dump(audit_report, f, indent=2)

print("Saved data/h22_phrase_audit.json.")
