// tools/validate_h29_complete_project.mjs
import fs from 'fs';
import path from 'path';
import assert from 'node:assert/strict';
import { execSync } from 'child_process';

console.log('======================================================================');
console.log('PHASE H29: MASTER PROJECT QUALITY GATE & REGRESSION VALIDATOR');
console.log('======================================================================');

// 1. Check Accounting Reconciliation & Invariants
console.log('\n--- 1. Checking Mathematical & Corpus Accounting Invariant ---');
const accPath = path.resolve('data', 'h22_accounting_verified.json');
assert(fs.existsSync(accPath), 'data/h22_accounting_verified.json must exist');
const acc = JSON.parse(fs.readFileSync(accPath, 'utf8'));

const totalTokens = (
  acc.dispositions.IMPLEMENTED_PENDING_LINGUISTIC_REVIEW.tokens +
  acc.dispositions.GRAMMAR_OMISSION.tokens +
  acc.dispositions.PHRASE_TRANSLATED.tokens +
  acc.dispositions.FINGERSPELLED.tokens +
  acc.dispositions.SUBTITLE_FALLBACK.tokens
);

assert.equal(totalTokens, 23258, 'Corpus total must equal 23,258 tokens');
assert.equal(acc.discrepancy, 0, 'Silent loss discrepancy must be 0');
assert.equal(acc.dispositions.SUBTITLE_FALLBACK.tokens, 2226, 'Fallback count must be exactly 2,226 tokens');
console.log('PASS: Token accounting invariant verified (23,258 tokens, 0 discrepancy).');

// 2. Check Sign Manifest (570 Signs)
console.log('\n--- 2. Checking Playable Sign Library (570 Signs) ---');
const manifestPath = path.resolve('signs', 'manifest.json');
const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
const signCount = manifest.total_playable_signs || manifest.signs.length;
assert.equal(signCount, 570, 'Must have exactly 570 signs');
assert.equal(manifest.signs.length, 570, 'Manifest signs array must have 570 entries');
console.log('PASS: Sign library manifest verified (570 playable signs).');

// 3. Check All Documentation Deliverables
console.log('\n--- 3. Checking All Phase H29 Documentation Deliverables ---');
const requiredDocs = [
  'docs/h29_initial_baseline.md',
  'docs/h29_fallback_reduction_report.md',
  'docs/h29_asr_performance_report.md',
  'docs/h29_pipeline_optimization_report.md',
  'docs/h29_translation_quality_report.md',
  'docs/h29_chrome_acceptance_report.md',
  'docs/h29_execution_timeline.md',
  'docs/h29_final_project_report.md'
];

for (const doc of requiredDocs) {
  const p = path.resolve(doc);
  assert(fs.existsSync(p), `Missing required document: ${doc}`);
  const stats = fs.statSync(p);
  assert(stats.size > 200, `Document is suspiciously small: ${doc}`);
  console.log(`  [OK] ${doc.padEnd(45)} (${stats.size.toLocaleString()} bytes)`);
}
console.log('PASS: All documentation deliverables verified.');

// 4. Check All Machine-Readable Data Deliverables
console.log('\n--- 4. Checking Machine-Readable Data Deliverables ---');
const requiredData = [
  'data/h29_initial_baseline.json',
  'data/h29_remaining_fallback_inventory.json',
  'data/h29_remaining_fallback_frequency.csv',
  'data/h29_new_sign_results.json',
  'data/h29_fallback_resolution.json',
  'data/h29_asr_benchmark.json',
  'data/h29_pipeline_performance.json',
  'data/h29_translation_benchmark.json',
  'data/h29_translation_quality_results.json',
  'data/h29_phrase_quality_results.json',
  'data/h29_chrome_e2e_results.json',
  'data/h29_execution_checkpoint.json'
];

for (const dataFile of requiredData) {
  const p = path.resolve(dataFile);
  assert(fs.existsSync(p), `Missing required data file: ${dataFile}`);
  if (dataFile.endsWith('.json')) {
    const parsed = JSON.parse(fs.readFileSync(p, 'utf8'));
    assert(parsed, `Invalid JSON in ${dataFile}`);
  }
  const stats = fs.statSync(p);
  console.log(`  [OK] ${dataFile.padEnd(45)} (${stats.size.toLocaleString()} bytes)`);
}
console.log('PASS: All machine-readable data deliverables verified.');

// 5. Execute Sub-Validators
console.log('\n--- 5. Executing Specialized Quality Validators ---');
const validators = [
  'tools/validate_h29_fallback_resolution.mjs',
  'tools/validate_h29_translation_quality.mjs',
  'tools/validate_h29_asr_performance.mjs',
  'tools/validate_h29_sign_runtime.mjs',
  'tools/validate_h29_live_integration.mjs'
];

for (const v of validators) {
  console.log(`\n>>> Running ${v}...`);
  try {
    execSync(`node "${path.resolve(v)}"`, { stdio: 'inherit' });
    console.log(`[PASS] ${v}`);
  } catch (err) {
    console.error(`[FAIL] ${v} failed!`);
    throw err;
  }
}

console.log('\n======================================================================');
console.log('SUCCESS: ALL PHASE H29 QUALITY GATES AND VALIDATION SUITES PASSED!');
console.log('======================================================================');
