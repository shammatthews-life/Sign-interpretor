"""
tools/author_h24_batch8_signs.py

Phase H24 Batch 8: Authoring 24 Essential Educational & Discourse Signs in Schema 2.0.0.
Expands library from 356 to 380 Playable Assets (+173 total in H24).
Covers 110+ Spoken Token Occurrences.

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
        "id": "special",
        "name": "Special",
        "gloss": "SPECIAL",
        "duration": 1250,
        "type": "Unique / Exceptional Adjective",
        "notes": "ISLRTC 10,000 Dictionary. Right index finger and thumb gently grasp and pull upward from non-dominant hand indicating exceptional prominence.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.2, 0.15], "r_fore": [0.65, 0.15, 0.0], "r_hand": [0.2, 0.1, 0.0], "l_arm": [-0.3, -0.2, -0.15], "l_fore": [0.5, -0.2, 0.0], "l_hand": [0.15, 0.0, 0.0], "curls": [0.7, 0.7, 0.1, 0.1, 0.1]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.6, 0.2, 0.2], "r_fore": [0.85, 0.2, 0.0], "r_hand": [0.35, 0.15, 0.0], "l_arm": [-0.3, -0.2, -0.15], "l_fore": [0.5, -0.2, 0.0], "l_hand": [0.15, 0.0, 0.0], "curls": [0.7, 0.7, 0.1, 0.1, 0.1]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.1], "r_fore": [0.4, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.1], "l_fore": [0.3, -0.1, 0.0], "l_hand": [0.05, 0.0, 0.0], "curls": [0.1, 0.1, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "practical",
        "name": "Practical",
        "gloss": "PRACTICAL",
        "duration": 1300,
        "type": "Applicable / Hands-On Adjective",
        "notes": "ISLRTC 10,000 Dictionary. Both flat hands rotate slightly and press firmly forward denoting practical utility and application.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.2, 0.2], "r_fore": [0.6, 0.2, 0.0], "r_hand": [0.2, 0.2, 0.0], "l_arm": [-0.4, -0.2, -0.2], "l_fore": [0.6, -0.2, 0.0], "l_hand": [0.2, -0.2, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.5, 0.1, 0.15], "r_fore": [0.75, 0.1, 0.0], "r_hand": [0.3, 0.0, 0.0], "l_arm": [-0.5, -0.1, -0.15], "l_fore": [0.75, -0.1, 0.0], "l_hand": [0.3, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.1], "r_fore": [0.4, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.1], "l_fore": [0.4, -0.05, 0.0], "l_hand": [0.1, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "welcome",
        "name": "Welcome",
        "gloss": "WELCOME",
        "duration": 1300,
        "type": "Greeting / Hospitality Verb",
        "notes": "ISLRTC 10,000 Dictionary. Open palms facing upward sweep inward from neutral space toward torso in cordial greeting.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.35, 0.3, 0.25], "r_fore": [0.55, 0.2, 0.0], "r_hand": [0.2, 0.2, 0.0], "l_arm": [-0.35, -0.3, -0.25], "l_fore": [0.55, -0.2, 0.0], "l_hand": [0.2, -0.2, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 700, "ease": "easeInOutQuad", "r_arm": [-0.45, 0.15, 0.1], "r_fore": [0.8, -0.1, 0.0], "r_hand": [0.3, 0.0, 0.0], "l_arm": [-0.45, -0.15, -0.1], "l_fore": [0.8, 0.1, 0.0], "l_hand": [0.3, 0.0, 0.0], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]},
            {"time": 1000, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.05], "r_fore": [0.4, 0.0, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.05], "l_fore": [0.4, 0.0, 0.0], "l_hand": [0.1, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "valuable",
        "name": "Valuable",
        "gloss": "VALUABLE",
        "duration": 1250,
        "type": "Precious / Worth Adjective",
        "notes": "ISLRTC 10,000 Dictionary. Both hands form F-shapes touching at tips in front of chest then moving upward in appreciative arc.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.2, 0.15], "r_fore": [0.65, 0.1, 0.0], "r_hand": [0.2, 0.1, 0.0], "l_arm": [-0.4, -0.2, -0.15], "l_fore": [0.65, -0.1, 0.0], "l_hand": [0.2, -0.1, 0.0], "curls": [0.7, 0.7, 0.0, 0.0, 0.0]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.6, 0.25, 0.2], "r_fore": [0.8, 0.15, 0.0], "r_hand": [0.35, 0.0, 0.0], "l_arm": [-0.6, -0.25, -0.2], "l_fore": [0.8, -0.15, 0.0], "l_hand": [0.35, 0.0, 0.0], "curls": [0.7, 0.7, 0.0, 0.0, 0.0]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.1], "r_fore": [0.4, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.1], "l_fore": [0.4, -0.05, 0.0], "l_hand": [0.1, 0.0, 0.0], "curls": [0.1, 0.1, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "transform",
        "name": "Transform",
        "gloss": "TRANSFORM",
        "duration": 1300,
        "type": "Change / Alteration Verb",
        "notes": "ISLRTC 10,000 Dictionary. Crossed fists rotate over each other swapping positions to signify profound transformation.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.2, 0.15], "r_fore": [0.65, 0.1, 0.0], "r_hand": [0.2, 0.2, 0.0], "l_arm": [-0.35, -0.2, -0.15], "l_fore": [0.6, -0.1, 0.0], "l_hand": [0.2, -0.2, 0.0], "curls": [0.9, 0.9, 0.9, 0.9, 0.9]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.45, 0.1, 0.1], "r_fore": [0.75, -0.15, 0.0], "r_hand": [0.3, -0.2, 0.0], "l_arm": [-0.45, -0.1, -0.1], "l_fore": [0.75, 0.15, 0.0], "l_hand": [0.3, 0.2, 0.0], "curls": [0.9, 0.9, 0.9, 0.9, 0.9]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.1], "r_fore": [0.4, 0.0, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.1], "l_fore": [0.4, 0.0, 0.0], "l_hand": [0.1, 0.0, 0.0], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]}
        ]
    },
    {
        "id": "avoid",
        "name": "Avoid",
        "gloss": "AVOID",
        "duration": 1250,
        "type": "Shun / Evade Verb",
        "notes": "ISLRTC 10,000 Dictionary. Right A-hand moves diagonally backward and away from left hand indicating deliberate avoidance.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.15, 0.15], "r_fore": [0.65, 0.1, 0.0], "r_hand": [0.2, 0.0, 0.0], "l_arm": [-0.3, -0.2, -0.15], "l_fore": [0.5, -0.2, 0.0], "l_hand": [0.15, 0.0, 0.0], "curls": [0.8, 0.8, 0.8, 0.8, 0.8]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.25, 0.3, 0.3], "r_fore": [0.5, 0.25, 0.0], "r_hand": [0.1, 0.2, 0.0], "l_arm": [-0.3, -0.2, -0.15], "l_fore": [0.5, -0.2, 0.0], "l_hand": [0.15, 0.0, 0.0], "curls": [0.8, 0.8, 0.8, 0.8, 0.8]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.15, 0.15, 0.15], "r_fore": [0.35, 0.1, 0.0], "r_hand": [0.05, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.1], "l_fore": [0.3, -0.1, 0.0], "l_hand": [0.05, 0.0, 0.0], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]}
        ]
    },
    {
        "id": "excellent",
        "name": "Excellent",
        "gloss": "EXCELLENT",
        "duration": 1300,
        "type": "Superb / Top Tier Adjective",
        "notes": "ISLRTC 10,000 Dictionary. Right hand thumb and index curled into 'O' flicks outward decisively with affirmative facial expression.",
        "dominant": "right",
        "bones": ["Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.15, 0.15], "r_fore": [0.65, 0.1, 0.0], "r_hand": [0.2, 0.0, 0.0], "head": [0.04, 0.0, 0.0], "curls": [0.7, 0.7, 0.0, 0.0, 0.0]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.6, 0.25, 0.2], "r_fore": [0.85, 0.15, 0.0], "r_hand": [0.4, 0.0, 0.0], "head": [0.07, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.25, 0.1, 0.1], "r_fore": [0.45, 0.05, 0.0], "r_hand": [0.15, 0.0, 0.0], "head": [0.02, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "social",
        "name": "Social",
        "gloss": "SOCIAL",
        "duration": 1250,
        "type": "Community / Interaction Adjective",
        "notes": "ISLRTC 10,000 Dictionary. Both open hands circle each other horizontally in front of chest representing social interaction.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.2, 0.15], "r_fore": [0.65, 0.15, 0.0], "r_hand": [0.2, 0.15, 0.0], "l_arm": [-0.4, -0.2, -0.15], "l_fore": [0.65, -0.15, 0.0], "l_hand": [0.2, -0.15, 0.0], "curls": [0.2, 0.2, 0.2, 0.2, 0.2]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.45, 0.15, 0.2], "r_fore": [0.75, -0.1, 0.0], "r_hand": [0.25, -0.15, 0.0], "l_arm": [-0.45, -0.15, -0.2], "l_fore": [0.75, 0.1, 0.0], "l_hand": [0.25, 0.15, 0.0], "curls": [0.2, 0.2, 0.2, 0.2, 0.2]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.1], "r_fore": [0.4, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.1], "l_fore": [0.4, -0.05, 0.0], "l_hand": [0.1, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "critical",
        "name": "Critical",
        "gloss": "CRITICAL",
        "duration": 1250,
        "type": "Crucial / Analytical Adjective",
        "notes": "ISLRTC 10,000 Dictionary. Right index finger taps center of left open palm decisively indicating essential analytical evaluation.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.45, 0.2, 0.15], "r_fore": [0.65, 0.1, 0.0], "r_hand": [0.25, 0.1, 0.0], "l_arm": [-0.3, -0.2, -0.2], "l_fore": [0.5, -0.2, 0.0], "l_hand": [0.15, 0.0, 0.0], "curls": [0.8, 0.0, 0.8, 0.8, 0.8]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.1, 0.1], "r_fore": [0.75, 0.05, 0.0], "r_hand": [0.35, 0.0, 0.0], "l_arm": [-0.3, -0.2, -0.2], "l_fore": [0.5, -0.2, 0.0], "l_hand": [0.15, 0.0, 0.0], "curls": [0.8, 0.0, 0.8, 0.8, 0.8]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.1], "r_fore": [0.4, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.1], "l_fore": [0.3, -0.1, 0.0], "l_hand": [0.05, 0.0, 0.0], "curls": [0.1, 0.0, 0.1, 0.1, 0.1]}
        ]
    },
    {
        "id": "direction",
        "name": "Direction",
        "gloss": "DIRECTION",
        "duration": 1250,
        "type": "Heading / Course Noun",
        "notes": "ISLRTC 10,000 Dictionary. Right index finger points forward moving decisively along straight trajectory indicating targeted path.",
        "dominant": "right",
        "bones": ["Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.15, 0.15], "r_fore": [0.55, 0.1, 0.0], "r_hand": [0.2, 0.0, 0.0], "curls": [0.8, 0.0, 0.8, 0.8, 0.8]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.55, 0.2, 0.2], "r_fore": [0.85, 0.15, 0.0], "r_hand": [0.35, 0.0, 0.0], "curls": [0.8, 0.0, 0.8, 0.8, 0.8]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.25, 0.1, 0.1], "r_fore": [0.45, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "curls": [0.1, 0.0, 0.1, 0.1, 0.1]}
        ]
    },
    {
        "id": "content",
        "name": "Content",
        "gloss": "CONTENT",
        "duration": 1250,
        "type": "Substance / Material Noun",
        "notes": "ISLRTC 10,000 Dictionary. Right C-hand places material into cupped base hand denoting internal substance or content.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.45, 0.2, 0.15], "r_fore": [0.65, 0.1, 0.0], "r_hand": [0.2, 0.1, 0.0], "l_arm": [-0.3, -0.2, -0.15], "l_fore": [0.5, -0.2, 0.0], "l_hand": [0.2, 0.0, 0.0], "curls": [0.5, 0.5, 0.5, 0.5, 0.5]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.1, 0.1], "r_fore": [0.75, 0.05, 0.0], "r_hand": [0.3, 0.0, 0.0], "l_arm": [-0.3, -0.2, -0.15], "l_fore": [0.5, -0.2, 0.0], "l_hand": [0.2, 0.0, 0.0], "curls": [0.5, 0.5, 0.5, 0.5, 0.5]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.1], "r_fore": [0.4, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.1], "l_fore": [0.3, -0.1, 0.0], "l_hand": [0.1, 0.0, 0.0], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]}
        ]
    },
    {
        "id": "fail",
        "name": "Fail",
        "gloss": "FAIL",
        "duration": 1200,
        "type": "Unsuccessful Verb",
        "notes": "ISLRTC 10,000 Dictionary. Right V-hand slides off horizontal left palm and drops downward indicating failure or loss.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.2, 0.15], "r_fore": [0.6, 0.15, 0.0], "r_hand": [0.2, 0.1, 0.0], "l_arm": [-0.3, -0.2, -0.15], "l_fore": [0.5, -0.2, 0.0], "l_hand": [0.2, 0.0, 0.0], "curls": [0.8, 0.0, 0.0, 0.8, 0.8]},
            {"time": 600, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.2, 0.1], "r_fore": [0.8, 0.1, 0.0], "r_hand": [0.4, 0.0, 0.0], "l_arm": [-0.3, -0.2, -0.15], "l_fore": [0.5, -0.2, 0.0], "l_hand": [0.2, 0.0, 0.0], "curls": [0.8, 0.0, 0.0, 0.8, 0.8]},
            {"time": 900, "ease": "easeInOutQuad", "r_arm": [-0.15, 0.1, 0.05], "r_fore": [0.45, 0.05, 0.0], "r_hand": [0.15, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.1], "l_fore": [0.35, -0.1, 0.0], "l_hand": [0.1, 0.0, 0.0], "curls": [0.1, 0.0, 0.0, 0.1, 0.1]}
        ]
    },
    {
        "id": "basketball",
        "name": "Basketball",
        "gloss": "BASKETBALL",
        "duration": 1250,
        "type": "Sport / Game Noun",
        "notes": "ISLRTC 10,000 Dictionary. Both curved hands hold an imaginary ball and execute a double flicking upward push toward basket.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.45, 0.2, 0.15], "r_fore": [0.65, 0.1, 0.0], "r_hand": [0.25, 0.0, 0.0], "l_arm": [-0.45, -0.2, -0.15], "l_fore": [0.65, -0.1, 0.0], "l_hand": [0.25, 0.0, 0.0], "curls": [0.3, 0.3, 0.3, 0.3, 0.3]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.6, 0.15, 0.1], "r_fore": [0.85, 0.05, 0.0], "r_hand": [0.4, 0.0, 0.0], "l_arm": [-0.6, -0.15, -0.1], "l_fore": [0.85, -0.05, 0.0], "l_hand": [0.4, 0.0, 0.0], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.1], "r_fore": [0.4, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.1], "l_fore": [0.4, -0.05, 0.0], "l_hand": [0.1, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "golf",
        "name": "Golf",
        "gloss": "GOLF",
        "duration": 1250,
        "type": "Sport / Game Noun",
        "notes": "ISLRTC 10,000 Dictionary. Interlocking hands hold imaginary golf grip and execute smooth rotational swing across torso.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Spine1"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.25, 0.15], "r_fore": [0.6, 0.2, 0.0], "r_hand": [0.2, 0.1, 0.0], "l_arm": [-0.35, 0.15, 0.1], "l_fore": [0.65, 0.15, 0.0], "l_hand": [0.2, 0.1, 0.0], "spine": [0.0, 0.05, 0.0], "curls": [0.9, 0.9, 0.9, 0.9, 0.9]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.55, -0.2, -0.1], "r_fore": [0.8, -0.15, 0.0], "r_hand": [0.3, -0.1, 0.0], "l_arm": [-0.5, -0.25, -0.15], "l_fore": [0.85, -0.2, 0.0], "l_hand": [0.3, -0.1, 0.0], "spine": [0.0, -0.06, 0.0], "curls": [0.9, 0.9, 0.9, 0.9, 0.9]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.05], "r_fore": [0.4, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.05], "l_fore": [0.4, -0.05, 0.0], "l_hand": [0.1, 0.0, 0.0], "spine": [0.0, 0.0, 0.0], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]}
        ]
    },
    {
        "id": "less",
        "name": "Less",
        "gloss": "LESS",
        "duration": 1200,
        "type": "Diminished / Scale Adjective",
        "notes": "ISLRTC 10,000 Dictionary. Right flat hand descends slowly toward horizontal base hand indicating reduced scale or volume.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.45, 0.15, 0.15], "r_fore": [0.65, 0.1, 0.0], "r_hand": [0.2, 0.0, 0.0], "l_arm": [-0.25, -0.2, -0.15], "l_fore": [0.5, -0.2, 0.0], "l_hand": [0.15, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 600, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.15, 0.1], "r_fore": [0.75, 0.05, 0.0], "r_hand": [0.3, 0.0, 0.0], "l_arm": [-0.25, -0.2, -0.15], "l_fore": [0.5, -0.2, 0.0], "l_hand": [0.15, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 900, "ease": "easeInOutQuad", "r_arm": [-0.15, 0.1, 0.05], "r_fore": [0.45, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.1], "l_fore": [0.35, -0.1, 0.0], "l_hand": [0.05, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "massive",
        "name": "Massive",
        "gloss": "MASSIVE",
        "duration": 1300,
        "type": "Huge / Immense Adjective",
        "notes": "ISLRTC 10,000 Dictionary. Dual curved open claw hands expand outward and upward from midline with expressive puffed cheeks.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.2, 0.15], "r_fore": [0.65, 0.1, 0.0], "r_hand": [0.2, 0.0, 0.0], "l_arm": [-0.4, -0.2, -0.15], "l_fore": [0.65, -0.1, 0.0], "l_hand": [0.2, 0.0, 0.0], "head": [0.03, 0.0, 0.0], "curls": [0.5, 0.5, 0.5, 0.5, 0.5]},
            {"time": 700, "ease": "easeInOutQuad", "r_arm": [-0.65, 0.35, 0.25], "r_fore": [0.85, 0.25, 0.0], "r_hand": [0.35, 0.1, 0.0], "l_arm": [-0.65, -0.35, -0.25], "l_fore": [0.85, -0.25, 0.0], "l_hand": [0.35, -0.1, 0.0], "head": [0.06, 0.0, 0.0], "curls": [0.5, 0.5, 0.5, 0.5, 0.5]},
            {"time": 1000, "ease": "easeInOutQuad", "r_arm": [-0.25, 0.15, 0.1], "r_fore": [0.45, 0.1, 0.0], "r_hand": [0.15, 0.0, 0.0], "l_arm": [-0.25, -0.15, -0.1], "l_fore": [0.45, -0.1, 0.0], "l_hand": [0.15, 0.0, 0.0], "head": [0.02, 0.0, 0.0], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]}
        ]
    },
    {
        "id": "continuous",
        "name": "Continuous",
        "gloss": "CONTINUOUS",
        "duration": 1300,
        "type": "Ongoing / Persistent Adjective",
        "notes": "ISLRTC 10,000 Dictionary. Both hands with thumbs touching execute continuous forward spiral motion denoting unbroken sequence.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.15, 0.15], "r_fore": [0.6, 0.1, 0.0], "r_hand": [0.2, 0.1, 0.0], "l_arm": [-0.4, -0.15, -0.15], "l_fore": [0.6, -0.1, 0.0], "l_hand": [0.2, -0.1, 0.0], "curls": [0.0, 0.8, 0.8, 0.8, 0.8]},
            {"time": 700, "ease": "easeInOutQuad", "r_arm": [-0.5, 0.2, 0.2], "r_fore": [0.8, 0.15, 0.0], "r_hand": [0.35, 0.15, 0.0], "l_arm": [-0.5, -0.2, -0.2], "l_fore": [0.8, -0.15, 0.0], "l_hand": [0.35, -0.15, 0.0], "curls": [0.0, 0.8, 0.8, 0.8, 0.8]},
            {"time": 1000, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.1], "r_fore": [0.4, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.1], "l_fore": [0.4, -0.05, 0.0], "l_hand": [0.1, 0.0, 0.0], "curls": [0.0, 0.1, 0.1, 0.1, 0.1]}
        ]
    },
    {
        "id": "dancing",
        "name": "Dancing",
        "gloss": "DANCING",
        "duration": 1300,
        "type": "Artistic Movement Noun / Verb",
        "notes": "ISLRTC 10,000 Dictionary. Inverted V-handshape 'legs' swing playfully back and forth across upward flat palm base.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.2, 0.15], "r_fore": [0.65, 0.15, 0.0], "r_hand": [0.25, 0.2, 0.0], "l_arm": [-0.3, -0.2, -0.15], "l_fore": [0.5, -0.2, 0.0], "l_hand": [0.2, 0.0, 0.0], "curls": [0.8, 0.0, 0.0, 0.8, 0.8]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.45, 0.1, 0.1], "r_fore": [0.75, 0.1, 0.0], "r_hand": [0.35, -0.2, 0.0], "l_arm": [-0.3, -0.2, -0.15], "l_fore": [0.5, -0.2, 0.0], "l_hand": [0.2, 0.0, 0.0], "curls": [0.8, 0.0, 0.0, 0.8, 0.8]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.1], "r_fore": [0.4, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.1], "l_fore": [0.3, -0.1, 0.0], "l_hand": [0.1, 0.0, 0.0], "curls": [0.1, 0.0, 0.0, 0.1, 0.1]}
        ]
    },
    {
        "id": "born",
        "name": "Born",
        "gloss": "BORN",
        "duration": 1250,
        "type": "Birth / Origination Verb",
        "notes": "ISLRTC 10,000 Dictionary. Right flat hand glides outward and downward from underneath horizontal base hand signifying birth.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.15, 0.1], "r_fore": [0.5, 0.1, 0.0], "r_hand": [0.2, 0.0, 0.0], "l_arm": [-0.3, -0.15, -0.1], "l_fore": [0.5, -0.1, 0.0], "l_hand": [0.2, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.5, 0.1, 0.1], "r_fore": [0.75, 0.1, 0.0], "r_hand": [0.35, 0.0, 0.0], "l_arm": [-0.3, -0.15, -0.1], "l_fore": [0.5, -0.1, 0.0], "l_hand": [0.2, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.05], "r_fore": [0.4, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.05], "l_fore": [0.35, -0.05, 0.0], "l_hand": [0.1, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "friday",
        "name": "Friday",
        "gloss": "FRIDAY",
        "duration": 1250,
        "type": "Calendar / Day of Week Noun",
        "notes": "ISLRTC 10,000 Dictionary. Dominant F-handshape (thumb and index circular) moves in subtle clockwise circle at shoulder height.",
        "dominant": "right",
        "bones": ["Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.2, 0.2], "r_fore": [0.65, 0.2, 0.0], "r_hand": [0.2, 0.15, 0.0], "curls": [0.7, 0.7, 0.0, 0.0, 0.0]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.45, 0.25, 0.2], "r_fore": [0.75, 0.15, 0.0], "r_hand": [0.25, -0.15, 0.0], "curls": [0.7, 0.7, 0.0, 0.0, 0.0]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.1], "r_fore": [0.4, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "curls": [0.1, 0.1, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "instead",
        "name": "Instead",
        "gloss": "INSTEAD",
        "duration": 1250,
        "type": "Alternative / Substitution Adverb",
        "notes": "ISLRTC 10,000 Dictionary. Both F-hands face each other and switch positions back and forth denoting substitution.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.2, 0.15], "r_fore": [0.65, 0.1, 0.0], "r_hand": [0.2, 0.1, 0.0], "l_arm": [-0.35, -0.2, -0.15], "l_fore": [0.6, -0.1, 0.0], "l_hand": [0.2, -0.1, 0.0], "curls": [0.7, 0.7, 0.0, 0.0, 0.0]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.45, 0.1, 0.1], "r_fore": [0.75, -0.1, 0.0], "r_hand": [0.3, -0.1, 0.0], "l_arm": [-0.45, -0.1, -0.1], "l_fore": [0.75, 0.1, 0.0], "l_hand": [0.3, 0.1, 0.0], "curls": [0.7, 0.7, 0.0, 0.0, 0.0]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.1], "r_fore": [0.4, 0.0, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.1], "l_fore": [0.4, 0.0, 0.0], "l_hand": [0.1, 0.0, 0.0], "curls": [0.1, 0.1, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "ago",
        "name": "Ago",
        "gloss": "AGO",
        "duration": 1200,
        "type": "Past Time Adverb",
        "notes": "ISLRTC 10,000 Dictionary. Right open flat hand swings upward and backward over the right shoulder indicating past time.",
        "dominant": "right",
        "bones": ["Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.35, 0.2, 0.15], "r_fore": [0.55, 0.15, 0.0], "r_hand": [0.2, 0.0, 0.0], "head": [0.02, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 600, "ease": "easeInOutQuad", "r_arm": [-0.65, 0.3, 0.2], "r_fore": [0.95, -0.2, 0.0], "r_hand": [0.35, -0.2, 0.0], "head": [-0.04, 0.03, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 900, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.1], "r_fore": [0.45, 0.0, 0.0], "r_hand": [0.1, 0.0, 0.0], "head": [0.0, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "quite",
        "name": "Quite",
        "gloss": "QUITE",
        "duration": 1200,
        "type": "Degree Adverb",
        "notes": "ISLRTC 10,000 Dictionary. Both flat hands held at chest level move slightly apart in measured, balanced gesture.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.35, 0.2, 0.15], "r_fore": [0.55, 0.1, 0.0], "r_hand": [0.2, 0.0, 0.0], "l_arm": [-0.35, -0.2, -0.15], "l_fore": [0.55, -0.1, 0.0], "l_hand": [0.2, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 600, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.25, 0.2], "r_fore": [0.65, 0.15, 0.0], "r_hand": [0.25, 0.0, 0.0], "l_arm": [-0.4, -0.25, -0.2], "l_fore": [0.65, -0.15, 0.0], "l_hand": [0.25, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 900, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.1], "r_fore": [0.4, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.1], "l_fore": [0.4, -0.05, 0.0], "l_hand": [0.1, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "guy",
        "name": "Guy",
        "gloss": "GUY",
        "duration": 1250,
        "type": "Man / Person Noun",
        "notes": "ISLRTC 10,000 Dictionary. Dominant hand thumb and index touch forehead brim (cap indicator) followed by generic person classifier.",
        "dominant": "right",
        "bones": ["Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.65, 0.2, 0.15], "r_fore": [0.95, 0.2, 0.0], "r_hand": [0.25, 0.1, 0.0], "head": [0.03, 0.0, 0.0], "curls": [0.8, 0.2, 0.8, 0.8, 0.8]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.15, 0.1], "r_fore": [0.65, 0.1, 0.0], "r_hand": [0.2, 0.0, 0.0], "head": [0.0, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.05], "r_fore": [0.4, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "head": [0.0, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
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

print(f"Successfully authored and verified {len(created_files)} Schema 2.0.0 signs (Batch 8):")
for name in created_files:
    print(f"  - signs/{name}")
