/**
 * H46 Duplicate Sign Trajectory & Handshape Repair Script
 * Eliminates all 13 exact rotation-duplicate groups (33 signs) by assigning
 * distinct, anatomically valid, ISLRTC-grounded 3D keyframes and finger curls.
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '..');
const SIGNS_DIR = path.join(ROOT, 'signs');

function makeNeutralFrame(bones, curls) {
  const rotations = {};
  for (const b of bones) rotations[b] = { x: 0, y: 0, z: 0 };
  return {
    time_ms: 0,
    label: 'Neutral',
    easing: 'easeInOutQuad',
    rotations,
    finger_curls: { ...curls }
  };
}

function buildKeyframes(durationMs, bones, approach, peak, holdOrFollow, curlsApproach, curlsPeak) {
  const neutralCurls = { thumb: 0, index: 0, middle: 0, ring: 0, pinky: 0 };
  const t1 = Math.round(durationMs * 0.25);
  const t2 = Math.round(durationMs * 0.50);
  const t3 = Math.round(durationMs * 0.75);
  return [
    makeNeutralFrame(bones, neutralCurls),
    { time_ms: t1, label: 'Approach', easing: 'easeInOutQuad', rotations: approach, finger_curls: curlsApproach },
    { time_ms: t2, label: 'Articulation Peak', easing: 'easeInOutQuad', rotations: peak, finger_curls: curlsPeak },
    { time_ms: t3, label: 'Follow-Through', easing: 'easeInOutQuad', rotations: holdOrFollow, finger_curls: curlsPeak },
    { ...makeNeutralFrame(bones, neutralCurls), time_ms: durationMs, label: 'Return Neutral' }
  ];
}

const REPAIRS = {
  hold: {
    duration_ms: 1100,
    notes: 'H46 distinct trajectory: firm two-hand/dominant chest grasp with closed grip.',
    bones: ['Bip001_R_Clavicle', 'Bip001_R_UpperArm', 'Bip001_R_Forearm', 'Bip001_R_Hand', 'Bip001_L_UpperArm', 'Bip001_L_Forearm'],
    approach: { Bip001_R_Clavicle: { x: 0, y: 5, z: -3 }, Bip001_R_UpperArm: { x: 24, y: 18, z: -48 }, Bip001_R_Forearm: { x: 0, y: -30, z: -78 }, Bip001_R_Hand: { x: 8, y: -12, z: 4 }, Bip001_L_UpperArm: { x: 22, y: -16, z: 44 }, Bip001_L_Forearm: { x: 0, y: 26, z: 74 } },
    peak: { Bip001_R_Clavicle: { x: 0, y: 8, z: -4 }, Bip001_R_UpperArm: { x: 30, y: 26, z: -42 }, Bip001_R_Forearm: { x: 4, y: -38, z: -86 }, Bip001_R_Hand: { x: 14, y: -18, z: 8 }, Bip001_L_UpperArm: { x: 28, y: -24, z: 38 }, Bip001_L_Forearm: { x: 4, y: 34, z: 82 } },
    follow: { Bip001_R_Clavicle: { x: 0, y: 7, z: -3 }, Bip001_R_UpperArm: { x: 28, y: 24, z: -44 }, Bip001_R_Forearm: { x: 2, y: -36, z: -84 }, Bip001_R_Hand: { x: 12, y: -16, z: 6 }, Bip001_L_UpperArm: { x: 26, y: -22, z: 40 }, Bip001_L_Forearm: { x: 2, y: 32, z: 80 } },
    curlsA: { thumb: 0.4, index: 0.5, middle: 0.5, ring: 0.5, pinky: 0.5 },
    curlsP: { thumb: 0.75, index: 0.85, middle: 0.85, ring: 0.85, pinky: 0.85 }
  },
  minute: {
    duration_ms: 950,
    notes: 'H46 distinct trajectory: upright index finger ticking forward at wrist level.',
    bones: ['Bip001_R_Clavicle', 'Bip001_R_UpperArm', 'Bip001_R_Forearm', 'Bip001_R_Hand'],
    approach: { Bip001_R_Clavicle: { x: 0, y: 3, z: -2 }, Bip001_R_UpperArm: { x: 18, y: 14, z: -56 }, Bip001_R_Forearm: { x: 0, y: -22, z: -92 }, Bip001_R_Hand: { x: -10, y: 0, z: 12 } },
    peak: { Bip001_R_Clavicle: { x: 0, y: 4, z: -2 }, Bip001_R_UpperArm: { x: 20, y: 18, z: -54 }, Bip001_R_Forearm: { x: 0, y: -24, z: -95 }, Bip001_R_Hand: { x: 16, y: 6, z: 14 } },
    follow: { Bip001_R_Clavicle: { x: 0, y: 4, z: -2 }, Bip001_R_UpperArm: { x: 18, y: 16, z: -56 }, Bip001_R_Forearm: { x: 0, y: -22, z: -92 }, Bip001_R_Hand: { x: -6, y: 2, z: 10 } },
    curlsA: { thumb: 0.7, index: 0.0, middle: 0.85, ring: 0.85, pinky: 0.85 },
    curlsP: { thumb: 0.75, index: 0.0, middle: 0.9, ring: 0.9, pinky: 0.9 }
  },
  keep: {
    duration_ms: 1050,
    notes: 'H46 distinct trajectory: steady cupped downward hold.',
    bones: ['Bip001_R_Clavicle', 'Bip001_R_UpperArm', 'Bip001_R_Forearm', 'Bip001_R_Hand'],
    approach: { Bip001_R_Clavicle: { x: 0, y: 4, z: -2 }, Bip001_R_UpperArm: { x: 22, y: 12, z: -42 }, Bip001_R_Forearm: { x: 0, y: -28, z: -72 }, Bip001_R_Hand: { x: 18, y: -8, z: -6 } },
    peak: { Bip001_R_Clavicle: { x: 0, y: 5, z: -3 }, Bip001_R_UpperArm: { x: 26, y: 14, z: -36 }, Bip001_R_Forearm: { x: 0, y: -32, z: -66 }, Bip001_R_Hand: { x: 24, y: -10, z: -10 } },
    follow: { Bip001_R_Clavicle: { x: 0, y: 5, z: -3 }, Bip001_R_UpperArm: { x: 24, y: 13, z: -38 }, Bip001_R_Forearm: { x: 0, y: -30, z: -68 }, Bip001_R_Hand: { x: 20, y: -8, z: -8 } },
    curlsA: { thumb: 0.25, index: 0.4, middle: 0.4, ring: 0.4, pinky: 0.4 },
    curlsP: { thumb: 0.35, index: 0.45, middle: 0.45, ring: 0.45, pinky: 0.45 }
  },
  long: {
    duration_ms: 1150,
    notes: 'H46 distinct trajectory: right index tracing upward along left forearm.',
    bones: ['Bip001_R_Clavicle', 'Bip001_R_UpperArm', 'Bip001_R_Forearm', 'Bip001_R_Hand', 'Bip001_L_UpperArm', 'Bip001_L_Forearm'],
    approach: { Bip001_R_Clavicle: { x: 0, y: 6, z: -2 }, Bip001_R_UpperArm: { x: 16, y: 24, z: -48 }, Bip001_R_Forearm: { x: 0, y: -34, z: -82 }, Bip001_R_Hand: { x: 4, y: -12, z: 6 }, Bip001_L_UpperArm: { x: 24, y: -14, z: 48 }, Bip001_L_Forearm: { x: 0, y: 18, z: 78 } },
    peak: { Bip001_R_Clavicle: { x: 0, y: 8, z: -4 }, Bip001_R_UpperArm: { x: 28, y: 10, z: -62 }, Bip001_R_Forearm: { x: 0, y: -18, z: -96 }, Bip001_R_Hand: { x: 6, y: -4, z: 10 }, Bip001_L_UpperArm: { x: 24, y: -14, z: 48 }, Bip001_L_Forearm: { x: 0, y: 18, z: 78 } },
    follow: { Bip001_R_Clavicle: { x: 0, y: 7, z: -3 }, Bip001_R_UpperArm: { x: 30, y: 6, z: -66 }, Bip001_R_Forearm: { x: 0, y: -14, z: -98 }, Bip001_R_Hand: { x: 4, y: -2, z: 12 }, Bip001_L_UpperArm: { x: 22, y: -12, z: 46 }, Bip001_L_Forearm: { x: 0, y: 16, z: 76 } },
    curlsA: { thumb: 0.7, index: 0.0, middle: 0.85, ring: 0.85, pinky: 0.85 },
    curlsP: { thumb: 0.75, index: 0.0, middle: 0.9, ring: 0.9, pinky: 0.9 }
  },
  new: {
    duration_ms: 1000,
    notes: 'H46 distinct trajectory: sweeping curved palm forward and upward.',
    bones: ['Bip001_R_Clavicle', 'Bip001_R_UpperArm', 'Bip001_R_Forearm', 'Bip001_R_Hand'],
    approach: { Bip001_R_Clavicle: { x: 0, y: 2, z: -2 }, Bip001_R_UpperArm: { x: 14, y: -10, z: -42 }, Bip001_R_Forearm: { x: 0, y: -18, z: -76 }, Bip001_R_Hand: { x: 12, y: 10, z: -8 } },
    peak: { Bip001_R_Clavicle: { x: 0, y: 8, z: -4 }, Bip001_R_UpperArm: { x: 34, y: 16, z: -60 }, Bip001_R_Forearm: { x: 0, y: -8, z: -64 }, Bip001_R_Hand: { x: -16, y: 16, z: 12 } },
    follow: { Bip001_R_Clavicle: { x: 0, y: 6, z: -3 }, Bip001_R_UpperArm: { x: 38, y: 20, z: -56 }, Bip001_R_Forearm: { x: 0, y: -6, z: -58 }, Bip001_R_Hand: { x: -12, y: 14, z: 10 } },
    curlsA: { thumb: 0.15, index: 0.2, middle: 0.2, ring: 0.2, pinky: 0.2 },
    curlsP: { thumb: 0.1, index: 0.15, middle: 0.15, ring: 0.15, pinky: 0.15 }
  },
  next: {
    duration_ms: 950,
    notes: 'H46 distinct trajectory: arched flat hand hopping forward across neutral space.',
    bones: ['Bip001_R_Clavicle', 'Bip001_R_UpperArm', 'Bip001_R_Forearm', 'Bip001_R_Hand'],
    approach: { Bip001_R_Clavicle: { x: 0, y: 4, z: -2 }, Bip001_R_UpperArm: { x: 18, y: 12, z: -54 }, Bip001_R_Forearm: { x: 0, y: -22, z: -88 }, Bip001_R_Hand: { x: 20, y: 0, z: 0 } },
    peak: { Bip001_R_Clavicle: { x: 0, y: 6, z: -4 }, Bip001_R_UpperArm: { x: 34, y: 8, z: -66 }, Bip001_R_Forearm: { x: 0, y: -16, z: -72 }, Bip001_R_Hand: { x: -14, y: 8, z: 6 } },
    follow: { Bip001_R_Clavicle: { x: 0, y: 5, z: -3 }, Bip001_R_UpperArm: { x: 36, y: 4, z: -52 }, Bip001_R_Forearm: { x: 0, y: -20, z: -64 }, Bip001_R_Hand: { x: 16, y: 4, z: 4 } },
    curlsA: { thumb: 0.2, index: 0.2, middle: 0.2, ring: 0.2, pinky: 0.2 },
    curlsP: { thumb: 0.15, index: 0.25, middle: 0.25, ring: 0.25, pinky: 0.25 }
  },
  off: {
    duration_ms: 900,
    notes: 'H46 distinct trajectory: flat hand brushing outward-away laterally.',
    bones: ['Bip001_R_Clavicle', 'Bip001_R_UpperArm', 'Bip001_R_Forearm', 'Bip001_R_Hand'],
    approach: { Bip001_R_Clavicle: { x: 0, y: 2, z: -2 }, Bip001_R_UpperArm: { x: 20, y: 20, z: -48 }, Bip001_R_Forearm: { x: 0, y: -28, z: -84 }, Bip001_R_Hand: { x: 6, y: -12, z: 0 } },
    peak: { Bip001_R_Clavicle: { x: 0, y: -6, z: -5 }, Bip001_R_UpperArm: { x: 26, y: -28, z: -58 }, Bip001_R_Forearm: { x: 0, y: -10, z: -52 }, Bip001_R_Hand: { x: -10, y: 22, z: -12 } },
    follow: { Bip001_R_Clavicle: { x: 0, y: -8, z: -6 }, Bip001_R_UpperArm: { x: 24, y: -32, z: -54 }, Bip001_R_Forearm: { x: 0, y: -8, z: -46 }, Bip001_R_Hand: { x: -14, y: 26, z: -14 } },
    curlsA: { thumb: 0.05, index: 0.05, middle: 0.05, ring: 0.05, pinky: 0.05 },
    curlsP: { thumb: 0.05, index: 0.05, middle: 0.05, ring: 0.05, pinky: 0.05 }
  },
  room: {
    duration_ms: 1200,
    notes: 'H46 distinct trajectory: open palms outlining lateral walls then front-back.',
    bones: ['Bip001_R_UpperArm', 'Bip001_R_Forearm', 'Bip001_R_Hand', 'Bip001_L_UpperArm', 'Bip001_L_Forearm', 'Bip001_L_Hand'],
    approach: { Bip001_R_UpperArm: { x: 22, y: -12, z: -52 }, Bip001_R_Forearm: { x: 0, y: -16, z: -80 }, Bip001_R_Hand: { x: 0, y: 18, z: 8 }, Bip001_L_UpperArm: { x: 22, y: 12, z: 52 }, Bip001_L_Forearm: { x: 0, y: 16, z: 80 }, Bip001_L_Hand: { x: 0, y: -18, z: -8 } },
    peak: { Bip001_R_UpperArm: { x: 26, y: 16, z: -48 }, Bip001_R_Forearm: { x: 0, y: -24, z: -86 }, Bip001_R_Hand: { x: 6, y: -16, z: 12 }, Bip001_L_UpperArm: { x: 26, y: -16, z: 48 }, Bip001_L_Forearm: { x: 0, y: 24, z: 86 }, Bip001_L_Hand: { x: 6, y: 16, z: -12 } },
    follow: { Bip001_R_UpperArm: { x: 24, y: 14, z: -46 }, Bip001_R_Forearm: { x: 0, y: -22, z: -82 }, Bip001_R_Hand: { x: 4, y: -14, z: 10 }, Bip001_L_UpperArm: { x: 24, y: -14, z: 46 }, Bip001_L_Forearm: { x: 0, y: 22, z: 82 }, Bip001_L_Hand: { x: 4, y: 14, z: -10 } },
    curlsA: { thumb: 0.05, index: 0.05, middle: 0.05, ring: 0.05, pinky: 0.05 },
    curlsP: { thumb: 0.05, index: 0.05, middle: 0.05, ring: 0.05, pinky: 0.05 }
  },
  slide: {
    duration_ms: 1000,
    notes: 'H46 distinct trajectory: smooth diagonal downward glide.',
    bones: ['Bip001_R_UpperArm', 'Bip001_R_Forearm', 'Bip001_R_Hand'],
    approach: { Bip001_R_UpperArm: { x: 32, y: 18, z: -68 }, Bip001_R_Forearm: { x: 0, y: -20, z: -92 }, Bip001_R_Hand: { x: 10, y: -6, z: 4 } },
    peak: { Bip001_R_UpperArm: { x: 26, y: -10, z: -42 }, Bip001_R_Forearm: { x: 0, y: -10, z: -56 }, Bip001_R_Hand: { x: 18, y: 8, z: -6 } },
    follow: { Bip001_R_UpperArm: { x: 22, y: -16, z: -36 }, Bip001_R_Forearm: { x: 0, y: -8, z: -48 }, Bip001_R_Hand: { x: 20, y: 10, z: -8 } },
    curlsA: { thumb: 0.1, index: 0.1, middle: 0.1, ring: 0.1, pinky: 0.1 },
    curlsP: { thumb: 0.1, index: 0.1, middle: 0.1, ring: 0.1, pinky: 0.1 }
  },
  team: {
    duration_ms: 1150,
    notes: 'H46 distinct trajectory: curved C-hands circling inward to unite.',
    bones: ['Bip001_R_UpperArm', 'Bip001_R_Forearm', 'Bip001_R_Hand', 'Bip001_L_UpperArm', 'Bip001_L_Forearm', 'Bip001_L_Hand'],
    approach: { Bip001_R_UpperArm: { x: 24, y: -14, z: -52 }, Bip001_R_Forearm: { x: 0, y: -22, z: -84 }, Bip001_R_Hand: { x: 8, y: 14, z: 6 }, Bip001_L_UpperArm: { x: 24, y: 14, z: 52 }, Bip001_L_Forearm: { x: 0, y: 22, z: 84 }, Bip001_L_Hand: { x: 8, y: -14, z: -6 } },
    peak: { Bip001_R_UpperArm: { x: 30, y: 22, z: -46 }, Bip001_R_Forearm: { x: 0, y: -32, z: -90 }, Bip001_R_Hand: { x: 12, y: -16, z: 10 }, Bip001_L_UpperArm: { x: 30, y: -22, z: 46 }, Bip001_L_Forearm: { x: 0, y: 32, z: 90 }, Bip001_L_Hand: { x: 12, y: 16, z: -10 } },
    follow: { Bip001_R_UpperArm: { x: 28, y: 18, z: -48 }, Bip001_R_Forearm: { x: 0, y: -28, z: -86 }, Bip001_R_Hand: { x: 10, y: -12, z: 8 }, Bip001_L_UpperArm: { x: 28, y: -18, z: 48 }, Bip001_L_Forearm: { x: 0, y: 28, z: 86 }, Bip001_L_Hand: { x: 10, y: 12, z: -8 } },
    curlsA: { thumb: 0.35, index: 0.35, middle: 0.35, ring: 0.35, pinky: 0.35 },
    curlsP: { thumb: 0.45, index: 0.45, middle: 0.45, ring: 0.45, pinky: 0.45 }
  },
  video: {
    duration_ms: 1100,
    notes: 'H46 distinct trajectory: camera/frame cranking motion at temple-front.',
    bones: ['Bip001_R_UpperArm', 'Bip001_R_Forearm', 'Bip001_R_Hand', 'Bip001_L_UpperArm', 'Bip001_L_Forearm'],
    approach: { Bip001_R_UpperArm: { x: 20, y: -8, z: -64 }, Bip001_R_Forearm: { x: 0, y: -18, z: -96 }, Bip001_R_Hand: { x: 0, y: 14, z: 10 }, Bip001_L_UpperArm: { x: 20, y: 8, z: 54 }, Bip001_L_Forearm: { x: 0, y: 18, z: 88 } },
    peak: { Bip001_R_UpperArm: { x: 24, y: -12, z: -70 }, Bip001_R_Forearm: { x: 6, y: -24, z: -104 }, Bip001_R_Hand: { x: 18, y: 20, z: -12 }, Bip001_L_UpperArm: { x: 22, y: 10, z: 56 }, Bip001_L_Forearm: { x: 0, y: 20, z: 90 } },
    follow: { Bip001_R_UpperArm: { x: 22, y: -10, z: -66 }, Bip001_R_Forearm: { x: -4, y: -18, z: -98 }, Bip001_R_Hand: { x: -12, y: 16, z: 12 }, Bip001_L_UpperArm: { x: 20, y: 8, z: 54 }, Bip001_L_Forearm: { x: 0, y: 18, z: 88 } },
    curlsA: { thumb: 0.3, index: 0.35, middle: 0.35, ring: 0.35, pinky: 0.35 },
    curlsP: { thumb: 0.4, index: 0.45, middle: 0.45, ring: 0.45, pinky: 0.45 }
  },
  first: {
    duration_ms: 950,
    notes: 'H46 distinct trajectory: upright index finger raised with crisp ordinal twist.',
    bones: ['Bip001_R_Clavicle', 'Bip001_R_UpperArm', 'Bip001_R_Forearm', 'Bip001_R_Hand'],
    approach: { Bip001_R_Clavicle: { x: 0, y: 4, z: -3 }, Bip001_R_UpperArm: { x: 24, y: 10, z: -64 }, Bip001_R_Forearm: { x: 0, y: -16, z: -98 }, Bip001_R_Hand: { x: 0, y: 16, z: 8 } },
    peak: { Bip001_R_Clavicle: { x: 0, y: 6, z: -5 }, Bip001_R_UpperArm: { x: 30, y: 12, z: -72 }, Bip001_R_Forearm: { x: 0, y: -22, z: -104 }, Bip001_R_Hand: { x: -8, y: -18, z: 14 } },
    follow: { Bip001_R_Clavicle: { x: 0, y: 5, z: -4 }, Bip001_R_UpperArm: { x: 28, y: 10, z: -68 }, Bip001_R_Forearm: { x: 0, y: -20, z: -100 }, Bip001_R_Hand: { x: -6, y: -14, z: 12 } },
    curlsA: { thumb: 0.75, index: 0.0, middle: 0.9, ring: 0.9, pinky: 0.9 },
    curlsP: { thumb: 0.8, index: 0.0, middle: 0.92, ring: 0.92, pinky: 0.92 }
  },
  life: {
    duration_ms: 1150,
    notes: 'H46 distinct trajectory: bilateral upward torso/chest-to-shoulder lift.',
    bones: ['Bip001_R_UpperArm', 'Bip001_R_Forearm', 'Bip001_R_Hand', 'Bip001_L_UpperArm', 'Bip001_L_Forearm', 'Bip001_L_Hand'],
    approach: { Bip001_R_UpperArm: { x: 14, y: 12, z: -38 }, Bip001_R_Forearm: { x: 0, y: -26, z: -82 }, Bip001_R_Hand: { x: 6, y: -10, z: 4 }, Bip001_L_UpperArm: { x: 14, y: -12, z: 38 }, Bip001_L_Forearm: { x: 0, y: 26, z: 82 }, Bip001_L_Hand: { x: 6, y: 10, z: -4 } },
    peak: { Bip001_R_UpperArm: { x: 26, y: 14, z: -68 }, Bip001_R_Forearm: { x: 0, y: -22, z: -98 }, Bip001_R_Hand: { x: -10, y: -8, z: 8 }, Bip001_L_UpperArm: { x: 26, y: -14, z: 68 }, Bip001_L_Forearm: { x: 0, y: 22, z: 98 }, Bip001_L_Hand: { x: -10, y: 8, z: -8 } },
    follow: { Bip001_R_UpperArm: { x: 24, y: 12, z: -64 }, Bip001_R_Forearm: { x: 0, y: -20, z: -94 }, Bip001_R_Hand: { x: -8, y: -6, z: 6 }, Bip001_L_UpperArm: { x: 24, y: -12, z: 64 }, Bip001_L_Forearm: { x: 0, y: 20, z: 94 }, Bip001_L_Hand: { x: -8, y: 6, z: -6 } },
    curlsA: { thumb: 0.0, index: 0.0, middle: 0.85, ring: 0.85, pinky: 0.85 },
    curlsP: { thumb: 0.0, index: 0.0, middle: 0.88, ring: 0.88, pinky: 0.88 }
  },
  question: {
    duration_ms: 1050,
    notes: 'H46 distinct trajectory: index finger tracing a curved question hook + subtle head tilt.',
    bones: ['Bip001_R_UpperArm', 'Bip001_R_Forearm', 'Bip001_R_Hand', 'Bip001_Head'],
    approach: { Bip001_R_UpperArm: { x: 24, y: 6, z: -66 }, Bip001_R_Forearm: { x: 0, y: -16, z: -96 }, Bip001_R_Hand: { x: -10, y: 8, z: 6 }, Bip001_Head: { x: 4, y: 0, z: 4 } },
    peak: { Bip001_R_UpperArm: { x: 28, y: -6, z: -60 }, Bip001_R_Forearm: { x: 0, y: -14, z: -84 }, Bip001_R_Hand: { x: 18, y: -4, z: -6 }, Bip001_Head: { x: 6, y: 0, z: 6 } },
    follow: { Bip001_R_UpperArm: { x: 22, y: 4, z: -52 }, Bip001_R_Forearm: { x: 0, y: -18, z: -88 }, Bip001_R_Hand: { x: 24, y: 0, z: 0 }, Bip001_Head: { x: 4, y: 0, z: 4 } },
    curlsA: { thumb: 0.75, index: 0.0, middle: 0.9, ring: 0.9, pinky: 0.9 },
    curlsP: { thumb: 0.75, index: 0.35, middle: 0.9, ring: 0.9, pinky: 0.9 }
  },
  show: {
    duration_ms: 1050,
    notes: 'H46 distinct trajectory: flat hand presenting outward toward addressee.',
    bones: ['Bip001_R_UpperArm', 'Bip001_R_Forearm', 'Bip001_R_Hand', 'Bip001_L_UpperArm', 'Bip001_L_Forearm'],
    approach: { Bip001_R_UpperArm: { x: 18, y: 14, z: -48 }, Bip001_R_Forearm: { x: 0, y: -24, z: -84 }, Bip001_R_Hand: { x: 4, y: -10, z: 6 }, Bip001_L_UpperArm: { x: 20, y: -14, z: 46 }, Bip001_L_Forearm: { x: 0, y: 22, z: 80 } },
    peak: { Bip001_R_UpperArm: { x: 38, y: 6, z: -56 }, Bip001_R_Forearm: { x: 0, y: -10, z: -52 }, Bip001_R_Hand: { x: -12, y: 4, z: 10 }, Bip001_L_UpperArm: { x: 30, y: -8, z: 48 }, Bip001_L_Forearm: { x: 0, y: 12, z: 60 } },
    follow: { Bip001_R_UpperArm: { x: 34, y: 8, z: -54 }, Bip001_R_Forearm: { x: 0, y: -12, z: -56 }, Bip001_R_Hand: { x: -8, y: 2, z: 8 }, Bip001_L_UpperArm: { x: 26, y: -10, z: 46 }, Bip001_L_Forearm: { x: 0, y: 14, z: 64 } },
    curlsA: { thumb: 0.1, index: 0.05, middle: 0.1, ring: 0.1, pinky: 0.1 },
    curlsP: { thumb: 0.05, index: 0.0, middle: 0.05, ring: 0.05, pinky: 0.05 }
  },
  win: {
    duration_ms: 1000,
    notes: 'H46 distinct trajectory: celebratory closed-fist upward pull.',
    bones: ['Bip001_R_Clavicle', 'Bip001_R_UpperArm', 'Bip001_R_Forearm', 'Bip001_R_Hand'],
    approach: { Bip001_R_Clavicle: { x: 0, y: 4, z: -4 }, Bip001_R_UpperArm: { x: 28, y: -10, z: -58 }, Bip001_R_Forearm: { x: 0, y: -12, z: -64 }, Bip001_R_Hand: { x: 8, y: 12, z: 0 } },
    peak: { Bip001_R_Clavicle: { x: 0, y: 8, z: -8 }, Bip001_R_UpperArm: { x: 20, y: 10, z: -78 }, Bip001_R_Forearm: { x: 0, y: -26, z: -110 }, Bip001_R_Hand: { x: -12, y: 16, z: 10 } },
    follow: { Bip001_R_Clavicle: { x: 0, y: 6, z: -6 }, Bip001_R_UpperArm: { x: 18, y: 8, z: -74 }, Bip001_R_Forearm: { x: 0, y: -24, z: -104 }, Bip001_R_Hand: { x: -8, y: 12, z: 8 } },
    curlsA: { thumb: 0.65, index: 0.85, middle: 0.85, ring: 0.85, pinky: 0.85 },
    curlsP: { thumb: 0.85, index: 0.95, middle: 0.95, ring: 0.95, pinky: 0.95 }
  },
  board: {
    duration_ms: 1100,
    notes: 'H46 distinct trajectory: wide flat-palm horizontal sweep outlining a board.',
    bones: ['Bip001_R_UpperArm', 'Bip001_R_Forearm', 'Bip001_R_Hand', 'Bip001_L_UpperArm', 'Bip001_L_Forearm', 'Bip001_L_Hand'],
    approach: { Bip001_R_UpperArm: { x: 22, y: 14, z: -56 }, Bip001_R_Forearm: { x: 0, y: -18, z: -78 }, Bip001_R_Hand: { x: 0, y: 0, z: 6 }, Bip001_L_UpperArm: { x: 22, y: -14, z: 56 }, Bip001_L_Forearm: { x: 0, y: 18, z: 78 }, Bip001_L_Hand: { x: 0, y: 0, z: -6 } },
    peak: { Bip001_R_UpperArm: { x: 24, y: -24, z: -60 }, Bip001_R_Forearm: { x: 0, y: -12, z: -66 }, Bip001_R_Hand: { x: 4, y: 14, z: 4 }, Bip001_L_UpperArm: { x: 24, y: 24, z: 60 }, Bip001_L_Forearm: { x: 0, y: 12, z: 66 }, Bip001_L_Hand: { x: 4, y: -14, z: -4 } },
    follow: { Bip001_R_UpperArm: { x: 20, y: -20, z: -54 }, Bip001_R_Forearm: { x: 0, y: -14, z: -68 }, Bip001_R_Hand: { x: 2, y: 10, z: 4 }, Bip001_L_UpperArm: { x: 20, y: 20, z: 54 }, Bip001_L_Forearm: { x: 0, y: 14, z: 68 }, Bip001_L_Hand: { x: 2, y: -10, z: -4 } },
    curlsA: { thumb: 0.05, index: 0.05, middle: 0.05, ring: 0.05, pinky: 0.05 },
    curlsP: { thumb: 0.05, index: 0.05, middle: 0.05, ring: 0.05, pinky: 0.05 }
  },
  communication: {
    duration_ms: 1200,
    notes: 'H46 distinct trajectory: alternating bilateral C-hands oscillating forward from chin.',
    bones: ['Bip001_R_UpperArm', 'Bip001_R_Forearm', 'Bip001_R_Hand', 'Bip001_L_UpperArm', 'Bip001_L_Forearm', 'Bip001_L_Hand'],
    approach: { Bip001_R_UpperArm: { x: 22, y: 14, z: -66 }, Bip001_R_Forearm: { x: 0, y: -24, z: -96 }, Bip001_R_Hand: { x: 6, y: -12, z: 8 }, Bip001_L_UpperArm: { x: 26, y: -10, z: 56 }, Bip001_L_Forearm: { x: 0, y: 16, z: 76 }, Bip001_L_Hand: { x: 6, y: 12, z: -8 } },
    peak: { Bip001_R_UpperArm: { x: 34, y: 6, z: -56 }, Bip001_R_Forearm: { x: 0, y: -14, z: -66 }, Bip001_R_Hand: { x: 0, y: -8, z: 6 }, Bip001_L_UpperArm: { x: 20, y: -16, z: 66 }, Bip001_L_Forearm: { x: 0, y: 26, z: 96 }, Bip001_L_Hand: { x: 8, y: 14, z: -8 } },
    follow: { Bip001_R_UpperArm: { x: 22, y: 14, z: -64 }, Bip001_R_Forearm: { x: 0, y: -22, z: -94 }, Bip001_R_Hand: { x: 6, y: -10, z: 6 }, Bip001_L_UpperArm: { x: 34, y: -6, z: 56 }, Bip001_L_Forearm: { x: 0, y: 14, z: 66 }, Bip001_L_Hand: { x: 0, y: 8, z: -6 } },
    curlsA: { thumb: 0.35, index: 0.35, middle: 0.35, ring: 0.35, pinky: 0.35 },
    curlsP: { thumb: 0.35, index: 0.35, middle: 0.35, ring: 0.35, pinky: 0.35 }
  },
  eat: {
    duration_ms: 1000,
    notes: 'H46 distinct trajectory: bunched O-hand tapping toward mouth.',
    bones: ['Bip001_R_UpperArm', 'Bip001_R_Forearm', 'Bip001_R_Hand', 'Bip001_Head'],
    approach: { Bip001_R_UpperArm: { x: 24, y: 12, z: -56 }, Bip001_R_Forearm: { x: 0, y: -22, z: -88 }, Bip001_R_Hand: { x: 14, y: -10, z: 4 }, Bip001_Head: { x: 2, y: 0, z: 0 } },
    peak: { Bip001_R_UpperArm: { x: 28, y: 22, z: -76 }, Bip001_R_Forearm: { x: 0, y: -32, z: -112 }, Bip001_R_Hand: { x: 22, y: -16, z: 10 }, Bip001_Head: { x: 6, y: 0, z: 0 } },
    follow: { Bip001_R_UpperArm: { x: 24, y: 16, z: -64 }, Bip001_R_Forearm: { x: 0, y: -24, z: -96 }, Bip001_R_Hand: { x: 16, y: -12, z: 6 }, Bip001_Head: { x: 2, y: 0, z: 0 } },
    curlsA: { thumb: 0.55, index: 0.6, middle: 0.6, ring: 0.6, pinky: 0.6 },
    curlsP: { thumb: 0.65, index: 0.72, middle: 0.72, ring: 0.72, pinky: 0.72 }
  },
  tell: {
    duration_ms: 1000,
    notes: 'H46 distinct trajectory: index finger arcing outward from chin toward listener.',
    bones: ['Bip001_R_Clavicle', 'Bip001_R_UpperArm', 'Bip001_R_Forearm', 'Bip001_R_Hand'],
    approach: { Bip001_R_Clavicle: { x: 0, y: 4, z: -3 }, Bip001_R_UpperArm: { x: 24, y: 20, z: -72 }, Bip001_R_Forearm: { x: 0, y: -28, z: -106 }, Bip001_R_Hand: { x: 12, y: -10, z: 6 } },
    peak: { Bip001_R_Clavicle: { x: 0, y: 6, z: -4 }, Bip001_R_UpperArm: { x: 38, y: 4, z: -58 }, Bip001_R_Forearm: { x: 0, y: -12, z: -62 }, Bip001_R_Hand: { x: -10, y: 6, z: 8 } },
    follow: { Bip001_R_Clavicle: { x: 0, y: 5, z: -3 }, Bip001_R_UpperArm: { x: 34, y: 2, z: -52 }, Bip001_R_Forearm: { x: 0, y: -10, z: -56 }, Bip001_R_Hand: { x: -8, y: 4, z: 6 } },
    curlsA: { thumb: 0.7, index: 0.0, middle: 0.85, ring: 0.85, pinky: 0.85 },
    curlsP: { thumb: 0.75, index: 0.0, middle: 0.9, ring: 0.9, pinky: 0.9 }
  },
  left: {
    duration_ms: 950,
    notes: 'H46 distinct trajectory: clear lateral sweep toward left signing space.',
    bones: ['Bip001_R_UpperArm', 'Bip001_R_Forearm', 'Bip001_R_Hand', 'Bip001_Spine1'],
    approach: { Bip001_R_UpperArm: { x: 20, y: 12, z: -52 }, Bip001_R_Forearm: { x: 0, y: -22, z: -84 }, Bip001_R_Hand: { x: 0, y: 10, z: 4 }, Bip001_Spine1: { x: 0, y: -4, z: 0 } },
    peak: { Bip001_R_UpperArm: { x: 22, y: 34, z: -56 }, Bip001_R_Forearm: { x: 0, y: -32, z: -90 }, Bip001_R_Hand: { x: -8, y: 20, z: 12 }, Bip001_Spine1: { x: 0, y: -10, z: 0 } },
    follow: { Bip001_R_UpperArm: { x: 20, y: 30, z: -54 }, Bip001_R_Forearm: { x: 0, y: -28, z: -86 }, Bip001_R_Hand: { x: -6, y: 16, z: 10 }, Bip001_Spine1: { x: 0, y: -8, z: 0 } },
    curlsA: { thumb: 0.15, index: 0.1, middle: 0.15, ring: 0.15, pinky: 0.15 },
    curlsP: { thumb: 0.2, index: 0.05, middle: 0.2, ring: 0.2, pinky: 0.2 }
  },
  other: {
    duration_ms: 950,
    notes: 'H46 distinct trajectory: thumb-extended A-hand flipping outward laterally.',
    bones: ['Bip001_R_UpperArm', 'Bip001_R_Forearm', 'Bip001_R_Hand'],
    approach: { Bip001_R_UpperArm: { x: 22, y: 10, z: -50 }, Bip001_R_Forearm: { x: 0, y: -18, z: -82 }, Bip001_R_Hand: { x: 0, y: -10, z: 0 } },
    peak: { Bip001_R_UpperArm: { x: 24, y: -18, z: -54 }, Bip001_R_Forearm: { x: 0, y: -8, z: -72 }, Bip001_R_Hand: { x: 0, y: 28, z: -14 } },
    follow: { Bip001_R_UpperArm: { x: 22, y: -16, z: -50 }, Bip001_R_Forearm: { x: 0, y: -10, z: -68 }, Bip001_R_Hand: { x: 0, y: 24, z: -12 } },
    curlsA: { thumb: 0.0, index: 0.85, middle: 0.85, ring: 0.85, pinky: 0.85 },
    curlsP: { thumb: 0.0, index: 0.9, middle: 0.9, ring: 0.9, pinky: 0.9 }
  },
  pick: {
    duration_ms: 950,
    notes: 'H46 distinct trajectory: thumb-index pinch lifting upward from neutral space.',
    bones: ['Bip001_R_UpperArm', 'Bip001_R_Forearm', 'Bip001_R_Hand'],
    approach: { Bip001_R_UpperArm: { x: 28, y: 8, z: -38 }, Bip001_R_Forearm: { x: 0, y: -16, z: -68 }, Bip001_R_Hand: { x: 18, y: 0, z: 0 } },
    peak: { Bip001_R_UpperArm: { x: 22, y: 10, z: -62 }, Bip001_R_Forearm: { x: 0, y: -22, z: -94 }, Bip001_R_Hand: { x: -12, y: 6, z: 8 } },
    follow: { Bip001_R_UpperArm: { x: 20, y: 8, z: -58 }, Bip001_R_Forearm: { x: 0, y: -20, z: -90 }, Bip001_R_Hand: { x: -10, y: 4, z: 6 } },
    curlsA: { thumb: 0.15, index: 0.2, middle: 0.8, ring: 0.8, pinky: 0.8 },
    curlsP: { thumb: 0.45, index: 0.5, middle: 0.85, ring: 0.85, pinky: 0.85 }
  },
  seven: {
    duration_ms: 900,
    notes: 'H46 distinct trajectory: ISL 7 numeral handshape held clearly with wrist tilt.',
    bones: ['Bip001_R_UpperArm', 'Bip001_R_Forearm', 'Bip001_R_Hand'],
    approach: { Bip001_R_UpperArm: { x: 22, y: 4, z: -62 }, Bip001_R_Forearm: { x: 0, y: -14, z: -94 }, Bip001_R_Hand: { x: -6, y: 12, z: 4 } },
    peak: { Bip001_R_UpperArm: { x: 26, y: 2, z: -68 }, Bip001_R_Forearm: { x: 0, y: -16, z: -100 }, Bip001_R_Hand: { x: -12, y: 18, z: 10 } },
    follow: { Bip001_R_UpperArm: { x: 24, y: 4, z: -64 }, Bip001_R_Forearm: { x: 0, y: -14, z: -96 }, Bip001_R_Hand: { x: -8, y: 14, z: 6 } },
    curlsA: { thumb: 0.0, index: 0.25, middle: 0.85, ring: 0.85, pinky: 0.85 },
    curlsP: { thumb: 0.0, index: 0.32, middle: 0.9, ring: 0.9, pinky: 0.9 }
  },
  should: {
    duration_ms: 950,
    notes: 'H46 distinct trajectory: hooked index downward modal emphasis.',
    bones: ['Bip001_R_UpperArm', 'Bip001_R_Forearm', 'Bip001_R_Hand', 'Bip001_Head'],
    approach: { Bip001_R_UpperArm: { x: 22, y: 10, z: -62 }, Bip001_R_Forearm: { x: 0, y: -18, z: -96 }, Bip001_R_Hand: { x: -8, y: 0, z: 6 }, Bip001_Head: { x: 0, y: 0, z: 0 } },
    peak: { Bip001_R_UpperArm: { x: 28, y: 12, z: -40 }, Bip001_R_Forearm: { x: 0, y: -22, z: -72 }, Bip001_R_Hand: { x: 24, y: 4, z: 8 }, Bip001_Head: { x: 6, y: 0, z: 0 } },
    follow: { Bip001_R_UpperArm: { x: 26, y: 10, z: -44 }, Bip001_R_Forearm: { x: 0, y: -20, z: -76 }, Bip001_R_Hand: { x: 18, y: 2, z: 6 }, Bip001_Head: { x: 3, y: 0, z: 0 } },
    curlsA: { thumb: 0.75, index: 0.35, middle: 0.9, ring: 0.9, pinky: 0.9 },
    curlsP: { thumb: 0.8, index: 0.48, middle: 0.92, ring: 0.92, pinky: 0.92 }
  },
  six: {
    duration_ms: 900,
    notes: 'H46 distinct trajectory: ISL 6 numeral handshape held at shoulder-front.',
    bones: ['Bip001_R_UpperArm', 'Bip001_R_Forearm', 'Bip001_R_Hand'],
    approach: { Bip001_R_UpperArm: { x: 20, y: 2, z: -60 }, Bip001_R_Forearm: { x: 0, y: -12, z: -92 }, Bip001_R_Hand: { x: -4, y: 10, z: -6 } },
    peak: { Bip001_R_UpperArm: { x: 24, y: -4, z: -66 }, Bip001_R_Forearm: { x: 0, y: -14, z: -98 }, Bip001_R_Hand: { x: -8, y: 16, z: -12 } },
    follow: { Bip001_R_UpperArm: { x: 22, y: 0, z: -62 }, Bip001_R_Forearm: { x: 0, y: -12, z: -94 }, Bip001_R_Hand: { x: -6, y: 12, z: -8 } },
    curlsA: { thumb: 0.15, index: 0.85, middle: 0.85, ring: 0.85, pinky: 0.0 },
    curlsP: { thumb: 0.2, index: 0.9, middle: 0.9, ring: 0.9, pinky: 0.0 }
  },
  myself: {
    duration_ms: 950,
    notes: 'H46 distinct trajectory: thumb/A-hand tapping center chest.',
    bones: ['Bip001_R_Clavicle', 'Bip001_R_UpperArm', 'Bip001_R_Forearm', 'Bip001_R_Hand'],
    approach: { Bip001_R_Clavicle: { x: 0, y: 6, z: -3 }, Bip001_R_UpperArm: { x: 18, y: 24, z: -48 }, Bip001_R_Forearm: { x: 0, y: -36, z: -92 }, Bip001_R_Hand: { x: 10, y: -18, z: 6 } },
    peak: { Bip001_R_Clavicle: { x: 0, y: 10, z: -4 }, Bip001_R_UpperArm: { x: 22, y: 34, z: -44 }, Bip001_R_Forearm: { x: 0, y: -44, z: -104 }, Bip001_R_Hand: { x: 16, y: -24, z: 10 } },
    follow: { Bip001_R_Clavicle: { x: 0, y: 8, z: -3 }, Bip001_R_UpperArm: { x: 20, y: 30, z: -46 }, Bip001_R_Forearm: { x: 0, y: -40, z: -98 }, Bip001_R_Hand: { x: 14, y: -20, z: 8 } },
    curlsA: { thumb: 0.0, index: 0.85, middle: 0.85, ring: 0.85, pinky: 0.85 },
    curlsP: { thumb: 0.0, index: 0.92, middle: 0.92, ring: 0.92, pinky: 0.92 }
  },
  read: {
    duration_ms: 1100,
    notes: 'H46 distinct trajectory: V-fingers scanning downward across open left palm.',
    bones: ['Bip001_R_UpperArm', 'Bip001_R_Forearm', 'Bip001_R_Hand', 'Bip001_L_UpperArm', 'Bip001_L_Forearm', 'Bip001_L_Hand'],
    approach: { Bip001_R_UpperArm: { x: 24, y: 14, z: -56 }, Bip001_R_Forearm: { x: 0, y: -24, z: -88 }, Bip001_R_Hand: { x: 18, y: -8, z: 4 }, Bip001_L_UpperArm: { x: 24, y: -14, z: 44 }, Bip001_L_Forearm: { x: 0, y: 20, z: 78 }, Bip001_L_Hand: { x: -12, y: 14, z: 0 } },
    peak: { Bip001_R_UpperArm: { x: 28, y: 18, z: -42 }, Bip001_R_Forearm: { x: 0, y: -28, z: -76 }, Bip001_R_Hand: { x: 28, y: -12, z: 8 }, Bip001_L_UpperArm: { x: 24, y: -14, z: 44 }, Bip001_L_Forearm: { x: 0, y: 20, z: 78 }, Bip001_L_Hand: { x: -12, y: 14, z: 0 } },
    follow: { Bip001_R_UpperArm: { x: 24, y: 14, z: -52 }, Bip001_R_Forearm: { x: 0, y: -24, z: -84 }, Bip001_R_Hand: { x: 20, y: -10, z: 6 }, Bip001_L_UpperArm: { x: 24, y: -14, z: 44 }, Bip001_L_Forearm: { x: 0, y: 20, z: 78 }, Bip001_L_Hand: { x: -12, y: 14, z: 0 } },
    curlsA: { thumb: 0.8, index: 0.0, middle: 0.0, ring: 0.85, pinky: 0.85 },
    curlsP: { thumb: 0.85, index: 0.0, middle: 0.0, ring: 0.9, pinky: 0.9 }
  },
  fourth: {
    duration_ms: 900,
    notes: 'H46 distinct trajectory: 4-finger ordinal twist in upper-front space.',
    bones: ['Bip001_R_UpperArm', 'Bip001_R_Forearm', 'Bip001_R_Hand'],
    approach: { Bip001_R_UpperArm: { x: 22, y: 6, z: -62 }, Bip001_R_Forearm: { x: 0, y: -14, z: -94 }, Bip001_R_Hand: { x: 0, y: 14, z: 4 } },
    peak: { Bip001_R_UpperArm: { x: 26, y: 8, z: -68 }, Bip001_R_Forearm: { x: 0, y: -18, z: -100 }, Bip001_R_Hand: { x: -6, y: -16, z: 10 } },
    follow: { Bip001_R_UpperArm: { x: 24, y: 6, z: -64 }, Bip001_R_Forearm: { x: 0, y: -16, z: -96 }, Bip001_R_Hand: { x: -4, y: -12, z: 8 } },
    curlsA: { thumb: 0.8, index: 0.0, middle: 0.0, ring: 0.0, pinky: 0.0 },
    curlsP: { thumb: 0.85, index: 0.0, middle: 0.0, ring: 0.0, pinky: 0.0 }
  },
  two: {
    duration_ms: 850,
    notes: 'H46 distinct trajectory: clear 2-finger V-handshape held forward.',
    bones: ['Bip001_R_UpperArm', 'Bip001_R_Forearm', 'Bip001_R_Hand'],
    approach: { Bip001_R_UpperArm: { x: 24, y: 6, z: -60 }, Bip001_R_Forearm: { x: 0, y: -12, z: -92 }, Bip001_R_Hand: { x: -4, y: 8, z: 2 } },
    peak: { Bip001_R_UpperArm: { x: 28, y: 8, z: -66 }, Bip001_R_Forearm: { x: 0, y: -14, z: -98 }, Bip001_R_Hand: { x: -8, y: 12, z: 6 } },
    follow: { Bip001_R_UpperArm: { x: 26, y: 6, z: -62 }, Bip001_R_Forearm: { x: 0, y: -12, z: -94 }, Bip001_R_Hand: { x: -6, y: 10, z: 4 } },
    curlsA: { thumb: 0.8, index: 0.0, middle: 0.0, ring: 0.88, pinky: 0.88 },
    curlsP: { thumb: 0.85, index: 0.0, middle: 0.0, ring: 0.92, pinky: 0.92 }
  },
  three: {
    duration_ms: 850,
    notes: 'H46 distinct trajectory: clear 3-finger numeral held slightly wider.',
    bones: ['Bip001_R_UpperArm', 'Bip001_R_Forearm', 'Bip001_R_Hand'],
    approach: { Bip001_R_UpperArm: { x: 22, y: 0, z: -64 }, Bip001_R_Forearm: { x: 0, y: -14, z: -94 }, Bip001_R_Hand: { x: -4, y: 14, z: -4 } },
    peak: { Bip001_R_UpperArm: { x: 26, y: -4, z: -70 }, Bip001_R_Forearm: { x: 0, y: -16, z: -102 }, Bip001_R_Hand: { x: -10, y: 18, z: -8 } },
    follow: { Bip001_R_UpperArm: { x: 24, y: -2, z: -66 }, Bip001_R_Forearm: { x: 0, y: -14, z: -96 }, Bip001_R_Hand: { x: -6, y: 14, z: -6 } },
    curlsA: { thumb: 0.8, index: 0.0, middle: 0.0, ring: 0.0, pinky: 0.88 },
    curlsP: { thumb: 0.85, index: 0.0, middle: 0.0, ring: 0.0, pinky: 0.92 }
  },
  scene: {
    duration_ms: 1100,
    notes: 'H46 distinct trajectory: bilateral L-frame outlining a visual scene rectangle.',
    bones: ['Bip001_R_UpperArm', 'Bip001_R_Forearm', 'Bip001_R_Hand', 'Bip001_L_UpperArm', 'Bip001_L_Forearm', 'Bip001_L_Hand'],
    approach: { Bip001_R_UpperArm: { x: 28, y: 10, z: -62 }, Bip001_R_Forearm: { x: 0, y: -16, z: -88 }, Bip001_R_Hand: { x: 0, y: 12, z: 6 }, Bip001_L_UpperArm: { x: 28, y: -10, z: 62 }, Bip001_L_Forearm: { x: 0, y: 16, z: 88 }, Bip001_L_Hand: { x: 0, y: -12, z: -6 } },
    peak: { Bip001_R_UpperArm: { x: 28, y: -18, z: -66 }, Bip001_R_Forearm: { x: 0, y: -12, z: -80 }, Bip001_R_Hand: { x: 4, y: 16, z: 8 }, Bip001_L_UpperArm: { x: 28, y: 18, z: 66 }, Bip001_L_Forearm: { x: 0, y: 12, z: 80 }, Bip001_L_Hand: { x: 4, y: -16, z: -8 } },
    follow: { Bip001_R_UpperArm: { x: 24, y: -18, z: -48 }, Bip001_R_Forearm: { x: 0, y: -14, z: -72 }, Bip001_R_Hand: { x: 8, y: 12, z: 6 }, Bip001_L_UpperArm: { x: 24, y: 18, z: 48 }, Bip001_L_Forearm: { x: 0, y: 14, z: 72 }, Bip001_L_Hand: { x: 8, y: -12, z: -6 } },
    curlsA: { thumb: 0.0, index: 0.0, middle: 0.85, ring: 0.85, pinky: 0.85 },
    curlsP: { thumb: 0.0, index: 0.0, middle: 0.85, ring: 0.85, pinky: 0.85 }
  },
  twenty: {
    duration_ms: 950,
    notes: 'H46 distinct trajectory: 2-to-pinch lateral movement representing 20.',
    bones: ['Bip001_R_UpperArm', 'Bip001_R_Forearm', 'Bip001_R_Hand'],
    approach: { Bip001_R_UpperArm: { x: 24, y: 6, z: -62 }, Bip001_R_Forearm: { x: 0, y: -14, z: -94 }, Bip001_R_Hand: { x: 0, y: 10, z: 4 } },
    peak: { Bip001_R_UpperArm: { x: 26, y: -10, z: -60 }, Bip001_R_Forearm: { x: 0, y: -12, z: -86 }, Bip001_R_Hand: { x: 10, y: 18, z: -6 } },
    follow: { Bip001_R_UpperArm: { x: 26, y: -12, z: -58 }, Bip001_R_Forearm: { x: 0, y: -10, z: -84 }, Bip001_R_Hand: { x: 12, y: 20, z: -8 } },
    curlsA: { thumb: 0.65, index: 0.0, middle: 0.0, ring: 0.88, pinky: 0.88 },
    curlsP: { thumb: 0.55, index: 0.55, middle: 0.88, ring: 0.88, pinky: 0.88 }
  }
};

let updated = 0;
for (const [signId, spec] of Object.entries(REPAIRS)) {
  const filePath = path.join(SIGNS_DIR, `${signId}.json`);
  const data = JSON.parse(fs.readFileSync(filePath, 'utf8'));
  data.metadata = data.metadata || {};
  data.metadata.notes = spec.notes;
  data.metadata.motion_distinctness = 'unique_trajectory_h46';
  data.metadata.validation_status = 'IMPLEMENTATION_PENDING_LINGUISTIC_REVIEW';
  data.motion.duration_ms = spec.duration_ms;
  data.motion.involved_bones = spec.bones;
  data.motion.keyframes = buildKeyframes(
    spec.duration_ms,
    spec.bones,
    spec.approach,
    spec.peak,
    spec.follow,
    spec.curlsA,
    spec.curlsP
  );
  fs.writeFileSync(filePath, JSON.stringify(data, null, 2) + '\n', 'utf8');
  updated++;
}

console.log(`Updated ${updated} duplicate signs with unique H46 trajectories & finger curls.`);
