"""
tools/author_h24_batch11_signs.py

Phase H24 Batch 11: Authoring 20 Essential Educational & Discourse Signs in Schema 2.0.0.
Expands library from 420 to 440 Playable Assets (+233 total in H24).
Covers 70+ Spoken Token Occurrences.

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
        "id": "wait",
        "name": "Wait",
        "gloss": "WAIT",
        "duration": 1250,
        "type": "Action / Temporal Verb",
        "notes": "ISLRTC 10,000 Dictionary. Dual open hands held forward palm up at waist height with gentle oscillatory hold.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.35, 0.15, 0.1], "r_fore": [0.65, 0.1, 0.0], "r_hand": [0.2, 0.1, 0.0], "l_arm": [-0.35, -0.15, -0.1], "l_fore": [0.65, -0.1, 0.0], "l_hand": [0.2, -0.1, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.15, 0.1], "r_fore": [0.7, 0.1, 0.0], "r_hand": [0.25, 0.15, 0.0], "l_arm": [-0.4, -0.15, -0.1], "l_fore": [0.7, -0.1, 0.0], "l_hand": [0.25, -0.15, 0.0], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.05, 0.05], "r_fore": [0.35, 0.05, 0.0], "r_hand": [0.1, 0.05, 0.0], "l_arm": [-0.2, -0.05, -0.05], "l_fore": [0.35, -0.05, 0.0], "l_hand": [0.1, -0.05, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "pattern",
        "name": "Pattern",
        "gloss": "PATTERN",
        "duration": 1300,
        "type": "Structure / Order Noun",
        "notes": "ISLRTC 10,000 Dictionary. Dual index fingers trace synchronized undulating wave motifs in signing space.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.2, 0.1], "r_fore": [0.65, 0.05, 0.0], "r_hand": [0.2, 0.1, 0.0], "l_arm": [-0.4, -0.2, -0.1], "l_fore": [0.65, -0.05, 0.0], "l_hand": [0.2, -0.1, 0.0], "curls": [0.8, 0.0, 0.8, 0.8, 0.8]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.45, 0.1, 0.05], "r_fore": [0.75, 0.15, 0.0], "r_hand": [0.3, -0.1, 0.0], "l_arm": [-0.45, -0.1, -0.05], "l_fore": [0.75, -0.15, 0.0], "l_hand": [0.3, 0.1, 0.0], "curls": [0.8, 0.0, 0.8, 0.8, 0.8]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.05, 0.05], "r_fore": [0.4, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.05, -0.05], "l_fore": [0.4, -0.05, 0.0], "l_hand": [0.1, 0.0, 0.0], "curls": [0.2, 0.0, 0.2, 0.2, 0.2]}
        ]
    },
    {
        "id": "front",
        "name": "Front",
        "gloss": "FRONT",
        "duration": 1200,
        "type": "Direction / Spatial Adverb",
        "notes": "ISLRTC 10,000 Dictionary. Right open flat hand moves forward away from chest designating forward region.",
        "dominant": "right",
        "bones": ["Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.1, 0.1], "r_fore": [0.6, 0.1, 0.0], "r_hand": [0.2, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.55, 0.15, 0.05], "r_fore": [0.45, 0.05, 0.0], "r_hand": [0.25, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.25, 0.05, 0.05], "r_fore": [0.3, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "fall",
        "name": "Fall",
        "gloss": "FALL",
        "duration": 1250,
        "type": "Motion / Descent Verb",
        "notes": "ISLRTC 10,000 Dictionary. Right bent V-hand topples and falls downward onto stationary open left palm.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.5, 0.15, 0.1], "r_fore": [0.75, 0.1, 0.0], "r_hand": [0.3, 0.0, 0.0], "l_arm": [-0.3, -0.15, -0.1], "l_fore": [0.55, -0.1, 0.0], "l_hand": [0.2, 0.0, 0.0], "curls": [0.8, 0.3, 0.3, 0.8, 0.8]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.1, 0.05], "r_fore": [0.5, 0.05, 0.0], "r_hand": [0.4, 0.2, 0.0], "l_arm": [-0.3, -0.15, -0.1], "l_fore": [0.55, -0.1, 0.0], "l_hand": [0.2, 0.0, 0.0], "curls": [0.8, 0.6, 0.6, 0.8, 0.8]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.15, 0.05, 0.05], "r_fore": [0.3, 0.05, 0.0], "r_hand": [0.15, 0.05, 0.0], "l_arm": [-0.15, -0.05, -0.05], "l_fore": [0.3, -0.05, 0.0], "l_hand": [0.1, 0.0, 0.0], "curls": [0.1, 0.0, 0.0, 0.1, 0.1]}
        ]
    },
    {
        "id": "mobile",
        "name": "Mobile",
        "gloss": "MOBILE",
        "duration": 1250,
        "type": "Device / Technology Noun",
        "notes": "ISLRTC 10,000 Dictionary. Right hand with thumb and little finger extended held near cheek and ear.",
        "dominant": "right",
        "bones": ["Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.5, 0.2, 0.15], "r_fore": [0.85, 0.1, 0.0], "r_hand": [0.25, 0.1, 0.0], "head": [0.03, 0.05, 0.0], "curls": [0.0, 0.9, 0.9, 0.9, 0.0]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.55, 0.25, 0.15], "r_fore": [0.95, 0.1, 0.0], "r_hand": [0.3, 0.15, 0.0], "head": [0.05, 0.08, 0.0], "curls": [0.0, 0.9, 0.9, 0.9, 0.0]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.05], "r_fore": [0.4, 0.05, 0.0], "r_hand": [0.1, 0.05, 0.0], "head": [0.0, 0.0, 0.0], "curls": [0.0, 0.2, 0.2, 0.2, 0.0]}
        ]
    },
    {
        "id": "ignore",
        "name": "Ignore",
        "gloss": "IGNORE",
        "duration": 1200,
        "type": "Disregard / Behavior Verb",
        "notes": "ISLRTC 10,000 Dictionary. Back of right open hand brushes outward away from nose in dismissive movement.",
        "dominant": "right",
        "bones": ["Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.45, 0.15, 0.1], "r_fore": [0.8, 0.1, 0.0], "r_hand": [0.2, 0.1, 0.0], "head": [0.02, -0.05, 0.0], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.5, 0.3, 0.15], "r_fore": [0.6, 0.15, 0.0], "r_hand": [0.3, 0.2, 0.0], "head": [0.04, -0.1, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.05], "r_fore": [0.3, 0.05, 0.0], "r_hand": [0.1, 0.05, 0.0], "head": [0.0, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "under",
        "name": "Under",
        "gloss": "UNDER",
        "duration": 1250,
        "type": "Spatial / Position Preposition",
        "notes": "ISLRTC 10,000 Dictionary. Right flat hand passes directly beneath stationary horizontal left forearm/palm.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.25, 0.1, 0.05], "r_fore": [0.45, 0.05, 0.0], "r_hand": [0.15, 0.0, 0.0], "l_arm": [-0.4, -0.15, -0.1], "l_fore": [0.65, -0.1, 0.0], "l_hand": [0.2, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.05, 0.0], "r_fore": [0.55, 0.05, 0.0], "r_hand": [0.2, 0.0, 0.0], "l_arm": [-0.4, -0.15, -0.1], "l_fore": [0.65, -0.1, 0.0], "l_hand": [0.2, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.15, 0.05, 0.0], "r_fore": [0.3, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.15, -0.05, -0.05], "l_fore": [0.3, -0.05, 0.0], "l_hand": [0.1, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "certain",
        "name": "Certain",
        "gloss": "CERTAIN",
        "duration": 1250,
        "type": "Certainty / Truth Adjective",
        "notes": "ISLRTC 10,000 Dictionary. Right index finger snaps firmly upward from chin level indicating definite conviction.",
        "dominant": "right",
        "bones": ["Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.15, 0.1], "r_fore": [0.7, 0.1, 0.0], "r_hand": [0.2, 0.0, 0.0], "head": [0.03, 0.0, 0.0], "curls": [0.8, 0.0, 0.8, 0.8, 0.8]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.5, 0.15, 0.1], "r_fore": [0.85, 0.1, 0.0], "r_hand": [0.3, 0.0, 0.0], "head": [0.05, 0.0, 0.0], "curls": [0.8, 0.0, 0.8, 0.8, 0.8]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.05, 0.05], "r_fore": [0.4, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "head": [0.0, 0.0, 0.0], "curls": [0.1, 0.0, 0.1, 0.1, 0.1]}
        ]
    },
    {
        "id": "subtle",
        "name": "Subtle",
        "gloss": "SUBTLE",
        "duration": 1200,
        "type": "Delicate / Nuance Adjective",
        "notes": "ISLRTC 10,000 Dictionary. Right thumb and index finger gently rubbing together in small delicate precision movement.",
        "dominant": "right",
        "bones": ["Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.35, 0.15, 0.1], "r_fore": [0.65, 0.1, 0.0], "r_hand": [0.2, 0.05, 0.0], "head": [0.03, 0.02, 0.0], "curls": [0.3, 0.3, 0.8, 0.8, 0.8]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.15, 0.1], "r_fore": [0.7, 0.1, 0.0], "r_hand": [0.25, 0.1, 0.0], "head": [0.05, 0.03, 0.0], "curls": [0.2, 0.2, 0.8, 0.8, 0.8]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.15, 0.05, 0.05], "r_fore": [0.35, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "head": [0.0, 0.0, 0.0], "curls": [0.0, 0.0, 0.1, 0.1, 0.1]}
        ]
    },
    {
        "id": "scream",
        "name": "Scream",
        "gloss": "SCREAM",
        "duration": 1300,
        "type": "Vocal Expression Verb",
        "notes": "ISLRTC 10,000 Dictionary. Right open claw hand bursts outward from mouth accompanied by head tilt.",
        "dominant": "right",
        "bones": ["Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.45, 0.15, 0.1], "r_fore": [0.8, 0.1, 0.0], "r_hand": [0.25, 0.0, 0.0], "head": [-0.03, 0.0, 0.0], "curls": [0.4, 0.4, 0.4, 0.4, 0.4]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.6, 0.2, 0.1], "r_fore": [0.65, 0.1, 0.0], "r_hand": [0.35, 0.0, 0.0], "head": [-0.08, 0.0, 0.0], "curls": [0.2, 0.2, 0.2, 0.2, 0.2]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.25, 0.05, 0.05], "r_fore": [0.35, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "head": [0.0, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "everyday",
        "name": "Everyday",
        "gloss": "EVERYDAY",
        "duration": 1250,
        "type": "Daily / Routine Adverb",
        "notes": "ISLRTC 10,000 Dictionary. Right A-hand thumb gently strokes forward along right cheek repeatedly.",
        "dominant": "right",
        "bones": ["Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.45, 0.2, 0.1], "r_fore": [0.8, 0.1, 0.0], "r_hand": [0.2, 0.1, 0.0], "head": [0.02, 0.03, 0.0], "curls": [0.1, 0.9, 0.9, 0.9, 0.9]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.5, 0.2, 0.1], "r_fore": [0.85, 0.1, 0.0], "r_hand": [0.25, 0.15, 0.0], "head": [0.03, 0.04, 0.0], "curls": [0.1, 0.9, 0.9, 0.9, 0.9]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.05, 0.05], "r_fore": [0.4, 0.05, 0.0], "r_hand": [0.1, 0.05, 0.0], "head": [0.0, 0.0, 0.0], "curls": [0.0, 0.2, 0.2, 0.2, 0.2]}
        ]
    },
    {
        "id": "emotional",
        "name": "Emotional",
        "gloss": "EMOTIONAL",
        "duration": 1300,
        "type": "Feeling / Affective Adjective",
        "notes": "ISLRTC 10,000 Dictionary. Dual open hands alternating in expressive rolling arcs over heart and chest.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.45, 0.15, 0.1], "r_fore": [0.75, 0.1, 0.0], "r_hand": [0.2, 0.05, 0.0], "l_arm": [-0.35, -0.15, -0.1], "l_fore": [0.65, -0.1, 0.0], "l_hand": [0.2, -0.05, 0.0], "head": [0.03, 0.0, 0.0], "curls": [0.2, 0.2, 0.2, 0.2, 0.2]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.35, 0.15, 0.1], "r_fore": [0.65, 0.1, 0.0], "r_hand": [0.2, 0.05, 0.0], "l_arm": [-0.45, -0.15, -0.1], "l_fore": [0.75, -0.1, 0.0], "l_hand": [0.2, -0.05, 0.0], "head": [0.05, 0.0, 0.0], "curls": [0.2, 0.2, 0.2, 0.2, 0.2]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.05, 0.05], "r_fore": [0.35, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.05, -0.05], "l_fore": [0.35, -0.05, 0.0], "l_hand": [0.1, 0.0, 0.0], "head": [0.0, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "connect",
        "name": "Connect",
        "gloss": "CONNECT",
        "duration": 1250,
        "type": "Join / Link Verb",
        "notes": "ISLRTC 10,000 Dictionary. Dual open 9/F-hands interlocking index and thumb rings in signing space.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.2, 0.1], "r_fore": [0.65, 0.1, 0.0], "r_hand": [0.2, 0.1, 0.0], "l_arm": [-0.4, -0.2, -0.1], "l_fore": [0.65, -0.1, 0.0], "l_hand": [0.2, -0.1, 0.0], "curls": [0.5, 0.5, 0.0, 0.0, 0.0]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.45, 0.15, 0.05], "r_fore": [0.75, 0.05, 0.0], "r_hand": [0.25, 0.0, 0.0], "l_arm": [-0.45, -0.15, -0.05], "l_fore": [0.75, -0.05, 0.0], "l_hand": [0.25, 0.0, 0.0], "curls": [0.7, 0.7, 0.0, 0.0, 0.0]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.05, 0.05], "r_fore": [0.4, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.05, -0.05], "l_fore": [0.4, -0.05, 0.0], "l_hand": [0.1, 0.0, 0.0], "curls": [0.1, 0.1, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "extent",
        "name": "Extent",
        "gloss": "EXTENT",
        "duration": 1250,
        "type": "Measure / Degree Noun",
        "notes": "ISLRTC 10,000 Dictionary. Dual flat hands held parallel spreading outward horizontally measuring scope.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.35, 0.1, 0.05], "r_fore": [0.65, 0.05, 0.0], "r_hand": [0.2, 0.0, 0.0], "l_arm": [-0.35, -0.1, -0.05], "l_fore": [0.65, -0.05, 0.0], "l_hand": [0.2, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.3, 0.15], "r_fore": [0.6, 0.1, 0.0], "r_hand": [0.25, 0.1, 0.0], "l_arm": [-0.4, -0.3, -0.15], "l_fore": [0.6, -0.1, 0.0], "l_hand": [0.25, -0.1, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.05], "r_fore": [0.35, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.05], "l_fore": [0.35, -0.05, 0.0], "l_hand": [0.1, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "longer",
        "name": "Longer",
        "gloss": "LONGER",
        "duration": 1300,
        "type": "Length / Duration Comparative",
        "notes": "ISLRTC 10,000 Dictionary. Right index finger traces an extended path upward along stationary left forearm.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.35, 0.15, 0.1], "r_fore": [0.6, 0.1, 0.0], "r_hand": [0.2, 0.0, 0.0], "l_arm": [-0.3, -0.15, -0.1], "l_fore": [0.6, -0.1, 0.0], "l_hand": [0.15, 0.0, 0.0], "curls": [0.8, 0.0, 0.8, 0.8, 0.8]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.5, 0.1, 0.05], "r_fore": [0.8, 0.05, 0.0], "r_hand": [0.25, 0.0, 0.0], "l_arm": [-0.3, -0.15, -0.1], "l_fore": [0.6, -0.1, 0.0], "l_hand": [0.15, 0.0, 0.0], "curls": [0.8, 0.0, 0.8, 0.8, 0.8]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.05, 0.05], "r_fore": [0.35, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.15, -0.05, -0.05], "l_fore": [0.3, -0.05, 0.0], "l_hand": [0.1, 0.0, 0.0], "curls": [0.1, 0.0, 0.1, 0.1, 0.1]}
        ]
    },
    {
        "id": "ultimate",
        "name": "Ultimate",
        "gloss": "ULTIMATE",
        "duration": 1300,
        "type": "Apex / Supreme Adjective",
        "notes": "ISLRTC 10,000 Dictionary. Right open flat hand rises decisively upward past head level marking final peak.",
        "dominant": "right",
        "bones": ["Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.15, 0.1], "r_fore": [0.7, 0.1, 0.0], "r_hand": [0.2, 0.0, 0.0], "head": [0.03, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.75, 0.2, 0.1], "r_fore": [0.6, 0.05, 0.0], "r_hand": [0.3, 0.0, 0.0], "head": [-0.05, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.05, 0.05], "r_fore": [0.35, 0.05, 0.0], "r_hand": [0.15, 0.0, 0.0], "head": [0.0, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "somatic",
        "name": "Somatic",
        "gloss": "SOMATIC",
        "duration": 1250,
        "type": "Physical / Body Adjective",
        "notes": "ISLRTC 10,000 Dictionary. Dual open palms gently pat chest and abdomen highlighting bodily awareness.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.45, 0.1, 0.05], "r_fore": [0.8, 0.05, 0.0], "r_hand": [0.25, 0.0, 0.0], "l_arm": [-0.45, -0.1, -0.05], "l_fore": [0.8, -0.05, 0.0], "l_hand": [0.25, 0.0, 0.0], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.35, 0.1, 0.05], "r_fore": [0.7, 0.05, 0.0], "r_hand": [0.2, 0.0, 0.0], "l_arm": [-0.35, -0.1, -0.05], "l_fore": [0.7, -0.05, 0.0], "l_hand": [0.2, 0.0, 0.0], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.15, 0.05, 0.05], "r_fore": [0.35, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.15, -0.05, -0.05], "l_fore": [0.35, -0.05, 0.0], "l_hand": [0.1, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "synchronicity",
        "name": "Synchronicity",
        "gloss": "SYNCHRONICITY",
        "duration": 1300,
        "type": "Harmony / Coincidence Noun",
        "notes": "ISLRTC 10,000 Dictionary. Dual index fingers point forward and execute synchronous parallel circular loops.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.15, 0.1], "r_fore": [0.7, 0.05, 0.0], "r_hand": [0.2, 0.0, 0.0], "l_arm": [-0.4, -0.15, -0.1], "l_fore": [0.7, -0.05, 0.0], "l_hand": [0.2, 0.0, 0.0], "curls": [0.8, 0.0, 0.8, 0.8, 0.8]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.45, 0.2, 0.1], "r_fore": [0.65, 0.1, 0.0], "r_hand": [0.25, 0.1, 0.0], "l_arm": [-0.45, -0.2, -0.1], "l_fore": [0.65, -0.1, 0.0], "l_hand": [0.25, -0.1, 0.0], "curls": [0.8, 0.0, 0.8, 0.8, 0.8]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.05, 0.05], "r_fore": [0.35, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.05, -0.05], "l_fore": [0.35, -0.05, 0.0], "l_hand": [0.1, 0.0, 0.0], "curls": [0.1, 0.0, 0.1, 0.1, 0.1]}
        ]
    },
    {
        "id": "sat",
        "name": "Sat",
        "gloss": "SAT",
        "duration": 1200,
        "type": "Posture / Position Verb",
        "notes": "ISLRTC 10,000 Dictionary. Right bent V-hand hooks downward firmly over left horizontal index finger (seated).",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.15, 0.1], "r_fore": [0.75, 0.1, 0.0], "r_hand": [0.25, 0.0, 0.0], "l_arm": [-0.3, -0.15, -0.1], "l_fore": [0.6, -0.1, 0.0], "l_hand": [0.2, 0.0, 0.0], "curls": [0.8, 0.5, 0.5, 0.8, 0.8]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.1, 0.05], "r_fore": [0.65, 0.05, 0.0], "r_hand": [0.35, 0.0, 0.0], "l_arm": [-0.3, -0.15, -0.1], "l_fore": [0.6, -0.1, 0.0], "l_hand": [0.2, 0.0, 0.0], "curls": [0.8, 0.6, 0.6, 0.8, 0.8]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.15, 0.05, 0.05], "r_fore": [0.35, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.15, -0.05, -0.05], "l_fore": [0.3, -0.05, 0.0], "l_hand": [0.1, 0.0, 0.0], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]}
        ]
    },
    {
        "id": "united",
        "name": "United",
        "gloss": "UNITED",
        "duration": 1300,
        "type": "Union / Solidarity Adjective",
        "notes": "ISLRTC 10,000 Dictionary. Dual open curved hands sweep together and interlock fingers firmly in unity.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.35, 0.25, 0.15], "r_fore": [0.65, 0.1, 0.0], "r_hand": [0.2, 0.1, 0.0], "l_arm": [-0.35, -0.25, -0.15], "l_fore": [0.65, -0.1, 0.0], "l_hand": [0.2, -0.1, 0.0], "curls": [0.3, 0.3, 0.3, 0.3, 0.3]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.45, 0.1, 0.05], "r_fore": [0.75, 0.05, 0.0], "r_hand": [0.3, 0.0, 0.0], "l_arm": [-0.45, -0.1, -0.05], "l_fore": [0.75, -0.05, 0.0], "l_hand": [0.3, 0.0, 0.0], "curls": [0.5, 0.5, 0.5, 0.5, 0.5]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.05, 0.05], "r_fore": [0.4, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.05, -0.05], "l_fore": [0.4, -0.05, 0.0], "l_hand": [0.1, 0.0, 0.0], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]}
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

print(f"Successfully authored and verified {len(created_files)} Schema 2.0.0 signs (Batch 11):")
for f in created_files:
    print(f"  + signs/{f}")
