import assert from 'node:assert/strict';
import { test } from 'node:test';
import * as THREE from 'three';
import { SignAnimationPlayer } from './SignAnimationPlayer.js';

function makeBone(name, restZ = 0) {
  const rot = new THREE.Euler(0, 0, restZ);
  rot.clone = () => new THREE.Euler(rot.x, rot.y, rot.z);
  const pos = new THREE.Vector3(0, 0, 0);
  pos.clone = () => new THREE.Vector3(pos.x, pos.y, pos.z);
  return {
    isBone: true,
    name,
    rotation: rot,
    position: pos
  };
}

function makeRig() {
  const bonesMap = new Map();
  const register = bone => {
    bonesMap.set(bone.name, bone);
    return bone;
  };

  const rightArm = register(makeBone('mixamorigRightArm', 0));
  const leftArm = register(makeBone('mixamorigLeftArm', 0));

  const handRig = {
    right: {
      thumb: [register(makeBone('mixamorigRightHandThumb1', 0.1))],
      index: [register(makeBone('mixamorigRightHandIndex1', 0.1)), register(makeBone('mixamorigRightHandIndex2', 0.1))],
      middle: [],
      ring: [],
      pinky: []
    },
    left: {
      thumb: [register(makeBone('mixamorigLeftHandThumb1', 0.2))],
      index: [register(makeBone('mixamorigLeftHandIndex1', 0.2)), register(makeBone('mixamorigLeftHandIndex2', 0.2))],
      middle: [],
      ring: [],
      pinky: []
    }
  };

  const avatarModel = {
    traverse(fn) {
      bonesMap.forEach(b => fn(b));
    }
  };

  return { avatarModel, bonesMap, handRig, rightArm, leftArm };
}

test('SignAnimationPlayer converts keyframe rotations from degrees to radians relative to rest', () => {
  const { avatarModel, bonesMap, handRig, rightArm } = makeRig();
  const player = new SignAnimationPlayer(avatarModel, bonesMap, handRig);
  const playable = {
    signId: 'test_deg',
    duration_ms: 1000,
    dominant_hand: 'right',
    return_to_neutral: false,
    involved_bones: ['mixamorigRightArm'],
    keyframes: [
      { time_ms: 0, rotations: { mixamorigRightArm: { x: 0, y: 0, z: 0 } } },
      { time_ms: 1000, rotations: { mixamorigRightArm: { x: 45, y: 0, z: -90 } } }
    ]
  };

  player.loadSign(playable);
  player.play();
  player.update(1000);

  assert.ok(Math.abs(rightArm.rotation.x - THREE.MathUtils.degToRad(45)) < 1e-5);
  assert.ok(Math.abs(rightArm.rotation.z - THREE.MathUtils.degToRad(-90)) < 1e-5);
});

test('SignAnimationPlayer applies finger_curls to both hands when dominant_hand is both', () => {
  const { avatarModel, bonesMap, handRig } = makeRig();
  const player = new SignAnimationPlayer(avatarModel, bonesMap, handRig);
  const playable = {
    signId: 'test_bimanual_curls',
    duration_ms: 1000,
    dominant_hand: 'both',
    return_to_neutral: false,
    involved_bones: [],
    keyframes: [
      { time_ms: 0, rotations: {}, finger_curls: { index: 0 } },
      { time_ms: 1000, rotations: {}, finger_curls: { index: 80 } }
    ]
  };

  player.loadSign(playable);
  player.play();
  player.update(1000);

  const expectedRight = 0.1 + THREE.MathUtils.degToRad(80) * 0.75;
  const expectedLeft = 0.2 + THREE.MathUtils.degToRad(80) * 0.75;
  assert.ok(Math.abs(handRig.right.index[0].rotation.z - expectedRight) < 1e-5);
  assert.ok(Math.abs(handRig.left.index[0].rotation.z - expectedLeft) < 1e-5);
});

test('SignAnimationPlayer supports per-hand finger_curls dictionaries', () => {
  const { avatarModel, bonesMap, handRig } = makeRig();
  const player = new SignAnimationPlayer(avatarModel, bonesMap, handRig);
  const playable = {
    signId: 'test_per_hand_curls',
    duration_ms: 1000,
    dominant_hand: 'both',
    return_to_neutral: false,
    involved_bones: [],
    keyframes: [
      { time_ms: 0, rotations: {}, finger_curls: { left: { index: 0 }, right: { thumb: 0 } } },
      { time_ms: 1000, rotations: {}, finger_curls: { left: { index: 60 }, right: { thumb: 40 } } }
    ]
  };

  player.loadSign(playable);
  player.play();
  player.update(1000);

  assert.ok(Math.abs(handRig.left.index[0].rotation.z - (0.2 + THREE.MathUtils.degToRad(60) * 0.75)) < 1e-5);
  assert.ok(Math.abs(handRig.right.thumb[0].rotation.z - (0.1 + THREE.MathUtils.degToRad(40) * 0.75)) < 1e-5);
});


test('SignAnimationPlayer supports co-articulated pose blending across consecutive signs without snapping to zero', () => {
  const { avatarModel, bonesMap, handRig, rightArm } = makeRig();
  const player = new SignAnimationPlayer(avatarModel, bonesMap, handRig);
  rightArm.rotation.z = THREE.MathUtils.degToRad(-60);

  const nextSign = {
    signId: 'test_next',
    duration_ms: 1000,
    dominant_hand: 'right',
    return_to_neutral: true,
    involved_bones: ['mixamorigRightArm'],
    keyframes: [
      { time_ms: 0, rotations: { mixamorigRightArm: { x: 0, y: 0, z: 0 } } },
      { time_ms: 500, rotations: { mixamorigRightArm: { x: 0, y: 0, z: -80 } } },
      { time_ms: 1000, rotations: { mixamorigRightArm: { x: 0, y: 0, z: 0 } } }
    ]
  };

  player.loadSign(nextSign, { blendFromCurrentPose: true, blendMs: 200 });
  // Must NOT immediately reset rightArm to 0 at t=0
  assert.ok(Math.abs(rightArm.rotation.z - THREE.MathUtils.degToRad(-60)) < 1e-5);
  player.play();
  player.update(50);
  assert.ok(rightArm.rotation.z < THREE.MathUtils.degToRad(-30), 'Mid-blend holds smooth non-zero pose');
});
