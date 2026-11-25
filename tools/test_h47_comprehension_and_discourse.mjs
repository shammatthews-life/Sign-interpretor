/**
 * H47 Comprehension-Oriented, Discourse Continuity, NMM Scoping & Polysemy Audit.
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { EnglishToISLTranslator } from './avatar_viewer/EnglishToISLTranslator.js';
import { SignAnimationPlayer } from './avatar_viewer/SignAnimationPlayer.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '..');

function createMockSkeletonRig() {
  const bones = {};
  const bonesMap = new Map();
  for (const n of ['Bip001_Head', 'Bip001_Spine1', 'Bip001_R_UpperArm', 'Bip001_R_Forearm', 'Bip001_R_Hand']) {
    bones[n] = {
      name: n,
      isBone: true,
      position: { x: 0, y: 0, z: 0, copy(v) { this.x = v.x; this.y = v.y; this.z = v.z; }, clone() { return { x: this.x, y: this.y, z: this.z }; } },
      rotation: { x: 0, y: 0, z: 0, set(x, y, z) { this.x = x; this.y = y; this.z = z; }, copy(v) { this.x = v.x; this.y = v.y; this.z = v.z; }, clone() { return { x: this.x, y: this.y, z: this.z }; } }
    };
    bonesMap.set(n, bones[n]);
  }
  return { rigRoot: { traverse(fn) { Object.values(bones).forEach(fn); } }, bones, bonesMap };
}

const translator = new EnglishToISLTranslator();
const results = [];
const record = (id, pass, detail) => {
  results.push({ id, pass, detail });
  console.log(`[${pass ? 'PASS' : 'FAIL'}] ${id}: ${detail}`);
};

// 1. Cross-Cue Discourse Locus Persistence
const ctx = translator.createDiscourseContext();
const s1 = translator.translate('The teacher explained the plan.', { discourseContext: ctx });
const s2 = translator.translate('Then she helped the teacher.', { discourseContext: ctx });
const teacherLocus1 = s1.spatial_plan.locus_assignments.find(l => l.referent === 'teacher')?.locus;
const teacherLocus2 = s2.spatial_plan.locus_assignments.find(l => l.referent === 'teacher');
const sheLocus2 = s2.spatial_plan.locus_assignments.find(l => l.referent === 'she')?.locus;
record(
  'DISCOURSE_LOCUS_PERSISTENCE',
  Boolean(teacherLocus1 && teacherLocus2?.locus === teacherLocus1 && teacherLocus2?.persisted_from_discourse === true && sheLocus2 && sheLocus2 !== teacherLocus1),
  `teacher1=${teacherLocus1}, teacher2=${teacherLocus2?.locus} (persisted=${teacherLocus2?.persisted_from_discourse}), she2=${sheLocus2}`
);

// 2. Scoped NMMs (Not Broadcast Flatly to Unrelated Opening Nouns)
const negRes = translator.translate('Today the team did not finish the video.');
const firstScope = negRes.nmm_scopes[0] || [];
const hasNegScopeOnEnd = negRes.nmm_scopes.some(arr => arr.includes('NMM-NEG-HEADSHAKE'));
record(
  'NMM_CONSTITUENT_SCOPING',
  !firstScope.includes('NMM-NEG-HEADSHAKE') && hasNegScopeOnEnd,
  `firstSignScope=[${firstScope.join(',')}], scopes=${JSON.stringify(negRes.nmm_scopes)}`
);

// 3. Minimal-Pair NMM Contrast on Identical Manual Sign
const { rigRoot, bones, bonesMap } = createMockSkeletonRig();
const player = new SignAnimationPlayer(rigRoot, bonesMap, null);
const helpRaw = JSON.parse(fs.readFileSync(path.join(ROOT, 'signs/help.json'), 'utf8'));
const helpPlayable = { ...helpRaw.motion, sign_id: helpRaw.sign_id };
const tMid = Math.round(helpPlayable.duration_ms * 0.35);

player.loadSign(helpPlayable, { nonManualMarkers: [], spatialYawDeg: 0 });
player.applyFrame(tMid);
const neuY = bones.Bip001_Head.rotation.y;
const neuX = bones.Bip001_Head.rotation.x;

player.loadSign(helpPlayable, { nonManualMarkers: ['NMM-NEG-HEADSHAKE'], spatialYawDeg: 0 });
player.applyFrame(tMid);
const negY = bones.Bip001_Head.rotation.y;

player.loadSign(helpPlayable, { nonManualMarkers: ['NMM-YESNO-BROW-RAISE'], spatialYawDeg: 0 });
player.applyFrame(tMid);
const ynX = bones.Bip001_Head.rotation.x;

player.loadSign(helpPlayable, { nonManualMarkers: ['NMM-WH-BROW-FURROW'], spatialYawDeg: 0 });
player.applyFrame(tMid);
const whX = bones.Bip001_Head.rotation.x;

record(
  'NMM_MINIMAL_PAIR_CONTRAST',
  Math.abs(negY - neuY) > 0.05 && ynX < neuX - 0.04 && whX > neuX + 0.05,
  `negYawDelta=${(negY - neuY).toFixed(4)}, ynPitchDelta=${(ynX - neuX).toFixed(4)}, whPitchDelta=${(whX - neuX).toFixed(4)}`
);

// 4. Held-Out Generalization Benchmark (Strictly Separate from Locked A & B)
const gen = JSON.parse(fs.readFileSync(path.join(ROOT, 'artifacts/h47/h47_generalization_benchmark.json'), 'utf8'));
let genPass = 0;
for (const c of gen.cases) {
  const out = translator.translate(c.text);
  let ok = true;
  if (c.expect_signs_include) {
    ok = ok && c.expect_signs_include.every(s => out.sign_ids.includes(s));
  }
  if (c.forbid_signs) {
    ok = ok && c.forbid_signs.every(s => !out.sign_ids.includes(s));
  }
  if (c.expect_nmm) {
    ok = ok && c.expect_nmm.every(m => out.non_manual_markers.includes(m));
  }
  if (ok) genPass++;
  else console.log(`  [GEN MISS] ${c.id}: got signs=[${out.sign_ids.join(',')}] nmm=[${out.non_manual_markers.join(',')}]`);
}
record('GENERALIZATION_BENCHMARK', genPass === gen.cases.length, `${genPass}/${gen.cases.length} held-out cases passed`);

const passed = results.filter(r => r.pass).length;
console.log(`\nH47 Comprehension & Discourse Summary: ${passed}/${results.length} passed`);
if (passed !== results.length) process.exitCode = 1;
