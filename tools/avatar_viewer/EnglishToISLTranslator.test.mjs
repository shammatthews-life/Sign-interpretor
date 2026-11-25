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

test('H44 regression fixes across A05, A12, A15, A18, B01, B03, B18, B21, B23, B25, B30, B31', () => {
  const tr = new EnglishToISLTranslator();

  // A05: nominal pseudo-cleft keeps WHAT at start without WH-question fronting reversal
  const a05 = tr.translate("What you're about to watch is a live coaching.");
  assert.equal(a05.gloss_sequence[0], 'WHAT');
  assert.equal(a05.intermediate_semantic_representation.clauses[0].is_matrix_wh_question, false);

  // A12 & B23 & B21: newly curated semantic signs (FAMOUS, REMAINING, AROUND)
  const a12 = tr.translate('I am perhaps best known for my TEDx talks.');
  assert.ok(a12.sign_ids.includes('famous'));

  // A15: avoid FIND CLEAR CLEAR duplication
  const a15 = tr.translate('And from this coaching, you are going to be able to pinpoint the exact parts.');
  assert.ok(a15.gloss_sequence.includes('FIND'));

  // A18: possessive noun strips 's before lookup (audience's -> AUDIENCE)
  const a18 = tr.translate("So many things when it comes to capturing an audience's attention.");
  assert.equal(a18.unknown_terms.length, 0, `Unexpected unknowns: ${a18.unknown_terms.join(', ')}`);
  assert.ok(a18.sign_ids.includes('audience'));
  assert.ok(a18.sign_ids.includes('many'));

  // B01: generic noun TIME not falsely fronted ahead of SUMMER
  const b01 = tr.translate("Summer is here, and it's the best time to go out and make a vlog.");
  assert.equal(b01.gloss_sequence[0], 'SUMMER');

  // B03: "in the back of your mind" resolves strictly to playable sign_ids (deep)
  const b03 = tr.translate("That kind of puts a barrier in the back of your mind.");
  assert.ok(b03.sign_ids.includes('deep'));
  assert.equal(b03.unknown_terms.length, 0);

  // B18: SOV stops before relative THAT ("compilation of scenes that when stitched together...")
  const b18 = tr.translate('You need a compilation of scenes that when stitched together tell a greater and broader story.');
  assert.ok(b18.gloss_sequence.indexOf('SCENE') < b18.gloss_sequence.indexOf('NEED'));

  // B21: "or so" approximator preserved as AROUND without trailing OR
  const b21 = tr.translate("If I'm going to meet someone in an hour or so and I know we'll eat together,");
  assert.ok(b21.sign_ids.includes('around'));
  assert.notEqual(b21.gloss_sequence.at(-1), 'OR');

  // B23: "rest of the evening" -> REMAINING EVENING
  const b23 = tr.translate('Maybe we film a scene or two for the rest of the evening.');
  assert.ok(b23.sign_ids.includes('remaining'));

  // B25: embedded direct question "shooting of what is my story" -> MY STORY WHAT
  const b25 = tr.translate('Before you start shooting of what is my story?');
  assert.equal(b25.gloss_sequence.slice(-3).join(' '), 'MY STORY WHAT');

  // B30: "capture some dialogue" maps to RECORD rather than literal HOLD
  const b30 = tr.translate("I'll also capture some dialogue, some talking.");
  assert.ok(b30.sign_ids.includes('record'));

  // B31: "show not tell" contrastive idiom does NOT invert polarity with trailing NOT
  const b31 = tr.translate('You have probably heard of the phrase show not tell.');
  assert.equal(b31.gloss_sequence.includes('NOT'), false);
  assert.ok(b31.gloss_sequence.includes('SHOW'));
});
