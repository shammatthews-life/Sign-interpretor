#!/usr/bin/env node
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import * as THREE from 'three';
import { SignAnimationPlayer } from '../tools/avatar_viewer/SignAnimationPlayer.js';
import { SignLibrary } from '../tools/avatar_viewer/SignLibrary.js';
import { SignScheduler } from '../tools/avatar_viewer/SignScheduler.js';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const signDefinition = JSON.parse(fs.readFileSync(path.join(root, 'signs', 'hello.json'), 'utf8'));
const bonesMap = new Map();
const avatar = new THREE.Group();
for (const name of signDefinition.motion.involved_bones) {
  const bone = new THREE.Bone();
  bone.name = name;
  bonesMap.set(name, bone);
  avatar.add(bone);
}

const library = new SignLibrary();
library.cache.set('hello', signDefinition);
const player = new SignAnimationPlayer(avatar, bonesMap, null);
const lifecycle = [];
const scheduler = new SignScheduler(player, library, bonesMap, null, event => lifecycle.push(event));
const neutral = new Map(
  [...bonesMap].map(([name, bone]) => [name, [bone.rotation.x, bone.rotation.y, bone.rotation.z]])
);

assert.deepEqual(scheduler.enqueue('hello', 'h33.4-avatar-smoke'), { accepted: true });
player.update(750);
const movement = Math.max(
  ...[...bonesMap.values()].map(bone => Math.abs(bone.rotation.x)
    + Math.abs(bone.rotation.y) + Math.abs(bone.rotation.z))
);
assert.ok(movement > 0.1, `Expected visible bone rotation, observed ${movement}.`);
player.update(signDefinition.motion.duration_ms);
assert.equal(scheduler.currentId, null);

const neutralError = Math.max(
  ...[...bonesMap].map(([name, bone]) => Math.max(
    ...[bone.rotation.x, bone.rotation.y, bone.rotation.z]
      .map((value, index) => Math.abs(value - neutral.get(name)[index]))
  ))
);
assert.ok(neutralError <= 1e-10, `Avatar did not return to neutral; maximum rotation error ${neutralError}.`);
assert.deepEqual(lifecycle.map(event => [event.type, event.id, event.eventId]), [
  ['accepted', 'hello', 'h33.4-avatar-smoke'],
  ['playback_start', 'hello', 'h33.4-avatar-smoke'],
  ['playback_end', 'hello', 'h33.4-avatar-smoke']
]);

const evidence = {
  status: 'PASS_ENGINE_LEVEL_ASSET_PLAYBACK_NOT_BROWSER_RENDER',
  asset: 'signs/hello.json',
  sign_id: signDefinition.sign_id,
  duration_ms: signDefinition.motion.duration_ms,
  involved_bones: signDefinition.motion.involved_bones.length,
  measured_maximum_bone_rotation_rad: movement,
  neutral_reset_maximum_error_rad: neutralError,
  lifecycle_events: lifecycle.map(event => ({
    type: event.type,
    sign_id: event.id,
    event_id: event.eventId
  })),
  browser_rendered: false,
  chrome_extension_acceptance: 'NOT RUN'
};
fs.writeFileSync(
  path.join(root, 'data', 'h33_4_avatar_motion_test.json'),
  `${JSON.stringify(evidence, null, 2)}\n`,
  'utf8'
);
console.log(JSON.stringify(evidence, null, 2));
