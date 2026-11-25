# Phase A: Aether 3D Avatar Inspection and First Display Report

**Project:** ISL Accessibility Translator
**Phase:** Phase A — Aether Avatar Asset Inspection & Minimal Viewer Proof-of-Concept
**Asset Path:** `D:\sign interpretor\Avatar_Boy_Gun_AetherShadow`
**Date:** October 1, 2026

---

## 1. Executive Summary

As part of the initial investigation into visual 3D avatar rendering for Indian Sign Language (ISL), the local 3D character asset `Avatar_Boy_Gun_AetherShadow` was thoroughly inspected at the binary, structural, and skeletal levels.

The inspection confirms that **Aether is a high-fidelity, production-grade 3D bipedal character model with fully articulated 5-finger skeletal rigs on both hands**, making it ideally suited for the fine-grained finger spelling and lexical handshape requirements of Indian Sign Language.

---

## 2. File Inventory

The asset folder contains 11 primary files and 1 subdirectory (`Materials/`):

| File Name | Size | Type / Role |
| :--- | :--- | :--- |
| `Avatar_Boy_Gun_AetherShadow.fbx` | 2,809,152 bytes (~2.8 MB) | **Primary 3D Avatar Model** (FBX Binary) |
| `Avatar_Boy_Gun_AetherShadow_Tex_Body_Diffuse.png` | 853,997 bytes | Diffuse texture for body and garments |
| `Avatar_Boy_Gun_AetherShadow_Tex_Body_Shadow_Ramp.png` | 604 bytes | Cel-shading shadow gradient ramp for body |
| `Avatar_Boy_Gun_AetherShadow_Tex_Face_Diffuse.png` | 287,900 bytes | Diffuse texture for face and eyebrows |
| `Avatar_Boy_Gun_AetherShadow_Tex_Hair_Diffuse.png` | 880,595 bytes | Diffuse texture for hair and bangs |
| `Avatar_Boy_Gun_AetherShadow_Tex_Hair_Lightmap.png` | 436,320 bytes | Specular/hair highlight map |
| `Avatar_Boy_Gun_AetherShadow_Tex_Hair_Normalmap.png` | 402,862 bytes | Normal bump map for hair strands |
| `Avatar_Boy_Gun_AetherShadow_Tex_Hair_Shadow_Ramp.png` | 517 bytes | Cel-shading shadow ramp for hair |
| `Avatar_Boy_Gun_AetherShadow_Tex_Pupil_Diffuse.png` | 21,936 bytes | Eye pupil and iris diffuse texture |
| `Avatar_Boy_Gun_AetherShadow_Tex_Pupil_Lightmap.png` | 871 bytes | Eye glint and reflection map |
| `Avatar_Boy_Tex_FaceSDF.png` | 153,037 bytes | Signed Distance Field (SDF) face shadow mask |
| `Materials/` (Directory) | 8 JSON files | Serialized Unity toon/cel shader material presets |

---

## 3. Model Format & Technical Specifications

- **Container Format:** Autodesk Kaydara FBX Binary format.
- **FBX Version:** `7300` (FBX 2013/2014 specification).
- **Coordinate System:** Standard Y-up orientation, right-handed coordinates.
- **Mesh Objects (10 distinct mesh layers):**
  1. `Body` (Main torso, legs, arms, hands)
  2. `Face` (Facial skin geometry)
  3. `Bang` (Front hair fringe / bangs)
  4. `Brow` (Eyebrow geometry)
  5. `Face_Eye` (Eye sockets/sclera)
  6. `Pupil` (Irises and pupils)
  7. `EyeStar` (Stylized anime eye highlights)
  8. `EffectMesh` (Garment trim / accessory overlays)
  9. `Eff_Model_TPS_Dress_Upgrade_01` (Costume upgrade layer 1)
  10. `Eff_Model_TPS_Dress_Upgrade_02` (Costume upgrade layer 2)
- **Materials (8 materials):**
  - `Avatar_Boy_Gun_AetherShadow_Mat_Body`
  - `Avatar_Boy_Gun_AetherShadow_Mat_Face`
  - `Avatar_Boy_Gun_AetherShadow_Mat_Hair`
  - `Avatar_Boy_Gun_AetherShadow_Mat_Pupil`
  - `Avatar_Boy_Gun_AetherShadow_Mat_Brow`
  - `Avatar_Boy_Gun_AetherShadow_Mat_Dress`
  - `Eff_Aura_996_UD_T_38`
  - `Eff_Aura_996_UD_T_40`

---

## 4. Skeletal Armature & Rig Analysis

- **Total Rig Elements:** **254 models** (10 meshes + **244 LimbNode bone joints**).
- **Rig Standard:** Follows industry-standard 3ds Max Biped / Unity Humanoid conventions (`Bip001 ...`).
- **Core Skeleton:**
  - Root: `Bip001`
  - Spine chain: `Bip001 Pelvis` → `Bip001 Spine` → `Bip001 Spine1` → `Bip001 Spine2` → `Bip001 Neck` → `Bip001 Head`
  - Left arm: `Bip001 L Clavicle` → `Bip001 L UpperArm` (with twist joints) → `Bip001 L Forearm` → `Bip001 L Hand`
  - Right arm: `Bip001 R Clavicle` → `Bip001 R UpperArm` (with twist joints) → `Bip001 R Forearm` → `Bip001 R Hand`
  - Legs & Feet: Full hip, knee, ankle, and toe joints (`Bip001 L/R Thigh`, `Calf`, `Foot`, `Toe0`).
  - Auxiliary rigs: Complete dynamic hair strand bones (`Bone_Hair01_M` through `05_M`, `Bone_HairA01_L` through `F01_L`, `Bone_HairG01_R` through `M01_R`).

---

## 5. Hand and Finger Rigging Assessment (Critical for ISL)

Indian Sign Language requires precise, distinct finger configurations (e.g., thumb extensions, index pointing, V-handshapes, open palms, fists, and hooked fingers).

### Left Hand Finger Hierarchy:
- **Thumb (`Finger0`):** `Bip001 L Finger0` (Proximal) → `Bip001 L Finger01` (Intermediate) → `Bip001 L Finger02` (Distal) → `Bip001 L Finger0Nub` (Tip)
- **Index (`Finger1`):** `Bip001 L Finger1` (Proximal) → `Bip001 L Finger11` (Intermediate) → `Bip001 L Finger12` (Distal) → `Bip001 L Finger1Nub` (Tip)
- **Middle (`Finger2`):** `Bip001 L Finger2` (Proximal) → `Bip001 L Finger21` (Intermediate) → `Bip001 L Finger22` (Distal) → `Bip001 L Finger2Nub` (Tip)
- **Ring (`Finger3`):** `Bip001 L Finger3` (Proximal) → `Bip001 L Finger31` (Intermediate) → `Bip001 L Finger32` (Distal) → `Bip001 L Finger3Nub` (Tip)
- **Little/Pinky (`Finger4`):** `Bip001 L Finger4` (Proximal) → `Bip001 L Finger41` (Intermediate) → `Bip001 L Finger42` (Distal) → `Bip001 L Finger4Nub` (Tip)

### Right Hand Finger Hierarchy:
- Symmetrically identical to the left hand (`Bip001 R Finger0` through `Bip001 R Finger4` with joints `0`, `01`, `02`, and `Nub`).

### Articulation Verdict:
- **Individual Control:** **100% Yes.** Every single finger can be curled, splayed, or rotated independently across its 3 anatomical joints.
- **IK & Helpers:** Includes `Bone_IkHand01_L` and `Bone_IkHand01_R` for Inverse Kinematics hand positioning, as well as forearm twist compensation bones (`Bone_ForearmTwistA01_L/R`).

---

## 6. Facial Structure & Morphs

- **Bones:** Includes `Bip001 Head`, `Bip001 HeadNub`, `MoveHead`, `AO_Bip001 Head`, and four dedicated eye orientation bones:
  - `+EyeBone L A01`, `+EyeBone L A02`
  - `+EyeBone R A01`, `+EyeBone R A02`
- **Morphs / Blendshapes:** The FBX binary does not embed separate geometric blendshape target curves. Facial variation (eyes, eyebrows, mouth) is architected through layered modular meshes (`Brow`, `Face_Eye`, `Pupil`, `Face`) and texture masking (FaceSDF map).

---

## 7. Recommended Runtime: Three.js (WebGL)

### Why Three.js WebGL is the Optimal Approach:
1. **Zero Native C++ Compilation Overhead:** Python 3.12 lacks native, precompiled FBX SDK packages. Alternative Python 3D libraries (Open3D, PyBullet, Ursina) either do not support skinned FBX binary animations or require cumbersome C++ build tools.
2. **First-Class FBX Support:** Three.js features a mature, battle-tested `FBXLoader` that parses FBX 7300 binary geometry, skeletal skinning weights, and bone hierarchies natively.
3. **Hardware Acceleration:** Real-time 60 FPS WebGL rendering with PBR / Cel-shading in modern web browsers and desktop webviews.
4. **Direct Programmatic Bone Control:** Rotating any bone (e.g. `Bip001 L Finger1.rotation.z = -1.2`) instantly updates the 3D hand shape in the browser canvas.
5. **Portability:** Fits future project plans (desktop Electron/webview, standalone web app, or browser extension overlay).

---

## 8. Minimal Viewer Implementation

We implemented a lightweight, non-invasive proof-of-concept viewer in:
- `tools/avatar_viewer/index.html`: Three.js WebGL application featuring:
  - Full FBXLoader pipeline loading `/Avatar_Boy_Gun_AetherShadow/Avatar_Boy_Gun_AetherShadow.fbx`
  - Automatic diffuse texture mapping (`Body`, `Face`, `Hair`, `Pupil`)
  - 360-degree OrbitControls (pan, tilt, zoom)
  - Toggleable `SkeletonHelper` visualizer
  - Real-time Left Hand finger sliders (`Thumb`, `Index`, `Middle`, `Ring`, `Pinky`)
  - Quick pose test presets (`Left Fist`, `Left Point`, `Open Palm`, `Reset T-Pose`)
  - Camera presets (`Full Body`, `Upper Body`, `Left Hand`, `Right Hand`, `Face`)
- `tools/run_avatar_viewer.py`: Local Python HTTP server (with CORS headers) that serves the repository root and launches the browser viewer with a single command.

---

## 9. Verification & Test Results

1. **Model Loading:** **PASSED.** `Avatar_Boy_Gun_AetherShadow.fbx` loads completely without errors.
2. **Texture Loading:** **PASSED.** Body diffuse, face diffuse, hair diffuse, and pupil textures are mapped correctly.
3. **Skeleton Loading:** **PASSED.** All 244 LimbNodes are registered in the scene graph.
4. **Finger Articulation:** **PASSED.** Individual rotation of finger joints (Finger0–Finger4) verified.
5. **Git Safety:** **VERIFIED.** Added `Avatar_Boy_Gun_AetherShadow/` to `.gitignore` to prevent committing or pushing 3D binary assets to GitHub.

---

## 10. How to Run the Viewer

From the project root:

```powershell
.\.venv\Scripts\python.exe tools/run_avatar_viewer.py
```

This starts the server on `http://localhost:8000/` and automatically opens the 3D inspection viewer in your default browser.
