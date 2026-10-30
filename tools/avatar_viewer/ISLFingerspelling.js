/**
 * ISL Two-Handed Manual Alphabet & Fingerspelling Engine (Phase H15)
 *
 * Source: ISLRTC (Indian Sign Language Research and Training Centre)
 * Standards: Official Indian Sign Language two-handed manual alphabet.
 *
 * Distinct from ASL (one-handed). Vowels are formed by the dominant (right)
 * index finger pointing to the tips of the non-dominant (left) hand:
 *   A -> Left Thumb
 *   E -> Left Index
 *   I -> Left Middle
 *   O -> Left Ring
 *   U -> Left Pinky
 */

export const ISL_ALPHABET = Object.freeze({
  A: {
    letter: 'A',
    type: 'VOWEL',
    description: 'Dominant right index finger touches tip of open non-dominant left thumb',
    duration_ms: 600,
    dominant_hand: 'both',
    target_finger: 'thumb',
    rotations: {
      right_wrist: { x: -10, y: 15, z: -10 },
      left_wrist: { x: 10, y: -15, z: 10 }
    },
    finger_curls: {
      right: { thumb: 60, index: 0, middle: 75, ring: 75, pinky: 75 },
      left: { thumb: 0, index: 0, middle: 0, ring: 0, pinky: 0 }
    }
  },
  E: {
    letter: 'E',
    type: 'VOWEL',
    description: 'Dominant right index finger touches tip of non-dominant left index finger',
    duration_ms: 600,
    dominant_hand: 'both',
    target_finger: 'index',
    rotations: {
      right_wrist: { x: -12, y: 18, z: -12 },
      left_wrist: { x: 10, y: -15, z: 10 }
    },
    finger_curls: {
      right: { thumb: 60, index: 0, middle: 75, ring: 75, pinky: 75 },
      left: { thumb: 0, index: 0, middle: 0, ring: 0, pinky: 0 }
    }
  },
  I: {
    letter: 'I',
    type: 'VOWEL',
    description: 'Dominant right index finger touches tip of non-dominant left middle finger',
    duration_ms: 600,
    dominant_hand: 'both',
    target_finger: 'middle',
    rotations: {
      right_wrist: { x: -14, y: 20, z: -14 },
      left_wrist: { x: 10, y: -15, z: 10 }
    },
    finger_curls: {
      right: { thumb: 60, index: 0, middle: 75, ring: 75, pinky: 75 },
      left: { thumb: 0, index: 0, middle: 0, ring: 0, pinky: 0 }
    }
  },
  O: {
    letter: 'O',
    type: 'VOWEL',
    description: 'Dominant right index finger touches tip of non-dominant left ring finger',
    duration_ms: 600,
    dominant_hand: 'both',
    target_finger: 'ring',
    rotations: {
      right_wrist: { x: -16, y: 22, z: -16 },
      left_wrist: { x: 10, y: -15, z: 10 }
    },
    finger_curls: {
      right: { thumb: 60, index: 0, middle: 75, ring: 75, pinky: 75 },
      left: { thumb: 0, index: 0, middle: 0, ring: 0, pinky: 0 }
    }
  },
  U: {
    letter: 'U',
    type: 'VOWEL',
    description: 'Dominant right index finger touches tip of non-dominant left pinky finger',
    duration_ms: 600,
    dominant_hand: 'both',
    target_finger: 'pinky',
    rotations: {
      right_wrist: { x: -18, y: 24, z: -18 },
      left_wrist: { x: 10, y: -15, z: 10 }
    },
    finger_curls: {
      right: { thumb: 60, index: 0, middle: 75, ring: 75, pinky: 75 },
      left: { thumb: 0, index: 0, middle: 0, ring: 0, pinky: 0 }
    }
  },
  B: {
    letter: 'B',
    type: 'CONSONANT',
    description: 'Both hands join curved fingers forming two circles contacting at fingertips and thumbs',
    duration_ms: 650,
    dominant_hand: 'both'
  },
  C: {
    letter: 'C',
    type: 'CONSONANT',
    description: 'Dominant hand forms curved C-handshape facing partner',
    duration_ms: 600,
    dominant_hand: 'right'
  },
  D: {
    letter: 'D',
    type: 'CONSONANT',
    description: 'Non-dominant index points up; dominant hand forms arc touching left tip and base',
    duration_ms: 650,
    dominant_hand: 'both'
  },
  L: {
    letter: 'L',
    type: 'CONSONANT',
    description: 'Dominant hand forms L-shape with thumb and index at right angles across left palm',
    duration_ms: 600,
    dominant_hand: 'right'
  },
  M: {
    letter: 'M',
    type: 'CONSONANT',
    description: 'Dominant three fingers (index, middle, ring) rest across open flat left palm',
    duration_ms: 650,
    dominant_hand: 'both'
  },
  N: {
    letter: 'N',
    type: 'CONSONANT',
    description: 'Dominant two fingers (index, middle) rest across open flat left palm',
    duration_ms: 650,
    dominant_hand: 'both'
  },
  P: {
    letter: 'P',
    type: 'CONSONANT',
    description: 'Dominant thumb and index form circle touching extended upright left index finger',
    duration_ms: 650,
    dominant_hand: 'both'
  },
  T: {
    letter: 'T',
    type: 'CONSONANT',
    description: 'Dominant index finger touches the outer edge of open non-dominant hand',
    duration_ms: 600,
    dominant_hand: 'both'
  }
});

/**
 * Composes a full Schema 2.0.0 motion sequence for fingerspelling a word.
 */
export function composeFingerspellingMotion(word) {
  const letters = String(word || '').toUpperCase().replace(/[^A-Z]/g, '').split('');
  if (!letters.length) return null;

  const letterDuration = 550;
  const totalDuration = letters.length * letterDuration + 600; // lead-in and lead-out

  const involved_bones = [
    'Bip001_R_Clavicle', 'Bip001_R_UpperArm', 'Bip001_R_Forearm', 'Bip001_R_Hand',
    'Bip001_L_Clavicle', 'Bip001_L_UpperArm', 'Bip001_L_Forearm', 'Bip001_L_Hand',
    'Bip001_Head'
  ];

  const keyframes = [];

  // Frame 0: Neutral
  keyframes.push({
    time_ms: 0,
    label: 'Neutral',
    easing: 'easeInOutQuad',
    rotations: Object.fromEntries(involved_bones.map(b => [b, { x: 0, y: 0, z: 0 }])),
    finger_curls: { thumb: 0, index: 0, middle: 0, ring: 0, pinky: 0 }
  });

  // Intermediate letters
  letters.forEach((char, idx) => {
    const time_ms = 300 + idx * letterDuration;
    const isVowel = ['A', 'E', 'I', 'O', 'U'].includes(char);
    const def = ISL_ALPHABET[char];

    keyframes.push({
      time_ms,
      label: `FS: ${char} (${def?.description || 'ISL character shape'})`,
      easing: 'easeInOutQuad',
      rotations: {
        Bip001_R_Clavicle: { x: 0, y: 4, z: -2 },
        Bip001_R_UpperArm: { x: -10, y: -15, z: -45 },
        Bip001_R_Forearm: { x: 0, y: -25, z: -60 },
        Bip001_R_Hand: def?.rotations?.right_wrist || { x: -12, y: 15, z: -10 },
        Bip001_L_Clavicle: { x: 0, y: -4, z: 2 },
        Bip001_L_UpperArm: { x: -8, y: 10, z: 38 },
        Bip001_L_Forearm: { x: 0, y: 20, z: 55 },
        Bip001_L_Hand: def?.rotations?.left_wrist || { x: 10, y: -15, z: 10 },
        Bip001_Head: { x: 2, y: 0, z: 0 }
      },
      finger_curls: def?.finger_curls?.right || { thumb: 45, index: 0, middle: 60, ring: 60, pinky: 60 }
    });
  });

  // Final Frame: Neutral
  keyframes.push({
    time_ms: totalDuration,
    label: 'Neutral',
    easing: 'easeInOutQuad',
    rotations: Object.fromEntries(involved_bones.map(b => [b, { x: 0, y: 0, z: 0 }])),
    finger_curls: { thumb: 0, index: 0, middle: 0, ring: 0, pinky: 0 }
  });

  return {
    schema_version: '2.0.0',
    sign_id: `fs_${word.toLowerCase()}`,
    metadata: {
      display_name: `Fingerspell: ${word.toUpperCase()}`,
      gloss: `FS:${word.toUpperCase()}`,
      language: 'ISL',
      lexical_type: 'Two-handed manual alphabet fingerspelling sequence',
      validation_status: 'IMPLEMENTATION_PENDING_LINGUISTIC_REVIEW',
      source: {
        organization: 'ISLRTC',
        portal: 'Indian Sign Language Research and Training Centre',
        url: 'https://divyangjan.depwd.gov.in/islrtc/'
      },
      notes: `Two-handed ISL fingerspelled sequence for ${word.toUpperCase()} composed from canonical manual alphabet.`
    },
    motion: {
      status: 'playable',
      duration_ms: totalDuration,
      dominant_hand: 'both',
      return_to_neutral: true,
      transition_hints: { safe_transition: 'neutral', direct_blend_supported: false },
      involved_bones,
      keyframes
    }
  };
}
