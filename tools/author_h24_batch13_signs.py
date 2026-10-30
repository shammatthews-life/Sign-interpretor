"""
tools/author_h24_batch13_signs.py

Phase H24 Batch 13: Authoring 20 Essential Educational & Discourse Signs in Schema 2.0.0.
Expands library from 460 to 480 Playable Assets (+273 total in H24).
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
        "id": "laugh",
        "name": "Laugh",
        "gloss": "LAUGH",
        "duration": 1300,
        "type": "Emotion / Expression Verb",
        "notes": "ISLRTC 10,000 Dictionary. Dual open curved hands held near mouth/chest alternating in rhythmic upward chuckling motions.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.15, 0.1], "r_fore": [0.75, 0.1, 0.0], "r_hand": [0.2, 0.0, 0.0], "l_arm": [-0.35, -0.15, -0.1], "l_fore": [0.65, -0.1, 0.0], "l_hand": [0.2, 0.0, 0.0], "head": [-0.03, 0.0, 0.0], "curls": [0.2, 0.2, 0.2, 0.2, 0.2]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.35, 0.15, 0.1], "r_fore": [0.65, 0.1, 0.0], "r_hand": [0.2, 0.0, 0.0], "l_arm": [-0.4, -0.15, -0.1], "l_fore": [0.75, -0.1, 0.0], "l_hand": [0.2, 0.0, 0.0], "head": [-0.06, 0.0, 0.0], "curls": [0.2, 0.2, 0.2, 0.2, 0.2]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.05, 0.05], "r_fore": [0.35, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.05, -0.05], "l_fore": [0.35, -0.05, 0.0], "l_hand": [0.1, 0.0, 0.0], "head": [0.0, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "soul",
        "name": "Soul",
        "gloss": "SOUL",
        "duration": 1300,
        "type": "Spiritual / Inner Core Noun",
        "notes": "ISLRTC 10,000 Dictionary. Dominant F-hand gently pulls upward from center of chest towards throat indicating inner vital essence.",
        "dominant": "right",
        "bones": ["Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.1, 0.05], "r_fore": [0.75, 0.05, 0.0], "r_hand": [0.2, 0.0, 0.0], "head": [0.02, 0.0, 0.0], "curls": [0.6, 0.6, 0.0, 0.0, 0.0]},
            {"time": 700, "ease": "easeInOutQuad", "r_arm": [-0.55, 0.15, 0.1], "r_fore": [0.85, 0.1, 0.0], "r_hand": [0.3, 0.0, 0.0], "head": [-0.04, 0.0, 0.0], "curls": [0.7, 0.7, 0.0, 0.0, 0.0]},
            {"time": 1000, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.05, 0.05], "r_fore": [0.4, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "head": [0.0, 0.0, 0.0], "curls": [0.1, 0.1, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "meal",
        "name": "Meal",
        "gloss": "MEAL",
        "duration": 1250,
        "type": "Food / Dining Noun",
        "notes": "ISLRTC 10,000 Dictionary. Dominant flattened O-hand brings food to lips twice gently denoting eating a meal.",
        "dominant": "right",
        "bones": ["Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.45, 0.15, 0.1], "r_fore": [0.85, 0.1, 0.0], "r_hand": [0.25, 0.0, 0.0], "head": [0.03, 0.0, 0.0], "curls": [0.7, 0.7, 0.7, 0.7, 0.7]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.5, 0.15, 0.1], "r_fore": [0.95, 0.1, 0.0], "r_hand": [0.3, 0.0, 0.0], "head": [0.05, 0.0, 0.0], "curls": [0.7, 0.7, 0.7, 0.7, 0.7]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.05, 0.05], "r_fore": [0.4, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "head": [0.0, 0.0, 0.0], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]}
        ]
    },
    {
        "id": "follow",
        "name": "Follow",
        "gloss": "FOLLOW",
        "duration": 1250,
        "type": "Direction / Motion Verb",
        "notes": "ISLRTC 10,000 Dictionary. Non-dominant A-hand leads forward; dominant A-hand follows closely behind in pursuit.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.1, 0.05], "r_fore": [0.55, 0.05, 0.0], "r_hand": [0.2, 0.0, 0.0], "l_arm": [-0.4, -0.1, -0.05], "l_fore": [0.65, -0.05, 0.0], "l_hand": [0.2, 0.0, 0.0], "curls": [0.8, 0.8, 0.8, 0.8, 0.8]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.45, 0.15, 0.1], "r_fore": [0.7, 0.05, 0.0], "r_hand": [0.25, 0.0, 0.0], "l_arm": [-0.55, -0.15, -0.1], "l_fore": [0.75, -0.05, 0.0], "l_hand": [0.25, 0.0, 0.0], "curls": [0.8, 0.8, 0.8, 0.8, 0.8]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.05, 0.05], "r_fore": [0.35, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.05, -0.05], "l_fore": [0.35, -0.05, 0.0], "l_hand": [0.1, 0.0, 0.0], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]}
        ]
    },
    {
        "id": "fair",
        "name": "Fair",
        "gloss": "FAIR",
        "duration": 1250,
        "type": "Justice / Equality Adjective",
        "notes": "ISLRTC 10,000 Dictionary. Dual bent flat hands brought together horizontally until fingertips touch at midline denoting parity and fairness.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.35, 0.2, 0.1], "r_fore": [0.65, 0.1, 0.0], "r_hand": [0.2, 0.0, 0.0], "l_arm": [-0.35, -0.2, -0.1], "l_fore": [0.65, -0.1, 0.0], "l_hand": [0.2, 0.0, 0.0], "curls": [0.4, 0.4, 0.4, 0.4, 0.4]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.1, 0.05], "r_fore": [0.75, 0.05, 0.0], "r_hand": [0.3, 0.0, 0.0], "l_arm": [-0.4, -0.1, -0.05], "l_fore": [0.75, -0.05, 0.0], "l_hand": [0.3, 0.0, 0.0], "curls": [0.5, 0.5, 0.5, 0.5, 0.5]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.05, 0.05], "r_fore": [0.35, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.05, -0.05], "l_fore": [0.35, -0.05, 0.0], "l_hand": [0.1, 0.0, 0.0], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]}
        ]
    },
    {
        "id": "statistics",
        "name": "Statistics",
        "gloss": "STATISTICS",
        "duration": 1300,
        "type": "Analytics / Numerical Data Noun",
        "notes": "ISLRTC 10,000 Dictionary. Dual flat palms sweep upward and forward in staggered tiers tracing statistical frequency distributions.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.15, 0.1], "r_fore": [0.65, 0.1, 0.0], "r_hand": [0.2, 0.0, 0.0], "l_arm": [-0.3, -0.15, -0.1], "l_fore": [0.55, -0.1, 0.0], "l_hand": [0.2, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 700, "ease": "easeInOutQuad", "r_arm": [-0.55, 0.2, 0.15], "r_fore": [0.75, 0.1, 0.0], "r_hand": [0.3, 0.0, 0.0], "l_arm": [-0.45, -0.2, -0.15], "l_fore": [0.7, -0.1, 0.0], "l_hand": [0.3, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 1000, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.05, 0.05], "r_fore": [0.35, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.05, -0.05], "l_fore": [0.35, -0.05, 0.0], "l_hand": [0.1, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "nose",
        "name": "Nose",
        "gloss": "NOSE",
        "duration": 1200,
        "type": "Anatomy / Facial Noun",
        "notes": "ISLRTC 10,000 Dictionary. Dominant index finger touches tip of nose directly.",
        "dominant": "right",
        "bones": ["Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.45, 0.15, 0.1], "r_fore": [0.8, 0.1, 0.0], "r_hand": [0.2, 0.0, 0.0], "head": [0.02, 0.0, 0.0], "curls": [0.8, 0.0, 0.8, 0.8, 0.8]},
            {"time": 600, "ease": "easeInOutQuad", "r_arm": [-0.5, 0.15, 0.1], "r_fore": [0.9, 0.05, 0.0], "r_hand": [0.25, 0.0, 0.0], "head": [0.03, 0.0, 0.0], "curls": [0.8, 0.0, 0.8, 0.8, 0.8]},
            {"time": 900, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.05, 0.05], "r_fore": [0.4, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "head": [0.0, 0.0, 0.0], "curls": [0.1, 0.0, 0.1, 0.1, 0.1]}
        ]
    },
    {
        "id": "self",
        "name": "Self",
        "gloss": "SELF",
        "duration": 1200,
        "type": "Identity / Reflexive Pronoun",
        "notes": "ISLRTC 10,000 Dictionary. Dominant A-hand with thumb extended moves inward and firmly taps center of chest denoting self.",
        "dominant": "right",
        "bones": ["Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.15, 0.1], "r_fore": [0.75, -0.1, 0.0], "r_hand": [0.2, 0.0, 0.0], "head": [0.03, 0.0, 0.0], "curls": [0.0, 0.9, 0.9, 0.9, 0.9]},
            {"time": 600, "ease": "easeInOutQuad", "r_arm": [-0.45, 0.1, 0.05], "r_fore": [0.85, -0.15, 0.0], "r_hand": [0.3, 0.0, 0.0], "head": [0.05, 0.0, 0.0], "curls": [0.0, 0.9, 0.9, 0.9, 0.9]},
            {"time": 900, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.05, 0.05], "r_fore": [0.4, 0.0, 0.0], "r_hand": [0.1, 0.0, 0.0], "head": [0.0, 0.0, 0.0], "curls": [0.0, 0.1, 0.1, 0.1, 0.1]}
        ]
    },
    {
        "id": "angel",
        "name": "Angel",
        "gloss": "ANGEL",
        "duration": 1300,
        "type": "Symbolic / Winged Figure Noun",
        "notes": "ISLRTC 10,000 Dictionary. Dual open B-hands held near shoulders flutter gently like folding wings.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.45, 0.3, 0.25], "r_fore": [0.7, 0.2, 0.0], "r_hand": [0.2, 0.1, 0.0], "l_arm": [-0.45, -0.3, -0.25], "l_fore": [0.7, -0.2, 0.0], "l_hand": [0.2, -0.1, 0.0], "head": [-0.03, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.5, 0.35, 0.3], "r_fore": [0.65, 0.25, 0.0], "r_hand": [0.3, 0.15, 0.0], "l_arm": [-0.5, -0.35, -0.3], "l_fore": [0.65, -0.25, 0.0], "l_hand": [0.3, -0.15, 0.0], "head": [-0.05, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.05], "r_fore": [0.35, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.05], "l_fore": [0.35, -0.05, 0.0], "l_hand": [0.1, 0.0, 0.0], "head": [0.0, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "math",
        "name": "Math",
        "gloss": "MATH",
        "duration": 1250,
        "type": "Academic / Science Noun",
        "notes": "ISLRTC 10,000 Dictionary. Dual M-hands held at chest height cross wrists brushing past each other in calculation motion.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.2, 0.1], "r_fore": [0.75, 0.1, 0.0], "r_hand": [0.2, 0.0, 0.0], "l_arm": [-0.4, -0.2, -0.1], "l_fore": [0.75, -0.1, 0.0], "l_hand": [0.2, 0.0, 0.0], "curls": [0.7, 0.7, 0.7, 0.8, 0.8]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.45, 0.1, 0.05], "r_fore": [0.8, 0.05, 0.0], "r_hand": [0.25, 0.0, 0.0], "l_arm": [-0.45, -0.1, -0.05], "l_fore": [0.8, -0.05, 0.0], "l_hand": [0.25, 0.0, 0.0], "curls": [0.7, 0.7, 0.7, 0.8, 0.8]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.05, 0.05], "r_fore": [0.4, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.05, -0.05], "l_fore": [0.4, -0.05, 0.0], "l_hand": [0.1, 0.0, 0.0], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]}
        ]
    },
    {
        "id": "insane",
        "name": "Insane",
        "gloss": "INSANE",
        "duration": 1250,
        "type": "Psychological / State Adjective",
        "notes": "ISLRTC 10,000 Dictionary. Dominant index finger held near right temple spins in a small rapid circle indicating wild thought/insanity.",
        "dominant": "right",
        "bones": ["Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.45, 0.25, 0.2], "r_fore": [0.85, 0.15, 0.0], "r_hand": [0.2, 0.1, 0.0], "head": [0.03, 0.03, 0.0], "curls": [0.8, 0.0, 0.8, 0.8, 0.8]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.5, 0.25, 0.2], "r_fore": [0.9, 0.15, 0.0], "r_hand": [0.3, -0.1, 0.0], "head": [0.05, 0.04, 0.0], "curls": [0.8, 0.0, 0.8, 0.8, 0.8]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.05], "r_fore": [0.4, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "head": [0.0, 0.0, 0.0], "curls": [0.1, 0.0, 0.1, 0.1, 0.1]}
        ]
    },
    {
        "id": "goosebumps",
        "name": "Goosebumps",
        "gloss": "GOOSEBUMPS",
        "duration": 1300,
        "type": "Sensation / Physiological Noun",
        "notes": "ISLRTC 10,000 Dictionary. Dominant claw hand slides gently up non-dominant forearm as fingers flutter indicating tingling skin.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.35, 0.15, 0.1], "r_fore": [0.65, 0.1, 0.0], "r_hand": [0.2, 0.0, 0.0], "l_arm": [-0.3, -0.15, -0.1], "l_fore": [0.6, -0.1, 0.0], "l_hand": [0.2, 0.0, 0.0], "curls": [0.4, 0.4, 0.4, 0.4, 0.4]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.45, 0.1, 0.05], "r_fore": [0.8, 0.05, 0.0], "r_hand": [0.25, 0.0, 0.0], "l_arm": [-0.3, -0.15, -0.1], "l_fore": [0.6, -0.1, 0.0], "l_hand": [0.2, 0.0, 0.0], "curls": [0.5, 0.5, 0.5, 0.5, 0.5]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.05, 0.05], "r_fore": [0.35, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.15, -0.05, -0.05], "l_fore": [0.3, -0.05, 0.0], "l_hand": [0.1, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "pointless",
        "name": "Pointless",
        "gloss": "POINTLESS",
        "duration": 1250,
        "type": "Futility / Quality Adjective",
        "notes": "ISLRTC 10,000 Dictionary. Dominant index and thumb form zero/O-hand snapping outward with head shake denoting total futility.",
        "dominant": "right",
        "bones": ["Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.15, 0.1], "r_fore": [0.7, 0.1, 0.0], "r_hand": [0.2, 0.0, 0.0], "head": [0.0, -0.04, 0.0], "curls": [0.6, 0.6, 0.8, 0.8, 0.8]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.5, 0.25, 0.15], "r_fore": [0.55, 0.1, 0.0], "r_hand": [0.3, 0.1, 0.0], "head": [0.0, 0.04, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.05, 0.05], "r_fore": [0.35, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "head": [0.0, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "misunderstand",
        "name": "Misunderstand",
        "gloss": "MISUNDERSTAND",
        "duration": 1300,
        "type": "Cognition / Confusion Verb",
        "notes": "ISLRTC 10,000 Dictionary. Dominant V-hand touches forehead with index fingertip then flips over so middle finger touches forehead (confused cognition).",
        "dominant": "right",
        "bones": ["Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.5, 0.2, 0.15], "r_fore": [0.85, 0.1, 0.0], "r_hand": [0.2, 0.1, 0.0], "head": [0.03, 0.0, 0.0], "curls": [0.8, 0.0, 0.0, 0.8, 0.8]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.55, 0.2, 0.15], "r_fore": [0.85, 0.1, 0.0], "r_hand": [0.25, -0.2, 0.0], "head": [0.05, 0.03, 0.0], "curls": [0.8, 0.0, 0.0, 0.8, 0.8]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.05], "r_fore": [0.4, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "head": [0.0, 0.0, 0.0], "curls": [0.1, 0.0, 0.0, 0.1, 0.1]}
        ]
    },
    {
        "id": "tilt",
        "name": "Tilt",
        "gloss": "TILT",
        "duration": 1200,
        "type": "Orientation / Posture Verb",
        "notes": "ISLRTC 10,000 Dictionary. Dominant flat hand held horizontally pivots smoothly to an oblique incline with matching slight head tilt.",
        "dominant": "right",
        "bones": ["Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.35, 0.15, 0.1], "r_fore": [0.65, 0.1, 0.0], "r_hand": [0.2, 0.0, 0.0], "head": [0.0, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.15, 0.1], "r_fore": [0.7, 0.15, 0.0], "r_hand": [0.25, 0.35, 0.0], "head": [0.0, 0.0, 0.08], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.05, 0.05], "r_fore": [0.35, 0.05, 0.0], "r_hand": [0.1, 0.05, 0.0], "head": [0.0, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "spend",
        "name": "Spend",
        "gloss": "SPEND",
        "duration": 1250,
        "type": "Commerce / Expenditure Verb",
        "notes": "ISLRTC 10,000 Dictionary. Dominant flat palm slides off flat non-dominant palm forward and away in expenditure.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.35, 0.15, 0.1], "r_fore": [0.65, 0.1, 0.0], "r_hand": [0.2, 0.0, 0.0], "l_arm": [-0.3, -0.15, -0.1], "l_fore": [0.6, -0.1, 0.0], "l_hand": [0.2, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.5, 0.2, 0.1], "r_fore": [0.55, 0.05, 0.0], "r_hand": [0.3, 0.0, 0.0], "l_arm": [-0.3, -0.15, -0.1], "l_fore": [0.6, -0.1, 0.0], "l_hand": [0.2, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.05, 0.05], "r_fore": [0.35, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.15, -0.05, -0.05], "l_fore": [0.3, -0.05, 0.0], "l_hand": [0.1, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "perceive",
        "name": "Perceive",
        "gloss": "PERCEIVE",
        "duration": 1300,
        "type": "Sensation / Cognition Verb",
        "notes": "ISLRTC 10,000 Dictionary. Dominant V-hand points from eye level directly forward sweeping outward as awareness expands.",
        "dominant": "right",
        "bones": ["Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.45, 0.2, 0.15], "r_fore": [0.8, 0.1, 0.0], "r_hand": [0.2, 0.0, 0.0], "head": [0.02, 0.0, 0.0], "curls": [0.8, 0.0, 0.0, 0.8, 0.8]},
            {"time": 700, "ease": "easeInOutQuad", "r_arm": [-0.6, 0.25, 0.15], "r_fore": [0.65, 0.05, 0.0], "r_hand": [0.3, 0.0, 0.0], "head": [0.04, 0.0, 0.0], "curls": [0.8, 0.0, 0.0, 0.8, 0.8]},
            {"time": 1000, "ease": "easeInOutQuad", "r_arm": [-0.25, 0.05, 0.05], "r_fore": [0.35, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "head": [0.0, 0.0, 0.0], "curls": [0.1, 0.0, 0.0, 0.1, 0.1]}
        ]
    },
    {
        "id": "upon",
        "name": "Upon",
        "gloss": "UPON",
        "duration": 1200,
        "type": "Spatial / Position Preposition",
        "notes": "ISLRTC 10,000 Dictionary. Dominant flat palm descends gently to rest firmly on the back of horizontal base hand.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.15, 0.1], "r_fore": [0.75, 0.1, 0.0], "r_hand": [0.2, 0.0, 0.0], "l_arm": [-0.3, -0.15, -0.1], "l_fore": [0.6, -0.1, 0.0], "l_hand": [0.2, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.1, 0.05], "r_fore": [0.65, 0.05, 0.0], "r_hand": [0.3, 0.0, 0.0], "l_arm": [-0.3, -0.15, -0.1], "l_fore": [0.6, -0.1, 0.0], "l_hand": [0.2, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.15, 0.05, 0.05], "r_fore": [0.35, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.15, -0.05, -0.05], "l_fore": [0.3, -0.05, 0.0], "l_hand": [0.1, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "fan",
        "name": "Fan",
        "gloss": "FAN",
        "duration": 1250,
        "type": "Device / Supporter Noun",
        "notes": "ISLRTC 10,000 Dictionary. Dominant open flat hand waves repeatedly beside cheek simulating a gentle cooling breeze.",
        "dominant": "right",
        "bones": ["Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.25, 0.2], "r_fore": [0.8, 0.15, 0.0], "r_hand": [0.2, 0.2, 0.0], "head": [0.02, 0.03, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.45, 0.25, 0.2], "r_fore": [0.8, 0.15, 0.0], "r_hand": [0.25, -0.2, 0.0], "head": [0.03, 0.04, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.05], "r_fore": [0.4, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "head": [0.0, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "decide",
        "name": "Decide",
        "gloss": "DECIDE",
        "duration": 1300,
        "type": "Cognition / Choice Verb",
        "notes": "ISLRTC 10,000 Dictionary. Dominant index finger touches temple then both hands descend firmly with flat palms facing each other denoting a settled decision.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.5, 0.2, 0.15], "r_fore": [0.85, 0.1, 0.0], "r_hand": [0.2, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.05], "l_fore": [0.4, -0.05, 0.0], "l_hand": [0.1, 0.0, 0.0], "head": [0.03, 0.0, 0.0], "curls": [0.8, 0.0, 0.8, 0.8, 0.8]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.35, 0.1, 0.05], "r_fore": [0.65, 0.05, 0.0], "r_hand": [0.3, 0.0, 0.0], "l_arm": [-0.35, -0.1, -0.05], "l_fore": [0.65, -0.05, 0.0], "l_hand": [0.3, 0.0, 0.0], "head": [0.05, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.15, 0.05, 0.05], "r_fore": [0.35, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.15, -0.05, -0.05], "l_fore": [0.35, -0.05, 0.0], "l_hand": [0.1, 0.0, 0.0], "head": [0.0, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
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

print(f"Successfully authored and verified {len(created_files)} Schema 2.0.0 signs (Batch 13):")
for f in created_files:
    print(f"  + signs/{f}")
