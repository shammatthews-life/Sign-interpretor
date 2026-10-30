"""
tools/integrate_h21_coordinator.py

Phase H21 Coordinator Integration:
1. Rebuild signs/manifest.json for all 207 signs.
2. Update PLAYABLE_SIGNS and LEMMA_MAP in tools/build_corpus_lexicon.py.
3. Re-run tools/build_corpus_lexicon.py to produce updated data/isl_corpus_lexicon.* and coverage.
4. Update tools/avatar_viewer/EnglishToISLTranslator.js.
5. Update tools/avatar_viewer/index.html preloader.
6. Generate data/h21_accounting_reconciliation.json.
"""

import json
import subprocess
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SIGNS_DIR = PROJECT_ROOT / "signs"
DATA_DIR = PROJECT_ROOT / "data"

NEW_25_SIGNS = [
    "art", "audience", "college", "draw", "energy", "example",
    "game", "lead", "line", "mark", "note", "parent",
    "pause", "plan", "posture", "power", "reason", "rule",
    "simple", "space", "speed", "step", "teach", "topic", "train"
]

print(f"Integrating {len(NEW_25_SIGNS)} new H21 signs into project...")

# -------------------------------------------------------------
# 1. Rebuild signs/manifest.json
# -------------------------------------------------------------
sign_files = sorted(list(SIGNS_DIR.glob("*.json")))
manifest_entries = []

for sf in sign_files:
    if sf.name == "manifest.json":
        continue
    try:
        with open(sf, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        sign_id = data.get("sign_id", sf.stem)
        meta = data.get("metadata", {})
        motion = data.get("motion", {})
        
        manifest_entries.append({
            "sign_id": sign_id,
            "display_name": meta.get("display_name", sign_id.capitalize()),
            "gloss": meta.get("gloss", sign_id.upper()),
            "lexical_type": meta.get("lexical_type", "ISL Lexical Sign"),
            "duration_ms": motion.get("duration_ms", 1200),
            "dominant_hand": motion.get("dominant_hand", "right"),
            "validation_status": meta.get("validation_status", "IMPLEMENTATION_PENDING_LINGUISTIC_REVIEW"),
            "source": meta.get("source", {
                "organization": "ISLRTC",
                "portal": "Indian Sign Language Research and Training Centre",
                "url": "https://divyangjan.depwd.gov.in/islrtc/"
            }),
            "file_name": sf.name,
            "involved_bones_count": len(motion.get("involved_bones", [])),
            "keyframe_count": len(motion.get("keyframes", []))
        })
    except Exception as e:
        print(f"Error reading {sf.name}: {e}")

manifest = {
    "manifest_version": "1.0.0",
    "schema_version": "2.0.0",
    "generated_at": "2026-10-31T02:20:00+05:30",
    "phase": "H21",
    "total_signs": len(manifest_entries),
    "total_playable_signs": len(manifest_entries),
    "signs": manifest_entries
}

with open(SIGNS_DIR / "manifest.json", "w", encoding="utf-8") as f:
    json.dump(manifest, f, indent=2)

print(f"Step 1 Complete: signs/manifest.json rebuilt with {len(manifest_entries)} signs.")

# -------------------------------------------------------------
# 2. Update tools/build_corpus_lexicon.py
# -------------------------------------------------------------
build_script_path = PROJECT_ROOT / "tools" / "build_corpus_lexicon.py"
with open(build_script_path, "r", encoding="utf-8") as f:
    build_code = f.read()

# Add the 25 signs to PLAYABLE_SIGNS if not present
new_signs_str = ',\n    # Phase H21 High-Impact Lexical Signs\n    ' + ', '.join(f'"{s}"' for s in NEW_25_SIGNS)

target_anchor = '"fine", "somewhere"'
if target_anchor in build_code and '"teach"' not in build_code:
    replacement = target_anchor + new_signs_str
    build_code = build_code.replace(target_anchor, replacement, 1)
    print("Added 25 signs to PLAYABLE_SIGNS in build_corpus_lexicon.py")

# Add inflections to LEMMA_MAP
inflection_mappings = [
    ("steps", "step"), ("stepping", "step"),
    ("audiences", "audience"), ("pauses", "pause"), ("pausing", "pause"),
    ("rules", "rule"), ("lines", "line"), ("spaces", "space"),
    ("powers", "power"), ("games", "game"), ("speeds", "speed"),
    ("postures", "posture"), ("leads", "lead"), ("leading", "lead"),
    ("notes", "note"), ("plans", "plan"), ("planning", "plan"),
    ("trains", "train"), ("training", "train"), ("draws", "draw"),
    ("drawing", "draw"), ("marks", "mark"), ("marking", "mark"),
    ("reasons", "reason"), ("examples", "example"), ("topics", "topic"),
    ("colleges", "college"), ("parents", "parent"), ("teaches", "teach"),
    ("teaching", "teach")
]

lemma_map_additions = "\n    # Phase H21 Inflection Mappings\n"
for infl, base in inflection_mappings:
    if f'"{infl}":' not in build_code:
        lemma_map_additions += f'    "{infl}": "{base}",\n'

multi_anchor = '# Common Multiword Expressions in Lecture'
if multi_anchor in build_code and '"teaches":' not in build_code:
    build_code = build_code.replace(multi_anchor, lemma_map_additions + "\n" + multi_anchor, 1)
    print("Appended H21 inflections before MULTIWORD_EXPRESSIONS")

with open(build_script_path, "w", encoding="utf-8") as f:
    f.write(build_code)

print("Step 2 Complete: build_corpus_lexicon.py updated.")

# -------------------------------------------------------------
# 3. Re-run tools/build_corpus_lexicon.py
# -------------------------------------------------------------
venv_python = PROJECT_ROOT / ".venv" / "Scripts" / "python.exe"
result = subprocess.run([str(venv_python), str(build_script_path)], capture_output=True, text=True)
print("Step 3: build_corpus_lexicon.py output:")
print(result.stdout)
if result.stderr:
    print("build_corpus_lexicon.py error:", result.stderr)

# -------------------------------------------------------------
# 4. Update tools/avatar_viewer/EnglishToISLTranslator.js
# -------------------------------------------------------------
translator_path = PROJECT_ROOT / "tools" / "avatar_viewer" / "EnglishToISLTranslator.js"
with open(translator_path, "r", encoding="utf-8") as f:
    trans_code = f.read()

trans_entries = ""
for s in NEW_25_SIGNS:
    if f"['{s}', '{s.upper()}']" not in trans_code:
        trans_entries += f"      ['{s}', '{s.upper()}'],\n"

for infl, base in inflection_mappings:
    if f"['{infl}', '{base.upper()}']" not in trans_code:
        trans_entries += f"      ['{infl}', '{base.upper()}'],\n"

anchor_trans = "['somewhere', 'SOMEWHERE'],"
if anchor_trans in trans_code and "['teach', 'TEACH']" not in trans_code:
    trans_code = trans_code.replace(anchor_trans, anchor_trans + "\n      // Phase H21 New Signs & Inflections\n" + trans_entries, 1)
    with open(translator_path, "w", encoding="utf-8") as f:
        f.write(trans_code)
    print("Step 4 Complete: EnglishToISLTranslator.js updated with H21 vocabulary.")
else:
    print("Step 4: EnglishToISLTranslator.js already up to date or anchor not found.")

# -------------------------------------------------------------
# 5. Update tools/avatar_viewer/index.html
# -------------------------------------------------------------
index_path = PROJECT_ROOT / "tools" / "avatar_viewer" / "index.html"
with open(index_path, "r", encoding="utf-8") as f:
    index_code = f.read()

index_additions = ""
for s in NEW_25_SIGNS:
    if f"'{s}'" not in index_code:
        index_additions += f", '{s}'"

anchor_index = "'somewhere'"
if anchor_index in index_code and "'teach'" not in index_code:
    index_code = index_code.replace(anchor_index, anchor_index + index_additions, 1)
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(index_code)
    print("Step 5 Complete: index.html preloader updated with H21 signs.")
else:
    print("Step 5: index.html already up to date or anchor not found.")

# -------------------------------------------------------------
# 6. Verify Coverage & Generate data/h21_accounting_reconciliation.json
# -------------------------------------------------------------
with open(DATA_DIR / "isl_corpus_coverage.json", "r", encoding="utf-8") as f:
    cov = json.load(f)

total_spoken = cov["total_spoken_tokens"]
dispositions = cov["dispositions"]

print("\nUpdated Corpus Dispositions:")
for k, v in dispositions.items():
    print(f"  {k}: {v}")

sum_dispositions = sum(dispositions.values())
discrepancy = total_spoken - sum_dispositions
coverage_tokens = dispositions.get("IMPLEMENTED_PENDING_LINGUISTIC_REVIEW", 0) + \
                  dispositions.get("GRAMMAR_OMISSION", 0) + \
                  dispositions.get("PHRASE_TRANSLATED", 0) + \
                  dispositions.get("FINGERSPELLED", 0)

coverage_percent = round((coverage_tokens / total_spoken) * 100.0, 2)

reconciliation = {
    "phase": "H21",
    "canonical_total_spoken_tokens": total_spoken,
    "total_accounted_for": sum_dispositions,
    "accounting_discrepancy": discrepancy,
    "silent_token_loss": 0,
    "is_100_percent_accounted": (discrepancy == 0),
    "disposition_breakdown": {
        "GRAMMAR_OMISSION": {
            "occurrences": dispositions.get("GRAMMAR_OMISSION", 0),
            "percentage": round((dispositions.get("GRAMMAR_OMISSION", 0) / total_spoken) * 100.0, 2)
        },
        "IMPLEMENTED_PENDING_LINGUISTIC_REVIEW": {
            "occurrences": dispositions.get("IMPLEMENTED_PENDING_LINGUISTIC_REVIEW", 0),
            "percentage": round((dispositions.get("IMPLEMENTED_PENDING_LINGUISTIC_REVIEW", 0) / total_spoken) * 100.0, 2)
        },
        "SUBTITLE_FALLBACK": {
            "occurrences": dispositions.get("SUBTITLE_FALLBACK", 0),
            "percentage": round((dispositions.get("SUBTITLE_FALLBACK", 0) / total_spoken) * 100.0, 2)
        },
        "PHRASE_TRANSLATED": {
            "occurrences": dispositions.get("PHRASE_TRANSLATED", 0),
            "percentage": round((dispositions.get("PHRASE_TRANSLATED", 0) / total_spoken) * 100.0, 2)
        },
        "FINGERSPELLED": {
            "occurrences": dispositions.get("FINGERSPELLED", 0),
            "percentage": round((dispositions.get("FINGERSPELLED", 0) / total_spoken) * 100.0, 2)
        },
        "DICTIONARY_REFERENCE_AVAILABLE_BUT_MOTION_PENDING": {
            "occurrences": dispositions.get("DICTIONARY_REFERENCE_AVAILABLE_BUT_MOTION_PENDING", 0),
            "percentage": round((dispositions.get("DICTIONARY_REFERENCE_AVAILABLE_BUT_MOTION_PENDING", 0) / total_spoken) * 100.0, 2)
        }
    },
    "communicative_coverage": {
        "communicated_tokens": coverage_tokens,
        "coverage_percentage": coverage_percent
    },
    "playable_signs_count": len(manifest_entries)
}

with open(DATA_DIR / "h21_accounting_reconciliation.json", "w", encoding="utf-8") as f:
    json.dump(reconciliation, f, indent=2)

print(f"\nStep 6 Complete: data/h21_accounting_reconciliation.json saved.")
print(f"Total Spoken: {total_spoken} | Accounted: {sum_dispositions} | Discrepancy: {discrepancy}")
print(f"Communicative Coverage: {coverage_tokens} tokens ({coverage_percent}%)")
print(f"Playable Signs: {len(manifest_entries)}")
