/**
 * SignAnimationPlayer.js
 * Reusable animation engine for Indian Sign Language (ISL) 3D avatar gestures.
 *
 * Features:
 * - Loads machine-readable JSON sign motion definitions
 * - Smooth keyframe interpolation with standard easing curves
 * - Delta-based rotation offsets relative to bind pose (guaranteeing ZERO drift)
 * - Safe rest pose restoration
 * - Real-time scrubbing, pause, play, loop, and speed controls
 */

import * as THREE from 'three';

export const Easing = {
  linear: t => t,
  easeInOutQuad: t => t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2,
  easeOutQuad: t => 1 - (1 - t) * (1 - t),
  easeOutCubic: t => 1 - Math.pow(1 - t, 3),
  easeInOutCubic: t => t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2
};

export class SignAnimationPlayer {
  constructor(avatarModel, bonesMap, handRig) {
    this.avatarModel = avatarModel;
    this.bonesMap = bonesMap;
    this.handRig = handRig;

    this.currentSign = null;
    this.currentTimeMs = 0;
    this.isPlaying = false;
    this.isPaused = false;
    this.loop = false;
    this.playbackSpeed = 1.0;

    this.onFrameCallback = null;
    this.onCompleteCallback = null;

    // Cache initial bind pose rotations and positions for safe restoration
    this.restRotations = new Map();
    this.restPositions = new Map();
    this._entryPoseSnapshot = null;
    this._entryBlendMs = 0;

    if (this.avatarModel) {
      this.avatarModel.traverse(c => {
        if (c.isBone) {
          this.restRotations.set(c.name, c.rotation.clone());
          this.restPositions.set(c.name, c.position.clone());
        }
      });
    }
  }

  _capturePoseSnapshot() {
    const snap = new Map();
    if (!this.bonesMap) return snap;
    this.bonesMap.forEach((bone, name) => {
      const rest = this.restRotations.get(name);
      if (!rest || !bone?.rotation) return;
      const dx = bone.rotation.x - rest.x;
      const dy = bone.rotation.y - rest.y;
      const dz = bone.rotation.z - rest.z;
      if (Math.abs(dx) > 1e-4 || Math.abs(dy) > 1e-4 || Math.abs(dz) > 1e-4) {
        snap.set(name, { dx, dy, dz });
      }
    });
    return snap;
  }

  loadSign(signData, options = {}) {
    const blend = Boolean(options && options.blendFromCurrentPose);
    this._entryPoseSnapshot = blend ? this._capturePoseSnapshot() : null;
    const hintMs = Number(options?.blendMs ?? signData?.transition_hints?.recommended_blend_ms ?? 160);
    const durMs = Number(signData?.duration_ms ?? 1000);
    this._entryBlendMs = (blend && this._entryPoseSnapshot.size > 0 && Number.isFinite(hintMs) && hintMs > 0)
      ? Math.min(hintMs, durMs * 0.3)
      : 0;

    this.currentSign = signData;
    this.currentTimeMs = 0;
    this.isPlaying = false;
    this.isPaused = false;
    this._nonManualMarkers = Array.isArray(options?.nonManualMarkers) ? options.nonManualMarkers : [];
    this._spatialYawDeg = Number.isFinite(options?.spatialYawDeg) ? options.spatialYawDeg : 0;
    this._precomputeSign(signData);
    if (!blend) {
      this.resetNeutral();
    }
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
  }

  play() {
    if (!this.currentSign) return;
    if (this.currentTimeMs >= this.currentSign.duration_ms) {
      this.currentTimeMs = 0;
    }
    this.isPlaying = true;
    this.isPaused = false;
  }

  pause() {
    this.isPlaying = false;
    this.isPaused = true;
  }

  stop() {
    this.isPlaying = false;
    this.isPaused = false;
    this.currentTimeMs = 0;
    this.resetNeutral();
    if (this.onFrameCallback) this.onFrameCallback(this.getState());
  }

  replay() {
    this.stop();
    this.play();
  }

  seek(timeMs) {
    if (!this.currentSign) return;
    this.currentTimeMs = Math.max(0, Math.min(timeMs, this.currentSign.duration_ms));
    this.applyFrame(this.currentTimeMs);
    if (this.onFrameCallback) this.onFrameCallback(this.getState());
  }

  resetNeutral() {
    if (!this.currentSign) return;

    // Reset involved bones
    const bonesToReset = this.currentSign.involved_bones || [];
    bonesToReset.forEach(bName => {
      const bone = this.bonesMap.get(bName);
      const rest = this.restRotations.get(bName);
      if (bone && rest) {
        bone.rotation.copy(rest);
      }
    });

    // Reset fingers of dominant hand and secondary hand
    ['left', 'right'].forEach(side => {
      if (this.handRig && this.handRig[side]) {
        ['thumb', 'index', 'middle', 'ring', 'pinky'].forEach(f => {
          const chain = this.handRig[side][f];
          if (chain) {
            chain.forEach(b => {
              const rest = this.restRotations.get(b.name);
              if (rest) b.rotation.copy(rest);
            });
          }
        });
      }
    });
  }

  getState() {
    const dur = this.currentSign ? this.currentSign.duration_ms : 0;
    const progress = dur > 0 ? this.currentTimeMs / dur : 0;
    return {
      isPlaying: this.isPlaying,
      isPaused: this.isPaused,
      currentTimeMs: this.currentTimeMs,
      durationMs: dur,
      progress: progress,
      signName: this.currentSign ? this.currentSign.gloss : 'None',
      activeKeyframe: this.getActiveKeyframeLabel(),
      keyframeIndex: this.getActiveKeyframeIndex(),
      totalKeyframes: this.currentSign && this.currentSign.keyframes ? this.currentSign.keyframes.length : 0
    };
  }

  getActiveKeyframeIndex() {
    if (!this.currentSign || !this.currentSign.keyframes) return 0;
    const kfs = this.currentSign.keyframes;
    for (let i = kfs.length - 1; i >= 0; i--) {
      if (this.currentTimeMs >= kfs[i].time_ms) {
        return i;
      }
    }
    return 0;
  }

  getActiveKeyframeLabel() {
    if (!this.currentSign || !this.currentSign.keyframes) return 'Neutral Rest Pose';
    const kfs = this.currentSign.keyframes;
    const idx = this.getActiveKeyframeIndex();
    return kfs[idx].label;
  }

  update(deltaMs) {
    if (!this.isPlaying || !this.currentSign) return;

    this.currentTimeMs += deltaMs * this.playbackSpeed;

    if (this.currentTimeMs >= this.currentSign.duration_ms) {
      if (this.loop) {
        this.currentTimeMs = this.currentTimeMs % this.currentSign.duration_ms;
      } else {
        this.currentTimeMs = this.currentSign.duration_ms;
        this.applyFrame(this.currentTimeMs);
        this.isPlaying = false;
        if (this.onCompleteCallback) this.onCompleteCallback();
        if (this.onFrameCallback) this.onFrameCallback(this.getState());
        return;
      }
    }

    this.applyFrame(this.currentTimeMs);
    if (this.onFrameCallback) this.onFrameCallback(this.getState());
  }

  applyFrame(timeMs) {
    if (!this.currentSign || !this.currentSign.keyframes) return;
    const kfs = this.currentSign.keyframes;
    if (kfs.length === 0) return;

    // Locate segment between k0 and k1
    let k0 = kfs[0];
    let k1 = kfs[kfs.length - 1];

    for (let i = 0; i < kfs.length - 1; i++) {
      if (timeMs >= kfs[i].time_ms && timeMs <= kfs[i + 1].time_ms) {
        k0 = kfs[i];
        k1 = kfs[i + 1];
        break;
      }
    }

    const span = k1.time_ms - k0.time_ms;
    const rawAlpha = span > 0 ? (timeMs - k0.time_ms) / span : 1.0;
    const easeFn = Easing[k0.easing] || Easing.easeInOutQuad;
    const alpha = easeFn(Math.max(0, Math.min(1.0, rawAlpha)));

    // Interpolate rotational deltas for all involved skeleton bones (H30 Zero-Allocation Fast Path)
    const boneDeltas = k0._optimizedBones;
    const entryBlendActive = Boolean(this._entryPoseSnapshot && this._entryBlendMs > 0 && timeMs < this._entryBlendMs);
    const entryWeight = entryBlendActive
      ? (1.0 - Easing.easeInOutQuad(Math.max(0, Math.min(1.0, timeMs / this._entryBlendMs))))
      : 0.0;
    const appliedBones = entryBlendActive ? new Set() : null;

    if (boneDeltas) {
      for (let j = 0; j < boneDeltas.length; j++) {
        const bd = boneDeltas[j];
        const bone = this.bonesMap.get(bd.name);
        const rest = this.restRotations.get(bd.name);
        if (bone && rest) {
          let tx = bd.r0x + bd.dx * alpha;
          let ty = bd.r0y + bd.dy * alpha;
          let tz = bd.r0z + bd.dz * alpha;
          if (entryBlendActive) {
            appliedBones.add(bd.name);
            const prev = this._entryPoseSnapshot.get(bd.name) || { dx: 0, dy: 0, dz: 0 };
            tx = prev.dx * entryWeight + tx * (1 - entryWeight);
            ty = prev.dy * entryWeight + ty * (1 - entryWeight);
            tz = prev.dz * entryWeight + tz * (1 - entryWeight);
          }
          bone.rotation.set(rest.x + tx, rest.y + ty, rest.z + tz);
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
        let dx = THREE.MathUtils.degToRad(r0.x + (r1.x - r0.x) * alpha);
        let dy = THREE.MathUtils.degToRad(r0.y + (r1.y - r0.y) * alpha);
        let dz = THREE.MathUtils.degToRad(r0.z + (r1.z - r0.z) * alpha);
        if (entryBlendActive) {
          appliedBones.add(bName);
          const prev = this._entryPoseSnapshot.get(bName) || { dx: 0, dy: 0, dz: 0 };
          dx = prev.dx * entryWeight + dx * (1 - entryWeight);
          dy = prev.dy * entryWeight + dy * (1 - entryWeight);
          dz = prev.dz * entryWeight + dz * (1 - entryWeight);
        }
        bone.rotation.set(rest.x + dx, rest.y + dy, rest.z + dz);
      });
    }

    if (entryBlendActive) {
      this._entryPoseSnapshot.forEach((prev, bName) => {
        if (appliedBones.has(bName)) return;
        const bone = this.bonesMap.get(bName);
        const rest = this.restRotations.get(bName);
        if (bone && rest) {
          bone.rotation.set(
            rest.x + prev.dx * entryWeight,
            rest.y + prev.dy * entryWeight,
            rest.z + prev.dz * entryWeight
          );
        }
      });
    }

    // Legacy finger curls remain a fallback; explicit per-joint rotations win.
    const domSide = this.currentSign.dominant_hand || 'right';
    const targetSides = domSide === 'both' ? ['left', 'right'] : [domSide];
    const c0 = k0.finger_curls || {};
    const c1 = k1.finger_curls || {};

    targetSides.forEach(side => {
      const sideRig = this.handRig && this.handRig[side] ? this.handRig[side] : null;
      if (!sideRig) return;
      const sideC0 = (c0[side] && typeof c0[side] === 'object') ? c0[side] : c0;
      const sideC1 = (c1[side] && typeof c1[side] === 'object') ? c1[side] : c1;

      ['thumb', 'index', 'middle', 'ring', 'pinky'].forEach(f => {
        const val0 = Number.isFinite(sideC0[f]) ? sideC0[f] : 0;
        const val1 = Number.isFinite(sideC1[f]) ? sideC1[f] : 0;
        const curlDeg = val0 + (val1 - val0) * alpha;

        const chain = sideRig[f] || null;
        if (chain) {
          const rad = THREE.MathUtils.degToRad(curlDeg);
          chain.forEach((b, idx) => {
            const explicitlyKeyframed = Boolean(
              (k0.rotations && Object.prototype.hasOwnProperty.call(k0.rotations, b.name))
              || (k1.rotations && Object.prototype.hasOwnProperty.call(k1.rotations, b.name))
            );
            if (explicitlyKeyframed) return;
            const rest = this.restRotations.get(b.name);
            if (rest) {
              const factor = idx === 0 ? 0.75 : 1.0;
              b.rotation.z = rest.z + (rad * factor);
            }
          });
        }
      });
    });

    this._applyNonManualAndSpatialOverlays(timeMs, this.currentSign.duration_ms || 1000, appliedBones);
  }

  _applyNonManualAndSpatialOverlays(timeMs, durationMs, appliedBones = null) {
    const markers = this._nonManualMarkers || [];
    const spatialYawDeg = this._spatialYawDeg || 0;
    if (markers.length === 0 && spatialYawDeg === 0) return;

    const progress = Math.max(0, Math.min(1.0, durationMs > 0 ? timeMs / durationMs : 0.5));
    const env = Math.sin(Math.PI * progress);

    let headDx = 0;
    let headDy = 0;
    let headDz = 0;
    let spineDx = 0;
    let spineDy = 0;
    let armDy = 0;

    if (markers.includes('NMM-NEG-HEADSHAKE') || markers.includes('NEGATION')) {
      headDy += THREE.MathUtils.degToRad(10 * Math.sin(progress * Math.PI * 4) * (0.4 + 0.6 * env));
      headDx += THREE.MathUtils.degToRad(2 * env);
    }
    if (markers.includes('NMM-WH-BROW-FURROW') || markers.includes('WH_QUESTION')) {
      headDx += THREE.MathUtils.degToRad(6.5 * env);
      headDz += THREE.MathUtils.degToRad(4.0 * env);
      spineDx += THREE.MathUtils.degToRad(2.5 * env);
    }
    if (markers.includes('NMM-YESNO-BROW-RAISE') || markers.includes('NMM-COND-BROW-RAISE') || markers.includes('YES_NO_QUESTION')) {
      headDx += THREE.MathUtils.degToRad(-5.5 * env);
      spineDx += THREE.MathUtils.degToRad(3.0 * env);
    }
    if (markers.includes('NMM-EMPHATIC-NOD')) {
      headDx += THREE.MathUtils.degToRad(6.0 * Math.abs(Math.sin(progress * Math.PI * 2)));
    }
    if (spatialYawDeg !== 0) {
      spineDy += THREE.MathUtils.degToRad(spatialYawDeg * env);
      headDy += THREE.MathUtils.degToRad(spatialYawDeg * 0.55 * env);
      armDy += THREE.MathUtils.degToRad(spatialYawDeg * 0.45 * env);
    }

    const addOverlay = (boneName, dx, dy, dz) => {
      if (dx === 0 && dy === 0 && dz === 0) return;
      const bone = this.bonesMap.get(boneName);
      const rest = this.restRotations.get(boneName);
      if (!bone || !rest) return;
      const k0 = this.currentSign?.keyframes?.[0];
      const hasKeyframe = Boolean(
        (appliedBones && appliedBones.has(boneName)) ||
        (k0 && ((k0.rotations && k0.rotations[boneName]) || (k0._optimizedBones && k0._optimizedBones.some(b => b.name === boneName))))
      );
      if (hasKeyframe) {
        bone.rotation.set(bone.rotation.x + dx, bone.rotation.y + dy, bone.rotation.z + dz);
      } else {
        bone.rotation.set(rest.x + dx, rest.y + dy, rest.z + dz);
      }
    };

    addOverlay('Bip001_Head', headDx, headDy, headDz);
    addOverlay('Bip001_Spine1', spineDx, spineDy, 0);
    addOverlay('Bip001_R_UpperArm', 0, armDy, 0);
  }
}
