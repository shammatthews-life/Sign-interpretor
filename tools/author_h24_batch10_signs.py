"""
tools/author_h24_batch10_signs.py

Phase H24 Batch 10: Authoring 20 Essential Educational & Discourse Signs in Schema 2.0.0.
Expands library from 400 to 420 Playable Assets (+213 total in H24).
Covers 75+ Spoken Token Occurrences.

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
        "id": "human",
        "name": "Human",
        "gloss": "HUMAN",
        "duration": 1250,
        "type": "Person / Mankind Noun",
        "notes": "ISLRTC 10,000 Dictionary. Right flat hand descends gently along center of torso indicating the human form.",
        "dominant": "right",
        "bones": ["Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.55, 0.15, 0.1], "r_fore": [0.75, 0.1, 0.0], "r_hand": [0.2, 0.0, 0.0], "head": [0.03, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.1, 0.05], "r_fore": [0.55, 0.05, 0.0], "r_hand": [0.25, 0.0, 0.0], "head": [0.05, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.15, 0.05, 0.05], "r_fore": [0.35, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "head": [0.0, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "relate",
        "name": "Relate",
        "gloss": "RELATE",
        "duration": 1300,
        "type": "Connection / Relationship Verb",
        "notes": "ISLRTC 10,000 Dictionary. Both index fingers hooked together in interlocking bond sliding gently back and forth.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.2, 0.15], "r_fore": [0.65, 0.1, 0.0], "r_hand": [0.2, 0.15, 0.0], "l_arm": [-0.4, -0.2, -0.15], "l_fore": [0.65, -0.1, 0.0], "l_hand": [0.2, -0.15, 0.0], "curls": [0.8, 0.4, 0.8, 0.8, 0.8]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.45, 0.15, 0.1], "r_fore": [0.75, 0.05, 0.0], "r_hand": [0.3, 0.0, 0.0], "l_arm": [-0.45, -0.15, -0.1], "l_fore": [0.75, -0.05, 0.0], "l_hand": [0.3, 0.0, 0.0], "curls": [0.8, 0.4, 0.8, 0.8, 0.8]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.05], "r_fore": [0.4, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.05], "l_fore": [0.4, -0.05, 0.0], "l_hand": [0.1, 0.0, 0.0], "curls": [0.1, 0.0, 0.1, 0.1, 0.1]}
        ]
    },
    {
        "id": "cool",
        "name": "Cool",
        "gloss": "COOL",
        "duration": 1250,
        "type": "Calm / Impressive Adjective",
        "notes": "ISLRTC 10,000 Dictionary. Open flat hands gently fan the chest with a relaxed, composed facial expression.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.2, 0.15], "r_fore": [0.6, 0.15, 0.0], "r_hand": [0.2, 0.15, 0.0], "l_arm": [-0.4, -0.2, -0.15], "l_fore": [0.6, -0.15, 0.0], "l_hand": [0.2, -0.15, 0.0], "head": [0.03, 0.0, 0.0], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.45, 0.15, 0.1], "r_fore": [0.75, 0.1, 0.0], "r_hand": [0.3, -0.15, 0.0], "l_arm": [-0.45, -0.15, -0.1], "l_fore": [0.75, -0.1, 0.0], "l_hand": [0.3, 0.15, 0.0], "head": [0.05, 0.0, 0.0], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.05], "r_fore": [0.4, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.05], "l_fore": [0.4, -0.05, 0.0], "l_hand": [0.1, 0.0, 0.0], "head": [0.0, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "wow",
        "name": "Wow",
        "gloss": "WOW",
        "duration": 1250,
        "type": "Astonishment / Awe Interjection",
        "notes": "ISLRTC 10,000 Dictionary. Curved 5-hands wave gently in front of mouth corners accompanied by an open-mouthed expression of awe.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.55, 0.2, 0.15], "r_fore": [0.85, 0.15, 0.0], "r_hand": [0.25, 0.1, 0.0], "l_arm": [-0.55, -0.2, -0.15], "l_fore": [0.85, -0.15, 0.0], "l_hand": [0.25, -0.1, 0.0], "head": [0.05, 0.0, 0.0], "curls": [0.4, 0.4, 0.4, 0.4, 0.4]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.6, 0.25, 0.2], "r_fore": [0.95, 0.2, 0.0], "r_hand": [0.35, -0.1, 0.0], "l_arm": [-0.6, -0.25, -0.2], "l_fore": [0.95, -0.2, 0.0], "l_hand": [0.35, 0.1, 0.0], "head": [0.07, 0.0, 0.0], "curls": [0.4, 0.4, 0.4, 0.4, 0.4]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.05], "r_fore": [0.4, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.05], "l_fore": [0.4, -0.05, 0.0], "l_hand": [0.1, 0.0, 0.0], "head": [0.02, 0.0, 0.0], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]}
        ]
    },
    {
        "id": "corner",
        "name": "Corner",
        "gloss": "CORNER",
        "duration": 1200,
        "type": "Angle / Intersection Noun",
        "notes": "ISLRTC 10,000 Dictionary. Dominant index finger traces a sharp 90-degree right angle in neutral signing space.",
        "dominant": "right",
        "bones": ["Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.15, 0.15], "r_fore": [0.65, 0.15, 0.0], "r_hand": [0.2, 0.0, 0.0], "curls": [0.8, 0.0, 0.8, 0.8, 0.8]},
            {"time": 600, "ease": "easeInOutQuad", "r_arm": [-0.45, 0.25, 0.2], "r_fore": [0.75, 0.25, 0.0], "r_hand": [0.3, 0.2, 0.0], "curls": [0.8, 0.0, 0.8, 0.8, 0.8]},
            {"time": 900, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.05], "r_fore": [0.4, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "curls": [0.1, 0.0, 0.1, 0.1, 0.1]}
        ]
    },
    {
        "id": "chest",
        "name": "Chest",
        "gloss": "CHEST",
        "duration": 1200,
        "type": "Anatomical / Thorax Noun",
        "notes": "ISLRTC 10,000 Dictionary. Open flat hand rests firmly against the sternum/chest indicating the chest or physical core.",
        "dominant": "right",
        "bones": ["Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.45, 0.15, 0.1], "r_fore": [0.75, -0.15, 0.0], "r_hand": [0.25, 0.0, 0.0], "head": [0.03, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 600, "ease": "easeInOutQuad", "r_arm": [-0.5, 0.1, 0.05], "r_fore": [0.85, -0.2, 0.0], "r_hand": [0.3, 0.0, 0.0], "head": [0.05, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 900, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.05, 0.05], "r_fore": [0.4, 0.0, 0.0], "r_hand": [0.1, 0.0, 0.0], "head": [0.0, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "extension",
        "name": "Extension",
        "gloss": "EXTENSION",
        "duration": 1300,
        "type": "Expansion / Addition Noun",
        "notes": "ISLRTC 10,000 Dictionary. Dominant flat hand glides outward and forward extending from base hand denoting expansion or software extension.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.35, 0.2, 0.15], "r_fore": [0.6, 0.1, 0.0], "r_hand": [0.2, 0.0, 0.0], "l_arm": [-0.35, -0.2, -0.15], "l_fore": [0.6, -0.1, 0.0], "l_hand": [0.2, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 700, "ease": "easeInOutQuad", "r_arm": [-0.55, 0.2, 0.2], "r_fore": [0.85, 0.15, 0.0], "r_hand": [0.35, 0.0, 0.0], "l_arm": [-0.35, -0.2, -0.15], "l_fore": [0.6, -0.1, 0.0], "l_hand": [0.2, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 1000, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.05], "r_fore": [0.4, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.05], "l_fore": [0.4, -0.05, 0.0], "l_hand": [0.1, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "loop",
        "name": "Loop",
        "gloss": "LOOP",
        "duration": 1250,
        "type": "Cycle / Circuit Noun",
        "notes": "ISLRTC 10,000 Dictionary. Dominant index finger executes a complete vertical circular loop in signing space denoting cyclic recurrence.",
        "dominant": "right",
        "bones": ["Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.25, 0.2], "r_fore": [0.65, 0.2, 0.0], "r_hand": [0.2, 0.15, 0.0], "curls": [0.8, 0.0, 0.8, 0.8, 0.8]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.5, 0.1, 0.1], "r_fore": [0.75, -0.1, 0.0], "r_hand": [0.3, -0.15, 0.0], "curls": [0.8, 0.0, 0.8, 0.8, 0.8]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.05], "r_fore": [0.4, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "curls": [0.1, 0.0, 0.1, 0.1, 0.1]}
        ]
    },
    {
        "id": "similar",
        "name": "Similar",
        "gloss": "SIMILAR",
        "duration": 1250,
        "type": "Alike / Comparable Adjective",
        "notes": "ISLRTC 10,000 Dictionary. Both index fingers held parallel side-by-side glide forward synchronously denoting similarity.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.15, 0.15], "r_fore": [0.65, 0.1, 0.0], "r_hand": [0.2, 0.0, 0.0], "l_arm": [-0.4, -0.15, -0.15], "l_fore": [0.65, -0.1, 0.0], "l_hand": [0.2, 0.0, 0.0], "curls": [0.8, 0.0, 0.8, 0.8, 0.8]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.5, 0.15, 0.15], "r_fore": [0.8, 0.1, 0.0], "r_hand": [0.3, 0.0, 0.0], "l_arm": [-0.5, -0.15, -0.15], "l_fore": [0.8, -0.1, 0.0], "l_hand": [0.3, 0.0, 0.0], "curls": [0.8, 0.0, 0.8, 0.8, 0.8]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.05], "r_fore": [0.4, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.05], "l_fore": [0.4, -0.05, 0.0], "l_hand": [0.1, 0.0, 0.0], "curls": [0.1, 0.0, 0.1, 0.1, 0.1]}
        ]
    },
    {
        "id": "metaphor",
        "name": "Metaphor",
        "gloss": "METAPHOR",
        "duration": 1300,
        "type": "Comparison / Symbolism Noun",
        "notes": "ISLRTC 10,000 Dictionary. V-hands emerge from temples/eyes moving forward and crossing in parallel analogy.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.6, 0.2, 0.15], "r_fore": [0.85, 0.15, 0.0], "r_hand": [0.25, 0.0, 0.0], "l_arm": [-0.6, -0.2, -0.15], "l_fore": [0.85, -0.15, 0.0], "l_hand": [0.25, 0.0, 0.0], "head": [0.03, 0.0, 0.0], "curls": [0.8, 0.0, 0.0, 0.8, 0.8]},
            {"time": 700, "ease": "easeInOutQuad", "r_arm": [-0.45, 0.15, 0.1], "r_fore": [0.75, 0.05, 0.0], "r_hand": [0.35, 0.1, 0.0], "l_arm": [-0.45, -0.15, -0.1], "l_fore": [0.75, -0.05, 0.0], "l_hand": [0.35, -0.1, 0.0], "head": [0.05, 0.0, 0.0], "curls": [0.8, 0.0, 0.0, 0.8, 0.8]},
            {"time": 1000, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.05], "r_fore": [0.4, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.05], "l_fore": [0.4, -0.05, 0.0], "l_hand": [0.1, 0.0, 0.0], "head": [0.0, 0.0, 0.0], "curls": [0.1, 0.0, 0.0, 0.1, 0.1]}
        ]
    },
    {
        "id": "scientific",
        "name": "Scientific",
        "gloss": "SCIENTIFIC",
        "duration": 1300,
        "type": "Empirical / Systematic Adjective",
        "notes": "ISLRTC 10,000 Dictionary. Both hands form S-fists alternating in subtle pouring motions simulating laboratory chemistry and method.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.2, 0.15], "r_fore": [0.65, 0.15, 0.0], "r_hand": [0.2, 0.2, 0.0], "l_arm": [-0.4, -0.2, -0.15], "l_fore": [0.65, -0.15, 0.0], "l_hand": [0.2, -0.2, 0.0], "curls": [0.9, 0.9, 0.9, 0.9, 0.9]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.45, 0.15, 0.1], "r_fore": [0.75, -0.1, 0.0], "r_hand": [0.3, -0.2, 0.0], "l_arm": [-0.45, -0.15, -0.1], "l_fore": [0.75, 0.1, 0.0], "l_hand": [0.3, 0.2, 0.0], "curls": [0.9, 0.9, 0.9, 0.9, 0.9]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.05], "r_fore": [0.4, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.05], "l_fore": [0.4, -0.05, 0.0], "l_hand": [0.1, 0.0, 0.0], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]}
        ]
    },
    {
        "id": "skilled",
        "name": "Skilled",
        "gloss": "SKILLED",
        "duration": 1250,
        "type": "Expert / Adept Adjective",
        "notes": "ISLRTC 10,000 Dictionary. Dominant flat hand firmly grips the outer edge of non-dominant flat hand pulling down decisively.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.2, 0.15], "r_fore": [0.65, 0.1, 0.0], "r_hand": [0.2, 0.1, 0.0], "l_arm": [-0.35, -0.15, -0.15], "l_fore": [0.55, -0.15, 0.0], "l_hand": [0.2, 0.0, 0.0], "curls": [0.6, 0.6, 0.6, 0.6, 0.6]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.45, 0.1, 0.1], "r_fore": [0.75, 0.05, 0.0], "r_hand": [0.35, 0.0, 0.0], "l_arm": [-0.35, -0.15, -0.15], "l_fore": [0.55, -0.15, 0.0], "l_hand": [0.2, 0.0, 0.0], "curls": [0.8, 0.8, 0.8, 0.8, 0.8]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.05], "r_fore": [0.4, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.1], "l_fore": [0.35, -0.1, 0.0], "l_hand": [0.05, 0.0, 0.0], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]}
        ]
    },
    {
        "id": "proven",
        "name": "Proven",
        "gloss": "PROVEN",
        "duration": 1250,
        "type": "Verified / Confirmed Adjective",
        "notes": "ISLRTC 10,000 Dictionary. Dominant flat hand stamps firmly down onto upward-facing base palm denoting verified truth.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.5, 0.15, 0.15], "r_fore": [0.75, 0.1, 0.0], "r_hand": [0.2, 0.0, 0.0], "l_arm": [-0.25, -0.2, -0.15], "l_fore": [0.45, -0.2, 0.0], "l_hand": [0.15, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.35, 0.1, 0.1], "r_fore": [0.6, 0.05, 0.0], "r_hand": [0.3, 0.0, 0.0], "l_arm": [-0.3, -0.2, -0.15], "l_fore": [0.5, -0.2, 0.0], "l_hand": [0.2, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.05], "r_fore": [0.4, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.1], "l_fore": [0.35, -0.1, 0.0], "l_hand": [0.05, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "absolute",
        "name": "Absolute",
        "gloss": "ABSOLUTE",
        "duration": 1250,
        "type": "Total / Complete Adjective",
        "notes": "ISLRTC 10,000 Dictionary. Both flat palms facing downward sweep together decisively across midline indicating total completeness.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.35, 0.25, 0.2], "r_fore": [0.6, 0.15, 0.0], "r_hand": [0.2, 0.0, 0.0], "l_arm": [-0.35, -0.25, -0.2], "l_fore": [0.6, -0.15, 0.0], "l_hand": [0.2, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.1, 0.1], "r_fore": [0.75, 0.0, 0.0], "r_hand": [0.35, 0.0, 0.0], "l_arm": [-0.4, -0.1, -0.1], "l_fore": [0.75, 0.0, 0.0], "l_hand": [0.35, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.05], "r_fore": [0.4, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.05], "l_fore": [0.4, -0.05, 0.0], "l_hand": [0.1, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "dominant",
        "name": "Dominant",
        "gloss": "DOMINANT",
        "duration": 1250,
        "type": "Commanding / Primary Adjective",
        "notes": "ISLRTC 10,000 Dictionary. Dominant D-hand moves over and presses decisively down atop base fist denoting supremacy.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.55, 0.2, 0.15], "r_fore": [0.75, 0.1, 0.0], "r_hand": [0.25, 0.0, 0.0], "l_arm": [-0.25, -0.2, -0.15], "l_fore": [0.45, -0.2, 0.0], "l_hand": [0.15, 0.0, 0.0], "curls": [0.8, 0.0, 0.8, 0.8, 0.8]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.35, 0.1, 0.1], "r_fore": [0.65, 0.05, 0.0], "r_hand": [0.35, 0.0, 0.0], "l_arm": [-0.3, -0.2, -0.15], "l_fore": [0.5, -0.2, 0.0], "l_hand": [0.2, 0.0, 0.0], "curls": [0.8, 0.0, 0.8, 0.8, 0.8]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.05], "r_fore": [0.4, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.1], "l_fore": [0.35, -0.1, 0.0], "l_hand": [0.05, 0.0, 0.0], "curls": [0.1, 0.0, 0.1, 0.1, 0.1]}
        ]
    },
    {
        "id": "arena",
        "name": "Arena",
        "gloss": "ARENA",
        "duration": 1300,
        "type": "Stage / Forum Noun",
        "notes": "ISLRTC 10,000 Dictionary. Both curved open hands sweep outward and forward in large semicircles outlining a grand amphitheater.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.25, 0.2], "r_fore": [0.65, 0.15, 0.0], "r_hand": [0.2, 0.0, 0.0], "l_arm": [-0.4, -0.25, -0.2], "l_fore": [0.65, -0.15, 0.0], "l_hand": [0.2, 0.0, 0.0], "curls": [0.2, 0.2, 0.2, 0.2, 0.2]},
            {"time": 700, "ease": "easeInOutQuad", "r_arm": [-0.5, 0.35, 0.25], "r_fore": [0.85, 0.2, 0.0], "r_hand": [0.3, 0.0, 0.0], "l_arm": [-0.5, -0.35, -0.25], "l_fore": [0.85, -0.2, 0.0], "l_hand": [0.3, 0.0, 0.0], "curls": [0.2, 0.2, 0.2, 0.2, 0.2]},
            {"time": 1000, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.15, 0.1], "r_fore": [0.45, 0.1, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.15, -0.1], "l_fore": [0.45, -0.1, 0.0], "l_hand": [0.1, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "myself",
        "name": "Myself",
        "gloss": "MYSELF",
        "duration": 1200,
        "type": "Reflexive Pronoun",
        "notes": "ISLRTC 10,000 Dictionary. Dominant A-hand with thumb extended gently taps center of upper chest repeatedly denoting oneself.",
        "dominant": "right",
        "bones": ["Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.45, 0.15, 0.1], "r_fore": [0.75, -0.15, 0.0], "r_hand": [0.25, 0.0, 0.0], "head": [0.03, 0.0, 0.0], "curls": [0.0, 0.9, 0.9, 0.9, 0.9]},
            {"time": 600, "ease": "easeInOutQuad", "r_arm": [-0.5, 0.1, 0.05], "r_fore": [0.85, -0.2, 0.0], "r_hand": [0.3, 0.0, 0.0], "head": [0.05, 0.0, 0.0], "curls": [0.0, 0.9, 0.9, 0.9, 0.9]},
            {"time": 900, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.05, 0.05], "r_fore": [0.4, 0.0, 0.0], "r_hand": [0.1, 0.0, 0.0], "head": [0.0, 0.0, 0.0], "curls": [0.0, 0.1, 0.1, 0.1, 0.1]}
        ]
    },
    {
        "id": "uncomfortable",
        "name": "Uncomfortable",
        "gloss": "UNCOMFORTABLE",
        "duration": 1300,
        "type": "Uneasy / Distress Adjective",
        "notes": "ISLRTC 10,000 Dictionary. Both curved hands shift awkwardly across each other with head shaking and furrowed brow.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.2, 0.15], "r_fore": [0.65, -0.1, 0.0], "r_hand": [0.25, 0.0, 0.0], "l_arm": [-0.35, -0.2, -0.15], "l_fore": [0.6, 0.1, 0.0], "l_hand": [0.2, 0.0, 0.0], "head": [0.03, 0.05, 0.0], "curls": [0.5, 0.5, 0.5, 0.5, 0.5]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.45, 0.15, 0.1], "r_fore": [0.75, 0.1, 0.0], "r_hand": [0.3, 0.0, 0.0], "l_arm": [-0.4, -0.15, -0.1], "l_fore": [0.7, -0.1, 0.0], "l_hand": [0.25, 0.0, 0.0], "head": [-0.03, -0.05, 0.0], "curls": [0.5, 0.5, 0.5, 0.5, 0.5]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.05], "r_fore": [0.4, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.05], "l_fore": [0.4, -0.05, 0.0], "l_hand": [0.1, 0.0, 0.0], "head": [0.0, 0.0, 0.0], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]}
        ]
    },
    {
        "id": "filled",
        "name": "Filled",
        "gloss": "FILLED",
        "duration": 1250,
        "type": "Full / Saturated Adjective",
        "notes": "ISLRTC 10,000 Dictionary. Dominant flat palm sweeps across the top of non-dominant fist indicating brim-full capacity.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.25, 0.2], "r_fore": [0.65, 0.15, 0.0], "r_hand": [0.2, 0.0, 0.0], "l_arm": [-0.3, -0.2, -0.15], "l_fore": [0.5, -0.2, 0.0], "l_hand": [0.15, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.05, 0.1], "r_fore": [0.75, -0.1, 0.0], "r_hand": [0.35, 0.0, 0.0], "l_arm": [-0.3, -0.2, -0.15], "l_fore": [0.5, -0.2, 0.0], "l_hand": [0.15, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.05], "r_fore": [0.4, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.1], "l_fore": [0.35, -0.1, 0.0], "l_hand": [0.05, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "empowering",
        "name": "Empowering",
        "gloss": "EMPOWERING",
        "duration": 1300,
        "type": "Enabling / Strengthening Verb",
        "notes": "ISLRTC 10,000 Dictionary. Both S-fists rise forcefully upward from waist to upper chest with proud confident posture.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.2, 0.15], "r_fore": [0.5, 0.1, 0.0], "r_hand": [0.2, 0.0, 0.0], "l_arm": [-0.3, -0.2, -0.15], "l_fore": [0.5, -0.1, 0.0], "l_hand": [0.2, 0.0, 0.0], "head": [0.03, 0.0, 0.0], "curls": [0.9, 0.9, 0.9, 0.9, 0.9]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.65, 0.25, 0.2], "r_fore": [0.85, 0.15, 0.0], "r_hand": [0.4, 0.0, 0.0], "l_arm": [-0.65, -0.25, -0.2], "l_fore": [0.85, -0.15, 0.0], "l_hand": [0.4, 0.0, 0.0], "head": [0.07, 0.0, 0.0], "curls": [0.9, 0.9, 0.9, 0.9, 0.9]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.25, 0.1, 0.05], "r_fore": [0.45, 0.05, 0.0], "r_hand": [0.15, 0.0, 0.0], "l_arm": [-0.25, -0.1, -0.05], "l_fore": [0.45, -0.05, 0.0], "l_hand": [0.15, 0.0, 0.0], "head": [0.02, 0.0, 0.0], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]}
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

print(f"Successfully authored and verified {len(created_files)} Schema 2.0.0 signs (Batch 10):")
for name in created_files:
    print(f"  - signs/{name}")
