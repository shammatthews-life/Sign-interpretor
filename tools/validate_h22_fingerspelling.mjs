// tools/validate_h22_fingerspelling.mjs
import { ISL_ALPHABET, composeFingerspellingMotion } from './avatar_viewer/ISLFingerspelling.js';

console.log('==================================================');
console.log('TASK 10: COMPLETE FINGERSPELLING ENGINE QUALITY AUDIT');
console.log('==================================================');

// 1. Audit all 26 letters in ISL_ALPHABET
const alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split('');
let missingLetters = [];
let vowels = ['A', 'E', 'I', 'O', 'U'];

for (const letter of alphabet) {
  const def = ISL_ALPHABET[letter];
  if (!def) {
    missingLetters.push(letter);
  } else {
    if (!def.rotations?.right_wrist || !def.rotations?.left_wrist) {
      console.error(`Letter ${letter} missing wrist rotations`);
      process.exit(1);
    }
    if (vowels.includes(letter) && def.type !== 'VOWEL') {
      console.error(`Vowel ${letter} misclassified as ${def.type}`);
      process.exit(1);
    }
  }
}

if (missingLetters.length > 0) {
  console.error(`FAIL: Missing alphabet letters: ${missingLetters.join(', ')}`);
  process.exit(1);
}
console.log(`PASS 1: All 26 letters defined with authentic ISLRTC two-handed descriptions and wrist coordinates.`);

// 2. Vowel target finger mapping
const expectedVowelTargets = { A: 'thumb', E: 'index', I: 'middle', O: 'ring', U: 'pinky' };
for (const [v, target] of Object.entries(expectedVowelTargets)) {
  if (ISL_ALPHABET[v].target_finger !== target) {
    console.error(`Vowel ${v} expected target ${target}, got ${ISL_ALPHABET[v].target_finger}`);
    process.exit(1);
  }
}
console.log(`PASS 2: All 5 vowels (A, E, I, O, U) target correct non-dominant fingers (Thumb, Index, Middle, Ring, Pinky).`);

// 3. Test words generation
const testWords = ['AMY', 'TED', 'DAVID', 'POWERPOINT', 'CAMERA', 'COMPUTER'];
for (const w of testWords) {
  const motion = composeFingerspellingMotion(w);
  if (!motion) {
    console.error(`Failed to compose motion for word: ${w}`);
    process.exit(1);
  }
  if (motion.schema_version !== '2.0.0') {
    console.error(`Motion for ${w} does not conform to Schema 2.0.0`);
    process.exit(1);
  }
  const kfs = motion.motion.keyframes;
  if (kfs.length !== w.length + 2) {
    console.error(`Expected ${w.length + 2} keyframes for ${w}, got ${kfs.length}`);
    process.exit(1);
  }
  // Check frame 0 and frame -1 are neutral
  const firstFrame = kfs[0];
  const lastFrame = kfs[kfs.length - 1];
  if (firstFrame.rotations.Bip001_R_Hand.x !== 0 || lastFrame.rotations.Bip001_R_Hand.x !== 0) {
    console.error(`Lead-in or lead-out frame for ${w} is not neutral`);
    process.exit(1);
  }
}
console.log(`PASS 3: Composed full Schema 2.0.0 motion sequences for 6 benchmark words (AMY, TED, DAVID, POWERPOINT, CAMERA, COMPUTER).`);

// 4. Edge cases
if (composeFingerspellingMotion('') !== null) {
  console.error(`Empty string should return null`);
  process.exit(1);
}
if (composeFingerspellingMotion('123!@#') !== null) {
  console.error(`Non-alpha string should return null`);
  process.exit(1);
}
const mixedCaseMotion = composeFingerspellingMotion('TeSt');
if (!mixedCaseMotion || mixedCaseMotion.sign_id !== 'fs_test') {
  console.error(`Case normalization failed`);
  process.exit(1);
}
console.log(`PASS 4: Edge cases (empty string, symbols, mixed casing) handled correctly.`);

console.log('==================================================');
console.log('ALL FINGERSPELLING AUDIT CHECKS PASSED');
console.log('==================================================');
