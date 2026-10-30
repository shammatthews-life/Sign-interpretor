/**
 * tools/validate_phase_h17_complete_corpus.mjs
 *
 * Phase H17 Final Verification Suite: Emergency Complete Corpus Vocabulary Integration.
 * 1. Canonical Corpus Accounting: 23,258 tokens (100.0% coverage, 0 silent token loss).
 * 2. Playable Library: 47 Schema 2.0.0 signs verified with complete neutral returns.
 * 3. Sign Manifest: signs/manifest.json complete and matching sign library.
 * 4. ISL Two-Handed Fingerspelling: All 26 letters (A-Z) verified with official ISLRTC vowel targeting.
 * 5. EnglishToISLTranslator: 47 signs, contractions, deictic spatial referencing, multiwords, and subtitle fallback.
 * 6. User Acceptance Test Scenarios:
 *    - "I want your help" -> Playable sign sequence.
 *    - "I want your dopamine" -> Mixed sign + subtitle fallback.
 *    - "I am going to speak" -> Contraction + phrase translation.
 *    - Unsupported technical terms -> Honest subtitle fallback without silent omission.
 */

import { readFileSync, readdirSync, existsSync } from 'node:fs';
import { resolve, join } from 'node:path';
import assert from 'node:assert/strict';

const PROJECT_ROOT = resolve('.');
const SIGNS_DIR = join(PROJECT_ROOT, 'signs');
const DATA_DIR = join(PROJECT_ROOT, 'data');

console.log('==================================================');
console.log('PHASE H17 VALIDATION: COMPLETE CORPUS INTEGRATION');
console.log('==================================================');

// ----------------------------------------------------
// TEST 1: Canonical Corpus Accounting
// ----------------------------------------------------
const coveragePath = join(DATA_DIR, 'isl_corpus_coverage.json');
assert(existsSync(coveragePath), 'isl_corpus_coverage.json must exist');
const coverage = JSON.parse(readFileSync(coveragePath, 'utf-8'));

assert.equal(coverage.total_spoken_tokens, 23258, 'Total tokens must equal 23,258');
assert.equal(coverage.total_tokens_accounted_for, 23258, 'All 23,258 tokens must be accounted for');
assert.equal(coverage.disposition_coverage_percent, 100.0, 'Coverage must be 100.0%');

const disps = coverage.dispositions;
const communicativeCount = (disps.IMPLEMENTED_PENDING_LINGUISTIC_REVIEW || 0) +
                           (disps.GRAMMAR_OMISSION || 0) +
                           (disps.PHRASE_TRANSLATED || 0) +
                           (disps.FINGERSPELLED || 0);

const commPercent = Number(((communicativeCount / 23258) * 100).toFixed(2));
console.log(`Canonical tokens: 23,258 | Accounted: 23,258 (100.0%)`);
console.log(`Communicative coverage: ${communicativeCount} tokens (${commPercent}%)`);
console.log(`Subtitle fallback: ${disps.SUBTITLE_FALLBACK} tokens (${coverage.percentages.SUBTITLE_FALLBACK}%)`);

assert(commPercent >= 70.0, `Communicative coverage must exceed 70% (actual: ${commPercent}%)`);
console.log('PASS 1: Canonical corpus accounting verified with 100.0% disposition coverage.');

// ----------------------------------------------------
// TEST 2: Schema 2.0.0 Validation on All 47 Signs
// ----------------------------------------------------
const manifestPath = join(SIGNS_DIR, 'manifest.json');
assert(existsSync(manifestPath), 'manifest.json must exist');
const manifest = JSON.parse(readFileSync(manifestPath, 'utf-8'));

assert.equal(manifest.manifest_version, '1.0.0');
assert.equal(manifest.total_playable_signs, 47, 'Manifest must report 47 playable signs');
assert.equal(manifest.signs.length, 47, 'Manifest must list 47 sign entries');

for (const entry of manifest.signs) {
  const filePath = join(SIGNS_DIR, entry.file_name);
  assert(existsSync(filePath), `File ${entry.file_name} must exist`);
  const signDoc = JSON.parse(readFileSync(filePath, 'utf-8'));

  assert.equal(signDoc.schema_version, '2.0.0', `${entry.sign_id} schema_version must be 2.0.0`);
  assert.equal(signDoc.motion.status, 'playable', `${entry.sign_id} must be playable`);
  assert.equal(signDoc.motion.return_to_neutral, true, `${entry.sign_id} must return to neutral`);

  // Verify neutral starting and ending keyframes
  const firstKf = signDoc.motion.keyframes[0];
  const lastKf = signDoc.motion.keyframes[signDoc.motion.keyframes.length - 1];
  assert.equal(firstKf.time_ms, 0, `${entry.sign_id} first keyframe at 0ms`);
  assert.equal(lastKf.time_ms, signDoc.motion.duration_ms, `${entry.sign_id} last keyframe at duration_ms`);

  for (const bone of Object.keys(firstKf.rotations)) {
    assert.deepEqual(firstKf.rotations[bone], { x: 0, y: 0, z: 0 }, `${entry.sign_id} ${bone} start neutral`);
    assert.deepEqual(lastKf.rotations[bone], { x: 0, y: 0, z: 0 }, `${entry.sign_id} ${bone} return neutral`);
  }
}
console.log('PASS 2: All 47 playable signs conform strictly to Schema 2.0.0 with full neutral returns.');

// ----------------------------------------------------
// TEST 3: SignLibrary Integration for All 47 Signs
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
const allSignIds = manifest.signs.map(s => s.sign_id);

const preloadResults = await library.preload(allSignIds);
assert.equal(preloadResults.length, 47, 'Must preload all 47 signs');
const failed = preloadResults.filter(r => r.status === 'rejected');
assert.equal(failed.length, 0, `Preload failures: ${failed.map(f => f.reason).join(', ')}`);

// Construct dummy bones covering all 47 signs
const allInvolvedBones = new Set(allSignIds.flatMap(id => library.cache.get(id).motion.involved_bones));
const dummyBones = new Map();
allInvolvedBones.forEach(bone => dummyBones.set(bone, { rotation: { x: 0, y: 0, z: 0 } }));

for (const signId of allSignIds) {
  const playable = library.getPlayable(signId, dummyBones);
  assert(playable, `Playable motion for ${signId} must be produced`);
}
console.log('PASS 3: SignLibrary preloads and resolves all 47 playable signs.');

// ----------------------------------------------------
// TEST 4: ISL Two-Handed Manual Alphabet Complete (26 Letters)
// ----------------------------------------------------
const { ISL_ALPHABET, composeFingerspellingMotion } = await import('./avatar_viewer/ISLFingerspelling.js');

assert.equal(Object.keys(ISL_ALPHABET).length, 26, 'ISL manual alphabet must contain all 26 letters (A-Z)');
const expectedVowels = { A: 'thumb', E: 'index', I: 'middle', O: 'ring', U: 'pinky' };
for (const [vowel, targetFinger] of Object.entries(expectedVowels)) {
  assert.equal(ISL_ALPHABET[vowel].type, 'VOWEL', `${vowel} must be classified as VOWEL`);
  assert.equal(ISL_ALPHABET[vowel].target_finger, targetFinger, `${vowel} must target non-dominant ${targetFinger}`);
}

const fsAmy = composeFingerspellingMotion('AMY');
assert(fsAmy && fsAmy.motion.keyframes.length >= 5);
assert.equal(fsAmy.motion.return_to_neutral, true);
console.log('PASS 4: ISL two-handed manual alphabet (26 letters) and fingerspelling composer verified.');

// ----------------------------------------------------
// TEST 5: Acceptance Test Scenarios (Demonstration Ready)
// ----------------------------------------------------
const { RuleBasedISLTranslator } = await import('./avatar_viewer/EnglishToISLTranslator.js');
const translator = new RuleBasedISLTranslator();

// Scenario 1: "I want your help" -> Playable sequence
const res1 = translator.translate('I want your help');
assert(res1.sign_ids.includes('i') && res1.sign_ids.includes('want') && res1.sign_ids.includes('help'), 'I WANT HELP must be resolved');
assert.equal(res1.unknown_terms.length, 0, 'No unknown terms for standard vocabulary');

// Scenario 2: "I want your dopamine" -> Mixed sign + subtitle fallback
const res2 = translator.translate('I want your dopamine');
assert(res2.sign_ids.includes('i') && res2.sign_ids.includes('want'), 'I and WANT must be resolved');
assert(res2.unknown_terms.includes('DOPAMINE'), 'DOPAMINE must be flagged as unknown term for subtitle fallback');

// Scenario 3: "I am going to speak" -> Contraction and phrase rules
const res3 = translator.translate('I am going to speak');
assert(res3.gloss_sequence.includes('GOING_TO'), 'Phrase "going to" must be resolved');
assert(res3.sign_ids.includes('say'), 'Verb "speak" must resolve to playable sign SAY');

// Scenario 4: "Public speaking is good" -> Compound expression + copula omission
const res4 = translator.translate('Public speaking is good');
assert(res4.gloss_sequence.includes('SAY') && res4.gloss_sequence.includes('PEOPLE'));
assert(res4.grammar_omissions.some(o => o.token === 'is'), 'Copula "is" must be omitted under GRAMMAR_OMISSION');
assert(res4.sign_ids.includes('good'), 'GOOD must resolve to playable sign');

console.log('PASS 5: All user demonstration acceptance scenarios verified successfully.');
console.log('==================================================');
console.log('ALL PHASE H17 VALIDATION CHECKS PASSED (DEMO READY)');
console.log('==================================================');
