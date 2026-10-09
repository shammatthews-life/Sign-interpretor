import { SentenceProcessor } from './avatar_viewer/SentenceProcessor.js';
import { SignScheduler } from './avatar_viewer/SignScheduler.js';

const assert = (condition, message) => { if (!condition) throw new Error(message); };
const processor = new SentenceProcessor();
const controlled = processor.process('Hello good morning');
assert(JSON.stringify(controlled.signIds) === JSON.stringify(['hello', 'good', 'morning']), 'Controlled sentence mapping failed.');
assert(controlled.unknownWords.length === 0, 'Known sentence reported unknown words.');
const withUnknown = processor.process('Hello good morning xyz');
assert(JSON.stringify(withUnknown.signIds) === JSON.stringify(['hello', 'good', 'morning']), 'Unknown word changed known sequence.');
assert(JSON.stringify(withUnknown.unknownWords) === JSON.stringify(['XYZ']), 'Unknown word was not reported.');

class FakePlayer {
  constructor() { this.currentTimeMs = 0; this.onCompleteCallback = null; this.loaded = []; }
  loadSign(sign) { this.loaded.push(sign.sign_id); this.currentTimeMs = 0; }
  play() { this.playing = true; }
  pause() { this.playing = false; }
  stop() { this.playing = false; this.currentTimeMs = 0; }
  complete() { this.playing = false; this.onCompleteCallback(); }
}
const available = new Set(['hello', 'good', 'morning']);
const library = { getPlayable(id) { if (!available.has(id)) throw new Error(`Unplayable sign: ${id}`); return { sign_id: id, duration_ms: 1, involved_bones: [], keyframes: [] }; } };
const player = new FakePlayer();
const scheduler = new SignScheduler(player, library, new Map());
scheduler.enqueue('hello');
assert(scheduler.getState().current === 'hello', 'HELLO did not start.');
scheduler.enqueue('good'); scheduler.enqueue('morning');
assert(JSON.stringify(scheduler.getState().queued) === JSON.stringify(['good', 'morning']), 'Incremental queue ordering failed.');
player.complete(); player.complete(); player.complete();
assert(JSON.stringify(player.loaded) === JSON.stringify(['hello', 'good', 'morning']), 'Streamed signs were not played in sequence.');
assert(!scheduler.getState().current && scheduler.getState().queued.length === 0, 'Scheduler did not finish cleanly.');
console.log('PASS: controlled text maps HELLO GOOD MORNING to sign IDs');
console.log('PASS: unknown words are reported and never fabricated');
console.log('PASS: scheduler accepts GOOD and MORNING while HELLO is active');
