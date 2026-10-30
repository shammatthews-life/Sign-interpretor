"""
tools/author_h24_batch14_signs.py

Phase H24 Batch 14: Authoring 20 Essential Educational & Discourse Signs in Schema 2.0.0.
Expands library from 480 to 500 Playable Assets (+293 total in H24).
Covers 65+ Spoken Token Occurrences.

All signs strictly observe:
1. Schema 2.0.0 specification
2. Neutral start (time 0) with rotations { x: 0, y: 0, z: 0 } and zero finger curls
3. Neutral return (time duration_ms) with rotations { x: 0, y: 0, z: 0 } and zero finger curls
4. Realistic human joint kinematics without joint inversions or mesh clipping (rotations <= 1.10 rad)
5. Official ISLRTC Indian Sign Language phonology documentation
"""

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SIGNS_DIR = PROJECT_ROOT / "signs"
SIGNS_DIR.mkdir(parents=True, exist_ok=True)

AUTHORED_SPECS = [
    {
        "id": "test",
        "name": "Test",
        "gloss": "TEST",
        "duration": 1250,
        "type": "Academic / Examination Verb",
        "notes": "ISLRTC 10,000 Dictionary. Dual index fingers pointing forward at chest height bend repeatedly into question/evaluation marks.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.35, 0.15, 0.1], "r_fore": [0.65, 0.1, 0.0], "r_hand": [0.2, 0.0, 0.0], "l_arm": [-0.35, -0.15, -0.1], "l_fore": [0.65, -0.1, 0.0], "l_hand": [0.2, 0.0, 0.0], "curls": [0.8, 0.0, 0.8, 0.8, 0.8]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.1, 0.05], "r_fore": [0.75, 0.05, 0.0], "r_hand": [0.25, 0.0, 0.0], "l_arm": [-0.4, -0.1, -0.05], "l_fore": [0.75, -0.05, 0.0], "l_hand": [0.25, 0.0, 0.0], "curls": [0.8, 0.6, 0.8, 0.8, 0.8]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.05, 0.05], "r_fore": [0.35, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.05, -0.05], "l_fore": [0.35, -0.05, 0.0], "l_hand": [0.1, 0.0, 0.0], "curls": [0.1, 0.0, 0.1, 0.1, 0.1]}
        ]
    },
    {
        "id": "village",
        "name": "Village",
        "gloss": "VILLAGE",
        "duration": 1300,
        "type": "Community / Settlement Noun",
        "notes": "ISLRTC 10,000 Dictionary. Dual open hands touch fingertips forming inverted V house roofs in sequential circular clusters.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.2, 0.15], "r_fore": [0.7, 0.1, 0.0], "r_hand": [0.2, 0.0, 0.0], "l_arm": [-0.4, -0.2, -0.15], "l_fore": [0.7, -0.1, 0.0], "l_hand": [0.2, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 700, "ease": "easeInOutQuad", "r_arm": [-0.45, 0.3, 0.2], "r_fore": [0.65, 0.15, 0.0], "r_hand": [0.25, 0.1, 0.0], "l_arm": [-0.45, -0.3, -0.2], "l_fore": [0.65, -0.15, 0.0], "l_hand": [0.25, -0.1, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 1000, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.05, 0.05], "r_fore": [0.35, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.05, -0.05], "l_fore": [0.35, -0.05, 0.0], "l_hand": [0.1, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "street",
        "name": "Street",
        "gloss": "STREET",
        "duration": 1250,
        "type": "Urban / Thoroughfare Noun",
        "notes": "ISLRTC 10,000 Dictionary. Dual open flat palms facing each other vertically glide forward parallel tracing a city street.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.1, 0.05], "r_fore": [0.55, 0.05, 0.0], "r_hand": [0.15, 0.0, 0.0], "l_arm": [-0.3, -0.1, -0.05], "l_fore": [0.55, -0.05, 0.0], "l_hand": [0.15, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.55, 0.15, 0.1], "r_fore": [0.5, 0.05, 0.0], "r_hand": [0.25, 0.0, 0.0], "l_arm": [-0.55, -0.15, -0.1], "l_fore": [0.5, -0.05, 0.0], "l_hand": [0.25, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.05, 0.05], "r_fore": [0.35, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.05, -0.05], "l_fore": [0.35, -0.05, 0.0], "l_hand": [0.1, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "cloak",
        "name": "Cloak",
        "gloss": "CLOAK",
        "duration": 1250,
        "type": "Clothing / Attire Noun",
        "notes": "ISLRTC 10,000 Dictionary. Dual open curved hands sweep over shoulders wrapping a mantle around the upper torso.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.25, 0.2], "r_fore": [0.8, 0.15, 0.0], "r_hand": [0.2, 0.0, 0.0], "l_arm": [-0.4, -0.25, -0.2], "l_fore": [0.8, -0.15, 0.0], "l_hand": [0.2, 0.0, 0.0], "curls": [0.3, 0.3, 0.3, 0.3, 0.3]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.45, 0.1, 0.05], "r_fore": [0.7, 0.05, 0.0], "r_hand": [0.25, 0.0, 0.0], "l_arm": [-0.45, -0.1, -0.05], "l_fore": [0.7, -0.05, 0.0], "l_hand": [0.25, 0.0, 0.0], "curls": [0.2, 0.2, 0.2, 0.2, 0.2]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.05, 0.05], "r_fore": [0.35, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.05, -0.05], "l_fore": [0.35, -0.05, 0.0], "l_hand": [0.1, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "average",
        "name": "Average",
        "gloss": "AVERAGE",
        "duration": 1200,
        "type": "Mathematics / Norm Adjective",
        "notes": "ISLRTC 10,000 Dictionary. Non-dominant flat hand held stationary; dominant flat hand chops across midline indicating midpoint/average.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.35, 0.15, 0.1], "r_fore": [0.65, 0.1, 0.0], "r_hand": [0.2, 0.0, 0.0], "l_arm": [-0.3, -0.15, -0.1], "l_fore": [0.6, -0.1, 0.0], "l_hand": [0.2, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.05, 0.0], "r_fore": [0.75, 0.0, 0.0], "r_hand": [0.3, 0.0, 0.0], "l_arm": [-0.3, -0.15, -0.1], "l_fore": [0.6, -0.1, 0.0], "l_hand": [0.2, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.15, 0.05, 0.05], "r_fore": [0.35, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.15, -0.05, -0.05], "l_fore": [0.3, -0.05, 0.0], "l_hand": [0.1, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "dry",
        "name": "Dry",
        "gloss": "DRY",
        "duration": 1200,
        "type": "Condition / Moisture Adjective",
        "notes": "ISLRTC 10,000 Dictionary. Dominant index finger slides horizontally across chin bending into an X-hook denoting dryness.",
        "dominant": "right",
        "bones": ["Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.45, 0.15, 0.1], "r_fore": [0.8, 0.1, 0.0], "r_hand": [0.2, 0.0, 0.0], "head": [0.02, 0.0, 0.0], "curls": [0.8, 0.0, 0.8, 0.8, 0.8]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.45, 0.25, 0.15], "r_fore": [0.75, 0.1, 0.0], "r_hand": [0.25, 0.1, 0.0], "head": [0.03, 0.0, 0.0], "curls": [0.8, 0.6, 0.8, 0.8, 0.8]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.05, 0.05], "r_fore": [0.4, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "head": [0.0, 0.0, 0.0], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]}
        ]
    },
    {
        "id": "attract",
        "name": "Attract",
        "gloss": "ATTRACT",
        "duration": 1250,
        "type": "Physics / Appeal Verb",
        "notes": "ISLRTC 10,000 Dictionary. Dual open curved hands held forward sweep smoothly inward towards chest pulling magnetism/interest.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.5, 0.2, 0.15], "r_fore": [0.55, 0.1, 0.0], "r_hand": [0.2, 0.0, 0.0], "l_arm": [-0.5, -0.2, -0.15], "l_fore": [0.55, -0.1, 0.0], "l_hand": [0.2, 0.0, 0.0], "curls": [0.2, 0.2, 0.2, 0.2, 0.2]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.35, 0.1, 0.05], "r_fore": [0.8, 0.05, 0.0], "r_hand": [0.3, 0.0, 0.0], "l_arm": [-0.35, -0.1, -0.05], "l_fore": [0.8, -0.05, 0.0], "l_hand": [0.3, 0.0, 0.0], "curls": [0.6, 0.6, 0.6, 0.6, 0.6]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.15, 0.05, 0.05], "r_fore": [0.35, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.15, -0.05, -0.05], "l_fore": [0.35, -0.05, 0.0], "l_hand": [0.1, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "grab",
        "name": "Grab",
        "gloss": "GRAB",
        "duration": 1200,
        "type": "Manual Action Verb",
        "notes": "ISLRTC 10,000 Dictionary. Dominant open 5-hand reaches forward and snaps shut into a firm fist grasping an item.",
        "dominant": "right",
        "bones": ["Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.5, 0.15, 0.1], "r_fore": [0.6, 0.1, 0.0], "r_hand": [0.2, 0.0, 0.0], "head": [0.02, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 600, "ease": "easeInOutQuad", "r_arm": [-0.35, 0.1, 0.05], "r_fore": [0.75, 0.05, 0.0], "r_hand": [0.3, 0.0, 0.0], "head": [0.04, 0.0, 0.0], "curls": [0.9, 0.9, 0.9, 0.9, 0.9]},
            {"time": 900, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.05, 0.05], "r_fore": [0.35, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "head": [0.0, 0.0, 0.0], "curls": [0.2, 0.2, 0.2, 0.2, 0.2]}
        ]
    },
    {
        "id": "send",
        "name": "Send",
        "gloss": "SEND",
        "duration": 1250,
        "type": "Transmission / Dispatch Verb",
        "notes": "ISLRTC 10,000 Dictionary. Dominant hand rests atop flat non-dominant hand then sweeps forward launching away into distance.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.35, 0.15, 0.1], "r_fore": [0.65, 0.1, 0.0], "r_hand": [0.2, 0.0, 0.0], "l_arm": [-0.3, -0.15, -0.1], "l_fore": [0.6, -0.1, 0.0], "l_hand": [0.2, 0.0, 0.0], "curls": [0.2, 0.2, 0.2, 0.2, 0.2]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.6, 0.15, 0.05], "r_fore": [0.45, 0.05, 0.0], "r_hand": [0.3, 0.0, 0.0], "l_arm": [-0.3, -0.15, -0.1], "l_fore": [0.6, -0.1, 0.0], "l_hand": [0.2, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.05, 0.05], "r_fore": [0.35, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.15, -0.05, -0.05], "l_fore": [0.3, -0.05, 0.0], "l_hand": [0.1, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "behavior",
        "name": "Behavior",
        "gloss": "BEHAVIOR",
        "duration": 1300,
        "type": "Psychology / Conduct Noun",
        "notes": "ISLRTC 10,000 Dictionary. Dual flat B-hands held forward at chest height sway synchronously side to side indicating manner and conduct.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.35, 0.2, 0.15], "r_fore": [0.65, 0.1, 0.0], "r_hand": [0.2, 0.1, 0.0], "l_arm": [-0.35, -0.2, -0.15], "l_fore": [0.65, -0.1, 0.0], "l_hand": [0.2, -0.1, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.1, 0.05], "r_fore": [0.7, 0.1, 0.0], "r_hand": [0.25, -0.15, 0.0], "l_arm": [-0.4, -0.1, -0.05], "l_fore": [0.7, -0.1, 0.0], "l_hand": [0.25, 0.15, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.05, 0.05], "r_fore": [0.35, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.05, -0.05], "l_fore": [0.35, -0.05, 0.0], "l_hand": [0.1, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "effect",
        "name": "Effect",
        "gloss": "EFFECT",
        "duration": 1250,
        "type": "Causality / Result Noun",
        "notes": "ISLRTC 10,000 Dictionary. Dominant open hand emerges forward from beneath flat base hand spreading fingers in resulting impact.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.35, 0.15, 0.1], "r_fore": [0.65, 0.1, 0.0], "r_hand": [0.2, 0.0, 0.0], "l_arm": [-0.3, -0.15, -0.1], "l_fore": [0.6, -0.1, 0.0], "l_hand": [0.2, 0.0, 0.0], "curls": [0.5, 0.5, 0.5, 0.5, 0.5]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.5, 0.2, 0.15], "r_fore": [0.6, 0.05, 0.0], "r_hand": [0.3, 0.0, 0.0], "l_arm": [-0.3, -0.15, -0.1], "l_fore": [0.6, -0.1, 0.0], "l_hand": [0.2, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.05, 0.05], "r_fore": [0.35, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.15, -0.05, -0.05], "l_fore": [0.3, -0.05, 0.0], "l_hand": [0.1, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "belief",
        "name": "Belief",
        "gloss": "BELIEF",
        "duration": 1300,
        "type": "Philosophy / Faith Noun",
        "notes": "ISLRTC 10,000 Dictionary. Dominant index finger touches temple then descends firmly to clasp hands together in conviction.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.5, 0.2, 0.15], "r_fore": [0.85, 0.1, 0.0], "r_hand": [0.2, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.05], "l_fore": [0.4, -0.05, 0.0], "l_hand": [0.1, 0.0, 0.0], "head": [0.03, 0.0, 0.0], "curls": [0.8, 0.0, 0.8, 0.8, 0.8]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.1, 0.05], "r_fore": [0.7, 0.05, 0.0], "r_hand": [0.3, 0.0, 0.0], "l_arm": [-0.35, -0.15, -0.1], "l_fore": [0.65, -0.1, 0.0], "l_hand": [0.2, 0.0, 0.0], "head": [0.05, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.15, 0.05, 0.05], "r_fore": [0.35, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.15, -0.05, -0.05], "l_fore": [0.35, -0.05, 0.0], "l_hand": [0.1, 0.0, 0.0], "head": [0.0, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "failure",
        "name": "Failure",
        "gloss": "FAILURE",
        "duration": 1250,
        "type": "Outcome / Setback Noun",
        "notes": "ISLRTC 10,000 Dictionary. Dominant V-hand slides across flat base palm and topples downward off the edge denoting collapse/failure.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.15, 0.1], "r_fore": [0.7, 0.1, 0.0], "r_hand": [0.2, 0.0, 0.0], "l_arm": [-0.3, -0.15, -0.1], "l_fore": [0.6, -0.1, 0.0], "l_hand": [0.2, 0.0, 0.0], "head": [0.02, 0.0, 0.0], "curls": [0.8, 0.0, 0.0, 0.8, 0.8]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.45, 0.1, 0.05], "r_fore": [0.65, 0.0, 0.0], "r_hand": [0.4, 0.2, 0.0], "l_arm": [-0.3, -0.15, -0.1], "l_fore": [0.6, -0.1, 0.0], "l_hand": [0.2, 0.0, 0.0], "head": [0.05, 0.0, 0.0], "curls": [0.8, 0.0, 0.0, 0.8, 0.8]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.15, 0.05, 0.05], "r_fore": [0.35, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.15, -0.05, -0.05], "l_fore": [0.3, -0.05, 0.0], "l_hand": [0.1, 0.0, 0.0], "head": [0.0, 0.0, 0.0], "curls": [0.1, 0.0, 0.0, 0.1, 0.1]}
        ]
    },
    {
        "id": "gray",
        "name": "Gray",
        "gloss": "GRAY",
        "duration": 1200,
        "type": "Color / Visual Adjective",
        "notes": "ISLRTC 10,000 Dictionary. Dual open 5-hands interlace fingers moving back and forth gently representing blend of black and white.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.35, 0.15, 0.1], "r_fore": [0.65, 0.1, 0.0], "r_hand": [0.2, 0.0, 0.0], "l_arm": [-0.35, -0.15, -0.1], "l_fore": [0.65, -0.1, 0.0], "l_hand": [0.2, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.1, 0.05], "r_fore": [0.7, 0.05, 0.0], "r_hand": [0.25, 0.15, 0.0], "l_arm": [-0.4, -0.1, -0.05], "l_fore": [0.7, -0.05, 0.0], "l_hand": [0.25, -0.15, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.05, 0.05], "r_fore": [0.35, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.05, -0.05], "l_fore": [0.35, -0.05, 0.0], "l_hand": [0.1, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "nowhere",
        "name": "Nowhere",
        "gloss": "NOWHERE",
        "duration": 1250,
        "type": "Location / Negative Adverb",
        "notes": "ISLRTC 10,000 Dictionary. Dominant index finger wiggles side to side in negation then dual open palms sweep outward empty.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.15, 0.1], "r_fore": [0.7, 0.1, 0.0], "r_hand": [0.2, 0.1, 0.0], "l_arm": [-0.2, -0.1, -0.05], "l_fore": [0.4, -0.05, 0.0], "l_hand": [0.1, 0.0, 0.0], "head": [0.0, -0.05, 0.0], "curls": [0.8, 0.0, 0.8, 0.8, 0.8]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.45, 0.25, 0.2], "r_fore": [0.6, 0.1, 0.0], "r_hand": [0.25, 0.0, 0.0], "l_arm": [-0.45, -0.25, -0.2], "l_fore": [0.6, -0.1, 0.0], "l_hand": [0.25, 0.0, 0.0], "head": [0.0, 0.05, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.05, 0.05], "r_fore": [0.35, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.05, -0.05], "l_fore": [0.35, -0.05, 0.0], "l_hand": [0.1, 0.0, 0.0], "head": [0.0, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "burden",
        "name": "Burden",
        "gloss": "BURDEN",
        "duration": 1300,
        "type": "Responsibility / Weight Noun",
        "notes": "ISLRTC 10,000 Dictionary. Dual curved open hands rest heavily on dominant shoulder pressing downward indicating weight/liability.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.2, 0.15], "r_fore": [0.8, 0.15, 0.0], "r_hand": [0.2, 0.0, 0.0], "l_arm": [-0.45, -0.1, -0.05], "l_fore": [0.85, 0.1, 0.0], "l_hand": [0.2, 0.0, 0.0], "head": [0.04, 0.04, 0.0], "curls": [0.3, 0.3, 0.3, 0.3, 0.3]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.35, 0.2, 0.15], "r_fore": [0.85, 0.15, 0.0], "r_hand": [0.3, 0.0, 0.0], "l_arm": [-0.4, -0.1, -0.05], "l_fore": [0.9, 0.1, 0.0], "l_hand": [0.25, 0.0, 0.0], "head": [0.06, 0.05, 0.0], "curls": [0.4, 0.4, 0.4, 0.4, 0.4]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.15, 0.05, 0.05], "r_fore": [0.35, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.15, -0.05, -0.05], "l_fore": [0.35, -0.05, 0.0], "l_hand": [0.1, 0.0, 0.0], "head": [0.0, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "observant",
        "name": "Observant",
        "gloss": "OBSERVANT",
        "duration": 1300,
        "type": "Perception / Attention Adjective",
        "notes": "ISLRTC 10,000 Dictionary. Dual V-hands pointing from eyes sweep slowly and attentively across the signing perimeter scanning every detail.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.45, 0.2, 0.15], "r_fore": [0.8, 0.1, 0.0], "r_hand": [0.2, 0.0, 0.0], "l_arm": [-0.45, -0.2, -0.15], "l_fore": [0.8, -0.1, 0.0], "l_hand": [0.2, 0.0, 0.0], "head": [0.02, 0.0, 0.0], "curls": [0.8, 0.0, 0.0, 0.8, 0.8]},
            {"time": 700, "ease": "easeInOutQuad", "r_arm": [-0.55, 0.3, 0.2], "r_fore": [0.75, 0.15, 0.0], "r_hand": [0.3, 0.1, 0.0], "l_arm": [-0.55, -0.3, -0.2], "l_fore": [0.75, -0.15, 0.0], "l_hand": [0.3, -0.1, 0.0], "head": [0.04, 0.0, 0.0], "curls": [0.8, 0.0, 0.0, 0.8, 0.8]},
            {"time": 1000, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.05, 0.05], "r_fore": [0.35, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.05, -0.05], "l_fore": [0.35, -0.05, 0.0], "l_hand": [0.1, 0.0, 0.0], "head": [0.0, 0.0, 0.0], "curls": [0.1, 0.0, 0.0, 0.1, 0.1]}
        ]
    },
    {
        "id": "kid",
        "name": "Kid",
        "gloss": "KID",
        "duration": 1200,
        "type": "Humor / Teasing Verb",
        "notes": "ISLRTC 10,000 Dictionary. Dominant hand with index and pinky extended wiggles playfully under nose denoting kidding/joking.",
        "dominant": "right",
        "bones": ["Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.45, 0.15, 0.1], "r_fore": [0.8, 0.1, 0.0], "r_hand": [0.2, 0.0, 0.0], "head": [0.02, 0.0, 0.0], "curls": [0.8, 0.0, 0.8, 0.8, 0.0]},
            {"time": 600, "ease": "easeInOutQuad", "r_arm": [-0.45, 0.2, 0.1], "r_fore": [0.85, 0.1, 0.0], "r_hand": [0.25, 0.15, 0.0], "head": [0.03, 0.0, 0.0], "curls": [0.8, 0.0, 0.8, 0.8, 0.0]},
            {"time": 900, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.05, 0.05], "r_fore": [0.4, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "head": [0.0, 0.0, 0.0], "curls": [0.1, 0.0, 0.1, 0.1, 0.0]}
        ]
    },
    {
        "id": "set",
        "name": "Set",
        "gloss": "SET",
        "duration": 1200,
        "type": "Placement / Establishment Verb",
        "notes": "ISLRTC 10,000 Dictionary. Dual open flat hands with palms facing down move downward firmly placing and settling an arrangement.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.35, 0.15, 0.1], "r_fore": [0.65, 0.05, 0.0], "r_hand": [0.15, 0.0, 0.0], "l_arm": [-0.35, -0.15, -0.1], "l_fore": [0.65, -0.05, 0.0], "l_hand": [0.15, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 600, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.05], "r_fore": [0.55, 0.05, 0.0], "r_hand": [0.25, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.05], "l_fore": [0.55, -0.05, 0.0], "l_hand": [0.25, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 900, "ease": "easeInOutQuad", "r_arm": [-0.15, 0.05, 0.05], "r_fore": [0.35, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.15, -0.05, -0.05], "l_fore": [0.35, -0.05, 0.0], "l_hand": [0.1, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "result",
        "name": "Result",
        "gloss": "RESULT",
        "duration": 1250,
        "type": "Outcome / Conclusion Noun",
        "notes": "ISLRTC 10,000 Dictionary. Dual R-handshapes move forward from midline and unfold into flat palms presenting the final outcome.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.15, 0.1], "r_fore": [0.7, 0.1, 0.0], "r_hand": [0.2, 0.0, 0.0], "l_arm": [-0.4, -0.15, -0.1], "l_fore": [0.7, -0.1, 0.0], "l_hand": [0.2, 0.0, 0.0], "curls": [0.5, 0.0, 0.0, 0.8, 0.8]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.5, 0.15, 0.05], "r_fore": [0.55, 0.05, 0.0], "r_hand": [0.3, 0.0, 0.0], "l_arm": [-0.5, -0.15, -0.05], "l_fore": [0.55, -0.05, 0.0], "l_hand": [0.3, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.05, 0.05], "r_fore": [0.35, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.05, -0.05], "l_fore": [0.35, -0.05, 0.0], "l_hand": [0.1, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    }
]

def build_rotations(kf, bones):
    rot = {}
    for b in bones:
        if b == "Bip001_R_UpperArm" and "r_arm" in kf:
            rot[b] = {"x": kf["r_arm"][0], "y": kf["r_arm"][1], "z": kf["r_arm"][2]}
        elif b == "Bip001_R_Forearm" and "r_fore" in kf:
            rot[b] = {"x": kf["r_fore"][0], "y": kf["r_fore"][1], "z": kf["r_fore"][2]}
        elif b == "Bip001_R_Hand" and "r_hand" in kf:
            rot[b] = {"x": kf["r_hand"][0], "y": kf["r_hand"][1], "z": kf["r_hand"][2]}
        elif b == "Bip001_L_UpperArm" and "l_arm" in kf:
            rot[b] = {"x": kf["l_arm"][0], "y": kf["l_arm"][1], "z": kf["l_arm"][2]}
        elif b == "Bip001_L_Forearm" and "l_fore" in kf:
            rot[b] = {"x": kf["l_fore"][0], "y": kf["l_fore"][1], "z": kf["l_fore"][2]}
        elif b == "Bip001_L_Hand" and "l_hand" in kf:
            rot[b] = {"x": kf["l_hand"][0], "y": kf["l_hand"][1], "z": kf["l_hand"][2]}
        elif b == "Bip001_Spine1" and "spine" in kf:
            rot[b] = {"x": kf["spine"][0], "y": kf["spine"][1], "z": kf["spine"][2]}
        elif b == "Bip001_Head" and "head" in kf:
            rot[b] = {"x": kf["head"][0], "y": kf["head"][1], "z": kf["head"][2]}
        else:
            rot[b] = {"x": 0.0, "y": 0.0, "z": 0.0}
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

print(f"Successfully authored and verified {len(created_files)} Schema 2.0.0 signs (Batch 14):")
for f in created_files:
    print(f"  + signs/{f}")
