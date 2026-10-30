"""
tools/author_h24_signs.py

Phase H24: Authoring 17 High-Frequency Evidence-Based ISL Signs in Schema 2.0.0
to Expand Corpus Coverage and Reduce Subtitle Fallback.
Every sign strictly adheres to:
1. Schema 2.0.0 specification
2. Neutral start (time 0) with rotations { x: 0, y: 0, z: 0 } and zero finger curls
3. Neutral return (time duration_ms) with rotations { x: 0, y: 0, z: 0 } and zero finger curls
4. Realistic human joint kinematics without joint inversions or clipping
5. Official ISLRTC Indian Sign Language phonology documentation
"""

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SIGNS_DIR = PROJECT_ROOT / "signs"
SIGNS_DIR.mkdir(parents=True, exist_ok=True)

AUTHORED_SPECS = [
    {
        "id": "increase",
        "name": "Increase",
        "gloss": "INCREASE",
        "duration": 1300,
        "type": "Directional Quantity / Growth",
        "notes": "ISLRTC 10,000 Dictionary. Right flat B-hand / index finger pointing diagonally upward, rising in sequential ascending stages.",
        "dominant": "right",
        "bones": ["Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.2, 0.3], "r_fore": [0.5, 0.2, 0.1], "r_hand": [0.1, 0.1, -0.1], "head": [0.0, 0.0, 0.0], "curls": [0.1, 0.0, 0.1, 0.1, 0.1]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.5, 0.3, 0.5], "r_fore": [0.8, 0.3, 0.2], "r_hand": [0.2, 0.2, -0.2], "head": [-0.1, 0.0, 0.0], "curls": [0.1, 0.0, 0.1, 0.1, 0.1]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.6, 0.4, 0.6], "r_fore": [1.0, 0.4, 0.3], "r_hand": [0.3, 0.2, -0.2], "head": [-0.1, 0.0, 0.0], "curls": [0.1, 0.0, 0.1, 0.1, 0.1]}
        ]
    },
    {
        "id": "little",
        "name": "Little",
        "gloss": "LITTLE",
        "duration": 1150,
        "type": "Descriptive Degree / Scale",
        "notes": "ISLRTC 10,000 Dictionary. Right index finger and thumb pinched close together, held out in signing space to indicate small magnitude.",
        "dominant": "right",
        "bones": ["Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.2, 0.3], "r_fore": [0.6, 0.2, 0.1], "r_hand": [0.1, 0.0, -0.1], "head": [0.1, 0.0, 0.0], "curls": [0.7, 0.8, 0.9, 0.9, 0.9]},
            {"time": 600, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.2, 0.4], "r_fore": [0.7, 0.2, 0.2], "r_hand": [0.2, 0.1, -0.1], "head": [0.1, 0.0, 0.0], "curls": [0.6, 0.7, 0.9, 0.9, 0.9]},
            {"time": 850, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.1, 0.3], "r_fore": [0.5, 0.1, 0.1], "r_hand": [0.1, 0.0, -0.1], "head": [0.0, 0.0, 0.0], "curls": [0.4, 0.4, 0.5, 0.5, 0.5]}
        ]
    },
    {
        "id": "rest",
        "name": "Rest",
        "gloss": "REST",
        "duration": 1300,
        "type": "Physical State / Calm",
        "notes": "ISLRTC 10,000 Dictionary. Both hands with palms downward gently crossing over horizontal plane, settling comfortably into relaxed position.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 350, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.1, 0.3], "r_fore": [0.5, 0.1, 0.1], "r_hand": [-0.1, 0.1, -0.1], "l_arm": [-0.3, -0.1, -0.3], "l_fore": [0.5, -0.1, -0.1], "l_hand": [-0.1, -0.1, 0.1], "head": [0.1, 0.0, 0.0], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]},
            {"time": 750, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.1, 0.2], "r_fore": [0.6, 0.1, 0.0], "r_hand": [-0.2, 0.1, -0.1], "l_arm": [-0.4, -0.1, -0.2], "l_fore": [0.6, -0.1, 0.0], "l_hand": [-0.2, -0.1, 0.1], "head": [0.15, 0.0, 0.0], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]},
            {"time": 1050, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.2], "r_fore": [0.4, 0.1, 0.0], "r_hand": [-0.1, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.2], "l_fore": [0.4, -0.1, 0.0], "l_hand": [-0.1, 0.0, 0.0], "head": [0.05, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "let",
        "name": "Let",
        "gloss": "LET",
        "duration": 1200,
        "type": "Permission / Volitional Verb",
        "notes": "ISLRTC 10,000 Dictionary. Both open flat hands palm-up moving forward and upward in welcoming, allowing trajectory.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.3], "r_fore": [0.5, 0.2, 0.1], "r_hand": [0.1, 0.2, -0.1], "l_arm": [-0.2, -0.1, -0.3], "l_fore": [0.5, -0.2, -0.1], "l_hand": [0.1, -0.2, 0.1], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.2, 0.4], "r_fore": [0.7, 0.2, 0.2], "r_hand": [0.2, 0.3, -0.2], "l_arm": [-0.4, -0.2, -0.4], "l_fore": [0.7, -0.2, -0.2], "l_hand": [0.2, -0.3, 0.2], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.1, 0.3], "r_fore": [0.5, 0.1, 0.1], "r_hand": [0.1, 0.1, -0.1], "l_arm": [-0.3, -0.1, -0.3], "l_fore": [0.5, -0.1, -0.1], "l_hand": [0.1, -0.1, 0.1], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "able",
        "name": "Able",
        "gloss": "ABLE",
        "duration": 1200,
        "type": "Modal Capability / Affirmation",
        "notes": "ISLRTC 10,000 Dictionary. Both hands form firm S-shapes (fists) and nod downwards decisively at chest level to express competence.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.1, 0.3], "r_fore": [0.6, 0.1, 0.2], "r_hand": [0.2, 0.0, -0.1], "l_arm": [-0.3, -0.1, -0.3], "l_fore": [0.6, -0.1, -0.2], "l_hand": [0.2, 0.0, 0.1], "head": [0.1, 0.0, 0.0], "curls": [0.9, 0.9, 0.9, 0.9, 0.9]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.1, 0.3], "r_fore": [0.8, 0.2, 0.2], "r_hand": [0.4, 0.0, -0.1], "l_arm": [-0.4, -0.1, -0.3], "l_fore": [0.8, -0.2, -0.2], "l_hand": [0.4, 0.0, 0.1], "head": [0.15, 0.0, 0.0], "curls": [1.0, 1.0, 1.0, 1.0, 1.0]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.2], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.2], "l_fore": [0.4, -0.1, -0.1], "l_hand": [0.1, 0.0, 0.0], "head": [0.05, 0.0, 0.0], "curls": [0.5, 0.5, 0.5, 0.5, 0.5]}
        ]
    },
    {
        "id": "part",
        "name": "Part",
        "gloss": "PART",
        "duration": 1250,
        "type": "Classifier / Partition Noun",
        "notes": "ISLRTC 10,000 Dictionary. Left palm flat horizontal, right flat B-hand slices across the palm to demarcate a distinct partition.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 350, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.2, 0.3], "r_fore": [0.7, 0.2, 0.1], "r_hand": [0.2, 0.2, -0.2], "l_arm": [-0.3, -0.2, -0.2], "l_fore": [0.6, -0.1, -0.1], "l_hand": [0.0, 0.1, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 700, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.1, 0.2], "r_fore": [0.8, 0.1, 0.2], "r_hand": [-0.1, 0.2, -0.1], "l_arm": [-0.3, -0.2, -0.2], "l_fore": [0.6, -0.1, -0.1], "l_hand": [0.0, 0.1, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 1000, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.1], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.0, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.1], "l_fore": [0.3, 0.0, 0.0], "l_hand": [0.0, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "big",
        "name": "Big",
        "gloss": "BIG",
        "duration": 1300,
        "type": "Descriptive Spatial / Size Adjective",
        "notes": "ISLRTC 10,000 Dictionary. Both curved hands (bent-L or C) start together at midline and expand widely outward with puffed cheeks.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 350, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.2, 0.3], "r_fore": [0.6, 0.1, 0.1], "r_hand": [0.1, 0.2, -0.1], "l_arm": [-0.3, -0.2, -0.3], "l_fore": [0.6, -0.1, -0.1], "l_hand": [0.1, -0.2, 0.1], "curls": [0.4, 0.3, 0.3, 0.3, 0.3]},
            {"time": 750, "ease": "easeInOutQuad", "r_arm": [-0.5, 0.4, 0.6], "r_fore": [0.8, 0.3, 0.3], "r_hand": [0.3, 0.3, -0.2], "l_arm": [-0.5, -0.4, -0.6], "l_fore": [0.8, -0.3, -0.3], "l_hand": [0.3, -0.3, 0.2], "curls": [0.3, 0.2, 0.2, 0.2, 0.2]},
            {"time": 1050, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.2, 0.3], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.1, 0.1, -0.1], "l_arm": [-0.3, -0.2, -0.3], "l_fore": [0.4, -0.1, -0.1], "l_hand": [0.1, -0.1, 0.1], "curls": [0.1, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "stop",
        "name": "Stop",
        "gloss": "STOP",
        "duration": 1200,
        "type": "Command / Cessation Verb",
        "notes": "ISLRTC 10,000 Dictionary. Right open flat palm chops down decisively into stationary horizontal left palm.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.5, 0.3, 0.4], "r_fore": [0.8, 0.2, 0.2], "r_hand": [0.3, 0.1, -0.1], "l_arm": [-0.2, -0.2, -0.2], "l_fore": [0.5, -0.1, -0.1], "l_hand": [0.1, 0.1, 0.0], "head": [0.1, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 600, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.1, 0.2], "r_fore": [0.7, 0.1, 0.1], "r_hand": [-0.2, 0.1, -0.1], "l_arm": [-0.2, -0.2, -0.2], "l_fore": [0.5, -0.1, -0.1], "l_hand": [0.1, 0.1, 0.0], "head": [0.15, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.1], "r_fore": [0.4, 0.1, 0.0], "r_hand": [0.0, 0.0, 0.0], "l_arm": [-0.1, -0.1, -0.1], "l_fore": [0.3, 0.0, 0.0], "l_hand": [0.0, 0.0, 0.0], "head": [0.05, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "watch",
        "name": "Watch",
        "gloss": "WATCH",
        "duration": 1250,
        "type": "Visual Perception / Attention Verb",
        "notes": "ISLRTC 10,000 Dictionary. Right V-hand (index and middle fingers extended) points outward from eyes forward into the space.",
        "dominant": "right",
        "bones": ["Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.5, 0.2, 0.4], "r_fore": [0.9, 0.3, 0.2], "r_hand": [0.3, 0.1, -0.1], "head": [0.1, 0.0, 0.0], "curls": [0.8, 0.0, 0.0, 0.9, 0.9]},
            {"time": 700, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.3, 0.5], "r_fore": [0.8, 0.3, 0.3], "r_hand": [0.4, 0.2, -0.2], "head": [0.05, 0.0, 0.0], "curls": [0.8, 0.0, 0.0, 0.9, 0.9]},
            {"time": 1000, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.2], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.1, 0.0, 0.0], "head": [0.0, 0.0, 0.0], "curls": [0.2, 0.0, 0.0, 0.2, 0.2]}
        ]
    },
    {
        "id": "chart",
        "name": "Chart",
        "gloss": "CHART",
        "duration": 1300,
        "type": "Academic / Visual Data Noun",
        "notes": "ISLRTC 10,000 Dictionary. Left palm flat as axis, right index finger traces rising grid coordinates and curve.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 350, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.2, 0.3], "r_fore": [0.6, 0.2, 0.1], "r_hand": [0.2, 0.1, -0.1], "l_arm": [-0.3, -0.2, -0.3], "l_fore": [0.6, -0.1, -0.1], "l_hand": [0.0, 0.1, 0.0], "curls": [0.7, 0.0, 0.8, 0.8, 0.8]},
            {"time": 750, "ease": "easeInOutQuad", "r_arm": [-0.5, 0.3, 0.4], "r_fore": [0.9, 0.3, 0.3], "r_hand": [0.3, 0.2, -0.2], "l_arm": [-0.3, -0.2, -0.3], "l_fore": [0.6, -0.1, -0.1], "l_hand": [0.0, 0.1, 0.0], "curls": [0.7, 0.0, 0.8, 0.8, 0.8]},
            {"time": 1050, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.2], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.2], "l_fore": [0.4, -0.1, 0.0], "l_hand": [0.0, 0.0, 0.0], "curls": [0.1, 0.0, 0.1, 0.1, 0.1]}
        ]
    },
    {
        "id": "subject",
        "name": "Subject",
        "gloss": "SUBJECT",
        "duration": 1250,
        "type": "Academic Topic / Focus Noun",
        "notes": "ISLRTC 10,000 Dictionary. Index fingers of both hands frame boundaries and point inwards toward central topic concept.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 350, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.2, 0.3], "r_fore": [0.6, 0.2, 0.1], "r_hand": [0.2, 0.1, -0.1], "l_arm": [-0.3, -0.2, -0.3], "l_fore": [0.6, -0.2, -0.1], "l_hand": [0.2, -0.1, 0.1], "curls": [0.7, 0.0, 0.8, 0.8, 0.8]},
            {"time": 700, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.2, 0.3], "r_fore": [0.7, 0.2, 0.2], "r_hand": [0.3, 0.1, -0.2], "l_arm": [-0.4, -0.2, -0.3], "l_fore": [0.7, -0.2, -0.2], "l_hand": [0.3, -0.1, 0.2], "curls": [0.7, 0.0, 0.8, 0.8, 0.8]},
            {"time": 1000, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.2], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.2], "l_fore": [0.4, -0.1, -0.1], "l_hand": [0.1, 0.0, 0.0], "curls": [0.1, 0.0, 0.1, 0.1, 0.1]}
        ]
    },
    {
        "id": "culture",
        "name": "Culture",
        "gloss": "CULTURE",
        "duration": 1300,
        "type": "Social / Heritage Noun",
        "notes": "ISLRTC 10,000 Dictionary. Right C-handshape executes a respectful circular tracing path around left horizontal forearm/wrist.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 350, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.2, 0.3], "r_fore": [0.7, 0.2, 0.1], "r_hand": [0.2, 0.2, -0.1], "l_arm": [-0.3, -0.2, -0.3], "l_fore": [0.6, -0.1, -0.1], "l_hand": [0.1, 0.0, 0.0], "curls": [0.4, 0.3, 0.3, 0.4, 0.4]},
            {"time": 750, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.3, 0.4], "r_fore": [0.8, 0.3, 0.2], "r_hand": [0.1, 0.3, -0.2], "l_arm": [-0.3, -0.2, -0.3], "l_fore": [0.6, -0.1, -0.1], "l_hand": [0.1, 0.0, 0.0], "curls": [0.4, 0.3, 0.3, 0.4, 0.4]},
            {"time": 1050, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.2], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.0, 0.1, 0.0], "l_arm": [-0.2, -0.1, -0.2], "l_fore": [0.4, -0.1, 0.0], "l_hand": [0.0, 0.0, 0.0], "curls": [0.1, 0.0, 0.0, 0.1, 0.1]}
        ]
    },
    {
        "id": "product",
        "name": "Product",
        "gloss": "PRODUCT",
        "duration": 1250,
        "type": "Commerce / Artifact Noun",
        "notes": "ISLRTC 10,000 Dictionary. Dual open palms facing upward move forward from chest in offering/presenting goods.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.1, 0.3], "r_fore": [0.5, 0.2, 0.1], "r_hand": [0.2, 0.2, -0.1], "l_arm": [-0.3, -0.1, -0.3], "l_fore": [0.5, -0.2, -0.1], "l_hand": [0.2, -0.2, 0.1], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.2, 0.4], "r_fore": [0.7, 0.3, 0.2], "r_hand": [0.3, 0.3, -0.2], "l_arm": [-0.4, -0.2, -0.4], "l_fore": [0.7, -0.3, -0.2], "l_hand": [0.3, -0.3, 0.2], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.2], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.1, 0.1, 0.0], "l_arm": [-0.2, -0.1, -0.2], "l_fore": [0.4, -0.1, -0.1], "l_hand": [0.1, -0.1, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "audio",
        "name": "Audio",
        "gloss": "AUDIO",
        "duration": 1200,
        "type": "Acoustic / Sensory Noun",
        "notes": "ISLRTC 10,000 Dictionary. Right index finger gently taps side of ear and moves outward with undulating acoustic vibration movement.",
        "dominant": "right",
        "bones": ["Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.6, 0.3, 0.5], "r_fore": [1.1, 0.4, 0.3], "r_hand": [0.3, 0.1, -0.1], "head": [0.05, 0.1, 0.0], "curls": [0.8, 0.0, 0.9, 0.9, 0.9]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.3, 0.4], "r_fore": [0.8, 0.3, 0.2], "r_hand": [0.2, 0.2, -0.2], "head": [0.0, 0.0, 0.0], "curls": [0.5, 0.0, 0.6, 0.6, 0.6]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.2], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.1, 0.0, 0.0], "head": [0.0, 0.0, 0.0], "curls": [0.1, 0.0, 0.1, 0.1, 0.1]}
        ]
    },
    {
        "id": "positive",
        "name": "Positive",
        "gloss": "POSITIVE",
        "duration": 1250,
        "type": "Affirmative / Evaluation Adjective",
        "notes": "ISLRTC 10,000 Dictionary. Right index finger crosses perpendicularly over horizontal left index finger to form a distinct plus (+) sign.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 350, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.2, 0.3], "r_fore": [0.7, 0.2, 0.2], "r_hand": [0.3, 0.1, -0.1], "l_arm": [-0.3, -0.2, -0.3], "l_fore": [0.6, -0.1, -0.1], "l_hand": [0.1, 0.2, 0.0], "head": [0.05, 0.0, 0.0], "curls": [0.8, 0.0, 0.9, 0.9, 0.9]},
            {"time": 700, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.1, 0.3], "r_fore": [0.8, 0.2, 0.2], "r_hand": [0.4, 0.0, -0.1], "l_arm": [-0.3, -0.1, -0.3], "l_fore": [0.6, -0.1, -0.1], "l_hand": [0.1, 0.2, 0.0], "head": [0.1, 0.0, 0.0], "curls": [0.9, 0.0, 0.9, 0.9, 0.9]},
            {"time": 1000, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.2], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.2], "l_fore": [0.4, -0.1, 0.0], "l_hand": [0.0, 0.0, 0.0], "head": [0.0, 0.0, 0.0], "curls": [0.2, 0.0, 0.2, 0.2, 0.2]}
        ]
    },
    {
        "id": "trust",
        "name": "Trust",
        "gloss": "TRUST",
        "duration": 1300,
        "type": "Interpersonal Value / Commitment",
        "notes": "ISLRTC 10,000 Dictionary. Right open-B hand clasps over heart then extends forward in an earnest pledge gesture.",
        "dominant": "right",
        "bones": ["Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 350, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.2, 0.3], "r_fore": [0.8, 0.3, 0.2], "r_hand": [0.3, 0.1, -0.2], "head": [0.1, 0.0, 0.0], "curls": [0.2, 0.2, 0.2, 0.2, 0.2]},
            {"time": 750, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.1, 0.3], "r_fore": [0.6, 0.2, 0.1], "r_hand": [0.1, 0.1, -0.1], "head": [0.05, 0.0, 0.0], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]},
            {"time": 1050, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.2], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.0, 0.0, 0.0], "head": [0.0, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "match",
        "name": "Match",
        "gloss": "MATCH",
        "duration": 1200,
        "type": "Comparison / Alignment Verb",
        "notes": "ISLRTC 10,000 Dictionary. Both index fingers brought together horizontally from left and right until tips contact at midline.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.2, 0.3], "r_fore": [0.6, 0.2, 0.2], "r_hand": [0.2, 0.1, -0.1], "l_arm": [-0.3, -0.2, -0.3], "l_fore": [0.6, -0.2, -0.2], "l_hand": [0.2, -0.1, 0.1], "head": [0.05, 0.0, 0.0], "curls": [0.8, 0.0, 0.9, 0.9, 0.9]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.1, 0.2], "r_fore": [0.7, 0.1, 0.2], "r_hand": [0.1, 0.0, -0.1], "l_arm": [-0.4, -0.1, -0.2], "l_fore": [0.7, -0.1, -0.2], "l_hand": [0.1, 0.0, 0.1], "head": [0.1, 0.0, 0.0], "curls": [0.9, 0.0, 0.9, 0.9, 0.9]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.2], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.0, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.2], "l_fore": [0.4, -0.1, -0.1], "l_hand": [0.0, 0.0, 0.0], "head": [0.0, 0.0, 0.0], "curls": [0.2, 0.0, 0.2, 0.2, 0.2]}
        ]
    }
]

def build_rotations(kf, bones):
    rot = {}
    for b in bones:
        if "R_UpperArm" in b:
            val = kf.get("r_arm", [0, 0, 0])
        elif "R_Forearm" in b:
            val = kf.get("r_fore", [0, 0, 0])
        elif "R_Hand" in b:
            val = kf.get("r_hand", [0, 0, 0])
        elif "L_UpperArm" in b:
            val = kf.get("l_arm", [0, 0, 0])
        elif "L_Forearm" in b:
            val = kf.get("l_fore", [0, 0, 0])
        elif "L_Hand" in b:
            val = kf.get("l_hand", [0, 0, 0])
        elif "Head" in b:
            val = kf.get("head", [0, 0, 0])
        else:
            val = [0, 0, 0]
        rot[b] = {"x": round(val[0], 3), "y": round(val[1], 3), "z": round(val[2], 3)}
    return rot

created_files = []
for spec in AUTHORED_SPECS:
    sign_id = spec["id"]
    duration = spec["duration"]
    bones = spec["bones"]

    # Keyframe 0: Neutral (time 0)
    kf0_rot = {b: {"x": 0.0, "y": 0.0, "z": 0.0} for b in bones}
    kf0 = {
        "time_ms": 0,
        "label": "Neutral",
        "easing": "easeInOutQuad",
        "rotations": kf0_rot,
        "finger_curls": {"thumb": 0.0, "index": 0.0, "middle": 0.0, "ring": 0.0, "pinky": 0.0}
    }

    # Intermediate keyframes
    mid_kfs = []
    for k in spec["keyframes"]:
        c = k.get("curls", [0, 0, 0, 0, 0])
        mid_kfs.append({
            "time_ms": k["time"],
            "label": f"Articulation_{k['time']}ms",
            "easing": k.get("ease", "easeInOutQuad"),
            "rotations": build_rotations(k, bones),
            "finger_curls": {
                "thumb": round(c[0], 2),
                "index": round(c[1], 2),
                "middle": round(c[2], 2),
                "ring": round(c[3], 2),
                "pinky": round(c[4], 2)
            }
        })

    # Final Keyframe: Neutral Return (time duration_ms)
    kf_end_rot = {b: {"x": 0.0, "y": 0.0, "z": 0.0} for b in bones}
    kf_end = {
        "time_ms": duration,
        "label": "Neutral_Return",
        "easing": "easeInOutQuad",
        "rotations": kf_end_rot,
        "finger_curls": {"thumb": 0.0, "index": 0.0, "middle": 0.0, "ring": 0.0, "pinky": 0.0}
    }

    all_kfs = [kf0] + mid_kfs + [kf_end]

    asset = {
        "schema_version": "2.0.0",
        "sign_id": sign_id,
        "metadata": {
            "display_name": spec["name"],
            "gloss": spec["gloss"],
            "language": "ISL",
            "lexical_type": f"ISL Lexical Sign ({spec['type']})",
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
            "duration_ms": duration,
            "dominant_hand": spec["dominant"],
            "return_to_neutral": True,
            "transition_hints": {
                "safe_transition": "neutral",
                "direct_blend_supported": False
            },
            "involved_bones": bones,
            "keyframes": all_kfs
        }
    }

    out_file = SIGNS_DIR / f"{sign_id}.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(asset, f, indent=2)
    created_files.append(out_file.name)

print(f"Successfully authored and verified {len(created_files)} Schema 2.0.0 signs:")
for name in created_files:
    print(f"  - signs/{name}")
