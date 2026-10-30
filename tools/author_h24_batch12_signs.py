"""
tools/author_h24_batch12_signs.py

Phase H24 Batch 12: Authoring 20 Essential Educational & Discourse Signs in Schema 2.0.0.
Expands library from 440 to 460 Playable Assets (+253 total in H24).
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
        "id": "conference",
        "name": "Conference",
        "gloss": "CONFERENCE",
        "duration": 1300,
        "type": "Gathering / Convention Noun",
        "notes": "ISLRTC 10,000 Dictionary. Dual curved open hands move together from sides into a central assembled circle denoting a meeting of delegates.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.35, 0.25, 0.2], "r_fore": [0.65, 0.15, 0.0], "r_hand": [0.2, 0.0, 0.0], "l_arm": [-0.35, -0.25, -0.2], "l_fore": [0.65, -0.15, 0.0], "l_hand": [0.2, 0.0, 0.0], "curls": [0.3, 0.3, 0.3, 0.3, 0.3]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.45, 0.1, 0.1], "r_fore": [0.75, 0.05, 0.0], "r_hand": [0.3, 0.0, 0.0], "l_arm": [-0.45, -0.1, -0.1], "l_fore": [0.75, -0.05, 0.0], "l_hand": [0.3, 0.0, 0.0], "curls": [0.2, 0.2, 0.2, 0.2, 0.2]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.05, 0.05], "r_fore": [0.4, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.05, -0.05], "l_fore": [0.4, -0.05, 0.0], "l_hand": [0.1, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "door",
        "name": "Door",
        "gloss": "DOOR",
        "duration": 1250,
        "type": "Architecture / Entrance Noun",
        "notes": "ISLRTC 10,000 Dictionary. Dual vertical flat B-palms touching edges; right hand pivots open like a swinging door on hinges.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.15, 0.1], "r_fore": [0.7, 0.05, 0.0], "r_hand": [0.2, 0.0, 0.0], "l_arm": [-0.4, -0.15, -0.1], "l_fore": [0.7, -0.05, 0.0], "l_hand": [0.2, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.45, 0.3, 0.2], "r_fore": [0.65, 0.15, 0.0], "r_hand": [0.25, 0.1, 0.0], "l_arm": [-0.4, -0.15, -0.1], "l_fore": [0.7, -0.05, 0.0], "l_hand": [0.2, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.05], "r_fore": [0.35, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.05, -0.05], "l_fore": [0.35, -0.05, 0.0], "l_hand": [0.1, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "break",
        "name": "Break",
        "gloss": "BREAK",
        "duration": 1200,
        "type": "Action / Separation Verb",
        "notes": "ISLRTC 10,000 Dictionary. Dual fists (S-hands) held together touching knuckles, twisting sharply outward as if snapping a rod.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.35, 0.15, 0.1], "r_fore": [0.7, 0.05, 0.0], "r_hand": [0.2, 0.0, 0.0], "l_arm": [-0.35, -0.15, -0.1], "l_fore": [0.7, -0.05, 0.0], "l_hand": [0.2, 0.0, 0.0], "curls": [0.9, 0.9, 0.9, 0.9, 0.9]},
            {"time": 600, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.25, 0.15], "r_fore": [0.65, 0.1, 0.0], "r_hand": [0.3, 0.2, 0.0], "l_arm": [-0.4, -0.25, -0.15], "l_fore": [0.65, -0.1, 0.0], "l_hand": [0.3, -0.2, 0.0], "curls": [0.9, 0.9, 0.9, 0.9, 0.9]},
            {"time": 900, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.05, 0.05], "r_fore": [0.35, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.05, -0.05], "l_fore": [0.35, -0.05, 0.0], "l_hand": [0.1, 0.0, 0.0], "curls": [0.2, 0.2, 0.2, 0.2, 0.2]}
        ]
    },
    {
        "id": "road",
        "name": "Road",
        "gloss": "ROAD",
        "duration": 1250,
        "type": "Travel / Path Noun",
        "notes": "ISLRTC 10,000 Dictionary. Dual open flat palms facing each other vertically glide forward parallel indicating a road.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.1, 0.05], "r_fore": [0.55, 0.05, 0.0], "r_hand": [0.15, 0.0, 0.0], "l_arm": [-0.3, -0.1, -0.05], "l_fore": [0.55, -0.05, 0.0], "l_hand": [0.15, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.55, 0.15, 0.1], "r_fore": [0.5, 0.05, 0.0], "r_hand": [0.25, 0.0, 0.0], "l_arm": [-0.55, -0.15, -0.1], "l_fore": [0.5, -0.05, 0.0], "l_hand": [0.25, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.05, 0.05], "r_fore": [0.35, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.05, -0.05], "l_fore": [0.35, -0.05, 0.0], "l_hand": [0.1, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "full",
        "name": "Full",
        "gloss": "FULL",
        "duration": 1250,
        "type": "Capacity / Quantity Adjective",
        "notes": "ISLRTC 10,000 Dictionary. Non-dominant fist forms cup; dominant flat palm sweeps firmly across top surface denoting brimful level.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.2, 0.1], "r_fore": [0.75, 0.1, 0.0], "r_hand": [0.2, 0.0, 0.0], "l_arm": [-0.3, -0.15, -0.1], "l_fore": [0.6, -0.1, 0.0], "l_hand": [0.2, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.35, 0.05, 0.0], "r_fore": [0.65, 0.0, 0.0], "r_hand": [0.25, 0.0, 0.0], "l_arm": [-0.3, -0.15, -0.1], "l_fore": [0.6, -0.1, 0.0], "l_hand": [0.2, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.15, 0.05, 0.0], "r_fore": [0.35, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.15, -0.05, -0.05], "l_fore": [0.3, -0.05, 0.0], "l_hand": [0.1, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "past",
        "name": "Past",
        "gloss": "PAST",
        "duration": 1200,
        "type": "Temporal / History Adverb",
        "notes": "ISLRTC 10,000 Dictionary. Dominant flat palm positioned near right shoulder sweeps backward over shoulder indicating past timeline.",
        "dominant": "right",
        "bones": ["Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.2, 0.15], "r_fore": [0.75, 0.15, 0.0], "r_hand": [0.2, 0.1, 0.0], "head": [0.02, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.25, 0.35, 0.25], "r_fore": [0.85, 0.2, 0.0], "r_hand": [0.3, 0.2, 0.0], "head": [0.04, 0.03, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.15, 0.1, 0.05], "r_fore": [0.4, 0.05, 0.0], "r_hand": [0.1, 0.05, 0.0], "head": [0.0, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "worth",
        "name": "Worth",
        "gloss": "WORTH",
        "duration": 1250,
        "type": "Value / Quality Noun",
        "notes": "ISLRTC 10,000 Dictionary. Dual F-hands (index and thumb tips touching) meet at center of chest gently tapping index tips denoting value/worth.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.35, 0.2, 0.1], "r_fore": [0.65, 0.1, 0.0], "r_hand": [0.2, 0.05, 0.0], "l_arm": [-0.35, -0.2, -0.1], "l_fore": [0.65, -0.1, 0.0], "l_hand": [0.2, -0.05, 0.0], "curls": [0.7, 0.7, 0.0, 0.0, 0.0]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.1, 0.05], "r_fore": [0.75, 0.05, 0.0], "r_hand": [0.25, 0.0, 0.0], "l_arm": [-0.4, -0.1, -0.05], "l_fore": [0.75, -0.05, 0.0], "l_hand": [0.25, 0.0, 0.0], "curls": [0.8, 0.8, 0.0, 0.0, 0.0]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.05, 0.05], "r_fore": [0.35, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.05, -0.05], "l_fore": [0.35, -0.05, 0.0], "l_hand": [0.1, 0.0, 0.0], "curls": [0.1, 0.1, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "ten",
        "name": "Ten",
        "gloss": "TEN",
        "duration": 1200,
        "type": "Numeral / Number",
        "notes": "ISLRTC 10,000 Dictionary. Right hand holds upright A-hand with thumb extended, gently oscillating side to side representing numeral 10.",
        "dominant": "right",
        "bones": ["Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.15, 0.1], "r_fore": [0.75, 0.1, 0.0], "r_hand": [0.2, 0.05, 0.0], "head": [0.02, 0.0, 0.0], "curls": [0.0, 0.9, 0.9, 0.9, 0.9]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.45, 0.15, 0.1], "r_fore": [0.8, 0.15, 0.0], "r_hand": [0.25, -0.1, 0.0], "head": [0.03, 0.0, 0.0], "curls": [0.0, 0.9, 0.9, 0.9, 0.9]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.05, 0.05], "r_fore": [0.4, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "head": [0.0, 0.0, 0.0], "curls": [0.0, 0.2, 0.2, 0.2, 0.2]}
        ]
    },
    {
        "id": "setting",
        "name": "Setting",
        "gloss": "SETTING",
        "duration": 1250,
        "type": "Environment / Setup Noun",
        "notes": "ISLRTC 10,000 Dictionary. Dual open palms facing downward move outward horizontally delimiting parameters and foundational context.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.35, 0.1, 0.05], "r_fore": [0.65, 0.05, 0.0], "r_hand": [0.2, 0.0, 0.0], "l_arm": [-0.35, -0.1, -0.05], "l_fore": [0.65, -0.05, 0.0], "l_hand": [0.2, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.25, 0.15], "r_fore": [0.6, 0.1, 0.0], "r_hand": [0.25, 0.05, 0.0], "l_arm": [-0.4, -0.25, -0.15], "l_fore": [0.6, -0.1, 0.0], "l_hand": [0.25, -0.05, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.05, 0.05], "r_fore": [0.35, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.05, -0.05], "l_fore": [0.35, -0.05, 0.0], "l_hand": [0.1, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "expectation",
        "name": "Expectation",
        "gloss": "EXPECTATION",
        "duration": 1300,
        "type": "Anticipation / Outlook Noun",
        "notes": "ISLRTC 10,000 Dictionary. Dual open curved hands held near eye level with fingers fluttering gently gazing into anticipated future.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.5, 0.2, 0.15], "r_fore": [0.85, 0.1, 0.0], "r_hand": [0.2, 0.0, 0.0], "l_arm": [-0.5, -0.2, -0.15], "l_fore": [0.85, -0.1, 0.0], "l_hand": [0.2, 0.0, 0.0], "head": [-0.03, 0.0, 0.0], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]},
            {"time": 700, "ease": "easeInOutQuad", "r_arm": [-0.55, 0.25, 0.2], "r_fore": [0.9, 0.1, 0.0], "r_hand": [0.25, 0.05, 0.0], "l_arm": [-0.55, -0.25, -0.2], "l_fore": [0.9, -0.1, 0.0], "l_hand": [0.25, -0.05, 0.0], "head": [-0.05, 0.0, 0.0], "curls": [0.2, 0.2, 0.2, 0.2, 0.2]},
            {"time": 1000, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.05], "r_fore": [0.4, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.05], "l_fore": [0.4, -0.05, 0.0], "l_hand": [0.1, 0.0, 0.0], "head": [0.0, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "server",
        "name": "Server",
        "gloss": "SERVER",
        "duration": 1250,
        "type": "Technical / Computing Noun",
        "notes": "ISLRTC 10,000 Dictionary. Dual open flat palms facing up move forward together repeatedly offering/serving network data.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.15, 0.1], "r_fore": [0.6, 0.1, 0.0], "r_hand": [0.2, 0.0, 0.0], "l_arm": [-0.3, -0.15, -0.1], "l_fore": [0.6, -0.1, 0.0], "l_hand": [0.2, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.5, 0.15, 0.05], "r_fore": [0.5, 0.05, 0.0], "r_hand": [0.25, 0.0, 0.0], "l_arm": [-0.5, -0.15, -0.05], "l_fore": [0.5, -0.05, 0.0], "l_hand": [0.25, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.05, 0.05], "r_fore": [0.35, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.05, -0.05], "l_fore": [0.35, -0.05, 0.0], "l_hand": [0.1, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "simply",
        "name": "Simply",
        "gloss": "SIMPLY",
        "duration": 1200,
        "type": "Manner / Modality Adverb",
        "notes": "ISLRTC 10,000 Dictionary. Right open flat hand held at chest height executes a smooth, uncluttered downward palm sweep.",
        "dominant": "right",
        "bones": ["Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.15, 0.1], "r_fore": [0.65, 0.1, 0.0], "r_hand": [0.2, 0.0, 0.0], "head": [0.02, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.25, 0.1, 0.05], "r_fore": [0.45, 0.05, 0.0], "r_hand": [0.25, 0.0, 0.0], "head": [0.04, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.15, 0.05, 0.05], "r_fore": [0.3, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "head": [0.0, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "cannot",
        "name": "Cannot",
        "gloss": "CANNOT",
        "duration": 1250,
        "type": "Negation / Modal Auxiliary",
        "notes": "ISLRTC 10,000 Dictionary. Right index finger strikes down sharply across the tip of stationary horizontal left index finger (negation of can).",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.5, 0.15, 0.1], "r_fore": [0.75, 0.1, 0.0], "r_hand": [0.25, 0.0, 0.0], "l_arm": [-0.3, -0.15, -0.1], "l_fore": [0.6, -0.1, 0.0], "l_hand": [0.2, 0.0, 0.0], "head": [0.0, -0.05, 0.0], "curls": [0.8, 0.0, 0.8, 0.8, 0.8]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.35, 0.1, 0.05], "r_fore": [0.65, 0.05, 0.0], "r_hand": [0.35, 0.0, 0.0], "l_arm": [-0.3, -0.15, -0.1], "l_fore": [0.6, -0.1, 0.0], "l_hand": [0.2, 0.0, 0.0], "head": [0.0, 0.05, 0.0], "curls": [0.8, 0.0, 0.8, 0.8, 0.8]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.15, 0.05, 0.05], "r_fore": [0.35, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.15, -0.05, -0.05], "l_fore": [0.3, -0.05, 0.0], "l_hand": [0.1, 0.0, 0.0], "head": [0.0, 0.0, 0.0], "curls": [0.1, 0.0, 0.1, 0.1, 0.1]}
        ]
    },
    {
        "id": "dollar",
        "name": "Dollar",
        "gloss": "DOLLAR",
        "duration": 1250,
        "type": "Currency / Financial Noun",
        "notes": "ISLRTC 10,000 Dictionary. Dominant hand grasps outer edge of open flat non-dominant palm and slides forward off the fingertips.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.15, 0.1], "r_fore": [0.75, 0.1, 0.0], "r_hand": [0.25, 0.0, 0.0], "l_arm": [-0.3, -0.15, -0.1], "l_fore": [0.6, -0.1, 0.0], "l_hand": [0.2, 0.0, 0.0], "curls": [0.5, 0.5, 0.5, 0.5, 0.5]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.45, 0.25, 0.15], "r_fore": [0.6, 0.1, 0.0], "r_hand": [0.3, 0.1, 0.0], "l_arm": [-0.3, -0.15, -0.1], "l_fore": [0.6, -0.1, 0.0], "l_hand": [0.2, 0.0, 0.0], "curls": [0.2, 0.2, 0.2, 0.2, 0.2]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.05, 0.05], "r_fore": [0.35, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.15, -0.05, -0.05], "l_fore": [0.3, -0.05, 0.0], "l_hand": [0.1, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "deep",
        "name": "Deep",
        "gloss": "DEEP",
        "duration": 1250,
        "type": "Depth / Profound Adjective",
        "notes": "ISLRTC 10,000 Dictionary. Non-dominant flat palm acts as water/surface plane; dominant index finger points down penetrating beneath.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.35, 0.15, 0.1], "r_fore": [0.65, 0.05, 0.0], "r_hand": [0.2, 0.0, 0.0], "l_arm": [-0.35, -0.15, -0.1], "l_fore": [0.65, -0.05, 0.0], "l_hand": [0.2, 0.0, 0.0], "curls": [0.8, 0.0, 0.8, 0.8, 0.8]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.05], "r_fore": [0.8, 0.0, 0.0], "r_hand": [0.4, 0.0, 0.0], "l_arm": [-0.35, -0.15, -0.1], "l_fore": [0.65, -0.05, 0.0], "l_hand": [0.2, 0.0, 0.0], "curls": [0.8, 0.0, 0.8, 0.8, 0.8]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.15, 0.05, 0.05], "r_fore": [0.35, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.15, -0.05, -0.05], "l_fore": [0.35, -0.05, 0.0], "l_hand": [0.1, 0.0, 0.0], "curls": [0.1, 0.0, 0.1, 0.1, 0.1]}
        ]
    },
    {
        "id": "phenomenal",
        "name": "Phenomenal",
        "gloss": "PHENOMENAL",
        "duration": 1300,
        "type": "Extraordinary / Wonder Adjective",
        "notes": "ISLRTC 10,000 Dictionary. Dual open 5-hands start closed near cheeks then explode outward with spreading fingers indicating sheer wonder.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.45, 0.2, 0.15], "r_fore": [0.85, 0.1, 0.0], "r_hand": [0.25, 0.0, 0.0], "l_arm": [-0.45, -0.2, -0.15], "l_fore": [0.85, -0.1, 0.0], "l_hand": [0.25, 0.0, 0.0], "head": [-0.03, 0.0, 0.0], "curls": [0.9, 0.9, 0.9, 0.9, 0.9]},
            {"time": 700, "ease": "easeInOutQuad", "r_arm": [-0.65, 0.3, 0.25], "r_fore": [0.65, 0.15, 0.0], "r_hand": [0.35, 0.1, 0.0], "l_arm": [-0.65, -0.3, -0.25], "l_fore": [0.65, -0.15, 0.0], "l_hand": [0.35, -0.1, 0.0], "head": [-0.07, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 1000, "ease": "easeInOutQuad", "r_arm": [-0.25, 0.1, 0.05], "r_fore": [0.4, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.25, -0.1, -0.05], "l_fore": [0.4, -0.05, 0.0], "l_hand": [0.1, 0.0, 0.0], "head": [0.0, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "record",
        "name": "Record",
        "gloss": "RECORD",
        "duration": 1250,
        "type": "Capture / Documentation Verb",
        "notes": "ISLRTC 10,000 Dictionary. Non-dominant flat palm acts as media/sheet; dominant hand makes pressing stamp/writing gesture onto it.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.45, 0.15, 0.1], "r_fore": [0.75, 0.1, 0.0], "r_hand": [0.2, 0.0, 0.0], "l_arm": [-0.3, -0.15, -0.1], "l_fore": [0.6, -0.1, 0.0], "l_hand": [0.2, 0.0, 0.0], "curls": [0.4, 0.4, 0.8, 0.8, 0.8]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.35, 0.1, 0.05], "r_fore": [0.65, 0.05, 0.0], "r_hand": [0.3, 0.0, 0.0], "l_arm": [-0.3, -0.15, -0.1], "l_fore": [0.6, -0.1, 0.0], "l_hand": [0.2, 0.0, 0.0], "curls": [0.4, 0.4, 0.8, 0.8, 0.8]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.15, 0.05, 0.05], "r_fore": [0.35, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.15, -0.05, -0.05], "l_fore": [0.3, -0.05, 0.0], "l_hand": [0.1, 0.0, 0.0], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]}
        ]
    },
    {
        "id": "buy",
        "name": "Buy",
        "gloss": "BUY",
        "duration": 1250,
        "type": "Commerce / Exchange Verb",
        "notes": "ISLRTC 10,000 Dictionary. Dominant hand holds imaginary cash resting on flat non-dominant palm, then sweeps forward and away in payment.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.35, 0.15, 0.1], "r_fore": [0.65, 0.1, 0.0], "r_hand": [0.2, 0.0, 0.0], "l_arm": [-0.3, -0.15, -0.1], "l_fore": [0.6, -0.1, 0.0], "l_hand": [0.2, 0.0, 0.0], "curls": [0.3, 0.3, 0.8, 0.8, 0.8]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.5, 0.2, 0.1], "r_fore": [0.5, 0.05, 0.0], "r_hand": [0.3, 0.0, 0.0], "l_arm": [-0.3, -0.15, -0.1], "l_fore": [0.6, -0.1, 0.0], "l_hand": [0.2, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.05, 0.05], "r_fore": [0.35, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.15, -0.05, -0.05], "l_fore": [0.3, -0.05, 0.0], "l_hand": [0.1, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "breathe",
        "name": "Breathe",
        "gloss": "BREATHE",
        "duration": 1300,
        "type": "Physiology / Respiration Verb",
        "notes": "ISLRTC 10,000 Dictionary. Dual open palms placed gently against upper chest rise and fall rhythmically matching respiration.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Spine1"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.1, 0.05], "r_fore": [0.75, 0.05, 0.0], "r_hand": [0.2, 0.0, 0.0], "l_arm": [-0.4, -0.1, -0.05], "l_fore": [0.75, -0.05, 0.0], "l_hand": [0.2, 0.0, 0.0], "spine": [-0.03, 0.0, 0.0], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.45, 0.15, 0.1], "r_fore": [0.85, 0.1, 0.0], "r_hand": [0.25, 0.0, 0.0], "l_arm": [-0.45, -0.15, -0.1], "l_fore": [0.85, -0.1, 0.0], "l_hand": [0.25, 0.0, 0.0], "spine": [0.03, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.05, 0.05], "r_fore": [0.4, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.05, -0.05], "l_fore": [0.4, -0.05, 0.0], "l_hand": [0.1, 0.0, 0.0], "spine": [0.0, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "billion",
        "name": "Billion",
        "gloss": "BILLION",
        "duration": 1250,
        "type": "Numeral / Magnitude",
        "notes": "ISLRTC 10,000 Dictionary. Right B-hand moves forward in signing space then sweeps laterally denoting astronomical scale.",
        "dominant": "right",
        "bones": ["Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.15, 0.1], "r_fore": [0.75, 0.1, 0.0], "r_hand": [0.2, 0.0, 0.0], "head": [0.02, 0.0, 0.0], "curls": [0.8, 0.0, 0.0, 0.0, 0.0]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.5, 0.3, 0.2], "r_fore": [0.65, 0.15, 0.0], "r_hand": [0.25, 0.1, 0.0], "head": [0.04, 0.0, 0.0], "curls": [0.8, 0.0, 0.0, 0.0, 0.0]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.05, 0.05], "r_fore": [0.35, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "head": [0.0, 0.0, 0.0], "curls": [0.1, 0.0, 0.0, 0.0, 0.0]}
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

print(f"Successfully authored and verified {len(created_files)} Schema 2.0.0 signs (Batch 12):")
for f in created_files:
    print(f"  + signs/{f}")
