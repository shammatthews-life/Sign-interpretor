/**
 * tools/validate_phase_h18_100_concept_expansion.mjs
 *
 * Phase H18 Verification Suite: 100-Concept High-Throughput ISL Vocabulary Expansion.
 * Verifies:
 * 1. Corpus Token Accounting: 23,258 tokens (100.0% accounted for, 0 silent loss).
 * 2. 147 Playable ISL Signs in Library (47 baseline + 100 Phase H18 expansion).
 * 3. Strict Schema 2.0.0 compliance and complete neutral return on all 147 signs.
 * 4. SignLibrary preloading and keyframe compilation across all 147 signs.
 * 5. EnglishToISLTranslator motion catalog, lexicon resolution, inflections, and fallback.
 * 6. Demonstration scenario validation for college mentor review.
 */

import { readFileSync, readdirSync, existsSync } from 'node:fs';
import { resolve, join } from 'node:path';
import assert from 'node:assert/strict';

const PROJECT_ROOT = resolve('.');
const SIGNS_DIR = join(PROJECT_ROOT, 'signs');
const DATA_DIR = join(PROJECT_ROOT, 'data');

console.log('==================================================');
console.log('PHASE H18 VALIDATION: 100-CONCEPT ISL EXPANSION');
console.log('==================================================');

// ----------------------------------------------------
// TEST 1: Corpus Accounting & Communicative Coverage
// ----------------------------------------------------
const coveragePath = join(DATA_DIR, 'isl_corpus_coverage.json');
assert(existsSync(coveragePath), 'isl_corpus_coverage.json must exist');
const coverage = JSON.parse(readFileSync(coveragePath, 'utf-8'));

assert.equal(coverage.total_spoken_tokens, 23258, 'Total tokens must equal 23,258');
assert.equal(coverage.total_tokens_accounted_for, 23258, 'All 23,258 tokens must be accounted for');
assert.equal(coverage.disposition_coverage_percent, 100.0, 'Coverage must be exactly 100.0%');

const disps = coverage.dispositions;
const communicativeCount = (disps.IMPLEMENTED_PENDING_LINGUISTIC_REVIEW || 0) +
                           (disps.GRAMMAR_OMISSION || 0) +
                           (disps.PHRASE_TRANSLATED || 0) +
                           (disps.FINGERSPELLED || 0);

const commPercent = Number(((communicativeCount / 23258) * 100).toFixed(2));
console.log(`Canonical tokens: 23,258 | Accounted: 23,258 (100.0%)`);
console.log(`Communicative coverage: ${communicativeCount} tokens (${commPercent}%)`);
console.log(`Implemented playable signs: ${disps.IMPLEMENTED_PENDING_LINGUISTIC_REVIEW} tokens (${coverage.percentages.IMPLEMENTED_PENDING_LINGUISTIC_REVIEW}%)`);
console.log(`Grammar omissions: ${disps.GRAMMAR_OMISSION} tokens (${coverage.percentages.GRAMMAR_OMISSION}%)`);
console.log(`Subtitle fallback: ${disps.SUBTITLE_FALLBACK} tokens (${coverage.percentages.SUBTITLE_FALLBACK}%)`);

assert(commPercent >= 75.0, `Communicative coverage must exceed 75% (actual: ${commPercent}%)`);
assert(disps.IMPLEMENTED_PENDING_LINGUISTIC_REVIEW >= 8000, 'Implemented sign occurrences must exceed 8,000');
console.log('PASS 1: Canonical corpus accounting verified with 100.0% disposition coverage.');

// ----------------------------------------------------
// TEST 2: Manifest & 147 Sign Asset Verification
// ----------------------------------------------------
const manifestPath = join(SIGNS_DIR, 'manifest.json');
assert(existsSync(manifestPath), 'manifest.json must exist');
const manifest = JSON.parse(readFileSync(manifestPath, 'utf-8'));

assert.equal(manifest.manifest_version, '1.0.0');
assert(manifest.total_playable_signs >= 147, 'Manifest must report at least 147 playable signs');
assert(manifest.signs.length >= 147, 'Manifest must contain at least 147 sign entries');

// Load H18 100 candidates to verify presence
const h18CandidatesPath = join(DATA_DIR, 'h18_batch_100_candidates.json');
assert(existsSync(h18CandidatesPath), 'h18_batch_100_candidates.json must exist');
const h18Candidates = JSON.parse(readFileSync(h18CandidatesPath, 'utf-8'));
assert.equal(h18Candidates.length, 100, 'Must have 100 candidate concepts');

const manifestSignIds = new Set(manifest.signs.map(s => s.sign_id));
for (const cand of h18Candidates) {
  assert(manifestSignIds.has(cand.canonical_concept), `Candidate ${cand.canonical_concept} must be in manifest`);
}

for (const entry of manifest.signs) {
  const filePath = join(SIGNS_DIR, entry.file_name);
  assert(existsSync(filePath), `File ${entry.file_name} must exist`);
  const signDoc = JSON.parse(readFileSync(filePath, 'utf-8'));

  assert.equal(signDoc.schema_version, '2.0.0', `${entry.sign_id} schema_version must be 2.0.0`);
  assert.equal(signDoc.motion.status, 'playable', `${entry.sign_id} must be playable`);
  assert.equal(signDoc.motion.return_to_neutral, true, `${entry.sign_id} must return to neutral`);
  assert(signDoc.motion.duration_ms >= 800 && signDoc.motion.duration_ms <= 2500, `${entry.sign_id} duration_ms reasonable`);

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
console.log('PASS 2: All 147 playable signs conform strictly to Schema 2.0.0 with full neutral returns.');

// ----------------------------------------------------
// TEST 3: SignLibrary Preload and Cache for All 147 Signs
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
assert(preloadResults.length >= 147, 'Must preload at least 147 signs');
const failed = preloadResults.filter(r => r.status === 'rejected');
assert.equal(failed.length, 0, `Preload failures: ${failed.map(f => f.reason).join(', ')}`);

// Construct dummy bones covering all 147 signs
const allInvolvedBones = new Set(allSignIds.flatMap(id => library.cache.get(id).motion.involved_bones));
const dummyBones = new Map();
allInvolvedBones.forEach(bone => dummyBones.set(bone, { rotation: { x: 0, y: 0, z: 0 } }));

for (const signId of allSignIds) {
  const playable = library.getPlayable(signId, dummyBones);
  assert(playable, `Playable motion for ${signId} must be produced`);
  assert(playable.keyframes.length >= 4, `${signId} must contain at least 4 keyframes`);
}
console.log('PASS 3: SignLibrary preloads and compiles all 147 playable signs without error.');

// ----------------------------------------------------
// TEST 4: EnglishToISLTranslator 147 Vocabulary Resolution
// ----------------------------------------------------
const { RuleBasedISLTranslator } = await import('./avatar_viewer/EnglishToISLTranslator.js');
const translator = new RuleBasedISLTranslator();

// Test that all 100 new concepts resolve directly to playable sign IDs
for (const cand of h18Candidates) {
  const concept = cand.canonical_concept;
  const res = translator.translate(concept);
  assert(res.sign_ids.includes(concept), `Concept "${concept}" must resolve to playable sign ID in translator`);
}

// Test inflection mappings
const inflectionChecks = [
  { text: 'skills', expectedSign: 'skill' },
  { text: 'walking', expectedSign: 'walk' },
  { text: 'questions', expectedSign: 'question' },
  { text: 'writes', expectedSign: 'write' },
  { text: 'teachers', expectedSign: 'teacher' },
  { text: 'understanding', expectedSign: 'understand' },
  { text: 'practices', expectedSign: 'practice' },
  { text: 'videos', expectedSign: 'video' }
];

for (const chk of inflectionChecks) {
  const res = translator.translate(chk.text);
  assert(res.sign_ids.includes(chk.expectedSign), `Inflection "${chk.text}" must resolve to "${chk.expectedSign}"`);
}
console.log('PASS 4: EnglishToISLTranslator resolves all 100 new concepts and inflection variants.');

// ----------------------------------------------------
// TEST 5: Demonstration Scenarios (Mentor Presentation Ready)
// ----------------------------------------------------

// Scenario 1: Complex lecture sentence from target video
const demo1 = translator.translate('The teacher will share an important lesson today');
assert(demo1.sign_ids.includes('teacher'), 'Must sign TEACHER');
assert(demo1.sign_ids.includes('share'), 'Must sign SHARE');
assert(demo1.sign_ids.includes('important'), 'Must sign IMPORTANT');
assert(demo1.sign_ids.includes('lesson'), 'Must sign LESSON');
assert(demo1.sign_ids.includes('today'), 'Must sign TODAY');
assert.equal(demo1.unknown_terms.length, 0, 'No unknown terms for demo sentence 1');

// Scenario 2: Two-handed and cognitive signs
const demo2 = translator.translate('Practice will make you confident on stage');
assert(demo2.sign_ids.includes('practice'), 'Must sign PRACTICE');
assert(demo2.sign_ids.includes('confident'), 'Must sign CONFIDENT');
assert(demo2.sign_ids.includes('stage'), 'Must sign STAGE');

// Scenario 3: Mixed sequence with subtitle fallback
const demo3 = translator.translate('I understand your question about quantum physics');
assert(demo3.sign_ids.includes('understand'), 'Must sign UNDERSTAND');
assert(demo3.sign_ids.includes('question'), 'Must sign QUESTION');
assert(demo3.unknown_terms.includes('QUANTUM'), 'Must flag QUANTUM for subtitle fallback');
assert(demo3.unknown_terms.includes('PHYSICS'), 'Must flag PHYSICS for subtitle fallback');

console.log('PASS 5: Demonstration scenarios verified with avatar motion and subtitle fallback.');
console.log('==================================================');
console.log('ALL PHASE H18 VALIDATION CHECKS PASSED (DEMO READY)');
console.log('==================================================');
