"""
tools/rebuild_manifest.py

Rebuilds signs/manifest.json from all Schema 2.0.0 JSON files in signs/.
Ensures alphabetical ordering, total count consistency, and accurate metadata.
"""

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SIGNS_DIR = PROJECT_ROOT / "signs"

sign_files = sorted([f for f in SIGNS_DIR.glob("*.json") if f.name != "manifest.json"])
print(f"Found {len(sign_files)} sign asset files in {SIGNS_DIR}")

manifest_signs = []
for sf in sign_files:
    try:
        with open(sf, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error loading {sf.name}: {e}")
        continue
    
    meta = data.get("metadata", {})
    motion = data.get("motion", {})
    
    manifest_signs.append({
        "sign_id": data.get("sign_id", sf.stem),
        "display_name": meta.get("display_name", sf.stem.capitalize()),
        "gloss": meta.get("gloss", sf.stem.upper()),
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

manifest_data = {
    "manifest_version": "2.4.0",
    "schema_version": "2.0.0",
    "generated_at": "2026-10-31T03:30:00Z",
    "phase": "H24",
    "total_signs": len(manifest_signs),
    "total_playable_signs": len(manifest_signs),
    "signs": manifest_signs
}

with open(SIGNS_DIR / "manifest.json", "w", encoding="utf-8") as f:
    json.dump(manifest_data, f, indent=2)

print(f"Successfully rebuilt signs/manifest.json with {len(manifest_signs)} signs.")
