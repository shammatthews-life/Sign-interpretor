import * as THREE from 'three';

const FINGERS = ['thumb', 'index', 'middle', 'ring', 'pinky'];
const SEGMENTS = ['base', 'middle', 'tip'];
const RESTORAGE_KEY = 'aether-r1-technical-poses-v1';
const TO_RAD = Math.PI / 180;

export class ArticulationTestController {
  constructor({ bonesMap, handRig, player, scheduler, model }) {
    this.bonesMap = bonesMap;
    this.handRig = handRig;
    this.player = player;
    this.scheduler = scheduler;
    this.model = model;
    this.rest = new Map([...bonesMap].map(([name, bone]) => [name, {
      rotation: bone.rotation.clone(),
      position: bone.position.clone()
    }]));
  }

  reset() {
    if (this.scheduler) this.scheduler.cancel();
    else this.player.stop();
    this.rest.forEach((pose, name) => {
      const bone = this.bonesMap.get(name);
      if (!bone) return;
      bone.rotation.copy(pose.rotation);
      bone.position.copy(pose.position);
    });
    this.model.updateMatrixWorld(true);
  }

  auditBoneMap() {
    const entries = [];
    for (const side of ['left', 'right']) {
      const prefix = side === 'left' ? 'L' : 'R';
      for (const [name, wristComponent] of [
        [`Bip001_${prefix}_Forearm`, 'forearm'],
        [`Bip001_${prefix}_Hand`, 'hand']
      ]) {
        const bone = this.bonesMap.get(name);
        if (bone) entries.push(this.describeBone(bone, side, null, wristComponent));
      }
      for (const finger of FINGERS) {
        const chain = this.handRig[side][finger] || [];
        chain.forEach((bone, index) => entries.push(
          this.describeBone(bone, side, finger, SEGMENTS[index] || `segment-${index + 1}`)
        ));
      }
    }
    return entries;
  }

  describeBone(bone, side, finger, segment) {
    return {
      runtime_bone_name: bone.name,
      parent: bone.parent?.name || null,
      side,
      finger,
      segment,
      wrist_component: finger ? null : segment,
      available_rotation_axes: ['x', 'y', 'z'].filter(axis => Number.isFinite(bone.rotation[axis]))
    };
  }

  singleJointTests() {
    const tests = [];
    for (const side of ['left', 'right']) {
      const prefix = side === 'left' ? 'L' : 'R';
      const hand = `Bip001_${prefix}_Hand`;
      tests.push(
        { id: `${side}-wrist-flexion`, side, joint: hand, axis: 'x', degrees: 30, expected: 'Hand bone rotates about local X toward flexion.' },
        { id: `${side}-wrist-extension`, side, joint: hand, axis: 'x', degrees: -30, expected: 'Hand bone rotates about local X toward extension.' },
        { id: `${side}-wrist-rotation`, side, joint: hand, axis: 'y', degrees: 30, expected: 'Hand bone rotates about local Y.' }
      );
      for (const finger of FINGERS) {
        (this.handRig[side][finger] || []).forEach((bone, index) => {
          tests.push({
            id: `${side}-${finger}-${SEGMENTS[index] || `segment-${index + 1}`}`,
            side, finger, segment: SEGMENTS[index] || `segment-${index + 1}`,
            joint: bone.name, axis: 'z', degrees: 30,
            expected: `${finger} ${SEGMENTS[index] || `segment ${index + 1}`} rotates about local Z.`
          });
        });
      }
    }
    return tests;
  }

  applySingleJoint(testId) {
    const test = this.singleJointTests().find(item => item.id === testId);
    if (!test) throw new Error(`Unknown articulation test: ${testId}`);
    this.reset();
    const bone = this.bonesMap.get(test.joint);
    const rest = this.rest.get(test.joint);
    if (!bone || !rest) throw new Error(`Required runtime bone is unavailable: ${test.joint}`);
    const before = this.descendantPositions(bone);
    bone.rotation[test.axis] = rest.rotation[test.axis] + test.degrees * TO_RAD;
    this.model.updateMatrixWorld(true);
    const after = this.descendantPositions(bone);
    return {
      ...test,
      observed_rotation_degrees: (bone.rotation[test.axis] - rest.rotation[test.axis]) / TO_RAD,
      descendant_displacement: this.positionDisplacement(before, after)
    };
  }

  poseDefinitions() {
    const rotationsFor = (predicate, axis = 'z', degrees = -25) => {
      const rotations = {};
      for (const side of ['left', 'right']) {
        for (const finger of FINGERS) {
          (this.handRig[side][finger] || []).forEach((bone, index) => {
            const amount = predicate(side, finger, index);
            if (amount !== null) rotations[bone.name] = { x: 0, y: 0, z: 0, [axis]: amount };
          });
        }
      }
      return rotations;
    };
    const all = value => rotationsFor(() => value);
    return {
      neutral: { label: 'Neutral hand', rotations: {} },
      all_fingers_extended: { label: 'All fingers extended', rotations: all(-25) },
      partially_curled: { label: 'All fingers partially curled', rotations: all(25) },
      fist: { label: 'Fist technical pose', rotations: all(55) },
      thumb_index_isolated: {
        label: 'Thumb/index isolated',
        rotations: rotationsFor((side, finger) => ['thumb', 'index'].includes(finger) ? -20 : 45)
      },
      open_palm: { label: 'Open palm technical pose', rotations: all(-30) },
      wrist_flexed: { label: 'Wrist flexed', rotations: { Bip001_R_Hand: { x: 30, y: 0, z: 0 } } },
      wrist_extended: { label: 'Wrist extended', rotations: { Bip001_R_Hand: { x: -30, y: 0, z: 0 } } },
      wrist_rotated: { label: 'Wrist rotated', rotations: { Bip001_R_Hand: { x: 0, y: 30, z: 0 } } },
      asymmetric_fingers: {
        label: 'Asymmetric finger test',
        rotations: rotationsFor((side, finger, index) => {
          if (side === 'right' && finger === 'index') return 30;
          if (side === 'right' && finger === 'middle') return -20;
          if (side === 'left' && finger === 'ring') return 30;
          return null;
        })
      }
    };
  }

  applyPose(poseId) {
    const pose = this.poseDefinitions()[poseId];
    if (!pose) throw new Error(`Unknown technical pose: ${poseId}`);
    this.reset();
    this.applyRotations(pose.rotations);
    return { pose_id: poseId, label: pose.label, rotation_count: Object.keys(pose.rotations).length };
  }

  savePose(name) {
    const key = String(name).trim();
    if (!key) throw new Error('Enter a name for the technical pose.');
    const rotations = {};
    for (const [name, bone] of this.bonesMap) {
      const rest = this.rest.get(name);
      if (!rest) continue;
      const delta = {
        x: (bone.rotation.x - rest.rotation.x) / TO_RAD,
        y: (bone.rotation.y - rest.rotation.y) / TO_RAD,
        z: (bone.rotation.z - rest.rotation.z) / TO_RAD
      };
      if (Math.abs(delta.x) + Math.abs(delta.y) + Math.abs(delta.z) > 0.001) rotations[name] = delta;
    }
    const store = JSON.parse(localStorage.getItem(RESTORAGE_KEY) || '{}');
    store[key] = {
      schema: 'aether-r1-technical-pose/1.0',
      label: 'Saved technical articulation pose',
      rotations_degrees: rotations,
      saved_at: new Date().toISOString()
    };
    localStorage.setItem(RESTORAGE_KEY, JSON.stringify(store));
    return key;
  }

  replaySavedPose(name, speed = 1) {
    const store = JSON.parse(localStorage.getItem(RESTORAGE_KEY) || '{}');
    const pose = store[String(name).trim()];
    if (!pose) throw new Error(`No saved technical pose named "${name}".`);
    return this.playPose(pose.rotations_degrees, speed, pose.label);
  }

  runAutomatedSuite() {
    const jointResults = this.singleJointTests().map(test => {
      const result = this.applySingleJoint(test.id);
      const rotationPassed = Math.abs(result.observed_rotation_degrees - test.degrees) < 1e-5;
      const movementPassed = result.descendant_displacement !== null && result.descendant_displacement > 1e-5;
      return {
        id: test.id,
        expected: test.expected,
        observed: `${result.observed_rotation_degrees.toFixed(1)}° local ${test.axis.toUpperCase()}`,
        status: rotationPassed && movementPassed ? 'PASS' : 'FAIL',
        descendant_displacement: result.descendant_displacement
      };
    });

    const poseResults = Object.entries(this.poseDefinitions()).map(([id, pose]) => {
      this.reset();
      this.applyRotations(pose.rotations);
      const passed = Object.entries(pose.rotations).every(([name, expected]) => {
        const bone = this.bonesMap.get(name);
        const rest = this.rest.get(name);
        return bone && rest && ['x', 'y', 'z'].every(axis =>
          Math.abs((bone.rotation[axis] - rest.rotation[axis]) / TO_RAD - (expected[axis] || 0)) < 1e-5
        );
      });
      return { id, label: pose.label, articulated_joints: Object.keys(pose.rotations).length, status: passed ? 'PASS' : 'FAIL' };
    });

    const restPlaybackSpeed = this.player.playbackSpeed;
    const speedResults = [];
    const replayPose = {
      ...this.poseDefinitions().asymmetric_fingers.rotations,
      Bip001_R_Hand: { x: 0, y: 30, z: 0 }
    };
    for (const speed of [0.5, 1, 1.25, 1.5]) {
      let maxResetDrift = 0;
      let midPoseObserved = false;
      for (let replay = 0; replay < 3; replay++) {
        this.playPose(replayPose, speed, 'R1 repeated replay test');
        this.player.seek(750);
        const hand = this.bonesMap.get('Bip001_R_Hand');
        const handRest = this.rest.get('Bip001_R_Hand');
        midPoseObserved ||= Math.abs(hand.rotation.y - handRest.rotation.y) > 1e-5;
        this.player.update(750 / speed);
        maxResetDrift = Math.max(maxResetDrift, this.measureResetDrift());
      }
      speedResults.push({
        speed,
        repeats: 3,
        mid_pose_observed: midPoseObserved,
        max_reset_drift_radians: maxResetDrift,
        status: midPoseObserved && maxResetDrift < 1e-7 ? 'PASS' : 'FAIL'
      });
    }
    this.player.playbackSpeed = restPlaybackSpeed;
    this.reset();
    return {
      isolated_joints: jointResults,
      poses: poseResults,
      replay_speeds: speedResults,
      hac: (() => {
        const testedJointIds = [...new Set(jointResults.filter(result => result.status === 'PASS')
          .map(result => result.id.replace(/-(wrist-flexion|wrist-extension|wrist-rotation)$/, '-wrist')))].sort();
        return { tested_joint_ids: testedJointIds, numerator: testedJointIds.length, denominator: 32 };
      })(),
      preexisting_non_finite_rest_components: this.countNonFiniteRestComponents()
    };
  }

  measureResetDrift() {
    let maxDrift = 0;
    for (const [name, bone] of this.bonesMap) {
      const rest = this.rest.get(name);
      if (!rest) continue;
      for (const axis of ['x', 'y', 'z']) {
        for (const [current, original] of [
          [bone.rotation[axis], rest.rotation[axis]],
          [bone.position[axis], rest.position[axis]]
        ]) {
          if (Number.isFinite(original)) {
            if (!Number.isFinite(current)) return Infinity;
            maxDrift = Math.max(maxDrift, Math.abs(current - original));
          }
        }
      }
    }
    return maxDrift;
  }

  countNonFiniteRestComponents() {
    let count = 0;
    for (const pose of this.rest.values()) {
      for (const axis of ['x', 'y', 'z']) {
        if (!Number.isFinite(pose.rotation[axis])) count++;
        if (!Number.isFinite(pose.position[axis])) count++;
      }
    }
    return count;
  }

  playPose(rotations, speed = 1, label = 'Technical pose replay') {
    if (![0.5, 1, 1.25, 1.5].includes(Number(speed))) throw new Error('Unsupported articulation test speed.');
    this.scheduler?.cancel();
    this.player.playbackSpeed = Number(speed);
    const involved = Object.keys(rotations);
    this.player.loop = false;
    this.player.loadSign({
      status: 'playable',
      duration_ms: 1500,
      dominant_hand: 'right',
      return_to_neutral: true,
      involved_bones: involved,
      keyframes: [
        { time_ms: 0, label: 'Technical neutral', easing: 'linear', rotations: {} },
        { time_ms: 500, label, easing: 'linear', rotations },
        { time_ms: 1000, label, easing: 'linear', rotations },
        { time_ms: 1500, label: 'Technical neutral reset', easing: 'linear', rotations: {} }
      ]
    });
    this.player.play();
    return { label, speed: Number(speed), duration_ms: 1500, articulated_bones: involved.length };
  }

  applyRotations(rotations) {
    for (const [name, delta] of Object.entries(rotations)) {
      const bone = this.bonesMap.get(name);
      const rest = this.rest.get(name);
      if (!bone || !rest) throw new Error(`Required runtime bone is unavailable: ${name}`);
      bone.rotation.set(
        rest.rotation.x + (delta.x || 0) * TO_RAD,
        rest.rotation.y + (delta.y || 0) * TO_RAD,
        rest.rotation.z + (delta.z || 0) * TO_RAD
      );
    }
    this.model.updateMatrixWorld(true);
  }

  descendantPositions(bone) {
    this.model.updateMatrixWorld(true);
    const points = [];
    bone.traverse(child => {
      if (child.isBone && child !== bone) {
        const position = child.getWorldPosition(new THREE.Vector3());
        points.push(position.toArray());
      }
    });
    return points;
  }

  positionDisplacement(before, after) {
    const count = Math.min(before.length, after.length);
    if (!count) return null;
    let sum = 0;
    for (let i = 0; i < count; i++) {
      sum += Math.hypot(...before[i].map((value, axis) => after[i][axis] - value));
    }
    return sum / count;
  }
}
