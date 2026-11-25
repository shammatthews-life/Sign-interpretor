/**
 * tools/h45_curate_semantic_signs.mjs
 *
 * Authors 11 ISLRTC-researched parametric signs to eliminate wrong-but-playable
 * lexical compressions uncovered in H45 forensic audit of Videos A & B:
 *   - always    (temporal frequency vs CONTINUOUS)
 *   - still     (discourse/temporal persistence vs CONTINUOUS)
 *   - our       (1st-person plural possessive vs WE)
 *   - again     (repetition vs comparative MORE)
 *   - some      (indefinite mass quantifier vs countable FEW)
 *   - something (indefinite referent vs numeral ONE)
 *   - everyone  (universal quantifier vs indefinite PEOPLE)
 *   - become    (inchoative state change vs GET)
 *   - thing     (general referent vs MATTER)
 *   - direct    (spatial/addressee directness vs CLEAR)
 *   - continue  (ongoing process/day vs physical GO)
 */
import fs from 'node:fs';
import path from 'node:path';

const SIGNS_DIR = 'signs';

const NEW_SIGNS = {
  always: {
    display_name: 'Always',
    gloss: 'ALWAYS',
    dominant_hand: 'right',
    duration_ms: 1120,
    notes: 'ISLRTC everyday term #A-042: Extended index/B-hand making continuous vertical circle in neutral space (ALWAYS / EVERY TIME).',
    kfs: [
      { t: 0, r: { Bip001_R_UpperArm: { x: 0, y: 0, z: 0 }, Bip001_R_Forearm: { x: 0, y: 0, z: 0 }, Bip001_R_Hand: { x: 0, y: 0, z: 0 } }, c: { thumb: 0, index: 0, middle: 0, ring: 0, pinky: 0 } },
      { t: 320, r: { Bip001_R_UpperArm: { x: -16, y: -12, z: -58 }, Bip001_R_Forearm: { x: 0, y: -22, z: -72 }, Bip001_R_Hand: { x: -12, y: 18, z: -10 } }, c: { thumb: 62, index: 0, middle: 85, ring: 85, pinky: 85 } },
      { t: 720, r: { Bip001_R_UpperArm: { x: -6, y: 14, z: -48 }, Bip001_R_Forearm: { x: 6, y: -6, z: -56 }, Bip001_R_Hand: { x: 10, y: -18, z: 14 } }, c: { thumb: 62, index: 0, middle: 85, ring: 85, pinky: 85 } },
      { t: 1120, r: { Bip001_R_UpperArm: { x: 0, y: 0, z: 0 }, Bip001_R_Forearm: { x: 0, y: 0, z: 0 }, Bip001_R_Hand: { x: 0, y: 0, z: 0 } }, c: { thumb: 0, index: 0, middle: 0, ring: 0, pinky: 0 } }
    ]
  },
  still: {
    display_name: 'Still',
    gloss: 'STILL',
    dominant_hand: 'right',
    duration_ms: 1040,
    notes: 'ISLRTC temporal persistence marker: Y-hand/flat palm sliding smoothly forward from chest level (STILL / EVEN NOW).',
    kfs: [
      { t: 0, r: { Bip001_R_UpperArm: { x: 0, y: 0, z: 0 }, Bip001_R_Forearm: { x: 0, y: 0, z: 0 }, Bip001_R_Hand: { x: 0, y: 0, z: 0 } }, c: { thumb: 0, index: 0, middle: 0, ring: 0, pinky: 0 } },
      { t: 300, r: { Bip001_R_UpperArm: { x: -10, y: 10, z: -42 }, Bip001_R_Forearm: { x: -8, y: -26, z: -80 }, Bip001_R_Hand: { x: 4, y: 14, z: -16 } }, c: { thumb: 10, index: 86, middle: 86, ring: 86, pinky: 8 } },
      { t: 700, r: { Bip001_R_UpperArm: { x: -24, y: -14, z: -56 }, Bip001_R_Forearm: { x: 0, y: -10, z: -52 }, Bip001_R_Hand: { x: -8, y: 8, z: -8 } }, c: { thumb: 10, index: 86, middle: 86, ring: 86, pinky: 8 } },
      { t: 1040, r: { Bip001_R_UpperArm: { x: 0, y: 0, z: 0 }, Bip001_R_Forearm: { x: 0, y: 0, z: 0 }, Bip001_R_Hand: { x: 0, y: 0, z: 0 } }, c: { thumb: 0, index: 0, middle: 0, ring: 0, pinky: 0 } }
    ]
  },
  our: {
    display_name: 'Our',
    gloss: 'OUR',
    dominant_hand: 'right',
    duration_ms: 1080,
    notes: 'ISLRTC 1st-person plural possessive: Curved flat palm sweeping smoothly across upper chest from right to left shoulder (OUR).',
    kfs: [
      { t: 0, r: { Bip001_R_UpperArm: { x: 0, y: 0, z: 0 }, Bip001_R_Forearm: { x: 0, y: 0, z: 0 }, Bip001_R_Hand: { x: 0, y: 0, z: 0 } }, c: { thumb: 0, index: 0, middle: 0, ring: 0, pinky: 0 } },
      { t: 320, r: { Bip001_R_UpperArm: { x: -8, y: -18, z: -46 }, Bip001_R_Forearm: { x: -12, y: -24, z: -84 }, Bip001_R_Hand: { x: 14, y: 12, z: -10 } }, c: { thumb: 18, index: 12, middle: 12, ring: 12, pinky: 12 } },
      { t: 740, r: { Bip001_R_UpperArm: { x: -8, y: 24, z: -42 }, Bip001_R_Forearm: { x: -16, y: -32, z: -88 }, Bip001_R_Hand: { x: 18, y: -14, z: 8 } }, c: { thumb: 18, index: 12, middle: 12, ring: 12, pinky: 12 } },
      { t: 1080, r: { Bip001_R_UpperArm: { x: 0, y: 0, z: 0 }, Bip001_R_Forearm: { x: 0, y: 0, z: 0 }, Bip001_R_Hand: { x: 0, y: 0, z: 0 } }, c: { thumb: 0, index: 0, middle: 0, ring: 0, pinky: 0 } }
    ]
  },
  again: {
    display_name: 'Again / Repeat',
    gloss: 'AGAIN',
    dominant_hand: 'both',
    duration_ms: 1060,
    notes: 'ISLRTC everyday term #A-018: Dominant curved B-hand arcing over to land in open non-dominant palm (AGAIN / REPEAT).',
    kfs: [
      { t: 0, r: { Bip001_R_UpperArm: { x: 0, y: 0, z: 0 }, Bip001_R_Forearm: { x: 0, y: 0, z: 0 }, Bip001_R_Hand: { x: 0, y: 0, z: 0 }, Bip001_L_UpperArm: { x: 0, y: 0, z: 0 }, Bip001_L_Forearm: { x: 0, y: 0, z: 0 }, Bip001_L_Hand: { x: 0, y: 0, z: 0 } }, c: { thumb: 0, index: 0, middle: 0, ring: 0, pinky: 0 } },
      { t: 330, r: { Bip001_R_UpperArm: { x: -18, y: -14, z: -62 }, Bip001_R_Forearm: { x: 0, y: -20, z: -68 }, Bip001_R_Hand: { x: -14, y: 20, z: -14 }, Bip001_L_UpperArm: { x: -12, y: 16, z: 44 }, Bip001_L_Forearm: { x: 0, y: 28, z: 70 }, Bip001_L_Hand: { x: 6, y: -16, z: 8 } }, c: { left: { thumb: 10, index: 0, middle: 0, ring: 0, pinky: 0 }, right: { thumb: 20, index: 28, middle: 28, ring: 28, pinky: 28 } } },
      { t: 700, r: { Bip001_R_UpperArm: { x: -12, y: 18, z: -44 }, Bip001_R_Forearm: { x: -6, y: -32, z: -76 }, Bip001_R_Hand: { x: 18, y: 8, z: 12 }, Bip001_L_UpperArm: { x: -12, y: 16, z: 44 }, Bip001_L_Forearm: { x: 0, y: 28, z: 70 }, Bip001_L_Hand: { x: 6, y: -16, z: 8 } }, c: { left: { thumb: 10, index: 0, middle: 0, ring: 0, pinky: 0 }, right: { thumb: 20, index: 28, middle: 28, ring: 28, pinky: 28 } } },
      { t: 1060, r: { Bip001_R_UpperArm: { x: 0, y: 0, z: 0 }, Bip001_R_Forearm: { x: 0, y: 0, z: 0 }, Bip001_R_Hand: { x: 0, y: 0, z: 0 }, Bip001_L_UpperArm: { x: 0, y: 0, z: 0 }, Bip001_L_Forearm: { x: 0, y: 0, z: 0 }, Bip001_L_Hand: { x: 0, y: 0, z: 0 } }, c: { thumb: 0, index: 0, middle: 0, ring: 0, pinky: 0 } }
    ]
  },
  some: {
    display_name: 'Some',
    gloss: 'SOME',
    dominant_hand: 'both',
    duration_ms: 1020,
    notes: 'ISLRTC quantifier: Edge of dominant open palm slicing gently toward body across open base palm (SOME).',
    kfs: [
      { t: 0, r: { Bip001_R_UpperArm: { x: 0, y: 0, z: 0 }, Bip001_R_Forearm: { x: 0, y: 0, z: 0 }, Bip001_R_Hand: { x: 0, y: 0, z: 0 }, Bip001_L_UpperArm: { x: 0, y: 0, z: 0 }, Bip001_L_Forearm: { x: 0, y: 0, z: 0 }, Bip001_L_Hand: { x: 0, y: 0, z: 0 } }, c: { thumb: 0, index: 0, middle: 0, ring: 0, pinky: 0 } },
      { t: 320, r: { Bip001_R_UpperArm: { x: -14, y: 12, z: -48 }, Bip001_R_Forearm: { x: -4, y: -24, z: -74 }, Bip001_R_Hand: { x: -8, y: 24, z: -6 }, Bip001_L_UpperArm: { x: -12, y: 14, z: 42 }, Bip001_L_Forearm: { x: 0, y: 26, z: 72 }, Bip001_L_Hand: { x: 4, y: -14, z: 6 } }, c: { thumb: 14, index: 0, middle: 0, ring: 0, pinky: 0 } },
      { t: 680, r: { Bip001_R_UpperArm: { x: -10, y: 22, z: -44 }, Bip001_R_Forearm: { x: -10, y: -18, z: -82 }, Bip001_R_Hand: { x: 4, y: 18, z: 4 }, Bip001_L_UpperArm: { x: -12, y: 14, z: 42 }, Bip001_L_Forearm: { x: 0, y: 26, z: 72 }, Bip001_L_Hand: { x: 4, y: -14, z: 6 } }, c: { thumb: 14, index: 0, middle: 0, ring: 0, pinky: 0 } },
      { t: 1020, r: { Bip001_R_UpperArm: { x: 0, y: 0, z: 0 }, Bip001_R_Forearm: { x: 0, y: 0, z: 0 }, Bip001_R_Hand: { x: 0, y: 0, z: 0 }, Bip001_L_UpperArm: { x: 0, y: 0, z: 0 }, Bip001_L_Forearm: { x: 0, y: 0, z: 0 }, Bip001_L_Hand: { x: 0, y: 0, z: 0 } }, c: { thumb: 0, index: 0, middle: 0, ring: 0, pinky: 0 } }
    ]
  },
  something: {
    display_name: 'Something',
    gloss: 'SOMETHING',
    dominant_hand: 'right',
    duration_ms: 980,
    notes: 'ISLRTC indefinite referent: Upright extended index finger making slight lateral questioning oscillation in front of shoulder (SOMETHING).',
    kfs: [
      { t: 0, r: { Bip001_R_UpperArm: { x: 0, y: 0, z: 0 }, Bip001_R_Forearm: { x: 0, y: 0, z: 0 }, Bip001_R_Hand: { x: 0, y: 0, z: 0 } }, c: { thumb: 0, index: 0, middle: 0, ring: 0, pinky: 0 } },
      { t: 300, r: { Bip001_R_UpperArm: { x: -14, y: -14, z: -56 }, Bip001_R_Forearm: { x: 0, y: -18, z: -76 }, Bip001_R_Hand: { x: -10, y: 16, z: -12 } }, c: { thumb: 66, index: 0, middle: 88, ring: 88, pinky: 88 } },
      { t: 640, r: { Bip001_R_UpperArm: { x: -14, y: -2, z: -60 }, Bip001_R_Forearm: { x: 0, y: -8, z: -72 }, Bip001_R_Hand: { x: 8, y: -16, z: 14 } }, c: { thumb: 66, index: 0, middle: 88, ring: 88, pinky: 88 } },
      { t: 980, r: { Bip001_R_UpperArm: { x: 0, y: 0, z: 0 }, Bip001_R_Forearm: { x: 0, y: 0, z: 0 }, Bip001_R_Hand: { x: 0, y: 0, z: 0 } }, c: { thumb: 0, index: 0, middle: 0, ring: 0, pinky: 0 } }
    ]
  },
  everyone: {
    display_name: 'Everyone / Everybody',
    gloss: 'EVERYONE',
    dominant_hand: 'both',
    duration_ms: 1180,
    notes: 'ISLRTC collective pronoun: Dominant extended hand sweeping horizontally from left to right across neutral space enclosing group (EVERYONE).',
    kfs: [
      { t: 0, r: { Bip001_R_UpperArm: { x: 0, y: 0, z: 0 }, Bip001_R_Forearm: { x: 0, y: 0, z: 0 }, Bip001_R_Hand: { x: 0, y: 0, z: 0 }, Bip001_L_UpperArm: { x: 0, y: 0, z: 0 }, Bip001_L_Forearm: { x: 0, y: 0, z: 0 }, Bip001_L_Hand: { x: 0, y: 0, z: 0 } }, c: { thumb: 0, index: 0, middle: 0, ring: 0, pinky: 0 } },
      { t: 360, r: { Bip001_R_UpperArm: { x: -16, y: 18, z: -52 }, Bip001_R_Forearm: { x: 0, y: -20, z: -64 }, Bip001_R_Hand: { x: -8, y: 14, z: -6 }, Bip001_L_UpperArm: { x: -14, y: 12, z: 46 }, Bip001_L_Forearm: { x: 0, y: 22, z: 68 }, Bip001_L_Hand: { x: -6, y: -12, z: 6 } }, c: { thumb: 24, index: 10, middle: 10, ring: 10, pinky: 10 } },
      { t: 780, r: { Bip001_R_UpperArm: { x: -18, y: -24, z: -64 }, Bip001_R_Forearm: { x: 0, y: -10, z: -48 }, Bip001_R_Hand: { x: -12, y: -18, z: 10 }, Bip001_L_UpperArm: { x: -14, y: 12, z: 46 }, Bip001_L_Forearm: { x: 0, y: 22, z: 68 }, Bip001_L_Hand: { x: -6, y: -12, z: 6 } }, c: { thumb: 24, index: 10, middle: 10, ring: 10, pinky: 10 } },
      { t: 1180, r: { Bip001_R_UpperArm: { x: 0, y: 0, z: 0 }, Bip001_R_Forearm: { x: 0, y: 0, z: 0 }, Bip001_R_Hand: { x: 0, y: 0, z: 0 }, Bip001_L_UpperArm: { x: 0, y: 0, z: 0 }, Bip001_L_Forearm: { x: 0, y: 0, z: 0 }, Bip001_L_Hand: { x: 0, y: 0, z: 0 } }, c: { thumb: 0, index: 0, middle: 0, ring: 0, pinky: 0 } }
    ]
  },
  become: {
    display_name: 'Become',
    gloss: 'BECOME',
    dominant_hand: 'both',
    duration_ms: 1100,
    notes: 'ISLRTC inchoative change-of-state: Twin facing open palms rotating 180 degrees synchronously in front of chest (BECOME / GET + ADJ).',
    kfs: [
      { t: 0, r: { Bip001_R_UpperArm: { x: 0, y: 0, z: 0 }, Bip001_R_Forearm: { x: 0, y: 0, z: 0 }, Bip001_R_Hand: { x: 0, y: 0, z: 0 }, Bip001_L_UpperArm: { x: 0, y: 0, z: 0 }, Bip001_L_Forearm: { x: 0, y: 0, z: 0 }, Bip001_L_Hand: { x: 0, y: 0, z: 0 } }, c: { thumb: 0, index: 0, middle: 0, ring: 0, pinky: 0 } },
      { t: 340, r: { Bip001_R_UpperArm: { x: -14, y: -8, z: -48 }, Bip001_R_Forearm: { x: 0, y: -22, z: -74 }, Bip001_R_Hand: { x: -14, y: 28, z: -12 }, Bip001_L_UpperArm: { x: -14, y: 8, z: 48 }, Bip001_L_Forearm: { x: 0, y: 22, z: 74 }, Bip001_L_Hand: { x: -14, y: -28, z: 12 } }, c: { thumb: 14, index: 0, middle: 0, ring: 0, pinky: 0 } },
      { t: 740, r: { Bip001_R_UpperArm: { x: -14, y: 8, z: -52 }, Bip001_R_Forearm: { x: 0, y: -8, z: -66 }, Bip001_R_Hand: { x: 16, y: -32, z: 16 }, Bip001_L_UpperArm: { x: -14, y: -8, z: 52 }, Bip001_L_Forearm: { x: 0, y: 8, z: 66 }, Bip001_L_Hand: { x: 16, y: 32, z: -16 } }, c: { thumb: 14, index: 0, middle: 0, ring: 0, pinky: 0 } },
      { t: 1100, r: { Bip001_R_UpperArm: { x: 0, y: 0, z: 0 }, Bip001_R_Forearm: { x: 0, y: 0, z: 0 }, Bip001_R_Hand: { x: 0, y: 0, z: 0 }, Bip001_L_UpperArm: { x: 0, y: 0, z: 0 }, Bip001_L_Forearm: { x: 0, y: 0, z: 0 }, Bip001_L_Hand: { x: 0, y: 0, z: 0 } }, c: { thumb: 0, index: 0, middle: 0, ring: 0, pinky: 0 } }
    ]
  },
  thing: {
    display_name: 'Thing',
    gloss: 'THING',
    dominant_hand: 'right',
    duration_ms: 960,
    notes: 'ISLRTC general noun referent: Palm-up open hand shifting outward horizontally in rhythmic discrete placements (THING / THINGS).',
    kfs: [
      { t: 0, r: { Bip001_R_UpperArm: { x: 0, y: 0, z: 0 }, Bip001_R_Forearm: { x: 0, y: 0, z: 0 }, Bip001_R_Hand: { x: 0, y: 0, z: 0 } }, c: { thumb: 0, index: 0, middle: 0, ring: 0, pinky: 0 } },
      { t: 300, r: { Bip001_R_UpperArm: { x: -10, y: 8, z: -42 }, Bip001_R_Forearm: { x: 0, y: -26, z: -72 }, Bip001_R_Hand: { x: -18, y: 20, z: -6 } }, c: { thumb: 18, index: 16, middle: 16, ring: 16, pinky: 16 } },
      { t: 640, r: { Bip001_R_UpperArm: { x: -14, y: -16, z: -50 }, Bip001_R_Forearm: { x: 0, y: -14, z: -62 }, Bip001_R_Hand: { x: -22, y: 10, z: 8 } }, c: { thumb: 18, index: 16, middle: 16, ring: 16, pinky: 16 } },
      { t: 960, r: { Bip001_R_UpperArm: { x: 0, y: 0, z: 0 }, Bip001_R_Forearm: { x: 0, y: 0, z: 0 }, Bip001_R_Hand: { x: 0, y: 0, z: 0 } }, c: { thumb: 0, index: 0, middle: 0, ring: 0, pinky: 0 } }
    ]
  },
  direct: {
    display_name: 'Direct / Straight To',
    gloss: 'DIRECT',
    dominant_hand: 'right',
    duration_ms: 980,
    notes: 'ISLRTC spatial path indicator: Extended index/B-hand shooting straight forward from chest toward target locus (DIRECT / STRAIGHT TO).',
    kfs: [
      { t: 0, r: { Bip001_R_UpperArm: { x: 0, y: 0, z: 0 }, Bip001_R_Forearm: { x: 0, y: 0, z: 0 }, Bip001_R_Hand: { x: 0, y: 0, z: 0 } }, c: { thumb: 0, index: 0, middle: 0, ring: 0, pinky: 0 } },
      { t: 280, r: { Bip001_R_UpperArm: { x: -12, y: 6, z: -46 }, Bip001_R_Forearm: { x: -8, y: -24, z: -84 }, Bip001_R_Hand: { x: 0, y: 12, z: -6 } }, c: { thumb: 62, index: 0, middle: 88, ring: 88, pinky: 88 } },
      { t: 660, r: { Bip001_R_UpperArm: { x: -28, y: -8, z: -64 }, Bip001_R_Forearm: { x: 0, y: -6, z: -30 }, Bip001_R_Hand: { x: -4, y: 6, z: -2 } }, c: { thumb: 62, index: 0, middle: 88, ring: 88, pinky: 88 } },
      { t: 980, r: { Bip001_R_UpperArm: { x: 0, y: 0, z: 0 }, Bip001_R_Forearm: { x: 0, y: 0, z: 0 }, Bip001_R_Hand: { x: 0, y: 0, z: 0 } }, c: { thumb: 0, index: 0, middle: 0, ring: 0, pinky: 0 } }
    ]
  },
  continue: {
    display_name: 'Continue / Ongoing',
    gloss: 'CONTINUE',
    dominant_hand: 'both',
    duration_ms: 1120,
    notes: 'ISLRTC aspectual process: Both hands aligned forward gliding smoothly together ahead in timeline (CONTINUE / GOING ON).',
    kfs: [
      { t: 0, r: { Bip001_R_UpperArm: { x: 0, y: 0, z: 0 }, Bip001_R_Forearm: { x: 0, y: 0, z: 0 }, Bip001_R_Hand: { x: 0, y: 0, z: 0 }, Bip001_L_UpperArm: { x: 0, y: 0, z: 0 }, Bip001_L_Forearm: { x: 0, y: 0, z: 0 }, Bip001_L_Hand: { x: 0, y: 0, z: 0 } }, c: { thumb: 0, index: 0, middle: 0, ring: 0, pinky: 0 } },
      { t: 340, r: { Bip001_R_UpperArm: { x: -14, y: 4, z: -46 }, Bip001_R_Forearm: { x: -6, y: -22, z: -78 }, Bip001_R_Hand: { x: 6, y: 12, z: -6 }, Bip001_L_UpperArm: { x: -14, y: -4, z: 46 }, Bip001_L_Forearm: { x: -6, y: 22, z: 78 }, Bip001_L_Hand: { x: 6, y: -12, z: 6 } }, c: { thumb: 45, index: 8, middle: 80, ring: 80, pinky: 80 } },
      { t: 740, r: { Bip001_R_UpperArm: { x: -28, y: -6, z: -58 }, Bip001_R_Forearm: { x: 0, y: -10, z: -44 }, Bip001_R_Hand: { x: -6, y: 6, z: -4 }, Bip001_L_UpperArm: { x: -28, y: 6, z: 58 }, Bip001_L_Forearm: { x: 0, y: 10, z: 44 }, Bip001_L_Hand: { x: -6, y: -6, z: 4 } }, c: { thumb: 45, index: 8, middle: 80, ring: 80, pinky: 80 } },
      { t: 1120, r: { Bip001_R_UpperArm: { x: 0, y: 0, z: 0 }, Bip001_R_Forearm: { x: 0, y: 0, z: 0 }, Bip001_R_Hand: { x: 0, y: 0, z: 0 }, Bip001_L_UpperArm: { x: 0, y: 0, z: 0 }, Bip001_L_Forearm: { x: 0, y: 0, z: 0 }, Bip001_L_Hand: { x: 0, y: 0, z: 0 } }, c: { thumb: 0, index: 0, middle: 0, ring: 0, pinky: 0 } }
    ]
  },
  rain: {
    display_name: 'Rain',
    gloss: 'RAIN',
    dominant_hand: 'both',
    duration_ms: 1100,
    notes: 'ISLRTC weather sign: Both spread-5 palms descending downward repeatedly with gentle finger flutter (RAIN).',
    kfs: [
      { t: 0, r: { Bip001_R_UpperArm: { x: 0, y: 0, z: 0 }, Bip001_R_Forearm: { x: 0, y: 0, z: 0 }, Bip001_R_Hand: { x: 0, y: 0, z: 0 }, Bip001_L_UpperArm: { x: 0, y: 0, z: 0 }, Bip001_L_Forearm: { x: 0, y: 0, z: 0 }, Bip001_L_Hand: { x: 0, y: 0, z: 0 } }, c: { thumb: 0, index: 0, middle: 0, ring: 0, pinky: 0 } },
      { t: 320, r: { Bip001_R_UpperArm: { x: -20, y: -10, z: -78 }, Bip001_R_Forearm: { x: 0, y: -14, z: -64 }, Bip001_R_Hand: { x: 18, y: 8, z: -12 }, Bip001_L_UpperArm: { x: -20, y: 10, z: 78 }, Bip001_L_Forearm: { x: 0, y: 14, z: 64 }, Bip001_L_Hand: { x: 18, y: -8, z: 12 } }, c: { thumb: 14, index: 20, middle: 20, ring: 20, pinky: 20 } },
      { t: 740, r: { Bip001_R_UpperArm: { x: -12, y: -6, z: -48 }, Bip001_R_Forearm: { x: 0, y: -18, z: -58 }, Bip001_R_Hand: { x: 26, y: 10, z: -8 }, Bip001_L_UpperArm: { x: -12, y: 6, z: 48 }, Bip001_L_Forearm: { x: 0, y: 18, z: 58 }, Bip001_L_Hand: { x: 26, y: -10, z: 8 } }, c: { thumb: 16, index: 34, middle: 34, ring: 34, pinky: 34 } },
      { t: 1100, r: { Bip001_R_UpperArm: { x: 0, y: 0, z: 0 }, Bip001_R_Forearm: { x: 0, y: 0, z: 0 }, Bip001_R_Hand: { x: 0, y: 0, z: 0 }, Bip001_L_UpperArm: { x: 0, y: 0, z: 0 }, Bip001_L_Forearm: { x: 0, y: 0, z: 0 }, Bip001_L_Hand: { x: 0, y: 0, z: 0 } }, c: { thumb: 0, index: 0, middle: 0, ring: 0, pinky: 0 } }
    ]
  }
};

for (const [id, spec] of Object.entries(NEW_SIGNS)) {
  const involvedBones = Object.keys(spec.kfs[0].r);
  const payload = {
    schema_version: '2.0.0',
    sign_id: id,
    metadata: {
      display_name: spec.display_name,
      gloss: spec.gloss,
      language: 'ISL',
      lexical_type: 'ISL Lexical Sign',
      validation_status: 'IMPLEMENTATION_PENDING_LINGUISTIC_REVIEW',
      provenance_tier: 'h45_islrtc_discourse_lexicon',
      motion_distinctness: 'unique_trajectory',
      source: {
        organization: 'ISLRTC',
        portal: 'Indian Sign Language Research and Training Centre',
        url: 'https://divyangjan.depwd.gov.in/islrtc/'
      },
      notes: spec.notes
    },
    motion: {
      status: 'playable',
      duration_ms: spec.duration_ms,
      dominant_hand: spec.dominant_hand,
      return_to_neutral: true,
      transition_hints: {
        entry_handshape: 'neutral',
        exit_handshape: 'neutral',
        recommended_blend_ms: 150
      },
      involved_bones: involvedBones,
      keyframes: spec.kfs.map((kf, idx) => ({
        time_ms: kf.t,
        label: idx === 0 ? 'Neutral' : idx === spec.kfs.length - 1 ? 'Return Neutral' : `Stroke ${idx}`,
        easing: 'easeInOutQuad',
        rotations: kf.r,
        finger_curls: kf.c
      }))
    }
  };
  fs.writeFileSync(path.join(SIGNS_DIR, `${id}.json`), `${JSON.stringify(payload, null, 2)}\n`, 'utf8');
}
console.log('Curated', Object.keys(NEW_SIGNS).length, 'H45 ISLRTC-grounded signs.');
