# H46 Independent ISL Linguistic Research & Kinematic Specification

**Research Date:** 2026-11-25  
**Validation Boundary:** Engineering implementation grounded in published linguistic literature and ISLRTC documentation; remains `PENDING_DEAF_COMMUNITY_REVIEW` until evaluated by Deaf ISL linguists and native signers.

---

## 1. Primary Linguistic Sources & Provenance

1. **Ulrike Zeshan** (*Sign Language Typology*, Indo-Pakistani Sign Language / ISL clause-typing, negation, and interrogatives; ACL Anthology / ResearchGate / CSLDS):
   - **Negation (`NMM-NEG-HEADSHAKE`):** Horizontal headshake acts as a prosodic/syntactic scope marker spanning the negative predicate or clause-final negative particle.
   - **Wh-Questions (`NMM-WH-BROW-FURROW`):** Wh-elements typically occupy clause-final position in ISL (`YOU NAME WHAT`), accompanied by lowered/furrowed brows and slight forward head/chin pitch.
   - **Polar Yes/No & Conditional Clauses (`NMM-YESNO-BROW-RAISE`, `NMM-COND-BROW-RAISE`):** Marked by raised eyebrows, slight upward chin/head posture, and subtle forward torso/head lean over the scope of the question or condition.
2. **Dr. Samar Sinha** (*Indian Sign Language: An Analysis of its Grammar*, JNU):
   - **Spatial Locus Assignment:** Referents (people, groups, objects, contrasting topics) are assigned distinct spatial loci (`LOCUS_LEFT`, `LOCUS_RIGHT`) in 3D signing space for discourse cohesion and anaphoric reference.
   - **Agreement / Directional Verbs:** Verbs such as `HELP`, `GIVE`, `TELL`, `SHOW`, `ASK`, `TEACH`, `BRING` inflect spatially from source locus toward target locus.
   - **Role Shift (Body Shift / Perspective):** Signer shifts upper torso (`Bip001_Spine1`) and head/gaze toward a character locus to mark reported speech or character perspective without spoken quote tags.
3. **ISLRTC (Indian Sign Language Research and Training Centre, New Delhi)** — *ISL Dictionary / Sign Learn*:
   - **Five-Parameter Phonological Distinctiveness:** Handshape (`finger_curls`), palm orientation, location, movement, and NMMs distinguish minimal pairs. Identical 3D bone rotations across unrelated concepts (`beautiful` vs `tell`, `two` vs `three` vs `five`, `base` vs `communication`, `open` vs `scene`, `ask` vs `show`) violate ISL phonological distinctiveness and impair comprehension.

---

## 2. H46 3D Skeletal & Kinematic Mapping (Engineered Approximation)

Because the AetherShadow GLB rig exposes skeletal joints (`Bip001_Head`, `Bip001_Spine1`, `Bip001_R_*`, `Bip001_L_*`, and 5-finger curl channels) without facial blendshapes, H46 maps NMMs and spatial grammar to readable upper-body and head kinematics layered additively over base sign keyframes:

| Grammatical Marker | Linguistic Basis | 3D Kinematic Actuation in `SignAnimationPlayer.js` |
|---|---|---|
| `NMM-NEG-HEADSHAKE` | Zeshan (IPSL/ISL negation scope) | Sinusoidal `Bip001_Head.rotation.y` (`±10°`, 2 cycles per sign) + subtle brow-tension pitch (`+2°`) |
| `NMM-WH-BROW-FURROW` | Zeshan / ISL clause-final WH marking | Forward attentive head pitch (`Bip001_Head.rotation.x` `+6.5°`) + slight inquisitive lateral tilt (`Bip001_Head.rotation.z` `+4°`) + subtle forward torso lean (`Bip001_Spine1.rotation.x` `+2.5°`) |
| `NMM-YESNO-BROW-RAISE` / `NMM-COND-BROW-RAISE` | Zeshan / CSLDS polar & conditional NMM | Upward attentive chin (`Bip001_Head.rotation.x` `-5.5°`) + slight forward lean (`Bip001_Spine1.rotation.x` `+3°`) |
| `NMM-EMPHATIC-NOD` | Clause-level affirmative/assertion prosody | Rhythmic affirmative nod (`Bip001_Head.rotation.x` `+6°` downward pulse) |
| `LOCUS_LEFT` / `LOCUS_RIGHT` & `ROLE_SHIFT` | Sinha (ISL spatial grammar & role shift) | Upper-torso & shoulder yaw (`Bip001_Spine1.rotation.y` `±10°` for loci, `±12°` for role shift) + matching head gaze bias (`Bip001_Head.rotation.y` `±6°`) |
| `DIRECTIONAL_VERB` (`help`, `give`, `tell`, `show`, `ask`, `teach`, `bring`) | Sinha (ISL agreement verb inflection) | Directional yaw bias (`spatialYawDeg` on `Bip001_Spine1` & `Bip001_R_UpperArm` / `Bip001_L_UpperArm`) from subject locus toward object locus |

---

## 3. Regional & Engineering Scope Boundaries

- **Regional Variation:** ISL exhibits documented lexical variation across Delhi, Mumbai, Kolkata, Bengaluru, and regional Deaf communities; ISLRTC standardization is used as the primary reference baseline.
- **Facial Blendshape Limitation:** The current AetherShadow rig lacks eyebrow/lip morph targets; therefore brow furrow and brow raise are conveyed via head pitch/tilt and posture cues until a blendshape-capable avatar rig is introduced.
