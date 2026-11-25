/**
 * tools/h44_curate_semantic_signs.mjs
 *
 * Authors 5 strictly justified ISLRTC-researched parametric signs to eliminate
 * semantic collisions discovered during H44 sentence-level audit of Videos A and B:
 *   - famous     (prevents "best known" -> "I GOOD KNOW" role inversion)
 *   - only       (restrictive modifier "just a vlog / just a shot", vs SAME)
 *   - around     (approximative/spatial "hour or so", "around the world")
 *   - remaining  (prevents "rest of the evening" -> sleep/relax "REST")
 *   - many       (plural quantifier vs comparative "MORE")
 */
import fs from 'fs';
import path from 'path';

const SIGNS_DIR = 'signs';

const NEW_SIGNS = {
  famous: {
    display_name: 'Famous',
    gloss: 'FAMOUS',
    dominant_hand: 'both',
    duration_ms: 1200,
    notes: 'Two index fingers arcing upward and outward from temples/forehead (public recognition / FAMOUS).',
    kfs: [
      { t: 0, r: { Bip001_R_UpperArm: { x: 0, y: 0, z: 0 }, Bip001_R_Forearm: { x: 0, y: 0, z: 0 }, Bip001_R_Hand: { x: 0, y: 0, z: 0 }, Bip001_L_UpperArm: { x: 0, y: 0, z: 0 }, Bip001_L_Forearm: { x: 0, y: 0, z: 0 }, Bip001_L_Hand: { x: 0, y: 0, z: 0 }, Bip001_Head: { x: 0, y: 0, z: 0 } }, c: { thumb: 0, index: 0, middle: 0, ring: 0, pinky: 0 } },
      { t: 350, r: { Bip001_R_UpperArm: { x: -16, y: -6, z: -86 }, Bip001_R_Forearm: { x: 0, y: -26, z: -76 }, Bip001_R_Hand: { x: -8, y: 12, z: -8 }, Bip001_L_UpperArm: { x: -16, y: 6, z: 86 }, Bip001_L_Forearm: { x: 0, y: 26, z: 76 }, Bip001_L_Hand: { x: -8, y: -12, z: 8 }, Bip001_Head: { x: -3, y: 0, z: 0 } }, c: { thumb: 65, index: 0, middle: 85, ring: 85, pinky: 85 } },
      { t: 780, r: { Bip001_R_UpperArm: { x: -24, y: 14, z: -74 }, Bip001_R_Forearm: { x: 0, y: 6, z: -48 }, Bip001_R_Hand: { x: -14, y: 18, z: -12 }, Bip001_L_UpperArm: { x: -24, y: -14, z: 74 }, Bip001_L_Forearm: { x: 0, y: -6, z: 48 }, Bip001_L_Hand: { x: -14, y: -18, z: 12 }, Bip001_Head: { x: -5, y: 0, z: 0 } }, c: { thumb: 65, index: 0, middle: 85, ring: 85, pinky: 85 } },
      { t: 1200, r: { Bip001_R_UpperArm: { x: 0, y: 0, z: 0 }, Bip001_R_Forearm: { x: 0, y: 0, z: 0 }, Bip001_R_Hand: { x: 0, y: 0, z: 0 }, Bip001_L_UpperArm: { x: 0, y: 0, z: 0 }, Bip001_L_Forearm: { x: 0, y: 0, z: 0 }, Bip001_L_Hand: { x: 0, y: 0, z: 0 }, Bip001_Head: { x: 0, y: 0, z: 0 } }, c: { thumb: 0, index: 0, middle: 0, ring: 0, pinky: 0 } }
    ]
  },
  only: {
    display_name: 'Only',
    gloss: 'ONLY',
    dominant_hand: 'right',
    duration_ms: 980,
    notes: 'Single upright index finger twisting sharply in front of chest (restrictive ONLY / JUST).',
    kfs: [
      { t: 0, r: { Bip001_R_UpperArm: { x: 0, y: 0, z: 0 }, Bip001_R_Forearm: { x: 0, y: 0, z: 0 }, Bip001_R_Hand: { x: 0, y: 0, z: 0 }, Bip001_Head: { x: 0, y: 0, z: 0 } }, c: { thumb: 0, index: 0, middle: 0, ring: 0, pinky: 0 } },
      { t: 300, r: { Bip001_R_UpperArm: { x: -12, y: -6, z: -56 }, Bip001_R_Forearm: { x: 0, y: -22, z: -72 }, Bip001_R_Hand: { x: -8, y: 24, z: -12 }, Bip001_Head: { x: 0, y: 0, z: 0 } }, c: { thumb: 70, index: 0, middle: 88, ring: 88, pinky: 88 } },
      { t: 620, r: { Bip001_R_UpperArm: { x: -12, y: 4, z: -58 }, Bip001_R_Forearm: { x: 0, y: -12, z: -68 }, Bip001_R_Hand: { x: 10, y: -28, z: 16 }, Bip001_Head: { x: 2, y: 0, z: 0 } }, c: { thumb: 70, index: 0, middle: 88, ring: 88, pinky: 88 } },
      { t: 980, r: { Bip001_R_UpperArm: { x: 0, y: 0, z: 0 }, Bip001_R_Forearm: { x: 0, y: 0, z: 0 }, Bip001_R_Hand: { x: 0, y: 0, z: 0 }, Bip001_Head: { x: 0, y: 0, z: 0 } }, c: { thumb: 0, index: 0, middle: 0, ring: 0, pinky: 0 } }
    ]
  },
  around: {
    display_name: 'Around / Approximately',
    gloss: 'AROUND',
    dominant_hand: 'both',
    duration_ms: 1120,
    notes: 'Dominant spread hand orbiting around stationary base index finger in neutral space (AROUND / APPROXIMATELY).',
    kfs: [
      { t: 0, r: { Bip001_R_UpperArm: { x: 0, y: 0, z: 0 }, Bip001_R_Forearm: { x: 0, y: 0, z: 0 }, Bip001_R_Hand: { x: 0, y: 0, z: 0 }, Bip001_L_UpperArm: { x: 0, y: 0, z: 0 }, Bip001_L_Forearm: { x: 0, y: 0, z: 0 }, Bip001_L_Hand: { x: 0, y: 0, z: 0 } }, c: { left: { thumb: 65, index: 0, middle: 85, ring: 85, pinky: 85 }, right: { thumb: 0, index: 0, middle: 0, ring: 0, pinky: 0 } } },
      { t: 360, r: { Bip001_R_UpperArm: { x: -16, y: -14, z: -48 }, Bip001_R_Forearm: { x: 6, y: -28, z: -64 }, Bip001_R_Hand: { x: -10, y: 16, z: -8 }, Bip001_L_UpperArm: { x: -10, y: 10, z: 42 }, Bip001_L_Forearm: { x: 0, y: 24, z: 64 }, Bip001_L_Hand: { x: -6, y: -10, z: 6 } }, c: { left: { thumb: 65, index: 0, middle: 85, ring: 85, pinky: 85 }, right: { thumb: 20, index: 22, middle: 22, ring: 22, pinky: 22 } } },
      { t: 740, r: { Bip001_R_UpperArm: { x: -8, y: 16, z: -56 }, Bip001_R_Forearm: { x: -6, y: -12, z: -54 }, Bip001_R_Hand: { x: 12, y: -18, z: 12 }, Bip001_L_UpperArm: { x: -10, y: 10, z: 42 }, Bip001_L_Forearm: { x: 0, y: 24, z: 64 }, Bip001_L_Hand: { x: -6, y: -10, z: 6 } }, c: { left: { thumb: 65, index: 0, middle: 85, ring: 85, pinky: 85 }, right: { thumb: 20, index: 22, middle: 22, ring: 22, pinky: 22 } } },
      { t: 1120, r: { Bip001_R_UpperArm: { x: 0, y: 0, z: 0 }, Bip001_R_Forearm: { x: 0, y: 0, z: 0 }, Bip001_R_Hand: { x: 0, y: 0, z: 0 }, Bip001_L_UpperArm: { x: 0, y: 0, z: 0 }, Bip001_L_Forearm: { x: 0, y: 0, z: 0 }, Bip001_L_Hand: { x: 0, y: 0, z: 0 } }, c: { thumb: 0, index: 0, middle: 0, ring: 0, pinky: 0 } }
    ]
  },
  remaining: {
    display_name: 'Remaining',
    gloss: 'REMAINING',
    dominant_hand: 'both',
    duration_ms: 1100,
    notes: 'Open left palm dividing timeline while right flat hand sweeps forward into remaining space (REMAINING / REST OF).',
    kfs: [
      { t: 0, r: { Bip001_R_UpperArm: { x: 0, y: 0, z: 0 }, Bip001_R_Forearm: { x: 0, y: 0, z: 0 }, Bip001_R_Hand: { x: 0, y: 0, z: 0 }, Bip001_L_UpperArm: { x: 0, y: 0, z: 0 }, Bip001_L_Forearm: { x: 0, y: 0, z: 0 }, Bip001_L_Hand: { x: 0, y: 0, z: 0 } }, c: { thumb: 0, index: 0, middle: 0, ring: 0, pinky: 0 } },
      { t: 340, r: { Bip001_R_UpperArm: { x: -10, y: -10, z: -44 }, Bip001_R_Forearm: { x: 0, y: -24, z: -66 }, Bip001_R_Hand: { x: -8, y: 12, z: -6 }, Bip001_L_UpperArm: { x: -12, y: 12, z: 46 }, Bip001_L_Forearm: { x: 0, y: 26, z: 62 }, Bip001_L_Hand: { x: -6, y: -14, z: 6 } }, c: { thumb: 10, index: 0, middle: 0, ring: 0, pinky: 0 } },
      { t: 740, r: { Bip001_R_UpperArm: { x: -18, y: 14, z: -62 }, Bip001_R_Forearm: { x: 0, y: 8, z: -42 }, Bip001_R_Hand: { x: -14, y: 20, z: -10 }, Bip001_L_UpperArm: { x: -12, y: 12, z: 46 }, Bip001_L_Forearm: { x: 0, y: 26, z: 62 }, Bip001_L_Hand: { x: -6, y: -14, z: 6 } }, c: { thumb: 10, index: 0, middle: 0, ring: 0, pinky: 0 } },
      { t: 1100, r: { Bip001_R_UpperArm: { x: 0, y: 0, z: 0 }, Bip001_R_Forearm: { x: 0, y: 0, z: 0 }, Bip001_R_Hand: { x: 0, y: 0, z: 0 }, Bip001_L_UpperArm: { x: 0, y: 0, z: 0 }, Bip001_L_Forearm: { x: 0, y: 0, z: 0 }, Bip001_L_Hand: { x: 0, y: 0, z: 0 } }, c: { thumb: 0, index: 0, middle: 0, ring: 0, pinky: 0 } }
    ]
  },
  many: {
    display_name: 'Many',
    gloss: 'MANY',
    dominant_hand: 'both',
    duration_ms: 1080,
    notes: 'Two closed fists flicking open repeatedly upward into spread-5 shapes (MANY / NUMEROUS).',
    kfs: [
      { t: 0, r: { Bip001_R_UpperArm: { x: 0, y: 0, z: 0 }, Bip001_R_Forearm: { x: 0, y: 0, z: 0 }, Bip001_R_Hand: { x: 0, y: 0, z: 0 }, Bip001_L_UpperArm: { x: 0, y: 0, z: 0 }, Bip001_L_Forearm: { x: 0, y: 0, z: 0 }, Bip001_L_Hand: { x: 0, y: 0, z: 0 } }, c: { thumb: 0, index: 0, middle: 0, ring: 0, pinky: 0 } },
      { t: 300, r: { Bip001_R_UpperArm: { x: -12, y: -8, z: -48 }, Bip001_R_Forearm: { x: 0, y: -20, z: -68 }, Bip001_R_Hand: { x: -10, y: 14, z: -8 }, Bip001_L_UpperArm: { x: -12, y: 8, z: 48 }, Bip001_L_Forearm: { x: 0, y: 20, z: 68 }, Bip001_L_Hand: { x: -10, y: -14, z: 8 } }, c: { thumb: 78, index: 88, middle: 88, ring: 88, pinky: 88 } },
      { t: 680, r: { Bip001_R_UpperArm: { x: -16, y: 6, z: -58 }, Bip001_R_Forearm: { x: 0, y: 4, z: -50 }, Bip001_R_Hand: { x: -16, y: 20, z: -12 }, Bip001_L_UpperArm: { x: -16, y: -6, z: 58 }, Bip001_L_Forearm: { x: 0, y: -4, z: 50 }, Bip001_L_Hand: { x: -16, y: -20, z: 12 } }, c: { thumb: 0, index: 5, middle: 5, ring: 5, pinky: 5 } },
      { t: 1080, r: { Bip001_R_UpperArm: { x: 0, y: 0, z: 0 }, Bip001_R_Forearm: { x: 0, y: 0, z: 0 }, Bip001_R_Hand: { x: 0, y: 0, z: 0 }, Bip001_L_UpperArm: { x: 0, y: 0, z: 0 }, Bip001_L_Forearm: { x: 0, y: 0, z: 0 }, Bip001_L_Hand: { x: 0, y: 0, z: 0 } }, c: { thumb: 0, index: 0, middle: 0, ring: 0, pinky: 0 } }
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
      provenance_tier: 'h44_semantic_repair_parametric',
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
  fs.writeFileSync(path.join(SIGNS_DIR, `${id}.json`), JSON.stringify(payload, null, 2) + '\n', 'utf8');
}
console.log('Curated', Object.keys(NEW_SIGNS).length, 'H44 semantic repair signs.');
