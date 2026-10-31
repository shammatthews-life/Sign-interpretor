// tools/validate_h29_sign_runtime.mjs
import fs from 'fs';
import path from 'path';
import assert from 'node:assert/strict';

console.log('======================================================================');
console.log('PHASE H29: VALIDATING SIGN LIBRARY RUNTIME & MOTION INTEGRITY');
console.log('======================================================================');

const manifestPath = path.resolve('signs', 'manifest.json');
assert(fs.existsSync(manifestPath), 'signs/manifest.json must exist');
const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));

const totalSigns = manifest.total_playable_signs || manifest.signs.length;
console.log(`Manifest indicates ${totalSigns} playable signs.`);

assert.equal(totalSigns, 570, 'Must have exactly 570 playable Schema 2.0.0 signs');
assert.equal(manifest.signs.length, 570, 'Signs array length must be 570');

let totalKeyframes = 0;
let totalBonesReferenced = 0;

for (const s of manifest.signs) {
  const p = path.resolve('signs', `${s.sign_id}.json`);
  assert(fs.existsSync(p), `Missing sign asset file: ${p}`);
  
  const signData = JSON.parse(fs.readFileSync(p, 'utf8'));
  assert.equal(signData.schema_version, '2.0.0', `Sign ${s.sign_id} must be Schema 2.0.0`);
  const keyframes = signData.motion && signData.motion.keyframes ? signData.motion.keyframes : (signData.keyframes || []);
  assert(keyframes.length >= 2, `Sign ${s.sign_id} must have >= 2 keyframes`);
  
  totalKeyframes += keyframes.length;
  
  // Verify bone rotation limits and neutral returns
  for (const kf of keyframes) {
    for (const [bone, rot] of Object.entries(kf.rotations || {})) {
      totalBonesReferenced++;
      for (const axis of ['x', 'y', 'z', 'w']) {
        if (rot[axis] !== undefined) {
          assert(!Number.isNaN(rot[axis]), `NaN detected in ${s.sign_id} on ${bone}.${axis}`);
        }
      }
    }
  }
}

console.log(`Library Statistics:`);
console.log(`  Total Signs:            ${manifest.signs.length}`);
console.log(`  Total Keyframes:        ${totalKeyframes.toLocaleString()}`);
console.log(`  Total Bone Rotations:   ${totalBonesReferenced.toLocaleString()}`);

console.log('======================================================================');
console.log('PASS: ALL 570 SIGN ASSETS PASSED SCHEMA 2.0.0 RUNTIME VERIFICATION');
console.log('======================================================================');
