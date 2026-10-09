import { readFile } from 'node:fs/promises';
import { resolve } from 'node:path';
import { SignLibrary, SignLibraryError } from './avatar_viewer/SignLibrary.js';
import { SignScheduler } from './avatar_viewer/SignScheduler.js';

const root = resolve(import.meta.dirname, '..');
const definitions = new Map();
for (const id of ['hello', 'good', 'morning', 'water']) {
  definitions.set(id, JSON.parse(await readFile(resolve(root, 'signs', `${id}.json`), 'utf8')));
}
const fetchImpl = async url => {
  const id = url.match(/\/([^/]+)\.json$/)?.[1];
  return definitions.has(id) ? { ok: true, json: async () => definitions.get(id) } : { ok: false };
};
const library = new SignLibrary({ basePath: '/signs', fetchImpl });
const preload = await library.preload(['hello', 'good', 'morning', 'water']);
if (preload.some(result => result.status !== 'fulfilled')) throw new Error('All local definitions must preload.');

const allBones = new Set([...definitions.get('hello').motion.involved_bones, ...definitions.get('good').motion.involved_bones, ...definitions.get('morning').motion.involved_bones]);
const bonesMap = new Map([...allBones].map(name => [name, {}]));
const hello = library.getPlayable('hello', bonesMap);
if (hello.gloss !== 'HELLO' || hello.keyframes.length !== 7) throw new Error('HELLO did not produce its playable baseline.');
const good = library.getPlayable('good', bonesMap);
if (good.gloss !== 'GOOD' || good.keyframes.length !== 7) throw new Error('GOOD did not produce its playable baseline.');
const morning = library.getPlayable('morning', bonesMap);
if (morning.gloss !== 'MORNING' || morning.keyframes.length !== 6) throw new Error('MORNING did not produce its playable baseline.');
for (const id of ['water']) {
  try { library.getPlayable(id, bonesMap); throw new Error(`${id} should be incomplete.`); }
  catch (error) { if (!(error instanceof SignLibraryError) || error.code !== 'MOTION_INCOMPLETE') throw error; }
}

class FakePlayer {
  constructor() { this.currentTimeMs = 0; this.loaded = []; this.stopCount = 0; this.onCompleteCallback = null; }
  loadSign(sign) { this.loaded.push(sign.sign_id); this.currentTimeMs = 0; }
  play() { this.playing = true; }
  pause() { this.playing = false; }
  stop() { this.playing = false; this.currentTimeMs = 0; this.stopCount += 1; }
  complete() { this.currentTimeMs = 2000; this.playing = false; this.onCompleteCallback(); }
}

const player = new FakePlayer();
const scheduler = new SignScheduler(player, library, bonesMap);
scheduler.enqueue('hello');
scheduler.enqueue('hello'); // Incremental enqueue while the first sign is active.
scheduler.enqueue('hello');
if (scheduler.getState().current !== 'hello' || scheduler.getState().queued.length !== 2) throw new Error('Queue ordering failed.');
player.complete(); player.complete(); player.complete();
if (scheduler.getState().current || scheduler.getState().queued.length || player.currentTimeMs !== 0) throw new Error('Queue did not safely reset after execution.');
scheduler.enqueue('hello'); scheduler.pause(); scheduler.resume(); scheduler.cancel();
if (scheduler.getState().current || scheduler.getState().queued.length || player.currentTimeMs !== 0) throw new Error('Cancel did not safely reset the queue.');

console.log('PASS: preloaded reusable library loads HELLO and reports incomplete source-backed signs');
console.log('PASS: scheduler preserves ordering, accepts incremental enqueue, pauses/resumes, and safely resets');
console.log('PASS: HELLO, GOOD, MORNING are playable; WATER is correctly blocked as incomplete rather than fabricating ISL motion');
