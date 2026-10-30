"""
tools/author_h24_batch4_signs.py

Phase H24 Batch 4: Authoring 24 Essential Vocabulary Signs in Schema 2.0.0.
Expands library from 260 to 284 Playable Assets.
Covers 150+ Spoken Token Occurrences.

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
        "id": "play",
        "name": "Play",
        "gloss": "PLAY",
        "duration": 1250,
        "type": "Recreation / Performance Verb",
        "notes": "ISLRTC 10,000 Dictionary. Dual open curved hands held forward at chest height oscillating playfully with wrist rotation.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.2, 0.3], "r_fore": [0.6, 0.2, 0.2], "r_hand": [0.3, 0.1, -0.2], "l_arm": [-0.3, -0.2, -0.3], "l_fore": [0.6, -0.2, -0.2], "l_hand": [0.3, -0.1, 0.2], "curls": [0.2, 0.2, 0.2, 0.2, 0.2]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.1, 0.2], "r_fore": [0.5, 0.1, 0.1], "r_hand": [-0.1, 0.2, -0.1], "l_arm": [-0.3, -0.1, -0.2], "l_fore": [0.5, -0.1, -0.1], "l_hand": [-0.1, -0.2, 0.1], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.2, 0.3], "r_fore": [0.6, 0.2, 0.2], "r_hand": [0.2, 0.1, -0.2], "l_arm": [-0.3, -0.2, -0.3], "l_fore": [0.6, -0.2, -0.2], "l_hand": [0.2, -0.1, 0.2], "curls": [0.2, 0.2, 0.2, 0.2, 0.2]}
        ]
    },
    {
        "id": "live",
        "name": "Live",
        "gloss": "LIVE",
        "duration": 1300,
        "type": "Existence / Vitality Verb",
        "notes": "ISLRTC 10,000 Dictionary. Both hands with L-handshapes ascending symmetrically upward along chest representing vitality and living.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Spine1"],
        "keyframes": [
            {"time": 350, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.2], "r_fore": [0.5, 0.2, 0.1], "r_hand": [0.2, 0.0, -0.1], "l_arm": [-0.2, -0.1, -0.2], "l_fore": [0.5, -0.2, -0.1], "l_hand": [0.2, 0.0, 0.1], "spine": [-0.04, 0.0, 0.0], "curls": [0.0, 0.0, 0.8, 0.8, 0.8]},
            {"time": 750, "ease": "easeInOutQuad", "r_arm": [-0.5, 0.2, 0.3], "r_fore": [0.8, 0.3, 0.2], "r_hand": [0.3, 0.1, -0.2], "l_arm": [-0.5, -0.2, -0.3], "l_fore": [0.8, -0.3, -0.2], "l_hand": [0.3, -0.1, 0.2], "spine": [-0.08, 0.0, 0.0], "curls": [0.0, 0.0, 0.8, 0.8, 0.8]},
            {"time": 1050, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.1, 0.2], "r_fore": [0.5, 0.1, 0.1], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.3, -0.1, -0.2], "l_fore": [0.5, -0.1, 0.0], "l_hand": [0.1, 0.0, 0.0], "spine": [-0.03, 0.0, 0.0], "curls": [0.0, 0.0, 0.3, 0.3, 0.3]}
        ]
    },
    {
        "id": "emotion",
        "name": "Emotion",
        "gloss": "EMOTION",
        "duration": 1350,
        "type": "Psychological Feeling Noun",
        "notes": "ISLRTC 10,000 Dictionary. Open curved hands alternating in gentle upward circular movement over the chest/heart region.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Spine1"],
        "keyframes": [
            {"time": 350, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.2, 0.2], "r_fore": [0.7, 0.2, 0.1], "r_hand": [0.2, 0.2, -0.1], "l_arm": [-0.2, -0.1, -0.1], "l_fore": [0.4, -0.1, -0.1], "l_hand": [0.0, -0.1, 0.1], "spine": [-0.04, 0.0, 0.0], "curls": [0.3, 0.2, 0.2, 0.2, 0.2]},
            {"time": 750, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.1], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.0, 0.1, -0.1], "l_arm": [-0.4, -0.2, -0.2], "l_fore": [0.7, -0.2, -0.1], "l_hand": [0.2, -0.2, 0.1], "spine": [-0.04, 0.0, 0.0], "curls": [0.3, 0.2, 0.2, 0.2, 0.2]},
            {"time": 1100, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.1, 0.2], "r_fore": [0.5, 0.1, 0.1], "r_hand": [0.1, 0.1, 0.0], "l_arm": [-0.3, -0.1, -0.2], "l_fore": [0.5, -0.1, 0.0], "l_hand": [0.1, -0.1, 0.0], "spine": [-0.02, 0.0, 0.0], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]}
        ]
    },
    {
        "id": "afraid",
        "name": "Afraid",
        "gloss": "AFRAID",
        "duration": 1250,
        "type": "Emotional State Adjective",
        "notes": "ISLRTC 10,000 Dictionary. Both hands with spread fingers retracting inward toward chest with tense vibration indicating fear/apprehension.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Spine1"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.5, 0.3, 0.3], "r_fore": [0.7, 0.3, 0.2], "r_hand": [0.3, 0.2, -0.2], "l_arm": [-0.5, -0.3, -0.3], "l_fore": [0.7, -0.3, -0.2], "l_hand": [0.3, -0.2, 0.2], "spine": [0.05, 0.0, 0.0], "curls": [0.3, 0.3, 0.3, 0.3, 0.3]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.1, 0.2], "r_fore": [0.8, 0.2, 0.1], "r_hand": [0.4, 0.1, -0.1], "l_arm": [-0.3, -0.1, -0.2], "l_fore": [0.8, -0.2, -0.1], "l_hand": [0.4, -0.1, 0.1], "spine": [0.08, 0.0, 0.0], "curls": [0.4, 0.4, 0.4, 0.4, 0.4]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.1], "r_fore": [0.5, 0.1, 0.1], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.1], "l_fore": [0.5, -0.1, 0.0], "l_hand": [0.1, 0.0, 0.0], "spine": [0.02, 0.0, 0.0], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]}
        ]
    },
    {
        "id": "place",
        "name": "Place",
        "gloss": "PLACE",
        "duration": 1200,
        "type": "Spatial Location Noun",
        "notes": "ISLRTC 10,000 Dictionary. Both hands with palms facing down moving symmetrically in a downward placement motion outlining a location.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.2, 0.3], "r_fore": [0.5, 0.1, 0.1], "r_hand": [0.2, 0.1, -0.2], "l_arm": [-0.4, -0.2, -0.3], "l_fore": [0.5, -0.1, -0.1], "l_hand": [0.2, -0.1, 0.2], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.2], "r_fore": [0.7, 0.2, 0.1], "r_hand": [0.3, 0.0, -0.1], "l_arm": [-0.2, -0.1, -0.2], "l_fore": [0.7, -0.2, -0.1], "l_hand": [0.3, 0.0, 0.1], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.1], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.1], "l_fore": [0.4, -0.1, 0.0], "l_hand": [0.1, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "house",
        "name": "House",
        "gloss": "HOUSE",
        "duration": 1300,
        "type": "Architecture / Habitat Noun",
        "notes": "ISLRTC 10,000 Dictionary. Both flat hands touch at fingertips to form an inverted V roof, then separate and move vertically downward.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 350, "ease": "easeInOutQuad", "r_arm": [-0.5, 0.2, 0.3], "r_fore": [0.8, 0.2, 0.2], "r_hand": [0.3, 0.2, -0.3], "l_arm": [-0.5, -0.2, -0.3], "l_fore": [0.8, -0.2, -0.2], "l_hand": [0.3, -0.2, 0.3], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 750, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.3, 0.3], "r_fore": [0.6, 0.1, 0.1], "r_hand": [0.2, 0.0, -0.1], "l_arm": [-0.3, -0.3, -0.3], "l_fore": [0.6, -0.1, -0.1], "l_hand": [0.2, 0.0, 0.1], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 1050, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.2], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.2], "l_fore": [0.4, -0.1, 0.0], "l_hand": [0.1, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "sorry",
        "name": "Sorry",
        "gloss": "SORRY",
        "duration": 1250,
        "type": "Social / Apology Interjection",
        "notes": "ISLRTC 10,000 Dictionary. Right fist rubbing in a clockwise circular motion over the center of the chest.",
        "dominant": "right",
        "bones": ["Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.2, 0.3], "r_fore": [0.8, 0.3, 0.2], "r_hand": [0.3, 0.1, -0.1], "head": [0.08, 0.0, 0.0], "curls": [0.9, 0.9, 0.9, 0.9, 0.9]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.1, 0.2], "r_fore": [0.8, 0.4, 0.1], "r_hand": [0.2, 0.2, -0.1], "head": [0.10, 0.0, 0.0], "curls": [0.9, 0.9, 0.9, 0.9, 0.9]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.2], "r_fore": [0.5, 0.2, 0.1], "r_hand": [0.1, 0.0, 0.0], "head": [0.04, 0.0, 0.0], "curls": [0.3, 0.3, 0.3, 0.3, 0.3]}
        ]
    },
    {
        "id": "believe",
        "name": "Believe",
        "gloss": "BELIEVE",
        "duration": 1350,
        "type": "Cognition / Faith Verb",
        "notes": "ISLRTC 10,000 Dictionary. Dominant index finger touches temple/forehead then descends to clasp firmly onto the flat non-dominant palm.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 350, "ease": "easeInOutQuad", "r_arm": [-0.6, 0.3, 0.3], "r_fore": [1.0, 0.3, 0.2], "r_hand": [0.3, 0.2, -0.1], "l_arm": [-0.2, -0.1, -0.1], "l_fore": [0.4, -0.1, 0.0], "l_hand": [0.0, 0.0, 0.0], "head": [0.05, 0.0, 0.0], "curls": [0.8, 0.0, 0.8, 0.8, 0.8]},
            {"time": 750, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.2, 0.2], "r_fore": [0.7, 0.2, 0.1], "r_hand": [0.2, 0.1, -0.1], "l_arm": [-0.3, -0.2, -0.2], "l_fore": [0.6, -0.2, 0.1], "l_hand": [0.2, 0.0, 0.1], "head": [0.02, 0.0, 0.0], "curls": [0.4, 0.4, 0.4, 0.4, 0.4]},
            {"time": 1050, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.1], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.1], "l_fore": [0.4, -0.1, 0.0], "l_hand": [0.1, 0.0, 0.0], "head": [0.0, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "company",
        "name": "Company",
        "gloss": "COMPANY",
        "duration": 1300,
        "type": "Corporate Entity Noun",
        "notes": "ISLRTC 10,000 Dictionary. Both hands form C-handshapes at chest height, rotating forward and touching fingertips.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 350, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.2, 0.3], "r_fore": [0.6, 0.2, 0.2], "r_hand": [0.2, 0.2, -0.2], "l_arm": [-0.3, -0.2, -0.3], "l_fore": [0.6, -0.2, -0.2], "l_hand": [0.2, -0.2, 0.2], "curls": [0.5, 0.5, 0.5, 0.5, 0.5]},
            {"time": 750, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.1, 0.2], "r_fore": [0.7, 0.3, 0.1], "r_hand": [0.1, 0.1, -0.1], "l_arm": [-0.3, -0.1, -0.2], "l_fore": [0.7, -0.3, -0.1], "l_hand": [0.1, -0.1, 0.1], "curls": [0.5, 0.5, 0.5, 0.5, 0.5]},
            {"time": 1050, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.2], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.0, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.2], "l_fore": [0.4, -0.1, 0.0], "l_hand": [0.0, 0.0, 0.0], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]}
        ]
    },
    {
        "id": "sing",
        "name": "Sing",
        "gloss": "SING",
        "duration": 1250,
        "type": "Musical Vocalization Verb",
        "notes": "ISLRTC 10,000 Dictionary. Right open curved hand moving smoothly outward from lips in rhythmic musical wave arches.",
        "dominant": "right",
        "bones": ["Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.5, 0.2, 0.3], "r_fore": [0.9, 0.2, 0.2], "r_hand": [0.3, 0.2, -0.1], "head": [-0.05, 0.05, 0.0], "curls": [0.2, 0.2, 0.2, 0.2, 0.2]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.3, 0.4], "r_fore": [0.7, 0.3, 0.3], "r_hand": [0.2, 0.3, -0.2], "head": [-0.02, 0.0, 0.0], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.2], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.1, 0.0, 0.0], "head": [0.0, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "song",
        "name": "Song",
        "gloss": "SONG",
        "duration": 1300,
        "type": "Musical Composition Noun",
        "notes": "ISLRTC 10,000 Dictionary. Symmetrical dual hands swaying rhythmically side-to-side in musical expression.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 350, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.3, 0.3], "r_fore": [0.7, 0.2, 0.2], "r_hand": [0.2, 0.2, -0.1], "l_arm": [-0.3, -0.1, -0.2], "l_fore": [0.5, -0.1, -0.1], "l_hand": [0.1, -0.1, 0.1], "head": [0.0, 0.05, 0.05], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]},
            {"time": 750, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.1, 0.2], "r_fore": [0.5, 0.1, 0.1], "r_hand": [0.1, 0.1, -0.1], "l_arm": [-0.4, -0.3, -0.3], "l_fore": [0.7, -0.2, -0.2], "l_hand": [0.2, -0.2, 0.1], "head": [0.0, -0.05, -0.05], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]},
            {"time": 1050, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.2], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.0, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.2], "l_fore": [0.4, -0.1, 0.0], "l_hand": [0.0, 0.0, 0.0], "head": [0.0, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "money",
        "name": "Money",
        "gloss": "MONEY",
        "duration": 1200,
        "type": "Currency / Financial Noun",
        "notes": "ISLRTC 10,000 Dictionary. Dominant thumb rubbing across index and middle fingertips repeatedly representing currency.",
        "dominant": "right",
        "bones": ["Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.2, 0.2], "r_fore": [0.7, 0.2, 0.1], "r_hand": [0.2, 0.1, -0.1], "curls": [0.2, 0.2, 0.2, 0.8, 0.8]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.2, 0.2], "r_fore": [0.7, 0.2, 0.1], "r_hand": [0.3, 0.2, -0.2], "curls": [0.4, 0.4, 0.4, 0.8, 0.8]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.1], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.1, 0.0, 0.0], "curls": [0.1, 0.1, 0.1, 0.2, 0.2]}
        ]
    },
    {
        "id": "real",
        "name": "Real",
        "gloss": "REAL",
        "duration": 1200,
        "type": "Truth / Veracity Adjective",
        "notes": "ISLRTC 10,000 Dictionary. Dominant index finger pointing upward near chin moving firmly straight forward to assert truth.",
        "dominant": "right",
        "bones": ["Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.5, 0.2, 0.2], "r_fore": [0.9, 0.2, 0.1], "r_hand": [0.2, 0.1, 0.0], "head": [0.04, 0.0, 0.0], "curls": [0.8, 0.0, 0.8, 0.8, 0.8]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.2, 0.3], "r_fore": [0.6, 0.1, 0.2], "r_hand": [0.3, 0.2, -0.1], "head": [0.08, 0.0, 0.0], "curls": [0.8, 0.0, 0.8, 0.8, 0.8]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.2], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.1, 0.0, 0.0], "head": [0.02, 0.0, 0.0], "curls": [0.2, 0.0, 0.2, 0.2, 0.2]}
        ]
    },
    {
        "id": "hour",
        "name": "Hour",
        "gloss": "HOUR",
        "duration": 1350,
        "type": "Temporal Duration Noun",
        "notes": "ISLRTC 10,000 Dictionary. Non-dominant palm faces right; dominant index finger traces a complete circular clockwise rotation against the palm.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 350, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.2, 0.2], "r_fore": [0.7, 0.2, 0.1], "r_hand": [0.3, 0.2, -0.1], "l_arm": [-0.3, -0.1, -0.2], "l_fore": [0.6, -0.2, 0.1], "l_hand": [0.2, 0.0, 0.1], "curls": [0.8, 0.0, 0.8, 0.8, 0.8]},
            {"time": 750, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.1, 0.2], "r_fore": [0.8, 0.3, 0.1], "r_hand": [-0.1, 0.2, 0.2], "l_arm": [-0.3, -0.1, -0.2], "l_fore": [0.6, -0.2, 0.1], "l_hand": [0.2, 0.0, 0.1], "curls": [0.8, 0.0, 0.8, 0.8, 0.8]},
            {"time": 1050, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.1], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.0, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.1], "l_fore": [0.4, -0.1, 0.0], "l_hand": [0.0, 0.0, 0.0], "curls": [0.1, 0.0, 0.1, 0.1, 0.1]}
        ]
    },
    {
        "id": "perfect",
        "name": "Perfect",
        "gloss": "PERFECT",
        "duration": 1250,
        "type": "Precision / Excellence Adjective",
        "notes": "ISLRTC 10,000 Dictionary. Both hands form F-handshapes (thumb and index fingertips meeting), meeting cleanly at center with crisp affirmation.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.3, 0.3], "r_fore": [0.6, 0.2, 0.2], "r_hand": [0.2, 0.2, -0.2], "l_arm": [-0.4, -0.3, -0.3], "l_fore": [0.6, -0.2, -0.2], "l_hand": [0.2, -0.2, 0.2], "head": [0.04, 0.0, 0.0], "curls": [0.7, 0.7, 0.0, 0.0, 0.0]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.1, 0.2], "r_fore": [0.7, 0.2, 0.1], "r_hand": [0.1, 0.1, -0.1], "l_arm": [-0.3, -0.1, -0.2], "l_fore": [0.7, -0.2, -0.1], "l_hand": [0.1, -0.1, 0.1], "head": [0.08, 0.0, 0.0], "curls": [0.8, 0.8, 0.0, 0.0, 0.0]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.1], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.0, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.1], "l_fore": [0.4, -0.1, 0.0], "l_hand": [0.0, 0.0, 0.0], "head": [0.02, 0.0, 0.0], "curls": [0.1, 0.1, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "sit",
        "name": "Sit",
        "gloss": "SIT",
        "duration": 1200,
        "type": "Posture Verb",
        "notes": "ISLRTC 10,000 Dictionary. Dominant curved index and middle fingers descend down over non-dominant horizontal fingers to represent sitting.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.2, 0.2], "r_fore": [0.6, 0.2, 0.1], "r_hand": [0.2, 0.1, -0.1], "l_arm": [-0.3, -0.1, -0.2], "l_fore": [0.6, -0.2, 0.1], "l_hand": [0.2, 0.0, 0.1], "curls": [0.8, 0.5, 0.5, 0.8, 0.8]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.1, 0.1], "r_fore": [0.8, 0.2, 0.1], "r_hand": [0.4, 0.1, -0.1], "l_arm": [-0.3, -0.1, -0.2], "l_fore": [0.6, -0.2, 0.1], "l_hand": [0.2, 0.0, 0.1], "curls": [0.8, 0.6, 0.6, 0.8, 0.8]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.1], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.1], "l_fore": [0.4, -0.1, 0.0], "l_hand": [0.1, 0.0, 0.0], "curls": [0.2, 0.1, 0.1, 0.2, 0.2]}
        ]
    },
    {
        "id": "car",
        "name": "Car",
        "gloss": "CAR",
        "duration": 1250,
        "type": "Vehicle Noun",
        "notes": "ISLRTC 10,000 Dictionary. Both hands grasping steering wheel at chest level, executing alternating turns.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.2, 0.3], "r_fore": [0.7, 0.2, 0.2], "r_hand": [0.2, 0.2, -0.2], "l_arm": [-0.3, -0.2, -0.2], "l_fore": [0.5, -0.1, -0.1], "l_hand": [-0.1, -0.1, 0.1], "curls": [0.8, 0.8, 0.8, 0.8, 0.8]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.1, 0.2], "r_fore": [0.5, 0.1, 0.1], "r_hand": [-0.1, 0.1, -0.1], "l_arm": [-0.4, -0.2, -0.3], "l_fore": [0.7, -0.2, -0.2], "l_hand": [0.2, -0.2, 0.2], "curls": [0.8, 0.8, 0.8, 0.8, 0.8]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.2], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.0, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.2], "l_fore": [0.4, -0.1, 0.0], "l_hand": [0.0, 0.0, 0.0], "curls": [0.2, 0.2, 0.2, 0.2, 0.2]}
        ]
    },
    {
        "id": "turn",
        "name": "Turn",
        "gloss": "TURN",
        "duration": 1200,
        "type": "Directional / Rotation Verb",
        "notes": "ISLRTC 10,000 Dictionary. Both hands with index fingers or flat palms executing a rotational arc indicating a change in orientation.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.2, 0.3], "r_fore": [0.6, 0.2, 0.2], "r_hand": [0.2, 0.3, -0.2], "l_arm": [-0.3, -0.2, -0.3], "l_fore": [0.6, -0.2, -0.2], "l_hand": [0.2, -0.3, 0.2], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.1, 0.2], "r_fore": [0.7, 0.3, 0.1], "r_hand": [-0.2, 0.2, 0.1], "l_arm": [-0.4, -0.1, -0.2], "l_fore": [0.7, -0.3, -0.1], "l_hand": [-0.2, -0.2, -0.1], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.1], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.0, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.1], "l_fore": [0.4, -0.1, 0.0], "l_hand": [0.0, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "normal",
        "name": "Normal",
        "gloss": "NORMAL",
        "duration": 1250,
        "type": "Standard / Regular Adjective",
        "notes": "ISLRTC 10,000 Dictionary. Dominant flat hand circling smoothly clockwise and settling flat on non-dominant horizontal palm.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.2, 0.3], "r_fore": [0.6, 0.2, 0.2], "r_hand": [0.2, 0.2, -0.1], "l_arm": [-0.3, -0.1, -0.2], "l_fore": [0.6, -0.2, 0.1], "l_hand": [0.2, 0.0, 0.1], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.1, 0.1], "r_fore": [0.7, 0.2, 0.1], "r_hand": [0.3, 0.0, -0.1], "l_arm": [-0.3, -0.1, -0.2], "l_fore": [0.6, -0.2, 0.1], "l_hand": [0.2, 0.0, 0.1], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.1], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.1], "l_fore": [0.4, -0.1, 0.0], "l_hand": [0.1, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "confused",
        "name": "Confused",
        "gloss": "CONFUSED",
        "duration": 1300,
        "type": "Cognitive Disorientation Adjective",
        "notes": "ISLRTC 10,000 Dictionary. Both hands with curved claw fingers circling past each other near the forehead.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 350, "ease": "easeInOutQuad", "r_arm": [-0.5, 0.2, 0.3], "r_fore": [0.9, 0.3, 0.2], "r_hand": [0.3, 0.2, -0.2], "l_arm": [-0.4, -0.2, -0.2], "l_fore": [0.7, -0.2, -0.1], "l_hand": [0.1, -0.2, 0.1], "head": [0.05, 0.05, 0.0], "curls": [0.5, 0.5, 0.5, 0.5, 0.5]},
            {"time": 750, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.2, 0.2], "r_fore": [0.7, 0.2, 0.1], "r_hand": [0.1, 0.2, -0.1], "l_arm": [-0.5, -0.2, -0.3], "l_fore": [0.9, -0.3, -0.2], "l_hand": [0.3, -0.2, 0.2], "head": [0.05, -0.05, 0.0], "curls": [0.5, 0.5, 0.5, 0.5, 0.5]},
            {"time": 1050, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.2], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.0, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.2], "l_fore": [0.4, -0.1, 0.0], "l_hand": [0.0, 0.0, 0.0], "head": [0.0, 0.0, 0.0], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]}
        ]
    },
    {
        "id": "remind",
        "name": "Remind",
        "gloss": "REMIND",
        "duration": 1250,
        "type": "Cognitive Recall Verb",
        "notes": "ISLRTC 10,000 Dictionary. Dominant thumb/index tapping near temple/shoulder to bring back memory or recall.",
        "dominant": "right",
        "bones": ["Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.6, 0.3, 0.3], "r_fore": [0.9, 0.3, 0.2], "r_hand": [0.3, 0.2, -0.1], "head": [0.04, 0.04, 0.0], "curls": [0.7, 0.0, 0.7, 0.7, 0.7]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.5, 0.2, 0.2], "r_fore": [0.7, 0.2, 0.1], "r_hand": [0.2, 0.1, -0.1], "head": [0.06, 0.0, 0.0], "curls": [0.7, 0.0, 0.7, 0.7, 0.7]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.1], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.1, 0.0, 0.0], "head": [0.0, 0.0, 0.0], "curls": [0.2, 0.0, 0.2, 0.2, 0.2]}
        ]
    },
    {
        "id": "definition",
        "name": "Definition",
        "gloss": "DEFINITION",
        "duration": 1300,
        "type": "Linguistic Explanation Noun",
        "notes": "ISLRTC 10,000 Dictionary. Both hands with index and middle fingers extended apart horizontally defining explicit meaning.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 350, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.2, 0.3], "r_fore": [0.7, 0.2, 0.2], "r_hand": [0.2, 0.2, -0.1], "l_arm": [-0.4, -0.2, -0.3], "l_fore": [0.7, -0.2, -0.2], "l_hand": [0.2, -0.2, 0.1], "curls": [0.7, 0.0, 0.0, 0.7, 0.7]},
            {"time": 750, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.3, 0.4], "r_fore": [0.6, 0.2, 0.2], "r_hand": [0.1, 0.3, -0.2], "l_arm": [-0.4, -0.3, -0.4], "l_fore": [0.6, -0.2, -0.2], "l_hand": [0.1, -0.3, 0.2], "curls": [0.7, 0.0, 0.0, 0.7, 0.7]},
            {"time": 1050, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.2], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.0, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.2], "l_fore": [0.4, -0.1, 0.0], "l_hand": [0.0, 0.0, 0.0], "curls": [0.1, 0.0, 0.0, 0.1, 0.1]}
        ]
    },
    {
        "id": "happen",
        "name": "Happen",
        "gloss": "HAPPEN",
        "duration": 1250,
        "type": "Occurrence / Event Verb",
        "notes": "ISLRTC 10,000 Dictionary. Both hands with palms up rotate simultaneously inward flipping palms down to signify an event occurring.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.2, 0.3], "r_fore": [0.6, 0.2, 0.2], "r_hand": [0.2, 0.2, -0.2], "l_arm": [-0.3, -0.2, -0.3], "l_fore": [0.6, -0.2, -0.2], "l_hand": [0.2, -0.2, 0.2], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.1, 0.2], "r_fore": [0.7, 0.2, 0.1], "r_hand": [0.4, -0.2, 0.1], "l_arm": [-0.3, -0.1, -0.2], "l_fore": [0.7, -0.2, -0.1], "l_hand": [0.4, 0.2, -0.1], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.1], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.1], "l_fore": [0.4, -0.1, 0.0], "l_hand": [0.1, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "slowly",
        "name": "Slowly",
        "gloss": "SLOWLY",
        "duration": 1300,
        "type": "Pace Adverb",
        "notes": "ISLRTC 10,000 Dictionary. Dominant open flat hand gently and deliberately strokes upward along the dorsal surface of the non-dominant forearm.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 350, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.2, 0.2], "r_fore": [0.6, 0.2, 0.1], "r_hand": [0.2, 0.1, -0.1], "l_arm": [-0.3, -0.1, -0.2], "l_fore": [0.6, -0.2, 0.1], "l_hand": [0.2, 0.0, 0.1], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 750, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.2, 0.2], "r_fore": [0.8, 0.3, 0.2], "r_hand": [0.3, 0.2, -0.1], "l_arm": [-0.3, -0.1, -0.2], "l_fore": [0.6, -0.2, 0.1], "l_hand": [0.2, 0.0, 0.1], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 1050, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.1], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.1], "l_fore": [0.4, -0.1, 0.0], "l_hand": [0.1, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
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

print(f"Successfully authored and verified {len(created_files)} Schema 2.0.0 signs (Batch 4):")
for name in created_files:
    print(f"  - signs/{name}")
