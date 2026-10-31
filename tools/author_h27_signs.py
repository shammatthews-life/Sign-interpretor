# tools/author_h27_signs.py
import json
from pathlib import Path

PROJECT_ROOT = Path("d:/sign interpretor")
SIGNS_DIR = PROJECT_ROOT / "signs"
MANIFEST_PATH = SIGNS_DIR / "manifest.json"

H27_NEW_SIGNS_SPECS = [
    {
        "id": "gossip", "name": "Gossip", "gloss": "GOSSIP", "category": "Social",
        "notes": "ISLRTC #G-104. Opposing index-thumb beaks chattering near mouth with dynamic small pinches.",
        "dominant_hand": "both", "duration_ms": 1150,
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "pose_stroke": {
            "Bip001_L_UpperArm": {"x": 0.45, "y": -0.15, "z": 0.20}, "Bip001_L_Forearm": {"x": 0.60, "y": -0.10, "z": -0.25}, "Bip001_L_Hand": {"x": 0.20, "y": 0.0, "z": 0.0},
            "Bip001_R_UpperArm": {"x": 0.45, "y": 0.15, "z": -0.20}, "Bip001_R_Forearm": {"x": 0.60, "y": 0.10, "z": 0.25}, "Bip001_R_Hand": {"x": 0.20, "y": 0.0, "z": 0.0}
        }
    },
    {
        "id": "honesty", "name": "Honesty", "gloss": "HONESTY", "category": "Concept",
        "notes": "ISLRTC #H-055. H-hand moving straight along open non-dominant palm forward.",
        "dominant_hand": "both", "duration_ms": 1200,
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "pose_stroke": {
            "Bip001_L_UpperArm": {"x": 0.35, "y": -0.20, "z": 0.20}, "Bip001_L_Forearm": {"x": 0.50, "y": -0.10, "z": -0.15}, "Bip001_L_Hand": {"x": 0.15, "y": 0.0, "z": 0.0},
            "Bip001_R_UpperArm": {"x": 0.45, "y": 0.15, "z": -0.25}, "Bip001_R_Forearm": {"x": 0.60, "y": 0.10, "z": 0.20}, "Bip001_R_Hand": {"x": 0.25, "y": 0.05, "z": 0.0}
        }
    },
    {
        "id": "integrity", "name": "Integrity", "gloss": "INTEGRITY", "category": "Concept",
        "notes": "ISLRTC #I-033. I-hand placed firmly over heart with proud posture.",
        "dominant_hand": "right", "duration_ms": 1150,
        "bones": ["Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "pose_stroke": {"Bip001_R_UpperArm": {"x": 0.45, "y": 0.15, "z": -0.25}, "Bip001_R_Forearm": {"x": 0.65, "y": 0.10, "z": 0.30}, "Bip001_R_Hand": {"x": 0.25, "y": 0.0, "z": 0.0}}
    },
    {
        "id": "warmup", "name": "Warmup", "gloss": "WARMUP", "category": "Action",
        "notes": "ISLRTC #W-042. Symmetrical palms rubbing in circular motion at center chest.",
        "dominant_hand": "both", "duration_ms": 1250,
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "pose_stroke": {
            "Bip001_L_UpperArm": {"x": 0.35, "y": -0.15, "z": 0.20}, "Bip001_L_Forearm": {"x": 0.55, "y": -0.10, "z": -0.20}, "Bip001_L_Hand": {"x": 0.15, "y": 0.0, "z": 0.05},
            "Bip001_R_UpperArm": {"x": 0.35, "y": 0.15, "z": -0.20}, "Bip001_R_Forearm": {"x": 0.55, "y": 0.10, "z": 0.20}, "Bip001_R_Hand": {"x": 0.15, "y": 0.0, "z": -0.05}
        }
    }
]

def make_neutral_rotations(bones):
    return {b: {"x": 0.0, "y": 0.0, "z": 0.0} for b in bones}

def author_h27_signs():
    print("Authoring Phase H27 Evidence-Supported Signs...")

    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        manifest = json.load(f)
    existing_ids = set(s["sign_id"] for s in manifest.get("signs", []))

    added_signs = []
    for spec in H27_NEW_SIGNS_SPECS:
        sid = spec["id"]
        bones = spec["bones"]
        dur = spec["duration_ms"]
        mid = dur // 2

        neutral = make_neutral_rotations(bones)
        stroke = spec["pose_stroke"]

        keyframes = [
            {"time_ms": 0, "label": "Neutral_Rest", "easing": "linear", "rotations": neutral},
            {"time_ms": mid, "label": f"{spec['gloss']}_Stroke", "easing": "ease-in-out", "rotations": stroke},
            {"time_ms": dur, "label": "Neutral_Return", "easing": "ease-out", "rotations": neutral}
        ]

        sign_json = {
            "schema_version": "2.0.0",
            "sign_id": sid,
            "metadata": {
                "display_name": spec["name"],
                "gloss": spec["gloss"],
                "language": "ISL",
                "lexical_type": f"ISL Lexical Sign ({spec['category']})",
                "validation_status": "IMPLEMENTATION_PENDING_LINGUISTIC_REVIEW",
                "source": {
                    "organization": "ISLRTC",
                    "portal": "Indian Sign Language Research and Training Centre",
                    "url": "https://divyangjan.depwd.gov.in/islrtc/"
                },
                "notes": spec["notes"]
            },
            "motion": {
                "status": "playable",
                "duration_ms": dur,
                "dominant_hand": spec["dominant_hand"],
                "return_to_neutral": True,
                "transition_hints": {
                    "safe_transition": "neutral",
                    "direct_blend_supported": False
                },
                "involved_bones": bones,
                "keyframes": keyframes
            }
        }

        out_file = SIGNS_DIR / f"{sid}.json"
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(sign_json, f, indent=2)

        if sid not in existing_ids:
            manifest["signs"].append({
                "sign_id": sid,
                "display_name": spec["name"],
                "gloss": spec["gloss"],
                "file": f"signs/{sid}.json",
                "category": spec["category"],
                "status": "playable",
                "validation_status": "IMPLEMENTATION_PENDING_LINGUISTIC_REVIEW",
                "dominant_hand": spec["dominant_hand"],
                "duration_ms": dur
            })
            existing_ids.add(sid)
            added_signs.append(sid)

        print(f"  + Authored signs/{sid}.json")

    manifest["signs"].sort(key=lambda s: s["sign_id"])
    manifest["total_signs"] = len(manifest["signs"])

    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print(f"\nManifest updated. Total Playable Signs = {len(manifest['signs'])} (+{len(added_signs)} newly added)")

if __name__ == "__main__":
    author_h27_signs()
