"""
tools/author_6_additional_signs.py

Phase H21: Authoring 6 additional high-impact signs from ISLRTC Academic & Everyday:
reason, example, topic, study, college, parent.
Guarantees exact neutral start and return { x: 0, y: 0, z: 0 }.
"""

import json
from pathlib import Path

SIGNS_DIR = Path(__file__).resolve().parent.parent / "signs"

SPECS_6 = [
    {
        "id": "reason",
        "name": "Reason",
        "gloss": "REASON",
        "duration": 1300,
        "type": "Academic / Cognitive",
        "notes": "ISLRTC Academic. Right 'R' handshape making small circular motion at right temple indicating logical rationale.",
        "dominant": "right",
        "bones": ["Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 300, "r_arm": [-0.5, 0.2, 0.4], "r_fore": [1.0, 0.3, 0.2], "r_hand": [0.3, 0.1, -0.1], "head": [0.05, 0.0, 0.0], "curls": [0.8, 0.0, 0.0, 0.8, 0.8]},
            {"time": 700, "r_arm": [-0.52, 0.22, 0.42], "r_fore": [1.05, 0.3, 0.2], "r_hand": [0.35, 0.15, -0.1], "head": [0.05, 0.0, 0.0], "curls": [0.8, 0.0, 0.0, 0.8, 0.8]},
            {"time": 1000, "r_arm": [-0.2, 0.1, 0.1], "r_fore": [0.4, 0.1, 0.0], "r_hand": [0.0, 0.0, 0.0], "head": [0.0, 0.0, 0.0], "curls": [0.2, 0.0, 0.0, 0.2, 0.2]}
        ]
    },
    {
        "id": "example",
        "name": "Example",
        "gloss": "EXAMPLE",
        "duration": 1350,
        "type": "Academic / Pedagogical",
        "notes": "ISLRTC Academic. Right 'E' handshape touching base left vertical palm and moving forward.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 350, "r_arm": [-0.4, 0.2, 0.3], "r_fore": [0.8, 0.2, 0.2], "r_hand": [0.2, 0.1, -0.1], "l_arm": [-0.3, -0.2, -0.3], "l_fore": [0.6, -0.1, -0.1], "l_hand": [-0.2, 0.0, 0.0], "curls": [0.7, 0.6, 0.6, 0.6, 0.6]},
            {"time": 750, "r_arm": [-0.3, 0.2, 0.2], "r_fore": [0.6, 0.2, 0.1], "r_hand": [0.1, 0.1, -0.1], "l_arm": [-0.3, -0.2, -0.3], "l_fore": [0.6, -0.1, -0.1], "l_hand": [-0.2, 0.0, 0.0], "curls": [0.7, 0.6, 0.6, 0.6, 0.6]},
            {"time": 1050, "r_arm": [-0.2, 0.1, 0.1], "r_fore": [0.3, 0.1, 0.0], "r_hand": [0.0, 0.0, 0.0], "l_arm": [-0.1, -0.1, -0.1], "l_fore": [0.3, 0.0, 0.0], "l_hand": [0.0, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "topic",
        "name": "Topic",
        "gloss": "TOPIC",
        "duration": 1250,
        "type": "Academic / Discourse",
        "notes": "ISLRTC Academic. Both curved 'V' handshapes (rabbit ears) flexing forward emphasizing specific subject.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "r_arm": [-0.3, 0.2, 0.3], "r_fore": [0.7, 0.2, 0.2], "r_hand": [0.3, 0.1, -0.1], "l_arm": [-0.3, -0.2, -0.3], "l_fore": [0.7, -0.2, -0.2], "l_hand": [0.3, -0.1, 0.1], "curls": [0.8, 0.4, 0.4, 0.9, 0.9]},
            {"time": 700, "r_arm": [-0.35, 0.2, 0.3], "r_fore": [0.75, 0.2, 0.2], "r_hand": [0.35, 0.1, -0.1], "l_arm": [-0.35, -0.2, -0.3], "l_fore": [0.75, -0.2, -0.2], "l_hand": [0.35, -0.1, 0.1], "curls": [0.8, 0.6, 0.6, 0.9, 0.9]},
            {"time": 1000, "r_arm": [-0.2, 0.1, 0.1], "r_fore": [0.4, 0.1, 0.0], "r_hand": [0.0, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.1], "l_fore": [0.4, -0.1, 0.0], "l_hand": [0.0, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "study",
        "name": "Study",
        "gloss": "STUDY",
        "duration": 1350,
        "type": "Academic / Pedagogical",
        "notes": "ISLRTC Academic. Right fingers fluttering actively toward base upturned left flat palm (absorbing knowledge).",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 350, "r_arm": [-0.4, 0.2, 0.3], "r_fore": [0.8, 0.2, 0.2], "r_hand": [0.3, 0.2, -0.1], "l_arm": [-0.3, -0.2, -0.3], "l_fore": [0.6, -0.1, -0.1], "l_hand": [0.0, 0.0, 0.0], "head": [0.05, 0.0, 0.0], "curls": [0.1, 0.3, 0.1, 0.3, 0.1]},
            {"time": 750, "r_arm": [-0.38, 0.2, 0.3], "r_fore": [0.82, 0.2, 0.2], "r_hand": [0.32, 0.2, -0.1], "l_arm": [-0.3, -0.2, -0.3], "l_fore": [0.6, -0.1, -0.1], "l_hand": [0.0, 0.0, 0.0], "head": [0.08, 0.0, 0.0], "curls": [0.3, 0.1, 0.3, 0.1, 0.3]},
            {"time": 1050, "r_arm": [-0.2, 0.1, 0.1], "r_fore": [0.4, 0.1, 0.0], "r_hand": [0.0, 0.0, 0.0], "l_arm": [-0.1, -0.1, -0.1], "l_fore": [0.3, 0.0, 0.0], "l_hand": [0.0, 0.0, 0.0], "head": [0.0, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "college",
        "name": "College",
        "gloss": "COLLEGE",
        "duration": 1300,
        "type": "Academic / Institutional",
        "notes": "ISLRTC Academic. Right flat palm clapping against base left flat palm then sweeping upward in arcing trajectory.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "r_arm": [-0.3, 0.1, 0.2], "r_fore": [0.7, 0.2, 0.1], "r_hand": [0.1, 0.1, -0.1], "l_arm": [-0.3, -0.1, -0.2], "l_fore": [0.7, -0.2, -0.1], "l_hand": [0.1, -0.1, 0.1], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 750, "r_arm": [-0.6, 0.3, 0.5], "r_fore": [0.9, 0.2, 0.2], "r_hand": [0.2, 0.2, -0.2], "l_arm": [-0.3, -0.1, -0.2], "l_fore": [0.6, -0.1, -0.1], "l_hand": [0.0, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 1050, "r_arm": [-0.2, 0.1, 0.1], "r_fore": [0.4, 0.1, 0.0], "r_hand": [0.0, 0.0, 0.0], "l_arm": [-0.1, -0.1, -0.1], "l_fore": [0.3, 0.0, 0.0], "l_hand": [0.0, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "parent",
        "name": "Parent",
        "gloss": "PARENT",
        "duration": 1350,
        "type": "Everyday / Family",
        "notes": "ISLRTC Everyday. Right hand touching forehead (father locus) then chin (mother locus) expressing parental bond.",
        "dominant": "right",
        "bones": ["Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 300, "r_arm": [-0.5, 0.2, 0.4], "r_fore": [1.1, 0.3, 0.2], "r_hand": [0.3, 0.1, -0.1], "head": [0.05, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 750, "r_arm": [-0.4, 0.1, 0.3], "r_fore": [0.9, 0.2, 0.2], "r_hand": [0.2, 0.1, -0.1], "head": [0.0, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 1050, "r_arm": [-0.2, 0.1, 0.1], "r_fore": [0.4, 0.1, 0.0], "r_hand": [0.0, 0.0, 0.0], "head": [0.0, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    }
]

def build_rotations(kf, bones):
    rot = {}
    for b in bones:
        if "R_UpperArm" in b: val = kf.get("r_arm", [0, 0, 0])
        elif "R_Forearm" in b: val = kf.get("r_fore", [0, 0, 0])
        elif "R_Hand" in b: val = kf.get("r_hand", [0, 0, 0])
        elif "L_UpperArm" in b: val = kf.get("l_arm", [0, 0, 0])
        elif "L_Forearm" in b: val = kf.get("l_fore", [0, 0, 0])
        elif "L_Hand" in b: val = kf.get("l_hand", [0, 0, 0])
        elif "Head" in b: val = kf.get("head", [0, 0, 0])
        else: val = [0, 0, 0]
        rot[b] = {"x": round(val[0], 3), "y": round(val[1], 3), "z": round(val[2], 3)}
    return rot

for spec in SPECS_6:
    sign_id = spec["id"]
    duration = spec["duration"]
    bones = spec["bones"]
    
    kf0 = {
        "time_ms": 0, "label": "Neutral", "easing": "easeInOutQuad",
        "rotations": {b: {"x": 0.0, "y": 0.0, "z": 0.0} for b in bones},
        "finger_curls": {"thumb": 0.0, "index": 0.0, "middle": 0.0, "ring": 0.0, "pinky": 0.0}
    }
    mid_kfs = []
    for k in spec["keyframes"]:
        c = k.get("curls", [0, 0, 0, 0, 0])
        mid_kfs.append({
            "time_ms": k["time"], "label": f"Articulation_{k['time']}ms", "easing": "easeInOutQuad",
            "rotations": build_rotations(k, bones),
            "finger_curls": {"thumb": round(c[0], 2), "index": round(c[1], 2), "middle": round(c[2], 2), "ring": round(c[3], 2), "pinky": round(c[4], 2)}
        })
    kf_end = {
        "time_ms": duration, "label": "Neutral_Return", "easing": "easeInOutQuad",
        "rotations": {b: {"x": 0.0, "y": 0.0, "z": 0.0} for b in bones},
        "finger_curls": {"thumb": 0.0, "index": 0.0, "middle": 0.0, "ring": 0.0, "pinky": 0.0}
    }
    asset = {
        "schema_version": "2.0.0",
        "sign_id": sign_id,
        "metadata": {
            "display_name": spec["name"], "gloss": spec["gloss"], "language": "ISL",
            "lexical_type": f"ISL Lexical Sign ({spec['type']})",
            "validation_status": "IMPLEMENTATION_PENDING_LINGUISTIC_REVIEW",
            "source": {"organization": "ISLRTC", "portal": "Indian Sign Language Research and Training Centre", "url": "https://divyangjan.depwd.gov.in/islrtc/"},
            "notes": spec["notes"]
        },
        "motion": {
            "status": "playable", "duration_ms": duration, "dominant_hand": spec["dominant"], "return_to_neutral": True,
            "transition_hints": {"safe_transition": "neutral", "direct_blend_supported": False},
            "involved_bones": bones, "keyframes": [kf0] + mid_kfs + [kf_end]
        }
    }
    with open(SIGNS_DIR / f"{sign_id}.json", "w", encoding="utf-8") as f:
        json.dump(asset, f, indent=2)
    print(f"Authored: signs/{sign_id}.json")
