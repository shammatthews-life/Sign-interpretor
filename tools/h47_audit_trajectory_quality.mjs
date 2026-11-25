/**
 * H47 Trajectory Quality & Motion Feature Clustering Audit across all 647 signs.
 * Checks anatomical bounds, duration bounds, finger-curl contrast, and bimanual/spatial diversity.
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '..');
const SIGNS_DIR = path.join(ROOT, 'signs');
const outDir = path.join(ROOT, 'artifacts/h47');
fs.mkdirSync(outDir, { recursive: true });

const files = fs.readdirSync(SIGNS_DIR).filter(f => f.endsWith('.json') && f !== 'manifest.json');
const clusters = { bimanual: 0, unimanual_high_curl: 0, unimanual_open_or_pointing: 0 };
const extremeJointWarnings = [];
let minDuration = Infinity;
let maxDuration = 0;

for (const f of files) {
  const data = JSON.parse(fs.readFileSync(path.join(SIGNS_DIR, f), 'utf8'));
  const dur = data.motion?.duration_ms || 0;
  if (dur < minDuration) minDuration = dur;
  if (dur > maxDuration) maxDuration = dur;

  const bones = data.motion?.involved_bones || [];
  const isBimanual = bones.some(b => b.startsWith('Bip001_L_'));
  const kfs = data.motion?.keyframes || [];

  let maxAbsDeg = 0;
  let maxCurl = 0;
  for (const kf of kfs) {
    for (const [bName, rot] of Object.entries(kf.rotations || {})) {
      for (const axis of ['x', 'y', 'z']) {
        const val = Math.abs(Number(rot[axis] || 0));
        if (val > maxAbsDeg) maxAbsDeg = val;
        if (val > 165) extremeJointWarnings.push({ sign: data.sign_id, bone: bName, axis, deg: val });
      }
    }
    for (const v of Object.values(kf.finger_curls || {})) {
      if (typeof v === 'number' && v > maxCurl) maxCurl = v;
    }
  }

  if (isBimanual) clusters.bimanual++;
  else if (maxCurl >= 0.4) clusters.unimanual_high_curl++;
  else clusters.unimanual_open_or_pointing++;
}

const report = {
  milestone: 'H47',
  total_signs_audited: files.length,
  duration_ms_range: [minDuration, maxDuration],
  extreme_joint_warnings_count: extremeJointWarnings.length,
  extreme_joint_warnings: extremeJointWarnings,
  feature_clusters: clusters
};

const outPath = path.join(outDir, 'h47_trajectory_quality_audit.json');
fs.writeFileSync(outPath, JSON.stringify(report, null, 2) + '\n', 'utf8');
console.log(`Audited ${files.length} signs | duration=[${minDuration}, ${maxDuration}]ms | extremeJointWarnings=${extremeJointWarnings.length} | clusters=${JSON.stringify(clusters)}`);
if (extremeJointWarnings.length > 0) process.exitCode = 1;
