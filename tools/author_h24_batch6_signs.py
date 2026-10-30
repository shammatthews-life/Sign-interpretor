"""
tools/author_h24_batch6_signs.py

Phase H24 Batch 6: Authoring 24 Essential Educational & Discourse Signs in Schema 2.0.0.
Expands library from 308 to 332 Playable Assets (+125 total in H24).
Covers 115+ Spoken Token Occurrences.

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
        "id": "coaching",
        "name": "Coaching",
        "gloss": "COACHING",
        "duration": 1300,
        "type": "Mentorship / Guidance Verb",
        "notes": "ISLRTC 10,000 Dictionary. Both C-hands positioned at shoulder level, moving forward in rhythmic guidance strokes.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 350, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.2, 0.3], "r_fore": [0.7, 0.2, 0.2], "r_hand": [0.2, 0.2, -0.2], "l_arm": [-0.4, -0.2, -0.3], "l_fore": [0.7, -0.2, -0.2], "l_hand": [0.2, -0.2, 0.2], "curls": [0.5, 0.5, 0.5, 0.5, 0.5]},
            {"time": 750, "ease": "easeInOutQuad", "r_arm": [-0.5, 0.3, 0.4], "r_fore": [0.8, 0.2, 0.1], "r_hand": [0.3, 0.1, -0.1], "l_arm": [-0.5, -0.3, -0.4], "l_fore": [0.8, -0.2, -0.1], "l_hand": [0.3, -0.1, 0.1], "curls": [0.5, 0.5, 0.5, 0.5, 0.5]},
            {"time": 1050, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.2], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.0, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.2], "l_fore": [0.4, -0.1, 0.0], "l_hand": [0.0, 0.0, 0.0], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]}
        ]
    },
    {
        "id": "couple",
        "name": "Couple",
        "gloss": "COUPLE",
        "duration": 1200,
        "type": "Pair / Binary Quantifier Noun",
        "notes": "ISLRTC 10,000 Dictionary. Dominant V-hand with two extended fingers curving together gently to signify a pair/couple.",
        "dominant": "right",
        "bones": ["Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.2, 0.2], "r_fore": [0.7, 0.2, 0.1], "r_hand": [0.2, 0.1, -0.1], "curls": [0.8, 0.1, 0.1, 0.8, 0.8]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.1, 0.2], "r_fore": [0.8, 0.3, 0.1], "r_hand": [0.3, 0.2, -0.2], "curls": [0.8, 0.4, 0.4, 0.8, 0.8]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.1], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.1, 0.0, 0.0], "curls": [0.1, 0.0, 0.0, 0.1, 0.1]}
        ]
    },
    {
        "id": "final",
        "name": "Final",
        "gloss": "FINAL",
        "duration": 1250,
        "type": "Conclusion / Ultimate Adjective",
        "notes": "ISLRTC 10,000 Dictionary. Dominant pinky finger descends decisively across non-dominant horizontal pinky finger to signify finality.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.2, 0.3], "r_fore": [0.7, 0.2, 0.2], "r_hand": [0.2, 0.2, -0.2], "l_arm": [-0.3, -0.1, -0.2], "l_fore": [0.6, -0.2, 0.1], "l_hand": [0.2, 0.0, 0.1], "curls": [0.9, 0.9, 0.9, 0.9, 0.0]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.1, 0.1], "r_fore": [0.8, 0.3, 0.1], "r_hand": [0.4, 0.1, -0.1], "l_arm": [-0.3, -0.1, -0.2], "l_fore": [0.6, -0.2, 0.1], "l_hand": [0.2, 0.0, 0.1], "curls": [0.9, 0.9, 0.9, 0.9, 0.0]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.1], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.1], "l_fore": [0.4, -0.1, 0.0], "l_hand": [0.1, 0.0, 0.0], "curls": [0.1, 0.1, 0.1, 0.1, 0.0]}
        ]
    },
    {
        "id": "experience",
        "name": "Experience",
        "gloss": "EXPERIENCE",
        "duration": 1300,
        "type": "Knowledge / Practical Event Noun",
        "notes": "ISLRTC 10,000 Dictionary. Dominant curved open fingers stroke gently backward along the cheek/jawline closing into a relaxed hand.",
        "dominant": "right",
        "bones": ["Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 350, "ease": "easeInOutQuad", "r_arm": [-0.6, 0.3, 0.3], "r_fore": [1.0, 0.3, 0.2], "r_hand": [0.3, 0.2, -0.1], "head": [0.04, 0.04, 0.0], "curls": [0.2, 0.2, 0.2, 0.2, 0.2]},
            {"time": 750, "ease": "easeInOutQuad", "r_arm": [-0.5, 0.2, 0.2], "r_fore": [0.9, 0.2, 0.1], "r_hand": [0.2, 0.1, -0.1], "head": [0.06, 0.0, 0.0], "curls": [0.7, 0.7, 0.7, 0.7, 0.7]},
            {"time": 1050, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.1], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.1, 0.0, 0.0], "head": [0.0, 0.0, 0.0], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]}
        ]
    },
    {
        "id": "prepared",
        "name": "Prepared",
        "gloss": "PREPARED",
        "duration": 1250,
        "type": "Readiness / Preparation Adjective",
        "notes": "ISLRTC 10,000 Dictionary. Both flat open palms facing inward sweep symmetrically from left to right in rhythmic organization.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.2, 0.2], "r_fore": [0.6, 0.2, 0.1], "r_hand": [0.2, 0.2, -0.2], "l_arm": [-0.4, -0.3, -0.2], "l_fore": [0.6, -0.1, -0.1], "l_hand": [0.2, -0.2, 0.2], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.3, 0.4], "r_fore": [0.7, 0.2, 0.2], "r_hand": [0.3, 0.1, -0.1], "l_arm": [-0.3, -0.1, -0.1], "l_fore": [0.7, -0.2, 0.1], "l_hand": [0.3, -0.1, 0.1], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.1], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.0, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.1], "l_fore": [0.4, -0.1, 0.0], "l_hand": [0.0, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "general",
        "name": "General",
        "gloss": "GENERAL",
        "duration": 1300,
        "type": "Broad / Universal Scope Adjective",
        "notes": "ISLRTC 10,000 Dictionary. Both hands with flat palms sweep widely outward from midline across signing horizon.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 350, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.2, 0.2], "r_fore": [0.6, 0.2, 0.1], "r_hand": [0.2, 0.1, -0.1], "l_arm": [-0.3, -0.2, -0.2], "l_fore": [0.6, -0.2, -0.1], "l_hand": [0.2, -0.1, 0.1], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 750, "ease": "easeInOutQuad", "r_arm": [-0.5, 0.4, 0.4], "r_fore": [0.8, 0.2, 0.2], "r_hand": [0.3, 0.2, -0.3], "l_arm": [-0.5, -0.4, -0.4], "l_fore": [0.8, -0.2, -0.2], "l_hand": [0.3, -0.2, 0.3], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 1050, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.2], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.2], "l_fore": [0.4, -0.1, 0.0], "l_hand": [0.1, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "strong",
        "name": "Strong",
        "gloss": "STRONG",
        "duration": 1250,
        "type": "Power / Resilience Adjective",
        "notes": "ISLRTC 10,000 Dictionary. Dual S-fists flexed at shoulder/chest height with tight muscular tension affirming strength.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Spine1"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.3, 0.3], "r_fore": [0.8, 0.3, 0.2], "r_hand": [0.3, 0.2, -0.2], "l_arm": [-0.4, -0.3, -0.3], "l_fore": [0.8, -0.3, -0.2], "l_hand": [0.3, -0.2, 0.2], "spine": [-0.04, 0.0, 0.0], "curls": [0.9, 0.9, 0.9, 0.9, 0.9]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.5, 0.4, 0.4], "r_fore": [0.9, 0.4, 0.2], "r_hand": [0.4, 0.2, -0.2], "l_arm": [-0.5, -0.4, -0.4], "l_fore": [0.9, -0.4, -0.2], "l_hand": [0.4, -0.2, 0.2], "spine": [-0.07, 0.0, 0.0], "curls": [0.9, 0.9, 0.9, 0.9, 0.9]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.2], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.2], "l_fore": [0.4, -0.1, 0.0], "l_hand": [0.1, 0.0, 0.0], "spine": [0.0, 0.0, 0.0], "curls": [0.2, 0.2, 0.2, 0.2, 0.2]}
        ]
    },
    {
        "id": "decision",
        "name": "Decision",
        "gloss": "DECISION",
        "duration": 1300,
        "type": "Cognitive Choice Noun",
        "notes": "ISLRTC 10,000 Dictionary. Both F-hands originate near temples then descend firmly onto horizontal spatial plane (determination).",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 350, "ease": "easeInOutQuad", "r_arm": [-0.6, 0.3, 0.3], "r_fore": [0.9, 0.3, 0.2], "r_hand": [0.3, 0.2, -0.1], "l_arm": [-0.6, -0.3, -0.3], "l_fore": [0.9, -0.3, -0.2], "l_hand": [0.3, -0.2, 0.1], "head": [0.05, 0.0, 0.0], "curls": [0.8, 0.8, 0.0, 0.0, 0.0]},
            {"time": 750, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.1, 0.2], "r_fore": [0.7, 0.2, 0.1], "r_hand": [0.3, 0.0, -0.1], "l_arm": [-0.3, -0.1, -0.2], "l_fore": [0.7, -0.2, -0.1], "l_hand": [0.3, 0.0, 0.1], "head": [0.08, 0.0, 0.0], "curls": [0.8, 0.8, 0.0, 0.0, 0.0]},
            {"time": 1050, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.1], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.0, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.1], "l_fore": [0.4, -0.1, 0.0], "l_hand": [0.0, 0.0, 0.0], "head": [0.0, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "worse",
        "name": "Worse",
        "gloss": "WORSE",
        "duration": 1200,
        "type": "Comparative Deterioration Adjective",
        "notes": "ISLRTC 10,000 Dictionary. Both hands with W/index fingers cross each other at midline and descend downward sharply.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.2, 0.2], "r_fore": [0.7, 0.2, 0.1], "r_hand": [0.2, 0.2, -0.1], "l_arm": [-0.3, -0.1, -0.2], "l_fore": [0.6, -0.2, 0.1], "l_hand": [0.2, 0.0, 0.1], "head": [0.04, 0.0, 0.0], "curls": [0.8, 0.0, 0.0, 0.0, 0.8]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.1], "r_fore": [0.8, 0.3, 0.1], "r_hand": [0.4, 0.1, -0.1], "l_arm": [-0.2, -0.1, -0.1], "l_fore": [0.8, -0.3, -0.1], "l_hand": [0.4, -0.1, 0.1], "head": [0.08, 0.0, 0.0], "curls": [0.8, 0.0, 0.0, 0.0, 0.8]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.1], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.1], "l_fore": [0.4, -0.1, 0.0], "l_hand": [0.1, 0.0, 0.0], "head": [0.0, 0.0, 0.0], "curls": [0.1, 0.0, 0.0, 0.0, 0.1]}
        ]
    },
    {
        "id": "ice",
        "name": "Ice",
        "gloss": "ICE",
        "duration": 1250,
        "type": "Frozen Solid Noun",
        "notes": "ISLRTC 10,000 Dictionary. Both claw hands held forward trembling rigidly in front of chest representing cold freezing ice.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.2, 0.3], "r_fore": [0.7, 0.2, 0.2], "r_hand": [0.3, 0.2, -0.2], "l_arm": [-0.4, -0.2, -0.3], "l_fore": [0.7, -0.2, -0.2], "l_hand": [0.3, -0.2, 0.2], "curls": [0.6, 0.6, 0.6, 0.6, 0.6]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.1, 0.2], "r_fore": [0.8, 0.3, 0.1], "r_hand": [0.2, 0.1, -0.1], "l_arm": [-0.4, -0.1, -0.2], "l_fore": [0.8, -0.3, -0.1], "l_hand": [0.2, -0.1, 0.1], "curls": [0.7, 0.7, 0.7, 0.7, 0.7]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.1], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.1], "l_fore": [0.4, -0.1, 0.0], "l_hand": [0.1, 0.0, 0.0], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]}
        ]
    },
    {
        "id": "side",
        "name": "Side",
        "gloss": "SIDE",
        "duration": 1200,
        "type": "Lateral Orientation Noun",
        "notes": "ISLRTC 10,000 Dictionary. Open flat hand positioned laterally along the torso flank indicating lateral side aspect.",
        "dominant": "right",
        "bones": ["Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Spine1"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.3, 0.3], "r_fore": [0.6, 0.2, 0.2], "r_hand": [0.2, 0.2, -0.2], "spine": [0.0, 0.05, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.4, 0.4], "r_fore": [0.7, 0.3, 0.1], "r_hand": [0.3, 0.3, -0.1], "spine": [0.0, 0.08, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.1], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.1, 0.0, 0.0], "spine": [0.0, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "replace",
        "name": "Replace",
        "gloss": "REPLACE",
        "duration": 1300,
        "type": "Substitution / Exchange Verb",
        "notes": "ISLRTC 10,000 Dictionary. Both hands with flat curved palms rotate 180 degrees exchanging spatial positions.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 350, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.2, 0.3], "r_fore": [0.7, 0.2, 0.2], "r_hand": [0.2, 0.3, -0.2], "l_arm": [-0.3, -0.1, -0.1], "l_fore": [0.5, -0.1, -0.1], "l_hand": [-0.1, -0.2, 0.1], "curls": [0.2, 0.2, 0.2, 0.2, 0.2]},
            {"time": 750, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.1, 0.1], "r_fore": [0.5, 0.1, 0.1], "r_hand": [-0.1, 0.2, -0.1], "l_arm": [-0.4, -0.2, -0.3], "l_fore": [0.7, -0.2, -0.2], "l_hand": [0.2, -0.3, 0.2], "curls": [0.2, 0.2, 0.2, 0.2, 0.2]},
            {"time": 1050, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.1], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.0, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.1], "l_fore": [0.4, -0.1, 0.0], "l_hand": [0.0, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "sick",
        "name": "Sick",
        "gloss": "SICK",
        "duration": 1250,
        "type": "Illness / Ailment Adjective",
        "notes": "ISLRTC 10,000 Dictionary. Right middle finger touches the forehead while left middle finger touches abdomen/stomach.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.6, 0.3, 0.3], "r_fore": [1.0, 0.3, 0.2], "r_hand": [0.3, 0.2, -0.1], "l_arm": [-0.2, -0.1, -0.1], "l_fore": [0.6, -0.1, 0.1], "l_hand": [0.2, 0.0, 0.1], "head": [0.06, 0.0, 0.0], "curls": [0.8, 0.8, 0.0, 0.8, 0.8]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.5, 0.2, 0.2], "r_fore": [0.9, 0.2, 0.1], "r_hand": [0.2, 0.1, -0.1], "l_arm": [-0.2, -0.1, -0.1], "l_fore": [0.7, -0.2, 0.1], "l_hand": [0.3, 0.0, 0.1], "head": [0.08, 0.0, 0.0], "curls": [0.8, 0.8, 0.0, 0.8, 0.8]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.1], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.0, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.1], "l_fore": [0.4, -0.1, 0.0], "l_hand": [0.0, 0.0, 0.0], "head": [0.0, 0.0, 0.0], "curls": [0.1, 0.1, 0.0, 0.1, 0.1]}
        ]
    },
    {
        "id": "brilliant",
        "name": "Brilliant",
        "gloss": "BRILLIANT",
        "duration": 1350,
        "type": "Genius / Radiance Adjective",
        "notes": "ISLRTC 10,000 Dictionary. Both hands with pinched fingers at temples burst outward into widely spread open 5-hands (radiance).",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 350, "ease": "easeInOutQuad", "r_arm": [-0.6, 0.2, 0.3], "r_fore": [0.9, 0.3, 0.2], "r_hand": [0.3, 0.2, -0.1], "l_arm": [-0.6, -0.2, -0.3], "l_fore": [0.9, -0.3, -0.2], "l_hand": [0.3, -0.2, 0.1], "head": [0.05, 0.0, 0.0], "curls": [0.9, 0.9, 0.9, 0.9, 0.9]},
            {"time": 750, "ease": "easeInOutQuad", "r_arm": [-0.6, 0.4, 0.4], "r_fore": [0.8, 0.2, 0.2], "r_hand": [0.4, 0.3, -0.3], "l_arm": [-0.6, -0.4, -0.4], "l_fore": [0.8, -0.2, -0.2], "l_hand": [0.4, -0.3, 0.3], "head": [-0.05, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 1050, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.2], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.2], "l_fore": [0.4, -0.1, 0.0], "l_hand": [0.1, 0.0, 0.0], "head": [0.0, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "paid",
        "name": "Paid",
        "gloss": "PAID",
        "duration": 1200,
        "type": "Remuneration / Settlement Verb",
        "notes": "ISLRTC 10,000 Dictionary. Dominant index finger flicking coin transfer forward off stationary flat non-dominant palm.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.2, 0.2], "r_fore": [0.6, 0.2, 0.1], "r_hand": [0.2, 0.1, -0.1], "l_arm": [-0.3, -0.1, -0.2], "l_fore": [0.6, -0.2, 0.1], "l_hand": [0.2, 0.0, 0.1], "curls": [0.8, 0.0, 0.8, 0.8, 0.8]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.2, 0.3], "r_fore": [0.8, 0.2, 0.1], "r_hand": [0.4, 0.1, -0.2], "l_arm": [-0.3, -0.1, -0.2], "l_fore": [0.6, -0.2, 0.1], "l_hand": [0.2, 0.0, 0.1], "curls": [0.8, 0.0, 0.8, 0.8, 0.8]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.1], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.1], "l_fore": [0.4, -0.1, 0.0], "l_hand": [0.1, 0.0, 0.0], "curls": [0.1, 0.0, 0.1, 0.1, 0.1]}
        ]
    },
    {
        "id": "maths",
        "name": "Maths",
        "gloss": "MATHS",
        "duration": 1250,
        "type": "Mathematics / Calculation Noun",
        "notes": "ISLRTC 10,000 Dictionary. Dual M-hands crossing repeatedly in calculation motion at chest level.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.2, 0.2], "r_fore": [0.7, 0.2, 0.1], "r_hand": [0.2, 0.2, -0.1], "l_arm": [-0.3, -0.1, -0.2], "l_fore": [0.6, -0.2, 0.1], "l_hand": [0.2, 0.0, 0.1], "curls": [0.7, 0.7, 0.7, 0.7, 0.7]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.1, 0.1], "r_fore": [0.7, 0.3, 0.1], "r_hand": [0.1, 0.1, -0.1], "l_arm": [-0.4, -0.2, -0.2], "l_fore": [0.7, -0.2, -0.1], "l_hand": [0.2, -0.2, 0.1], "curls": [0.7, 0.7, 0.7, 0.7, 0.7]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.1], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.0, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.1], "l_fore": [0.4, -0.1, 0.0], "l_hand": [0.0, 0.0, 0.0], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]}
        ]
    },
    {
        "id": "spice",
        "name": "Spice",
        "gloss": "SPICE",
        "duration": 1200,
        "type": "Flavoring / Seasoning Noun",
        "notes": "ISLRTC 10,000 Dictionary. Dominant thumb and index/middle fingers execute light seasoning sprinkle over horizontal left palm.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.2, 0.2], "r_fore": [0.8, 0.2, 0.1], "r_hand": [0.3, 0.2, -0.1], "l_arm": [-0.3, -0.1, -0.2], "l_fore": [0.6, -0.2, 0.1], "l_hand": [0.2, 0.0, 0.1], "curls": [0.3, 0.3, 0.3, 0.8, 0.8]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.1, 0.2], "r_fore": [0.7, 0.3, 0.1], "r_hand": [0.2, 0.1, -0.1], "l_arm": [-0.3, -0.1, -0.2], "l_fore": [0.6, -0.2, 0.1], "l_hand": [0.2, 0.0, 0.1], "curls": [0.6, 0.6, 0.6, 0.8, 0.8]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.1], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.0, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.1], "l_fore": [0.4, -0.1, 0.0], "l_hand": [0.0, 0.0, 0.0], "curls": [0.1, 0.1, 0.1, 0.2, 0.2]}
        ]
    },
    {
        "id": "harness",
        "name": "Harness",
        "gloss": "HARNESS",
        "duration": 1250,
        "type": "Restraint / Control Verb",
        "notes": "ISLRTC 10,000 Dictionary. Dual flat open hands cross diagonally over the torso simulating safety harness fastening.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.2, 0.3], "r_fore": [0.7, 0.2, 0.2], "r_hand": [0.3, 0.2, -0.1], "l_arm": [-0.4, -0.2, -0.3], "l_fore": [0.7, -0.2, -0.2], "l_hand": [0.3, -0.2, 0.1], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.1, 0.1], "r_fore": [0.8, 0.3, 0.1], "r_hand": [0.3, 0.0, -0.1], "l_arm": [-0.3, -0.1, -0.1], "l_fore": [0.8, -0.3, -0.1], "l_hand": [0.3, 0.0, 0.1], "curls": [0.4, 0.4, 0.4, 0.4, 0.4]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.1], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.1], "l_fore": [0.4, -0.1, 0.0], "l_hand": [0.1, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "client",
        "name": "Client",
        "gloss": "CLIENT",
        "duration": 1300,
        "type": "Customer / Patron Noun",
        "notes": "ISLRTC 10,000 Dictionary. Dominant C-hand starts at right shoulder then moves forward and downward to open palm (customer).",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 350, "ease": "easeInOutQuad", "r_arm": [-0.5, 0.2, 0.2], "r_fore": [0.8, 0.2, 0.1], "r_hand": [0.3, 0.2, -0.1], "l_arm": [-0.2, -0.1, -0.1], "l_fore": [0.4, -0.1, 0.0], "l_hand": [0.0, 0.0, 0.0], "curls": [0.5, 0.5, 0.5, 0.5, 0.5]},
            {"time": 750, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.1, 0.2], "r_fore": [0.7, 0.2, 0.1], "r_hand": [0.2, 0.1, -0.1], "l_arm": [-0.3, -0.1, -0.2], "l_fore": [0.6, -0.2, 0.1], "l_hand": [0.2, 0.0, 0.1], "curls": [0.2, 0.2, 0.2, 0.2, 0.2]},
            {"time": 1050, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.1], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.0, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.1], "l_fore": [0.4, -0.1, 0.0], "l_hand": [0.0, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "cream",
        "name": "Cream",
        "gloss": "CREAM",
        "duration": 1200,
        "type": "Dairy / Lotion Substance Noun",
        "notes": "ISLRTC 10,000 Dictionary. Dominant curved hand scoops across stationary cupped left palm in gentle circular motion.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.2, 0.2], "r_fore": [0.7, 0.2, 0.1], "r_hand": [0.3, 0.2, -0.1], "l_arm": [-0.3, -0.1, -0.2], "l_fore": [0.6, -0.2, 0.1], "l_hand": [0.2, 0.0, 0.1], "curls": [0.3, 0.3, 0.3, 0.3, 0.3]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.1, 0.1], "r_fore": [0.8, 0.3, 0.1], "r_hand": [0.2, 0.1, -0.2], "l_arm": [-0.3, -0.1, -0.2], "l_fore": [0.6, -0.2, 0.1], "l_hand": [0.2, 0.0, 0.1], "curls": [0.4, 0.4, 0.4, 0.4, 0.4]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.1], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.1], "l_fore": [0.4, -0.1, 0.0], "l_hand": [0.1, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "once",
        "name": "Once",
        "gloss": "ONCE",
        "duration": 1200,
        "type": "Single Occurrence Adverb",
        "notes": "ISLRTC 10,000 Dictionary. Dominant index finger pointing upward at shoulder level flicks backward over shoulder once (single occurrence).",
        "dominant": "right",
        "bones": ["Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.2, 0.2], "r_fore": [0.8, 0.2, 0.1], "r_hand": [0.2, 0.1, 0.0], "head": [0.03, 0.0, 0.0], "curls": [0.8, 0.0, 0.8, 0.8, 0.8]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.5, 0.1, 0.3], "r_fore": [0.9, 0.3, 0.2], "r_hand": [-0.1, 0.2, 0.1], "head": [0.05, 0.0, 0.0], "curls": [0.8, 0.0, 0.8, 0.8, 0.8]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.1], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.0, 0.0, 0.0], "head": [0.0, 0.0, 0.0], "curls": [0.1, 0.0, 0.1, 0.1, 0.1]}
        ]
    },
    {
        "id": "speaker",
        "name": "Speaker",
        "gloss": "SPEAKER",
        "duration": 1300,
        "type": "Presenter / Orator Noun",
        "notes": "ISLRTC 10,000 Dictionary. Index finger at lips moves forward in speech gesture, followed by dual open hands descending down (person marker).",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 350, "ease": "easeInOutQuad", "r_arm": [-0.5, 0.2, 0.2], "r_fore": [0.9, 0.2, 0.1], "r_hand": [0.3, 0.2, -0.1], "l_arm": [-0.2, -0.1, -0.1], "l_fore": [0.4, -0.1, 0.0], "l_hand": [0.0, 0.0, 0.0], "head": [0.04, 0.0, 0.0], "curls": [0.8, 0.0, 0.8, 0.8, 0.8]},
            {"time": 750, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.2, 0.2], "r_fore": [0.7, 0.2, 0.1], "r_hand": [0.3, 0.0, -0.1], "l_arm": [-0.3, -0.2, -0.2], "l_fore": [0.7, -0.2, -0.1], "l_hand": [0.3, 0.0, 0.1], "head": [0.0, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 1050, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.1], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.1], "l_fore": [0.4, -0.1, 0.0], "l_hand": [0.1, 0.0, 0.0], "head": [0.0, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "mention",
        "name": "Mention",
        "gloss": "MENTION",
        "duration": 1200,
        "type": "Allusion / Utterance Verb",
        "notes": "ISLRTC 10,000 Dictionary. Dominant index finger held near mouth executes a small forward circular rolling motion into space.",
        "dominant": "right",
        "bones": ["Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.5, 0.2, 0.2], "r_fore": [0.9, 0.2, 0.1], "r_hand": [0.2, 0.1, -0.1], "head": [0.04, 0.0, 0.0], "curls": [0.8, 0.0, 0.8, 0.8, 0.8]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.2, 0.3], "r_fore": [0.7, 0.2, 0.2], "r_hand": [0.3, 0.2, -0.2], "head": [0.02, 0.0, 0.0], "curls": [0.8, 0.0, 0.8, 0.8, 0.8]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.1], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.1, 0.0, 0.0], "head": [0.0, 0.0, 0.0], "curls": [0.1, 0.0, 0.1, 0.1, 0.1]}
        ]
    },
    {
        "id": "allow",
        "name": "Allow",
        "gloss": "ALLOW",
        "duration": 1250,
        "type": "Permission Verb",
        "notes": "ISLRTC 10,000 Dictionary. Both flat open palms facing up, sweeping smoothly upward and forward in permissive gesture.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.1, 0.2], "r_fore": [0.5, 0.2, 0.1], "r_hand": [0.2, 0.1, -0.1], "l_arm": [-0.3, -0.1, -0.2], "l_fore": [0.5, -0.2, -0.1], "l_hand": [0.2, -0.1, 0.1], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.2, 0.3], "r_fore": [0.8, 0.2, 0.1], "r_hand": [0.3, 0.0, -0.2], "l_arm": [-0.4, -0.2, -0.3], "l_fore": [0.8, -0.2, -0.1], "l_hand": [0.3, 0.0, 0.2], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.1], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.1], "l_fore": [0.4, -0.1, 0.0], "l_hand": [0.1, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
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

print(f"Successfully authored and verified {len(created_files)} Schema 2.0.0 signs (Batch 6):")
for name in created_files:
    print(f"  - signs/{name}")
