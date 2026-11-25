# ISL Sign Reference Record: MORNING (SIGN 1)

## Metadata
- **Term**: MORNING
- **Gloss**: MORNING
- **Variant**: SIGN 1 (Rising Sun / Iconic Dawn; Morning-1)
- **Source**: Indian Sign Language Research and Training Centre (ISLRTC) & FDMSE RKMVERI Indian Sign Language Portal
- **Publication**: Indian Sign Language Dictionary / Basic Communication Skills Course Module 1.2
- **Reference URLs**:
  - ISLRTC Portal: https://divyangjan.depwd.gov.in/islrtc/
  - ISLRTC Video Dictionary / Module 1.2: https://www.youtube.com/watch?v=kYJp6hW9oM8
  - ISLRTC Dictionary Entry ("Good morning"): https://www.youtube.com/watch?v=A2P3iR20zXk
  - FDMSE RKMVERI ISL Dictionary Portal: https://indiansignlanguage.org (Entry: Morning-1)
- **Dominant Hand**: Right
- **Lexical Type**: Lexical sign (iconic representation of rising sun / dawn); not fingerspelling

---

## REFERENCE OBSERVATION

The following parameters are established directly from published Indian Sign Language documentation and official ISLRTC / FDMSE instructional materials:

1. **Dominant Hand**:
   - RIGHT hand is dominant.
   - Non-dominant (Left) hand remains resting in neutral position at the side.

2. **Handshape & Finger Configuration**:
   - Flat open hand (B-handshape).
   - Fingers (Index, Middle, Ring, Pinky) are fully extended straight, held naturally together.
   - Thumb is relaxed, extended naturally alongside the edge of the palm.
   - The handshape is held stable throughout the entire upward movement.
   - NOT fingerspelling (no letter-by-letter alphabet representation `M-O-R-N-I-N-G`).
   - Fingers do not flutter, waggle, or close during the gesture.

3. **Spatial Location & Trajectory**:
   - **Starting Location**: Lower torso / abdominal height in front of the right sagittal plane.
   - **Ending Location**: Upper chest / shoulder level (elevated dawn position).
   - **Path**: Continuous, smooth upward vertical/sagittal ascent symbolizing the rising sun.

4. **Palm Orientation**:
   - Palm faces inward towards the body (posterosuperior / facing signer's torso) with a slight upward tilt.
   - Extended fingers point upwards and slightly inwards toward the centerline.

5. **Wrist Orientation**:
   - Wrist is neutral-to-slightly extended, maintaining stable inward/upward orientation of the flat palm as the arm ascends.

6. **Movement Characteristics**:
   - Smooth, continuous upward rising stroke.
   - Single motion (1 cycle); NOT a repetitive pulse (unlike GOOD which pulses back and forth).
   - NOT a temple salute (unlike HELLO which starts near the temple and extends outward).
   - NOT an outward sweep from the chin (unlike THANK YOU).
   - Gesture exhibits an apex hold at peak height before returning smoothly to neutral resting position.

7. **Repetitions & Timing Characteristics**:
   - Exactly 1 upward ascending stroke.
   - Moderate, gentle tempo reflecting dawn/sunrise (~1800 ms total gesture cycle).

8. **Body & Head Movement**:
   - Torso remains upright and stable in neutral alignment.
   - Subtle, natural head focus with slight chin elevation accompanying the upward ascent of the hand.

---

## UNCERTAIN / NEEDS REVIEW FIELDS

The following parameters cannot be determined with mathematical certainty from two-dimensional video references alone and are explicitly documented as pending certified Deaf specialist and linguistic review:

- **Exact Palm Angle Deviation**: UNKNOWN / NEEDS REVIEW (approximated as inward-facing with ~10°–15° posterosuperior tilt)
- **Exact Wrist Angle (Euler)**: UNKNOWN / NEEDS REVIEW (approximated within ±12° of anatomical neutral upright)
- **Exact Spatial Coordinates**: UNKNOWN / NEEDS REVIEW (approximated relative to Aether's clavicle and chest rig)
- **Exact Movement Amplitude**: UNKNOWN / NEEDS REVIEW (observed as ~25–35 cm vertical ascent from lower abdominal plane to clavicle height)
- **Exact Apex Dwell Duration**: UNKNOWN / NEEDS REVIEW (modeled as 200 ms hold at 1100–1300 ms for perceptual clarity)
- **Linguistic Validation Status**: IMPLEMENTATION_PENDING_LINGUISTIC_REVIEW (Technical animation status: TECHNICALLY_PLAYABLE)

---

## AETHER IMPLEMENTATION

The technical implementation on the Aether 3D FBX rig translates the verified visual observations into machine-readable keyframes adhering to Schema 2.0.0:

1. **Rig & Bone Mapping**:
   - Involves verified right arm bones: `Bip001_R_Clavicle`, `Bip001_R_UpperArm`, `Bip001_R_Forearm`, `Bip001_R_Hand`.
   - Involves verified right hand finger bones: `Bip001_R_Finger0` through `Bip001_R_Finger42` (15 individual phalangeal joints) plus `Bip001_Head`.
   - Non-dominant left arm bones remain unmanipulated (0 delta), guaranteeing zero asymmetry or unwanted motion.

2. **Handshape Stabilization**:
   - Flat B-handshape is maintained with all 5 finger curls set to 0.
   - Finger rotations remain at zero relative to bind pose, preventing finger drift or joint distortion.

3. **Keyframe Plan (Minimum Keyframes for Observed Motion)**:
   - **0 ms (Neutral Rest)**: Full anatomical bind pose, all rotation deltas zero.
   - **350 ms (Dawn Origin / Lower Start)**: Clavicle slightly engaged, upper arm forward, forearm flexed (~-68° z) at lower torso, palm facing inward.
   - **800 ms (Ascending Transport)**: Smooth upward rising stroke, upper arm elevating, forearm unfolding, subtle head lift.
   - **1100 ms (Peak Apex)**: Hand reaches upper chest / shoulder height, palm facing inward/upward.
   - **1300 ms (Peak Hold)**: Stabilized apex hold for linguistic readability.
   - **1800 ms (Neutral Rest)**: Smooth return to exact resting bind pose.

4. **Zero-Drift & Replay Protection**:
   - Delta-based rotation relative to cached FBX rest rotations.
   - Keyframe 0 and Keyframe 1800 ms are identical pure neutral states.
   - Per-segment `easeInOutQuad` easing ensures smooth, non-oscillating interpolation without overshoot.
