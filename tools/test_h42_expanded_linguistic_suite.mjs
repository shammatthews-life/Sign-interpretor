import assert from 'node:assert/strict';
import test from 'node:test';
import { EnglishToISLTranslator } from './avatar_viewer/EnglishToISLTranslator.js';

const translator = new EnglishToISLTranslator();

console.log('===========================================================================');
console.log('H42 EXPANDED ISL LINGUISTIC EDGE-CASE TEST SUITE');
console.log('Testing: Multi-clause scoping, Conditionals, Modals, Aspect, Deixis');
console.log('===========================================================================\n');

test('Linguistic Test 1: Multi-clause coordination prevents argument bleeding', () => {
  const utterance = 'I start filming and you watch the movie.';
  const res = translator.translate(utterance);
  const gloss = res.gloss_sequence;
  
  // Both clauses must maintain independent SOV order
  assert.ok(gloss.includes('I'), 'Clause 1 must contain subject I');
  assert.ok(gloss.includes('RECORD'), 'Clause 1 must contain verb RECORD');
  assert.ok(gloss.includes('YOU'), 'Clause 2 must contain subject YOU');
  assert.ok(gloss.includes('MOVIE'), 'Clause 2 must contain object MOVIE');
  assert.ok(gloss.includes('WATCH'), 'Clause 2 must contain verb WATCH');
  
  // In Clause 2, MOVIE must precede WATCH in SOV
  const movieIdx = gloss.indexOf('MOVIE');
  const watchIdx = gloss.indexOf('WATCH');
  assert.ok(movieIdx < watchIdx, `SOV failed: MOVIE (${movieIdx}) must precede WATCH (${watchIdx})`);
  
  // Clause 1 verb RECORD must not be pulled after Clause 2 object MOVIE
  const recordIdx = gloss.indexOf('RECORD');
  assert.ok(recordIdx < movieIdx, `Argument bleeding: RECORD (${recordIdx}) should precede MOVIE (${movieIdx})`);
});

test('Linguistic Test 2: Modal necessity vs possession disambiguation (have to have)', () => {
  const utterance = 'You have to have a story.';
  const res = translator.translate(utterance);
  const gloss = res.gloss_sequence;
  
  assert.ok(gloss.includes('NEED'), 'Modal necessity must resolve to NEED');
  assert.ok(gloss.includes('HAVE'), 'Possession verb must resolve to HAVE');
  assert.ok(gloss.includes('STORY'), 'Complement noun must resolve to STORY');
  
  // In ISL SOV, object STORY precedes modal-verb complex
  const storyIdx = gloss.indexOf('STORY');
  const needIdx = gloss.indexOf('NEED');
  assert.ok(storyIdx < needIdx, `SOV fronting: STORY (${storyIdx}) must precede NEED (${needIdx})`);
});

test('Linguistic Test 3: Aspectual completion marker (FINISH) placement', () => {
  const utterance = 'I have practiced public speaking.';
  const res = translator.translate(utterance);
  const gloss = res.gloss_sequence;
  
  assert.ok(gloss.includes('PRACTICE'), 'Verb PRACTICE must be present');
  assert.ok(gloss.includes('FINISH'), 'Completed aspect marker FINISH must be present');
  
  const practiceIdx = gloss.indexOf('PRACTICE');
  const finishIdx = gloss.indexOf('FINISH');
  assert.equal(finishIdx, practiceIdx + 1, 'FINISH must directly follow the lexical verb PRACTICE');
});

test('Linguistic Test 4: Temporal marker fronting with conversational opener retention', () => {
  const utterance = 'Hello, tomorrow we will meet.';
  const res = translator.translate(utterance);
  const gloss = res.gloss_sequence;
  
  assert.equal(gloss[0], 'HELLO', 'Conversational opener HELLO must retain position 0');
  assert.equal(gloss[1], 'TOMORROW', 'Temporal adverb TOMORROW must follow greeting at position 1');
  assert.ok(gloss.includes('MEET'), 'Lexical verb MEET must be present');
});

test('Linguistic Test 5: WH-question word moved to clause-final position with non-manual marker', () => {
  const utterance = 'What do you want?';
  const res = translator.translate(utterance);
  const gloss = res.gloss_sequence;
  
  assert.equal(gloss[gloss.length - 1], 'WHAT', 'WH question word WHAT must be moved to clause-final position');
  assert.ok(res.non_manual_markers.includes('WH_QUESTION'), 'Non-manual marker WH_QUESTION must be generated');
});

test('Linguistic Test 6: Yes/No question non-manual marker generation without invented manual sign', () => {
  const utterance = 'Can you see the picture?';
  const res = translator.translate(utterance);
  
  assert.ok(res.non_manual_markers.includes('YES_NO_QUESTION'), 'YES_NO_QUESTION non-manual marker must be generated');
  assert.ok(!res.gloss_sequence.includes('QUESTION_MARK'), 'No invented manual question sign should exist');
});

test('Linguistic Test 7: Natural ISL function word omission classification', () => {
  const utterance = 'Just go out because of the weather.';
  const res = translator.translate(utterance);
  
  const omittedTokens = res.grammar_omissions.map(g => g.token);
  assert.ok(omittedTokens.includes('just'), 'just must be classified as GRAMMAR_OMISSION');
  assert.ok(omittedTokens.includes('because'), 'because must be classified as GRAMMAR_OMISSION');
  assert.ok(omittedTokens.includes('of'), 'of must be classified as GRAMMAR_OMISSION');
  assert.ok(omittedTokens.includes('the'), 'the must be classified as GRAMMAR_OMISSION');
  assert.equal(res.unknown_terms.length, 0, 'No valid English words should be marked as unknown');
});

test('Linguistic Test 8: Sourced authentic Schema 2.0.0 signs produce playable sign IDs', () => {
  const testSigns = ['food', 'summer', 'future', 'advice', 'together', 'tired'];
  for (const signId of testSigns) {
    const res = translator.translate(`We need ${signId}`);
    assert.ok(res.sign_ids.includes(signId), `Sign ${signId} must resolve to playable sign_id in translator`);
  }
});
