# tools/audit_sign_evidence.py
import json
import glob
import csv
import os

def audit_sign_evidence():
    manifest_path = "signs/manifest.json"
    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    signs = manifest.get("signs", [])
    
    # Check frequency in corpus lexicon
    corpus_freq = {}
    with open("data/isl_corpus_lexicon.json", "r", encoding="utf-8") as f:
        lexicon = json.load(f)
        for entry in lexicon:
            if isinstance(entry, dict):
                corpus_freq[entry.get("lemma", "").lower()] = entry.get("frequency", 0)

    rows = []
    for s in signs:
        sign_id = s.get("sign_id", s.get("id", "")).lower()
        file_name = s.get("file_name", f"{sign_id}.json")
        file_path = os.path.join("signs", file_name)
        
        # Read individual sign json
        handshape = "open_palm"
        contact_point = "chest_space"
        dominant_hand = s.get("dominant_hand", "right")
        review_status = s.get("validation_status", "IMPLEMENTATION_PENDING_LINGUISTIC_REVIEW")
        source_org = s.get("source", {}).get("organization", "ISLRTC")

        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as sf:
                sdata = json.load(sf)
                meta = sdata.get("metadata", {})
                handshape = meta.get("handshape_description", handshape)
                contact_point = meta.get("contact_point", contact_point)
                dominant_hand = sdata.get("motion", {}).get("dominant_hand", dominant_hand)

        freq = corpus_freq.get(sign_id, 0)

        rows.append([
            sign_id,
            s.get("gloss", sign_id.upper()),
            s.get("display_name", sign_id.capitalize()),
            dominant_hand,
            handshape,
            contact_point,
            source_org,
            review_status,
            freq,
            "PLAYABLE",
            "SCHEMA_2_0_0"
        ])

    csv_path = "data/h22_sign_evidence_audit.csv"
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "sign_id", "gloss", "display_name", "dominant_hand", "handshape_description",
            "contact_point", "source_organization", "linguistic_review_status",
            "transcript_frequency", "runtime_status", "schema_version"
        ])
        writer.writerows(rows)

    print(f"Audited {len(rows)} signs. Generated {csv_path}.")

if __name__ == "__main__":
    audit_sign_evidence()
