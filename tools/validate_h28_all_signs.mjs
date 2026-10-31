// tools/validate_h28_all_signs.mjs
import fs from 'fs';
import path from 'path';
import assert from 'node:assert/strict';

console.log('======================================================================');
console.log('PHASE H28: COMPREHENSIVE 566-SIGN ASSET & SCHEMA AUDIT');
console.log('======================================================================');

const manifestPath = path.resolve('signs', 'manifest.json');
assert(fs.existsSync(manifestPath), 'signs/manifest.json must exist');

const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
const signs = manifest.signs || [];
console.log(`Auditing sign manifest entries: ${signs.length}`);

let schemaCompliantCount = 0;
let neutralViolations = 0;
let nonFiniteErrors = 0;
let totalKeyframes = 0;
const signIdSet = new Set();
const duplicateIds = [];
const auditResults = [];

for (const signMeta of signs) {
  const sid = signMeta.sign_id;
  if (signIdSet.has(sid)) {
    duplicateIds.push(sid);
  }
  signIdSet.add(sid);

  const signPath = path.resolve('signs', `${sid}.json`);
  assert(fs.existsSync(signPath), `Sign file missing: ${signPath}`);

  const signData = JSON.parse(fs.readFileSync(signPath, 'utf8'));
  assert.equal(signData.schema_version, '2.0.0', `${sid} must adhere to Schema 2.0.0`);
  schemaCompliantCount++;

  const kfs = signData.motion?.keyframes || signData.keyframes || [];
  assert(kfs.length >= 2, `${sid} must contain >= 2 keyframes`);
  totalKeyframes += kfs.length;

  // Check neutral start & end
  const firstKf = kfs[0];
  const lastKf = kfs[kfs.length - 1];

  let neutralValid = true;
  for (const b of Object.keys(firstKf.rotations || {})) {
    const r = firstKf.rotations[b];
    if (r.x !== 0 || r.y !== 0 || r.z !== 0) neutralValid = false;
  }
  for (const b of Object.keys(lastKf.rotations || {})) {
    const r = lastKf.rotations[b];
    if (r.x !== 0 || r.y !== 0 || r.z !== 0) neutralValid = false;
  }
  if (!neutralValid) neutralViolations++;

  // Check finite values
  let isFinite = true;
  for (const kf of kfs) {
    for (const b of Object.keys(kf.rotations || {})) {
      const r = kf.rotations[b];
      if (!Number.isFinite(r.x) || !Number.isFinite(r.y) || !Number.isFinite(r.z)) {
        isFinite = false;
        nonFiniteErrors++;
      }
    }
  }

  auditResults.push({
    sign_id: sid,
    schema_version: signData.schema_version,
    keyframes: kfs.length,
    neutral_rest: neutralValid,
    is_finite: isFinite,
    two_handed: Boolean(signMeta.two_handed)
  });
}

console.log(`\nAudit Summary:`);
console.log(`  Total Audited Signs:     ${signs.length} / ${signs.length}`);
console.log(`  Schema 2.0.0 Compliant:  ${schemaCompliantCount}`);
console.log(`  Keyframes Inspected:     ${totalKeyframes}`);
console.log(`  Duplicate Sign IDs:      ${duplicateIds.length}`);
console.log(`  Neutral Rest Violations: ${neutralViolations}`);
console.log(`  Non-Finite Errors:       ${nonFiniteErrors}`);

assert.equal(signs.length, 566, 'Expected exactly 566 signs');
assert.equal(duplicateIds.length, 0, 'Must have zero duplicate IDs');
assert.equal(neutralViolations, 0, 'Must have zero neutral rest violations');
assert.equal(nonFiniteErrors, 0, 'Must have zero non-finite transforms');

console.log('\n======================================================================');
console.log('ALL 566 SIGN ASSETS PASS SCHEMA 2.0.0 & ARTICULATION AUDIT');
console.log('======================================================================');
