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
    rotations: { right_wrist: { x: -10, y: 15, z: -10 }, left_wrist: { x: 10, y: -15, z: 10 } },
    finger_curls: {
      right: { thumb: 60, index: 0, middle: 75, ring: 75, pinky: 75 },
      left: { thumb: 0, index: 0, middle: 0, ring: 0, pinky: 0 }
    }
  },
  B: {
    letter: 'B',
    type: 'CONSONANT',
    description: 'Both hands form rounded loops touching at index and thumb tips',
    duration_ms: 600,
    dominant_hand: 'both',
    rotations: { right_wrist: { x: -12, y: 14, z: -8 }, left_wrist: { x: 12, y: -14, z: 8 } },
    finger_curls: {
      right: { thumb: 50, index: 50, middle: 0, ring: 0, pinky: 0 },
      left: { thumb: 50, index: 50, middle: 0, ring: 0, pinky: 0 }
    }
  },
  C: {
    letter: 'C',
    type: 'CONSONANT',
    description: 'Dominant hand forms curved C-shape held against non-dominant palm',
    duration_ms: 600,
    dominant_hand: 'both',
    rotations: { right_wrist: { x: -15, y: 18, z: -10 }, left_wrist: { x: 10, y: -12, z: 6 } },
    finger_curls: {
      right: { thumb: 30, index: 40, middle: 40, ring: 40, pinky: 40 },
      left: { thumb: 0, index: 0, middle: 0, ring: 0, pinky: 0 }
    }
  },
  D: {
    letter: 'D',
    type: 'CONSONANT',
    description: 'Left index points upward, right thumb and index form loop against left index',
    duration_ms: 650,
    dominant_hand: 'both',
    rotations: { right_wrist: { x: -12, y: 15, z: -8 }, left_wrist: { x: 5, y: -10, z: 5 } },
    finger_curls: {
      right: { thumb: 60, index: 60, middle: 80, ring: 80, pinky: 80 },
      left: { thumb: 80, index: 0, middle: 80, ring: 80, pinky: 80 }
    }
  },
  E: {
    letter: 'E',
    type: 'VOWEL',
    description: 'Dominant right index finger touches tip of non-dominant left index finger',
    duration_ms: 600,
    dominant_hand: 'both',
    target_finger: 'index',
    rotations: { right_wrist: { x: -12, y: 18, z: -12 }, left_wrist: { x: 10, y: -15, z: 10 } },
    finger_curls: {
      right: { thumb: 60, index: 0, middle: 75, ring: 75, pinky: 75 },
      left: { thumb: 0, index: 0, middle: 0, ring: 0, pinky: 0 }
    }
  },
  F: {
    letter: 'F',
    type: 'CONSONANT',
    description: 'Dominant index and middle finger rest across non-dominant index and middle',
    duration_ms: 600,
    dominant_hand: 'both',
    rotations: { right_wrist: { x: -10, y: 12, z: -8 }, left_wrist: { x: 10, y: -12, z: 8 } },
    finger_curls: {
      right: { thumb: 75, index: 0, middle: 0, ring: 85, pinky: 85 },
      left: { thumb: 75, index: 0, middle: 0, ring: 85, pinky: 85 }
    }
  },
  G: {
    letter: 'G',
    type: 'CONSONANT',
    description: 'Both hands form fists, dominant fist placed directly over non-dominant fist',
    duration_ms: 600,
    dominant_hand: 'both',
    rotations: { right_wrist: { x: -15, y: 10, z: -10 }, left_wrist: { x: 15, y: -10, z: 10 } },
    finger_curls: {
      right: { thumb: 80, index: 85, middle: 85, ring: 85, pinky: 85 },
      left: { thumb: 80, index: 85, middle: 85, ring: 85, pinky: 85 }
    }
  },
  H: {
    letter: 'H',
    type: 'CONSONANT',
    description: 'Dominant flat open hand strokes horizontally across non-dominant open palm',
    duration_ms: 650,
    dominant_hand: 'both',
    rotations: { right_wrist: { x: -10, y: 16, z: -10 }, left_wrist: { x: 10, y: -16, z: 10 } },
    finger_curls: {
      right: { thumb: 15, index: 10, middle: 10, ring: 10, pinky: 10 },
      left: { thumb: 15, index: 10, middle: 10, ring: 10, pinky: 10 }
    }
  },
  I: {
    letter: 'I',
    type: 'VOWEL',
    description: 'Dominant right index finger touches tip of non-dominant left middle finger',
    duration_ms: 600,
    dominant_hand: 'both',
    target_finger: 'middle',
    rotations: { right_wrist: { x: -14, y: 20, z: -14 }, left_wrist: { x: 10, y: -15, z: 10 } },
    finger_curls: {
      right: { thumb: 60, index: 0, middle: 75, ring: 75, pinky: 75 },
      left: { thumb: 0, index: 0, middle: 0, ring: 0, pinky: 0 }
    }
  },
  J: {
    letter: 'J',
    type: 'CONSONANT',
    description: 'Dominant index traces letter J downwards from tip of non-dominant middle finger',
    duration_ms: 700,
    dominant_hand: 'both',
    rotations: { right_wrist: { x: -12, y: 18, z: -10 }, left_wrist: { x: 10, y: -15, z: 10 } },
    finger_curls: {
      right: { thumb: 60, index: 0, middle: 75, ring: 75, pinky: 75 },
      left: { thumb: 0, index: 0, middle: 0, ring: 0, pinky: 0 }
    }
  },
  K: {
    letter: 'K',
    type: 'CONSONANT',
    description: 'Dominant bent index finger rests against upright non-dominant index finger',
    duration_ms: 650,
    dominant_hand: 'both',
    rotations: { right_wrist: { x: -10, y: 15, z: -8 }, left_wrist: { x: 5, y: -10, z: 5 } },
    finger_curls: {
      right: { thumb: 65, index: 45, middle: 80, ring: 80, pinky: 80 },
      left: { thumb: 75, index: 0, middle: 80, ring: 80, pinky: 80 }
    }
  },
  L: {
    letter: 'L',
    type: 'CONSONANT',
    description: 'Dominant hand forms L-shape resting upright upon open non-dominant palm',
    duration_ms: 600,
    dominant_hand: 'both',
    rotations: { right_wrist: { x: -10, y: 12, z: -8 }, left_wrist: { x: 10, y: -12, z: 8 } },
    finger_curls: {
      right: { thumb: 0, index: 0, middle: 85, ring: 85, pinky: 85 },
      left: { thumb: 0, index: 0, middle: 0, ring: 0, pinky: 0 }
    }
  },
  M: {
    letter: 'M',
    type: 'CONSONANT',
    description: 'Dominant index, middle, and ring fingers rest across non-dominant palm',
    duration_ms: 650,
    dominant_hand: 'both',
    rotations: { right_wrist: { x: -12, y: 16, z: -10 }, left_wrist: { x: 10, y: -15, z: 10 } },
    finger_curls: {
      right: { thumb: 65, index: 15, middle: 15, ring: 15, pinky: 85 },
      left: { thumb: 0, index: 0, middle: 0, ring: 0, pinky: 0 }
    }
  },
  N: {
    letter: 'N',
    type: 'CONSONANT',
    description: 'Dominant index and middle fingers rest across non-dominant palm',
    duration_ms: 650,
    dominant_hand: 'both',
    rotations: { right_wrist: { x: -12, y: 16, z: -10 }, left_wrist: { x: 10, y: -15, z: 10 } },
    finger_curls: {
      right: { thumb: 65, index: 15, middle: 15, ring: 85, pinky: 85 },
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
    rotations: { right_wrist: { x: -16, y: 22, z: -16 }, left_wrist: { x: 10, y: -15, z: 10 } },
    finger_curls: {
      right: { thumb: 60, index: 0, middle: 75, ring: 75, pinky: 75 },
      left: { thumb: 0, index: 0, middle: 0, ring: 0, pinky: 0 }
    }
  },
  P: {
    letter: 'P',
    type: 'CONSONANT',
    description: 'Dominant thumb and index form circle touching extended upright left index finger tip',
    duration_ms: 650,
    dominant_hand: 'both',
    rotations: { right_wrist: { x: -10, y: 14, z: -8 }, left_wrist: { x: 5, y: -10, z: 5 } },
    finger_curls: {
      right: { thumb: 55, index: 55, middle: 85, ring: 85, pinky: 85 },
      left: { thumb: 80, index: 0, middle: 80, ring: 80, pinky: 80 }
    }
  },
  Q: {
    letter: 'Q',
    type: 'CONSONANT',
    description: 'Non-dominant hand forms O-circle; dominant index hooks downward through it',
    duration_ms: 650,
    dominant_hand: 'both',
    rotations: { right_wrist: { x: -14, y: 16, z: -10 }, left_wrist: { x: 10, y: -12, z: 8 } },
    finger_curls: {
      right: { thumb: 65, index: 45, middle: 80, ring: 80, pinky: 80 },
      left: { thumb: 50, index: 50, middle: 50, ring: 50, pinky: 50 }
    }
  },
  R: {
    letter: 'R',
    type: 'CONSONANT',
    description: 'Dominant crossed index and middle fingers rest upon open non-dominant palm',
    duration_ms: 650,
    dominant_hand: 'both',
    rotations: { right_wrist: { x: -12, y: 15, z: -10 }, left_wrist: { x: 10, y: -12, z: 8 } },
    finger_curls: {
      right: { thumb: 70, index: 10, middle: 10, ring: 85, pinky: 85 },
      left: { thumb: 0, index: 0, middle: 0, ring: 0, pinky: 0 }
    }
  },
  S: {
    letter: 'S',
    type: 'CONSONANT',
    description: 'Both pinky fingers hooked together at midline',
    duration_ms: 600,
    dominant_hand: 'both',
    rotations: { right_wrist: { x: -10, y: 14, z: -8 }, left_wrist: { x: 10, y: -14, z: 8 } },
    finger_curls: {
      right: { thumb: 75, index: 80, middle: 80, ring: 80, pinky: 40 },
      left: { thumb: 75, index: 80, middle: 80, ring: 80, pinky: 40 }
    }
  },
  T: {
    letter: 'T',
    type: 'CONSONANT',
    description: 'Dominant index finger touches the outer edge of open non-dominant hand perpendicularly',
    duration_ms: 600,
    dominant_hand: 'both',
    rotations: { right_wrist: { x: -12, y: 15, z: -10 }, left_wrist: { x: 8, y: -10, z: 6 } },
    finger_curls: {
      right: { thumb: 65, index: 0, middle: 80, ring: 80, pinky: 80 },
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
    rotations: { right_wrist: { x: -18, y: 24, z: -18 }, left_wrist: { x: 10, y: -15, z: 10 } },
    finger_curls: {
      right: { thumb: 60, index: 0, middle: 75, ring: 75, pinky: 75 },
      left: { thumb: 0, index: 0, middle: 0, ring: 0, pinky: 0 }
    }
  },
  V: {
    letter: 'V',
    type: 'CONSONANT',
    description: 'Dominant V-handshape (index + middle upright spread) rests on non-dominant palm',
    duration_ms: 600,
    dominant_hand: 'both',
    rotations: { right_wrist: { x: -10, y: 14, z: -8 }, left_wrist: { x: 10, y: -12, z: 8 } },
    finger_curls: {
      right: { thumb: 75, index: 0, middle: 0, ring: 85, pinky: 85 },
      left: { thumb: 0, index: 0, middle: 0, ring: 0, pinky: 0 }
    }
  },
  W: {
    letter: 'W',
    type: 'CONSONANT',
    description: 'Both hands form W-handshapes interlocking fingers at midline',
    duration_ms: 650,
    dominant_hand: 'both',
    rotations: { right_wrist: { x: -12, y: 14, z: -8 }, left_wrist: { x: 12, y: -14, z: 8 } },
    finger_curls: {
      right: { thumb: 70, index: 0, middle: 0, ring: 0, pinky: 85 },
      left: { thumb: 70, index: 0, middle: 0, ring: 0, pinky: 85 }
    }
  },
  X: {
    letter: 'X',
    type: 'CONSONANT',
    description: 'Both extended index fingers crossed over each other forming an X',
    duration_ms: 600,
    dominant_hand: 'both',
    rotations: { right_wrist: { x: -10, y: 12, z: -8 }, left_wrist: { x: 10, y: -12, z: 8 } },
    finger_curls: {
      right: { thumb: 70, index: 0, middle: 80, ring: 80, pinky: 80 },
      left: { thumb: 70, index: 0, middle: 80, ring: 80, pinky: 80 }
    }
  },
  Y: {
    letter: 'Y',
    type: 'CONSONANT',
    description: 'Dominant thumb and index form V-notch resting on upright non-dominant index',
    duration_ms: 650,
    dominant_hand: 'both',
    rotations: { right_wrist: { x: -12, y: 15, z: -10 }, left_wrist: { x: 5, y: -10, z: 5 } },
    finger_curls: {
      right: { thumb: 0, index: 0, middle: 85, ring: 85, pinky: 85 },
      left: { thumb: 80, index: 0, middle: 80, ring: 80, pinky: 80 }
    }
  },
  Z: {
    letter: 'Z',
    type: 'CONSONANT',
    description: 'Dominant index finger draws a Z trajectory across open non-dominant palm',
    duration_ms: 700,
    dominant_hand: 'both',
    rotations: { right_wrist: { x: -14, y: 16, z: -10 }, left_wrist: { x: 10, y: -12, z: 8 } },
    finger_curls: {
      right: { thumb: 65, index: 0, middle: 80, ring: 80, pinky: 80 },
      left: { thumb: 0, index: 0, middle: 0, ring: 0, pinky: 0 }
    }
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
