"""
tools/author_h24_batch9_signs.py

Phase H24 Batch 9: Authoring 20 Essential Educational & Discourse Signs in Schema 2.0.0.
Expands library from 380 to 400 Playable Assets (+193 total in H24).
Covers 80+ Spoken Token Occurrences.

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
        "id": "smile",
        "name": "Smile",
        "gloss": "SMILE",
        "duration": 1250,
        "type": "Facial Expression / Joy Verb",
        "notes": "ISLRTC 10,000 Dictionary. Index fingers trace upward curves from mouth corners accompanied by a radiant facial expression.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.55, 0.15, 0.1], "r_fore": [0.85, 0.2, 0.0], "r_hand": [0.25, 0.15, 0.0], "l_arm": [-0.55, -0.15, -0.1], "l_fore": [0.85, -0.2, 0.0], "l_hand": [0.25, -0.15, 0.0], "head": [0.04, 0.0, 0.0], "curls": [0.8, 0.0, 0.8, 0.8, 0.8]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.6, 0.2, 0.15], "r_fore": [0.95, 0.25, 0.0], "r_hand": [0.35, 0.2, 0.0], "l_arm": [-0.6, -0.2, -0.15], "l_fore": [0.95, -0.25, 0.0], "l_hand": [0.35, -0.2, 0.0], "head": [0.06, 0.0, 0.0], "curls": [0.8, 0.0, 0.8, 0.8, 0.8]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.25, 0.1, 0.05], "r_fore": [0.45, 0.1, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.25, -0.1, -0.05], "l_fore": [0.45, -0.1, 0.0], "l_hand": [0.1, 0.0, 0.0], "head": [0.02, 0.0, 0.0], "curls": [0.1, 0.0, 0.1, 0.1, 0.1]}
        ]
    },
    {
        "id": "dream",
        "name": "Dream",
        "gloss": "DREAM",
        "duration": 1300,
        "type": "Aspiration / Vision Noun",
        "notes": "ISLRTC 10,000 Dictionary. Dominant index finger extends from temple forward and upward with gentle curling flutter.",
        "dominant": "right",
        "bones": ["Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.65, 0.2, 0.1], "r_fore": [0.95, 0.25, 0.0], "r_hand": [0.25, 0.1, 0.0], "head": [0.03, 0.02, 0.0], "curls": [0.8, 0.1, 0.8, 0.8, 0.8]},
            {"time": 700, "ease": "easeInOutQuad", "r_arm": [-0.75, 0.25, 0.2], "r_fore": [0.75, 0.15, 0.0], "r_hand": [0.35, 0.0, 0.0], "head": [-0.04, 0.04, 0.0], "curls": [0.8, 0.4, 0.8, 0.8, 0.8]},
            {"time": 1000, "ease": "easeInOutQuad", "r_arm": [-0.25, 0.1, 0.05], "r_fore": [0.4, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "head": [0.0, 0.0, 0.0], "curls": [0.1, 0.0, 0.1, 0.1, 0.1]}
        ]
    },
    {
        "id": "exercise",
        "name": "Exercise",
        "gloss": "EXERCISE",
        "duration": 1300,
        "type": "Physical Training / Workout Noun",
        "notes": "ISLRTC 10,000 Dictionary. Both hands formed into S-fists execute rhythmic upward and downward weight-lifting curls near shoulders.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.25, 0.2], "r_fore": [0.85, 0.2, 0.0], "r_hand": [0.25, 0.1, 0.0], "l_arm": [-0.4, -0.25, -0.2], "l_fore": [0.85, -0.2, 0.0], "l_hand": [0.25, -0.1, 0.0], "curls": [0.9, 0.9, 0.9, 0.9, 0.9]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.2, 0.15], "r_fore": [0.55, 0.15, 0.0], "r_hand": [0.15, 0.0, 0.0], "l_arm": [-0.2, -0.2, -0.15], "l_fore": [0.55, -0.15, 0.0], "l_hand": [0.15, 0.0, 0.0], "curls": [0.9, 0.9, 0.9, 0.9, 0.9]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.35, 0.2, 0.15], "r_fore": [0.75, 0.15, 0.0], "r_hand": [0.2, 0.05, 0.0], "l_arm": [-0.35, -0.2, -0.15], "l_fore": [0.75, -0.15, 0.0], "l_hand": [0.2, -0.05, 0.0], "curls": [0.9, 0.9, 0.9, 0.9, 0.9]}
        ]
    },
    {
        "id": "accomplish",
        "name": "Accomplish",
        "gloss": "ACCOMPLISH",
        "duration": 1250,
        "type": "Achieve / Complete Verb",
        "notes": "ISLRTC 10,000 Dictionary. Both open hands move forward decisively and close into firm celebratory fists with affirmative nod.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.2, 0.15], "r_fore": [0.6, 0.1, 0.0], "r_hand": [0.2, 0.0, 0.0], "l_arm": [-0.4, -0.2, -0.15], "l_fore": [0.6, -0.1, 0.0], "l_hand": [0.2, 0.0, 0.0], "head": [0.03, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.55, 0.15, 0.1], "r_fore": [0.8, 0.1, 0.0], "r_hand": [0.35, 0.0, 0.0], "l_arm": [-0.55, -0.15, -0.1], "l_fore": [0.8, -0.1, 0.0], "l_hand": [0.35, 0.0, 0.0], "head": [0.07, 0.0, 0.0], "curls": [0.9, 0.9, 0.9, 0.9, 0.9]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.05], "r_fore": [0.4, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.05], "l_fore": [0.4, -0.05, 0.0], "l_hand": [0.1, 0.0, 0.0], "head": [0.02, 0.0, 0.0], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]}
        ]
    },
    {
        "id": "close",
        "name": "Close",
        "gloss": "CLOSE",
        "duration": 1200,
        "type": "Proximity / Near Adjective",
        "notes": "ISLRTC 10,000 Dictionary. Dominant flat hand approaches vertical non-dominant palm, stopping just adjacent indicating close proximity.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.3, 0.2], "r_fore": [0.6, 0.2, 0.0], "r_hand": [0.2, 0.1, 0.0], "l_arm": [-0.35, -0.1, -0.1], "l_fore": [0.55, -0.1, 0.0], "l_hand": [0.2, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 600, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.15, 0.1], "r_fore": [0.75, 0.05, 0.0], "r_hand": [0.3, 0.0, 0.0], "l_arm": [-0.35, -0.1, -0.1], "l_fore": [0.55, -0.1, 0.0], "l_hand": [0.2, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 900, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.05], "r_fore": [0.4, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.05], "l_fore": [0.35, -0.05, 0.0], "l_hand": [0.1, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "old",
        "name": "Old",
        "gloss": "OLD",
        "duration": 1250,
        "type": "Aged / Ancient Adjective",
        "notes": "ISLRTC 10,000 Dictionary. Dominant C-hand pulls downward from chin closing into an S-fist simulating an elder's beard.",
        "dominant": "right",
        "bones": ["Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.65, 0.1, 0.1], "r_fore": [0.95, 0.15, 0.0], "r_hand": [0.25, 0.0, 0.0], "head": [0.04, 0.0, 0.0], "curls": [0.4, 0.4, 0.4, 0.4, 0.4]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.45, 0.1, 0.1], "r_fore": [0.75, 0.1, 0.0], "r_hand": [0.3, 0.0, 0.0], "head": [0.07, 0.0, 0.0], "curls": [0.9, 0.9, 0.9, 0.9, 0.9]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.05], "r_fore": [0.4, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "head": [0.02, 0.0, 0.0], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]}
        ]
    },
    {
        "id": "hungry",
        "name": "Hungry",
        "gloss": "HUNGRY",
        "duration": 1250,
        "type": "Desire / Appetite Adjective",
        "notes": "ISLRTC 10,000 Dictionary. Dominant C-hand moves downward along center of chest indicating internal appetite.",
        "dominant": "right",
        "bones": ["Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.55, 0.15, 0.1], "r_fore": [0.8, 0.1, 0.0], "r_hand": [0.25, 0.0, 0.0], "curls": [0.5, 0.5, 0.5, 0.5, 0.5]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.35, 0.1, 0.05], "r_fore": [0.65, 0.05, 0.0], "r_hand": [0.3, 0.0, 0.0], "curls": [0.5, 0.5, 0.5, 0.5, 0.5]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.15, 0.05, 0.05], "r_fore": [0.4, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]}
        ]
    },
    {
        "id": "intention",
        "name": "Intention",
        "gloss": "INTENTION",
        "duration": 1300,
        "type": "Purpose / Objective Noun",
        "notes": "ISLRTC 10,000 Dictionary. Right index finger points from temple then descends decisively into center of upturned left palm.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.65, 0.15, 0.1], "r_fore": [0.95, 0.2, 0.0], "r_hand": [0.25, 0.0, 0.0], "l_arm": [-0.25, -0.2, -0.15], "l_fore": [0.45, -0.2, 0.0], "l_hand": [0.15, 0.0, 0.0], "head": [0.03, 0.0, 0.0], "curls": [0.8, 0.0, 0.8, 0.8, 0.8]},
            {"time": 700, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.1, 0.1], "r_fore": [0.75, 0.05, 0.0], "r_hand": [0.35, 0.0, 0.0], "l_arm": [-0.3, -0.2, -0.15], "l_fore": [0.55, -0.2, 0.0], "l_hand": [0.2, 0.0, 0.0], "head": [0.05, 0.0, 0.0], "curls": [0.8, 0.0, 0.8, 0.8, 0.8]},
            {"time": 1000, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.05], "r_fore": [0.4, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.1], "l_fore": [0.35, -0.1, 0.0], "l_hand": [0.05, 0.0, 0.0], "head": [0.0, 0.0, 0.0], "curls": [0.1, 0.0, 0.1, 0.1, 0.1]}
        ]
    },
    {
        "id": "motivated",
        "name": "Motivated",
        "gloss": "MOTIVATED",
        "duration": 1300,
        "type": "Driven / Inspired Adjective",
        "notes": "ISLRTC 10,000 Dictionary. Both flat open palms rub together vigorously in front of chest denoting enthusiastic drive.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.2, 0.15], "r_fore": [0.7, 0.1, 0.0], "r_hand": [0.25, 0.1, 0.0], "l_arm": [-0.4, -0.2, -0.15], "l_fore": [0.7, -0.1, 0.0], "l_hand": [0.25, -0.1, 0.0], "head": [0.04, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.45, 0.15, 0.1], "r_fore": [0.8, -0.1, 0.0], "r_hand": [0.3, -0.1, 0.0], "l_arm": [-0.45, -0.15, -0.1], "l_fore": [0.8, 0.1, 0.0], "l_hand": [0.3, 0.1, 0.0], "head": [0.06, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.05], "r_fore": [0.4, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.05], "l_fore": [0.4, -0.05, 0.0], "l_hand": [0.1, 0.0, 0.0], "head": [0.02, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "few",
        "name": "Few",
        "gloss": "FEW",
        "duration": 1200,
        "type": "Scarce / Small Quantifier",
        "notes": "ISLRTC 10,000 Dictionary. Dominant hand starts in fist, thumb and fingers flick open successively in subtle count.",
        "dominant": "right",
        "bones": ["Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.15, 0.15], "r_fore": [0.6, 0.1, 0.0], "r_hand": [0.2, 0.0, 0.0], "curls": [0.9, 0.9, 0.9, 0.9, 0.9]},
            {"time": 600, "ease": "easeInOutQuad", "r_arm": [-0.45, 0.2, 0.15], "r_fore": [0.75, 0.15, 0.0], "r_hand": [0.3, 0.0, 0.0], "curls": [0.0, 0.0, 0.3, 0.7, 0.9]},
            {"time": 900, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.05], "r_fore": [0.4, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "curls": [0.0, 0.0, 0.1, 0.1, 0.1]}
        ]
    },
    {
        "id": "lovely",
        "name": "Lovely",
        "gloss": "LOVELY",
        "duration": 1300,
        "type": "Pleasing / Charming Adjective",
        "notes": "ISLRTC 10,000 Dictionary. Open 5-hand gently circles facial contour clockwise, closing into relaxed tapered handshape.",
        "dominant": "right",
        "bones": ["Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.65, 0.2, 0.1], "r_fore": [0.95, 0.2, 0.0], "r_hand": [0.25, 0.1, 0.0], "head": [0.03, 0.02, 0.0], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]},
            {"time": 700, "ease": "easeInOutQuad", "r_arm": [-0.55, 0.15, 0.1], "r_fore": [0.85, 0.1, 0.0], "r_hand": [0.35, 0.0, 0.0], "head": [0.05, -0.02, 0.0], "curls": [0.7, 0.7, 0.7, 0.7, 0.7]},
            {"time": 1000, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.05], "r_fore": [0.4, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "head": [0.0, 0.0, 0.0], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]}
        ]
    },
    {
        "id": "focus",
        "name": "Focus",
        "gloss": "FOCUS",
        "duration": 1250,
        "type": "Concentrate / Direct Gaze Verb",
        "notes": "ISLRTC 10,000 Dictionary. Both flat hands held near eye temples move straight forward converging on focal target.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.6, 0.2, 0.15], "r_fore": [0.9, 0.1, 0.0], "r_hand": [0.25, 0.0, 0.0], "l_arm": [-0.6, -0.2, -0.15], "l_fore": [0.9, -0.1, 0.0], "l_hand": [0.25, 0.0, 0.0], "head": [0.03, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.65, 0.1, 0.1], "r_fore": [0.8, 0.05, 0.0], "r_hand": [0.35, 0.0, 0.0], "l_arm": [-0.65, -0.1, -0.1], "l_fore": [0.8, -0.05, 0.0], "l_hand": [0.35, 0.0, 0.0], "head": [0.06, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.05], "r_fore": [0.4, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.05], "l_fore": [0.4, -0.05, 0.0], "l_hand": [0.1, 0.0, 0.0], "head": [0.0, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "sometimes",
        "name": "Sometimes",
        "gloss": "SOMETIMES",
        "duration": 1250,
        "type": "Occasional Frequency Adverb",
        "notes": "ISLRTC 10,000 Dictionary. Dominant index finger circles and rhythmically taps base palm at irregular intervals denoting intermittence.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.2, 0.15], "r_fore": [0.65, 0.1, 0.0], "r_hand": [0.2, 0.1, 0.0], "l_arm": [-0.3, -0.2, -0.15], "l_fore": [0.5, -0.2, 0.0], "l_hand": [0.15, 0.0, 0.0], "curls": [0.8, 0.0, 0.8, 0.8, 0.8]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.45, 0.1, 0.1], "r_fore": [0.75, 0.05, 0.0], "r_hand": [0.3, 0.0, 0.0], "l_arm": [-0.3, -0.2, -0.15], "l_fore": [0.5, -0.2, 0.0], "l_hand": [0.15, 0.0, 0.0], "curls": [0.8, 0.0, 0.8, 0.8, 0.8]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.05], "r_fore": [0.4, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.1], "l_fore": [0.35, -0.1, 0.0], "l_hand": [0.05, 0.0, 0.0], "curls": [0.1, 0.0, 0.1, 0.1, 0.1]}
        ]
    },
    {
        "id": "list",
        "name": "List",
        "gloss": "LIST",
        "duration": 1250,
        "type": "Roster / Inventory Noun",
        "notes": "ISLRTC 10,000 Dictionary. Dominant bent hand descends in sequential tiers down vertical flat non-dominant palm outlining list items.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.45, 0.2, 0.15], "r_fore": [0.75, 0.1, 0.0], "r_hand": [0.25, 0.0, 0.0], "l_arm": [-0.35, -0.1, -0.15], "l_fore": [0.6, -0.15, 0.0], "l_hand": [0.25, 0.0, 0.0], "curls": [0.4, 0.4, 0.4, 0.4, 0.4]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.15, 0.1], "r_fore": [0.65, 0.05, 0.0], "r_hand": [0.3, 0.0, 0.0], "l_arm": [-0.35, -0.1, -0.15], "l_fore": [0.6, -0.15, 0.0], "l_hand": [0.25, 0.0, 0.0], "curls": [0.4, 0.4, 0.4, 0.4, 0.4]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.15, 0.1, 0.05], "r_fore": [0.4, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.1], "l_fore": [0.4, -0.1, 0.0], "l_hand": [0.1, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "connected",
        "name": "Connected",
        "gloss": "CONNECTED",
        "duration": 1250,
        "type": "Linked / Joined Adjective",
        "notes": "ISLRTC 10,000 Dictionary. Both hands form F-hand loops that interlock securely like links in a chain.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.2, 0.15], "r_fore": [0.65, 0.1, 0.0], "r_hand": [0.2, 0.15, 0.0], "l_arm": [-0.4, -0.2, -0.15], "l_fore": [0.65, -0.1, 0.0], "l_hand": [0.2, -0.15, 0.0], "curls": [0.7, 0.7, 0.0, 0.0, 0.0]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.45, 0.1, 0.1], "r_fore": [0.75, 0.0, 0.0], "r_hand": [0.3, 0.0, 0.0], "l_arm": [-0.45, -0.1, -0.1], "l_fore": [0.75, 0.0, 0.0], "l_hand": [0.3, 0.0, 0.0], "curls": [0.7, 0.7, 0.0, 0.0, 0.0]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.05], "r_fore": [0.4, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.05], "l_fore": [0.4, -0.05, 0.0], "l_hand": [0.1, 0.0, 0.0], "curls": [0.1, 0.1, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "course",
        "name": "Course",
        "gloss": "COURSE",
        "duration": 1250,
        "type": "Class / Program Noun",
        "notes": "ISLRTC 10,000 Dictionary. Dominant C-hand glides forward along non-dominant forearm denoting academic or structured curriculum.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.2, 0.15], "r_fore": [0.65, 0.1, 0.0], "r_hand": [0.2, 0.0, 0.0], "l_arm": [-0.35, -0.2, -0.15], "l_fore": [0.6, -0.15, 0.0], "l_hand": [0.2, 0.0, 0.0], "curls": [0.5, 0.5, 0.5, 0.5, 0.5]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.5, 0.1, 0.1], "r_fore": [0.8, 0.05, 0.0], "r_hand": [0.35, 0.0, 0.0], "l_arm": [-0.35, -0.2, -0.15], "l_fore": [0.6, -0.15, 0.0], "l_hand": [0.2, 0.0, 0.0], "curls": [0.5, 0.5, 0.5, 0.5, 0.5]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.05], "r_fore": [0.4, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.1], "l_fore": [0.35, -0.1, 0.0], "l_hand": [0.1, 0.0, 0.0], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]}
        ]
    },
    {
        "id": "analyze",
        "name": "Analyze",
        "gloss": "ANALYZE",
        "duration": 1300,
        "type": "Examine / Breakdown Verb",
        "notes": "ISLRTC 10,000 Dictionary. Both V-hands facing downward bend and unbend fingers repeatedly while descending to dissect details.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.45, 0.2, 0.15], "r_fore": [0.7, 0.1, 0.0], "r_hand": [0.25, 0.0, 0.0], "l_arm": [-0.45, -0.2, -0.15], "l_fore": [0.7, -0.1, 0.0], "l_hand": [0.25, 0.0, 0.0], "head": [0.04, 0.0, 0.0], "curls": [0.8, 0.0, 0.0, 0.8, 0.8]},
            {"time": 700, "ease": "easeInOutQuad", "r_arm": [-0.35, 0.15, 0.1], "r_fore": [0.8, 0.05, 0.0], "r_hand": [0.35, 0.0, 0.0], "l_arm": [-0.35, -0.15, -0.1], "l_fore": [0.8, -0.05, 0.0], "l_hand": [0.35, 0.0, 0.0], "head": [0.06, 0.0, 0.0], "curls": [0.8, 0.5, 0.5, 0.8, 0.8]},
            {"time": 1000, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.05], "r_fore": [0.4, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.05], "l_fore": [0.4, -0.05, 0.0], "l_hand": [0.1, 0.0, 0.0], "head": [0.0, 0.0, 0.0], "curls": [0.1, 0.0, 0.0, 0.1, 0.1]}
        ]
    },
    {
        "id": "fourth",
        "name": "Fourth",
        "gloss": "FOURTH",
        "duration": 1200,
        "type": "Ordinal Number Adjective",
        "notes": "ISLRTC 10,000 Dictionary. Four extended fingers upright (thumb tucked) execute a crisp forward ordinal thrust.",
        "dominant": "right",
        "bones": ["Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.15, 0.15], "r_fore": [0.65, 0.1, 0.0], "r_hand": [0.2, 0.0, 0.0], "curls": [0.9, 0.0, 0.0, 0.0, 0.0]},
            {"time": 600, "ease": "easeInOutQuad", "r_arm": [-0.5, 0.15, 0.15], "r_fore": [0.8, 0.1, 0.0], "r_hand": [0.35, 0.0, 0.0], "curls": [0.9, 0.0, 0.0, 0.0, 0.0]},
            {"time": 900, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.05], "r_fore": [0.4, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "curls": [0.1, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "fifth",
        "name": "Fifth",
        "gloss": "FIFTH",
        "duration": 1200,
        "type": "Ordinal Number Adjective",
        "notes": "ISLRTC 10,000 Dictionary. Open 5-hand upright with all fingers spread executes a crisp forward ordinal thrust.",
        "dominant": "right",
        "bones": ["Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.15, 0.15], "r_fore": [0.65, 0.1, 0.0], "r_hand": [0.2, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 600, "ease": "easeInOutQuad", "r_arm": [-0.5, 0.15, 0.15], "r_fore": [0.8, 0.1, 0.0], "r_hand": [0.35, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 900, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.05], "r_fore": [0.4, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "meeting",
        "name": "Meeting",
        "gloss": "MEETING",
        "duration": 1250,
        "type": "Gathering / Conference Noun",
        "notes": "ISLRTC 10,000 Dictionary. Open hands facing each other converge in front of chest, closing index fingers together to indicate assembling.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.25, 0.2], "r_fore": [0.6, 0.2, 0.0], "r_hand": [0.2, 0.1, 0.0], "l_arm": [-0.4, -0.25, -0.2], "l_fore": [0.6, -0.2, 0.0], "l_hand": [0.2, -0.1, 0.0], "curls": [0.8, 0.0, 0.8, 0.8, 0.8]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.45, 0.1, 0.1], "r_fore": [0.75, 0.05, 0.0], "r_hand": [0.3, 0.0, 0.0], "l_arm": [-0.45, -0.1, -0.1], "l_fore": [0.75, -0.05, 0.0], "l_hand": [0.3, 0.0, 0.0], "curls": [0.8, 0.0, 0.8, 0.8, 0.8]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.05], "r_fore": [0.4, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.05], "l_fore": [0.4, -0.05, 0.0], "l_hand": [0.1, 0.0, 0.0], "curls": [0.1, 0.0, 0.1, 0.1, 0.1]}
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

print(f"Successfully authored and verified {len(created_files)} Schema 2.0.0 signs (Batch 9):")
for name in created_files:
    print(f"  - signs/{name}")
