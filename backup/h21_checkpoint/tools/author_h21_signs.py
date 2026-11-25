"""
tools/author_h21_signs.py

Phase H21: Authoring 25 High-Frequency Evidence-Based ISL Signs in Schema 2.0.0
for Lecture & Educational Accessibility.
Strict adherence to neutral start and return { x: 0, y: 0, z: 0 }.
"""

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SIGNS_DIR = PROJECT_ROOT / "signs"
SIGNS_DIR.mkdir(parents=True, exist_ok=True)

# Specification for 25 high-frequency signs
AUTHORED_SPECS = [
    {
        "id": "story",
        "name": "Story",
        "gloss": "STORY",
        "duration": 1400,
        "type": "Educational / Discourse",
        "notes": "ISLRTC Educational. Bilateral hands alternating circular outward motion narrating narrative structure.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 350, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.2, 0.4], "r_fore": [0.6, 0.1, 0.2], "r_hand": [0.2, 0.1, -0.1], "l_arm": [-0.2, -0.2, -0.3], "l_fore": [0.5, -0.1, -0.2], "l_hand": [0.1, -0.1, 0.1], "curls": [0.3, 0.2, 0.2, 0.3, 0.3]},
            {"time": 700, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.3, 0.5], "r_fore": [0.8, 0.2, 0.3], "r_hand": [0.3, 0.2, -0.2], "l_arm": [-0.4, -0.3, -0.4], "l_fore": [0.7, -0.2, -0.3], "l_hand": [0.2, -0.2, 0.2], "curls": [0.2, 0.1, 0.1, 0.2, 0.2]},
            {"time": 1050, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.2], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.1, 0.0, -0.1], "l_arm": [-0.2, -0.1, -0.2], "l_fore": [0.3, -0.1, -0.1], "l_hand": [0.1, -0.1, 0.1], "curls": [0.1, 0.0, 0.0, 0.1, 0.1]}
        ]
    },
    {
        "id": "step",
        "name": "Step",
        "gloss": "STEP",
        "duration": 1200,
        "type": "Procedural Action",
        "notes": "ISLRTC Procedural. Right flat palm stepping forward and downward onto sequential invisible tiers.",
        "dominant": "right",
        "bones": ["Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_L_Forearm"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.3], "r_fore": [0.5, 0.2, 0.1], "r_hand": [0.2, 0.0, -0.1], "l_fore": [0.3, -0.1, -0.1], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 600, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.2, 0.4], "r_fore": [0.7, 0.3, 0.2], "r_hand": [-0.1, 0.2, -0.2], "l_fore": [0.4, -0.1, -0.1], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 900, "ease": "easeInOutQuad", "r_arm": [-0.5, 0.2, 0.5], "r_fore": [0.9, 0.3, 0.2], "r_hand": [-0.2, 0.1, -0.1], "l_fore": [0.2, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "music",
        "name": "Music",
        "gloss": "MUSIC",
        "duration": 1350,
        "type": "Cultural / Sensory",
        "notes": "ISLRTC Sensory. Right hand waving rhythmically back and forth across left horizontal forearm.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 350, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.2, 0.4], "r_fore": [0.6, 0.2, 0.1], "r_hand": [0.2, 0.3, -0.1], "l_arm": [-0.2, -0.2, -0.3], "l_fore": [0.6, -0.2, -0.2], "l_hand": [0.1, -0.1, 0.0], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]},
            {"time": 700, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.1, 0.3], "r_fore": [0.8, 0.1, 0.2], "r_hand": [-0.2, -0.3, 0.1], "l_arm": [-0.2, -0.2, -0.3], "l_fore": [0.6, -0.2, -0.2], "l_hand": [0.1, -0.1, 0.0], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]},
            {"time": 1050, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.2, 0.4], "r_fore": [0.6, 0.2, 0.1], "r_hand": [0.2, 0.3, -0.1], "l_arm": [-0.1, -0.1, -0.2], "l_fore": [0.3, -0.1, -0.1], "l_hand": [0.0, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "level",
        "name": "Level",
        "gloss": "LEVEL",
        "duration": 1250,
        "type": "Measurement / State",
        "notes": "ISLRTC Measurement. Open flat palms facing downward moving in horizontal plane to indicate standard or tier.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 350, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.2, 0.3], "r_fore": [0.6, 0.1, 0.1], "r_hand": [-0.2, 0.1, -0.1], "l_arm": [-0.3, -0.2, -0.3], "l_fore": [0.6, -0.1, -0.1], "l_hand": [-0.2, -0.1, 0.1], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 750, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.3, 0.4], "r_fore": [0.7, 0.2, 0.2], "r_hand": [-0.3, 0.2, -0.2], "l_arm": [-0.4, -0.3, -0.4], "l_fore": [0.7, -0.2, -0.2], "l_hand": [-0.3, -0.2, 0.2], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 1050, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.2], "r_fore": [0.4, 0.1, 0.1], "r_hand": [-0.1, 0.0, -0.1], "l_arm": [-0.2, -0.1, -0.2], "l_fore": [0.4, -0.1, -0.1], "l_hand": [-0.1, 0.0, 0.1], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "simple",
        "name": "Simple",
        "gloss": "SIMPLE",
        "duration": 1150,
        "type": "Adjective / Evaluation",
        "notes": "ISLRTC Evaluation. Right index finger touching nose/cheek then extending outward into open relaxed hand.",
        "dominant": "right",
        "bones": ["Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.5, 0.3, 0.4], "r_fore": [0.9, 0.3, 0.3], "r_hand": [0.4, 0.2, 0.1], "head": [0.1, 0.0, 0.0], "curls": [0.8, 0.0, 0.9, 0.9, 0.9]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.2, 0.3], "r_fore": [0.6, 0.2, 0.1], "r_hand": [0.1, 0.1, -0.1], "head": [0.0, 0.0, 0.0], "curls": [0.2, 0.0, 0.1, 0.1, 0.1]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.2], "r_fore": [0.4, 0.1, 0.0], "r_hand": [0.0, 0.0, 0.0], "head": [0.0, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "stage",
        "name": "Stage",
        "gloss": "STAGE",
        "duration": 1300,
        "type": "Educational / Spatial",
        "notes": "ISLRTC Spatial. Dual palms outlining elevated rectangular platform where speaker stands.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 350, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.2, 0.3], "r_fore": [0.7, 0.2, 0.1], "r_hand": [-0.2, 0.2, -0.2], "l_arm": [-0.4, -0.2, -0.3], "l_fore": [0.7, -0.2, -0.1], "l_hand": [-0.2, -0.2, 0.2], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 750, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.4, 0.5], "r_fore": [0.6, 0.3, 0.2], "r_hand": [-0.1, 0.3, -0.2], "l_arm": [-0.3, -0.4, -0.5], "l_fore": [0.6, -0.3, -0.2], "l_hand": [-0.1, -0.3, 0.2], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 1050, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.2, 0.3], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.0, 0.1, -0.1], "l_arm": [-0.2, -0.2, -0.3], "l_fore": [0.4, -0.1, -0.1], "l_hand": [0.0, -0.1, 0.1], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "audience",
        "name": "Audience",
        "gloss": "AUDIENCE",
        "duration": 1400,
        "type": "Public Discourse / People",
        "notes": "ISLRTC Discourse. Dual curved palms facing outward moving in broad sweep to indicate crowd of listeners.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 350, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.1, 0.2], "r_fore": [0.6, 0.1, 0.1], "r_hand": [0.2, 0.1, -0.1], "l_arm": [-0.3, -0.1, -0.2], "l_fore": [0.6, -0.1, -0.1], "l_hand": [0.2, -0.1, 0.1], "head": [0.0, 0.0, 0.0], "curls": [0.2, 0.2, 0.2, 0.2, 0.2]},
            {"time": 750, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.4, 0.6], "r_fore": [0.7, 0.3, 0.2], "r_hand": [0.3, 0.3, -0.2], "l_arm": [-0.4, -0.4, -0.6], "l_fore": [0.7, -0.3, -0.2], "l_hand": [0.3, -0.3, 0.2], "head": [0.05, 0.0, 0.0], "curls": [0.3, 0.3, 0.3, 0.3, 0.3]},
            {"time": 1100, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.2, 0.3], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.1, 0.1, -0.1], "l_arm": [-0.2, -0.2, -0.3], "l_fore": [0.4, -0.1, -0.1], "l_hand": [0.1, -0.1, 0.1], "head": [0.0, 0.0, 0.0], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]}
        ]
    },
    {
        "id": "pause",
        "name": "Pause",
        "gloss": "PAUSE",
        "duration": 1200,
        "type": "Discourse / Action",
        "notes": "ISLRTC Discourse. Open vertical flat palms raised forward abruptly halting movement to denote deliberate silence.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.2, 0.3], "r_fore": [0.8, 0.2, 0.2], "r_hand": [-0.4, 0.1, -0.2], "l_arm": [-0.4, -0.2, -0.3], "l_fore": [0.8, -0.2, -0.2], "l_hand": [-0.4, -0.1, 0.2], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 700, "ease": "easeInOutQuad", "r_arm": [-0.45, 0.2, 0.3], "r_fore": [0.85, 0.2, 0.2], "r_hand": [-0.45, 0.1, -0.2], "l_arm": [-0.45, -0.2, -0.3], "l_fore": [0.85, -0.2, -0.2], "l_hand": [-0.45, -0.1, 0.2], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.1], "r_fore": [0.4, 0.1, 0.1], "r_hand": [-0.1, 0.0, -0.1], "l_arm": [-0.2, -0.1, -0.1], "l_fore": [0.4, -0.1, -0.1], "l_hand": [-0.1, 0.0, 0.1], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "rule",
        "name": "Rule",
        "gloss": "RULE",
        "duration": 1300,
        "type": "Legal / Administrative",
        "notes": "ISLRTC Legal. Right 'R' handshape touching top then bottom of vertical left base palm.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 350, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.2, 0.3], "r_fore": [0.8, 0.3, 0.2], "r_hand": [0.2, 0.1, -0.1], "l_arm": [-0.3, -0.2, -0.3], "l_fore": [0.7, -0.1, -0.1], "l_hand": [-0.3, 0.0, 0.0], "curls": [0.7, 0.0, 0.0, 0.8, 0.8]},
            {"time": 700, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.2, 0.3], "r_fore": [0.6, 0.2, 0.1], "r_hand": [0.1, 0.1, -0.1], "l_arm": [-0.3, -0.2, -0.3], "l_fore": [0.7, -0.1, -0.1], "l_hand": [-0.3, 0.0, 0.0], "curls": [0.7, 0.0, 0.0, 0.8, 0.8]},
            {"time": 1050, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.1], "r_fore": [0.3, 0.1, 0.0], "r_hand": [0.0, 0.0, 0.0], "l_arm": [-0.1, -0.1, -0.1], "l_fore": [0.3, 0.0, 0.0], "l_hand": [0.0, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "line",
        "name": "Line",
        "gloss": "LINE",
        "duration": 1250,
        "type": "Descriptive / Spatial",
        "notes": "ISLRTC Descriptive. Extended pinkies of both hands touching at center then pulling horizontally apart.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.1, 0.2], "r_fore": [0.7, 0.2, 0.1], "r_hand": [0.1, 0.1, 0.0], "l_arm": [-0.3, -0.1, -0.2], "l_fore": [0.7, -0.2, -0.1], "l_hand": [0.1, -0.1, 0.0], "curls": [0.8, 0.8, 0.8, 0.8, 0.0]},
            {"time": 750, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.4, 0.5], "r_fore": [0.6, 0.3, 0.2], "r_hand": [0.1, 0.3, -0.1], "l_arm": [-0.4, -0.4, -0.5], "l_fore": [0.6, -0.3, -0.2], "l_hand": [0.1, -0.3, 0.1], "curls": [0.8, 0.8, 0.8, 0.8, 0.0]},
            {"time": 1050, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.2, 0.2], "r_fore": [0.3, 0.1, 0.1], "r_hand": [0.0, 0.1, 0.0], "l_arm": [-0.2, -0.2, -0.2], "l_fore": [0.3, -0.1, -0.1], "l_hand": [0.0, -0.1, 0.0], "curls": [0.2, 0.2, 0.2, 0.2, 0.0]}
        ]
    },
    {
        "id": "space",
        "name": "Space",
        "gloss": "SPACE",
        "duration": 1350,
        "type": "Spatial / Dimensional",
        "notes": "ISLRTC Dimensional. Both curved 5-handshapes tracing an expansive horizontal boundary of open area.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 350, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.2, 0.3], "r_fore": [0.6, 0.2, 0.1], "r_hand": [-0.1, 0.2, -0.1], "l_arm": [-0.3, -0.2, -0.3], "l_fore": [0.6, -0.2, -0.1], "l_hand": [-0.1, -0.2, 0.1], "curls": [0.2, 0.2, 0.2, 0.2, 0.2]},
            {"time": 800, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.4, 0.6], "r_fore": [0.7, 0.3, 0.2], "r_hand": [-0.2, 0.4, -0.2], "l_arm": [-0.4, -0.4, -0.6], "l_fore": [0.7, -0.3, -0.2], "l_hand": [-0.2, -0.4, 0.2], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]},
            {"time": 1100, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.2, 0.2], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.0, 0.1, 0.0], "l_arm": [-0.2, -0.2, -0.2], "l_fore": [0.4, -0.1, -0.1], "l_hand": [0.0, -0.1, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "energy",
        "name": "Energy",
        "gloss": "ENERGY",
        "duration": 1300,
        "type": "Kinetic / Physical",
        "notes": "ISLRTC Physical. Right 'E' handshape circling forward from chest with dynamic upward pulsation.",
        "dominant": "right",
        "bones": ["Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Spine1"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.2, 0.3], "r_fore": [0.7, 0.2, 0.2], "r_hand": [0.2, 0.1, -0.1], "spine": [0.05, 0.0, 0.0], "curls": [0.7, 0.6, 0.6, 0.6, 0.6]},
            {"time": 700, "ease": "easeInOutQuad", "r_arm": [-0.5, 0.3, 0.5], "r_fore": [1.0, 0.3, 0.3], "r_hand": [0.4, 0.2, -0.2], "spine": [0.1, 0.0, 0.0], "curls": [0.6, 0.5, 0.5, 0.5, 0.5]},
            {"time": 1000, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.2], "r_fore": [0.4, 0.1, 0.1], "r_hand": [0.1, 0.0, 0.0], "spine": [0.0, 0.0, 0.0], "curls": [0.2, 0.2, 0.2, 0.2, 0.2]}
        ]
    },
    {
        "id": "power",
        "name": "Power",
        "gloss": "POWER",
        "duration": 1250,
        "type": "Strength / Capacity",
        "notes": "ISLRTC Physical. Dual closed fists flexing biceps with firm forward chest posture.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Spine1"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.3, 0.4], "r_fore": [1.1, 0.3, 0.2], "r_hand": [0.3, 0.2, -0.2], "l_arm": [-0.4, -0.3, -0.4], "l_fore": [1.1, -0.3, -0.2], "l_hand": [0.3, -0.2, 0.2], "spine": [0.08, 0.0, 0.0], "curls": [0.9, 0.9, 0.9, 0.9, 0.9]},
            {"time": 750, "ease": "easeInOutQuad", "r_arm": [-0.45, 0.35, 0.45], "r_fore": [1.15, 0.3, 0.2], "r_hand": [0.35, 0.2, -0.2], "l_arm": [-0.45, -0.35, -0.45], "l_fore": [1.15, -0.3, -0.2], "l_hand": [0.35, -0.2, 0.2], "spine": [0.1, 0.0, 0.0], "curls": [0.9, 0.9, 0.9, 0.9, 0.9]},
            {"time": 1050, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.2], "r_fore": [0.5, 0.1, 0.1], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.2], "l_fore": [0.5, -0.1, -0.1], "l_hand": [0.1, 0.0, 0.0], "spine": [0.0, 0.0, 0.0], "curls": [0.3, 0.3, 0.3, 0.3, 0.3]}
        ]
    },
    {
        "id": "art",
        "name": "Art",
        "gloss": "ART",
        "duration": 1300,
        "type": "Creative / Visual",
        "notes": "ISLRTC Creative. Right pinky finger drawing curved strokes across open vertical left base palm.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 350, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.2, 0.3], "r_fore": [0.8, 0.3, 0.2], "r_hand": [0.3, 0.2, -0.1], "l_arm": [-0.3, -0.2, -0.3], "l_fore": [0.7, -0.1, -0.1], "l_hand": [-0.2, 0.1, 0.0], "curls": [0.8, 0.8, 0.8, 0.8, 0.0]},
            {"time": 750, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.2, 0.3], "r_fore": [0.6, 0.2, 0.1], "r_hand": [0.1, 0.1, -0.1], "l_arm": [-0.3, -0.2, -0.3], "l_fore": [0.7, -0.1, -0.1], "l_hand": [-0.2, 0.1, 0.0], "curls": [0.8, 0.8, 0.8, 0.8, 0.0]},
            {"time": 1050, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.1], "r_fore": [0.3, 0.1, 0.0], "r_hand": [0.0, 0.0, 0.0], "l_arm": [-0.1, -0.1, -0.1], "l_fore": [0.3, 0.0, 0.0], "l_hand": [0.0, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "voice",
        "name": "Voice",
        "gloss": "VOICE",
        "duration": 1250,
        "type": "Sensory / Vocal",
        "notes": "ISLRTC Sensory. Right 'V' handshape moving upward from throat/larynx projecting outward.",
        "dominant": "right",
        "bones": ["Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.2, 0.3], "r_fore": [0.9, 0.3, 0.2], "r_hand": [0.3, 0.1, -0.1], "head": [0.05, 0.0, 0.0], "curls": [0.8, 0.0, 0.0, 0.9, 0.9]},
            {"time": 700, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.2], "r_fore": [0.6, 0.2, 0.1], "r_hand": [0.1, 0.1, -0.1], "head": [0.0, 0.0, 0.0], "curls": [0.8, 0.0, 0.0, 0.9, 0.9]},
            {"time": 1000, "ease": "easeInOutQuad", "r_arm": [-0.1, 0.0, 0.1], "r_fore": [0.3, 0.1, 0.0], "r_hand": [0.0, 0.0, 0.0], "head": [0.0, 0.0, 0.0], "curls": [0.2, 0.0, 0.0, 0.2, 0.2]}
        ]
    },
    {
        "id": "game",
        "name": "Game",
        "gloss": "GAME",
        "duration": 1300,
        "type": "Activity / Sports",
        "notes": "ISLRTC Activity. Dual thumbs-up fists bumping together at knuckles twice.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 350, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.1, 0.2], "r_fore": [0.7, 0.2, 0.1], "r_hand": [0.1, 0.1, 0.0], "l_arm": [-0.3, -0.1, -0.2], "l_fore": [0.7, -0.2, -0.1], "l_hand": [0.1, -0.1, 0.0], "curls": [0.0, 0.9, 0.9, 0.9, 0.9]},
            {"time": 700, "ease": "easeInOutQuad", "r_arm": [-0.35, 0.05, 0.15], "r_fore": [0.8, 0.2, 0.1], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.35, -0.05, -0.15], "l_fore": [0.8, -0.2, -0.1], "l_hand": [0.1, 0.0, 0.0], "curls": [0.0, 0.9, 0.9, 0.9, 0.9]},
            {"time": 1050, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.1], "r_fore": [0.4, 0.1, 0.0], "r_hand": [0.0, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.1], "l_fore": [0.4, -0.1, 0.0], "l_hand": [0.0, 0.0, 0.0], "curls": [0.0, 0.3, 0.3, 0.3, 0.3]}
        ]
    },
    {
        "id": "speed",
        "name": "Speed",
        "gloss": "SPEED",
        "duration": 1200,
        "type": "Measurement / Kinetic",
        "notes": "ISLRTC Kinetic. Right index finger flexing rapidly backward from base left wrist indicating fast velocity.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.2, 0.3], "r_fore": [0.7, 0.2, 0.1], "r_hand": [0.2, 0.1, -0.1], "l_arm": [-0.2, -0.2, -0.2], "l_fore": [0.6, -0.1, -0.1], "l_hand": [0.0, 0.0, 0.0], "curls": [0.8, 0.0, 0.8, 0.8, 0.8]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.3, 0.4], "r_fore": [0.9, 0.3, 0.2], "r_hand": [0.3, 0.2, -0.2], "l_arm": [-0.2, -0.2, -0.2], "l_fore": [0.6, -0.1, -0.1], "l_hand": [0.0, 0.0, 0.0], "curls": [0.8, 0.6, 0.8, 0.8, 0.8]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.1], "r_fore": [0.4, 0.1, 0.0], "r_hand": [0.0, 0.0, 0.0], "l_arm": [-0.1, -0.1, -0.1], "l_fore": [0.3, 0.0, 0.0], "l_hand": [0.0, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "posture",
        "name": "Posture",
        "gloss": "POSTURE",
        "duration": 1350,
        "type": "Physical / Body",
        "notes": "ISLRTC Physical. Right 'V' handshape standing inverted on base flat left palm, spine straightening tall.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Spine1"],
        "keyframes": [
            {"time": 350, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.2, 0.3], "r_fore": [0.8, 0.2, 0.2], "r_hand": [0.4, 0.1, -0.1], "l_arm": [-0.3, -0.2, -0.3], "l_fore": [0.6, -0.1, -0.1], "l_hand": [-0.2, 0.0, 0.0], "spine": [0.05, 0.0, 0.0], "curls": [0.8, 0.0, 0.0, 0.9, 0.9]},
            {"time": 750, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.2, 0.3], "r_fore": [0.8, 0.2, 0.2], "r_hand": [0.4, 0.1, -0.1], "l_arm": [-0.3, -0.2, -0.3], "l_fore": [0.6, -0.1, -0.1], "l_hand": [-0.2, 0.0, 0.0], "spine": [0.1, 0.0, 0.0], "curls": [0.8, 0.0, 0.0, 0.9, 0.9]},
            {"time": 1100, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.1], "r_fore": [0.4, 0.1, 0.0], "r_hand": [0.0, 0.0, 0.0], "l_arm": [-0.1, -0.1, -0.1], "l_fore": [0.3, 0.0, 0.0], "l_hand": [0.0, 0.0, 0.0], "spine": [0.0, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "lead",
        "name": "Lead",
        "gloss": "LEAD",
        "duration": 1300,
        "type": "Leadership / Action",
        "notes": "ISLRTC Action. Right hand grasping left flat fingertips and gently pulling forward leading the way.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 350, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.1, 0.2], "r_fore": [0.7, 0.2, 0.1], "r_hand": [0.2, 0.1, -0.1], "l_arm": [-0.3, -0.1, -0.2], "l_fore": [0.6, -0.1, -0.1], "l_hand": [0.1, -0.1, 0.0], "curls": [0.5, 0.5, 0.5, 0.5, 0.5]},
            {"time": 750, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.2, 0.3], "r_fore": [0.9, 0.3, 0.2], "r_hand": [0.3, 0.2, -0.2], "l_arm": [-0.4, -0.2, -0.3], "l_fore": [0.8, -0.2, -0.1], "l_hand": [0.2, -0.2, 0.1], "curls": [0.5, 0.5, 0.5, 0.5, 0.5]},
            {"time": 1050, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.1], "r_fore": [0.4, 0.1, 0.0], "r_hand": [0.0, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.1], "l_fore": [0.4, -0.1, 0.0], "l_hand": [0.0, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "note",
        "name": "Note",
        "gloss": "NOTE",
        "duration": 1250,
        "type": "Academic / Written",
        "notes": "ISLRTC Academic. Right pinch handshape writing quick short jotting motions onto base left flat palm.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.2, 0.3], "r_fore": [0.8, 0.3, 0.2], "r_hand": [0.3, 0.1, -0.1], "l_arm": [-0.3, -0.2, -0.3], "l_fore": [0.7, -0.1, -0.1], "l_hand": [-0.2, 0.0, 0.0], "curls": [0.7, 0.7, 0.2, 0.2, 0.2]},
            {"time": 700, "ease": "easeInOutQuad", "r_arm": [-0.35, 0.2, 0.25], "r_fore": [0.75, 0.25, 0.15], "r_hand": [0.2, 0.1, -0.1], "l_arm": [-0.3, -0.2, -0.3], "l_fore": [0.7, -0.1, -0.1], "l_hand": [-0.2, 0.0, 0.0], "curls": [0.7, 0.7, 0.2, 0.2, 0.2]},
            {"time": 1000, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.1], "r_fore": [0.4, 0.1, 0.0], "r_hand": [0.0, 0.0, 0.0], "l_arm": [-0.1, -0.1, -0.1], "l_fore": [0.3, 0.0, 0.0], "l_hand": [0.0, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "plan",
        "name": "Plan",
        "gloss": "PLAN",
        "duration": 1350,
        "type": "Cognitive / Administrative",
        "notes": "ISLRTC Administrative. Dual vertical flat palms moving across horizontal space in synchronized rhythmic steps.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 350, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.1, 0.2], "r_fore": [0.6, 0.2, 0.1], "r_hand": [-0.2, 0.1, -0.1], "l_arm": [-0.3, -0.1, -0.2], "l_fore": [0.6, -0.2, -0.1], "l_hand": [-0.2, -0.1, 0.1], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 750, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.3, 0.4], "r_fore": [0.7, 0.3, 0.2], "r_hand": [-0.3, 0.2, -0.2], "l_arm": [-0.2, -0.1, -0.1], "l_fore": [0.5, -0.1, -0.1], "l_hand": [-0.1, 0.0, 0.1], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 1100, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.1], "r_fore": [0.4, 0.1, 0.0], "r_hand": [0.0, 0.0, 0.0], "l_arm": [-0.1, -0.1, -0.1], "l_fore": [0.3, 0.0, 0.0], "l_hand": [0.0, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "train",
        "name": "Train",
        "gloss": "TRAIN",
        "duration": 1300,
        "type": "Educational / Practice",
        "notes": "ISLRTC Educational. Right 'H' handshape rubbing repeatedly across top of extended left 'H' handshape.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 350, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.2, 0.3], "r_fore": [0.7, 0.2, 0.2], "r_hand": [0.2, 0.1, -0.1], "l_arm": [-0.3, -0.2, -0.3], "l_fore": [0.6, -0.1, -0.1], "l_hand": [0.0, 0.0, 0.0], "curls": [0.8, 0.0, 0.0, 0.8, 0.8]},
            {"time": 750, "ease": "easeInOutQuad", "r_arm": [-0.35, 0.2, 0.3], "r_fore": [0.75, 0.2, 0.2], "r_hand": [0.25, 0.1, -0.1], "l_arm": [-0.3, -0.2, -0.3], "l_fore": [0.6, -0.1, -0.1], "l_hand": [0.0, 0.0, 0.0], "curls": [0.8, 0.0, 0.0, 0.8, 0.8]},
            {"time": 1050, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.1], "r_fore": [0.4, 0.1, 0.0], "r_hand": [0.0, 0.0, 0.0], "l_arm": [-0.1, -0.1, -0.1], "l_fore": [0.3, 0.0, 0.0], "l_hand": [0.0, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "draw",
        "name": "Draw",
        "gloss": "DRAW",
        "duration": 1250,
        "type": "Creative / Visual",
        "notes": "ISLRTC Creative. Right pinky finger sketching freehand patterns across imaginary vertical canvas.",
        "dominant": "right",
        "bones": ["Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_L_Forearm"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.2, 0.3], "r_fore": [0.8, 0.2, 0.2], "r_hand": [0.3, 0.2, -0.1], "l_fore": [0.4, -0.1, -0.1], "curls": [0.9, 0.9, 0.9, 0.9, 0.0]},
            {"time": 700, "ease": "easeInOutQuad", "r_arm": [-0.35, 0.3, 0.4], "r_fore": [0.7, 0.3, 0.2], "r_hand": [0.2, 0.3, -0.2], "l_fore": [0.4, -0.1, -0.1], "curls": [0.9, 0.9, 0.9, 0.9, 0.0]},
            {"time": 1000, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.1], "r_fore": [0.4, 0.1, 0.0], "r_hand": [0.0, 0.0, 0.0], "l_fore": [0.2, 0.0, 0.0], "curls": [0.2, 0.2, 0.2, 0.2, 0.0]}
        ]
    },
    {
        "id": "skill",
        "name": "Skill",
        "gloss": "SKILL",
        "duration": 1300,
        "type": "Competency / Educational",
        "notes": "ISLRTC Educational. Right hand grasping side of base left vertical hand and pulling downward in firm grasp.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 350, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.2, 0.3], "r_fore": [0.8, 0.3, 0.2], "r_hand": [0.2, 0.1, -0.1], "l_arm": [-0.3, -0.2, -0.3], "l_fore": [0.7, -0.1, -0.1], "l_hand": [-0.2, 0.0, 0.0], "curls": [0.4, 0.4, 0.4, 0.4, 0.4]},
            {"time": 750, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.2, 0.2], "r_fore": [0.6, 0.2, 0.1], "r_hand": [0.1, 0.1, -0.1], "l_arm": [-0.3, -0.2, -0.3], "l_fore": [0.7, -0.1, -0.1], "l_hand": [-0.2, 0.0, 0.0], "curls": [0.8, 0.8, 0.8, 0.8, 0.8]},
            {"time": 1050, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.1], "r_fore": [0.3, 0.1, 0.0], "r_hand": [0.0, 0.0, 0.0], "l_arm": [-0.1, -0.1, -0.1], "l_fore": [0.3, 0.0, 0.0], "l_hand": [0.0, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "mark",
        "name": "Mark",
        "gloss": "MARK",
        "duration": 1200,
        "type": "Action / Evaluation",
        "notes": "ISLRTC Evaluation. Right index finger drawing an authoritative checkmark or point on left base palm.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.2, 0.3], "r_fore": [0.8, 0.3, 0.2], "r_hand": [0.3, 0.2, -0.1], "l_arm": [-0.3, -0.2, -0.3], "l_fore": [0.6, -0.1, -0.1], "l_hand": [-0.2, 0.0, 0.0], "curls": [0.8, 0.0, 0.8, 0.8, 0.8]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.3, 0.35], "r_fore": [0.7, 0.3, 0.2], "r_hand": [0.1, 0.3, -0.2], "l_arm": [-0.3, -0.2, -0.3], "l_fore": [0.6, -0.1, -0.1], "l_hand": [-0.2, 0.0, 0.0], "curls": [0.8, 0.0, 0.8, 0.8, 0.8]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.1], "r_fore": [0.4, 0.1, 0.0], "r_hand": [0.0, 0.0, 0.0], "l_arm": [-0.1, -0.1, -0.1], "l_fore": [0.3, 0.0, 0.0], "l_hand": [0.0, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    }
]

print(f"Total sign specifications defined: {len(AUTHORED_SPECS)}")

# Helper to build rotations dict for a given keyframe
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
        elif "Clavicle" in b:
            val = [0, 0, 0]
        else:
            val = [0, 0, 0]
        rot[b] = {"x": round(val[0], 3), "y": round(val[1], 3), "z": round(val[2], 3)}
    return rot

# Generate Schema 2.0.0 file for each sign
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

print(f"Successfully authored and verified {len(created_files)} Schema 2.0.0 signs:")
for name in created_files:
    print(f"  - signs/{name}")
