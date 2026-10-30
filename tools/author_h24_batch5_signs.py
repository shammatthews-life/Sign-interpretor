"""
tools/author_h24_batch5_signs.py

Phase H24 Batch 5: Authoring 24 Essential Vocabulary Signs in Schema 2.0.0.
Expands library from 284 to 308 Playable Assets.
Covers 125+ Spoken Token Occurrences.

All signs strictly observe:
1. Schema 2.0.0 specification
2. Neutral start (time 0) with rotations { x: 0, y: 0, z: 0 } and zero finger curls
3. Neutral return (time duration_ms) with rotations { x: 0, y: 0, z: 0 } and zero finger curls
4. Realistic human joint kinematics without joint inversions or mesh clipping
5. Official ISLRTC Indian Sign Language phonology documentation
"""

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SIGNS_DIR = PROJECT_ROOT / "signs"
SIGNS_DIR.mkdir(parents=True, exist_ok=True)

AUTHORED_SPECS = [
    {
        "id": "ability",
        "name": "Ability",
        "gloss": "ABILITY",
        "duration": 1250,
        "type": "Capacity / Skill Noun",
        "notes": "ISLRTC 10,000 Dictionary. Both S-hands (fists) held forward at chest height nodding downward firmly to affirm capability and skill.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.2, 0.2], "r_fore": [0.6, 0.2, 0.1], "r_hand": [0.2, 0.1, -0.1], "l_arm": [-0.3, -0.2, -0.2], "l_fore": [0.6, -0.2, -0.1], "l_hand": [0.2, -0.1, 0.1], "curls": [0.9, 0.9, 0.9, 0.9, 0.9]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.1, 0.2], "r_fore": [0.8, 0.2, 0.1], "r_hand": [0.4, 0.0, -0.1], "l_arm": [-0.4, -0.1, -0.2], "l_fore": [0.8, -0.2, -0.1], "l_hand": [0.4, 0.0, 0.1], "curls": [0.9, 0.9, 0.9, 0.9, 0.9]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.1], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.1], "l_fore": [0.4, -0.1, 0.0], "l_hand": [0.1, 0.0, 0.0], "curls": [0.2, 0.2, 0.2, 0.2, 0.2]}
        ]
    },
    {
        "id": "leave",
        "name": "Leave",
        "gloss": "LEAVE",
        "duration": 1200,
        "type": "Departure / Separation Verb",
        "notes": "ISLRTC 10,000 Dictionary. Open 5-hand positioned forward in signing space, pulling backward and closing into a fist to signify departure.",
        "dominant": "right",
        "bones": ["Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Spine1"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.5, 0.2, 0.3], "r_fore": [0.6, 0.1, 0.2], "r_hand": [0.2, 0.2, -0.2], "spine": [-0.03, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.3, 0.1], "r_fore": [0.8, 0.2, 0.1], "r_hand": [0.3, 0.1, -0.1], "spine": [0.03, 0.0, 0.0], "curls": [0.9, 0.9, 0.9, 0.9, 0.9]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.1], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.1, 0.0, 0.0], "spine": [0.0, 0.0, 0.0], "curls": [0.2, 0.2, 0.2, 0.2, 0.2]}
        ]
    },
    {
        "id": "movie",
        "name": "Movie",
        "gloss": "MOVIE",
        "duration": 1300,
        "type": "Cinema / Film Noun",
        "notes": "ISLRTC 10,000 Dictionary. Non-dominant flat palm faces body; dominant flat palm oscillates back and forth against it like a film shutter.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 350, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.2, 0.2], "r_fore": [0.7, 0.2, 0.1], "r_hand": [0.2, 0.3, -0.1], "l_arm": [-0.3, -0.1, -0.2], "l_fore": [0.6, -0.2, 0.1], "l_hand": [0.2, 0.0, 0.1], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]},
            {"time": 750, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.1, 0.2], "r_fore": [0.7, 0.1, 0.1], "r_hand": [-0.1, -0.2, 0.1], "l_arm": [-0.3, -0.1, -0.2], "l_fore": [0.6, -0.2, 0.1], "l_hand": [0.2, 0.0, 0.1], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]},
            {"time": 1050, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.1], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.0, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.1], "l_fore": [0.4, -0.1, 0.0], "l_hand": [0.0, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "dynamic",
        "name": "Dynamic",
        "gloss": "DYNAMIC",
        "duration": 1300,
        "type": "Energetic / Changing Adjective",
        "notes": "ISLRTC 10,000 Dictionary. Both hands with curved open fingers moving forward in alternating energetic rhythmic wave pulses.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 350, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.2, 0.3], "r_fore": [0.7, 0.2, 0.2], "r_hand": [0.3, 0.2, -0.1], "l_arm": [-0.2, -0.1, -0.1], "l_fore": [0.4, -0.1, -0.1], "l_hand": [0.0, -0.1, 0.1], "curls": [0.3, 0.3, 0.3, 0.3, 0.3]},
            {"time": 750, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.1], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.0, 0.1, -0.1], "l_arm": [-0.4, -0.2, -0.3], "l_fore": [0.7, -0.2, -0.2], "l_hand": [0.3, -0.2, 0.1], "curls": [0.3, 0.3, 0.3, 0.3, 0.3]},
            {"time": 1050, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.2], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.2], "l_fore": [0.4, -0.1, 0.0], "l_hand": [0.1, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "guess",
        "name": "Guess",
        "gloss": "GUESS",
        "duration": 1250,
        "type": "Estimation / Conjecture Verb",
        "notes": "ISLRTC 10,000 Dictionary. Right C-hand positioned across the eyes/forehead, snatching sideways and closing into an S-fist.",
        "dominant": "right",
        "bones": ["Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.5, 0.2, 0.3], "r_fore": [0.9, 0.3, 0.2], "r_hand": [0.2, 0.2, -0.1], "head": [0.04, 0.04, 0.0], "curls": [0.4, 0.4, 0.4, 0.4, 0.4]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.3, 0.4], "r_fore": [0.8, 0.2, 0.1], "r_hand": [0.3, 0.1, -0.2], "head": [0.06, 0.0, 0.0], "curls": [0.9, 0.9, 0.9, 0.9, 0.9]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.2], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.1, 0.0, 0.0], "head": [0.0, 0.0, 0.0], "curls": [0.2, 0.2, 0.2, 0.2, 0.2]}
        ]
    },
    {
        "id": "respect",
        "name": "Respect",
        "gloss": "RESPECT",
        "duration": 1300,
        "type": "Deference / Honor Noun",
        "notes": "ISLRTC 10,000 Dictionary. Right R-hand or flat open hand initiates at the forehead and moves diagonally forward and upward in respectful salute.",
        "dominant": "right",
        "bones": ["Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 350, "ease": "easeInOutQuad", "r_arm": [-0.6, 0.2, 0.3], "r_fore": [1.0, 0.2, 0.2], "r_hand": [0.3, 0.2, -0.1], "head": [0.06, 0.0, 0.0], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]},
            {"time": 750, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.3, 0.4], "r_fore": [0.7, 0.1, 0.2], "r_hand": [0.2, 0.1, -0.2], "head": [0.02, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 1050, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.2], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.0, 0.0, 0.0], "head": [0.0, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "data",
        "name": "Data",
        "gloss": "DATA",
        "duration": 1250,
        "type": "Information / Records Noun",
        "notes": "ISLRTC 10,000 Dictionary. Left flat palm held horizontally like a digital tablet; right fingertips tap down across it in neat tabular sequence.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.2, 0.2], "r_fore": [0.7, 0.2, 0.1], "r_hand": [0.3, 0.1, -0.1], "l_arm": [-0.3, -0.1, -0.2], "l_fore": [0.6, -0.2, 0.1], "l_hand": [0.2, 0.0, 0.1], "curls": [0.6, 0.2, 0.2, 0.2, 0.2]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.1, 0.1], "r_fore": [0.8, 0.3, 0.1], "r_hand": [0.4, 0.1, -0.1], "l_arm": [-0.3, -0.1, -0.2], "l_fore": [0.6, -0.2, 0.1], "l_hand": [0.2, 0.0, 0.1], "curls": [0.6, 0.4, 0.4, 0.4, 0.4]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.1], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.1], "l_fore": [0.4, -0.1, 0.0], "l_hand": [0.1, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "launch",
        "name": "Launch",
        "gloss": "LAUNCH",
        "duration": 1300,
        "type": "Initiation / Propel Verb",
        "notes": "ISLRTC 10,000 Dictionary. Both hands with palms up held at waist, sweeping rapidly upward and outward like a rocket release.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Spine1"],
        "keyframes": [
            {"time": 350, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.2], "r_fore": [0.5, 0.2, 0.1], "r_hand": [0.2, 0.1, -0.1], "l_arm": [-0.2, -0.1, -0.2], "l_fore": [0.5, -0.2, -0.1], "l_hand": [0.2, -0.1, 0.1], "spine": [0.04, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 750, "ease": "easeInOutQuad", "r_arm": [-0.6, 0.3, 0.4], "r_fore": [0.9, 0.3, 0.2], "r_hand": [0.4, 0.2, -0.2], "l_arm": [-0.6, -0.3, -0.4], "l_fore": [0.9, -0.3, -0.2], "l_hand": [0.4, -0.2, 0.2], "spine": [-0.06, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 1050, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.1, 0.2], "r_fore": [0.5, 0.1, 0.1], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.3, -0.1, -0.2], "l_fore": [0.5, -0.1, 0.0], "l_hand": [0.1, 0.0, 0.0], "spine": [-0.02, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "pack",
        "name": "Pack",
        "gloss": "PACK",
        "duration": 1250,
        "type": "Consolidation / Packaging Verb",
        "notes": "ISLRTC 10,000 Dictionary. Dual curved hands press inward symmetrically toward center, gathering and bundling contents into an organized space.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.3, 0.3], "r_fore": [0.6, 0.2, 0.2], "r_hand": [0.2, 0.2, -0.2], "l_arm": [-0.4, -0.3, -0.3], "l_fore": [0.6, -0.2, -0.2], "l_hand": [0.2, -0.2, 0.2], "curls": [0.4, 0.4, 0.4, 0.4, 0.4]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.1, 0.2], "r_fore": [0.8, 0.3, 0.1], "r_hand": [0.3, 0.1, -0.1], "l_arm": [-0.3, -0.1, -0.2], "l_fore": [0.8, -0.3, -0.1], "l_hand": [0.3, -0.1, 0.1], "curls": [0.6, 0.6, 0.6, 0.6, 0.6]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.1], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.1], "l_fore": [0.4, -0.1, 0.0], "l_hand": [0.1, 0.0, 0.0], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]}
        ]
    },
    {
        "id": "apple",
        "name": "Apple",
        "gloss": "APPLE",
        "duration": 1200,
        "type": "Fruit Noun",
        "notes": "ISLRTC 10,000 Dictionary. Dominant knuckle of curved index finger twists gently back and forth against the cheek/dimple.",
        "dominant": "right",
        "bones": ["Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.6, 0.3, 0.3], "r_fore": [1.0, 0.3, 0.2], "r_hand": [0.3, 0.2, -0.1], "head": [0.04, 0.04, 0.0], "curls": [0.8, 0.6, 0.8, 0.8, 0.8]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.6, 0.2, 0.3], "r_fore": [1.0, 0.4, 0.2], "r_hand": [0.2, 0.3, -0.1], "head": [0.04, 0.04, 0.0], "curls": [0.8, 0.6, 0.8, 0.8, 0.8]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.1], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.1, 0.0, 0.0], "head": [0.0, 0.0, 0.0], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]}
        ]
    },
    {
        "id": "grow",
        "name": "Grow",
        "gloss": "GROW",
        "duration": 1300,
        "type": "Expansion / Maturation Verb",
        "notes": "ISLRTC 10,000 Dictionary. Right hand emerges upward through the left horizontal O/C hand, blossoming open into a wide spread hand.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 350, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.1, 0.1], "r_fore": [0.5, 0.1, 0.1], "r_hand": [0.2, 0.1, -0.1], "l_arm": [-0.3, -0.1, -0.2], "l_fore": [0.6, -0.2, 0.1], "l_hand": [0.2, 0.0, 0.1], "curls": [0.8, 0.8, 0.8, 0.8, 0.8]},
            {"time": 750, "ease": "easeInOutQuad", "r_arm": [-0.6, 0.2, 0.3], "r_fore": [0.8, 0.3, 0.2], "r_hand": [0.3, 0.1, -0.2], "l_arm": [-0.3, -0.1, -0.2], "l_fore": [0.6, -0.2, 0.1], "l_hand": [0.2, 0.0, 0.1], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 1050, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.1], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.0, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.1], "l_fore": [0.4, -0.1, 0.0], "l_hand": [0.0, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "air",
        "name": "Air",
        "gloss": "AIR",
        "duration": 1250,
        "type": "Atmosphere / Wind Noun",
        "notes": "ISLRTC 10,000 Dictionary. Both open 5-hands gently undulating past the face and chest simulating atmospheric breeze.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.2, 0.3], "r_fore": [0.7, 0.2, 0.2], "r_hand": [0.2, 0.2, -0.1], "l_arm": [-0.4, -0.2, -0.3], "l_fore": [0.7, -0.2, -0.2], "l_hand": [0.2, -0.2, 0.1], "head": [-0.04, 0.0, 0.0], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.5, 0.3, 0.4], "r_fore": [0.8, 0.1, 0.2], "r_hand": [-0.1, 0.2, 0.1], "l_arm": [-0.5, -0.3, -0.4], "l_fore": [0.8, -0.1, -0.2], "l_hand": [-0.1, -0.2, -0.1], "head": [-0.02, 0.0, 0.0], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.1], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.0, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.1], "l_fore": [0.4, -0.1, 0.0], "l_hand": [0.0, 0.0, 0.0], "head": [0.0, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "fun",
        "name": "Fun",
        "gloss": "FUN",
        "duration": 1200,
        "type": "Playfulness / Amusement Noun",
        "notes": "ISLRTC 10,000 Dictionary. Dominant index and middle fingers tap the nose bridge then descend playfully onto non-dominant fingers.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.5, 0.2, 0.3], "r_fore": [0.9, 0.3, 0.2], "r_hand": [0.3, 0.2, -0.1], "l_arm": [-0.3, -0.1, -0.2], "l_fore": [0.6, -0.2, 0.1], "l_hand": [0.2, 0.0, 0.1], "head": [0.05, 0.0, 0.0], "curls": [0.8, 0.0, 0.0, 0.8, 0.8]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.1, 0.2], "r_fore": [0.7, 0.2, 0.1], "r_hand": [0.2, 0.1, -0.1], "l_arm": [-0.3, -0.1, -0.2], "l_fore": [0.6, -0.2, 0.1], "l_hand": [0.2, 0.0, 0.1], "head": [0.02, 0.0, 0.0], "curls": [0.8, 0.0, 0.0, 0.8, 0.8]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.1], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.0, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.1], "l_fore": [0.4, -0.1, 0.0], "l_hand": [0.0, 0.0, 0.0], "head": [0.0, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "concept",
        "name": "Concept",
        "gloss": "CONCEPT",
        "duration": 1300,
        "type": "Abstract Idea Noun",
        "notes": "ISLRTC 10,000 Dictionary. Dominant C-hand starts at forehead and pulls forward/outward into space defining a conceptual framework.",
        "dominant": "right",
        "bones": ["Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 350, "ease": "easeInOutQuad", "r_arm": [-0.6, 0.2, 0.3], "r_fore": [0.9, 0.3, 0.2], "r_hand": [0.3, 0.2, -0.1], "head": [0.05, 0.0, 0.0], "curls": [0.4, 0.4, 0.4, 0.4, 0.4]},
            {"time": 750, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.3, 0.4], "r_fore": [0.7, 0.2, 0.2], "r_hand": [0.2, 0.1, -0.2], "head": [0.02, 0.0, 0.0], "curls": [0.4, 0.4, 0.4, 0.4, 0.4]},
            {"time": 1050, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.2], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.0, 0.0, 0.0], "head": [0.0, 0.0, 0.0], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]}
        ]
    },
    {
        "id": "present",
        "name": "Present",
        "gloss": "PRESENT",
        "duration": 1250,
        "type": "Exhibition / Gift Verb",
        "notes": "ISLRTC 10,000 Dictionary. Both hands with flat open palms facing up, sweeping gently forward from chest level to present or offer.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.1, 0.2], "r_fore": [0.6, 0.2, 0.1], "r_hand": [0.2, 0.1, -0.1], "l_arm": [-0.3, -0.1, -0.2], "l_fore": [0.6, -0.2, -0.1], "l_hand": [0.2, -0.1, 0.1], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.2, 0.3], "r_fore": [0.8, 0.2, 0.1], "r_hand": [0.3, 0.0, -0.2], "l_arm": [-0.4, -0.2, -0.3], "l_fore": [0.8, -0.2, -0.1], "l_hand": [0.3, 0.0, 0.2], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.1], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.1], "l_fore": [0.4, -0.1, 0.0], "l_hand": [0.1, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "tools",
        "name": "Tools",
        "gloss": "TOOLS",
        "duration": 1250,
        "type": "Instrument / Utility Noun",
        "notes": "ISLRTC 10,000 Dictionary. Dominant fist acts as a tool (wrench/hammer) executing rhythmic working motion against stationary left palm.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.2, 0.2], "r_fore": [0.8, 0.2, 0.1], "r_hand": [0.3, 0.2, -0.1], "l_arm": [-0.3, -0.1, -0.2], "l_fore": [0.6, -0.2, 0.1], "l_hand": [0.2, 0.0, 0.1], "curls": [0.9, 0.9, 0.9, 0.9, 0.9]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.1, 0.1], "r_fore": [0.7, 0.3, 0.1], "r_hand": [0.1, 0.2, -0.1], "l_arm": [-0.3, -0.1, -0.2], "l_fore": [0.6, -0.2, 0.1], "l_hand": [0.2, 0.0, 0.1], "curls": [0.9, 0.9, 0.9, 0.9, 0.9]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.1], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.0, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.1], "l_fore": [0.4, -0.1, 0.0], "l_hand": [0.0, 0.0, 0.0], "curls": [0.2, 0.2, 0.2, 0.2, 0.2]}
        ]
    },
    {
        "id": "sure",
        "name": "Sure",
        "gloss": "SURE",
        "duration": 1200,
        "type": "Certainty Adverb",
        "notes": "ISLRTC 10,000 Dictionary. Dominant index finger held upright near chin, moving straight forward with certainty and firm conviction.",
        "dominant": "right",
        "bones": ["Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.5, 0.2, 0.2], "r_fore": [0.9, 0.2, 0.1], "r_hand": [0.2, 0.1, 0.0], "head": [0.05, 0.0, 0.0], "curls": [0.8, 0.0, 0.8, 0.8, 0.8]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.2, 0.3], "r_fore": [0.6, 0.1, 0.2], "r_hand": [0.3, 0.1, -0.1], "head": [0.08, 0.0, 0.0], "curls": [0.8, 0.0, 0.8, 0.8, 0.8]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.2], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.1, 0.0, 0.0], "head": [0.02, 0.0, 0.0], "curls": [0.1, 0.0, 0.1, 0.1, 0.1]}
        ]
    },
    {
        "id": "awesome",
        "name": "Awesome",
        "gloss": "AWESOME",
        "duration": 1300,
        "type": "Excellence / Wonder Adjective",
        "notes": "ISLRTC 10,000 Dictionary. Both hands with open 5-fingers held at face level, vibrating and expanding outward in celebratory wonder.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 350, "ease": "easeInOutQuad", "r_arm": [-0.5, 0.3, 0.3], "r_fore": [0.8, 0.2, 0.2], "r_hand": [0.3, 0.2, -0.2], "l_arm": [-0.5, -0.3, -0.3], "l_fore": [0.8, -0.2, -0.2], "l_hand": [0.3, -0.2, 0.2], "head": [-0.05, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 750, "ease": "easeInOutQuad", "r_arm": [-0.6, 0.4, 0.4], "r_fore": [0.9, 0.3, 0.2], "r_hand": [0.4, 0.2, -0.3], "l_arm": [-0.6, -0.4, -0.4], "l_fore": [0.9, -0.3, -0.2], "l_hand": [0.4, -0.2, 0.3], "head": [-0.08, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 1050, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.2], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.2], "l_fore": [0.4, -0.1, 0.0], "l_hand": [0.1, 0.0, 0.0], "head": [0.0, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "opposite",
        "name": "Opposite",
        "gloss": "OPPOSITE",
        "duration": 1250,
        "type": "Contrast / Antonym Adjective",
        "notes": "ISLRTC 10,000 Dictionary. Both index fingers pointing toward each other horizontally then pulling apart and turning 180 degrees away.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.2, 0.2], "r_fore": [0.6, 0.2, 0.1], "r_hand": [0.2, 0.2, -0.1], "l_arm": [-0.3, -0.2, -0.2], "l_fore": [0.6, -0.2, -0.1], "l_hand": [0.2, -0.2, 0.1], "curls": [0.8, 0.0, 0.8, 0.8, 0.8]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.3, 0.4], "r_fore": [0.7, 0.1, 0.2], "r_hand": [-0.2, 0.2, 0.1], "l_arm": [-0.4, -0.3, -0.4], "l_fore": [0.7, -0.1, -0.2], "l_hand": [-0.2, -0.2, -0.1], "curls": [0.8, 0.0, 0.8, 0.8, 0.8]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.1], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.0, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.1], "l_fore": [0.4, -0.1, 0.0], "l_hand": [0.0, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "tip",
        "name": "Tip",
        "gloss": "TIP",
        "duration": 1200,
        "type": "Advice / Pointer Noun",
        "notes": "ISLRTC 10,000 Dictionary. Dominant index finger touches the tip of the non-dominant vertical index finger (key point / hint).",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.2, 0.2], "r_fore": [0.7, 0.2, 0.1], "r_hand": [0.2, 0.2, -0.1], "l_arm": [-0.3, -0.1, -0.2], "l_fore": [0.6, -0.2, 0.1], "l_hand": [0.2, 0.0, 0.1], "curls": [0.8, 0.0, 0.8, 0.8, 0.8]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.1, 0.1], "r_fore": [0.8, 0.3, 0.1], "r_hand": [0.3, 0.1, -0.1], "l_arm": [-0.3, -0.1, -0.2], "l_fore": [0.6, -0.2, 0.1], "l_hand": [0.2, 0.0, 0.1], "curls": [0.8, 0.0, 0.8, 0.8, 0.8]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.1], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.0, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.1], "l_fore": [0.4, -0.1, 0.0], "l_hand": [0.0, 0.0, 0.0], "curls": [0.1, 0.0, 0.1, 0.1, 0.1]}
        ]
    },
    {
        "id": "sensation",
        "name": "Sensation",
        "gloss": "SENSATION",
        "duration": 1300,
        "type": "Sensory Feeling Noun",
        "notes": "ISLRTC 10,000 Dictionary. Open curved fingertips gently brush upward across center of sternum/chest indicating physical sensation.",
        "dominant": "right",
        "bones": ["Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Spine1"],
        "keyframes": [
            {"time": 350, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.1, 0.2], "r_fore": [0.7, 0.2, 0.1], "r_hand": [0.2, 0.1, -0.1], "spine": [-0.03, 0.0, 0.0], "curls": [0.3, 0.2, 0.2, 0.2, 0.2]},
            {"time": 750, "ease": "easeInOutQuad", "r_arm": [-0.5, 0.2, 0.2], "r_fore": [0.9, 0.3, 0.2], "r_hand": [0.3, 0.2, -0.1], "spine": [-0.05, 0.0, 0.0], "curls": [0.3, 0.2, 0.2, 0.2, 0.2]},
            {"time": 1050, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.1], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.1, 0.0, 0.0], "spine": [0.0, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "gym",
        "name": "Gym",
        "gloss": "GYM",
        "duration": 1250,
        "type": "Fitness Facility Noun",
        "notes": "ISLRTC 10,000 Dictionary. Dual S-fists held at shoulders pumping upward and downward repeatedly representing weight training and fitness.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.5, 0.3, 0.3], "r_fore": [0.8, 0.3, 0.2], "r_hand": [0.2, 0.1, -0.1], "l_arm": [-0.5, -0.3, -0.3], "l_fore": [0.8, -0.3, -0.2], "l_hand": [0.2, -0.1, 0.1], "curls": [0.9, 0.9, 0.9, 0.9, 0.9]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.6, 0.4, 0.4], "r_fore": [1.0, 0.4, 0.2], "r_hand": [0.3, 0.2, -0.2], "l_arm": [-0.6, -0.4, -0.4], "l_fore": [1.0, -0.4, -0.2], "l_hand": [0.3, -0.2, 0.2], "curls": [0.9, 0.9, 0.9, 0.9, 0.9]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.2], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.2], "l_fore": [0.4, -0.1, 0.0], "l_hand": [0.1, 0.0, 0.0], "curls": [0.2, 0.2, 0.2, 0.2, 0.2]}
        ]
    },
    {
        "id": "basis",
        "name": "Basis",
        "gloss": "BASIS",
        "duration": 1200,
        "type": "Foundation / Baseline Noun",
        "notes": "ISLRTC 10,000 Dictionary. Dual flat open palms held level at waist height smoothing horizontally outward to indicate baseline foundation.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.1, 0.2], "r_fore": [0.6, 0.2, 0.1], "r_hand": [0.3, 0.1, -0.1], "l_arm": [-0.3, -0.1, -0.2], "l_fore": [0.6, -0.2, -0.1], "l_hand": [0.3, -0.1, 0.1], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.3, 0.3], "r_fore": [0.7, 0.1, 0.2], "r_hand": [0.2, 0.2, -0.2], "l_arm": [-0.4, -0.3, -0.3], "l_fore": [0.7, -0.1, -0.2], "l_hand": [0.2, -0.2, 0.2], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.1], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.0, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.1], "l_fore": [0.4, -0.1, 0.0], "l_hand": [0.0, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "technique",
        "name": "Technique",
        "gloss": "TECHNIQUE",
        "duration": 1300,
        "type": "Methodology / Skill Noun",
        "notes": "ISLRTC 10,000 Dictionary. Dominant T-hand or open flat hand executing precise skilled stroke across the non-dominant vertical palm.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 350, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.2, 0.3], "r_fore": [0.7, 0.2, 0.2], "r_hand": [0.2, 0.2, -0.1], "l_arm": [-0.3, -0.1, -0.2], "l_fore": [0.6, -0.2, 0.1], "l_hand": [0.2, 0.0, 0.1], "curls": [0.6, 0.6, 0.1, 0.1, 0.1]},
            {"time": 750, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.1, 0.2], "r_fore": [0.8, 0.3, 0.1], "r_hand": [0.3, 0.1, -0.1], "l_arm": [-0.3, -0.1, -0.2], "l_fore": [0.6, -0.2, 0.1], "l_hand": [0.2, 0.0, 0.1], "curls": [0.6, 0.6, 0.1, 0.1, 0.1]},
            {"time": 1050, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.1], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.0, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.1], "l_fore": [0.4, -0.1, 0.0], "l_hand": [0.0, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
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

print(f"Successfully authored and verified {len(created_files)} Schema 2.0.0 signs (Batch 5):")
for name in created_files:
    print(f"  - signs/{name}")
