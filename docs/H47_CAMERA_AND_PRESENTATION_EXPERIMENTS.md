# H47 Camera & Presentation Experiments

- **Evaluated Modes in Chrome 158:**
  1. `Full Body` (`400x478` px): zero limb/head clipping across `11` phases on A and `11` phases on B.
  2. `Half Body` (Phase 11 toggle): crisp upper-body/head/hand framing with superior finger visibility.
  3. **Playback Speeds (`0.5x`, `1.0x`, `1.5x`):** `TimelineSynchronizer` + `SignScheduler` maintained synchronization without drift or lost state across speed changes, pause/resume, and forward/backward seeks.
- **Accessibility Recommendation:** Keep `Half Body` (hips/torso-up) as the recommended default for comprehension-oriented viewing, retaining `Full Body` as a one-click toggle.
