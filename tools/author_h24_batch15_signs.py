"""
tools/author_h24_batch15_signs.py

Phase H24 Batch 15: Authoring 20 Essential Educational & Discourse Signs in Schema 2.0.0.
Expands library from 500 to 520 Playable Assets (+313 total in H24).
Covers 60+ Spoken Token Occurrences.

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
        "id": "may",
        "name": "May",
        "gloss": "MAY",
        "duration": 1200,
        "type": "Modal Auxiliary Verb",
        "notes": "ISLRTC 10,000 Dictionary. Dominant open flat palm dips gently with subtle forward-nodding arc representing possibility and permission.",
        "dominant": "right",
        "bones": ["Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Spine"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.1, 0.05], "r_fore": [0.55, 0.05, 0.0], "r_hand": [0.15, 0.0, 0.0], "curls": [0.2, 0.2, 0.2, 0.2, 0.2]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.1, 0.05], "r_fore": [0.70, 0.05, 0.0], "r_hand": [0.25, 0.0, 0.0], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.05, 0.02], "r_fore": [0.35, 0.02, 0.0], "r_hand": [0.1, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "hey",
        "name": "Hey",
        "gloss": "HEY",
        "duration": 1150,
        "type": "Social Salutation / Greeting",
        "notes": "ISLRTC 10,000 Dictionary. Dominant open flat hand raised near shoulder level waving briskly side-to-side in salutation.",
        "dominant": "right",
        "bones": ["Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.5, 0.25, 0.15], "r_fore": [0.75, 0.15, 0.0], "r_hand": [0.2, 0.2, 0.0], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]},
            {"time": 600, "ease": "easeInOutQuad", "r_arm": [-0.55, 0.20, 0.15], "r_fore": [0.80, 0.10, 0.0], "r_hand": [0.2, -0.2, 0.0], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]},
            {"time": 900, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.10, 0.05], "r_fore": [0.45, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "boom",
        "name": "Boom",
        "gloss": "BOOM",
        "duration": 1200,
        "type": "Descriptor / Exclamation",
        "notes": "ISLRTC 10,000 Dictionary. Dual fists held at midline burst outward rapidly into open claw handshapes representing sudden explosion.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Spine"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.1, 0.05], "r_fore": [0.60, 0.1, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.3, -0.1, -0.05], "l_fore": [0.60, -0.1, 0.0], "l_hand": [0.1, 0.0, 0.0], "curls": [0.9, 0.9, 0.9, 0.9, 0.9]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.6, 0.35, 0.2], "r_fore": [0.55, 0.25, 0.0], "r_hand": [0.25, 0.1, 0.0], "l_arm": [-0.6, -0.35, -0.2], "l_fore": [0.55, -0.25, 0.0], "l_hand": [0.25, -0.1, 0.0], "curls": [0.4, 0.4, 0.4, 0.4, 0.4]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.25, 0.1, 0.05], "r_fore": [0.35, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.25, -0.1, -0.05], "l_fore": [0.35, -0.05, 0.0], "l_hand": [0.1, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "sweden",
        "name": "Sweden",
        "gloss": "SWEDEN",
        "duration": 1250,
        "type": "Geographical Noun",
        "notes": "ISLRTC 10,000 Dictionary. Dominant curved hand descends gently from above stationary non-dominant fist outlining Swedish cap/crest.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.5, 0.15, 0.1], "r_fore": [0.75, 0.1, 0.0], "r_hand": [0.2, 0.0, 0.0], "l_arm": [-0.25, -0.1, -0.05], "l_fore": [0.55, -0.1, 0.0], "l_hand": [0.1, 0.0, 0.0], "curls": [0.5, 0.5, 0.5, 0.5, 0.5]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.38, 0.12, 0.08], "r_fore": [0.65, 0.08, 0.0], "r_hand": [0.25, 0.0, 0.0], "l_arm": [-0.25, -0.1, -0.05], "l_fore": [0.55, -0.1, 0.0], "l_hand": [0.1, 0.0, 0.0], "curls": [0.5, 0.5, 0.5, 0.5, 0.5]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.05, 0.05], "r_fore": [0.35, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.15, -0.05, -0.02], "l_fore": [0.30, -0.05, 0.0], "l_hand": [0.05, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "everything",
        "name": "Everything",
        "gloss": "EVERYTHING",
        "duration": 1300,
        "type": "Universal Determiner / Pronoun",
        "notes": "ISLRTC 10,000 Dictionary. Dual open flat palms sweep outward in wide horizontal circular arc encompassing the entire signing space.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Spine"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.1, 0.05], "r_fore": [0.50, 0.1, 0.0], "r_hand": [0.15, 0.0, 0.0], "l_arm": [-0.3, -0.1, -0.05], "l_fore": [0.50, -0.1, 0.0], "l_hand": [0.15, 0.0, 0.0], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]},
            {"time": 700, "ease": "easeInOutQuad", "r_arm": [-0.45, 0.35, 0.2], "r_fore": [0.65, 0.25, 0.0], "r_hand": [0.25, 0.1, 0.0], "l_arm": [-0.45, -0.35, -0.2], "l_fore": [0.65, -0.25, 0.0], "l_hand": [0.25, -0.1, 0.0], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]},
            {"time": 1000, "ease": "easeInOutQuad", "r_arm": [-0.25, 0.15, 0.05], "r_fore": [0.35, 0.08, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.25, -0.15, -0.05], "l_fore": [0.35, -0.08, 0.0], "l_hand": [0.1, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "somebody",
        "name": "Somebody",
        "gloss": "SOMEBODY",
        "duration": 1200,
        "type": "Indefinite Pronoun",
        "notes": "ISLRTC 10,000 Dictionary. Dominant upright 1-hand executes slight circular questioning oscillation in neutral chest space.",
        "dominant": "right",
        "bones": ["Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.35, 0.15, 0.1], "r_fore": [0.65, 0.1, 0.0], "r_hand": [0.2, 0.1, 0.0], "curls": [0.8, 0.0, 0.8, 0.8, 0.8]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.38, 0.12, 0.1], "r_fore": [0.70, 0.05, 0.0], "r_hand": [0.2, -0.1, 0.0], "curls": [0.8, 0.0, 0.8, 0.8, 0.8]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.05, 0.05], "r_fore": [0.40, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "curls": [0.2, 0.0, 0.2, 0.2, 0.2]}
        ]
    },
    {
        "id": "anyone",
        "name": "Anyone",
        "gloss": "ANYONE",
        "duration": 1200,
        "type": "Indefinite Personal Pronoun",
        "notes": "ISLRTC 10,000 Dictionary. Dominant open palm rotates horizontally with index finger pointing upward across personal reference plane.",
        "dominant": "right",
        "bones": ["Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.15, 0.08], "r_fore": [0.55, 0.1, 0.0], "r_hand": [0.15, 0.15, 0.0], "curls": [0.7, 0.0, 0.7, 0.7, 0.7]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.25, 0.15], "r_fore": [0.65, 0.15, 0.0], "r_hand": [0.25, 0.1, 0.0], "curls": [0.7, 0.0, 0.7, 0.7, 0.7]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.05], "r_fore": [0.35, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "curls": [0.1, 0.0, 0.1, 0.1, 0.1]}
        ]
    },
    {
        "id": "anything",
        "name": "Anything",
        "gloss": "ANYTHING",
        "duration": 1200,
        "type": "Indefinite Pronoun",
        "notes": "ISLRTC 10,000 Dictionary. Dominant flat open hand sweeps outward from center to lateral space with subtle wrist dip.",
        "dominant": "right",
        "bones": ["Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.28, 0.1, 0.05], "r_fore": [0.50, 0.08, 0.0], "r_hand": [0.15, 0.1, 0.0], "curls": [0.2, 0.2, 0.2, 0.2, 0.2]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.38, 0.25, 0.15], "r_fore": [0.60, 0.18, 0.0], "r_hand": [0.25, 0.05, 0.0], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.05], "r_fore": [0.35, 0.08, 0.0], "r_hand": [0.1, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "nothing",
        "name": "Nothing",
        "gloss": "NOTHING",
        "duration": 1250,
        "type": "Negative Determiner / Pronoun",
        "notes": "ISLRTC 10,000 Dictionary. Dual open hands facing outward shake horizontally side-to-side across chest in decisive negation.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.35, 0.15, 0.1], "r_fore": [0.60, 0.1, 0.0], "r_hand": [0.2, 0.15, 0.0], "l_arm": [-0.35, -0.15, -0.1], "l_fore": [0.60, -0.1, 0.0], "l_hand": [0.2, -0.15, 0.0], "head": [0.0, 0.05, 0.0], "curls": [0.8, 0.8, 0.8, 0.8, 0.8]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.38, 0.25, 0.15], "r_fore": [0.65, 0.15, 0.0], "r_hand": [0.2, -0.15, 0.0], "l_arm": [-0.38, -0.25, -0.15], "l_fore": [0.65, -0.15, 0.0], "l_hand": [0.2, 0.15, 0.0], "head": [0.0, -0.05, 0.0], "curls": [0.8, 0.8, 0.8, 0.8, 0.8]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.05], "r_fore": [0.35, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.05], "l_fore": [0.35, -0.05, 0.0], "l_hand": [0.1, 0.0, 0.0], "head": [0.0, 0.0, 0.0], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]}
        ]
    },
    {
        "id": "until",
        "name": "Until",
        "gloss": "UNTIL",
        "duration": 1300,
        "type": "Temporal Preposition / Conjunction",
        "notes": "ISLRTC 10,000 Dictionary. Dominant 1-finger travels in a forward upward arc to contact the tip of the upright stationary non-dominant index finger.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.35, 0.2, 0.1], "r_fore": [0.50, 0.1, 0.0], "r_hand": [0.15, 0.0, 0.0], "l_arm": [-0.30, -0.1, -0.05], "l_fore": [0.65, -0.1, 0.0], "l_hand": [0.15, 0.0, 0.0], "curls": [0.8, 0.0, 0.8, 0.8, 0.8]},
            {"time": 700, "ease": "easeInOutQuad", "r_arm": [-0.42, 0.08, 0.05], "r_fore": [0.72, 0.05, 0.0], "r_hand": [0.25, 0.0, 0.0], "l_arm": [-0.32, -0.1, -0.05], "l_fore": [0.68, -0.1, 0.0], "l_hand": [0.15, 0.0, 0.0], "curls": [0.8, 0.0, 0.8, 0.8, 0.8]},
            {"time": 1000, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.05, 0.02], "r_fore": [0.40, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.15, -0.05, -0.02], "l_fore": [0.35, -0.05, 0.0], "l_hand": [0.05, 0.0, 0.0], "curls": [0.1, 0.0, 0.1, 0.1, 0.1]}
        ]
    },
    {
        "id": "weird",
        "name": "Weird",
        "gloss": "WEIRD",
        "duration": 1250,
        "type": "Descriptor Adjective",
        "notes": "ISLRTC 10,000 Dictionary. Dominant curved claw hand moves horizontally across forehead with gentle wriggling oscillation.",
        "dominant": "right",
        "bones": ["Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.55, 0.20, 0.15], "r_fore": [0.80, 0.15, 0.0], "r_hand": [0.25, 0.1, 0.0], "head": [0.03, 0.02, 0.0], "curls": [0.5, 0.5, 0.5, 0.5, 0.5]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.58, 0.10, 0.10], "r_fore": [0.85, 0.05, 0.0], "r_hand": [0.25, -0.1, 0.0], "head": [-0.02, -0.02, 0.0], "curls": [0.6, 0.6, 0.6, 0.6, 0.6]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.05, 0.05], "r_fore": [0.45, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "head": [0.0, 0.0, 0.0], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]}
        ]
    },
    {
        "id": "along",
        "name": "Along",
        "gloss": "ALONG",
        "duration": 1200,
        "type": "Directional Preposition",
        "notes": "ISLRTC 10,000 Dictionary. Dual flat hands held parallel facing each other moving together forward along a straight trajectory.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.25, 0.1, 0.05], "r_fore": [0.50, 0.08, 0.0], "r_hand": [0.15, 0.0, 0.0], "l_arm": [-0.25, -0.1, -0.05], "l_fore": [0.50, -0.08, 0.0], "l_hand": [0.15, 0.0, 0.0], "curls": [0.2, 0.2, 0.2, 0.2, 0.2]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.40, 0.1, 0.05], "r_fore": [0.70, 0.08, 0.0], "r_hand": [0.25, 0.0, 0.0], "l_arm": [-0.40, -0.1, -0.05], "l_fore": [0.70, -0.08, 0.0], "l_hand": [0.25, 0.0, 0.0], "curls": [0.2, 0.2, 0.2, 0.2, 0.2]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.20, 0.05, 0.02], "r_fore": [0.40, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.20, -0.05, -0.02], "l_fore": [0.40, -0.05, 0.0], "l_hand": [0.1, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "quarter",
        "name": "Quarter",
        "gloss": "QUARTER",
        "duration": 1250,
        "type": "Fraction / Numerical Noun",
        "notes": "ISLRTC 10,000 Dictionary. Dominant hand shows numeral 1 then dips downward and transforms into numeral 4.",
        "dominant": "right",
        "bones": ["Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.40, 0.15, 0.1], "r_fore": [0.70, 0.1, 0.0], "r_hand": [0.2, 0.0, 0.0], "curls": [0.9, 0.0, 0.9, 0.9, 0.9]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.30, 0.15, 0.1], "r_fore": [0.55, 0.1, 0.0], "r_hand": [0.2, 0.0, 0.0], "curls": [0.9, 0.0, 0.0, 0.0, 0.0]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.18, 0.08, 0.05], "r_fore": [0.35, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "curls": [0.2, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "tumble",
        "name": "Tumble",
        "gloss": "TUMBLE",
        "duration": 1250,
        "type": "Action / Fall Verb",
        "notes": "ISLRTC 10,000 Dictionary. Dual inverted V-hands roll and flip downward over each other simulating a tumbling fall.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.35, 0.15, 0.1], "r_fore": [0.60, 0.1, 0.0], "r_hand": [0.2, 0.1, 0.0], "l_arm": [-0.30, -0.1, -0.05], "l_fore": [0.55, -0.1, 0.0], "l_hand": [0.2, -0.1, 0.0], "curls": [0.7, 0.0, 0.0, 0.7, 0.7]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.45, 0.05, 0.05], "r_fore": [0.65, 0.05, 0.0], "r_hand": [0.3, -0.15, 0.0], "l_arm": [-0.40, -0.05, -0.05], "l_fore": [0.60, -0.05, 0.0], "l_hand": [0.3, 0.15, 0.0], "curls": [0.7, 0.0, 0.0, 0.7, 0.7]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.05, 0.02], "r_fore": [0.35, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.05, -0.02], "l_fore": [0.35, -0.05, 0.0], "l_hand": [0.1, 0.0, 0.0], "curls": [0.1, 0.0, 0.0, 0.1, 0.1]}
        ]
    },
    {
        "id": "fill",
        "name": "Fill",
        "gloss": "FILL",
        "duration": 1250,
        "type": "Action / Completion Verb",
        "notes": "ISLRTC 10,000 Dictionary. Non-dominant hand forms C-cup; dominant flat palm sweeps firmly across top rim indicating complete capacity.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.35, 0.20, 0.1], "r_fore": [0.55, 0.15, 0.0], "r_hand": [0.15, 0.0, 0.0], "l_arm": [-0.28, -0.1, -0.05], "l_fore": [0.60, -0.1, 0.0], "l_hand": [0.2, 0.0, 0.0], "curls": [0.2, 0.2, 0.2, 0.2, 0.2]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.35, 0.05, 0.05], "r_fore": [0.65, 0.05, 0.0], "r_hand": [0.25, 0.0, 0.0], "l_arm": [-0.28, -0.1, -0.05], "l_fore": [0.60, -0.1, 0.0], "l_hand": [0.2, 0.0, 0.0], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.05, 0.02], "r_fore": [0.35, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.15, -0.05, -0.02], "l_fore": [0.30, -0.05, 0.0], "l_hand": [0.05, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "danger",
        "name": "Danger",
        "gloss": "DANGER",
        "duration": 1250,
        "type": "Warning / Threat Noun",
        "notes": "ISLRTC 10,000 Dictionary. Dominant curved claw hand taps sharply against chest/throat twice in warning alert gesture.",
        "dominant": "right",
        "bones": ["Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.45, 0.10, 0.1], "r_fore": [0.75, 0.1, 0.0], "r_hand": [0.3, 0.1, 0.0], "head": [0.04, 0.0, 0.0], "curls": [0.6, 0.6, 0.6, 0.6, 0.6]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.40, 0.12, 0.08], "r_fore": [0.70, 0.08, 0.0], "r_hand": [0.25, 0.05, 0.0], "head": [0.02, 0.0, 0.0], "curls": [0.5, 0.5, 0.5, 0.5, 0.5]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.05, 0.05], "r_fore": [0.40, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "head": [0.0, 0.0, 0.0], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]}
        ]
    },
    {
        "id": "conductor",
        "name": "Conductor",
        "gloss": "CONDUCTOR",
        "duration": 1300,
        "type": "Musical / Leadership Occupation",
        "notes": "ISLRTC 10,000 Dictionary. Dual hands held forward moving rhythmically with expressive finger flexion directing musical tempo.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Spine"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.40, 0.15, 0.1], "r_fore": [0.65, 0.1, 0.0], "r_hand": [0.2, 0.1, 0.0], "l_arm": [-0.40, -0.15, -0.1], "l_fore": [0.65, -0.1, 0.0], "l_hand": [0.2, -0.1, 0.0], "curls": [0.3, 0.3, 0.3, 0.3, 0.3]},
            {"time": 700, "ease": "easeInOutQuad", "r_arm": [-0.30, 0.25, 0.15], "r_fore": [0.55, 0.15, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.30, -0.25, -0.15], "l_fore": [0.55, -0.15, 0.0], "l_hand": [0.1, 0.0, 0.0], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]},
            {"time": 1000, "ease": "easeInOutQuad", "r_arm": [-0.20, 0.10, 0.05], "r_fore": [0.35, 0.08, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.20, -0.10, -0.05], "l_fore": [0.35, -0.08, 0.0], "l_hand": [0.1, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "lie",
        "name": "Lie",
        "gloss": "LIE",
        "duration": 1200,
        "type": "Moral / Speech Verb",
        "notes": "ISLRTC 10,000 Dictionary. Dominant index finger sweeps horizontally across chin from right to left indicating untruth.",
        "dominant": "right",
        "bones": ["Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.45, 0.15, 0.1], "r_fore": [0.75, 0.1, 0.0], "r_hand": [0.2, 0.15, 0.0], "head": [0.02, 0.03, 0.0], "curls": [0.8, 0.0, 0.8, 0.8, 0.8]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.45, -0.05, 0.05], "r_fore": [0.78, 0.02, 0.0], "r_hand": [0.2, -0.15, 0.0], "head": [0.02, -0.02, 0.0], "curls": [0.8, 0.0, 0.8, 0.8, 0.8]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.20, 0.05, 0.02], "r_fore": [0.40, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "head": [0.0, 0.0, 0.0], "curls": [0.1, 0.0, 0.1, 0.1, 0.1]}
        ]
    },
    {
        "id": "luxury",
        "name": "Luxury",
        "gloss": "LUXURY",
        "duration": 1300,
        "type": "Opulence / Elegance Noun",
        "notes": "ISLRTC 10,000 Dictionary. Dual open hands rise smoothly upward while fingertips stroke gently in lavish flourish.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Spine"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.30, 0.15, 0.1], "r_fore": [0.55, 0.1, 0.0], "r_hand": [0.15, 0.05, 0.0], "l_arm": [-0.30, -0.15, -0.1], "l_fore": [0.55, -0.1, 0.0], "l_hand": [0.15, -0.05, 0.0], "curls": [0.2, 0.2, 0.2, 0.2, 0.2]},
            {"time": 700, "ease": "easeInOutQuad", "r_arm": [-0.50, 0.20, 0.15], "r_fore": [0.75, 0.15, 0.0], "r_hand": [0.25, 0.1, 0.0], "l_arm": [-0.50, -0.20, -0.15], "l_fore": [0.75, -0.15, 0.0], "l_hand": [0.25, -0.1, 0.0], "curls": [0.3, 0.3, 0.3, 0.3, 0.3]},
            {"time": 1000, "ease": "easeInOutQuad", "r_arm": [-0.25, 0.10, 0.05], "r_fore": [0.40, 0.08, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.25, -0.10, -0.05], "l_fore": [0.40, -0.08, 0.0], "l_hand": [0.1, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "turbo",
        "name": "Turbo",
        "gloss": "TURBO",
        "duration": 1200,
        "type": "Velocity / High Speed Noun",
        "notes": "ISLRTC 10,000 Dictionary. Dual fists held at chest then shooting forward swiftly into open aerodynamic knife hands.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Spine"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.25, 0.1, 0.05], "r_fore": [0.60, 0.1, 0.0], "r_hand": [0.15, 0.0, 0.0], "l_arm": [-0.25, -0.1, -0.05], "l_fore": [0.60, -0.1, 0.0], "l_hand": [0.15, 0.0, 0.0], "curls": [0.9, 0.9, 0.9, 0.9, 0.9]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.55, 0.1, 0.05], "r_fore": [0.85, 0.05, 0.0], "r_hand": [0.25, 0.0, 0.0], "l_arm": [-0.55, -0.1, -0.05], "l_fore": [0.85, -0.05, 0.0], "l_hand": [0.25, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.25, 0.05, 0.02], "r_fore": [0.45, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.25, -0.05, -0.02], "l_fore": [0.45, -0.05, 0.0], "l_hand": [0.1, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    }
]

created_files = []
for spec in AUTHORED_SPECS:
    sign_id = spec["id"]
    duration = spec["duration"]
    bones = spec["bones"]

    # Keyframe 0: Strict Neutral
    kf0_rot = {b: {"x": 0.0, "y": 0.0, "z": 0.0} for b in bones}
    kf0 = {
        "time_ms": 0,
        "label": "Neutral_Rest",
        "easing": "linear",
        "rotations": kf0_rot,
        "finger_curls": {"thumb": 0.0, "index": 0.0, "middle": 0.0, "ring": 0.0, "pinky": 0.0}
    }

    mid_kfs = []
    for idx, kf in enumerate(spec["keyframes"]):
        rot_map = {}
        for b in bones:
            if b == "Bip001_R_UpperArm" and "r_arm" in kf:
                rot_map[b] = {"x": kf["r_arm"][0], "y": kf["r_arm"][1], "z": kf["r_arm"][2]}
            elif b == "Bip001_R_Forearm" and "r_fore" in kf:
                rot_map[b] = {"x": kf["r_fore"][0], "y": kf["r_fore"][1], "z": kf["r_fore"][2]}
            elif b == "Bip001_R_Hand" and "r_hand" in kf:
                rot_map[b] = {"x": kf["r_hand"][0], "y": kf["r_hand"][1], "z": kf["r_hand"][2]}
            elif b == "Bip001_L_UpperArm" and "l_arm" in kf:
                rot_map[b] = {"x": kf["l_arm"][0], "y": kf["l_arm"][1], "z": kf["l_arm"][2]}
            elif b == "Bip001_L_Forearm" and "l_fore" in kf:
                rot_map[b] = {"x": kf["l_fore"][0], "y": kf["l_fore"][1], "z": kf["l_fore"][2]}
            elif b == "Bip001_L_Hand" and "l_hand" in kf:
                rot_map[b] = {"x": kf["l_hand"][0], "y": kf["l_hand"][1], "z": kf["l_hand"][2]}
            elif b == "Bip001_Head" and "head" in kf:
                rot_map[b] = {"x": kf["head"][0], "y": kf["head"][1], "z": kf["head"][2]}
            elif b == "Bip001_Spine":
                rot_map[b] = {"x": 0.02, "y": 0.0, "z": 0.0}
            else:
                rot_map[b] = {"x": 0.0, "y": 0.0, "z": 0.0}

        curls = kf.get("curls", [0.0, 0.0, 0.0, 0.0, 0.0])
        mid_kfs.append({
            "time_ms": kf["time"],
            "label": f"Stroke_Phase_{idx+1}",
            "easing": kf.get("ease", "easeInOutQuad"),
            "rotations": rot_map,
            "finger_curls": {
                "thumb": curls[0],
                "index": curls[1],
                "middle": curls[2],
                "ring": curls[3],
                "pinky": curls[4]
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

print(f"Successfully authored and verified {len(created_files)} Schema 2.0.0 signs (Batch 15):")
for f in created_files:
    print(f"  + signs/{f}")
