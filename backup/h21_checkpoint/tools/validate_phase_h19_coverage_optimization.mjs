/**
 * tools/validate_phase_h19_coverage_optimization.mjs
 *
 * Phase H19 Verification Suite: High-Throughput Coverage Optimization,
 * 250-Concept Processing & Demonstration Readiness.
 *
 * Validates:
 * 1. Corpus Token Accounting: 23,258 tokens (100.0% coverage, 0 silent token loss).
 * 2. 250 Concepts Processed across 5 balanced batch checkpoints.
 * 3. Mined Multiword Phrases (39 educational & discourse compounds).
 * 4. Sign Library Manifest: 167 Playable Schema 2.0.0 signs (147 existing + 20 new high-impact).
 * 5. Strict Schema 2.0.0 compliance & complete neutral return for all 167 signs.
 * 6. SignLibrary preloading and keyframe compilation across all 167 signs.
 * 7. YouTube Timeline Synchronizer: segment dispatch, pause/play, and seek recovery.
 * 8. EnglishToISLTranslator: phrase-first precedence, contractions, inflections, and subtitle fallback.
 * 9. Demonstration acceptance scenarios for college mentor review.
 */

import { readFileSync, existsSync } from 'node:fs';
import { resolve, join } from 'node:path';
import assert from 'node:assert/strict';

const PROJECT_ROOT = resolve('.');
const SIGNS_DIR = join(PROJECT_ROOT, 'signs');
const DATA_DIR = join(PROJECT_ROOT, 'data');
const EXTENSION_DIR = join(PROJECT_ROOT, 'extension');

console.log('====================================================');
console.log('PHASE H19 VALIDATION: HIGH-THROUGHPUT COVERAGE & SYNC');
console.log('====================================================');

// ----------------------------------------------------
// TEST 1: Corpus Token Accounting & Coverage Metrics
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
console.log(`Phrase translated tokens: ${disps.PHRASE_TRANSLATED} tokens (${coverage.percentages.PHRASE_TRANSLATED}%)`);
console.log(`Grammar omissions: ${disps.GRAMMAR_OMISSION} tokens (${coverage.percentages.GRAMMAR_OMISSION}%)`);
console.log(`Fingerspelled tokens: ${disps.FINGERSPELLED} tokens (${coverage.percentages.FINGERSPELLED}%)`);
console.log(`Subtitle fallback: ${disps.SUBTITLE_FALLBACK} tokens (${coverage.percentages.SUBTITLE_FALLBACK}%)`);

assert(commPercent >= 80.0, `Communicative coverage must exceed 80% (actual: ${commPercent}%)`);
assert(disps.SUBTITLE_FALLBACK <= 4000, 'Subtitle fallback must be reduced below 4,000 occurrences');
console.log('PASS 1: Canonical corpus accounting verified with 100.0% disposition coverage (0 silent loss).');

// ----------------------------------------------------
// TEST 2: 250-Concept Bulk Processing & 5 Checkpoints
// ----------------------------------------------------
const freqJsonPath = join(DATA_DIR, 'h19_remaining_fallback_frequency.json');
const freqCsvPath = join(DATA_DIR, 'h19_remaining_fallback_frequency.csv');
assert(existsSync(freqJsonPath) && existsSync(freqCsvPath), 'Fallback frequency reports must exist');

const processed250Path = join(DATA_DIR, 'h19_250_processed_concepts.json');
assert(existsSync(processed250Path), 'h19_250_processed_concepts.json must exist');
const processed250 = JSON.parse(readFileSync(processed250Path, 'utf-8'));
assert.equal(processed250.total_concepts_processed, 250, 'Must process exactly 250 concepts in bulk');

for (let b = 1; b <= 5; b++) {
  const ckptPath = join(DATA_DIR, `h19_batch${b}_checkpoint.json`);
  assert(existsSync(ckptPath), `Batch ${b} checkpoint must exist`);
  const ckpt = JSON.parse(readFileSync(ckptPath, 'utf-8'));
  assert.equal(ckpt.concepts_count, 50, `Batch ${b} must contain exactly 50 concepts`);
}
console.log('PASS 2: 250-concept processing and all 5 batch checkpoints verified.');

// ----------------------------------------------------
// TEST 3: Multiword Phrase Mining & Dictionaries
// ----------------------------------------------------
const phraseCsvPath = join(DATA_DIR, 'h19_phrase_frequency.csv');
const phraseDictPath = join(DATA_DIR, 'h19_phrase_dictionary.json');
const phraseEvidencePath = join(DATA_DIR, 'h19_phrase_evidence.json');

assert(existsSync(phraseCsvPath) && existsSync(phraseDictPath) && existsSync(phraseEvidencePath));
const phraseDict = JSON.parse(readFileSync(phraseDictPath, 'utf-8'));
assert(phraseDict.phrases.length >= 35, 'Must mine at least 35 repeated phrases');

const requiredPhrases = [
  'body language', 'facial expression', 'facial expressions',
  'have a look at', 'have a look', 'i don\'t know', 'a lot of', 'every single', 'listen to'
];
const minedPhrasesSet = new Set(phraseDict.phrases.map(p => p.phrase));
for (const rp of requiredPhrases) {
  assert(minedPhrasesSet.has(rp), `Required phrase "${rp}" must be mined`);
}
console.log('PASS 3: Mined phrases, dictionary, and linguistic evidence verified.');

// ----------------------------------------------------
// TEST 4: Manifest & 167 Sign Assets Schema 2.0.0
// ----------------------------------------------------
const manifestPath = join(SIGNS_DIR, 'manifest.json');
assert(existsSync(manifestPath), 'manifest.json must exist');
const manifest = JSON.parse(readFileSync(manifestPath, 'utf-8'));

assert.equal(manifest.manifest_version, '1.0.0');
assert(manifest.total_playable_signs >= 167, 'Manifest must report at least 167 playable signs');
assert(manifest.signs.length >= 167, 'Manifest must contain at least 167 sign entries');

const NEW_SIGNS_20 = [
  'other', 'six', 'seven', 'should', 'long', 'left', 'next', 'slide',
  'add', 'room', 'off', 'new', 'pick', 'case', 'keep', 'team', 'catch',
  'dead', 'later', 'mine'
];
const manifestIds = new Set(manifest.signs.map(s => s.sign_id));
for (const signId of NEW_SIGNS_20) {
  assert(manifestIds.has(signId), `New sign ${signId} must be in manifest`);
}

for (const entry of manifest.signs) {
  const filePath = join(SIGNS_DIR, entry.file_name);
  assert(existsSync(filePath), `File ${entry.file_name} must exist`);
  const signDoc = JSON.parse(readFileSync(filePath, 'utf-8'));

  assert.equal(signDoc.schema_version, '2.0.0', `${entry.sign_id} schema_version must be 2.0.0`);
  assert.equal(signDoc.motion.status, 'playable', `${entry.sign_id} must be playable`);
  assert.equal(signDoc.motion.return_to_neutral, true, `${entry.sign_id} must return to neutral`);

  const firstKf = signDoc.motion.keyframes[0];
  const lastKf = signDoc.motion.keyframes[signDoc.motion.keyframes.length - 1];
  assert.equal(firstKf.time_ms, 0, `${entry.sign_id} first keyframe at 0ms`);
  assert.equal(lastKf.time_ms, signDoc.motion.duration_ms, `${entry.sign_id} last keyframe at duration_ms`);

  for (const bone of Object.keys(firstKf.rotations)) {
    assert.deepEqual(firstKf.rotations[bone], { x: 0, y: 0, z: 0 }, `${entry.sign_id} ${bone} start neutral`);
    assert.deepEqual(lastKf.rotations[bone], { x: 0, y: 0, z: 0 }, `${entry.sign_id} ${bone} return neutral`);
  }
}
console.log('PASS 4: All 167 signs conform strictly to Schema 2.0.0 with full neutral returns.');

// ----------------------------------------------------
// TEST 5: SignLibrary Preloading & Keyframe Compilation
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
assert(preloadResults.length >= 167, 'Must preload at least 167 signs');
const failed = preloadResults.filter(r => r.status === 'rejected');
assert.equal(failed.length, 0, `Preload failures: ${failed.map(f => f.reason).join(', ')}`);

const allInvolvedBones = new Set(allSignIds.flatMap(id => library.cache.get(id).motion.involved_bones));
const dummyBones = new Map();
allInvolvedBones.forEach(bone => dummyBones.set(bone, { rotation: { x: 0, y: 0, z: 0 } }));

for (const signId of allSignIds) {
  const playable = library.getPlayable(signId, dummyBones);
  assert(playable, `Playable motion for ${signId} must be produced`);
  assert(playable.keyframes.length >= 4, `${signId} must contain at least 4 keyframes`);
}
console.log('PASS 5: SignLibrary preloads and compiles all 167 playable signs without error.');

// ----------------------------------------------------
// TEST 6: YouTube Timeline Synchronizer Verification
// ----------------------------------------------------
const syncMod = (await import('../extension/content/timeline-synchronizer.js')).default;
const YouTubeTimelineSynchronizer = syncMod.YouTubeTimelineSynchronizer || syncMod;

class MockVideoElement {
  constructor() {
    this.currentTime = 0;
    this.listeners = new Map();
  }
  addEventListener(event, fn) {
    if (!this.listeners.has(event)) this.listeners.set(event, []);
    this.listeners.get(event).push(fn);
  }
  removeEventListener(event, fn) {
    if (this.listeners.has(event)) {
      this.listeners.set(event, this.listeners.get(event).filter(f => f !== fn));
    }
  }
  emit(event) {
    (this.listeners.get(event) || []).forEach(fn => fn());
  }
}

const mockVideo = new MockVideoElement();
const dispatchedSigns = [];
const dispatchedCommands = [];
let fallbackTextEmitted = null;

const synchronizer = new YouTubeTimelineSynchronizer({
  videoElement: mockVideo,
  onDispatchSign: (id) => dispatchedSigns.push(id),
  onDispatchCommand: (cmd) => dispatchedCommands.push(cmd),
  onFallback: (txt) => { fallbackTextEmitted = txt; },
  onClearFallback: () => { fallbackTextEmitted = null; }
});

synchronizer.setSegments([
  { id: 1, start: 0.0, end: 5.0, text: 'Hello good morning', signIds: ['hello', 'good', 'morning'] },
  { id: 2, start: 5.5, end: 10.0, text: 'Quantum physics', fallbackWords: ['quantum', 'physics'] }
]);

// Test 1: Video at 1.0s -> Segment 1 signs dispatched
mockVideo.currentTime = 1.0;
mockVideo.emit('timeupdate');
assert.deepEqual(dispatchedSigns, ['hello', 'good', 'morning'], 'Segment 1 signs dispatched');

// Test 2: Video pauses -> PAUSE command dispatched
mockVideo.emit('pause');
assert(dispatchedCommands.includes('PAUSE'), 'Pause command dispatched');

// Test 3: Video resumes -> RESUME command dispatched
mockVideo.emit('play');
assert(dispatchedCommands.includes('RESUME'), 'Resume command dispatched');

// Test 4: Video seeks to 7.0s -> Seek cancels queue, resets avatar, dispatches fallback
mockVideo.currentTime = 7.0;
mockVideo.emit('seeking');
assert(dispatchedCommands.includes('RESET_AVATAR'), 'Reset avatar dispatched on seek');
mockVideo.emit('seeked');
assert.equal(fallbackTextEmitted, 'quantum, physics', 'Segment 2 fallback dispatched');

synchronizer.detach();
console.log('PASS 6: YouTube video timeline synchronizer lifecycle, seeking, and fallback verified.');

// ----------------------------------------------------
// TEST 7: EnglishToISLTranslator Phrase & Contraction Intelligence
// ----------------------------------------------------
const { RuleBasedISLTranslator } = await import('./avatar_viewer/EnglishToISLTranslator.js');
const translator = new RuleBasedISLTranslator();

// Test Phrase-first matching
const phrase1 = translator.translate('Observe your body language on stage');
assert(phrase1.gloss_sequence.includes('BODY') && phrase1.gloss_sequence.includes('GESTURE'), 'Body language compound mapped');

const phrase2 = translator.translate('Please have a look at the slide');
assert(phrase2.sign_ids.includes('look'), 'Have a look at mapped to LOOK');
assert(phrase2.sign_ids.includes('slide'), 'Slide mapped to SLIDE');

// Test Contraction expansions
const cont1 = translator.translate('You\'ll learn this lesson');
assert(cont1.normalized_text.includes('you will'), 'You\'ll normalized to you will');
assert(cont1.sign_ids.includes('you') && cont1.sign_ids.includes('learn'), 'You\'ll signed with YOU and LEARN');

const cont2 = translator.translate('We haven\'t finished yet');
assert(cont2.normalized_text.includes('have not'), 'Haven\'t normalized to have not');
assert(cont2.sign_ids.includes('not') && cont2.sign_ids.includes('finish'), 'Haven\'t signed with NOT and FINISH');

// Test Semantic equivalences
const syn1 = translator.translate('The coach delivers great advice');
assert(syn1.sign_ids.includes('teacher'), 'Coach mapped to TEACHER');
assert(syn1.sign_ids.includes('give'), 'Delivers mapped to GIVE');

console.log('PASS 7: Translator phrase-first precedence, contractions, and semantic equivalences verified.');

// ----------------------------------------------------
// TEST 8: Demonstration Acceptance Scenarios (Mentor Ready)
// ----------------------------------------------------
// Scenario 1: Lecture core sentence
const demo1 = translator.translate('The teacher will show you how to speak confidently');
assert(demo1.sign_ids.includes('teacher'), 'Must sign TEACHER');
assert(demo1.sign_ids.includes('show'), 'Must sign SHOW');
assert(demo1.sign_ids.includes('say'), 'Must sign SAY');
assert(demo1.sign_ids.includes('confident'), 'Must sign CONFIDENT');

// Scenario 2: Mixed sentence with honest subtitle fallback
const demo2 = translator.translate('Pay attention to your body language and neuroplasticity');
assert(demo2.sign_ids.includes('attention'), 'Must sign ATTENTION');
assert(demo2.sign_ids.includes('body'), 'Must sign BODY');
assert(demo2.sign_ids.includes('gesture'), 'Must sign GESTURE');
assert(demo2.unknown_terms.includes('NEUROPLASTICITY'), 'Neuroplasticity must trigger subtitle fallback');

console.log('PASS 8: Demonstration acceptance scenarios verified with avatar motion and subtitle fallback.');
console.log('====================================================');
console.log('ALL PHASE H19 VALIDATION CHECKS PASSED (DEMO READY)');
console.log('====================================================');
