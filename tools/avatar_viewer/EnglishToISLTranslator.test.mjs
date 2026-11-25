import assert from 'node:assert/strict';
import { test } from 'node:test';
import { EnglishToISLTranslator } from './EnglishToISLTranslator.js';

test('WS2/WS3 isolates negation strictly within its enclosing clause without bleeding', () => {
  const tr = new EnglishToISLTranslator();
  const res = tr.translate("See the problem isn't that you don't know that. It's that you need a story.");
  assert.ok(res.intermediate_semantic_representation.clause_count >= 2);
  const notIndices = res.gloss_sequence.reduce((acc, g, idx) => (g === 'NOT' ? [...acc, idx] : acc), []);
  // NOT appears only in the negated clause before STORY / NEED of the affirmative second sentence
  const storyIdx = res.gloss_sequence.indexOf('STORY');
  assert.ok(storyIdx > -1);
  assert.ok(notIndices.every(idx => idx < storyIdx), `Negation bled into second clause: ${res.gloss_sequence.join(' ')}`);

  const contrast = tr.translate("I might not know what I'm up to today, but I do know I will meet a friend.");
  const butIdx = contrast.gloss_sequence.indexOf('BUT');
  const firstNotIdx = contrast.gloss_sequence.indexOf('NOT');
  assert.ok(butIdx > 0, 'BUT must be retained');
  assert.ok(firstNotIdx > -1 && firstNotIdx < butIdx, `NOT must close first clause before BUT: ${contrast.gloss_sequence.join(' ')}`);
});

test('WS2/WS3 collapses double-negation auxiliary bugs and preserves privative WITHOUT and causal BECAUSE', () => {
  const tr = new EnglishToISLTranslator();
  const singleNeg = tr.translate("I bet something still just doesn't feel right about your vlog.");
  assert.equal(singleNeg.gloss_sequence.filter(g => g === 'NOT').length, 1);
  assert.equal(singleNeg.gloss_sequence.at(-1), 'NOT');
  assert.ok(singleNeg.gloss_sequence.includes('GOOD'), 'feel right disambiguates to GOOD');

  const privative = tr.translate('Start vlogging your life without overcomplicating the process.');
  assert.ok(privative.gloss_sequence.includes('WITHOUT'));
  assert.ok(privative.sign_ids.includes('without'));

  const causal = tr.translate('I film because I want a story.');
  assert.ok(causal.gloss_sequence.includes('BECAUSE'));
  assert.ok(causal.sign_ids.includes('because'));
});

test('WS2/WS3 distinguishes true perfective aspect from progressive getting and repairs corrupted lexicon targets', () => {
  const tr = new EnglishToISLTranslator();
  const getting = tr.translate("Is this just a shot that I'm getting because it looks cool?");
  assert.equal(getting.gloss_sequence.includes('FINISH'), false, 'getting must NOT trigger spurious FINISH');

  const perfect = tr.translate('We have gathered tools already.');
  assert.ok(perfect.gloss_sequence.includes('FINISH'), 'have + past participle triggers FINISH');

  const repaired = tr.translate('Tomorrow evening eight or nine people arrive on the third train back.');
  assert.ok(repaired.gloss_sequence.includes('EVENING'));
  assert.ok(repaired.gloss_sequence.includes('EIGHT'));
  assert.ok(repaired.gloss_sequence.includes('NINE'));
  assert.ok(repaired.gloss_sequence.includes('THIRD'));
  assert.ok(repaired.gloss_sequence.includes('BACK'));
  assert.equal(repaired.gloss_sequence.includes('MORNING'), false);
});

test('WS2/WS3 emits playable fingerspelling sign_ids for proper nouns, collapses stutters, and flags low ASR confidence', () => {
  const tr = new EnglishToISLTranslator();
  const proper = tr.translate("Hey, if we haven't met before, my name is David JP Phillips.");
  assert.ok(proper.sign_ids.includes('fs_david'));
  assert.ok(proper.sign_ids.includes('fs_jp'));
  assert.ok(proper.sign_ids.includes('fs_phillips'));

  const stutter = tr.translate("I've I've gathered essential tools.");
  assert.equal(stutter.gloss_sequence.filter(g => g === 'I').length, 1);

  const lowConf = tr.translate('Hello friend.', { asrContext: { confidence: 0.35 } });
  assert.equal(lowConf.status, 'TRANSLATION_UNCERTAIN');
  assert.equal(lowConf.asr_confidence, 0.35);
});
