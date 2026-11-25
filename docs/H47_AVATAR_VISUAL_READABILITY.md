# H47 Avatar Visual Readability Audit

- **Surface & Framing:** `400x478` px floating panel (`#isl-floating-avatar-surface`) with solid dark `#141422` backdrop, verified in Chrome 158.
- **Full Body vs. Half Body Readability Finding:**
  - `Full Body` frames head-to-toe cleanly with zero clipping (`PEOPLE`, `THOUSAND`, `CONFUSED`, `REAL`, `VERY`, `ADVICE`), making gross arm/torso spatial shifts easy to see.
  - `Half Body` (observed on tile 11 of both contact sheets) enlarges the upper torso, face, and hands by ~2x, substantially improving finger-level handshape legibility in alignment with `WCAG 2.2 SC 1.2.6` (hips/torso-up framing).
- **Rig Limitation:** AetherShadow lacks eyebrow/mouth morph targets and has metallic silver outfit highlights; facial NMMs rely on head pitch/yaw/tilt (`Bip001_Head`) and torso lean (`Bip001_Spine1`).
