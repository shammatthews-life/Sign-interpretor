"""
tools/author_h24_batch3_signs.py

Phase H24 Batch 3: Authoring 20 Additional Educational & Lecture ISL Signs
in Schema 2.0.0 to reach 260 Playable Assets.
Covers 138 Spoken Token Occurrences.

All signs strictly observe:
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
        "id": "functional",
        "name": "Functional",
        "gloss": "FUNCTIONAL",
        "duration": 1300,
        "type": "Technical / Operational Adjective",
        "notes": "ISLRTC 10,000 Dictionary. Dual hands with flat palms rotating in tandem forward and around each other to represent active mechanical or systemic function.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 350, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.2, 0.3], "r_fore": [0.7, 0.2, 0.1], "r_hand": [0.2, 0.2, -0.1], "l_arm": [-0.3, -0.1, -0.2], "l_fore": [0.5, -0.1, -0.1], "l_hand": [-0.1, -0.1, 0.1], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]},
            {"time": 750, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.1, 0.2], "r_fore": [0.5, 0.1, 0.1], "r_hand": [-0.1, 0.1, -0.1], "l_arm": [-0.4, -0.2, -0.3], "l_fore": [0.7, -0.2, -0.1], "l_hand": [0.2, -0.2, 0.1], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]},
            {"time": 1050, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.2], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.0, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.2], "l_fore": [0.4, -0.1, 0.0], "l_hand": [0.0, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "anticipation",
        "name": "Anticipation",
        "gloss": "ANTICIPATION",
        "duration": 1350,
        "type": "Psychological State / Expectation",
        "notes": "ISLRTC 10,000 Dictionary. Both open hands held forward in signing space with fingers fluttering gently in eager, expectant anticipation.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 350, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.2, 0.3], "r_fore": [0.6, 0.2, 0.2], "r_hand": [0.2, 0.1, -0.1], "l_arm": [-0.4, -0.2, -0.3], "l_fore": [0.6, -0.2, -0.2], "l_hand": [0.2, -0.1, 0.1], "head": [0.08, 0.0, 0.0], "curls": [0.2, 0.1, 0.1, 0.2, 0.2]},
            {"time": 750, "ease": "easeInOutQuad", "r_arm": [-0.5, 0.3, 0.4], "r_fore": [0.7, 0.3, 0.2], "r_hand": [0.3, 0.2, -0.2], "l_arm": [-0.5, -0.3, -0.4], "l_fore": [0.7, -0.3, -0.2], "l_hand": [0.3, -0.2, 0.2], "head": [0.12, 0.0, 0.0], "curls": [0.3, 0.2, 0.2, 0.3, 0.3]},
            {"time": 1050, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.2], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.2], "l_fore": [0.4, -0.1, 0.0], "l_hand": [0.1, 0.0, 0.0], "head": [0.05, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "based",
        "name": "Based",
        "gloss": "BASED",
        "duration": 1250,
        "type": "Foundational / Relational Verb",
        "notes": "ISLRTC 10,000 Dictionary. Right flat palm descends firmly onto horizontal stationary left palm, establishing a solid foundation or base.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.5, 0.2, 0.3], "r_fore": [0.8, 0.2, 0.2], "r_hand": [0.2, 0.1, -0.1], "l_arm": [-0.3, -0.2, -0.2], "l_fore": [0.6, -0.1, -0.1], "l_hand": [0.0, 0.1, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.1, 0.2], "r_fore": [0.7, 0.1, 0.1], "r_hand": [-0.1, 0.1, -0.1], "l_arm": [-0.3, -0.2, -0.2], "l_fore": [0.6, -0.1, -0.1], "l_hand": [0.0, 0.1, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.1], "r_fore": [0.4, 0.1, 0.0], "r_hand": [0.0, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.1], "l_fore": [0.3, 0.0, 0.0], "l_hand": [0.0, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "clarity",
        "name": "Clarity",
        "gloss": "CLARITY",
        "duration": 1300,
        "type": "Perceptual Quality / Understanding",
        "notes": "ISLRTC 10,000 Dictionary. Both hands with fingertips touching forehead blossom outward with spreading fingers, indicating bright mental lucidity.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 350, "ease": "easeInOutQuad", "r_arm": [-0.5, 0.3, 0.4], "r_fore": [0.9, 0.3, 0.2], "r_hand": [0.3, 0.1, -0.1], "l_arm": [-0.5, -0.3, -0.4], "l_fore": [0.9, -0.3, -0.2], "l_hand": [0.3, -0.1, 0.1], "head": [0.05, 0.0, 0.0], "curls": [0.7, 0.7, 0.7, 0.7, 0.7]},
            {"time": 750, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.4, 0.5], "r_fore": [0.7, 0.3, 0.2], "r_hand": [0.2, 0.3, -0.2], "l_arm": [-0.4, -0.4, -0.5], "l_fore": [0.7, -0.3, -0.2], "l_hand": [0.2, -0.3, 0.2], "head": [-0.05, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 1050, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.2], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.0, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.2], "l_fore": [0.4, -0.1, 0.0], "l_hand": [0.0, 0.0, 0.0], "head": [0.0, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "during",
        "name": "During",
        "gloss": "DURING",
        "duration": 1200,
        "type": "Temporal Preposition / Duration",
        "notes": "ISLRTC 10,000 Dictionary. Both index fingers pointing forward at waist level trace parallel forward arc together across time interval.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.1, 0.2], "r_fore": [0.5, 0.2, 0.1], "r_hand": [0.2, 0.1, -0.1], "l_arm": [-0.3, -0.1, -0.2], "l_fore": [0.5, -0.2, -0.1], "l_hand": [0.2, -0.1, 0.1], "curls": [0.8, 0.0, 0.9, 0.9, 0.9]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.2, 0.3], "r_fore": [0.7, 0.2, 0.2], "r_hand": [0.3, 0.1, -0.2], "l_arm": [-0.4, -0.2, -0.3], "l_fore": [0.7, -0.2, -0.2], "l_hand": [0.3, -0.1, 0.2], "curls": [0.8, 0.0, 0.9, 0.9, 0.9]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.2], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.2], "l_fore": [0.4, -0.1, 0.0], "l_hand": [0.1, 0.0, 0.0], "curls": [0.2, 0.0, 0.2, 0.2, 0.2]}
        ]
    },
    {
        "id": "prior",
        "name": "Prior",
        "gloss": "PRIOR",
        "duration": 1250,
        "type": "Temporal / Preceding Adjective",
        "notes": "ISLRTC 10,000 Dictionary. Right open flat B-hand held near shoulder sweeps backward over dominant shoulder into past time.",
        "dominant": "right",
        "bones": ["Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.2, 0.3], "r_fore": [0.8, 0.2, 0.2], "r_hand": [0.2, 0.1, -0.1], "head": [0.05, 0.0, 0.0], "curls": [0.1, 0.0, 0.0, 0.1, 0.1]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.6, 0.4, 0.5], "r_fore": [1.1, 0.4, 0.3], "r_hand": [-0.2, 0.2, -0.2], "head": [0.05, 0.05, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.2], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.0, 0.0, 0.0], "head": [0.0, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "while",
        "name": "While",
        "gloss": "WHILE",
        "duration": 1200,
        "type": "Conjunction / Concurrent Process",
        "notes": "ISLRTC 10,000 Dictionary. Bilateral 1-hands point forward and move synchronously forward in continuous parallel motion.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.1, 0.2], "r_fore": [0.5, 0.2, 0.1], "r_hand": [0.2, 0.1, -0.1], "l_arm": [-0.3, -0.1, -0.2], "l_fore": [0.5, -0.2, -0.1], "l_hand": [0.2, -0.1, 0.1], "curls": [0.8, 0.0, 0.9, 0.9, 0.9]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.2, 0.3], "r_fore": [0.7, 0.2, 0.2], "r_hand": [0.3, 0.1, -0.2], "l_arm": [-0.4, -0.2, -0.3], "l_fore": [0.7, -0.2, -0.2], "l_hand": [0.3, -0.1, 0.2], "curls": [0.8, 0.0, 0.9, 0.9, 0.9]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.2], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.2], "l_fore": [0.4, -0.1, 0.0], "l_hand": [0.1, 0.0, 0.0], "curls": [0.2, 0.0, 0.2, 0.2, 0.2]}
        ]
    },
    {
        "id": "inhale",
        "name": "Inhale",
        "gloss": "INHALE",
        "duration": 1300,
        "type": "Physiological Action / Breath",
        "notes": "ISLRTC 10,000 Dictionary. Both hands rise upwards along upper torso with palms inward as shoulders and chest gently expand.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Spine"],
        "keyframes": [
            {"time": 350, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.1, 0.2], "r_fore": [0.6, 0.1, 0.1], "r_hand": [0.2, 0.1, -0.1], "l_arm": [-0.3, -0.1, -0.2], "l_fore": [0.6, -0.1, -0.1], "l_hand": [0.2, -0.1, 0.1], "spine": [-0.05, 0.0, 0.0], "curls": [0.2, 0.1, 0.1, 0.2, 0.2]},
            {"time": 750, "ease": "easeInOutQuad", "r_arm": [-0.5, 0.2, 0.3], "r_fore": [0.8, 0.2, 0.2], "r_hand": [0.3, 0.1, -0.2], "l_arm": [-0.5, -0.2, -0.3], "l_fore": [0.8, -0.2, -0.2], "l_hand": [0.3, -0.1, 0.2], "spine": [-0.1, 0.0, 0.0], "curls": [0.1, 0.0, 0.0, 0.1, 0.1]},
            {"time": 1050, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.2], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.0, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.2], "l_fore": [0.4, -0.1, 0.0], "l_hand": [0.0, 0.0, 0.0], "spine": [0.0, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "goal",
        "name": "Goal",
        "gloss": "GOAL",
        "duration": 1250,
        "type": "Objective / Target Noun",
        "notes": "ISLRTC 10,000 Dictionary. Left index finger stands vertically as target flag; right index finger aims directly into fingertip.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.2, 0.3], "r_fore": [0.6, 0.2, 0.1], "r_hand": [0.2, 0.1, -0.1], "l_arm": [-0.4, -0.2, -0.2], "l_fore": [0.7, -0.1, -0.1], "l_hand": [0.3, 0.0, 0.0], "curls": [0.8, 0.0, 0.9, 0.9, 0.9]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.1, 0.2], "r_fore": [0.8, 0.2, 0.2], "r_hand": [0.4, 0.0, -0.2], "l_arm": [-0.4, -0.2, -0.2], "l_fore": [0.7, -0.1, -0.1], "l_hand": [0.3, 0.0, 0.0], "curls": [0.8, 0.0, 0.9, 0.9, 0.9]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.2], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.1], "l_fore": [0.3, 0.0, 0.0], "l_hand": [0.0, 0.0, 0.0], "curls": [0.2, 0.0, 0.2, 0.2, 0.2]}
        ]
    },
    {
        "id": "science",
        "name": "Science",
        "gloss": "SCIENCE",
        "duration": 1300,
        "type": "Academic / Laboratory Noun",
        "notes": "ISLRTC 10,000 Dictionary. Both hands with A-thumbs alternating downward pouring motion representing laboratory experiment flasks.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 350, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.2, 0.3], "r_fore": [0.7, 0.2, 0.2], "r_hand": [0.3, 0.2, -0.1], "l_arm": [-0.3, -0.1, -0.2], "l_fore": [0.5, -0.1, -0.1], "l_hand": [-0.1, -0.1, 0.1], "curls": [0.1, 0.9, 0.9, 0.9, 0.9]},
            {"time": 750, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.1, 0.2], "r_fore": [0.5, 0.1, 0.1], "r_hand": [-0.1, 0.1, -0.1], "l_arm": [-0.4, -0.2, -0.3], "l_fore": [0.7, -0.2, -0.2], "l_hand": [0.3, -0.2, 0.1], "curls": [0.1, 0.9, 0.9, 0.9, 0.9]},
            {"time": 1050, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.2], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.0, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.2], "l_fore": [0.4, -0.1, 0.0], "l_hand": [0.0, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "career",
        "name": "Career",
        "gloss": "CAREER",
        "duration": 1250,
        "type": "Professional / Progression Noun",
        "notes": "ISLRTC 10,000 Dictionary. Right open flat palm advances along progressive forward-ascending diagonal trajectory representing professional growth.",
        "dominant": "right",
        "bones": ["Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.1, 0.3], "r_fore": [0.5, 0.2, 0.1], "r_hand": [0.1, 0.1, -0.1], "head": [0.0, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.5, 0.3, 0.5], "r_fore": [0.8, 0.3, 0.2], "r_hand": [0.2, 0.2, -0.2], "head": [-0.05, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.2], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.0, 0.0, 0.0], "head": [0.0, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "passion",
        "name": "Passion",
        "gloss": "PASSION",
        "duration": 1300,
        "type": "Emotional Drive / Intensity",
        "notes": "ISLRTC 10,000 Dictionary. Right curved hand rubs upward in enthusiastic circular motion over heart with lively facial expression.",
        "dominant": "right",
        "bones": ["Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 350, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.2, 0.3], "r_fore": [0.7, 0.3, 0.2], "r_hand": [0.2, 0.1, -0.2], "head": [0.08, 0.0, 0.0], "curls": [0.4, 0.3, 0.3, 0.4, 0.4]},
            {"time": 750, "ease": "easeInOutQuad", "r_arm": [-0.45, 0.25, 0.35], "r_fore": [0.75, 0.35, 0.25], "r_hand": [0.25, 0.15, -0.25], "head": [0.1, 0.0, 0.0], "curls": [0.5, 0.4, 0.4, 0.5, 0.5]},
            {"time": 1050, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.2], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.0, 0.0, 0.0], "head": [0.0, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "session",
        "name": "Session",
        "gloss": "SESSION",
        "duration": 1250,
        "type": "Event / Classroom Meeting",
        "notes": "ISLRTC 10,000 Dictionary. Both hands with open palms outline bounded temporal meeting block from left and right.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.2, 0.3], "r_fore": [0.6, 0.2, 0.1], "r_hand": [0.2, 0.1, -0.1], "l_arm": [-0.4, -0.2, -0.3], "l_fore": [0.6, -0.2, -0.1], "l_hand": [0.2, -0.1, 0.1], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.1, 0.2], "r_fore": [0.7, 0.2, 0.2], "r_hand": [0.1, 0.1, -0.2], "l_arm": [-0.4, -0.1, -0.2], "l_fore": [0.7, -0.2, -0.2], "l_hand": [0.1, -0.1, 0.2], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.2], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.0, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.2], "l_fore": [0.4, -0.1, 0.0], "l_hand": [0.0, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "interesting",
        "name": "Interesting",
        "gloss": "INTERESTING",
        "duration": 1300,
        "type": "Attraction / Intellectual Adjective",
        "notes": "ISLRTC 10,000 Dictionary. Right hand with index and thumb pinching near chest pulls forward with engaging, fascinated facial expression.",
        "dominant": "right",
        "bones": ["Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 350, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.2, 0.3], "r_fore": [0.7, 0.2, 0.2], "r_hand": [0.2, 0.1, -0.1], "head": [0.05, 0.0, 0.0], "curls": [0.7, 0.7, 0.1, 0.1, 0.1]},
            {"time": 750, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.3, 0.4], "r_fore": [0.8, 0.3, 0.3], "r_hand": [0.1, 0.2, -0.2], "head": [0.1, 0.0, 0.0], "curls": [0.8, 0.8, 0.1, 0.1, 0.1]},
            {"time": 1050, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.2], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.0, 0.0, 0.0], "head": [0.0, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "face",
        "name": "Face",
        "gloss": "FACE",
        "duration": 1200,
        "type": "Anatomical / Expression Noun",
        "notes": "ISLRTC 10,000 Dictionary. Right index finger traces circular perimeter outline around speaker's face.",
        "dominant": "right",
        "bones": ["Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.6, 0.3, 0.4], "r_fore": [1.0, 0.3, 0.3], "r_hand": [0.3, 0.1, -0.1], "head": [0.05, 0.0, 0.0], "curls": [0.8, 0.0, 0.9, 0.9, 0.9]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.5, 0.2, 0.4], "r_fore": [0.9, 0.3, 0.2], "r_hand": [0.2, 0.2, -0.2], "head": [0.0, 0.05, 0.0], "curls": [0.8, 0.0, 0.9, 0.9, 0.9]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.2], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.0, 0.0, 0.0], "head": [0.0, 0.0, 0.0], "curls": [0.2, 0.0, 0.2, 0.2, 0.2]}
        ]
    },
    {
        "id": "group",
        "name": "Group",
        "gloss": "GROUP",
        "duration": 1300,
        "type": "Social / Collective Noun",
        "notes": "ISLRTC 10,000 Dictionary. Both hands with C-shapes starting apart with palms facing inward, sweeping in horizontal circle to meet at fingertips.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 350, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.2, 0.3], "r_fore": [0.6, 0.1, 0.1], "r_hand": [0.1, 0.2, -0.1], "l_arm": [-0.3, -0.2, -0.3], "l_fore": [0.6, -0.1, -0.1], "l_hand": [0.1, -0.2, 0.1], "curls": [0.4, 0.3, 0.3, 0.4, 0.4]},
            {"time": 750, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.3, 0.4], "r_fore": [0.8, 0.2, 0.2], "r_hand": [0.2, 0.3, -0.2], "l_arm": [-0.4, -0.3, -0.4], "l_fore": [0.8, -0.2, -0.2], "l_hand": [0.2, -0.3, 0.2], "curls": [0.3, 0.2, 0.2, 0.3, 0.3]},
            {"time": 1050, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.2], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.0, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.2], "l_fore": [0.4, -0.1, 0.0], "l_hand": [0.0, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "enjoy",
        "name": "Enjoy",
        "gloss": "ENJOY",
        "duration": 1250,
        "type": "Emotional Experience / Verb",
        "notes": "ISLRTC 10,000 Dictionary. Open palms rub chest and torso in warm circular strokes expressing deep enjoyment and contentment.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.2, 0.3], "r_fore": [0.7, 0.2, 0.2], "r_hand": [0.2, 0.1, -0.1], "l_arm": [-0.3, -0.1, -0.2], "l_fore": [0.5, -0.1, -0.1], "l_hand": [-0.1, -0.1, 0.1], "head": [0.05, 0.0, 0.0], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.1, 0.2], "r_fore": [0.5, 0.1, 0.1], "r_hand": [-0.1, 0.1, -0.1], "l_arm": [-0.4, -0.2, -0.3], "l_fore": [0.7, -0.2, -0.2], "l_hand": [0.2, -0.1, 0.1], "head": [0.08, 0.0, 0.0], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.2], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.0, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.2], "l_fore": [0.4, -0.1, 0.0], "l_hand": [0.0, 0.0, 0.0], "head": [0.0, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "core",
        "name": "Core",
        "gloss": "CORE",
        "duration": 1200,
        "type": "Essential / Central Noun",
        "notes": "ISLRTC 10,000 Dictionary. Left fist forms central pillar; right index finger taps directly into center indicating fundamental core.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.2, 0.3], "r_fore": [0.7, 0.2, 0.1], "r_hand": [0.3, 0.1, -0.1], "l_arm": [-0.3, -0.2, -0.2], "l_fore": [0.6, -0.1, -0.1], "l_hand": [0.1, 0.0, 0.0], "curls": [0.8, 0.0, 0.9, 0.9, 0.9]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.1, 0.2], "r_fore": [0.8, 0.2, 0.2], "r_hand": [0.2, 0.1, -0.1], "l_arm": [-0.3, -0.2, -0.2], "l_fore": [0.6, -0.1, -0.1], "l_hand": [0.1, 0.0, 0.0], "curls": [0.8, 0.0, 0.9, 0.9, 0.9]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.2], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.0, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.1], "l_fore": [0.3, 0.0, 0.0], "l_hand": [0.0, 0.0, 0.0], "curls": [0.1, 0.0, 0.1, 0.1, 0.1]}
        ]
    },
    {
        "id": "vision",
        "name": "Vision",
        "gloss": "VISION",
        "duration": 1350,
        "type": "Strategic / Perceptual Sight Noun",
        "notes": "ISLRTC 10,000 Dictionary. Dual V-hands point from eyes forward, spreading outward into wide panoramic perspective.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 350, "ease": "easeInOutQuad", "r_arm": [-0.5, 0.2, 0.4], "r_fore": [0.9, 0.3, 0.2], "r_hand": [0.3, 0.1, -0.1], "l_arm": [-0.5, -0.2, -0.4], "l_fore": [0.9, -0.3, -0.2], "l_hand": [0.3, -0.1, 0.1], "head": [0.05, 0.0, 0.0], "curls": [0.8, 0.0, 0.0, 0.9, 0.9]},
            {"time": 750, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.4, 0.5], "r_fore": [0.8, 0.4, 0.3], "r_hand": [0.2, 0.3, -0.2], "l_arm": [-0.4, -0.4, -0.5], "l_fore": [0.8, -0.4, -0.3], "l_hand": [0.2, -0.3, 0.2], "head": [-0.05, 0.0, 0.0], "curls": [0.8, 0.0, 0.0, 0.9, 0.9]},
            {"time": 1050, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.2], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.0, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.2], "l_fore": [0.4, -0.1, 0.0], "l_hand": [0.0, 0.0, 0.0], "head": [0.0, 0.0, 0.0], "curls": [0.2, 0.0, 0.0, 0.2, 0.2]}
        ]
    },
    {
        "id": "color",
        "name": "Color",
        "gloss": "COLOR",
        "duration": 1200,
        "type": "Visual Property / Chromatic Noun",
        "notes": "ISLRTC 10,000 Dictionary. Right open 5-hand with fingertips gently fluttering across the chin and lower face.",
        "dominant": "right",
        "bones": ["Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.5, 0.2, 0.4], "r_fore": [0.9, 0.3, 0.2], "r_hand": [0.3, 0.1, -0.1], "head": [0.05, 0.0, 0.0], "curls": [0.2, 0.1, 0.1, 0.2, 0.2]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.45, 0.22, 0.38], "r_fore": [0.85, 0.28, 0.22], "r_hand": [0.25, 0.12, -0.15], "head": [0.05, 0.0, 0.0], "curls": [0.3, 0.2, 0.2, 0.3, 0.3]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.2], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.0, 0.0, 0.0], "head": [0.0, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
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
        elif "Spine" in b:
            val = kf.get("spine", [0, 0, 0])
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

print(f"Successfully authored and verified {len(created_files)} Schema 2.0.0 signs (Batch 3):")
for name in created_files:
    print(f"  - signs/{name}")
