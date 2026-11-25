# H47 Motion Representation Research

1. **Current Representation:** Keyframed Euler bone rotations (`Bip001_*`) + 5-channel `finger_curls` + additive runtime procedural NMM/spatial overlays + co-articulated pose blending (`SignAnimationPlayer.js`).
2. **Strengths:** Deterministic, `0` extreme joint angles, smooth inter-sign transitions, and decoupled grammatical NMM/spatial overlays.
3. **Research Directions Identified for Future Work:**
   - **Parametric Spatial Anchors:** Parameterizing start/end wrist targets of agreement verbs (`HELP`, `GIVE`, `TELL`, `SHOW`) directly in 3D space rather than yawing the torso alone.
   - **Facial Blendshapes / Mouthing Rig:** Migrating or augmenting the GLB avatar with eyebrow/cheek/mouth morph targets for authentic non-manual articulation.
