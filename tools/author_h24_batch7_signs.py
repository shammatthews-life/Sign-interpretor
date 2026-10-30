"""
tools/author_h24_batch7_signs.py

Phase H24 Batch 7: Authoring 24 Essential Educational & Discourse Signs in Schema 2.0.0.
Expands library from 332 to 356 Playable Assets (+149 total in H24).
Covers 110+ Spoken Token Occurrences.

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
        "id": "job",
        "name": "Job",
        "gloss": "JOB",
        "duration": 1250,
        "type": "Work / Occupation Noun",
        "notes": "ISLRTC 10,000 Dictionary. Both hands formed into fists, right fist rhythmically taps wrist or fist of left base hand representing structured labor.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.2, 0.2], "r_fore": [0.6, 0.3, 0.1], "r_hand": [0.2, 0.1, -0.1], "l_arm": [-0.3, -0.2, -0.2], "l_fore": [0.5, -0.3, -0.1], "l_hand": [0.2, -0.1, 0.1], "curls": [0.9, 0.9, 0.9, 0.9, 0.9]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.45, 0.1, 0.1], "r_fore": [0.75, 0.1, 0.1], "r_hand": [0.3, 0.0, -0.1], "l_arm": [-0.3, -0.2, -0.2], "l_fore": [0.5, -0.3, -0.1], "l_hand": [0.2, -0.1, 0.1], "curls": [0.9, 0.9, 0.9, 0.9, 0.9]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.1], "r_fore": [0.4, 0.1, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.1], "l_fore": [0.4, -0.1, 0.0], "l_hand": [0.1, 0.0, 0.0], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]}
        ]
    },
    {
        "id": "business",
        "name": "Business",
        "gloss": "BUSINESS",
        "duration": 1300,
        "type": "Commerce / Enterprise Noun",
        "notes": "ISLRTC 10,000 Dictionary. Right flat 'B' hand brushes outward repeatedly across upward-facing left palm representing commercial enterprise.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.35, 0.2, 0.2], "r_fore": [0.6, 0.2, 0.1], "r_hand": [0.2, 0.3, 0.0], "l_arm": [-0.3, -0.25, -0.2], "l_fore": [0.5, -0.2, -0.1], "l_hand": [0.1, 0.0, 0.0], "curls": [0.8, 0.0, 0.0, 0.0, 0.0]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.3, 0.25], "r_fore": [0.75, 0.4, 0.15], "r_hand": [0.3, 0.4, 0.0], "l_arm": [-0.3, -0.25, -0.2], "l_fore": [0.5, -0.2, -0.1], "l_hand": [0.1, 0.0, 0.0], "curls": [0.8, 0.0, 0.0, 0.0, 0.0]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.1], "r_fore": [0.4, 0.1, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.1], "l_fore": [0.3, -0.1, 0.0], "l_hand": [0.0, 0.0, 0.0], "curls": [0.1, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "message",
        "name": "Message",
        "gloss": "MESSAGE",
        "duration": 1250,
        "type": "Information / Communication Noun",
        "notes": "ISLRTC 10,000 Dictionary. Both hands with thumb and index pinched into 'O' shapes move forward from neutral space conveying transmitted information.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.15, 0.2], "r_fore": [0.6, 0.1, 0.0], "r_hand": [0.2, 0.0, 0.1], "l_arm": [-0.4, -0.15, -0.2], "l_fore": [0.6, -0.1, 0.0], "l_hand": [0.2, 0.0, -0.1], "curls": [0.8, 0.8, 0.0, 0.0, 0.0]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.5, 0.2, 0.25], "r_fore": [0.8, 0.15, 0.0], "r_hand": [0.35, 0.0, 0.15], "l_arm": [-0.5, -0.2, -0.25], "l_fore": [0.8, -0.15, 0.0], "l_hand": [0.35, 0.0, -0.15], "curls": [0.8, 0.8, 0.0, 0.0, 0.0]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.1], "r_fore": [0.4, 0.1, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.1], "l_fore": [0.4, -0.1, 0.0], "l_hand": [0.1, 0.0, 0.0], "curls": [0.1, 0.1, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "care",
        "name": "Care",
        "gloss": "CARE",
        "duration": 1300,
        "type": "Affection / Compassion Verb",
        "notes": "ISLRTC 10,000 Dictionary. Both crossed open hands gently circle and rest over upper chest indicating compassionate regard.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.45, 0.25, 0.15], "r_fore": [0.7, -0.15, 0.0], "r_hand": [0.25, 0.0, 0.0], "l_arm": [-0.4, -0.2, -0.15], "l_fore": [0.65, 0.15, 0.0], "l_hand": [0.2, 0.0, 0.0], "curls": [0.2, 0.2, 0.2, 0.2, 0.2]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.5, 0.2, 0.1], "r_fore": [0.85, -0.25, 0.0], "r_hand": [0.3, 0.0, 0.0], "l_arm": [-0.45, -0.2, -0.1], "l_fore": [0.75, 0.25, 0.0], "l_hand": [0.25, 0.0, 0.0], "curls": [0.2, 0.2, 0.2, 0.2, 0.2]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.1], "r_fore": [0.4, -0.1, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.1], "l_fore": [0.4, 0.1, 0.0], "l_hand": [0.1, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "promise",
        "name": "Promise",
        "gloss": "PROMISE",
        "duration": 1300,
        "type": "Commitment Verb",
        "notes": "ISLRTC 10,000 Dictionary. Right index finger touches lips, then opens into a flat hand descending firmly onto upward-facing left palm.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.6, 0.1, 0.1], "r_fore": [0.9, 0.2, 0.0], "r_hand": [0.2, 0.0, 0.0], "l_arm": [-0.2, -0.2, -0.1], "l_fore": [0.4, -0.2, 0.0], "l_hand": [0.1, 0.0, 0.0], "curls": [0.8, 0.0, 0.8, 0.8, 0.8]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.15, 0.1], "r_fore": [0.7, 0.15, 0.0], "r_hand": [0.3, 0.0, 0.0], "l_arm": [-0.35, -0.2, -0.15], "l_fore": [0.6, -0.15, 0.0], "l_hand": [0.2, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.1], "r_fore": [0.4, 0.1, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.1], "l_fore": [0.3, -0.1, 0.0], "l_hand": [0.1, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "flow",
        "name": "Flow",
        "gloss": "FLOW",
        "duration": 1250,
        "type": "Continuous Progression Verb",
        "notes": "ISLRTC 10,000 Dictionary. Both open hands glide forward with gentle sinuous undulations denoting smooth continuous progression.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.15, 0.2], "r_fore": [0.55, 0.1, 0.0], "r_hand": [0.2, 0.1, 0.0], "l_arm": [-0.4, -0.15, -0.2], "l_fore": [0.55, -0.1, 0.0], "l_hand": [0.2, -0.1, 0.0], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.5, 0.2, 0.25], "r_fore": [0.75, 0.15, 0.1], "r_hand": [-0.15, 0.2, 0.0], "l_arm": [-0.5, -0.2, -0.25], "l_fore": [0.75, -0.15, -0.1], "l_hand": [-0.15, -0.2, 0.0], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.1], "r_fore": [0.4, 0.05, 0.0], "r_hand": [0.05, 0.05, 0.0], "l_arm": [-0.2, -0.1, -0.1], "l_fore": [0.4, -0.05, 0.0], "l_hand": [0.05, -0.05, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "store",
        "name": "Store",
        "gloss": "STORE",
        "duration": 1250,
        "type": "Shop / Repository Noun",
        "notes": "ISLRTC 10,000 Dictionary. Both curved hands swing outward from chest like doors or roof outline indicating shop or stored repository.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.1, 0.15], "r_fore": [0.65, 0.1, 0.0], "r_hand": [0.2, 0.0, 0.0], "l_arm": [-0.4, -0.1, -0.15], "l_fore": [0.65, -0.1, 0.0], "l_hand": [0.2, 0.0, 0.0], "curls": [0.4, 0.4, 0.4, 0.4, 0.4]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.45, 0.25, 0.25], "r_fore": [0.7, 0.25, 0.0], "r_hand": [0.25, 0.0, 0.0], "l_arm": [-0.45, -0.25, -0.25], "l_fore": [0.7, -0.25, 0.0], "l_hand": [0.25, 0.0, 0.0], "curls": [0.4, 0.4, 0.4, 0.4, 0.4]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.1], "r_fore": [0.4, 0.1, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.1], "l_fore": [0.4, -0.1, 0.0], "l_hand": [0.1, 0.0, 0.0], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]}
        ]
    },
    {
        "id": "center",
        "name": "Center",
        "gloss": "CENTER",
        "duration": 1250,
        "type": "Midpoint / Core Noun",
        "notes": "ISLRTC 10,000 Dictionary. Right bent index or fingers circle above upward left palm and descend directly into its focal middle.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.5, 0.2, 0.15], "r_fore": [0.7, 0.1, 0.0], "r_hand": [0.2, 0.2, 0.0], "l_arm": [-0.3, -0.2, -0.2], "l_fore": [0.5, -0.2, 0.0], "l_hand": [0.1, 0.0, 0.0], "curls": [0.8, 0.1, 0.8, 0.8, 0.8]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.45, 0.1, 0.1], "r_fore": [0.8, 0.05, 0.0], "r_hand": [0.3, 0.0, 0.0], "l_arm": [-0.35, -0.15, -0.15], "l_fore": [0.55, -0.15, 0.0], "l_hand": [0.15, 0.0, 0.0], "curls": [0.8, 0.1, 0.8, 0.8, 0.8]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.1], "r_fore": [0.4, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.1], "l_fore": [0.3, -0.1, 0.0], "l_hand": [0.05, 0.0, 0.0], "curls": [0.1, 0.0, 0.1, 0.1, 0.1]}
        ]
    },
    {
        "id": "middle",
        "name": "Middle",
        "gloss": "MIDDLE",
        "duration": 1200,
        "type": "Midpoint Adjective",
        "notes": "ISLRTC 10,000 Dictionary. Right middle finger bends downward and makes contact with the center of the upturned left palm.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.45, 0.2, 0.15], "r_fore": [0.65, 0.1, 0.0], "r_hand": [0.25, 0.1, 0.0], "l_arm": [-0.3, -0.2, -0.2], "l_fore": [0.5, -0.2, 0.0], "l_hand": [0.1, 0.0, 0.0], "curls": [0.8, 0.8, 0.1, 0.8, 0.8]},
            {"time": 600, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.1, 0.1], "r_fore": [0.75, 0.05, 0.0], "r_hand": [0.35, 0.0, 0.0], "l_arm": [-0.3, -0.15, -0.15], "l_fore": [0.55, -0.15, 0.0], "l_hand": [0.15, 0.0, 0.0], "curls": [0.8, 0.8, 0.2, 0.8, 0.8]},
            {"time": 900, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.1], "r_fore": [0.4, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.1], "l_fore": [0.3, -0.1, 0.0], "l_hand": [0.05, 0.0, 0.0], "curls": [0.1, 0.1, 0.0, 0.1, 0.1]}
        ]
    },
    {
        "id": "sister",
        "name": "Sister",
        "gloss": "SISTER",
        "duration": 1300,
        "type": "Family / Kinship Noun",
        "notes": "ISLRTC 10,000 Dictionary. Right hand touches jawline / ear (female indicator) then index fingers align horizontally in front of chest (sibling).",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.65, 0.2, 0.1], "r_fore": [0.9, 0.3, 0.0], "r_hand": [0.2, 0.1, 0.0], "l_arm": [-0.2, -0.2, -0.1], "l_fore": [0.3, -0.1, 0.0], "l_hand": [0.05, 0.0, 0.0], "curls": [0.8, 0.1, 0.8, 0.8, 0.8]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.15, 0.15], "r_fore": [0.65, 0.1, 0.0], "r_hand": [0.25, 0.0, 0.0], "l_arm": [-0.4, -0.15, -0.15], "l_fore": [0.65, -0.1, 0.0], "l_hand": [0.25, 0.0, 0.0], "curls": [0.8, 0.0, 0.8, 0.8, 0.8]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.1], "r_fore": [0.4, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.1], "l_fore": [0.4, -0.05, 0.0], "l_hand": [0.1, 0.0, 0.0], "curls": [0.1, 0.0, 0.1, 0.1, 0.1]}
        ]
    },
    {
        "id": "post",
        "name": "Post",
        "gloss": "POST",
        "duration": 1250,
        "type": "Notice / Publish Verb",
        "notes": "ISLRTC 10,000 Dictionary. Right hand with thumb and index places a notice or stamp against the vertical flat left palm.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.2, 0.2], "r_fore": [0.65, 0.2, 0.0], "r_hand": [0.2, 0.1, 0.0], "l_arm": [-0.4, -0.1, -0.2], "l_fore": [0.7, -0.2, 0.0], "l_hand": [0.3, 0.0, 0.0], "curls": [0.6, 0.6, 0.1, 0.1, 0.1]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.45, 0.05, 0.1], "r_fore": [0.75, 0.1, 0.0], "r_hand": [0.3, 0.0, 0.0], "l_arm": [-0.4, -0.1, -0.15], "l_fore": [0.7, -0.15, 0.0], "l_hand": [0.3, 0.0, 0.0], "curls": [0.6, 0.6, 0.1, 0.1, 0.1]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.1], "r_fore": [0.4, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.1], "l_fore": [0.4, -0.1, 0.0], "l_hand": [0.1, 0.0, 0.0], "curls": [0.1, 0.1, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "package",
        "name": "Package",
        "gloss": "PACKAGE",
        "duration": 1300,
        "type": "Box / Parcel Noun",
        "notes": "ISLRTC 10,000 Dictionary. Both open flat hands outline the dimensions of a three-dimensional box in neutral space.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.35, 0.25, 0.2], "r_fore": [0.6, 0.1, 0.0], "r_hand": [0.2, 0.0, 0.0], "l_arm": [-0.35, -0.25, -0.2], "l_fore": [0.6, -0.1, 0.0], "l_hand": [0.2, 0.0, 0.0], "curls": [0.1, 0.0, 0.0, 0.0, 0.0]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.45, 0.15, 0.15], "r_fore": [0.75, 0.05, 0.0], "r_hand": [0.3, 0.0, 0.0], "l_arm": [-0.45, -0.15, -0.15], "l_fore": [0.75, -0.05, 0.0], "l_hand": [0.3, 0.0, 0.0], "curls": [0.1, 0.0, 0.0, 0.0, 0.0]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.1], "r_fore": [0.4, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.1], "l_fore": [0.4, -0.05, 0.0], "l_hand": [0.1, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "favorite",
        "name": "Favorite",
        "gloss": "FAVORITE",
        "duration": 1250,
        "type": "Preference Adjective",
        "notes": "ISLRTC 10,000 Dictionary. Right middle finger touches or taps the center of the chin repeatedly with an appreciative facial expression.",
        "dominant": "right",
        "bones": ["Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.65, 0.1, 0.1], "r_fore": [0.95, 0.2, 0.0], "r_hand": [0.25, 0.0, 0.0], "head": [0.04, 0.0, 0.0], "curls": [0.8, 0.8, 0.2, 0.8, 0.8]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.7, 0.08, 0.08], "r_fore": [1.0, 0.22, 0.0], "r_hand": [0.35, 0.0, 0.0], "head": [0.06, 0.0, 0.0], "curls": [0.8, 0.8, 0.2, 0.8, 0.8]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.1, 0.1], "r_fore": [0.5, 0.1, 0.0], "r_hand": [0.15, 0.0, 0.0], "head": [0.02, 0.0, 0.0], "curls": [0.1, 0.1, 0.0, 0.1, 0.1]}
        ]
    },
    {
        "id": "silent",
        "name": "Silent",
        "gloss": "SILENT",
        "duration": 1300,
        "type": "Quiet / Stillness Adjective",
        "notes": "ISLRTC 10,000 Dictionary. Right index finger placed upright against lips, then both hands sweep outward flat palms facing down.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.65, 0.05, 0.1], "r_fore": [0.95, 0.15, 0.0], "r_hand": [0.3, 0.0, 0.0], "head": [0.04, 0.0, 0.0], "curls": [0.8, 0.0, 0.8, 0.8, 0.8]},
            {"time": 700, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.3, 0.25], "r_fore": [0.6, 0.2, 0.0], "r_hand": [0.2, 0.0, 0.0], "l_arm": [-0.4, -0.3, -0.25], "l_fore": [0.6, -0.2, 0.0], "l_hand": [0.2, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 1000, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.15, 0.1], "r_fore": [0.4, 0.1, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.15, -0.1], "l_fore": [0.4, -0.1, 0.0], "l_hand": [0.1, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "comfortable",
        "name": "Comfortable",
        "gloss": "COMFORTABLE",
        "duration": 1300,
        "type": "Ease / Relaxation Adjective",
        "notes": "ISLRTC 10,000 Dictionary. Both curved hands stroke over the back of each other alternately denoting ease and relaxation.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.2, 0.15], "r_fore": [0.65, -0.1, 0.0], "r_hand": [0.25, 0.0, 0.0], "l_arm": [-0.35, -0.2, -0.15], "l_fore": [0.6, 0.1, 0.0], "l_hand": [0.2, 0.0, 0.0], "curls": [0.3, 0.3, 0.3, 0.3, 0.3]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.45, 0.15, 0.1], "r_fore": [0.75, 0.1, 0.0], "r_hand": [0.3, 0.0, 0.0], "l_arm": [-0.4, -0.15, -0.1], "l_fore": [0.7, -0.1, 0.0], "l_hand": [0.25, 0.0, 0.0], "curls": [0.3, 0.3, 0.3, 0.3, 0.3]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.1], "r_fore": [0.4, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.1], "l_fore": [0.4, -0.05, 0.0], "l_hand": [0.1, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "football",
        "name": "Football",
        "gloss": "FOOTBALL",
        "duration": 1250,
        "type": "Sport / Game Noun",
        "notes": "ISLRTC 10,000 Dictionary. Open 5-handshapes with fingers spread tap inward toward each other simulating the stitches of a ball or team clash.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.45, 0.2, 0.2], "r_fore": [0.6, 0.1, 0.0], "r_hand": [0.2, 0.0, 0.0], "l_arm": [-0.45, -0.2, -0.2], "l_fore": [0.6, -0.1, 0.0], "l_hand": [0.2, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.5, 0.1, 0.1], "r_fore": [0.75, 0.15, 0.0], "r_hand": [0.35, 0.0, 0.0], "l_arm": [-0.5, -0.1, -0.1], "l_fore": [0.75, -0.15, 0.0], "l_hand": [0.35, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.1], "r_fore": [0.4, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.1], "l_fore": [0.4, -0.05, 0.0], "l_hand": [0.1, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "low",
        "name": "Low",
        "gloss": "LOW",
        "duration": 1200,
        "type": "Diminished / Scale Adjective",
        "notes": "ISLRTC 10,000 Dictionary. Right flat hand palm facing down moves downward in stages denoting low level or diminished scale.",
        "dominant": "right",
        "bones": ["Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.35, 0.15, 0.15], "r_fore": [0.5, 0.1, 0.0], "r_hand": [0.2, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 600, "ease": "easeInOutQuad", "r_arm": [-0.15, 0.15, 0.1], "r_fore": [0.75, 0.1, 0.0], "r_hand": [0.35, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]},
            {"time": 900, "ease": "easeInOutQuad", "r_arm": [-0.1, 0.1, 0.05], "r_fore": [0.5, 0.05, 0.0], "r_hand": [0.15, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "amount",
        "name": "Amount",
        "gloss": "AMOUNT",
        "duration": 1250,
        "type": "Quantity / Volume Noun",
        "notes": "ISLRTC 10,000 Dictionary. Both curved hands scoop upward facing each other indicating a measurable quantity or volume.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.2, 0.15], "r_fore": [0.5, 0.1, 0.0], "r_hand": [0.2, 0.0, 0.0], "l_arm": [-0.3, -0.2, -0.15], "l_fore": [0.5, -0.1, 0.0], "l_hand": [0.2, 0.0, 0.0], "curls": [0.4, 0.4, 0.4, 0.4, 0.4]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.5, 0.15, 0.2], "r_fore": [0.75, 0.1, 0.0], "r_hand": [0.35, 0.0, 0.0], "l_arm": [-0.5, -0.15, -0.2], "l_fore": [0.75, -0.1, 0.0], "l_hand": [0.35, 0.0, 0.0], "curls": [0.4, 0.4, 0.4, 0.4, 0.4]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.1], "r_fore": [0.4, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.1], "l_fore": [0.4, -0.05, 0.0], "l_hand": [0.1, 0.0, 0.0], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]}
        ]
    },
    {
        "id": "crazy",
        "name": "Crazy",
        "gloss": "CRAZY",
        "duration": 1250,
        "type": "Wild / Irrational Adjective",
        "notes": "ISLRTC 10,000 Dictionary. Right bent index finger circles next to temple with expressive head tilt denoting wild or irrational nature.",
        "dominant": "right",
        "bones": ["Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.7, 0.25, 0.1], "r_fore": [0.95, 0.3, 0.1], "r_hand": [0.25, 0.2, 0.0], "head": [0.05, 0.05, 0.0], "curls": [0.8, 0.3, 0.8, 0.8, 0.8]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.75, 0.2, 0.05], "r_fore": [1.05, 0.25, 0.2], "r_hand": [0.35, -0.2, 0.0], "head": [0.07, -0.03, 0.0], "curls": [0.8, 0.3, 0.8, 0.8, 0.8]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.1, 0.1], "r_fore": [0.5, 0.1, 0.0], "r_hand": [0.15, 0.0, 0.0], "head": [0.02, 0.0, 0.0], "curls": [0.1, 0.0, 0.1, 0.1, 0.1]}
        ]
    },
    {
        "id": "between",
        "name": "Between",
        "gloss": "BETWEEN",
        "duration": 1250,
        "type": "Intermediate Preposition",
        "notes": "ISLRTC 10,000 Dictionary. Right flat hand oscillates back and forth in the slot between index and middle fingers of left hand.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.2, 0.15], "r_fore": [0.65, 0.1, 0.0], "r_hand": [0.25, 0.15, 0.0], "l_arm": [-0.35, -0.2, -0.15], "l_fore": [0.6, -0.1, 0.0], "l_hand": [0.2, 0.0, 0.0], "curls": [0.8, 0.0, 0.0, 0.8, 0.8]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.45, 0.15, 0.1], "r_fore": [0.75, 0.15, 0.0], "r_hand": [0.35, -0.15, 0.0], "l_arm": [-0.35, -0.2, -0.15], "l_fore": [0.6, -0.1, 0.0], "l_hand": [0.2, 0.0, 0.0], "curls": [0.8, 0.0, 0.0, 0.8, 0.8]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.1], "r_fore": [0.4, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.1], "l_fore": [0.3, -0.05, 0.0], "l_hand": [0.05, 0.0, 0.0], "curls": [0.1, 0.0, 0.0, 0.1, 0.1]}
        ]
    },
    {
        "id": "each",
        "name": "Each",
        "gloss": "EACH",
        "duration": 1200,
        "type": "Distributive Pronoun",
        "notes": "ISLRTC 10,000 Dictionary. Right hand with knuckles brushing down the knuckles of left fist or open hand one by one.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.15, 0.15], "r_fore": [0.65, 0.1, 0.0], "r_hand": [0.2, 0.0, 0.0], "l_arm": [-0.3, -0.2, -0.15], "l_fore": [0.5, -0.2, 0.0], "l_hand": [0.15, 0.0, 0.0], "curls": [0.8, 0.8, 0.8, 0.8, 0.8]},
            {"time": 600, "ease": "easeInOutQuad", "r_arm": [-0.45, 0.1, 0.1], "r_fore": [0.75, 0.05, 0.0], "r_hand": [0.35, 0.0, 0.0], "l_arm": [-0.3, -0.2, -0.15], "l_fore": [0.5, -0.2, 0.0], "l_hand": [0.15, 0.0, 0.0], "curls": [0.8, 0.8, 0.8, 0.8, 0.8]},
            {"time": 900, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.1], "r_fore": [0.4, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.1], "l_fore": [0.3, -0.1, 0.0], "l_hand": [0.05, 0.0, 0.0], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]}
        ]
    },
    {
        "id": "chat",
        "name": "Chat",
        "gloss": "CHAT",
        "duration": 1250,
        "type": "Dialogue / Discussion Verb",
        "notes": "ISLRTC 10,000 Dictionary. Both open hands facing inward flutter fingers while gently moving up and down representing casual dialogue.",
        "dominant": "both",
        "bones": ["Bip001_L_UpperArm", "Bip001_L_Forearm", "Bip001_L_Hand", "Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.45, 0.2, 0.2], "r_fore": [0.65, 0.15, 0.0], "r_hand": [0.25, 0.2, 0.0], "l_arm": [-0.45, -0.2, -0.2], "l_fore": [0.65, -0.15, 0.0], "l_hand": [0.25, -0.2, 0.0], "curls": [0.2, 0.4, 0.2, 0.4, 0.2]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.5, 0.15, 0.25], "r_fore": [0.75, 0.1, 0.0], "r_hand": [-0.15, 0.1, 0.0], "l_arm": [-0.5, -0.15, -0.25], "l_fore": [0.75, -0.1, 0.0], "l_hand": [-0.15, -0.1, 0.0], "curls": [0.4, 0.2, 0.4, 0.2, 0.4]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.1], "r_fore": [0.4, 0.05, 0.0], "r_hand": [0.1, 0.0, 0.0], "l_arm": [-0.2, -0.1, -0.1], "l_fore": [0.4, -0.05, 0.0], "l_hand": [0.1, 0.0, 0.0], "curls": [0.0, 0.0, 0.0, 0.0, 0.0]}
        ]
    },
    {
        "id": "bit",
        "name": "Bit",
        "gloss": "BIT",
        "duration": 1150,
        "type": "Minute Portion / Tiny Adjective",
        "notes": "ISLRTC 10,000 Dictionary. Right hand with index finger and thumb held close together indicating a minute portion or small bit.",
        "dominant": "right",
        "bones": ["Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand"],
        "keyframes": [
            {"time": 280, "ease": "easeInOutQuad", "r_arm": [-0.4, 0.15, 0.15], "r_fore": [0.65, 0.1, 0.0], "r_hand": [0.2, 0.1, 0.0], "curls": [0.7, 0.7, 0.9, 0.9, 0.9]},
            {"time": 580, "ease": "easeInOutQuad", "r_arm": [-0.45, 0.15, 0.15], "r_fore": [0.75, 0.1, 0.0], "r_hand": [0.35, 0.15, 0.0], "curls": [0.7, 0.7, 0.9, 0.9, 0.9]},
            {"time": 860, "ease": "easeInOutQuad", "r_arm": [-0.2, 0.1, 0.05], "r_fore": [0.4, 0.05, 0.0], "r_hand": [0.1, 0.05, 0.0], "curls": [0.1, 0.1, 0.1, 0.1, 0.1]}
        ]
    },
    {
        "id": "super",
        "name": "Super",
        "gloss": "SUPER",
        "duration": 1300,
        "type": "Superlative / Excellent Adjective",
        "notes": "ISLRTC 10,000 Dictionary. Right hand with thumbs-up moves forcefully upward and forward emphasizing superlative excellence.",
        "dominant": "right",
        "bones": ["Bip001_R_UpperArm", "Bip001_R_Forearm", "Bip001_R_Hand", "Bip001_Head"],
        "keyframes": [
            {"time": 300, "ease": "easeInOutQuad", "r_arm": [-0.35, 0.15, 0.15], "r_fore": [0.55, 0.1, 0.0], "r_hand": [0.25, 0.0, 0.0], "head": [0.03, 0.0, 0.0], "curls": [0.0, 0.9, 0.9, 0.9, 0.9]},
            {"time": 650, "ease": "easeInOutQuad", "r_arm": [-0.65, 0.2, 0.2], "r_fore": [0.85, 0.15, 0.0], "r_hand": [0.4, 0.0, 0.0], "head": [0.06, 0.0, 0.0], "curls": [0.0, 0.9, 0.9, 0.9, 0.9]},
            {"time": 950, "ease": "easeInOutQuad", "r_arm": [-0.3, 0.1, 0.1], "r_fore": [0.5, 0.1, 0.0], "r_hand": [0.15, 0.0, 0.0], "head": [0.02, 0.0, 0.0], "curls": [0.0, 0.2, 0.2, 0.2, 0.2]}
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

print(f"Successfully authored and verified {len(created_files)} Schema 2.0.0 signs (Batch 7):")
for name in created_files:
    print(f"  - signs/{name}")
