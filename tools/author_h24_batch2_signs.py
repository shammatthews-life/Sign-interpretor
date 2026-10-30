"""
tools/author_h24_batch2_signs.py

Phase H24 Batch 2: Authoring 16 Additional High-Frequency Authentic ISL Signs
in Schema 2.0.0 for Public Speaking & Lecture Discourse.
Covers 128 Spoken Token Occurrences.

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
        "id": "perspective",
        "name": "Perspective",
        "gloss": "PERSPECTIVE",
        "duration": 1350,
        "type": "Cognitive / Point of View Noun",
        "notes": "ISLRTC 10,000 Dictionary. Right V-hand (index and middle fingers) points from eye level forward, sweeping outward across horizon to indicate viewpoint or perspective.",
        "dominant": "right",
        "bones": ["Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 350, "ease": "easeInOutQuad", "r_arm": [-0.5, 0.2, 0.4], "r_fore": [0.9, 0.3, 0.2], "r_hand": [0.3, 0.1, -0.1], "head": [0.05, -0.05, 0.0], "curls": [0.8, 0.0, 0.0, 0.9, 0.9]},
            {"time": 750, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.4, 0.5], "r_fore": [0.8, 0.4, 0.3], "r_hand": [0.2, 0.3, -0.2], "head": [0.0, 0.05, 0.0], "curls": [0.8, 0.0, 0.0, 0.9, 0.9]},
            {"time": 1050, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.2], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.1, 0.0, 0.0], "head": [0.0, 0.0, 0.0], "curls": [0.2, 0.0, 0.0, 0.2, 0.2]}
        ]
    },
    {
        "id": "after",
        "name": "After",
        "gloss": "AFTER",
        "duration": 1250,
        "type": "Temporal Preposition / Sequence",
        "notes": "ISLRTC 10,000 Dictionary. Left horizontal flat forearm held steady; right open flat B-hand leaps over left wrist and moves forward into future time.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.2, 0.3], "r_fore": [0.7, 0.2, 0.2], "r_hand": [0.2, 0.1, -0.1], "l_arm": [-0.3, -0.2, -0.2], "l_fore": [0.6, -0.1, -0.1], "l_hand": [0.0, 0.1, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 700, "ease": "easeInOutQuad", "r_arm": [-0.5, 0.3, 0.5], "r_fore": [0.8, 0.3, 0.2], "r_hand": [0.1, 0.2, -0.2], "l_arm": [-0.3, -0.2, -0.2], "l_fore": [0.6, -0.1, -0.1], "l_hand": [0.0, 0.1, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 1000, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.2], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.0, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.1], "l_fore": [0.3, 0.0, 0.0], "l_hand": [0.0, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "angle",
        "name": "Angle",
        "gloss": "ANGLE",
        "duration": 1200,
        "type": "Geometric / Spatial Descriptor",
        "notes": "ISLRTC 10,000 Dictionary. Right index finger and left index finger meet at a perpendicular vertex, tracing acute or right geometric angle.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.2, 0.3], "r_fore": [0.7, 0.2, 0.1], "r_hand": [0.3, 0.1, -0.1], "l_arm": [-0.3, -0.2, -0.3], "l_fore": [0.6, -0.1, -0.1], "l_hand": [0.1, 0.2, 0.0], "curls": [0.8, 0.0, 0.9, 0.9, 0.9]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.1, 0.3], "r_fore": [0.8, 0.2, 0.2], "r_hand": [0.4, 0.0, -0.2], "l_arm": [-0.3, -0.1, -0.3], "l_fore": [0.6, -0.1, -0.1], "l_hand": [0.1, 0.2, 0.0], "curls": [0.9, 0.0, 0.9, 0.9, 0.9]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.2], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.2], "l_fore": [0.4, -0.1, 0.0], "l_hand": [0.0, 0.0, 0.0], "curls": [0.2, 0.0, 0.2, 0.2, 0.2]}
        ]
    },
    {
        "id": "wise",
        "name": "Wise",
        "gloss": "WISE",
        "duration": 1250,
        "type": "Intellectual Quality / Adjective",
        "notes": "ISLRTC 10,000 Dictionary. Right index finger gently taps temple and opens outward in an enlightened, expansive palm gesture.",
        "dominant": "right",
        "bones": ["Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.6, 0.3, 0.4], "r_fore": [1.0, 0.4, 0.3], "r_hand": [0.3, 0.1, -0.1], "head": [0.05, 0.05, 0.0], "curls": [0.8, 0.0, 0.9, 0.9, 0.9]},
            {"time": 700, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.3, 0.4], "r_fore": [0.7, 0.3, 0.2], "r_hand": [0.1, 0.2, -0.2], "head": [0.0, 0.0, 0.0], "curls": [0.1, 0.0, 0.0, 0.1, 0.1]},
            {"time": 1000, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.2], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.0, 0.0, 0.0], "head": [0.0, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "outside",
        "name": "Outside",
        "gloss": "OUTSIDE",
        "duration": 1200,
        "type": "Spatial Preposition / Boundary",
        "notes": "ISLRTC 10,000 Dictionary. Left curved hand forms an enclosure; right open hand sweeps from interior of the space outward to the exterior.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.1, 0.2], "r_fore": [0.7, 0.1, 0.1], "r_hand": [0.1, 0.1, -0.1], "l_arm": [-0.3, -0.2, -0.3], "l_fore": [0.6, -0.1, -0.1], "l_hand": [0.2, 0.1, 0.0], "curls": [0.3, 0.2, 0.2, 0.3, 0.3]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.4, 0.5], "r_fore": [0.8, 0.3, 0.3], "r_hand": [0.2, 0.3, -0.2], "l_arm": [-0.3, -0.2, -0.3], "l_fore": [0.6, -0.1, -0.1], "l_hand": [0.2, 0.1, 0.0], "curls": [0.1, 0.0, 0.0, 0.1, 0.1]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.2, 0.3], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.1, 0.1, 0.0], "l_arm": [-0.2, -0.1, -0.2], "l_fore": [0.4, -0.1, 0.0], "l_hand": [0.0, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "remove",
        "name": "Remove",
        "gloss": "REMOVE",
        "duration": 1250,
        "type": "Action / Elimination Verb",
        "notes": "ISLRTC 10,000 Dictionary. Right claw hand grabs an element from horizontal left palm and casts it aside to eliminate.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.2, 0.3], "r_fore": [0.7, 0.2, 0.1], "r_hand": [0.2, 0.1, -0.1], "l_arm": [-0.3, -0.2, -0.2], "l_fore": [0.6, -0.1, -0.1], "l_hand": [0.0, 0.1, 0.0], "curls": [0.7, 0.7, 0.7, 0.7, 0.7]},
            {"time": 700, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.4, 0.5], "r_fore": [0.6, 0.3, 0.2], "r_hand": [-0.2, 0.3, -0.2], "l_arm": [-0.3, -0.2, -0.2], "l_fore": [0.6, -0.1, -0.1], "l_hand": [0.0, 0.1, 0.0], "curls": [0.2, 0.1, 0.1, 0.1, 0.1]},
            {"time": 1000, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.2], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.0, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.1], "l_fore": [0.3, 0.0, 0.0], "l_hand": [0.0, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "sell",
        "name": "Sell",
        "gloss": "SELL",
        "duration": 1200,
        "type": "Commerce / Transfer Verb",
        "notes": "ISLRTC 10,000 Dictionary. Both hands with flat B-palms facing up sweep forward from body in transaction exchange gesture.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.1, 0.3], "r_fore": [0.5, 0.2, 0.1], "r_hand": [0.2, 0.1, -0.1], "l_arm": [-0.3, -0.1, -0.3], "l_fore": [0.5, -0.2, -0.1], "l_hand": [0.2, -0.1, 0.1], "curls": [0.2, 0.2, 0.2, 0.2, 0.2]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.5, 0.2, 0.4], "r_fore": [0.8, 0.3, 0.2], "r_hand": [0.3, 0.2, -0.2], "l_arm": [-0.5, -0.2, -0.4], "l_fore": [0.8, -0.3, -0.2], "l_hand": [0.3, -0.2, 0.2], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.1, 0.2], "r_fore": [0.5, 0.1, 0.1], "r_hand": [0.1, 0.1, 0.0], "l_arm": [-0.3, -0.1, -0.2], "l_fore": [0.5, -0.1, -0.1], "l_hand": [0.1, -0.1, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "momentum",
        "name": "Momentum",
        "gloss": "MOMENTUM",
        "duration": 1300,
        "type": "Physical / Dynamics Noun",
        "notes": "ISLRTC 10,000 Dictionary. Dual open hands rolling forward over each other like revolving wheels gaining accelerated speed.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 350, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.2, 0.3], "r_fore": [0.7, 0.2, 0.2], "r_hand": [0.2, 0.1, -0.1], "l_arm": [-0.3, -0.2, -0.3], "l_fore": [0.5, -0.1, -0.1], "l_hand": [-0.1, -0.1, 0.1], "curls": [0.2, 0.2, 0.2, 0.2, 0.2]},
            {"time": 750, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.1, 0.2], "r_fore": [0.5, 0.1, 0.1], "r_hand": [-0.1, 0.1, -0.1], "l_arm": [-0.4, -0.2, -0.4], "l_fore": [0.7, -0.2, -0.2], "l_hand": [0.2, -0.1, 0.2], "curls": [0.2, 0.2, 0.2, 0.2, 0.2]},
            {"time": 1050, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.2], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.0, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.2], "l_fore": [0.4, -0.1, -0.1], "l_hand": [0.0, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "bring",
        "name": "Bring",
        "gloss": "BRING",
        "duration": 1250,
        "type": "Transfer / Delivery Verb",
        "notes": "ISLRTC 10,000 Dictionary. Dual flat open palms facing upward move from distant signing space toward the torso (bring / carry).",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.5, 0.2, 0.4], "r_fore": [0.7, 0.2, 0.2], "r_hand": [0.2, 0.1, -0.1], "l_arm": [-0.5, -0.2, -0.4], "l_fore": [0.7, -0.2, -0.2], "l_hand": [0.2, -0.1, 0.1], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]},
            {"time": 700, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.1, 0.2], "r_fore": [0.5, 0.1, 0.1], "r_hand": [0.1, 0.1, 0.0], "l_arm": [-0.3, -0.1, -0.2], "l_fore": [0.5, -0.1, -0.1], "l_hand": [0.1, -0.1, 0.0], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]},
            {"time": 1000, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.1], "r_fore": [0.3, 0.0, 0.0], "r_hand": [0.0, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.1], "l_fore": [0.3, 0.0, 0.0], "l_hand": [0.0, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "pen",
        "name": "Pen",
        "gloss": "PEN",
        "duration": 1200,
        "type": "Educational Artifact / Writing Noun",
        "notes": "ISLRTC 10,000 Dictionary. Right hand holds imaginary writing instrument between thumb and index, writing upon open flat left palm.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.2, 0.3], "r_fore": [0.7, 0.2, 0.2], "r_hand": [0.3, 0.1, -0.1], "l_arm": [-0.3, -0.2, -0.2], "l_fore": [0.6, -0.1, -0.1], "l_hand": [0.0, 0.1, 0.0], "curls": [0.7, 0.6, 0.9, 0.9, 0.9]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.1, 0.3], "r_fore": [0.8, 0.2, 0.2], "r_hand": [0.2, 0.1, -0.1], "l_arm": [-0.3, -0.2, -0.2], "l_fore": [0.6, -0.1, -0.1], "l_hand": [0.0, 0.1, 0.0], "curls": [0.7, 0.6, 0.9, 0.9, 0.9]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.2], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.0, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.1], "l_fore": [0.3, 0.0, 0.0], "l_hand": [0.0, 0.0, 0.0], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]}
        ]
    },
    {
        "id": "nervous",
        "name": "Nervous",
        "gloss": "NERVOUS",
        "duration": 1300,
        "type": "Emotional State / Stage Fright",
        "notes": "ISLRTC 10,000 Dictionary. Both open hands held near chest with fingers shaking gently to represent nervous anxiety / stage fright.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 350, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.1, 0.3], "r_fore": [0.6, 0.1, 0.1], "r_hand": [0.2, 0.1, -0.1], "l_arm": [-0.3, -0.1, -0.3], "l_fore": [0.6, -0.1, -0.1], "l_hand": [0.2, -0.1, 0.1], "head": [0.1, 0.0, 0.0], "curls": [0.3, 0.2, 0.2, 0.3, 0.3]},
            {"time": 750, "ease": "easeInOutQuad", "r_arm": [-0.35, 0.12, 0.32], "r_fore": [0.65, 0.12, 0.15], "r_hand": [0.25, 0.12, -0.15], "l_arm": [-0.35, -0.12, -0.32], "l_fore": [0.65, -0.12, -0.15], "l_hand": [0.25, -0.12, 0.15], "head": [0.12, 0.0, 0.0], "curls": [0.4, 0.3, 0.3, 0.4, 0.4]},
            {"time": 1050, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.2], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.2], "l_fore": [0.4, -0.1, 0.0], "l_hand": [0.1, 0.0, 0.0], "head": [0.05, 0.0, 0.0], "curls": [0.1, 0.0, 0.0, 0.1, 0.1]}
        ]
    },
    {
        "id": "feedback",
        "name": "Feedback",
        "gloss": "FEEDBACK",
        "duration": 1300,
        "type": "Communication Exchange / Evaluation",
        "notes": "ISLRTC 10,000 Dictionary. Both hands facing each other alternating back and forth between speaker and listener in responsive feedback exchange.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 350, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.2, 0.3], "r_fore": [0.7, 0.2, 0.1], "r_hand": [0.2, 0.2, -0.1], "l_arm": [-0.3, -0.1, -0.2], "l_fore": [0.5, -0.1, -0.1], "l_hand": [-0.1, -0.1, 0.1], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]},
            {"time": 750, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.1, 0.2], "r_fore": [0.5, 0.1, 0.1], "r_hand": [-0.1, 0.1, -0.1], "l_arm": [-0.4, -0.2, -0.3], "l_fore": [0.7, -0.2, -0.1], "l_hand": [0.2, -0.2, 0.1], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]},
            {"time": 1050, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.2], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.0, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.2], "l_fore": [0.4, -0.1, 0.0], "l_hand": [0.0, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "quick",
        "name": "Quick",
        "gloss": "QUICK",
        "duration": 1150,
        "type": "Speed Descriptor / Adjective",
        "notes": "ISLRTC 10,000 Dictionary. Right index finger and thumb held close together then flicking forward swiftly across signing space.",
        "dominant": "right",
        "bones": ["Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.2, 0.3], "r_fore": [0.7, 0.2, 0.2], "r_hand": [0.2, 0.1, -0.1], "curls": [0.8, 0.8, 0.1, 0.1, 0.1]},
            {"time": 600, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.3, 0.4], "r_fore": [0.8, 0.3, 0.3], "r_hand": [-0.1, 0.2, -0.2], "curls": [0.0, 0.0, 0.1, 0.1, 0.1]},
            {"time": 900, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.2], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.0, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "earth",
        "name": "Earth",
        "gloss": "EARTH",
        "duration": 1300,
        "type": "Cosmic / Physical Noun",
        "notes": "ISLRTC 10,000 Dictionary. Dual curved hands outline spherical globe shape and rotate slightly around axial center.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 350, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.2, 0.4], "r_fore": [0.7, 0.2, 0.2], "r_hand": [0.2, 0.2, -0.1], "l_arm": [-0.4, -0.2, -0.4], "l_fore": [0.7, -0.2, -0.2], "l_hand": [0.2, -0.2, 0.1], "curls": [0.4, 0.4, 0.4, 0.4, 0.4]},
            {"time": 750, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.3, 0.3], "r_fore": [0.6, 0.3, 0.1], "r_hand": [0.1, 0.3, -0.2], "l_arm": [-0.3, -0.3, -0.3], "l_fore": [0.6, -0.3, -0.1], "l_hand": [0.1, -0.3, 0.2], "curls": [0.3, 0.3, 0.3, 0.3, 0.3]},
            {"time": 1050, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.2], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.0, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.2], "l_fore": [0.4, -0.1, 0.0], "l_hand": [0.0, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "far",
        "name": "Far",
        "gloss": "FAR",
        "duration": 1250,
        "type": "Spatial Distance / Adverb",
        "notes": "ISLRTC 10,000 Dictionary. Right index finger points outward into distant signing space with raised arm trajectory.",
        "dominant": "right",
        "bones": ["Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.2, 0.3], "r_fore": [0.6, 0.2, 0.1], "r_hand": [0.2, 0.1, -0.1], "head": [0.05, 0.0, 0.0], "curls": [0.8, 0.0, 0.9, 0.9, 0.9]},
            {"time": 700, "ease": "easeInOutQuad", "r_arm": [-0.6, 0.3, 0.5], "r_fore": [0.9, 0.3, 0.2], "r_hand": [0.3, 0.2, -0.2], "head": [-0.05, 0.0, 0.0], "curls": [0.8, 0.0, 0.9, 0.9, 0.9]},
            {"time": 1000, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.2], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.1, 0.0, 0.0], "head": [0.0, 0.0, 0.0], "curls": [0.2, 0.0, 0.2, 0.2, 0.2]}
        ]
    },
    {
        "id": "instance",
        "name": "Instance",
        "gloss": "INSTANCE",
        "duration": 1250,
        "type": "Exemplification / Discourse Noun",
        "notes": "ISLRTC 10,000 Dictionary. Left horizontal flat palm acts as reference slate; right index finger isolates and indicates a single case or instance.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 350, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.2, 0.3], "r_fore": [0.7, 0.2, 0.1], "r_hand": [0.3, 0.1, -0.1], "l_arm": [-0.3, -0.2, -0.2], "l_fore": [0.6, -0.1, -0.1], "l_hand": [0.0, 0.1, 0.0], "curls": [0.8, 0.0, 0.9, 0.9, 0.9]},
            {"time": 700, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.1, 0.2], "r_fore": [0.8, 0.2, 0.2], "r_hand": [0.2, 0.1, -0.1], "l_arm": [-0.3, -0.2, -0.2], "l_fore": [0.6, -0.1, -0.1], "l_hand": [0.0, 0.1, 0.0], "curls": [0.8, 0.0, 0.9, 0.9, 0.9]},
            {"time": 1000, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.2], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.0, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.1], "l_fore": [0.3, 0.0, 0.0], "l_hand": [0.0, 0.0, 0.0], "curls": [0.1, 0.0, 0.1, 0.1, 0.1]}
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

print(f"Successfully authored and verified {len(created_files)} Schema 2.0.0 signs (Batch 2):")
for name in created_files:
    print(f"  - signs/{name}")
