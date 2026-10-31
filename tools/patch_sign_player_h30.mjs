// tools/patch_sign_player_h30.mjs
import fs from 'fs';
import path from 'path';

const filePath = path.resolve('tools', 'avatar_viewer', 'SignAnimationPlayer.js');
let code = fs.readFileSync(filePath, 'utf8');

const targetLoad = `  loadSign(signData) {
    this.currentSign = signData;
    this.currentTimeMs = 0;
    this.isPlaying = false;
    this.isPaused = false;
    this.resetNeutral();
    if (this.onFrameCallback) this.onFrameCallback(this.getState());
  }`;

const replacementLoad = `  loadSign(signData) {
    this.currentSign = signData;
    this.currentTimeMs = 0;
    this.isPlaying = false;
    this.isPaused = false;
    this._precomputeSign(signData);
    this.resetNeutral();
    if (this.onFrameCallback) this.onFrameCallback(this.getState());
  }

  _precomputeSign(signData) {
    if (!signData || !signData.keyframes) return;
    const kfs = signData.keyframes;
    const DEG2RAD = Math.PI / 180.0;
    for (let i = 0; i < kfs.length - 1; i++) {
      const k0 = kfs[i];
      const k1 = kfs[i + 1];
      if (k0._optimizedBones) continue;

      const bones = Array.from(new Set([
        ...Object.keys(k0.rotations || {}),
        ...Object.keys(k1.rotations || {})
      ]));

      const boneDeltas = [];
      for (let j = 0; j < bones.length; j++) {
        const bName = bones[j];
        const r0 = (k0.rotations && k0.rotations[bName]) || { x: 0, y: 0, z: 0 };
        const r1 = (k1.rotations && k1.rotations[bName]) || { x: 0, y: 0, z: 0 };
        boneDeltas.push({
          name: bName,
          r0x: r0.x * DEG2RAD,
          r0y: r0.y * DEG2RAD,
          r0z: r0.z * DEG2RAD,
          dx: (r1.x - r0.x) * DEG2RAD,
          dy: (r1.y - r0.y) * DEG2RAD,
          dz: (r1.z - r0.z) * DEG2RAD
        });
      }
      k0._optimizedBones = boneDeltas;
    }
  }`;

const targetApply = `    // Interpolate rotational deltas for all involved skeleton bones
    const rotBones = new Set([
      ...Object.keys(k0.rotations || {}),
      ...Object.keys(k1.rotations || {})
    ]);

    rotBones.forEach(bName => {
      const bone = this.bonesMap.get(bName);
      const rest = this.restRotations.get(bName);
      if (!bone || !rest) return;

      const r0 = (k0.rotations && k0.rotations[bName]) || { x: 0, y: 0, z: 0 };
      const r1 = (k1.rotations && k1.rotations[bName]) || { x: 0, y: 0, z: 0 };

      const dx = THREE.MathUtils.degToRad(r0.x + (r1.x - r0.x) * alpha);
      const dy = THREE.MathUtils.degToRad(r0.y + (r1.y - r0.y) * alpha);
      const dz = THREE.MathUtils.degToRad(r0.z + (r1.z - r0.z) * alpha);

      bone.rotation.set(rest.x + dx, rest.y + dy, rest.z + dz);
    });`;

const replacementApply = `    // Interpolate rotational deltas for all involved skeleton bones (H30 Zero-Allocation Fast Path)
    const boneDeltas = k0._optimizedBones;
    if (boneDeltas) {
      for (let j = 0; j < boneDeltas.length; j++) {
        const bd = boneDeltas[j];
        const bone = this.bonesMap.get(bd.name);
        const rest = this.restRotations.get(bd.name);
        if (bone && rest) {
          bone.rotation.set(
            rest.x + bd.r0x + bd.dx * alpha,
            rest.y + bd.r0y + bd.dy * alpha,
            rest.z + bd.r0z + bd.dz * alpha
          );
        }
      }
    } else {
      const rotBones = new Set([
        ...Object.keys(k0.rotations || {}),
        ...Object.keys(k1.rotations || {})
      ]);
      rotBones.forEach(bName => {
        const bone = this.bonesMap.get(bName);
        const rest = this.restRotations.get(bName);
        if (!bone || !rest) return;
        const r0 = (k0.rotations && k0.rotations[bName]) || { x: 0, y: 0, z: 0 };
        const r1 = (k1.rotations && k1.rotations[bName]) || { x: 0, y: 0, z: 0 };
        const dx = THREE.MathUtils.degToRad(r0.x + (r1.x - r0.x) * alpha);
        const dy = THREE.MathUtils.degToRad(r0.y + (r1.y - r0.y) * alpha);
        const dz = THREE.MathUtils.degToRad(r0.z + (r1.z - r0.z) * alpha);
        bone.rotation.set(rest.x + dx, rest.y + dy, rest.z + dz);
      });
    }`;

// Normalize line breaks
const normCode = code.replace(/\r\n/g, '\n');
const normTargetLoad = targetLoad.replace(/\r\n/g, '\n');
const normTargetApply = targetApply.replace(/\r\n/g, '\n');

if (!normCode.includes(normTargetLoad)) {
  console.error('Target load not found!');
  process.exit(1);
}
if (!normCode.includes(normTargetApply)) {
  console.error('Target apply not found!');
  process.exit(1);
}

let patched = normCode.replace(normTargetLoad, replacementLoad);
patched = patched.replace(normTargetApply, replacementApply);

fs.writeFileSync(filePath, patched, 'utf8');
console.log('Successfully patched SignAnimationPlayer.js for H30 fast path!');
