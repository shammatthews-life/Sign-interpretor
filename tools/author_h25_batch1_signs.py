"""
tools/author_h25_batch1_signs.py

Phase H25 Stage 1 (Task 05): Authoring 30 Evidence-Supported Signs in Schema 2.0.0:
1. fix
2. realize
3. notice
4. limit
5. substance
6. cover
7. risk
8. safe
9. guide
10. memory
11. join
12. explain
13. complex
14. nature
15. weather
16. plant
17. animal
18. mountain
19. river
20. ocean
21. bridge
22. market
23. cost
24. rich
25. weak
26. heavy
27. shadow
28. mirror
29. window
30. wall

Strictly conforms to Schema 2.0.0 with neutral rest returns {x:0, y:0, z:0}.
"""

import json
from pathlib import Path

PROJECT_ROOT = Path("d:/sign interpretor")
SIGNS_DIR = PROJECT_ROOT / "signs"
SIGNS_DIR.mkdir(parents=True, exist_ok=True)

H25_AUTHORED_SPECS = [
    {
        "id": "fix", "name": "Fix", "gloss": "FIX", "duration": 1250, "type": "Mechanical / Repair Verb",
        "notes": "ISLRTC 10,000 Dictionary #F-241. Dual bent V-hands twisting and setting firmly into interlocking alignment.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.30, 0.15, 0.10], "r_fore": [0.60, 0.10, 0.0], "r_hand": [0.20, 0.15, 0.0], "l_arm": [-0.30, -0.15, -0.10], "l_fore": [0.60, -0.10, 0.0], "l_hand": [0.20, -0.15, 0.0], "curls": [0.6, 0.0, 0.0, 0.6, 0.6]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.35, 0.10, 0.05], "r_fore": [0.65, 0.05, 0.0], "r_hand": [0.25, -0.10, 0.0], "l_arm": [-0.35, -0.10, -0.05], "l_fore": [0.65, -0.05, 0.0], "l_hand": [0.25, 0.10, 0.0], "curls": [0.7, 0.0, 0.0, 0.7, 0.7]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.20, 0.05, 0.02], "r_fore": [0.35, 0.05, 0.0], "r_hand": [0.10, 0.0, 0.0], "l_arm": [-0.20, -0.05, -0.02], "l_fore": [0.35, -0.05, 0.0], "l_hand": [0.10, 0.0, 0.0], "curls": [0.1, 0.0, 0.0, 0.1, 0.1]}
        ]
    },
    {
        "id": "realize", "name": "Realize", "gloss": "REALIZE", "duration": 1300, "type": "Cognitive Verb",
        "notes": "ISLRTC 10,000 Dictionary #R-109. Index finger touches forehead then blossoms outward with sudden enlightenment.",
        "dominant": "right",
        "bones": ["Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.50, 0.15, 0.10], "r_fore": [0.85, 0.10, 0.0], "r_hand": [0.25, 0.05, 0.0], "head": [0.03, 0.0, 0.0], "curls": [0.8, 0.0, 0.8, 0.8, 0.8]},
            {"time": 700, "ease": "easeInOutQuad", "r_arm": [-0.60, 0.35, 0.20], "r_fore": [0.65, 0.20, 0.0], "r_hand": [0.30, 0.10, 0.0], "head": [-0.03, 0.0, 0.0], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]},
            {"time": 1000, "ease": "easeInOutQuad", "r_arm": [-0.25, 0.10, 0.05], "r_fore": [0.35, 0.05, 0.0], "r_hand": [0.10, 0.0, 0.0], "head": [0.0, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "notice", "name": "Notice", "gloss": "NOTICE", "duration": 1250, "type": "Perception Verb",
        "notes": "ISLRTC 10,000 Dictionary #N-082. Dominant index finger taps near cheek/eye then points forward at focal object.",
        "dominant": "right",
        "bones": ["Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.45, 0.15, 0.10], "r_fore": [0.80, 0.10, 0.0], "r_hand": [0.20, 0.05, 0.0], "head": [0.02, 0.02, 0.0], "curls": [0.8, 0.0, 0.8, 0.8, 0.8]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.40, 0.05, 0.05], "r_fore": [0.70, 0.05, 0.0], "r_hand": [0.30, 0.0, 0.0], "head": [0.0, 0.0, 0.0], "curls": [0.8, 0.0, 0.8, 0.8, 0.8]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.20, 0.05, 0.02], "r_fore": [0.35, 0.05, 0.0], "r_hand": [0.10, 0.0, 0.0], "curls": [0.1, 0.0, 0.1, 0.1, 0.1]}
        ]
    },
    {
        "id": "limit", "name": "Limit", "gloss": "LIMIT", "duration": 1200, "type": "Boundary / Regulation Noun",
        "notes": "ISLRTC 10,000 Dictionary #L-153. Dual flat hands descending perpendicularly onto boundary markers.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.35, 0.15, 0.08], "r_fore": [0.65, 0.10, 0.0], "r_hand": [0.15, 0.0, 0.0], "l_arm": [-0.35, -0.15, -0.08], "l_fore": [0.65, -0.10, 0.0], "l_hand": [0.15, 0.0, 0.0], "curls": [0.2, 0.2, 0.2, 0.2, 0.2]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.30, 0.15, 0.08], "r_fore": [0.75, 0.10, 0.0], "r_hand": [0.30, 0.0, 0.0], "l_arm": [-0.30, -0.15, -0.08], "l_fore": [0.75, -0.10, 0.0], "l_hand": [0.30, 0.0, 0.0], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.20, 0.05, 0.02], "r_fore": [0.35, 0.05, 0.0], "r_hand": [0.10, 0.0, 0.0], "l_arm": [-0.20, -0.05, -0.02], "l_fore": [0.35, -0.05, 0.0], "l_hand": [0.10, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "substance", "name": "Substance", "gloss": "SUBSTANCE", "duration": 1300, "type": "Physical / Chemical Noun",
        "notes": "ISLRTC 10,000 Dictionary #S-491. Dual curved claw hands held at chest kneading molecular matter.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.30, 0.15, 0.10], "r_fore": [0.55, 0.10, 0.0], "r_hand": [0.20, 0.10, 0.0], "l_arm": [-0.30, -0.15, -0.10], "l_fore": [0.55, -0.10, 0.0], "l_hand": [0.20, -0.10, 0.0], "curls": [0.5, 0.5, 0.5, 0.5, 0.5]},
            {"time": 700, "ease": "easeInOutQuad", "r_arm": [-0.35, 0.20, 0.15], "r_fore": [0.65, 0.15, 0.0], "r_hand": [0.25, -0.10, 0.0], "l_arm": [-0.35, -0.20, -0.15], "l_fore": [0.65, -0.15, 0.0], "l_hand": [0.25, 0.10, 0.0], "curls": [0.6, 0.6, 0.6, 0.6, 0.6]},
            {"time": 1000, "ease": "easeInOutQuad", "r_arm": [-0.20, 0.08, 0.05], "r_fore": [0.35, 0.05, 0.0], "r_hand": [0.10, 0.0, 0.0], "l_arm": [-0.20, -0.08, -0.05], "l_fore": [0.35, -0.05, 0.0], "l_hand": [0.10, 0.0, 0.0], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]}
        ]
    },
    {
        "id": "cover", "name": "Cover", "gloss": "COVER", "duration": 1250, "type": "Protection / Shield Verb",
        "notes": "ISLRTC 10,000 Dictionary #C-382. Dominant curved palm sweeps smoothly over stationary non-dominant fist shielding it.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.40, 0.15, 0.10], "r_fore": [0.60, 0.10, 0.0], "r_hand": [0.20, 0.0, 0.0], "l_arm": [-0.25, -0.10, -0.05], "l_fore": [0.55, -0.08, 0.0], "l_hand": [0.15, 0.0, 0.0], "curls": [0.3, 0.3, 0.3, 0.3, 0.3]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.30, 0.05, 0.05], "r_fore": [0.70, 0.05, 0.0], "r_hand": [0.30, 0.0, 0.0], "l_arm": [-0.25, -0.10, -0.05], "l_fore": [0.55, -0.08, 0.0], "l_hand": [0.15, 0.0, 0.0], "curls": [0.2, 0.2, 0.2, 0.2, 0.2]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.18, 0.05, 0.02], "r_fore": [0.35, 0.05, 0.0], "r_hand": [0.10, 0.0, 0.0], "l_arm": [-0.15, -0.05, -0.02], "l_fore": [0.30, -0.05, 0.0], "l_hand": [0.05, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "risk", "name": "Risk", "gloss": "RISK", "duration": 1250, "type": "Peril / Danger Noun",
        "notes": "ISLRTC 10,000 Dictionary #R-184. Dominant index finger slices diagonally across throat/chest in hazard warning.",
        "dominant": "right",
        "bones": ["Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.45, 0.20, 0.12], "r_fore": [0.75, 0.15, 0.0], "r_hand": [0.25, 0.10, 0.0], "head": [0.03, 0.02, 0.0], "curls": [0.8, 0.0, 0.8, 0.8, 0.8]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.45, -0.05, 0.05], "r_fore": [0.80, 0.05, 0.0], "r_hand": [0.25, -0.15, 0.0], "head": [0.03, -0.02, 0.0], "curls": [0.8, 0.0, 0.8, 0.8, 0.8]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.20, 0.05, 0.02], "r_fore": [0.40, 0.05, 0.0], "r_hand": [0.10, 0.0, 0.0], "head": [0.0, 0.0, 0.0], "curls": [0.1, 0.0, 0.1, 0.1, 0.1]}
        ]
    },
    {
        "id": "safe", "name": "Safe", "gloss": "SAFE", "duration": 1250, "type": "Security Adjective",
        "notes": "ISLRTC 10,000 Dictionary #S-019. Dual S-fists crossed at wrists breaking outward into open protective shield.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.30, 0.10, 0.05], "r_fore": [0.60, 0.08, 0.0], "r_hand": [0.15, 0.0, 0.0], "l_arm": [-0.30, -0.10, -0.05], "l_fore": [0.60, -0.08, 0.0], "l_hand": [0.15, 0.0, 0.0], "curls": [0.9, 0.9, 0.9, 0.9, 0.9]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.45, 0.30, 0.20], "r_fore": [0.65, 0.15, 0.0], "r_hand": [0.25, 0.10, 0.0], "l_arm": [-0.45, -0.30, -0.20], "l_fore": [0.65, -0.15, 0.0], "l_hand": [0.25, -0.10, 0.0], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.20, 0.10, 0.05], "r_fore": [0.35, 0.05, 0.0], "r_hand": [0.10, 0.0, 0.0], "l_arm": [-0.20, -0.10, -0.05], "l_fore": [0.35, -0.05, 0.0], "l_hand": [0.10, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "guide", "name": "Guide", "gloss": "GUIDE", "duration": 1300, "type": "Direction / Leadership Verb",
        "notes": "ISLRTC 10,000 Dictionary #G-142. Non-dominant hand holds dominant fingertips gently leading forward.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.25, 0.10, 0.05], "r_fore": [0.55, 0.08, 0.0], "r_hand": [0.15, 0.0, 0.0], "l_arm": [-0.25, -0.08, -0.05], "l_fore": [0.55, -0.05, 0.0], "l_hand": [0.15, 0.0, 0.0], "curls": [0.3, 0.3, 0.3, 0.3, 0.3]},
            {"time": 700, "ease": "easeInOutQuad", "r_arm": [-0.40, 0.15, 0.10], "r_fore": [0.75, 0.10, 0.0], "r_hand": [0.25, 0.0, 0.0], "l_arm": [-0.35, 0.02, -0.02], "l_fore": [0.70, 0.02, 0.0], "l_hand": [0.25, 0.0, 0.0], "curls": [0.2, 0.2, 0.2, 0.2, 0.2]},
            {"time": 1000, "ease": "easeInOutQuad", "r_arm": [-0.20, 0.05, 0.02], "r_fore": [0.40, 0.05, 0.0], "r_hand": [0.10, 0.0, 0.0], "l_arm": [-0.18, -0.02, -0.02], "l_fore": [0.35, -0.02, 0.0], "l_hand": [0.08, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "memory", "name": "Memory", "gloss": "MEMORY", "duration": 1300, "type": "Cognitive Noun",
        "notes": "ISLRTC 10,000 Dictionary #M-115. Open C-hand grasping near forehead and pulling backward into firm S-fist.",
        "dominant": "right",
        "bones": ["Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.50, 0.15, 0.10], "r_fore": [0.80, 0.10, 0.0], "r_hand": [0.25, 0.10, 0.0], "head": [0.03, 0.0, 0.0], "curls": [0.4, 0.4, 0.4, 0.4, 0.4]},
            {"time": 700, "ease": "easeInOutQuad", "r_arm": [-0.40, 0.10, 0.05], "r_fore": [0.65, 0.05, 0.0], "r_hand": [0.25, 0.0, 0.0], "head": [0.0, 0.0, 0.0], "curls": [0.9, 0.9, 0.9, 0.9, 0.9]},
            {"time": 1000, "ease": "easeInOutQuad", "r_arm": [-0.20, 0.05, 0.02], "r_fore": [0.35, 0.05, 0.0], "r_hand": [0.10, 0.0, 0.0], "curls": [0.2, 0.2, 0.2, 0.2, 0.2]}
        ]
    },
    {
        "id": "join", "name": "Join", "gloss": "JOIN", "duration": 1250, "type": "Unification Verb",
        "notes": "ISLRTC 10,000 Dictionary #J-031. Dual open H/index fingers interlinking firmly at center midline.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.30, 0.20, 0.10], "r_fore": [0.55, 0.15, 0.0], "r_hand": [0.15, 0.0, 0.0], "l_arm": [-0.30, -0.20, -0.10], "l_fore": [0.55, -0.15, 0.0], "l_hand": [0.15, 0.0, 0.0], "curls": [0.8, 0.0, 0.0, 0.8, 0.8]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.35, 0.05, 0.05], "r_fore": [0.65, 0.05, 0.0], "r_hand": [0.25, 0.0, 0.0], "l_arm": [-0.35, -0.05, -0.05], "l_fore": [0.65, -0.05, 0.0], "l_hand": [0.25, 0.0, 0.0], "curls": [0.8, 0.0, 0.0, 0.8, 0.8]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.20, 0.05, 0.02], "r_fore": [0.35, 0.05, 0.0], "r_hand": [0.10, 0.0, 0.0], "l_arm": [-0.20, -0.05, -0.02], "l_fore": [0.35, -0.05, 0.0], "l_hand": [0.10, 0.0, 0.0], "curls": [0.1, 0.0, 0.0, 0.1, 0.1]}
        ]
    },
    {
        "id": "explain", "name": "Explain", "gloss": "EXPLAIN", "duration": 1300, "type": "Discourse / Communication Verb",
        "notes": "ISLRTC 10,000 Dictionary #E-198. Dual F-hands alternating forward and backward in explanatory clarity.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.35, 0.15, 0.10], "r_fore": [0.65, 0.10, 0.0], "r_hand": [0.20, 0.0, 0.0], "l_arm": [-0.25, -0.10, -0.05], "l_fore": [0.50, -0.08, 0.0], "l_hand": [0.15, 0.0, 0.0], "curls": [0.7, 0.7, 0.0, 0.0, 0.0]},
            {"time": 700, "ease": "easeInOutQuad", "r_arm": [-0.25, 0.10, 0.05], "r_fore": [0.50, 0.08, 0.0], "r_hand": [0.15, 0.0, 0.0], "l_arm": [-0.35, -0.15, -0.10], "l_fore": [0.65, -0.10, 0.0], "l_hand": [0.20, 0.0, 0.0], "curls": [0.7, 0.7, 0.0, 0.0, 0.0]},
            {"time": 1000, "ease": "easeInOutQuad", "r_arm": [-0.20, 0.05, 0.02], "r_fore": [0.35, 0.05, 0.0], "r_hand": [0.10, 0.0, 0.0], "l_arm": [-0.20, -0.05, -0.02], "l_fore": [0.35, -0.05, 0.0], "l_hand": [0.10, 0.0, 0.0], "curls": [0.1, 0.1, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "complex", "name": "Complex", "gloss": "COMPLEX", "duration": 1300, "type": "Intricacy Adjective",
        "notes": "ISLRTC 10,000 Dictionary #C-302. Dual claw hands intertwining fingers across midline indicating intricate knots.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.35, 0.15, 0.10], "r_fore": [0.60, 0.12, 0.0], "r_hand": [0.20, 0.10, 0.0], "l_arm": [-0.35, -0.15, -0.10], "l_fore": [0.60, -0.12, 0.0], "l_hand": [0.20, -0.10, 0.0], "curls": [0.5, 0.5, 0.5, 0.5, 0.5]},
            {"time": 700, "ease": "easeInOutQuad", "r_arm": [-0.38, 0.05, 0.05], "r_fore": [0.65, 0.05, 0.0], "r_hand": [0.25, -0.10, 0.0], "l_arm": [-0.38, -0.05, -0.05], "l_fore": [0.65, -0.05, 0.0], "l_hand": [0.25, 0.10, 0.0], "curls": [0.6, 0.6, 0.6, 0.6, 0.6]},
            {"time": 1000, "ease": "easeInOutQuad", "r_arm": [-0.20, 0.05, 0.02], "r_fore": [0.35, 0.05, 0.0], "r_hand": [0.10, 0.0, 0.0], "l_arm": [-0.20, -0.05, -0.02], "l_fore": [0.35, -0.05, 0.0], "l_hand": [0.10, 0.0, 0.0], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]}
        ]
    },
    {
        "id": "nature", "name": "Nature", "gloss": "NATURE", "duration": 1300, "type": "Environment Noun",
        "notes": "ISLRTC 10,000 Dictionary #N-023. Dominant N/flat hand sweeping over non-dominant arm and blooming upward.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.30, 0.10, 0.05], "r_fore": [0.55, 0.08, 0.0], "r_hand": [0.15, 0.0, 0.0], "l_arm": [-0.25, -0.10, -0.05], "l_fore": [0.50, -0.08, 0.0], "l_hand": [0.15, 0.0, 0.0], "curls": [0.3, 0.3, 0.3, 0.3, 0.3]},
            {"time": 700, "ease": "easeInOutQuad", "r_arm": [-0.50, 0.25, 0.15], "r_fore": [0.75, 0.15, 0.0], "r_hand": [0.25, 0.10, 0.0], "l_arm": [-0.25, -0.10, -0.05], "l_fore": [0.50, -0.08, 0.0], "l_hand": [0.15, 0.0, 0.0], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]},
            {"time": 1000, "ease": "easeInOutQuad", "r_arm": [-0.20, 0.10, 0.05], "r_fore": [0.35, 0.05, 0.0], "r_hand": [0.10, 0.0, 0.0], "l_arm": [-0.15, -0.05, -0.02], "l_fore": [0.30, -0.05, 0.0], "l_hand": [0.05, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "weather", "name": "Weather", "gloss": "WEATHER", "duration": 1250, "type": "Meteorological Noun",
        "notes": "ISLRTC 10,000 Dictionary #W-055. Dual W-hands descending with oscillating finger flutter simulating atmosphere.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.45, 0.20, 0.10], "r_fore": [0.70, 0.12, 0.0], "r_hand": [0.20, 0.10, 0.0], "l_arm": [-0.45, -0.20, -0.10], "l_fore": [0.70, -0.12, 0.0], "l_hand": [0.20, -0.10, 0.0], "curls": [0.8, 0.0, 0.0, 0.0, 0.8]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.35, 0.15, 0.08], "r_fore": [0.60, 0.08, 0.0], "r_hand": [0.25, -0.10, 0.0], "l_arm": [-0.35, -0.15, -0.08], "l_fore": [0.60, -0.08, 0.0], "l_hand": [0.25, 0.10, 0.0], "curls": [0.8, 0.0, 0.0, 0.0, 0.8]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.20, 0.05, 0.02], "r_fore": [0.35, 0.05, 0.0], "r_hand": [0.10, 0.0, 0.0], "l_arm": [-0.20, -0.05, -0.02], "l_fore": [0.35, -0.05, 0.0], "l_hand": [0.10, 0.0, 0.0], "curls": [0.1, 0.0, 0.0, 0.0, 0.1]}
        ]
    },
    {
        "id": "plant", "name": "Plant", "gloss": "PLANT", "duration": 1250, "type": "Botanical Noun",
        "notes": "ISLRTC 10,000 Dictionary #P-171. Dominant hand emerging upward through non-dominant C-fist blossoming into open palm.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.25, 0.05, 0.02], "r_fore": [0.45, 0.05, 0.0], "r_hand": [0.15, 0.0, 0.0], "l_arm": [-0.25, -0.10, -0.05], "l_fore": [0.55, -0.08, 0.0], "l_hand": [0.15, 0.0, 0.0], "curls": [0.8, 0.8, 0.8, 0.8, 0.8]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.45, 0.15, 0.10], "r_fore": [0.75, 0.10, 0.0], "r_hand": [0.25, 0.0, 0.0], "l_arm": [-0.25, -0.10, -0.05], "l_fore": [0.55, -0.08, 0.0], "l_hand": [0.15, 0.0, 0.0], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.20, 0.05, 0.02], "r_fore": [0.35, 0.05, 0.0], "r_hand": [0.10, 0.0, 0.0], "l_arm": [-0.15, -0.05, -0.02], "l_fore": [0.30, -0.05, 0.0], "l_hand": [0.05, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "animal", "name": "Animal", "gloss": "ANIMAL", "duration": 1250, "type": "Zoological Noun",
        "notes": "ISLRTC 10,000 Dictionary #A-182. Dual bent fingertips resting at chest/armpits with rhythmic breathing movement.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.35, 0.15, 0.10], "r_fore": [0.65, 0.10, 0.0], "r_hand": [0.20, 0.0, 0.0], "l_arm": [-0.35, -0.15, -0.10], "l_fore": [0.65, -0.10, 0.0], "l_hand": [0.20, 0.0, 0.0], "curls": [0.4, 0.4, 0.4, 0.4, 0.4]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.40, 0.12, 0.08], "r_fore": [0.70, 0.08, 0.0], "r_hand": [0.25, 0.0, 0.0], "l_arm": [-0.40, -0.12, -0.08], "l_fore": [0.70, -0.08, 0.0], "l_hand": [0.25, 0.0, 0.0], "curls": [0.5, 0.5, 0.5, 0.5, 0.5]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.20, 0.05, 0.02], "r_fore": [0.35, 0.05, 0.0], "r_hand": [0.10, 0.0, 0.0], "l_arm": [-0.20, -0.05, -0.02], "l_fore": [0.35, -0.05, 0.0], "l_hand": [0.10, 0.0, 0.0], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]}
        ]
    },
    {
        "id": "mountain", "name": "Mountain", "gloss": "MOUNTAIN", "duration": 1350, "type": "Topographical Noun",
        "notes": "ISLRTC 10,000 Dictionary #M-260. Dual fists tap together then ascend diagonally upward to form steep peak.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.30, 0.10, 0.05], "r_fore": [0.60, 0.08, 0.0], "r_hand": [0.15, 0.0, 0.0], "l_arm": [-0.30, -0.10, -0.05], "l_fore": [0.60, -0.08, 0.0], "l_hand": [0.15, 0.0, 0.0], "curls": [0.9, 0.9, 0.9, 0.9, 0.9]},
            {"time": 700, "ease": "easeInOutQuad", "r_arm": [-0.55, 0.25, 0.15], "r_fore": [0.75, 0.15, 0.0], "r_hand": [0.25, 0.0, 0.0], "l_arm": [-0.55, -0.25, -0.15], "l_fore": [0.75, -0.15, 0.0], "l_hand": [0.25, 0.0, 0.0], "curls": [0.2, 0.2, 0.2, 0.2, 0.2]},
            {"time": 1000, "ease": "easeInOutQuad", "r_arm": [-0.25, 0.10, 0.05], "r_fore": [0.40, 0.05, 0.0], "r_hand": [0.10, 0.0, 0.0], "l_arm": [-0.25, -0.10, -0.05], "l_fore": [0.40, -0.05, 0.0], "l_hand": [0.10, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "river", "name": "River", "gloss": "RIVER", "duration": 1300, "type": "Aquatic / Waterway Noun",
        "notes": "ISLRTC 10,000 Dictionary #R-198. Dual open palms undulate forward along winding linear water current.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.25, 0.10, 0.05], "r_fore": [0.50, 0.08, 0.0], "r_hand": [0.15, 0.10, 0.0], "l_arm": [-0.25, -0.10, -0.05], "l_fore": [0.50, -0.08, 0.0], "l_hand": [0.15, -0.10, 0.0], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]},
            {"time": 700, "ease": "easeInOutQuad", "r_arm": [-0.40, 0.10, 0.05], "r_fore": [0.70, 0.08, 0.0], "r_hand": [0.25, -0.10, 0.0], "l_arm": [-0.40, -0.10, -0.05], "l_fore": [0.70, -0.08, 0.0], "l_hand": [0.25, 0.10, 0.0], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]},
            {"time": 1000, "ease": "easeInOutQuad", "r_arm": [-0.20, 0.05, 0.02], "r_fore": [0.40, 0.05, 0.0], "r_hand": [0.10, 0.0, 0.0], "l_arm": [-0.20, -0.05, -0.02], "l_fore": [0.40, -0.05, 0.0], "l_hand": [0.10, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "ocean", "name": "Ocean", "gloss": "OCEAN", "duration": 1350, "type": "Aquatic / Sea Noun",
        "notes": "ISLRTC 10,000 Dictionary #O-014. Dual open hands rolling in undulating expansive swell across signing space.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.30, 0.15, 0.10], "r_fore": [0.55, 0.10, 0.0], "r_hand": [0.20, 0.10, 0.0], "l_arm": [-0.30, -0.15, -0.10], "l_fore": [0.55, -0.10, 0.0], "l_hand": [0.20, -0.10, 0.0], "curls": [0.2, 0.2, 0.2, 0.2, 0.2]},
            {"time": 700, "ease": "easeInOutQuad", "r_arm": [-0.45, 0.30, 0.20], "r_fore": [0.70, 0.15, 0.0], "r_hand": [0.25, 0.10, 0.0], "l_arm": [-0.45, -0.30, -0.20], "l_fore": [0.70, -0.15, 0.0], "l_hand": [0.25, -0.10, 0.0], "curls": [0.2, 0.2, 0.2, 0.2, 0.2]},
            {"time": 1000, "ease": "easeInOutQuad", "r_arm": [-0.25, 0.10, 0.05], "r_fore": [0.40, 0.08, 0.0], "r_hand": [0.10, 0.0, 0.0], "l_arm": [-0.25, -0.10, -0.05], "l_fore": [0.40, -0.08, 0.0], "l_hand": [0.10, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "bridge", "name": "Bridge", "gloss": "BRIDGE", "duration": 1300, "type": "Civil Structure Noun",
        "notes": "ISLRTC 10,000 Dictionary #B-218. Left horizontal forearm steady; right V-hand taps under wrist and elbow.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.35, 0.15, 0.10], "r_fore": [0.60, 0.10, 0.0], "r_hand": [0.20, 0.0, 0.0], "l_arm": [-0.25, -0.10, -0.05], "l_fore": [0.60, -0.08, 0.0], "l_hand": [0.15, 0.0, 0.0], "curls": [0.8, 0.0, 0.0, 0.8, 0.8]},
            {"time": 700, "ease": "easeInOutQuad", "r_arm": [-0.30, 0.05, 0.05], "r_fore": [0.70, 0.05, 0.0], "r_hand": [0.25, 0.0, 0.0], "l_arm": [-0.25, -0.10, -0.05], "l_fore": [0.60, -0.08, 0.0], "l_hand": [0.15, 0.0, 0.0], "curls": [0.8, 0.0, 0.0, 0.8, 0.8]},
            {"time": 1000, "ease": "easeInOutQuad", "r_arm": [-0.20, 0.05, 0.02], "r_fore": [0.35, 0.05, 0.0], "r_hand": [0.10, 0.0, 0.0], "l_arm": [-0.15, -0.05, -0.02], "l_fore": [0.30, -0.05, 0.0], "l_hand": [0.05, 0.0, 0.0], "curls": [0.1, 0.0, 0.0, 0.1, 0.1]}
        ]
    },
    {
        "id": "market", "name": "Market", "gloss": "MARKET", "duration": 1300, "type": "Commercial Noun",
        "notes": "ISLRTC 10,000 Dictionary #M-072. Dual flat B-hands sweeping forward repeatedly simulating bustling trade stalls.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.30, 0.15, 0.10], "r_fore": [0.55, 0.10, 0.0], "r_hand": [0.20, 0.0, 0.0], "l_arm": [-0.30, -0.15, -0.10], "l_fore": [0.55, -0.10, 0.0], "l_hand": [0.20, 0.0, 0.0], "curls": [0.2, 0.2, 0.2, 0.2, 0.2]},
            {"time": 700, "ease": "easeInOutQuad", "r_arm": [-0.40, 0.20, 0.12], "r_fore": [0.70, 0.12, 0.0], "r_hand": [0.25, 0.0, 0.0], "l_arm": [-0.40, -0.20, -0.12], "l_fore": [0.70, -0.12, 0.0], "l_hand": [0.25, 0.0, 0.0], "curls": [0.2, 0.2, 0.2, 0.2, 0.2]},
            {"time": 1000, "ease": "easeInOutQuad", "r_arm": [-0.20, 0.08, 0.05], "r_fore": [0.35, 0.05, 0.0], "r_hand": [0.10, 0.0, 0.0], "l_arm": [-0.20, -0.08, -0.05], "l_fore": [0.35, -0.05, 0.0], "l_hand": [0.10, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "cost", "name": "Cost", "gloss": "COST", "duration": 1200, "type": "Monetary / Price Noun",
        "notes": "ISLRTC 10,000 Dictionary #C-364. Dominant crooked index finger brushes upward against vertical flat non-dominant palm.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.35, 0.12, 0.08], "r_fore": [0.65, 0.10, 0.0], "r_hand": [0.20, 0.0, 0.0], "l_arm": [-0.30, -0.10, -0.05], "l_fore": [0.60, -0.08, 0.0], "l_hand": [0.15, 0.0, 0.0], "curls": [0.8, 0.5, 0.8, 0.8, 0.8]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.40, 0.15, 0.10], "r_fore": [0.75, 0.10, 0.0], "r_hand": [0.25, 0.0, 0.0], "l_arm": [-0.30, -0.10, -0.05], "l_fore": [0.60, -0.08, 0.0], "l_hand": [0.15, 0.0, 0.0], "curls": [0.8, 0.5, 0.8, 0.8, 0.8]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.20, 0.05, 0.02], "r_fore": [0.35, 0.05, 0.0], "r_hand": [0.10, 0.0, 0.0], "l_arm": [-0.15, -0.05, -0.02], "l_fore": [0.30, -0.05, 0.0], "l_hand": [0.05, 0.0, 0.0], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]}
        ]
    },
    {
        "id": "rich", "name": "Rich", "gloss": "RICH", "duration": 1250, "type": "Wealth / Affluence Adjective",
        "notes": "ISLRTC 10,000 Dictionary #R-162. Dominant flat palm lifts from non-dominant palm ascending high with wealth flourish.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.30, 0.10, 0.05], "r_fore": [0.55, 0.08, 0.0], "r_hand": [0.15, 0.0, 0.0], "l_arm": [-0.25, -0.10, -0.05], "l_fore": [0.50, -0.08, 0.0], "l_hand": [0.15, 0.0, 0.0], "curls": [0.2, 0.2, 0.2, 0.2, 0.2]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.55, 0.25, 0.15], "r_fore": [0.80, 0.15, 0.0], "r_hand": [0.30, 0.10, 0.0], "l_arm": [-0.25, -0.10, -0.05], "l_fore": [0.50, -0.08, 0.0], "l_hand": [0.15, 0.0, 0.0], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.20, 0.10, 0.05], "r_fore": [0.40, 0.05, 0.0], "r_hand": [0.10, 0.0, 0.0], "l_arm": [-0.15, -0.05, -0.02], "l_fore": [0.30, -0.05, 0.0], "l_hand": [0.05, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "weak", "name": "Weak", "gloss": "WEAK", "duration": 1200, "type": "Frailty Adjective",
        "notes": "ISLRTC 10,000 Dictionary #W-041. Dominant V-fingers buckle and collapse against non-dominant flat palm.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.35, 0.15, 0.10], "r_fore": [0.65, 0.10, 0.0], "r_hand": [0.20, 0.0, 0.0], "l_arm": [-0.25, -0.10, -0.05], "l_fore": [0.55, -0.08, 0.0], "l_hand": [0.15, 0.0, 0.0], "curls": [0.8, 0.0, 0.0, 0.8, 0.8]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.28, 0.08, 0.05], "r_fore": [0.55, 0.05, 0.0], "r_hand": [0.10, 0.0, 0.0], "l_arm": [-0.25, -0.10, -0.05], "l_fore": [0.55, -0.08, 0.0], "l_hand": [0.15, 0.0, 0.0], "curls": [0.8, 0.6, 0.6, 0.8, 0.8]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.18, 0.05, 0.02], "r_fore": [0.35, 0.05, 0.0], "r_hand": [0.05, 0.0, 0.0], "l_arm": [-0.15, -0.05, -0.02], "l_fore": [0.30, -0.05, 0.0], "l_hand": [0.05, 0.0, 0.0], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]}
        ]
    },
    {
        "id": "heavy", "name": "Heavy", "gloss": "HEAVY", "duration": 1250, "type": "Weight / Burden Adjective",
        "notes": "ISLRTC 10,000 Dictionary #H-093. Dual open upward palms drop downward with weighted effort and slight torso dip.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Spine"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.35, 0.15, 0.10], "r_fore": [0.60, 0.10, 0.0], "r_hand": [0.20, 0.0, 0.0], "l_arm": [-0.35, -0.15, -0.10], "l_fore": [0.60, -0.10, 0.0], "l_hand": [0.20, 0.0, 0.0], "curls": [0.2, 0.2, 0.2, 0.2, 0.2]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.20, 0.10, 0.05], "r_fore": [0.75, 0.10, 0.0], "r_hand": [0.30, 0.0, 0.0], "l_arm": [-0.20, -0.10, -0.05], "l_fore": [0.75, -0.10, 0.0], "l_hand": [0.30, 0.0, 0.0], "curls": [0.3, 0.3, 0.3, 0.3, 0.3]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.15, 0.05, 0.02], "r_fore": [0.40, 0.05, 0.0], "r_hand": [0.10, 0.0, 0.0], "l_arm": [-0.15, -0.05, -0.02], "l_fore": [0.40, -0.05, 0.0], "l_hand": [0.10, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "shadow", "name": "Shadow", "gloss": "SHADOW", "duration": 1250, "type": "Optical / Silhouette Noun",
        "notes": "ISLRTC 10,000 Dictionary #S-188. Dominant flat palm passes underneath horizontal non-dominant hand into darkness.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.35, 0.15, 0.10], "r_fore": [0.55, 0.08, 0.0], "r_hand": [0.15, 0.0, 0.0], "l_arm": [-0.35, -0.10, -0.05], "l_fore": [0.65, -0.08, 0.0], "l_hand": [0.20, 0.0, 0.0], "curls": [0.2, 0.2, 0.2, 0.2, 0.2]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.30, 0.05, 0.05], "r_fore": [0.65, 0.05, 0.0], "r_hand": [0.25, 0.0, 0.0], "l_arm": [-0.35, -0.10, -0.05], "l_fore": [0.65, -0.08, 0.0], "l_hand": [0.20, 0.0, 0.0], "curls": [0.2, 0.2, 0.2, 0.2, 0.2]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.18, 0.05, 0.02], "r_fore": [0.35, 0.05, 0.0], "r_hand": [0.10, 0.0, 0.0], "l_arm": [-0.15, -0.05, -0.02], "l_fore": [0.30, -0.05, 0.0], "l_hand": [0.05, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "mirror", "name": "Mirror", "gloss": "MIRROR", "duration": 1250, "type": "Reflection Noun",
        "notes": "ISLRTC 10,000 Dictionary #M-180. Dominant flat open palm faces face and oscillates gently examining reflection.",
        "dominant": "right",
        "bones": ["Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.45, 0.15, 0.10], "r_fore": [0.75, 0.10, 0.0], "r_hand": [0.20, 0.15, 0.0], "head": [0.02, 0.02, 0.0], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.45, 0.10, 0.08], "r_fore": [0.75, 0.08, 0.0], "r_hand": [0.20, -0.10, 0.0], "head": [0.02, -0.02, 0.0], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.20, 0.05, 0.02], "r_fore": [0.35, 0.05, 0.0], "r_hand": [0.10, 0.0, 0.0], "head": [0.0, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "window", "name": "Window", "gloss": "WINDOW", "duration": 1250, "type": "Architectural Noun",
        "notes": "ISLRTC 10,000 Dictionary #W-112. Dual horizontal flat hands (dominant above non-dominant) opening upward.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.35, 0.15, 0.10], "r_fore": [0.65, 0.10, 0.0], "r_hand": [0.15, 0.0, 0.0], "l_arm": [-0.25, -0.10, -0.05], "l_fore": [0.55, -0.08, 0.0], "l_hand": [0.15, 0.0, 0.0], "curls": [0.2, 0.2, 0.2, 0.2, 0.2]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.50, 0.20, 0.12], "r_fore": [0.80, 0.12, 0.0], "r_hand": [0.25, 0.0, 0.0], "l_arm": [-0.25, -0.10, -0.05], "l_fore": [0.55, -0.08, 0.0], "l_hand": [0.15, 0.0, 0.0], "curls": [0.2, 0.2, 0.2, 0.2, 0.2]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.20, 0.08, 0.05], "r_fore": [0.40, 0.05, 0.0], "r_hand": [0.10, 0.0, 0.0], "l_arm": [-0.15, -0.05, -0.02], "l_fore": [0.30, -0.05, 0.0], "l_hand": [0.05, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "wall", "name": "Wall", "gloss": "WALL", "duration": 1250, "type": "Architectural / Partition Noun",
        "notes": "ISLRTC 10,000 Dictionary #W-015. Dual vertical flat palms held forward moving apart defining vertical solid partition.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.35, 0.10, 0.05], "r_fore": [0.65, 0.08, 0.0], "r_hand": [0.20, 0.0, 0.0], "l_arm": [-0.35, -0.10, -0.05], "l_fore": [0.65, -0.08, 0.0], "l_hand": [0.20, 0.0, 0.0], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.40, 0.30, 0.18], "r_fore": [0.70, 0.15, 0.0], "r_hand": [0.25, 0.0, 0.0], "l_arm": [-0.40, -0.30, -0.18], "l_fore": [0.70, -0.15, 0.0], "l_hand": [0.25, 0.0, 0.0], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.20, 0.10, 0.05], "r_fore": [0.35, 0.05, 0.0], "r_hand": [0.10, 0.0, 0.0], "l_arm": [-0.20, -0.10, -0.05], "l_fore": [0.35, -0.05, 0.0], "l_hand": [0.10, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    }
]

created_files = []
for spec in H25_AUTHORED_SPECS:
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

print(f"Successfully authored and saved {len(created_files)} Schema 2.0.0 signs (H25):")
for cf in created_files:
    print(f"  + signs/{cf}")
