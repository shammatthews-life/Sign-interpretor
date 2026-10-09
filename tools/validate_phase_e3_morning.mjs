import { readFile } from 'node:fs/promises';
import { resolve } from 'node:path';
import { pathToFileURL } from 'node:url';

const root = resolve(import.meta.dirname, '..');
const morningDef = JSON.parse(await readFile(resolve(root, 'signs/morning.json'), 'utf8'));
const helloDef = JSON.parse(await readFile(resolve(root, 'signs/hello.json'), 'utf8'));
const libraryUrl = pathToFileURL(resolve(root, 'tools/avatar_viewer/SignLibrary.js')).href;
const schedulerUrl = pathToFileURL(resolve(root, 'tools/avatar_viewer/SignScheduler.js')).href;
const playerPath = resolve(root, 'tools/avatar_viewer/SignAnimationPlayer.js');
const assert = (condition, message) => { if (!condition) throw new Error(message); };

assert(morningDef.schema_version === '2.0.0', 'MORNING must use schema 2.0.0.');
assert(morningDef.motion.status === 'playable', 'MORNING must be technically playable.');
assert(morningDef.motion.duration_ms === 1800, 'MORNING duration must be 1800 ms.');
assert(morningDef.motion.keyframes.length === 6, 'MORNING must have six authored keyframes.');
assert(morningDef.metadata.linguistic_verification_status === 'IMPLEMENTATION_PENDING_LINGUISTIC_REVIEW', 'MORNING must not claim linguistic validation.');

const definitions = new Map([['hello', helloDef], ['morning', morningDef]]);
const { SignLibrary } = await import(libraryUrl);
const library = new SignLibrary({ basePath: '/signs', fetchImpl: async url => {
  const id = url.match(/\/([^/]+)\.json$/)?.[1];
  return definitions.has(id) ? { ok: true, json: async () => definitions.get(id) } : { ok: false };
} });
await library.preload(['hello', 'morning']);

const rotation = () => ({ x: 0, y: 0, z: 0, clone() { return { ...this, clone: this.clone, copy: this.copy, set: this.set }; }, copy(value) { this.x=value.x; this.y=value.y; this.z=value.z; return this; }, set(x,y,z) { this.x=x; this.y=y; this.z=z; return this; } });
const makeBone = name => ({ name, isBone: true, rotation: rotation(), position: { x: 0, y: 0, z: 0, clone: () => ({ x: 0, y: 0, z: 0 }) } });
const names = new Set([...morningDef.motion.involved_bones, ...helloDef.motion.involved_bones]);
const bones = new Map([...names].map(name => [name, makeBone(name)]));
const handRig = { left: {}, right: {} };
for (const side of ['L', 'R']) for (const [index, finger] of ['thumb','index','middle','ring','pinky'].entries()) {
  const chain = [0, 1, 2].map(joint => {
    const name = `Bip001_${side}_Finger${index}${joint || ''}`;
    if (!bones.has(name)) bones.set(name, makeBone(name));
    return bones.get(name);
  });
  handRig[side === 'L' ? 'left' : 'right'][finger] = chain;
}
const snapshot = () => JSON.stringify([...bones.entries()].map(([name, bone]) => [name, bone.rotation.x, bone.rotation.y, bone.rotation.z]));
const neutral = snapshot();
const playerCode = await readFile(playerPath, 'utf8');
const playerModule = await import(`data:text/javascript;base64,${Buffer.from(playerCode.replace("import * as THREE from 'three';", "const THREE = { MathUtils: { degToRad: d => d * Math.PI / 180 } };")).toString('base64')}`);
const player = new playerModule.SignAnimationPlayer({ traverse(callback) { for (const bone of bones.values()) callback(bone); } }, bones, handRig);
const morning = library.getPlayable('morning', bones);

for (const speed of [0.5, 1, 1.25, 1.5]) {
  player.loadSign(morning); player.playbackSpeed = speed; player.play();
  while (player.isPlaying) player.update(20);
  assert(snapshot() === neutral, `${speed}x playback did not return to neutral.`);
}
for (let cycle = 0; cycle < 5; cycle += 1) {
  player.replay(); player.update(700); player.stop();
  assert(snapshot() === neutral, `MORNING reset cycle ${cycle + 1} drifted.`);
}
const { SignScheduler } = await import(schedulerUrl);
const scheduler = new SignScheduler(player, library, bones);
scheduler.enqueue('morning');
assert(scheduler.getState().current === 'morning', 'Scheduler did not start MORNING.');
player.update(2000);
assert(!scheduler.getState().current && scheduler.getState().queued.length === 0 && snapshot() === neutral, 'MORNING scheduler playback did not reset cleanly.');

console.log('PASS: MORNING schema, cache loading, player playback, and scheduler queue verified');
console.log('PASS: MORNING works at 0.5x, 1.0x, 1.25x, 1.5x with no accumulation');
console.log('PASS: five MORNING -> Reset cycles restore the neutral pose with no finger drift');
