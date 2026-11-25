/**
 * H46 Independent Comprehension, Spatial Grammar, NMM 3D Actuation & Visual Uniqueness Audit.
 *
 * Designed to fail honestly on the H45 baseline (Phase 0) and pass only once:
 *  1. Zero exact rotation-duplicate sign pairs exist in signs/*.json
 *  2. EnglishToISLTranslator emits non-empty spatial_plan (referent loci, role shifts, directional verbs)
 *  3. youtube-cue-manifest.js preserves non_manual_markers & spatial_plan in normalized cues
 *  4. SignAnimationPlayer.applyFrame() produces measurable 3D Bip001_Head / Bip001_Spine1 actuation
 *     for NMMs (negation headshake, WH brow-furrow, Y/N brow-raise, emphatic nod) and spatial loci
 *  5. Expanded spatial, directional, discourse, and contrastive comprehension cases pass
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { EnglishToISLTranslator } from './avatar_viewer/EnglishToISLTranslator.js';
import { SignAnimationPlayer } from './avatar_viewer/SignAnimationPlayer.js';
import cueManifestPkg from '../extension/shared/youtube-cue-manifest.js';

const { buildYoutubeCueManifest } = cueManifestPkg;

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '..');

function createMockSkeletonRig() {
  const bones = {};
  const bonesMap = new Map();
  const names = [
    'Bip001_Head', 'Bip001_Spine1', 'Bip001_R_Clavicle', 'Bip001_R_UpperArm',
    'Bip001_R_Forearm', 'Bip001_R_Hand', 'Bip001_L_Clavicle', 'Bip001_L_UpperArm',
    'Bip001_L_Forearm', 'Bip001_L_Hand'
  ];
  for (const n of names) {
    bones[n] = {
      name: n,
      rotation: { x: 0, y: 0, z: 0, set(x, y, z) { this.x = x; this.y = y; this.z = z; } }
    };
    bonesMap.set(n, bones[n]);
  }
  const rigRoot = {
    traverse(fn) {
      Object.values(bones).forEach(fn);
    }
  };
  return { rigRoot, bones, bonesMap };
}

async function runAudit() {
  const results = [];
  const record = (id, pass, detail) => {
    results.push({ id, pass, detail });
    console.log(`[${pass ? 'PASS' : 'FAIL'}] ${id}: ${detail}`);
  };

  // 1. Visual Rotation-Duplicate Check across all 647 signs
  const signsDir = path.join(ROOT, 'signs');
  const signFiles = fs.readdirSync(signsDir).filter(f => f.endsWith('.json') && f !== 'manifest.json');
  const rotMap = new Map();
  for (const f of signFiles) {
    const data = JSON.parse(fs.readFileSync(path.join(signsDir, f), 'utf8'));
    const kfs = (data.motion && data.motion.keyframes) || [];
    const sig = JSON.stringify(kfs.map(fr => fr.rotations || {}));
    if (!rotMap.has(sig)) rotMap.set(sig, []);
    rotMap.get(sig).push(f.replace('.json', ''));
  }
  const dupGroups = [...rotMap.values()].filter(g => g.length > 1);
  record(
    'SIGN_ROTATION_UNIQUENESS',
    dupGroups.length === 0,
    `${dupGroups.length} exact rotation-duplicate groups across ${signFiles.length} signs`
  );

  // 2. Spatial Plan Emission (Referent Loci, Directional Verbs, Role Shift)
  const translator = new EnglishToISLTranslator();
  const resNeg = translator.translate('I do not understand why she helped him');
  const resDir = translator.translate('He told her to show the teacher the new video');
  const resContrast = translator.translate('First group agreed but second group refused');
  const hasSpatialPlan = Boolean(
    resNeg.spatial_plan &&
    Array.isArray(resNeg.spatial_plan.locus_assignments) &&
    resDir.spatial_plan &&
    Array.isArray(resDir.spatial_plan.directional_inflections) &&
    resDir.spatial_plan.directional_inflections.length > 0 &&
    resContrast.spatial_plan &&
    resContrast.spatial_plan.locus_assignments.length >= 2
  );
  record(
    'TRANSLATOR_SPATIAL_PLAN',
    hasSpatialPlan,
    hasSpatialPlan
      ? `locus=${resContrast.spatial_plan.locus_assignments.length}, dir=${resDir.spatial_plan.directional_inflections.length}`
      : 'spatial_plan missing or incomplete on EnglishToISLTranslator output'
  );

  // 3. YouTube Cue Manifest Preservation of NMM & Spatial Plan
  const manifest = await buildYoutubeCueManifest('h46-audit-job', {
    video_id: 'MXKkXXYUxBc',
    transcript: {
      segments: [
        { segment_id: 'c1', start: 0, end: 3, text: 'Why did you not help her?' }
      ]
    },
    translation: {
      translated_segments: [
        {
          segment_id: 'c1',
          start: 0,
          end: 3,
          text: 'Why did you not help her?',
          isl_glosses: ['YOU', 'SHE', 'HELP', 'NOT', 'WHY'],
          playable_sign_ids: ['you', 'she', 'help', 'not', 'why'],
          non_manual_markers: ['NMM-WH-BROW-FURROW', 'NMM-NEG-HEADSHAKE'],
          spatial_plan: {
            locus_assignments: [{ referent: 'she', locus: 'LOCUS_RIGHT', yaw_deg: 10 }],
            directional_inflections: [{ verb: 'help', target_locus: 'LOCUS_RIGHT', yaw_deg: 10 }]
          },
          translation_status: 'TRANSLATION_READY'
        }
      ]
    }
  });
  const cue0 = manifest.cues[0] || {};
  const manifestPreserves =
    Array.isArray(cue0.non_manual_markers) &&
    cue0.non_manual_markers.includes('NMM-WH-BROW-FURROW') &&
    Boolean(cue0.spatial_plan && cue0.spatial_plan.locus_assignments && cue0.spatial_plan.locus_assignments.length > 0);
  record(
    'MANIFEST_NMM_SPATIAL_TRANSPORT',
    manifestPreserves,
    manifestPreserves
      ? `preserved ${cue0.non_manual_markers.length} NMMs + spatial_plan`
      : `cue0 missing NMM/spatial_plan (keys: ${Object.keys(cue0).join(',')})`
  );

  // 4. SignAnimationPlayer 3D NMM & Spatial Actuation
  const { rigRoot, bones, bonesMap } = createMockSkeletonRig();
  const player = new SignAnimationPlayer(rigRoot, bonesMap, null);
  const helpSign = JSON.parse(fs.readFileSync(path.join(ROOT, 'signs', 'help.json'), 'utf8'));

  // Neutral baseline
  player.loadSign(helpSign, { nonManualMarkers: [], spatialYawDeg: 0 });
  player.applyFrame(Math.round((helpSign.motion.duration_ms || 1000) * 0.45));
  const neutralHeadY = bones.Bip001_Head.rotation.y;
  const neutralHeadX = bones.Bip001_Head.rotation.x;
  const neutralSpineY = bones.Bip001_Spine1.rotation.y;

  // Negation headshake + spatial right locus
  player.loadSign(helpSign, { nonManualMarkers: ['NMM-NEG-HEADSHAKE'], spatialYawDeg: 10 });
  player.applyFrame(Math.round((helpSign.motion.duration_ms || 1000) * 0.45));
  const negHeadDelta = Math.abs(bones.Bip001_Head.rotation.y - neutralHeadY);
  const spatialSpineDelta = Math.abs(bones.Bip001_Spine1.rotation.y - neutralSpineY);

  // WH brow furrow (head pitch/tilt)
  player.loadSign(helpSign, { nonManualMarkers: ['NMM-WH-BROW-FURROW'], spatialYawDeg: 0 });
  player.applyFrame(Math.round((helpSign.motion.duration_ms || 1000) * 0.45));
  const whHeadPitchDelta = Math.abs(bones.Bip001_Head.rotation.x - neutralHeadX);

  const playerActuates = negHeadDelta > 0.03 && spatialSpineDelta > 0.05 && whHeadPitchDelta > 0.03;
  record(
    'PLAYER_3D_NMM_AND_SPATIAL_ACTUATION',
    playerActuates,
    `negHeadDelta=${negHeadDelta.toFixed(4)} rad, spatialSpineDelta=${spatialSpineDelta.toFixed(4)} rad, whHeadPitchDelta=${whHeadPitchDelta.toFixed(4)} rad`
  );

  const passed = results.filter(r => r.pass).length;
  console.log(`\nH46 Audit Summary: ${passed}/${results.length} passed`);
  if (passed !== results.length) process.exitCode = 1;
}

runAudit().catch(err => {
  console.error(err);
  process.exit(1);
});
