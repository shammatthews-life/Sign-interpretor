/**
 * tools/validate_phase_h16_bulk_expansion.mjs
 *
 * Phase H16 Verification Suite:
 * 1. Corpus-wide resolution verification (>5,000 unaddressed occurrences transitioned).
 * 2. 100.0% Token disposition accounting (0 silent token loss).
 * 3. Batch 4 Schema 2.0.0 validation (15 newly authored motions).
 * 4. SignLibrary preloading and resolution of 37 playable signs.
 * 5. EnglishToISLTranslator integration with Batch 4 signs, contractions, and multiword phrases.
 */

import { readFileSync, readdirSync, existsSync } from 'node:fs';
import { resolve, join } from 'node:path';
import assert from 'node:assert/strict';

const PROJECT_ROOT = resolve('.');
const SIGNS_DIR = join(PROJECT_ROOT, 'signs');
const DATA_DIR = join(PROJECT_ROOT, 'data');

console.log('==================================================');
console.log('PHASE H16 VALIDATION: BULK EXPANSION & INTEGRATION');
console.log('==================================================');

// ----------------------------------------------------
// TEST 1: Canonical Corpus Accounting & >5,000 Occurrences Resolved
// ----------------------------------------------------
const coveragePath = join(DATA_DIR, 'isl_corpus_coverage.json');
assert(existsSync(coveragePath), 'isl_corpus_coverage.json must exist');
const coverage = JSON.parse(readFileSync(coveragePath, 'utf-8'));

assert.equal(coverage.total_spoken_tokens, 23258, 'Total tokens must equal 23,258');
assert.equal(coverage.total_tokens_accounted_for, 23258, 'All 23,258 tokens must be accounted for');
assert.equal(coverage.disposition_coverage_percent, 100.0, 'Coverage must be 100.0%');

const h15Unaddressed = 11991; // 11,227 subtitle fallback + 764 motion pending in H15
const h16SubtitleFallback = coverage.dispositions.SUBTITLE_FALLBACK;
const h16MotionPending = coverage.dispositions.DICTIONARY_REFERENCE_AVAILABLE_BUT_MOTION_PENDING || 0;
const h16Unaddressed = h16SubtitleFallback + h16MotionPending;
const occurrencesResolved = h15Unaddressed - h16Unaddressed;

console.log(`Phase H15 unaddressed pool: ${h15Unaddressed}`);
console.log(`Phase H16 unaddressed pool: ${h16Unaddressed} (Fallback: ${h16SubtitleFallback}, Pending: ${h16MotionPending})`);
console.log(`Total occurrences resolved in Phase H16: ${occurrencesResolved}`);
assert(occurrencesResolved >= 5000, `Must resolve at least 5,000 occurrences (actual: ${occurrencesResolved})`);

console.log(`PASS 1: Canonical corpus accounting verified: ${occurrencesResolved} occurrences resolved (target >= 5,000), 100.0% coverage.`);

// ----------------------------------------------------
// TEST 2: Batch 4 Signs Conformance to Schema 2.0.0
// ----------------------------------------------------
const BATCH_4_SIGNS = [
  'like', 'can', 'know', 'think', 'say', 'time', 'give', 'we', 'they',
  'will', 'two', 'yes', 'no', 'come', 'learn'
];

for (const signId of BATCH_4_SIGNS) {
  const filePath = join(SIGNS_DIR, `${signId}.json`);
  assert(existsSync(filePath), `Sign file ${signId}.json must exist`);
  const signDoc = JSON.parse(readFileSync(filePath, 'utf-8'));

  assert.equal(signDoc.schema_version, '2.0.0', `${signId} schema_version must be 2.0.0`);
  assert.equal(signDoc.sign_id, signId, `${signId} sign_id mismatch`);
  assert.equal(signDoc.metadata.language, 'ISL', `${signId} language must be ISL`);
  assert.equal(signDoc.metadata.validation_status, 'IMPLEMENTATION_PENDING_LINGUISTIC_REVIEW', `${signId} validation_status must be unreviewed`);
  assert.equal(signDoc.motion.status, 'playable', `${signId} motion.status must be playable`);
  assert.equal(signDoc.motion.return_to_neutral, true, `${signId} return_to_neutral must be true`);
  assert(signDoc.motion.duration_ms >= 800 && signDoc.motion.duration_ms <= 2000, `${signId} duration_ms within limits`);
  assert(signDoc.motion.involved_bones.length >= 4, `${signId} involved_bones must cover arm and head`);
  assert(signDoc.motion.keyframes.length >= 4, `${signId} must contain at least 4 keyframes`);

  // Verify neutral starting and ending keyframes
  const firstKf = signDoc.motion.keyframes[0];
  const lastKf = signDoc.motion.keyframes[signDoc.motion.keyframes.length - 1];
  assert.equal(firstKf.time_ms, 0, `${signId} first keyframe at 0ms`);
  assert.equal(lastKf.time_ms, signDoc.motion.duration_ms, `${signId} last keyframe at duration_ms`);

  for (const bone of signDoc.motion.involved_bones) {
    assert.deepEqual(firstKf.rotations[bone], { x: 0, y: 0, z: 0 }, `${signId} ${bone} start neutral`);
    assert.deepEqual(lastKf.rotations[bone], { x: 0, y: 0, z: 0 }, `${signId} ${bone} return neutral`);
  }
}
console.log(`PASS 2: All 15 Batch 4 signs conform strictly to Schema 2.0.0 with full neutral returns.`);

// ----------------------------------------------------
// TEST 3: SignLibrary Preloading and 37 Playable Signs
// ----------------------------------------------------
const { SignLibrary } = await import('./avatar_viewer/SignLibrary.js');

const mockFetch = async (url) => {
  const match = url.match(/\/signs\/([^/]+)\.json$/);
  if (!match) return { ok: false, status: 404 };
  const signId = match[1];
  const filePath = join(SIGNS_DIR, `${signId}.json`);
  if (!existsSync(filePath)) return { ok: false, status: 404 };
  const content = JSON.parse(readFileSync(filePath, 'utf-8'));
  return { ok: true, json: async () => content };
};

const library = new SignLibrary({ fetchImpl: mockFetch });

const all37Signs = [
  'hello', 'good', 'morning', 'water', 'you', 'i', 'what', 'not', 'how',
  'your', 'my', 'have', 'want', 'look', 'see', 'go', 'do', 'people', 'one',
  'when', 'now', 'more',
  'like', 'can', 'know', 'think', 'say', 'time', 'give', 'we', 'they',
  'will', 'two', 'yes', 'no', 'come', 'learn'
];

const preloadResults = await library.preload(all37Signs);
assert.equal(preloadResults.length, 37, 'Preload must attempt all 37 signs');
const failed = preloadResults.filter(r => r.status === 'rejected');
assert.equal(failed.length, 0, `Preload had failures: ${failed.map(f => f.reason).join(', ')}`);

// Construct dummy bones map covering all involved bones
const dummyBones = new Map();
const allBones = new Set(all37Signs.flatMap(id => library.cache.get(id).motion.involved_bones));
allBones.forEach(bone => dummyBones.set(bone, { rotation: { x: 0, y: 0, z: 0 } }));

for (const signId of all37Signs) {
  const playable = library.getPlayable(signId, dummyBones);
  assert(playable, `Playable motion for ${signId} must be produced`);
  const status = library.cache.get(signId).metadata.validation_status;
  assert(['IMPLEMENTATION_PENDING_LINGUISTIC_REVIEW', 'TECHNICALLY_PLAYABLE'].includes(status), `${signId} status must be uncertified / pending review`);
}
console.log('PASS 3: SignLibrary preloads and resolves all 37 playable signs in the expanded library.');

// ----------------------------------------------------
// TEST 4: EnglishToISLTranslator Integration & Contractions
// ----------------------------------------------------
const { RuleBasedISLTranslator } = await import('./avatar_viewer/EnglishToISLTranslator.js');
const translator = new RuleBasedISLTranslator();

// Test Batch 4 single signs
const resLike = translator.translate('I like you');
assert(resLike.sign_ids.includes('like'), 'Sign LIKE must be resolved in sign_ids');

const resKnow = translator.translate('We know them');
assert(resKnow.sign_ids.includes('we') && resKnow.sign_ids.includes('know') && resKnow.sign_ids.includes('they'), 'WE, KNOW, and THEY must be resolved');

const resThink = translator.translate('They think now');
assert(resThink.sign_ids.includes('they') && resThink.sign_ids.includes('think') && resThink.sign_ids.includes('now'));

const resTime = translator.translate('Give more time');
assert(resTime.sign_ids.includes('give') && resTime.sign_ids.includes('more') && resTime.sign_ids.includes('time'));

const resLearn = translator.translate('You will learn two');
assert(resLearn.sign_ids.includes('you') && resLearn.sign_ids.includes('learn') && resLearn.sign_ids.includes('two'));
assert(resLearn.grammar_omissions.some(o => o.token === 'will'), 'Future auxiliary "will" naturally omitted under GRAMMAR_OMISSION');

// Test Contraction Expansion
const resContraction = translator.translate("I'm gonna learn more");
assert(resContraction.sign_ids.includes('i') && resContraction.sign_ids.includes('go') && resContraction.sign_ids.includes('learn'));

const resDont = translator.translate("Don't go now");
assert(resDont.sign_ids.includes('not') && resDont.sign_ids.includes('go') && resDont.sign_ids.includes('now'));

// Test Multiword Phrase
const resPubSpeak = translator.translate('Public speaking is good');
assert(resPubSpeak.gloss_sequence.includes('SAY') && resPubSpeak.gloss_sequence.includes('PEOPLE'));
assert(resPubSpeak.grammar_omissions.some(o => o.token === 'is'), 'Copula "is" must be omitted under GRAMMAR_OMISSION');

console.log('PASS 4: EnglishToISLTranslator resolves Batch 4 signs, contractions, and multiword phrases.');

console.log('==================================================');
console.log('ALL PHASE H16 VALIDATION CHECKS PASSED');
console.log('==================================================');
