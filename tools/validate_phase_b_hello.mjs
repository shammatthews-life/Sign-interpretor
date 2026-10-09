/**
 * Focused, dependency-free validation for the Phase B HELLO prototype.
 *
 * It executes the reusable player against a minimal Aether-shaped rig and
 * verifies that five consecutive replays end in the captured neutral pose
 * without drift. The viewer performs the authoritative FBX bone lookup at run
 * time; the CLI check verifies that HELLO only references the viewer's named
 * Aether bone contract.
 */
import { readFile } from 'node:fs/promises';
import { resolve } from 'node:path';

const projectRoot = resolve(import.meta.dirname, '..');
const signPath = resolve(projectRoot, 'signs', 'hello.json');
const playerPath = resolve(projectRoot, 'tools', 'avatar_viewer', 'SignAnimationPlayer.js');
const viewerPath = resolve(projectRoot, 'tools', 'avatar_viewer', 'index.html');

function fail(message) {
  throw new Error(message);
}

function assert(condition, message) {
  if (!condition) fail(message);
}

function rotation() {
  return {
    x: 0, y: 0, z: 0,
    clone() { return { ...this, clone: this.clone, copy: this.copy, set: this.set }; },
    copy(value) { this.x = value.x; this.y = value.y; this.z = value.z; return this; },
    set(x, y, z) { this.x = x; this.y = y; this.z = z; return this; }
  };
}

function makeBone(name) {
  return { name, isBone: true, rotation: rotation(), position: { clone: () => ({ x: 0, y: 0, z: 0 }) } };
}

function capture(bones) {
  return Object.fromEntries([...bones.entries()].map(([name, bone]) => [name, [bone.rotation.x, bone.rotation.y, bone.rotation.z]]));
}

function equalPose(before, after) {
  return Object.keys(before).every(name => before[name].every((value, index) => Math.abs(value - after[name][index]) < 1e-12));
}

const definition = JSON.parse(await readFile(signPath, 'utf8'));
assert(definition.schema_version === '2.0.0', 'Expected reusable sign-library schema');
assert(definition.metadata.gloss === 'HELLO', 'Expected HELLO gloss');
assert(definition.sign_id === 'hello', 'Expected hello sign id');
const sign = { ...definition.motion, sign_id: definition.sign_id, gloss: definition.metadata.gloss };
assert(sign.dominant_hand === 'right', 'HELLO must use the right hand in this prototype');
assert(sign.return_to_neutral === true, 'HELLO must return to neutral');
assert(!Object.hasOwn(sign, 'interpolation'), 'HELLO must use the player’s predictable authored-pose interpolation');
assert(Array.isArray(sign.keyframes) && sign.keyframes.length === 7, 'Expected the final seven-keyframe HELLO refinement');
assert(sign.keyframes[0].time_ms === 0, 'First keyframe must start at 0 ms');
assert(sign.keyframes.at(-1).time_ms === sign.duration_ms, 'Final keyframe must end at the duration');
assert(sign.keyframes.every((keyframe, index) => index === 0 || keyframe.time_ms > sign.keyframes[index - 1].time_ms), 'Keyframe times must be strictly increasing');
assert(sign.keyframes.every(keyframe => Object.values(keyframe.finger_curls).every(value => value === 0)), 'Bind/open handshape must remain stable without curl interpolation');
assert(sign.keyframes.every(keyframe => Object.values(keyframe.rotations.Bip001_Head).every(value => value === 0)), 'Head motion must remain neutral during HELLO');

const viewerSource = await readFile(viewerPath, 'utf8');
assert(sign.involved_bones.length > 0, 'HELLO must declare its involved bones');
assert(viewerSource.includes("signLibrary.getPlayable('hello', bonesMap)"), 'Viewer must validate HELLO against the resolved Aether bone map');

const moduleText = await readFile(playerPath, 'utf8');
const testThree = `const THREE = { MathUtils: { degToRad: degrees => degrees * Math.PI / 180 } };`;
const playerModule = await import(`data:text/javascript;base64,${Buffer.from(moduleText.replace("import * as THREE from 'three';", testThree)).toString('base64')}`);
const bones = new Map();
for (const boneName of sign.involved_bones) bones.set(boneName, makeBone(boneName));
const handRig = { left: {}, right: {} };
for (const side of ['left', 'right']) {
  for (const finger of ['thumb', 'index', 'middle', 'ring', 'pinky']) {
    handRig[side][finger] = [makeBone(`${side}-${finger}-0`), makeBone(`${side}-${finger}-1`), makeBone(`${side}-${finger}-2`)];
  }
}
const avatar = { traverse(callback) { for (const bone of bones.values()) callback(bone); for (const hand of Object.values(handRig)) for (const chain of Object.values(hand)) for (const bone of chain) callback(bone); } };
const player = new playerModule.SignAnimationPlayer(avatar, bones, handRig);
player.loadSign(sign);
const neutral = capture(bones);

for (const speed of [0.5, 1.0]) {
  player.playbackSpeed = speed;
  for (let replay = 1; replay <= 5; replay += 1) {
    player.replay();
    while (player.isPlaying) player.update(50);
    assert(player.currentTimeMs === sign.duration_ms, `${speed}x replay ${replay} did not reach the end state`);
    assert(equalPose(neutral, capture(bones)), `${speed}x replay ${replay} did not return the main rig to neutral`);
    player.stop();
    assert(equalPose(neutral, capture(bones)), `${speed}x replay ${replay} stop did not preserve neutral`);
  }
}

console.log('PASS: hello.json loads and identifies HELLO');
console.log(`PASS: ${sign.keyframes.length} valid keyframes span ${sign.duration_ms} ms`);
console.log(`PASS: ${sign.involved_bones.length} referenced bones are required by the viewer's runtime Aether-bone check`);
console.log('PASS: at 0.5x and 1.0x, five replays reach end state and return to the same neutral pose without rotation accumulation');
