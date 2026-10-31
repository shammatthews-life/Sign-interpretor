// tools/validate_h27_full_sign_library.mjs
/**
 * Whole-Library Schema & Articulation Regression Validator for Phase H27.
 * Audits all 566 signs in signs/manifest.json across keyframes, bones, and rest boundaries.
 */

import fs from 'fs';
import path from 'path';
import assert from 'node:assert/strict';

console.log('======================================================================');
console.log('PHASE H27: COMPLETE FULL 566-SIGN LIBRARY REGRESSION AUDIT');
console.log('======================================================================');

const manifestPath = path.resolve('signs', 'manifest.json');
assert(fs.existsSync(manifestPath), 'manifest.json must exist');

const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
const signs = manifest.signs || [];
console.log(`Total signs in manifest: ${signs.length}`);

let totalKeyframes = 0;
let schemaCompliantCount = 0;
let neutralViolations = 0;
let nonFiniteErrors = 0;
const signIdSet = new Set();
const duplicateIds = [];

for (const signMeta of signs) {
  const sid = signMeta.sign_id;
  if (signIdSet.has(sid)) {
    duplicateIds.push(sid);
  }
  signIdSet.add(sid);

  const signPath = path.resolve('signs', `${sid}.json`);
  assert(fs.existsSync(signPath), `Sign file missing: ${signPath}`);

  const signData = JSON.parse(fs.readFileSync(signPath, 'utf8'));
  assert.equal(signData.schema_version, '2.0.0', `${sid} must have schema_version 2.0.0`);
  schemaCompliantCount++;

  const kfs = signData.motion?.keyframes || signData.keyframes || [];
  assert(kfs.length >= 2, `${sid} must have >= 2 keyframes`);
  totalKeyframes += kfs.length;

  // Check neutral return
  const lastKf = kfs[kfs.length - 1];
  for (const b of Object.keys(lastKf.rotations || {})) {
    const r = lastKf.rotations[b];
    if (r.x !== 0 || r.y !== 0 || r.z !== 0) {
      neutralViolations++;
    }
  }

  // Check finite
  for (const kf of kfs) {
    for (const b of Object.keys(kf.rotations || {})) {
      const r = kf.rotations[b];
      if (!Number.isFinite(r.x) || !Number.isFinite(r.y) || !Number.isFinite(r.z)) {
        nonFiniteErrors++;
      }
    }
  }
}

console.log(`\nRegression Audit Results:`);
console.log(`  Total Audited Signs:     ${signs.length} / ${signs.length}`);
console.log(`  Schema 2.0.0 Compliant:  ${schemaCompliantCount}`);
console.log(`  Keyframes Inspected:     ${totalKeyframes}`);
console.log(`  Duplicate Sign IDs:      ${duplicateIds.length}`);
console.log(`  Neutral Rest Violations: ${neutralViolations}`);
console.log(`  Non-Finite Errors:       ${nonFiniteErrors}`);

assert.equal(duplicateIds.length, 0, 'No duplicate sign IDs permitted');
assert.equal(neutralViolations, 0, 'All signs must return to neutral rest');
assert.equal(nonFiniteErrors, 0, 'All transforms must be finite numbers');
assert.equal(signs.length, 566, 'Expected exactly 566 signs');

console.log('\n======================================================================');
console.log('ALL PHASE H27 FULL SIGN LIBRARY REGRESSION CHECKS PASSED FLAWLESSLY!');
console.log('======================================================================');