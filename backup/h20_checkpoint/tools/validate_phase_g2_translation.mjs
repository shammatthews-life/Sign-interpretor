import { EnglishToISLTranslator } from './avatar_viewer/EnglishToISLTranslator.js';
import { SpeechSignOrchestrator } from './avatar_viewer/SpeechSignOrchestrator.js';
import { SentenceProcessor } from './avatar_viewer/SentenceProcessor.js';
import { SignScheduler } from './avatar_viewer/SignScheduler.js';
const assert = (ok, message) => { if (!ok) throw new Error(message); };
const translator = new EnglishToISLTranslator();
const cases = [
  ['Hello.', ['HELLO']], ['Good morning.', ['GOOD', 'MORNING']], ['I drink water.', ['I', 'WATER', 'DRINK']],
  ['You help me.', ['YOU', 'ME', 'HELP']], ['Thank you.', ['THANK_YOU']], ['Will you help me?', ['YOU', 'ME', 'HELP']], ['I need water.', ['I', 'WATER', 'NEED']],
];
for (const [english, expectedGloss] of cases) {
  const r = translator.translate(english);
  assert(JSON.stringify(r.gloss_sequence) === JSON.stringify(expectedGloss), `${english}: unexpected gloss`);
  assert(r.transformation_trace.length >= 2, `${english}: missing trace`);
  assert(Object.values(r.timings_ms).every(Number.isFinite), `${english}: missing timings`);
  console.log(`${english} -> ${r.normalized_text} -> ${r.gloss_sequence.join(' ')} | available: ${r.sign_ids.join(',') || 'none'} | unknown: ${r.unknown_terms.join(',') || 'none'} | unavailable: ${r.unavailable_signs.map(x => x.sign_id).join(',') || 'none'}`);
}
const water = translator.translate('I drink water.');
assert(water.unknown_terms.length === 0, 'WATER must be linguistically known.');
assert(water.unavailable_signs.some(x => x.sign_id === 'water'), 'WATER must be known but motion-unavailable.');
const unknown = translator.translate('I drink nebula.');
assert(unknown.unknown_terms.includes('NEBULA'), 'Unknown term must be retained.');
class Player { loadSign() {} play() {} pause() {} stop() {} }
const scheduler = new SignScheduler(new Player(), { getPlayable: () => ({ sign_id: 'hello' }) }, new Map());
const orchestrator = new SpeechSignOrchestrator({ sentenceProcessor: new SentenceProcessor(), translator, signScheduler: scheduler });
orchestrator.start(); orchestrator.handleTranscriptEvent({ kind: 'FINAL_TRANSCRIPT', text: 'hello good morning' });
assert(JSON.stringify(orchestrator.getDiagnostics().committedSignIds) === JSON.stringify(['hello', 'good', 'morning']), 'G2 must feed G1 sign IDs.');
console.log('PASS: G2 translator separates gloss, unknown terms, motion availability, timing, and G1 scheduling.');
