# H47 Accessibility Requirements Mapping (No False Compliance Claims)

| Standard Requirement | Project Component | Current Status | Identified Gap | Verification Method |
|---|---|---|---|---|
| **Intended meaning & ISL grammar** (ISO 20071-24 / WCAG 1.2.6) | `EnglishToISLTranslator.js` | **Partially Implemented** | Stateless cross-cue discourse, polysemy collisions, `PENDING_DEAF_COMMUNITY_REVIEW` | `test_h47_comprehension_and_discourse.mjs` + Deaf eval kit |
| **Sign-language selection & identification** | `manifest.json` (`language: "ISL"`) + popup UI | **Implemented (Technical)** | Regional ISL variants not yet selectable in UI | Manifest check + UI inspection |
| **Visual framing (hips/torso up & Full Body)** | `embed.js` + `CameraFraming` + `overlay.css` | **Implemented & Verified** | `Half Body` vs `Full Body` verified (`400x478` px); small-screen mobile responsive scaling untested | Chrome 158 contact sheets & crops |
| **Background contrast & clothing** | `embed.js` dark `#141422` backdrop + AetherShadow | **Partially Implemented** | AetherShadow outfit has metallic silver highlights; facial blendshapes absent | Visual accessibility audit |
| **Media synchronization (play/pause/seek/rate)** | `timeline-synchronizer.js` + `content-script.js` | **Implemented & Verified** | Verified on Chrome 158 for A & B (`0.5x`, `1.0x`, `1.5x`, seeks) | `run_h47_real_chrome_e2e.mjs` |
| **Facial NMM & finger legibility** | `SignAnimationPlayer.js` | **Partially Implemented** | Skeletal head/torso NMMs added in H46; true eyebrow/mouthing blendshapes unavailable on AetherShadow | Live Chrome bone telemetry + visual inspection |
| **Native Deaf user evaluation** | `tools/h47_build_deaf_eval_kit.mjs` | **Infrastructure Ready / Unverified by Users** | Zero Deaf participants recruited yet | `eval_protocol_pack.json` (`PENDING_DEAF_COMMUNITY_REVIEW`) |
