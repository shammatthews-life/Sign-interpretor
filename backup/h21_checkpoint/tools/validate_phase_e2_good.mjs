/**
 * Comprehensive validation for Phase E2: GOOD (SIGN 1)
 *
 * Verifies:
 * 1. signs/good.json adheres strictly to schema 2.0.0.
 * 2. Metadata separates technical animation status (TECHNICALLY_PLAYABLE)
 *    from linguistic verification status (IMPLEMENTATION_PENDING_LINGUISTIC_REVIEW).
 * 3. Dominant hand is right, involved bones include verified right-hand finger bones.
 * 4. SignLibrary preloads and validates GOOD without errors.
 * 5. SignAnimationPlayer plays GOOD at 0.5x, 1.0x, 1.25x, and 1.5x speeds.
 * 6. At least 5 consecutive GOOD -> Reset cycles guarantee 0 drift / zero accumulation.
 * 7. SignScheduler queues HELLO -> GOOD; neither sign contaminates the other's pose state.
 */
import { readFile } from 'node:fs/promises';
import { resolve } from 'node:path';
import { pathToFileURL } from 'node:url';

const projectRoot = resolve(import.meta.dirname, '..');
const goodPath = resolve(projectRoot, 'signs', 'good.json');
const helloPath = resolve(projectRoot, 'signs', 'hello.json');
const playerPath = resolve(projectRoot, 'tools', 'avatar_viewer', 'SignAnimationPlayer.js');
const libraryPath = pathToFileURL(resolve(projectRoot, 'tools', 'avatar_viewer', 'SignLibrary.js')).href;
const schedulerPath = pathToFileURL(resolve(projectRoot, 'tools', 'avatar_viewer', 'SignScheduler.js')).href;

function fail(msg) {
  throw new Error(msg);
}

function assert(cond, msg) {
  if (!cond) fail(msg);
}

function rotation() {
  return {
    x: 0, y: 0, z: 0,
    clone() { return { ...this, clone: this.clone, copy: this.copy, set: this.set }; },
    copy(v) { this.x = v.x; this.y = v.y; this.z = v.z; return this; },
    set(x, y, z) { this.x = x; this.y = y; this.z = z; return this; }
  };
}

function makeBone(name) {
  return {
    name,
    isBone: true,
    rotation: rotation(),
    position: { x: 0, y: 0, z: 0, clone: () => ({ x: 0, y: 0, z: 0 }) }
  };
}

function capture(bones) {
  return Object.fromEntries(
    [...bones.entries()].map(([name, bone]) => [
      name,
      [bone.rotation.x, bone.rotation.y, bone.rotation.z]
    ])
  );
}

function equalPose(before, after, eps = 1e-12) {
  for (const name of Object.keys(before)) {
    if (!after[name]) return false;
    for (let i = 0; i < 3; i++) {
      if (Math.abs(before[name][i] - after[name][i]) > eps) {
        return false;
      }
    }
  }
  return true;
}

// 1. Schema & Metadata Inspection
const goodDef = JSON.parse(await readFile(goodPath, 'utf8'));
assert(goodDef.schema_version === '2.0.0', 'Schema version must be 2.0.0');
assert(goodDef.sign_id === 'good', 'Sign ID must be good');
assert(goodDef.metadata.gloss === 'GOOD', 'Gloss must be GOOD');
assert(goodDef.metadata.display_name === 'Good', 'Display name must be Good');
assert(goodDef.metadata.variant === 'SIGN 1', 'Variant must be SIGN 1');
assert(goodDef.metadata.technical_animation_status === 'TECHNICALLY_PLAYABLE', 'Technical animation status must be TECHNICALLY_PLAYABLE');
assert(goodDef.metadata.linguistic_verification_status === 'IMPLEMENTATION_PENDING_LINGUISTIC_REVIEW', 'Linguistic verification status must be pending');
assert(goodDef.motion.status === 'playable', 'Motion status must be playable');
assert(goodDef.motion.duration_ms > 0 && goodDef.motion.duration_ms !== 2000, 'GOOD duration must be appropriate to gesture and not a copy of HELLO');
assert(goodDef.motion.dominant_hand === 'right', 'Dominant hand must be right');
assert(goodDef.motion.return_to_neutral === true, 'Return to neutral must be true');

// Verify right-hand finger bones
const expectedFingerBones = [
  'Bip001_R_Finger0', 'Bip001_R_Finger01', 'Bip001_R_Finger02',
  'Bip001_R_Finger1', 'Bip001_R_Finger11', 'Bip001_R_Finger12',
  'Bip001_R_Finger2', 'Bip001_R_Finger21', 'Bip001_R_Finger22',
  'Bip001_R_Finger3', 'Bip001_R_Finger31', 'Bip001_R_Finger32',
  'Bip001_R_Finger4', 'Bip001_R_Finger41', 'Bip001_R_Finger42'
];
for (const fb of expectedFingerBones) {
  assert(goodDef.motion.involved_bones.includes(fb), `Missing involved bone: ${fb}`);
}

// 2. SignLibrary Validation
const definitions = new Map();
definitions.set('good', goodDef);
const helloDef = JSON.parse(await readFile(helloPath, 'utf8'));
definitions.set('hello', helloDef);

const { SignLibrary, SignLibraryError } = await import(libraryPath);
const fetchImpl = async url => {
  const id = url.match(/\/([^/]+)\.json$/)?.[1];
  return definitions.has(id) ? { ok: true, json: async () => definitions.get(id) } : { ok: false };
};
const library = new SignLibrary({ basePath: '/signs', fetchImpl });
await library.preload(['hello', 'good']);

// Setup full bone rig
const allInvolved = new Set([...goodDef.motion.involved_bones, ...helloDef.motion.involved_bones]);
const bonesMap = new Map();
for (const name of allInvolved) {
  bonesMap.set(name, makeBone(name));
}

const playableGood = library.getPlayable('good', bonesMap);
assert(playableGood.sign_id === 'good', 'Playable sign_id mismatch');
assert(playableGood.keyframes.length >= 5, 'GOOD motion needs multiple keyframes for repeated pulse');

// Setup HandRig
const handRig = { left: {}, right: {} };
for (const side of ['left', 'right']) {
  const s = side === 'left' ? 'L' : 'R';
  for (let f = 0; f < 5; f++) {
    const fName = ['thumb', 'index', 'middle', 'ring', 'pinky'][f];
    const b0 = bonesMap.get(`Bip001_${s}_Finger${f}`) || makeBone(`Bip001_${s}_Finger${f}`);
    const b1 = bonesMap.get(`Bip001_${s}_Finger${f}1`) || makeBone(`Bip001_${s}_Finger${f}1`);
    const b2 = bonesMap.get(`Bip001_${s}_Finger${f}2`) || makeBone(`Bip001_${s}_Finger${f}2`);
    handRig[side][fName] = [b0, b1, b2];
    bonesMap.set(b0.name, b0);
    bonesMap.set(b1.name, b1);
    bonesMap.set(b2.name, b2);
  }
}

// Setup avatar mock
const avatar = {
  traverse(cb) {
    for (const b of bonesMap.values()) cb(b);
  }
};

// 3. Import SignAnimationPlayer with mocked THREE
const playerCode = await readFile(playerPath, 'utf8');
const testThree = `const THREE = { MathUtils: { degToRad: d => d * Math.PI / 180 } };`;
const playerModule = await import(
  `data:text/javascript;base64,${Buffer.from(playerCode.replace("import * as THREE from 'three';", testThree)).toString('base64')}`
);
const player = new playerModule.SignAnimationPlayer(avatar, bonesMap, handRig);
player.loadSign(playableGood);
const neutralState = capture(bonesMap);

// 4. Test GOOD at speeds 0.5x, 1.0x, 1.25x, 1.5x
for (const speed of [0.5, 1.0, 1.25, 1.5]) {
  player.playbackSpeed = speed;
  player.replay();
  while (player.isPlaying) {
    player.update(20);
  }
  assert(player.currentTimeMs === playableGood.duration_ms, `${speed}x did not reach end`);
  assert(equalPose(neutralState, capture(bonesMap)), `${speed}x end pose diverged from neutral`);
  player.stop();
  assert(equalPose(neutralState, capture(bonesMap)), `${speed}x stop diverged from neutral`);
}

// 5. At least 5 consecutive GOOD -> Reset cycles
for (let cycle = 1; cycle <= 6; cycle++) {
  player.replay();
  // advance partially to establish gesture
  player.update(playableGood.duration_ms * 0.4);
  assert(player.isPlaying, `Cycle ${cycle} should be playing mid-motion`);
  // Reset
  player.stop();
  assert(!player.isPlaying, `Cycle ${cycle} should be stopped`);
  assert(player.currentTimeMs === 0, `Cycle ${cycle} time should be 0 ms`);
  assert(
    equalPose(neutralState, capture(bonesMap)),
    `Cycle ${cycle} GOOD -> Reset left residual drift in bone rotations`
  );
}

// 6. SignScheduler queue test: HELLO -> GOOD
const { SignScheduler } = await import(schedulerPath);
const scheduler = new SignScheduler(player, library, bonesMap);

// Enqueue HELLO, then GOOD
scheduler.enqueue('hello');
scheduler.enqueue('good');

let state = scheduler.getState();
assert(state.current === 'hello', 'Current sign must be HELLO');
assert(state.queued.length === 1 && state.queued[0] === 'good', 'Queue must have GOOD next');

const playedSigns = [];
let lastCurrent = null;

// Step through scheduler until both signs finish
while (player.isPlaying) {
  const cur = scheduler.getState().current;
  if (cur && cur !== lastCurrent) {
    playedSigns.push(cur);
    lastCurrent = cur;
  }
  player.update(20);
}

assert(playedSigns[0] === 'hello' && playedSigns[1] === 'good', 'Scheduler must play HELLO then GOOD in order');

// Complete: entire queue finished
state = scheduler.getState();
assert(!state.current, 'Scheduler current must be null after completion');
assert(state.queued.length === 0, 'Scheduler queue must be empty');
assert(
  equalPose(neutralState, capture(bonesMap)),
  'HELLO -> GOOD execution left residual drift; pose state was contaminated'
);

// 7. Verify pause, resume, cancel on GOOD
scheduler.enqueue('good');
scheduler.pause();
assert(scheduler.isPaused, 'Scheduler must be paused');
scheduler.resume();
assert(!scheduler.isPaused, 'Scheduler must be resumed');
scheduler.cancel();
assert(!scheduler.currentId && scheduler.queue.length === 0, 'Cancel must clear queue');
assert(
  equalPose(neutralState, capture(bonesMap)),
  'Cancel did not restore clean neutral pose'
);

console.log('PASS: signs/good.json valid schema 2.0.0 with separated technical/linguistic metadata');
console.log(`PASS: Duration is ${playableGood.duration_ms} ms (independent from HELLO) with compact back-and-forth pulse`);
console.log('PASS: Right-hand finger bones (Finger0–Finger4, 15 joints) correctly defined');
console.log('PASS: Playback verified at 0.5x, 1.0x, 1.25x, 1.5x with zero accumulation');
console.log('PASS: 6 consecutive GOOD -> Reset cycles restore neutral pose with 0 drift');
console.log('PASS: SignScheduler HELLO -> GOOD sequence executes cleanly without pose contamination');
