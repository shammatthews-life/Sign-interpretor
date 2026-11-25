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

    if (this.avatarModel) {
      this.avatarModel.traverse(c => {
        if (c.isBone) {
          this.restRotations.set(c.name, c.rotation.clone());
          this.restPositions.set(c.name, c.position.clone());
        }
      });
    }
  }

  loadSign(signData) {
    this.currentSign = signData;
    this.currentTimeMs = 0;
    this.isPlaying = false;
    this.isPaused = false;
    this.resetNeutral();
    if (this.onFrameCallback) this.onFrameCallback(this.getState());
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

    // Interpolate rotational deltas for all involved skeleton bones
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

    // Legacy finger curls remain a fallback; explicit per-joint rotations win.
    const domSide = this.currentSign.dominant_hand || 'right';
    const c0 = k0.finger_curls || {};
    const c1 = k1.finger_curls || {};

    ['thumb', 'index', 'middle', 'ring', 'pinky'].forEach(f => {
      const val0 = c0[f] !== undefined ? c0[f] : 0;
      const val1 = c1[f] !== undefined ? c1[f] : 0;
      const curlDeg = val0 + (val1 - val0) * alpha;

      const chain = this.handRig && this.handRig[domSide] ? this.handRig[domSide][f] : null;
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
  }
}
