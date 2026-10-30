/**
 * Phase H15 Validation Suite:
 * Corpus-Wide ISL Dictionary Research, Lexicon Mapping & Batch 3 Expansion
 */
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');

const { SignLibrary } = await import('./avatar_viewer/SignLibrary.js');
const { RuleBasedISLTranslator } = await import('./avatar_viewer/EnglishToISLTranslator.js');
const { ISL_ALPHABET, composeFingerspellingMotion } = await import('./avatar_viewer/ISLFingerspelling.js');

console.log('==================================================');
console.log('PHASE H15 VALIDATION: CORPUS LEXICON & EXPANSION');
console.log('==================================================');

// ----------------------------------------------------
// TEST 1: Canonical Corpus Lexicon & 100% Accounting
// ----------------------------------------------------
const lexiconPath = path.join(root, 'data/isl_corpus_lexicon.json');
const coveragePath = path.join(root, 'data/isl_corpus_coverage.json');
const csvPath = path.join(root, 'data/isl_corpus_lexicon.csv');

assert(fs.existsSync(lexiconPath), 'data/isl_corpus_lexicon.json must exist');
assert(fs.existsSync(coveragePath), 'data/isl_corpus_coverage.json must exist');
assert(fs.existsSync(csvPath), 'data/isl_corpus_lexicon.csv must exist');

const lexicon = JSON.parse(fs.readFileSync(lexiconPath, 'utf8'));
const coverage = JSON.parse(fs.readFileSync(coveragePath, 'utf8'));

assert(Array.isArray(lexicon) && lexicon.length > 2000, 'Lexicon must record all unique corpus concepts (>2000)');
assert.equal(coverage.total_spoken_tokens, 23258, 'Total tokens must match canonical transcript (23,258)');
assert.equal(coverage.total_tokens_accounted_for, 23258, 'Every token must receive an explicit disposition (100%)');
assert.equal(coverage.disposition_coverage_percent, 100.0, 'Coverage percentage must be exactly 100%');

// Check required fields per concept record
const sample = lexicon[0];
for (const field of ['concept_id', 'lemma', 'surface_forms', 'frequency', 'semantic_category', 'translation_strategy', 'motion_status']) {
  assert(field in sample, `Lexicon record missing required field: ${field}`);
}
console.log(`PASS 1: Canonical corpus accounting verified: 23,258 tokens (100.0%) across ${lexicon.length} unique concepts.`);

// ----------------------------------------------------
// TEST 2: Batch 3 ISL Signs Conform to Schema 2.0.0
// ----------------------------------------------------
const batch3Signs = ['go', 'do', 'people', 'one', 'when', 'now', 'more'];

for (const signId of batch3Signs) {
  const filePath = path.join(root, 'signs', `${signId}.json`);
  assert(fs.existsSync(filePath), `Batch 3 file missing: ${filePath}`);
  const data = JSON.parse(fs.readFileSync(filePath, 'utf8'));

  assert.equal(data.schema_version, '2.0.0', `${signId} must be schema 2.0.0`);
  assert.equal(data.sign_id, signId, `${signId} sign_id mismatch`);
  assert.equal(data.metadata.language, 'ISL', `${signId} language must be ISL`);
  assert.equal(data.metadata.validation_status, 'IMPLEMENTATION_PENDING_LINGUISTIC_REVIEW');
  assert(data.metadata.source?.organization === 'ISLRTC', `${signId} must cite ISLRTC`);

  assert.equal(data.motion.status, 'playable');
  assert(data.motion.duration_ms >= 1000 && data.motion.duration_ms <= 1600);
  assert(data.motion.keyframes.length >= 4);

  // Check neutral return
  assert.equal(data.motion.keyframes[0].time_ms, 0);
  assert.equal(data.motion.keyframes.at(-1).time_ms, data.motion.duration_ms);
  const endRot = data.motion.keyframes.at(-1).rotations;
  for (const [bone, rot] of Object.entries(endRot)) {
    assert(rot.x === 0 && rot.y === 0 && rot.z === 0, `${signId}: terminal keyframe bone ${bone} must reset to 0,0,0`);
  }
}
console.log('PASS 2: All Batch 3 signs (GO, DO, PEOPLE, ONE, WHEN, NOW, MORE) conform to Schema 2.0.0.');

// ----------------------------------------------------
// TEST 3: Preload & Playable Retrieval for All 22 Signs
// ----------------------------------------------------
const all22Signs = [
  'hello', 'good', 'morning', 'water', 'you', 'i', 'what', 'not', 'how',
  'your', 'my', 'have', 'want', 'look', 'see',
  ...batch3Signs
];

const signLibrary = new SignLibrary({
  basePath: path.join(root, 'signs'),
  fetchImpl: async (url) => {
    const filename = path.basename(url);
    const filepath = path.join(root, 'signs', filename);
    if (!fs.existsSync(filepath)) return { ok: false, status: 404 };
    const content = JSON.parse(fs.readFileSync(filepath, 'utf8'));
    return { ok: true, json: async () => content };
  }
});

const preloadResults = await signLibrary.preload(all22Signs);
assert.equal(preloadResults.length, 22);
assert(preloadResults.every(r => r.status === 'fulfilled'), 'All 22 signs must preload successfully');

const allBones = new Set(all22Signs.flatMap(id => signLibrary.cache.get(id).motion.involved_bones));
const dummyBones = new Map([...allBones].map(name => [name, {}]));

for (const signId of all22Signs) {
  const playable = signLibrary.getPlayable(signId, dummyBones);
  assert.equal(playable.status, 'playable');
  assert.equal(playable.sign_id, signId);
}
console.log('PASS 3: SignLibrary preloads and resolves all 22 signs in the expanded library.');

// ----------------------------------------------------
// TEST 4: Two-Handed ISL Fingerspelling Engine
// ----------------------------------------------------
assert(ISL_ALPHABET.A && ISL_ALPHABET.E && ISL_ALPHABET.I && ISL_ALPHABET.O && ISL_ALPHABET.U,
  'All 5 vowels must be defined in ISL manual alphabet');
assert.equal(ISL_ALPHABET.A.target_finger, 'thumb');
assert.equal(ISL_ALPHABET.E.target_finger, 'index');
assert.equal(ISL_ALPHABET.I.target_finger, 'middle');
assert.equal(ISL_ALPHABET.O.target_finger, 'ring');
assert.equal(ISL_ALPHABET.U.target_finger, 'pinky');

const fsMotion = composeFingerspellingMotion('DOPAMINE');
assert(fsMotion, 'composeFingerspellingMotion must generate a motion sequence for DOPAMINE');
assert.equal(fsMotion.schema_version, '2.0.0');
assert.equal(fsMotion.motion.status, 'playable');
assert.equal(fsMotion.motion.dominant_hand, 'both');
assert(fsMotion.motion.keyframes.length >= 10);
console.log('PASS 4: ISL two-handed manual alphabet and fingerspelling composer verified.');

// ----------------------------------------------------
// TEST 5: EnglishToISLTranslator Integration & Phrase Handling
// ----------------------------------------------------
const translator = new RuleBasedISLTranslator();

// Test Batch 3 single signs
const resGo = translator.translate('Now people go');
assert.deepEqual(resGo.sign_ids, ['now', 'people', 'go']);

const resDo = translator.translate('People do more');
assert(resDo.sign_ids.includes('people') && resDo.sign_ids.includes('do') && resDo.sign_ids.includes('more'));

const resOne = translator.translate('When you have more than one');
assert(resOne.sign_ids.includes('when') && resOne.sign_ids.includes('one') && resOne.sign_ids.includes('more'));

// Test Multiword phrase recognition
const resPhrase = translator.translate('I am going to look at the morning');
assert(resPhrase.gloss_sequence.includes('GOING_TO'), 'Multiword expression "going to" must be resolved');
assert(resPhrase.gloss_sequence.includes('LOOK'), '"look at" must resolve to LOOK');
assert(resPhrase.grammar_omissions.some(o => o.token === 'the'), 'Function word "the" must be omitted under GRAMMAR_OMISSION');

console.log('PASS 5: EnglishToISLTranslator resolves Batch 3 signs and multiword grammatical phrases.');
console.log('==================================================');
console.log('ALL PHASE H15 VALIDATION CHECKS PASSED');
console.log('==================================================');
