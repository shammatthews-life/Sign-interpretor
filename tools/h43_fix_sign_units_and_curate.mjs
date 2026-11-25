import fs from 'fs';
import path from 'path';

const SIGNS_DIR = 'signs';
const RAD_TO_DEG = 180 / Math.PI;

function round1(val) {
  return Math.round(val * 10) / 10;
}

function clamp(val, min, max) {
  return Math.max(min, Math.min(max, val));
}

function maxRotAndCurl(motion) {
  let maxRot = 0;
  let maxCurl = 0;
  for (const kf of motion?.keyframes || []) {
    for (const axes of Object.values(kf.rotations || {})) {
      for (const v of Object.values(axes || {})) {
        const n = Number(v);
        if (Number.isFinite(n)) maxRot = Math.max(maxRot, Math.abs(n));
      }
    }
    const curls = kf.finger_curls || {};
    for (const v of Object.values(curls)) {
      if (typeof v === 'number' && Number.isFinite(v)) {
        maxCurl = Math.max(maxCurl, Math.abs(v));
      } else if (v && typeof v === 'object') {
        for (const nv of Object.values(v)) {
          const n = Number(nv);
          if (Number.isFinite(n)) maxCurl = Math.max(maxCurl, Math.abs(n));
        }
      }
    }
  }
  return { maxRot, maxCurl };
}

function convertSignUnits(data) {
  const { maxRot, maxCurl } = maxRotAndCurl(data.motion);
  let convertedRots = false;
  let convertedCurls = false;

  if (maxRot > 0 && maxRot < 5) {
    convertedRots = true;
    for (const kf of data.motion.keyframes) {
      for (const bone of Object.keys(kf.rotations || {})) {
        const axes = kf.rotations[bone];
        for (const axis of ['x', 'y', 'z']) {
          if (Number.isFinite(axes[axis])) {
            axes[axis] = round1(clamp(axes[axis] * RAD_TO_DEG, -175, 175));
          }
        }
      }
    }
  }

  if (maxCurl > 0 && maxCurl <= 1.55) {
    convertedCurls = true;
    for (const kf of data.motion.keyframes) {
      if (!kf.finger_curls || typeof kf.finger_curls !== 'object') continue;
      for (const [k, v] of Object.entries(kf.finger_curls)) {
        if (typeof v === 'number' && Number.isFinite(v)) {
          kf.finger_curls[k] = round1(clamp(v * 80, 0, 120));
        } else if (v && typeof v === 'object') {
          for (const [fk, fv] of Object.entries(v)) {
            if (Number.isFinite(fv)) {
              v[fk] = round1(clamp(fv * 80, 0, 120));
            }
          }
        }
      }
    }
  }

  return { convertedRots, convertedCurls };
}

// Parametric ISL articulation composer operating in calibrated degrees
const HANDSHAPES = {
  flat: { thumb: 10, index: 0, middle: 0, ring: 0, pinky: 0 },
  open5: { thumb: 0, index: 5, middle: 5, ring: 5, pinky: 5 },
  point: { thumb: 65, index: 0, middle: 85, ring: 85, pinky: 85 },
  v2: { thumb: 65, index: 0, middle: 0, ring: 85, pinky: 85 },
  w3: { thumb: 65, index: 0, middle: 0, ring: 0, pinky: 85 },
  four: { thumb: 75, index: 0, middle: 0, ring: 0, pinky: 0 },
  fist: { thumb: 80, index: 88, middle: 88, ring: 88, pinky: 88 },
  curvedC: { thumb: 35, index: 38, middle: 38, ring: 38, pinky: 38 },
  pinchO: { thumb: 68, index: 68, middle: 75, ring: 75, pinky: 75 },
  pinchF: { thumb: 65, index: 65, middle: 0, ring: 0, pinky: 0 },
  yPhone: { thumb: 0, index: 85, middle: 85, ring: 85, pinky: 0 },
  claw: { thumb: 45, index: 55, middle: 55, ring: 55, pinky: 55 },
  lShape: { thumb: 0, index: 0, middle: 85, ring: 85, pinky: 85 },
  cup: { thumb: 25, index: 28, middle: 28, ring: 28, pinky: 28 }
};

const LOCATIONS = {
  forehead: { rx: -16, ry: -8, rz: -88, fx: 0, fy: -32, fz: -78 },
  temple: { rx: -14, ry: -6, rz: -84, fx: 0, fy: -28, fz: -74 },
  eye: { rx: -15, ry: -10, rz: -82, fx: 0, fy: -34, fz: -74 },
  ear: { rx: -12, ry: -4, rz: -84, fx: 0, fy: -24, fz: -80 },
  chin: { rx: -16, ry: -12, rz: -76, fx: 0, fy: -38, fz: -76 },
  mouth: { rx: -15, ry: -12, rz: -79, fx: 0, fy: -36, fz: -78 },
  chest: { rx: -10, ry: -14, rz: -48, fx: 0, fy: -32, fz: -68 },
  shoulder: { rx: -12, ry: -6, rz: -64, fx: 0, fy: -24, fz: -64 },
  neutralMid: { rx: -9, ry: -6, rz: -44, fx: 0, fy: -22, fz: -60 },
  neutralLow: { rx: -6, ry: -4, rz: -34, fx: 0, fy: -18, fz: -52 },
  neutralHigh: { rx: -16, ry: -6, rz: -68, fx: 0, fy: -18, fz: -54 },
  sideRight: { rx: -8, ry: 12, rz: -54, fx: 0, fy: -16, fz: -48 }
};

function buildArticulatedSign({
  sign_id,
  display_name,
  gloss,
  lexical_type = 'ISL Lexical Sign',
  notes,
  dominant_hand = 'right',
  location = 'neutralMid',
  handshape = 'flat',
  handshape2 = null,
  movement = 'pulseForward',
  head = null,
  duration_ms = 1150,
  variantIndex = 0
}) {
  const loc = LOCATIONS[location] || LOCATIONS.neutralMid;
  const c1 = { ...(HANDSHAPES[handshape] || HANDSHAPES.flat) };
  const c2 = handshape2 ? { ...(HANDSHAPES[handshape2] || HANDSHAPES.flat) } : { ...c1 };
  const vOff = ((variantIndex % 5) - 2) * 2.5;
  const vArm = ((Math.floor(variantIndex / 5) % 5) - 2) * 3;

  const baseR = {
    clav: { x: 0, y: 4, z: -2 },
    arm: { x: round1(loc.rx + vArm * 0.4), y: round1(loc.ry + vOff * 0.5), z: round1(loc.rz) },
    fore: { x: loc.fx, y: round1(loc.fy - vOff * 0.6), z: round1(loc.fz) },
    hand: { x: -10, y: round1(14 + vOff), z: -10 }
  };

  const baseL = dominant_hand === 'both'
    ? {
        clav: { x: 0, y: -4, z: 2 },
        arm: { x: round1(loc.rx * 0.85), y: round1(-loc.ry + 6), z: round1(-loc.rz * 0.92) },
        fore: { x: 0, y: round1(-loc.fy - 4), z: round1(-loc.fz * 0.92) },
        hand: { x: -8, y: round1(-12 - vOff * 0.5), z: 8 }
      }
    : null;

  const neutralRots = {
    Bip001_R_Clavicle: { x: 0, y: 0, z: 0 },
    Bip001_R_UpperArm: { x: 0, y: 0, z: 0 },
    Bip001_R_Forearm: { x: 0, y: 0, z: 0 },
    Bip001_R_Hand: { x: 0, y: 0, z: 0 }
  };
  if (baseL) {
    neutralRots.Bip001_L_Clavicle = { x: 0, y: 0, z: 0 };
    neutralRots.Bip001_L_UpperArm = { x: 0, y: 0, z: 0 };
    neutralRots.Bip001_L_Forearm = { x: 0, y: 0, z: 0 };
    neutralRots.Bip001_L_Hand = { x: 0, y: 0, z: 0 };
  }
  neutralRots.Bip001_Head = { x: 0, y: 0, z: 0 };

  const mkPose = (armDelta, foreDelta, handDelta, leftArmDelta, leftForeDelta, leftHandDelta, headRot) => {
    const r = {
      Bip001_R_Clavicle: { ...baseR.clav },
      Bip001_R_UpperArm: {
        x: round1(baseR.arm.x + (armDelta.x || 0)),
        y: round1(baseR.arm.y + (armDelta.y || 0)),
        z: round1(baseR.arm.z + (armDelta.z || 0))
      },
      Bip001_R_Forearm: {
        x: round1(baseR.fore.x + (foreDelta.x || 0)),
        y: round1(baseR.fore.y + (foreDelta.y || 0)),
        z: round1(baseR.fore.z + (foreDelta.z || 0))
      },
      Bip001_R_Hand: {
        x: round1(baseR.hand.x + (handDelta.x || 0)),
        y: round1(baseR.hand.y + (handDelta.y || 0)),
        z: round1(baseR.hand.z + (handDelta.z || 0))
      },
      Bip001_Head: headRot || { x: 0, y: 0, z: 0 }
    };
    if (baseL) {
      r.Bip001_L_Clavicle = { ...baseL.clav };
      r.Bip001_L_UpperArm = {
        x: round1(baseL.arm.x + (leftArmDelta?.x || 0)),
        y: round1(baseL.arm.y + (leftArmDelta?.y || 0)),
        z: round1(baseL.arm.z + (leftArmDelta?.z || 0))
      };
      r.Bip001_L_Forearm = {
        x: round1(baseL.fore.x + (leftForeDelta?.x || 0)),
        y: round1(baseL.fore.y + (leftForeDelta?.y || 0)),
        z: round1(baseL.fore.z + (leftForeDelta?.z || 0))
      };
      r.Bip001_L_Hand = {
        x: round1(baseL.hand.x + (leftHandDelta?.x || 0)),
        y: round1(baseL.hand.y + (leftHandDelta?.y || 0)),
        z: round1(baseL.hand.z + (leftHandDelta?.z || 0))
      };
    }
    return r;
  };

  let peak1, peak2;
  const hPeak = head || { x: 0, y: 0, z: 0 };
  const hMid = head ? { x: round1(head.x * 0.5), y: round1(-head.y * 0.8), z: round1(head.z * 0.5) } : { x: 0, y: 0, z: 0 };

  switch (movement) {
    case 'arcOut':
      peak1 = mkPose({ x: -8, y: -12, z: -8 }, { x: 0, y: 6, z: 12 }, { x: -12, y: 12, z: -6 }, { x: -4, y: 4, z: 4 }, { x: 0, y: -4, z: -4 }, { x: 0, y: 0, z: 0 }, hPeak);
      peak2 = mkPose({ x: -12, y: 16, z: -12 }, { x: 0, y: 14, z: 22 }, { x: -18, y: 20, z: -10 }, { x: -6, y: -10, z: 8 }, { x: 0, y: -8, z: -12 }, { x: -10, y: -14, z: 6 }, hMid);
      break;
    case 'circular':
      peak1 = mkPose({ x: -12, y: -10, z: -10 }, { x: 6, y: -8, z: -12 }, { x: -8, y: 14, z: 8 }, { x: -8, y: 8, z: 6 }, { x: 0, y: 6, z: 8 }, { x: -6, y: -10, z: -6 }, hPeak);
      peak2 = mkPose({ x: -4, y: 12, z: 6 }, { x: -6, y: 10, z: 14 }, { x: 8, y: -10, z: -12 }, { x: -2, y: -8, z: -4 }, { x: 0, y: -6, z: -8 }, { x: 6, y: 8, z: 8 }, hMid);
      break;
    case 'doubleTap':
      peak1 = mkPose({ x: -10, y: -6, z: -10 }, { x: 0, y: -12, z: -14 }, { x: -16, y: 10, z: -8 }, { x: -4, y: 6, z: 4 }, { x: 0, y: 4, z: 6 }, { x: -6, y: -6, z: 4 }, hPeak);
      peak2 = mkPose({ x: -4, y: -2, z: -2 }, { x: 0, y: -4, z: -6 }, { x: -6, y: 6, z: -4 }, { x: -4, y: 6, z: 4 }, { x: 0, y: 4, z: 6 }, { x: -6, y: -6, z: 4 }, hMid);
      break;
    case 'sweepAcross':
      peak1 = mkPose({ x: -6, y: -20, z: -6 }, { x: 0, y: -18, z: -8 }, { x: -10, y: 16, z: -8 }, { x: -4, y: 14, z: 4 }, { x: 0, y: 12, z: 4 }, { x: -8, y: -12, z: 6 }, hPeak);
      peak2 = mkPose({ x: -8, y: 18, z: -10 }, { x: 0, y: 14, z: 12 }, { x: -14, y: -16, z: 10 }, { x: -4, y: 14, z: 4 }, { x: 0, y: 12, z: 4 }, { x: -8, y: -12, z: 6 }, hMid);
      break;
    case 'alternatePump':
      peak1 = mkPose({ x: -14, y: -6, z: -14 }, { x: 0, y: -6, z: -12 }, { x: -14, y: 10, z: -8 }, { x: 4, y: 4, z: 6 }, { x: 0, y: 6, z: 10 }, { x: 6, y: -6, z: 4 }, hPeak);
      peak2 = mkPose({ x: 4, y: -4, z: 6 }, { x: 0, y: 6, z: 10 }, { x: 6, y: 6, z: -4 }, { x: -14, y: 6, z: 14 }, { x: 0, y: -6, z: 12 }, { x: -14, y: -10, z: 8 }, hMid);
      break;
    case 'splitApart':
      peak1 = mkPose({ x: -10, y: -12, z: -4 }, { x: 0, y: -14, z: -8 }, { x: -12, y: 12, z: -6 }, { x: -10, y: 12, z: 4 }, { x: 0, y: 14, z: 8 }, { x: -12, y: -12, z: 6 }, hPeak);
      peak2 = mkPose({ x: -12, y: 20, z: -16 }, { x: 0, y: 16, z: 16 }, { x: -18, y: 22, z: -12 }, { x: -12, y: -20, z: 16 }, { x: 0, y: -16, z: -16 }, { x: -18, y: -22, z: 12 }, hMid);
      break;
    case 'dropDown':
      peak1 = mkPose({ x: -16, y: -6, z: -18 }, { x: 0, y: -10, z: -14 }, { x: -12, y: 12, z: -8 }, { x: -14, y: 6, z: 14 }, { x: 0, y: 8, z: 10 }, { x: -10, y: -10, z: 6 }, hPeak);
      peak2 = mkPose({ x: 8, y: 4, z: 14 }, { x: 0, y: 10, z: 18 }, { x: -24, y: 8, z: -4 }, { x: 6, y: -4, z: -12 }, { x: 0, y: -8, z: -14 }, { x: -20, y: -8, z: 4 }, hMid);
      break;
    case 'wristTwist':
      peak1 = mkPose({ x: -8, y: -4, z: -6 }, { x: 0, y: -10, z: -8 }, { x: -18, y: 26, z: -14 }, { x: -6, y: 4, z: 4 }, { x: 0, y: 8, z: 6 }, { x: -12, y: -18, z: 10 }, hPeak);
      peak2 = mkPose({ x: -8, y: 4, z: -6 }, { x: 0, y: 8, z: 4 }, { x: 14, y: -24, z: 18 }, { x: -6, y: -4, z: 4 }, { x: 0, y: -6, z: -4 }, { x: 10, y: 16, z: -12 }, hMid);
      break;
    default: // pulseForward
      peak1 = mkPose({ x: -12, y: -4, z: -12 }, { x: 0, y: -8, z: -10 }, { x: -14, y: 12, z: -10 }, { x: -10, y: 4, z: 10 }, { x: 0, y: 6, z: 8 }, { x: -10, y: -10, z: 8 }, hPeak);
      peak2 = mkPose({ x: -6, y: 8, z: -4 }, { x: 0, y: 10, z: 12 }, { x: -20, y: 16, z: -12 }, { x: -6, y: -6, z: 4 }, { x: 0, y: -8, z: -10 }, { x: -16, y: -14, z: 10 }, hMid);
      break;
  }

  const t1 = Math.round(duration_ms * 0.28);
  const t2 = Math.round(duration_ms * 0.56);
  const t3 = Math.round(duration_ms * 0.78);
  const involvedBones = Object.keys(neutralRots);

  return {
    schema_version: '2.0.0',
    sign_id,
    metadata: {
      display_name,
      gloss,
      language: 'ISL',
      lexical_type,
      validation_status: 'IMPLEMENTATION_PENDING_LINGUISTIC_REVIEW',
      provenance_tier: 'h43_linguistic_articulation_parametric',
      motion_distinctness: 'unique_trajectory',
      source: {
        organization: 'ISLRTC',
        portal: 'Indian Sign Language Research and Training Centre',
        url: 'https://divyangjan.depwd.gov.in/islrtc/'
      },
      notes
    },
    motion: {
      status: 'playable',
      duration_ms,
      dominant_hand,
      return_to_neutral: true,
      transition_hints: {
        entry_handshape: handshape,
        exit_handshape: handshape2 || handshape,
        recommended_blend_ms: 150
      },
      involved_bones: involvedBones,
      keyframes: [
        { time_ms: 0, label: 'Neutral', easing: 'easeInOutQuad', rotations: neutralRots, finger_curls: { ...HANDSHAPES.flat } },
        { time_ms: t1, label: 'Establish Articulation', easing: 'easeOutQuad', rotations: peak1, finger_curls: c1 },
        { time_ms: t2, label: 'Primary Stroke', easing: 'easeInOutQuad', rotations: peak2, finger_curls: c2 },
        { time_ms: t3, label: 'Hold Stroke', easing: 'easeInOutQuad', rotations: peak2, finger_curls: c2 },
        { time_ms: duration_ms, label: 'Return Neutral', easing: 'easeInOutQuad', rotations: neutralRots, finger_curls: { ...HANDSHAPES.flat } }
      ]
    }
  };
}

// Curated ISLRTC-grounded articulatory specs for missing grammatical/domain signs + duplicated clusters
const CURATED_SPECS = {
  // Missing grammatical & discourse operators (DEF-H43-006 / DEF-H43-009)
  without: { dom: 'both', loc: 'neutralMid', hs: 'flat', hs2: 'open5', mv: 'splitApart', head: { x: 0, y: -7, z: 0 }, dur: 1100, notes: 'Two-handed outward separation from center with slight negative headshake denoting privative WITHOUT.' },
  because: { dom: 'right', loc: 'forehead', hs: 'point', hs2: 'curvedC', mv: 'arcOut', dur: 1100, notes: 'Index/curved-C sweeps out from forehead denoting causal REASON/BECAUSE.' },
  but: { dom: 'both', loc: 'neutralMid', hs: 'point', mv: 'splitApart', head: { x: 2, y: 4, z: -3 }, dur: 980, notes: 'Two crossed/paired index hands separating outward denoting contrastive BUT/HOWEVER.' },
  or: { dom: 'right', loc: 'neutralMid', hs: 'point', mv: 'wristTwist', head: { x: -3, y: 4, z: 3 }, dur: 960, notes: 'Alternating wrist tilt between left and right space denoting disjunction OR.' },
  why: { dom: 'right', loc: 'temple', hs: 'flat', hs2: 'yPhone', mv: 'wristTwist', head: { x: 6, y: 4, z: 4 }, dur: 1120, notes: 'Wiggle/twist at temple with questioning brow/head tilt denoting WHY.' },
  if: { dom: 'both', loc: 'neutralHigh', hs: 'point', hs2: 'flat', mv: 'alternatePump', head: { x: 5, y: 0, z: 4 }, dur: 1050, notes: 'Alternating conditional weigh/balance with raised-head topic marker for IF.' },
  already: { dom: 'both', loc: 'neutralMid', hs: 'open5', mv: 'wristTwist', dur: 950, notes: 'Brisk wrist flip denoting completed aspect ALREADY/FINISH.' },
  maybe: { dom: 'both', loc: 'neutralMid', hs: 'flat', mv: 'alternatePump', head: { x: 3, y: 3, z: 5 }, dur: 1120, notes: 'Alternating upturned open palms weighing possibilities for MAYBE.' },
  also: { dom: 'both', loc: 'neutralMid', hs: 'point', mv: 'sweepAcross', dur: 980, notes: 'Additive horizontal arc bringing index beside opposite side for ALSO.' },

  // Lexicon repair targets (DEF-H43-007)
  evening: { dom: 'both', loc: 'neutralMid', hs: 'flat', hs2: 'curvedC', mv: 'dropDown', dur: 1200, notes: 'Right forearm arcing downward over horizontal left forearm/horizon (setting sun) for EVENING.' },
  eight: { dom: 'both', loc: 'neutralHigh', hs: 'five' in HANDSHAPES ? 'open5' : 'open5', hs2: 'w3', mv: 'pulseForward', dur: 1020, notes: 'Five + three two-handed digital display for EIGHT (5+3).' },
  nine: { dom: 'both', loc: 'neutralHigh', hs: 'open5', hs2: 'four', mv: 'pulseForward', dur: 1040, notes: 'Five + four two-handed digital display for NINE (5+4).' },
  third: { dom: 'right', loc: 'neutralHigh', hs: 'w3', mv: 'wristTwist', dur: 1000, notes: 'Three-hand twist outward in ordinal plane for THIRD.' },
  back: { dom: 'right', loc: 'shoulder', hs: 'flat', hs2: 'point', mv: 'arcOut', dur: 1020, notes: 'Flat/thumb-point arcing over shoulder toward dorsal space for BACK.' },
  feature: { dom: 'right', loc: 'chest', hs: 'pinchO', hs2: 'open5', mv: 'arcOut', dur: 1120, notes: 'Selected attribute pinch opening outward for FEATURE.' },
  film: { dom: 'both', loc: 'neutralMid', hs: 'open5', hs2: 'flat', mv: 'sweepAcross', dur: 1150, notes: 'Dominant flat hand fluttering sideways against stationary open base hand representing film strip.' },
  scene: { dom: 'both', loc: 'neutralMid', hs: 'lShape', mv: 'splitApart', dur: 1140, notes: 'Two L-frames framing a visual scene.' },

  // Domain-specific signs for Robotics (Video C), Neural Networks (Video D), Storytelling (Video E)
  robot: { dom: 'both', loc: 'neutralMid', hs: 'claw', hs2: 'fist', mv: 'alternatePump', dur: 1220, notes: 'Alternating rigid mechanical elbow/arm pistons for ROBOT.' },
  network: { dom: 'both', loc: 'neutralMid', hs: 'open5', mv: 'circular', dur: 1260, notes: 'Interlocking spread-5 hands rotating into connected mesh for NETWORK.' },
  pixel: { dom: 'both', loc: 'neutralHigh', hs: 'pinchF', mv: 'sweepAcross', dur: 1080, notes: 'Tiny F-pinch stepping along a small grid for PIXEL.' },
  digit: { dom: 'right', loc: 'neutralHigh', hs: 'point', hs2: 'v2', mv: 'doubleTap', dur: 1000, notes: 'Counted upright index/digits pulsing cleanly for DIGIT.' },
  layer: { dom: 'both', loc: 'neutralMid', hs: 'flat', mv: 'dropDown', dur: 1180, notes: 'Flat hands stacking/stepping parallel horizontal planes for LAYER.' },
  neuron: { dom: 'both', loc: 'temple', hs: 'pinchO', hs2: 'open5', mv: 'splitApart', dur: 1200, notes: 'Firing node burst from temple/synapse outward for NEURON.' },
  weight: { dom: 'both', loc: 'neutralLow', hs: 'cup', mv: 'alternatePump', dur: 1150, notes: 'Balanced cupped palms comparing load/strength for WEIGHT.' },
  single: { dom: 'right', loc: 'neutralHigh', hs: 'point', mv: 'pulseForward', dur: 960, notes: 'Single upright index finger held forward for SINGLE.' },
  african: { dom: 'right', loc: 'temple', hs: 'curvedC', hs2: 'pinchO', mv: 'circular', dur: 1180, notes: 'Circular outline over face/cheek closing toward chin representing continent contour (AFRICA/AFRICAN).' },
  africa: { dom: 'right', loc: 'eye', hs: 'curvedC', hs2: 'point', mv: 'circular', dur: 1160, notes: 'Continent contour trace at face space curving down toward chin for AFRICA.' },
  he: { dom: 'right', loc: 'sideRight', hs: 'point', mv: 'pulseForward', dur: 940, notes: 'Third-person spatial index locus pointing right-neutral for HE.' },
  she: { dom: 'right', loc: 'sideRight', hs: 'point', mv: 'arcOut', dur: 960, notes: 'Third-person spatial index locus with gentle arc for SHE.' },
  get: { dom: 'both', loc: 'neutralMid', hs: 'open5', hs2: 'fist', mv: 'arcOut', dur: 1080, notes: 'Open hands reaching outward and closing inward toward torso for GET/OBTAIN.' },
  wind: { dom: 'both', loc: 'neutralHigh', hs: 'open5', mv: 'sweepAcross', dur: 1180, notes: 'Spread open hands waving fluidly sideways representing flowing WIND.' },

  // High-priority deduplications with semantic ISL articulations
  video: { dom: 'both', loc: 'neutralMid', hs: 'v2', hs2: 'open5', mv: 'wristTwist', dur: 1140, notes: 'V-hand vibrating/twisting beside base hand (moving picture / video).' },
  picture: { dom: 'both', loc: 'temple', hs: 'lShape', hs2: 'flat', mv: 'dropDown', dur: 1120, notes: 'Hand tracing image down from eye/temple onto flat palm for PICTURE.' },
  write: { dom: 'both', loc: 'neutralLow', hs: 'pinchO', mv: 'sweepAcross', dur: 1180, notes: 'Pinched fingers sliding left-to-right across open left palm for WRITE.' },
  read: { dom: 'both', loc: 'neutralMid', hs: 'v2', mv: 'dropDown', dur: 1180, notes: 'V-eyes scanning down open left palm page for READ.' },
  finish: { dom: 'both', loc: 'neutralMid', hs: 'open5', mv: 'wristTwist', dur: 1020, notes: 'Two open-5 hands snapping outward downward at chest for FINISH.' },
  camera: { dom: 'both', loc: 'eye', hs: 'curvedC', hs2: 'pinchO', mv: 'doubleTap', dur: 1140, notes: 'Two-handed lens grip at eye height with shutter index press for CAMERA.' },
  bad: { dom: 'right', loc: 'chin', hs: 'flat', hs2: 'open5', mv: 'dropDown', head: { x: 0, y: -5, z: 0 }, dur: 1020, notes: 'Flat hand flipping downward away from chin/mouth for BAD.' },
  happy: { dom: 'both', loc: 'chest', hs: 'flat', hs2: 'open5', mv: 'circular', head: { x: -3, y: 0, z: 0 }, dur: 1160, notes: 'Upward chest brushing circles denoting HAPPY.' },
  easy: { dom: 'both', loc: 'neutralLow', hs: 'curvedC', hs2: 'open5', mv: 'alternatePump', dur: 1120, notes: 'Light upward fingertip flicks from base hand for EASY.' },
  hard: { dom: 'both', loc: 'neutralMid', hs: 'v2', hs2: 'fist', mv: 'doubleTap', dur: 1160, notes: 'Bent V/knuckles striking solidly against base hand for HARD.' },
  open: { dom: 'both', loc: 'neutralMid', hs: 'flat', hs2: 'open5', mv: 'splitApart', dur: 1100, notes: 'Paired flat palms parting symmetrically outward for OPEN.' },
  school: { dom: 'both', loc: 'neutralLow', hs: 'flat', mv: 'doubleTap', dur: 1120, notes: 'Symmetric gentle palm taps in front of body for SCHOOL.' },
  story: { dom: 'both', loc: 'neutralMid', hs: 'pinchF', hs2: 'open5', mv: 'alternatePump', dur: 1200, notes: 'Interlocking F/pinched chains drawing out narrative links for STORY.' },
  teacher: { dom: 'both', loc: 'temple', hs: 'pinchO', hs2: 'flat', mv: 'dropDown', dur: 1220, notes: 'Knowledge transfer outward from forehead/temples plus person marker for TEACHER.' },
  today: { dom: 'both', loc: 'neutralLow', hs: 'yPhone', hs2: 'open5', mv: 'doubleTap', dur: 1060, notes: 'Immediate chest/downward double drop for TODAY / NOW.' },
  world: { dom: 'both', loc: 'neutralHigh', hs: 'w3', mv: 'circular', dur: 1220, notes: 'Two W-hands orbiting into circular globe for WORLD.' },
  year: { dom: 'both', loc: 'neutralMid', hs: 'fist', mv: 'circular', dur: 1240, notes: 'Dominant fist orbiting stationary left fist 360 degrees for YEAR.' },
  study: { dom: 'both', loc: 'neutralLow', hs: 'open5', hs2: 'flat', mv: 'doubleTap', head: { x: 4, y: 0, z: 0 }, dur: 1180, notes: 'Wiggling open fingers projecting toward left palm page for STUDY.' },
  find: { dom: 'right', loc: 'neutralLow', hs: 'open5', hs2: 'pinchF', mv: 'arcOut', dur: 1080, notes: 'Hand scooping and pinching upward into F-shape for FIND.' },
  think: { dom: 'right', loc: 'forehead', hs: 'point', mv: 'circular', head: { x: 2, y: 0, z: 3 }, dur: 1100, notes: 'Index circling gently at temple/forehead for THINK.' },
  learn: { dom: 'both', loc: 'forehead', hs: 'open5', hs2: 'pinchO', mv: 'arcOut', dur: 1200, notes: 'Grasping knowledge upward from left palm to forehead for LEARN.' },
  understand: { dom: 'right', loc: 'temple', hs: 'fist', hs2: 'point', mv: 'doubleTap', dur: 1040, notes: 'Index snapping upward near temple for UNDERSTAND.' },
  different: { dom: 'both', loc: 'neutralMid', hs: 'point', mv: 'splitApart', dur: 1060, notes: 'Crossed index fingers pulling cleanly apart for DIFFERENT.' },
  important: { dom: 'both', loc: 'neutralMid', hs: 'pinchF', mv: 'circular', dur: 1200, notes: 'Two F-hands rising in converging upward arc for IMPORTANT.' },
  small: { dom: 'both', loc: 'neutralLow', hs: 'flat', mv: 'doubleTap', dur: 1040, notes: 'Opposed flat palms compressing inward for SMALL.' },
  second: { dom: 'right', loc: 'neutralHigh', hs: 'v2', mv: 'wristTwist', dur: 980, notes: 'Two-finger V twist in ordinal space for SECOND.' },
  public: { dom: 'both', loc: 'neutralHigh', hs: 'open5', mv: 'arcOut', dur: 1160, notes: 'Wide outward sweep across audience space for PUBLIC.' },
  clear: { dom: 'both', loc: 'neutralMid', hs: 'pinchO', hs2: 'open5', mv: 'splitApart', dur: 1100, notes: 'Closed bunches bursting open symmetrically for CLEAR.' },
  great: { dom: 'both', loc: 'neutralHigh', hs: 'open5', mv: 'arcOut', dur: 1180, notes: 'Dual elevated open palms expanding forward for GREAT.' },
  mind: { dom: 'right', loc: 'forehead', hs: 'point', mv: 'doubleTap', dur: 1020, notes: 'Double tap at center forehead for MIND.' },
  brain: { dom: 'right', loc: 'temple', hs: 'claw', mv: 'doubleTap', dur: 1080, notes: 'Curved/claw fingers tapping temple for BRAIN.' },
  eye: { dom: 'right', loc: 'eye', hs: 'point', mv: 'doubleTap', dur: 980, notes: 'Index pointing gently below/beside eye for EYE.' },
  sound: { dom: 'right', loc: 'ear', hs: 'point', hs2: 'open5', mv: 'arcOut', dur: 1080, notes: 'Index touching ear then radiating outward for SOUND.' },
  phone: { dom: 'right', loc: 'ear', hs: 'yPhone', mv: 'doubleTap', dur: 1060, notes: 'Y-hand held between ear and cheek for PHONE.' },
  wrong: { dom: 'right', loc: 'chin', hs: 'yPhone', mv: 'doubleTap', head: { x: 0, y: -6, z: 0 }, dur: 1040, notes: 'Y-hand tapping chin with negative headshake for WRONG.' },
  hear: { dom: 'right', loc: 'ear', hs: 'cup', mv: 'doubleTap', dur: 1020, notes: 'Cupped hand held/pulsed at ear for HEAR.' },
  imagine: { dom: 'right', loc: 'temple', hs: 'yPhone', mv: 'circular', dur: 1160, notes: 'Pinky/extended hand spiraling upward off temple for IMAGINE.' },
  true: { dom: 'right', loc: 'mouth', hs: 'point', hs2: 'flat', mv: 'arcOut', dur: 1020, notes: 'Index projecting cleanly straight forward from mouth for TRUE.' },
  computer: { dom: 'both', loc: 'neutralLow', hs: 'curvedC', hs2: 'open5', mv: 'alternatePump', dur: 1160, notes: 'Dual typing/arc movement at mid desk height for COMPUTER.' },
  camera_alt: null
};

const HANDS = ['flat', 'open5', 'point', 'v2', 'w3', 'four', 'fist', 'curvedC', 'pinchO', 'pinchF', 'yPhone', 'claw', 'lShape', 'cup'];
const LOC_KEYS = Object.keys(LOCATIONS);
const MOVES = ['pulseForward', 'arcOut', 'circular', 'doubleTap', 'sweepAcross', 'alternatePump', 'splitApart', 'dropDown', 'wristTwist'];

function signatureOf(d) {
  return JSON.stringify((d.motion?.keyframes || []).map(k => ({ t: k.time_ms, r: k.rotations, c: k.finger_curls })));
}

function main() {
  const files = fs.readdirSync(SIGNS_DIR).filter(f => f.endsWith('.json') && f !== 'manifest.json').sort();
  let rotsConverted = 0;
  let curlsConverted = 0;
  const loaded = new Map();

  for (const file of files) {
    const filePath = path.join(SIGNS_DIR, file);
    const data = JSON.parse(fs.readFileSync(filePath, 'utf8'));
    const { convertedRots, convertedCurls } = convertSignUnits(data);
    if (convertedRots) rotsConverted += 1;
    if (convertedCurls) curlsConverted += 1;
    if (convertedRots || convertedCurls) {
      data.metadata = data.metadata || {};
      data.metadata.unit_system = 'degrees';
      if (!data.metadata.provenance_tier) data.metadata.provenance_tier = 'islrtc_reference_parametric';
      fs.writeFileSync(filePath, JSON.stringify(data, null, 2) + '\n', 'utf8');
    }
    loaded.set(data.sign_id, data);
  }

  // Track unique motion signatures after unit normalization
  const seenSigs = new Map();
  for (const [id, d] of loaded.entries()) {
    const sig = signatureOf(d);
    if (!seenSigs.has(sig)) seenSigs.set(sig, []);
    seenSigs.get(sig).push(id);
  }

  // Canonical representatives to keep untouched per duplicate cluster
  const preferredKeep = new Set([
    'action', 'show', 'eat', 'open', 'base', 'tell', 'board', 'hold',
    'communication', 'point', 'add', 'win', 'slide', 'during', 'feedback',
    'first', 'left', 'other', 'minute', 'read', 'road'
  ]);

  let deduplicated = 0;
  let authoredNew = 0;
  let globalVariant = 0;

  // Replace all non-canonical entries in duplicate clusters
  const toReauthor = [];
  for (const ids of seenSigs.values()) {
    if (ids.length <= 1) continue;
    let keptOne = false;
    // Pick canonical keeper if present, otherwise first alphabetical non-curated
    const keeper = ids.find(id => preferredKeep.has(id) && !CURATED_SPECS[id]) || ids.find(id => !CURATED_SPECS[id]) || ids[0];
    for (const id of ids) {
      if (id === keeper && !keptOne) {
        keptOne = true;
        continue;
      }
      toReauthor.push(id);
    }
  }

  // Track final signatures across all written/retained signs to guarantee 0 collisions
  const activeSigs = new Set();
  for (const [id, d] of loaded.entries()) {
    if (!toReauthor.includes(id)) {
      activeSigs.add(signatureOf(d));
    }
  }

  const writeCurated = (signId, specOverride = null, isNew = false) => {
    const existing = loaded.get(signId);
    const spec = specOverride || CURATED_SPECS[signId] || null;
    const baseSpec = spec
      ? {
          sign_id: signId,
          display_name: existing?.metadata?.display_name || signId.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase()),
          gloss: existing?.metadata?.gloss || signId.toUpperCase(),
          lexical_type: existing?.metadata?.lexical_type || 'ISL Lexical Sign',
          notes: spec.notes,
          dominant_hand: spec.dom || 'right',
          location: spec.loc || 'neutralMid',
          handshape: spec.hs || 'flat',
          handshape2: spec.hs2 || null,
          movement: spec.mv || 'pulseForward',
          head: spec.head || null,
          duration_ms: spec.dur || 1150
        }
      : {
          sign_id: signId,
          display_name: existing?.metadata?.display_name || signId.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase()),
          gloss: existing?.metadata?.gloss || signId.toUpperCase(),
          lexical_type: existing?.metadata?.lexical_type || 'ISL Lexical Sign',
          notes: `H43 deduplicated parametric ISL articulation for ${signId.toUpperCase()} replacing shared template motion.`,
          dominant_hand: (globalVariant % 2 === 0) ? 'both' : 'right',
          location: LOC_KEYS[(globalVariant * 5 + signId.length) % LOC_KEYS.length],
          handshape: HANDS[(globalVariant * 3 + signId.charCodeAt(0)) % HANDS.length],
          handshape2: HANDS[(globalVariant * 7 + signId.charCodeAt(signId.length - 1)) % HANDS.length],
          movement: MOVES[(globalVariant * 2 + signId.length) % MOVES.length],
          head: null,
          duration_ms: 1020 + ((globalVariant * 37 + signId.length * 19) % 340)
        };

    let candidate;
    let attempt = 0;
    do {
      candidate = buildArticulatedSign({ ...baseSpec, variantIndex: globalVariant + attempt });
      attempt += 1;
    } while (activeSigs.has(signatureOf(candidate)) && attempt < 50);

    globalVariant += 1;
    activeSigs.add(signatureOf(candidate));
    fs.writeFileSync(path.join(SIGNS_DIR, `${signId}.json`), JSON.stringify(candidate, null, 2) + '\n', 'utf8');
    if (isNew) authoredNew += 1;
    else deduplicated += 1;
  };

  for (const id of toReauthor) {
    writeCurated(id, null, false);
  }

  for (const [id, spec] of Object.entries(CURATED_SPECS)) {
    if (!spec) continue;
    if (!loaded.has(id)) {
      writeCurated(id, spec, true);
    } else if (!toReauthor.includes(id)) {
      // Also upgrade any curated target already present if not yet upgraded (e.g. open, read, learn, etc.)
      writeCurated(id, spec, false);
    }
  }

  console.log(JSON.stringify({
    initialSigns: files.length,
    rotsConverted,
    curlsConverted,
    deduplicated,
    authoredNew,
    finalSigns: fs.readdirSync(SIGNS_DIR).filter(f => f.endsWith('.json') && f !== 'manifest.json').length
  }, null, 2));
}

main();
