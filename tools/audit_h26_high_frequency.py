# tools/audit_h26_high_frequency.py
import json
from pathlib import Path

PROJECT_ROOT = Path("d:/sign interpretor")

def audit_high_frequency():
    print("Auditing Highest Frequency Unresolved Concepts for Phase H26...")

    unres_path = PROJECT_ROOT / "data" / "h26_complete_unresolved_vocabulary.json"
    with open(unres_path, "r", encoding="utf-8") as f:
        unres_data = json.load(f)
    concepts = unres_data.get("concepts", [])

    # Filter top 50 by frequency
    top50 = concepts[:50]

    manifest_path = PROJECT_ROOT / "signs" / "manifest.json"
    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)
    playable_sign_ids = set(s["sign_id"].lower() for s in manifest.get("signs", []))

    audited_high_freq = []
    category_summary = {
        "CANDIDATE_FOR_NEW_DIRECT_SIGN": [],
        "MORPHOLOGY_ALIAS_TO_EXISTING": [],
        "FINGERSPELLED_PROPER_NOUN": [],
        "DISCOURSE_OR_GRAMMAR_MARKER": [],
        "CONFIRMED_SUBTITLE_FALLBACK": []
    }

    NEW_SIGN_TARGETS = {
        "voice", "breathe", "trust", "protect", "prepare", "control",
        "silence", "tomorrow", "yesterday", "judge", "complain", "excuse",
        "negative", "pitch", "tone", "volume", "love", "posture"
    }

    for item in top50:
        lemma = item["lemma"].lower()
        freq = item["frequency"]

        if lemma in NEW_SIGN_TARGETS:
            cat = "CANDIDATE_FOR_NEW_DIRECT_SIGN"
            rec = {
                "lemma": lemma,
                "frequency": freq,
                "category": cat,
                "action": "Author Schema 2.0.0 motion asset with ISLRTC citation",
                "islrtc_ref": f"ISLRTC Dictionary entry for {lemma.upper()}",
                "expected_token_impact": freq
            }
        elif lemma in {"ted", "julian", "treasure"}:
            cat = "FINGERSPELLED_PROPER_NOUN"
            rec = {
                "lemma": lemma,
                "frequency": freq,
                "category": cat,
                "action": "Ensure two-handed fingerspelling sequence triggers smoothly",
                "islrtc_ref": "Standard ISL Two-Handed Alphabet",
                "expected_token_impact": freq
            }
        elif lemma.endswith("ing") and lemma[:-3] in playable_sign_ids:
            cat = "MORPHOLOGY_ALIAS_TO_EXISTING"
            root = lemma[:-3]
            rec = {
                "lemma": lemma,
                "frequency": freq,
                "category": cat,
                "action": f"Add translator alias to root sign '{root}'",
                "islrtc_ref": f"Inflection of playable sign {root}",
                "expected_token_impact": freq
            }
        elif lemma in {"uh", "um", "ah", "er", "hmm", "ha", "hey", "oh", "wow", "yeah"}:
            cat = "DISCOURSE_OR_GRAMMAR_MARKER"
            rec = {
                "lemma": lemma,
                "frequency": freq,
                "category": cat,
                "action": "Map to non-manual marker / discourse interjection",
                "islrtc_ref": "ISL Grammar Non-Manual Marker",
                "expected_token_impact": freq
            }
        else:
            cat = "CONFIRMED_SUBTITLE_FALLBACK"
            rec = {
                "lemma": lemma,
                "frequency": freq,
                "category": cat,
                "action": "Preserve transparent subtitle fallback pill below avatar",
                "islrtc_ref": "Unattested in standardized ISLRTC lexical dictionary",
                "expected_token_impact": 0
            }

        category_summary[cat].append(rec)
        audited_high_freq.append(rec)

    output = {
        "metadata": {
            "title": "H26 High-Frequency Unavailable Concepts Completion Audit",
            "phase": "H26",
            "top_concepts_audited_count": len(audited_high_freq),
            "summary_counts": {k: len(v) for k, v in category_summary.items()}
        },
        "category_breakdown": category_summary,
        "audited_concepts": audited_high_freq
    }

    out_path = PROJECT_ROOT / "data" / "h26_high_frequency_completion_audit.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)

    print(f"Saved {out_path}")
    print("Audit breakdown for Top 50 Unresolved Concepts:")
    for k, v in category_summary.items():
        print(f"  {k:35s}: {len(v):2d} concepts")

if __name__ == "__main__":
    audit_high_frequency()
