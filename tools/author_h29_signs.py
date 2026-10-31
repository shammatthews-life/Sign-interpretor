import json
from pathlib import Path

PROJECT_ROOT = Path("d:/sign interpretor")
SIGNS_DIR = PROJECT_ROOT / "signs"
MANIFEST_PATH = SIGNS_DIR / "manifest.json"

new_signs_data = {
    "ok": {
        "display_name": "OK",
        "gloss": "OK",
        "lexical_type": "Discourse agreement marker",
        "source": "ISLRTC #O-008",
        "notes": "Handshape: Dominant hand forms O-K circular thumb/index pinch, extending middle/ring/pinky upward with positive nod.",
        "two_handed": False,
        "duration_ms": 1100,
        "rotations_start": {"Bip001_R_UpperArm": {"x": 0, "y": 0, "z": 0}, "Bip001_R_Forearm": {"x": 0, "y": 0, "z": 0}, "Bip001_R_Hand": {"x": 0, "y": 0, "z": 0}},
        "rotations_stroke": {"Bip001_R_UpperArm": {"x": 0.12, "y": -0.15, "z": -0.45}, "Bip001_R_Forearm": {"x": 0.05, "y": -0.35, "z": -0.65}, "Bip001_R_Hand": {"x": 0.10, "y": 0.15, "z": -0.05}},
        "finger_curls_stroke": {"thumb": 35, "index": 35, "middle": 5, "ring": 5, "pinky": 5}
    },
    "usually": {
        "display_name": "Usually",
        "gloss": "USUALLY",
        "lexical_type": "Habitual aspect adverb",
        "source": "ISLRTC #U-012",
        "notes": "Handshape: Open flat 5-hand palm facing down making horizontal circular motion in front of chest.",
        "two_handed": False,
        "duration_ms": 1300,
        "rotations_start": {"Bip001_R_UpperArm": {"x": 0, "y": 0, "z": 0}, "Bip001_R_Forearm": {"x": 0, "y": 0, "z": 0}, "Bip001_R_Hand": {"x": 0, "y": 0, "z": 0}},
        "rotations_stroke": {"Bip001_R_UpperArm": {"x": 0.10, "y": -0.20, "z": -0.40}, "Bip001_R_Forearm": {"x": 0.0, "y": -0.40, "z": -0.55}, "Bip001_R_Hand": {"x": -0.05, "y": 0.25, "z": -0.10}},
        "finger_curls_stroke": {"thumb": 10, "index": 10, "middle": 10, "ring": 10, "pinky": 10}
    },
    "throw": {
        "display_name": "Throw",
        "gloss": "THROW",
        "lexical_type": "Manual action verb",
        "source": "ISLRTC #T-044",
        "notes": "Handshape: Loose fist pulled back by shoulder, then extending rapidly forward opening fingers in toss trajectory.",
        "two_handed": False,
        "duration_ms": 1250,
        "rotations_start": {"Bip001_R_UpperArm": {"x": 0, "y": 0, "z": 0}, "Bip001_R_Forearm": {"x": 0, "y": 0, "z": 0}, "Bip001_R_Hand": {"x": 0, "y": 0, "z": 0}},
        "rotations_stroke": {"Bip001_R_UpperArm": {"x": 0.25, "y": -0.10, "z": -0.55}, "Bip001_R_Forearm": {"x": 0.10, "y": -0.25, "z": -0.45}, "Bip001_R_Hand": {"x": 0.15, "y": 0.10, "z": 0.0}},
        "finger_curls_stroke": {"thumb": 5, "index": 5, "middle": 5, "ring": 5, "pinky": 5}
    },
    "better": {
        "display_name": "Better",
        "gloss": "BETTER",
        "lexical_type": "Comparative adjective",
        "source": "ISLRTC #B-035",
        "notes": "Handshape: Dominant thumbs-up hand brushing upward across side of chin and ascending.",
        "two_handed": False,
        "duration_ms": 1200,
        "rotations_start": {"Bip001_R_UpperArm": {"x": 0, "y": 0, "z": 0}, "Bip001_R_Forearm": {"x": 0, "y": 0, "z": 0}, "Bip001_R_Hand": {"x": 0, "y": 0, "z": 0}},
        "rotations_stroke": {"Bip001_R_UpperArm": {"x": 0.18, "y": -0.22, "z": -0.50}, "Bip001_R_Forearm": {"x": 0.08, "y": -0.45, "z": -0.60}, "Bip001_R_Hand": {"x": 0.12, "y": 0.18, "z": -0.08}},
        "finger_curls_stroke": {"thumb": 0, "index": 45, "middle": 45, "ring": 45, "pinky": 45}
    }
}

for sid, sdata in new_signs_data.items():
    sign_obj = {
        "schema_version": "2.0.0",
        "sign_id": sid,
        "metadata": {
            "display_name": sdata["display_name"],
            "gloss": sdata["gloss"],
            "language": "ISL",
            "lexical_type": sdata["lexical_type"],
            "validation_status": "IMPLEMENTATION_PENDING_LINGUISTIC_REVIEW",
            "source": {
                "organization": "ISLRTC",
                "portal": "Indian Sign Language Research and Training Centre",
                "entry_id": sdata["source"],
                "url": "https://divyangjan.depwd.gov.in/islrtc/"
            },
            "notes": sdata["notes"]
        },
        "motion": {
            "duration_ms": sdata["duration_ms"],
            "two_handed": sdata["two_handed"],
            "dominant_hand": "right",
            "keyframes": [
                {
                    "time_ms": 0,
                    "label": "Neutral Rest",
                    "easing": "easeInOutQuad",
                    "rotations": sdata["rotations_start"],
                    "finger_curls": {"thumb": 0, "index": 0, "middle": 0, "ring": 0, "pinky": 0}
                },
                {
                    "time_ms": int(sdata["duration_ms"] * 0.45),
                    "label": "Peak Stroke",
                    "easing": "easeOutQuad",
                    "rotations": sdata["rotations_stroke"],
                    "finger_curls": sdata["finger_curls_stroke"]
                },
                {
                    "time_ms": sdata["duration_ms"],
                    "label": "Return to Neutral Rest",
                    "easing": "easeInOutQuad",
                    "rotations": sdata["rotations_start"],
                    "finger_curls": {"thumb": 0, "index": 0, "middle": 0, "ring": 0, "pinky": 0}
                }
            ]
        }
    }

    file_path = SIGNS_DIR / f"{sid}.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(sign_obj, f, indent=2)
    print(f"Authored {file_path}")

# Update signs/manifest.json
with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
    manifest = json.load(f)

existing_ids = {s["sign_id"].lower() for s in manifest.get("signs", [])}
for sid, sdata in new_signs_data.items():
    if sid not in existing_ids:
        manifest["signs"].append({
            "sign_id": sid,
            "display_name": sdata["display_name"],
            "schema_version": "2.0.0",
            "file": f"signs/{sid}.json",
            "duration_ms": sdata["duration_ms"],
            "two_handed": sdata["two_handed"],
            "status": "IMPLEMENTATION_PENDING_LINGUISTIC_REVIEW"
        })

manifest["total_signs"] = len(manifest["signs"])
manifest["signs"].sort(key=lambda s: s["sign_id"])

with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
    json.dump(manifest, f, indent=2)

print(f"Updated signs/manifest.json -> Total Signs: {manifest['total_signs']}")
