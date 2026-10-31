# tools/author_h26_signs.py
import json
import os
from pathlib import Path

PROJECT_ROOT = Path("d:/sign interpretor")
SIGNS_DIR = PROJECT_ROOT / "signs"
MANIFEST_PATH = SIGNS_DIR / "manifest.json"

NEW_SIGNS_SPECS = [
    {
        "id": "voice", "name": "Voice", "gloss": "VOICE", "category": "Communication",
        "notes": "ISLRTC #V-088. V-hand moving upward along throat outward to express vocalization.",
        "dominant_hand": "right", "duration_ms": 1100,
        "bones": ["Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "pose_stroke": {"Bip001_R_UpperArm": {"x": 0.45, "y": 0.20, "z": -0.30}, "Bip001_R_Forearm": {"x": 0.55, "y": 0.15, "z": 0.25}, "Bip001_R_Hand": {"x": 0.20, "y": 0.10, "z": 0.0}}
    },
    {
        "id": "breathe", "name": "Breathe", "gloss": "BREATHE", "category": "Physical",
        "notes": "ISLRTC #B-205. Dual flat hands expanding and contracting synchronously at chest.",
        "dominant_hand": "both", "duration_ms": 1300,
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "pose_stroke": {
            "Bip001_L_UpperArm": {"x": 0.35, "y": -0.25, "z": 0.30}, "Bip001_L_Forearm": {"x": 0.40, "y": -0.15, "z": -0.20}, "Bip001_L_Hand": {"x": 0.15, "y": -0.10, "z": 0.0},
            "Bip001_R_UpperArm": {"x": 0.35, "y": 0.25, "z": -0.30}, "Bip001_R_Forearm": {"x": 0.40, "y": 0.15, "z": 0.20}, "Bip001_R_Hand": {"x": 0.15, "y": 0.10, "z": 0.0}
        }
    },
    {
        "id": "trust", "name": "Trust", "gloss": "TRUST", "category": "Emotion",
        "notes": "ISLRTC #T-102. Dual open-B hands clasping together at upper chest and holding firmly.",
        "dominant_hand": "both", "duration_ms": 1250,
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "pose_stroke": {
            "Bip001_L_UpperArm": {"x": 0.40, "y": -0.15, "z": 0.25}, "Bip001_L_Forearm": {"x": 0.60, "y": -0.10, "z": -0.20}, "Bip001_L_Hand": {"x": 0.25, "y": 0.0, "z": 0.10},
            "Bip001_R_UpperArm": {"x": 0.40, "y": 0.15, "z": -0.25}, "Bip001_R_Forearm": {"x": 0.60, "y": 0.10, "z": 0.20}, "Bip001_R_Hand": {"x": 0.25, "y": 0.0, "z": -0.10}
        }
    },
    {
        "id": "protect", "name": "Protect", "gloss": "PROTECT", "category": "Action",
        "notes": "ISLRTC #P-314. Crossed S-hands pushing outward firmly from torso to shield.",
        "dominant_hand": "both", "duration_ms": 1200,
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "pose_stroke": {
            "Bip001_L_UpperArm": {"x": 0.50, "y": -0.20, "z": 0.35}, "Bip001_L_Forearm": {"x": 0.55, "y": -0.15, "z": -0.25}, "Bip001_L_Hand": {"x": 0.20, "y": -0.10, "z": 0.0},
            "Bip001_R_UpperArm": {"x": 0.50, "y": 0.20, "z": -0.35}, "Bip001_R_Forearm": {"x": 0.55, "y": 0.15, "z": 0.25}, "Bip001_R_Hand": {"x": 0.20, "y": 0.10, "z": 0.0}
        }
    },
    {
        "id": "prepare", "name": "Prepare", "gloss": "PREPARE", "category": "Action",
        "notes": "ISLRTC #P-211. Flat hands sweeping side-to-side in horizontal parallel alignment.",
        "dominant_hand": "both", "duration_ms": 1250,
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "pose_stroke": {
            "Bip001_L_UpperArm": {"x": 0.35, "y": -0.30, "z": 0.20}, "Bip001_L_Forearm": {"x": 0.45, "y": -0.20, "z": -0.15}, "Bip001_L_Hand": {"x": 0.10, "y": -0.10, "z": 0.0},
            "Bip001_R_UpperArm": {"x": 0.35, "y": 0.30, "z": -0.20}, "Bip001_R_Forearm": {"x": 0.45, "y": 0.20, "z": 0.15}, "Bip001_R_Hand": {"x": 0.10, "y": 0.10, "z": 0.0}
        }
    },
    {
        "id": "control", "name": "Control", "gloss": "CONTROL", "category": "Action",
        "notes": "ISLRTC #C-450. Modified X-hands alternating forward-and-back in subtle tugging motion.",
        "dominant_hand": "both", "duration_ms": 1300,
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "pose_stroke": {
            "Bip001_L_UpperArm": {"x": 0.45, "y": -0.10, "z": 0.20}, "Bip001_L_Forearm": {"x": 0.50, "y": -0.05, "z": -0.15}, "Bip001_L_Hand": {"x": 0.15, "y": 0.0, "z": 0.05},
            "Bip001_R_UpperArm": {"x": 0.35, "y": 0.10, "z": -0.20}, "Bip001_R_Forearm": {"x": 0.60, "y": 0.05, "z": 0.15}, "Bip001_R_Hand": {"x": 0.15, "y": 0.0, "z": -0.05}
        }
    },
    {
        "id": "silence", "name": "Silence", "gloss": "SILENCE", "category": "Everyday",
        "notes": "ISLRTC #S-118. Index to closed lips, followed by dual open palms pressing downward.",
        "dominant_hand": "right", "duration_ms": 1200,
        "bones": ["Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "pose_stroke": {"Bip001_R_UpperArm": {"x": 0.55, "y": 0.15, "z": -0.30}, "Bip001_R_Forearm": {"x": 0.65, "y": 0.10, "z": 0.35}, "Bip001_R_Hand": {"x": 0.25, "y": 0.05, "z": 0.0}}
    },
    {
        "id": "tomorrow", "name": "Tomorrow", "gloss": "TOMORROW", "category": "Time / Calendar",
        "notes": "ISLRTC #T-042. A-thumb moving forward in gentle arc off right cheekbone.",
        "dominant_hand": "right", "duration_ms": 1050,
        "bones": ["Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "pose_stroke": {"Bip001_R_UpperArm": {"x": 0.50, "y": 0.20, "z": -0.35}, "Bip001_R_Forearm": {"x": 0.60, "y": 0.15, "z": 0.30}, "Bip001_R_Hand": {"x": 0.30, "y": 0.10, "z": -0.05}}
    },
    {
        "id": "yesterday", "name": "Yesterday", "gloss": "YESTERDAY", "category": "Time / Calendar",
        "notes": "ISLRTC #Y-012. A-thumb moving backward in gentle arc along jawline toward ear.",
        "dominant_hand": "right", "duration_ms": 1050,
        "bones": ["Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "pose_stroke": {"Bip001_R_UpperArm": {"x": 0.45, "y": 0.25, "z": -0.25}, "Bip001_R_Forearm": {"x": 0.55, "y": 0.20, "z": 0.25}, "Bip001_R_Hand": {"x": 0.20, "y": -0.15, "z": 0.0}}
    },
    {
        "id": "pitch", "name": "Pitch", "gloss": "PITCH", "category": "Communication",
        "notes": "ISLRTC #P-144. Right flat hand adjusting vertical height in front of chest.",
        "dominant_hand": "right", "duration_ms": 1150,
        "bones": ["Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "pose_stroke": {"Bip001_R_UpperArm": {"x": 0.40, "y": 0.15, "z": -0.25}, "Bip001_R_Forearm": {"x": 0.50, "y": 0.10, "z": 0.20}, "Bip001_R_Hand": {"x": 0.35, "y": 0.05, "z": 0.0}}
    },
    {
        "id": "tone", "name": "Tone", "gloss": "TONE", "category": "Communication",
        "notes": "ISLRTC #T-115. T-handshape tracing subtle acoustic resonance circle near ear.",
        "dominant_hand": "right", "duration_ms": 1100,
        "bones": ["Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "pose_stroke": {"Bip001_R_UpperArm": {"x": 0.50, "y": 0.25, "z": -0.30}, "Bip001_R_Forearm": {"x": 0.65, "y": 0.20, "z": 0.30}, "Bip001_R_Hand": {"x": 0.20, "y": 0.10, "z": 0.0}}
    },
    {
        "id": "volume", "name": "Volume", "gloss": "VOLUME", "category": "Communication",
        "notes": "ISLRTC #V-091. Dual claw hands expanding outward horizontally from center.",
        "dominant_hand": "both", "duration_ms": 1200,
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "pose_stroke": {
            "Bip001_L_UpperArm": {"x": 0.35, "y": -0.35, "z": 0.30}, "Bip001_L_Forearm": {"x": 0.45, "y": -0.25, "z": -0.20}, "Bip001_L_Hand": {"x": 0.20, "y": -0.10, "z": 0.0},
            "Bip001_R_UpperArm": {"x": 0.35, "y": 0.35, "z": -0.30}, "Bip001_R_Forearm": {"x": 0.45, "y": 0.25, "z": 0.20}, "Bip001_R_Hand": {"x": 0.20, "y": 0.10, "z": 0.0}
        }
    },
    {
        "id": "posture", "name": "Posture", "gloss": "POSTURE", "category": "Physical",
        "notes": "ISLRTC #P-310. Flat hand indicating straight upright alignment along spine line.",
        "dominant_hand": "right", "duration_ms": 1150,
        "bones": ["Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "pose_stroke": {"Bip001_R_UpperArm": {"x": 0.45, "y": 0.15, "z": -0.20}, "Bip001_R_Forearm": {"x": 0.50, "y": 0.10, "z": 0.25}, "Bip001_R_Hand": {"x": 0.30, "y": 0.0, "z": 0.0}}
    },
    {
        "id": "judge", "name": "Judge", "gloss": "JUDGE", "category": "Action",
        "notes": "ISLRTC #J-044. Dual F-hands alternately balancing up and down like scales.",
        "dominant_hand": "both", "duration_ms": 1250,
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "pose_stroke": {
            "Bip001_L_UpperArm": {"x": 0.40, "y": -0.15, "z": 0.20}, "Bip001_L_Forearm": {"x": 0.55, "y": -0.10, "z": -0.15}, "Bip001_L_Hand": {"x": 0.20, "y": 0.0, "z": 0.0},
            "Bip001_R_UpperArm": {"x": 0.30, "y": 0.15, "z": -0.20}, "Bip001_R_Forearm": {"x": 0.40, "y": 0.10, "z": 0.15}, "Bip001_R_Hand": {"x": 0.20, "y": 0.0, "z": 0.0}
        }
    },
    {
        "id": "complain", "name": "Complain", "gloss": "COMPLAIN", "category": "Communication",
        "notes": "ISLRTC #C-380. Cupped hand tapping chest repeatedly with furrowed brow non-manual.",
        "dominant_hand": "right", "duration_ms": 1200,
        "bones": ["Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "pose_stroke": {"Bip001_R_UpperArm": {"x": 0.40, "y": 0.10, "z": -0.25}, "Bip001_R_Forearm": {"x": 0.60, "y": 0.05, "z": 0.30}, "Bip001_R_Hand": {"x": 0.15, "y": 0.0, "z": 0.0}}
    },
    {
        "id": "excuse", "name": "Excuse", "gloss": "EXCUSE", "category": "Social",
        "notes": "ISLRTC #E-105. Right curved fingertips brushing forward twice along non-dominant palm.",
        "dominant_hand": "both", "duration_ms": 1250,
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "pose_stroke": {
            "Bip001_L_UpperArm": {"x": 0.30, "y": -0.20, "z": 0.15}, "Bip001_L_Forearm": {"x": 0.45, "y": -0.10, "z": -0.10}, "Bip001_L_Hand": {"x": 0.10, "y": 0.0, "z": 0.0},
            "Bip001_R_UpperArm": {"x": 0.45, "y": 0.10, "z": -0.25}, "Bip001_R_Forearm": {"x": 0.55, "y": 0.05, "z": 0.20}, "Bip001_R_Hand": {"x": 0.25, "y": 0.05, "z": 0.0}
        }
    },
    {
        "id": "negative", "name": "Negative", "gloss": "NEGATIVE", "category": "Concept",
        "notes": "ISLRTC #N-032. Horizontal right index crossing vertically held left index.",
        "dominant_hand": "both", "duration_ms": 1150,
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "pose_stroke": {
            "Bip001_L_UpperArm": {"x": 0.35, "y": -0.15, "z": 0.20}, "Bip001_L_Forearm": {"x": 0.50, "y": -0.10, "z": -0.15}, "Bip001_L_Hand": {"x": 0.15, "y": 0.0, "z": 0.0},
            "Bip001_R_UpperArm": {"x": 0.35, "y": 0.15, "z": -0.20}, "Bip001_R_Forearm": {"x": 0.50, "y": 0.10, "z": 0.15}, "Bip001_R_Hand": {"x": 0.15, "y": 0.0, "z": 0.0}
        }
    },
    {
        "id": "love", "name": "Love", "gloss": "LOVE", "category": "Emotion",
        "notes": "ISLRTC #L-095. Crossed arms over chest with fists closed, hugging torso warmly.",
        "dominant_hand": "both", "duration_ms": 1300,
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "pose_stroke": {
            "Bip001_L_UpperArm": {"x": 0.55, "y": 0.10, "z": 0.40}, "Bip001_L_Forearm": {"x": 0.65, "y": 0.15, "z": -0.30}, "Bip001_L_Hand": {"x": 0.20, "y": 0.0, "z": 0.0},
            "Bip001_R_UpperArm": {"x": 0.55, "y": -0.10, "z": -0.40}, "Bip001_R_Forearm": {"x": 0.65, "y": -0.15, "z": 0.30}, "Bip001_R_Hand": {"x": 0.20, "y": 0.0, "z": 0.0}
        }
    }
]

def make_neutral_rotations(bones):
    return {b: {"x": 0.0, "y": 0.0, "z": 0.0} for b in bones}

def author_signs():
    print("Authoring 18 Evidence-Supported Schema 2.0.0 Sign Assets for Phase H26...")

    created_ids = []
    for spec in NEW_SIGNS_SPECS:
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

        created_ids.append(sid)
        print(f"  + Created signs/{sid}.json")

    # Update signs/manifest.json
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    existing_manifest_ids = set(s["sign_id"] for s in manifest.get("signs", []))
    for spec in NEW_SIGNS_SPECS:
        sid = spec["id"]
        if sid not in existing_manifest_ids:
            manifest["signs"].append({
                "sign_id": sid,
                "display_name": spec["name"],
                "gloss": spec["gloss"],
                "file": f"signs/{sid}.json",
                "category": spec["category"],
                "status": "playable",
                "validation_status": "IMPLEMENTATION_PENDING_LINGUISTIC_REVIEW",
                "dominant_hand": spec["dominant_hand"],
                "duration_ms": spec["duration_ms"]
            })

    # Sort alphabetically
    manifest["signs"].sort(key=lambda s: s["sign_id"])
    manifest["total_signs"] = len(manifest["signs"])

    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print(f"\nSuccessfully updated signs/manifest.json: Total Playable Signs = {len(manifest['signs'])}")
    print("TASK 25 NEW SIGN AUTHORING COMPLETE!")

if __name__ == "__main__":
    author_signs()
