// tools/validate_h30_complete_project.mjs
import fs from 'fs';
import path from 'path';
import assert from 'node:assert/strict';
import { execSync } from 'child_process';

console.log('======================================================================');
console.log('PHASE H30: MASTER PERFORMANCE & REGRESSION QUALITY GATE VALIDATOR');
console.log('======================================================================');

// 1. Check Accounting Reconciliation & Invariants
console.log('\n--- 1. Checking Mathematical Corpus Invariants ---');
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
assert.equal(acc.discrepancy, 0, 'Silent loss discrepancy must be exactly 0');
console.log('PASS: Corpus accounting invariant verified (23,258 tokens, 0 discrepancy).');

// 2. Check Playable Sign Manifest (570 Signs)
console.log('\n--- 2. Checking Playable Sign Library (570 Signs) ---');
const manifestPath = path.resolve('signs', 'manifest.json');
const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
const signCount = manifest.total_playable_signs || manifest.signs.length;
assert.equal(signCount, 570, 'Must have exactly 570 playable signs');
console.log('PASS: Sign library manifest verified (570 signs).');

// 3. Check All Documentation Deliverables
console.log('\n--- 3. Checking All 9 Phase H30 Documentation Deliverables ---');
const requiredDocs = [
  'docs/h30_initial_performance_audit.md',
  'docs/h30_bottleneck_analysis.md',
  'docs/h30_gpu_optimization_report.md',
  'docs/h30_incremental_processing_report.md',
  'docs/h30_pipeline_optimization_report.md',
  'docs/h30_performance_methodology.md',
  'docs/h30_full_video_acceptance.md',
  'docs/h30_final_project_report.md',
  'docs/h30_execution_timeline.md'
];

for (const doc of requiredDocs) {
  const p = path.resolve(doc);
  assert(fs.existsSync(p), `Missing required document: ${doc}`);
  const stats = fs.statSync(p);
  assert(stats.size > 200, `Document is suspiciously small: ${doc}`);
  console.log(`  [OK] ${doc.padEnd(45)} (${stats.size.toLocaleString()} bytes)`);
}
console.log('PASS: All 9 documentation deliverables verified.');

// 4. Check All Machine-Readable Data Deliverables
console.log('\n--- 4. Checking All 15 Machine-Readable Data Deliverables ---');
const requiredData = [
  'data/h30_initial_performance_baseline.json',
  'data/h30_pipeline_waterfall.json',
  'data/h30_progressive_audio_results.json',
  'data/h30_gpu_benchmark.json',
  'data/h30_incremental_asr_results.json',
  'data/h30_incremental_translation_results.json',
  'data/h30_video_readiness_results.json',
  'data/h30_asset_preload_benchmark.json',
  'data/h30_aether_render_results.json',
  'data/h30_extension_latency_results.json',
  'data/h30_timeline_precision_results.json',
  'data/h30_resource_usage.json',
  'data/h30_raw_benchmark_observations.json',
  'data/h30_performance_summary.json',
  'data/h30_execution_checkpoint.json'
];

for (const dataFile of requiredData) {
  const p = path.resolve(dataFile);
  assert(fs.existsSync(p), `Missing required data file: ${dataFile}`);
  const parsed = JSON.parse(fs.readFileSync(p, 'utf8'));
  assert(parsed, `Invalid JSON in ${dataFile}`);
  const stats = fs.statSync(p);
  console.log(`  [OK] ${dataFile.padEnd(45)} (${stats.size.toLocaleString()} bytes)`);
}
console.log('PASS: All 15 machine-readable data deliverables verified.');

// 5. Execute Specialized Quality Gates & Regression Suites
console.log('\n--- 5. Executing Specialized Test Suites ---');
const suites = [
  'tools/test_h30_full_video_acceptance.mjs',
  'tools/test_h30_progressive_acceptance.mjs',
  'tools/test_h30_incremental_translation_and_cache.mjs',
  'tools/benchmark_h30_asset_preload.mjs',
  'tools/test_h30_aether_rendering.mjs',
  'tools/test_h30_extension_latency.mjs',
  'tools/test_h30_timeline_precision.mjs',
  'tools/validate_h29_complete_project.mjs'
];

for (const s of suites) {
  console.log(`\n>>> Running ${s}...`);
  try {
    execSync(`node "${path.resolve(s)}"`, { stdio: 'inherit' });
    console.log(`[PASS] ${s}`);
  } catch (err) {
    console.error(`[FAIL] ${s} failed!`);
    throw err;
  }
}

console.log('\n======================================================================');
console.log('SUCCESS: ALL PHASE H30 MASTER QUALITY GATES & REGRESSIONS PASSED!');
console.log('======================================================================');
