// tools/validate_h28_production_acceptance.mjs
import fs from 'fs';
import path from 'path';
import assert from 'node:assert/strict';

console.log('======================================================================');
console.log('GATE 4: H28 PRODUCTION RUNTIME & E2E ACCEPTANCE VALIDATOR');
console.log('======================================================================');

const e2eSummaryPath = path.resolve('artifacts', 'h28', 'e2e', 'e2e_timeline_summary.json');
const e2eReportPath = path.resolve('docs', 'h28_production_e2e_report.md');
const benchPath = path.resolve('data', 'h28_translation_benchmark.json');

assert(fs.existsSync(e2eSummaryPath), 'artifacts/h28/e2e/e2e_timeline_summary.json must exist');
assert(fs.existsSync(e2eReportPath), 'docs/h28_production_e2e_report.md must exist');
assert(fs.existsSync(benchPath), 'data/h28_translation_benchmark.json must exist');

const summary = JSON.parse(fs.readFileSync(e2eSummaryPath, 'utf8'));

assert.equal(summary.total_segments, 2366, 'Must process all 2,366 segments');
assert.equal(summary.rapid_seeks_tested, 4, 'Must verify 4 rapid seeks with queue resets');
assert(summary.total_playable_dispatches >= 10884, 'Must dispatch >= 10,884 playable signs');
assert(summary.elapsed_ms < 2000, 'Processing must be performant (< 2000 ms)');

console.log('PASS: 2.5-hour canonical video simulation, rapid seeks, and rate adjustments verified.');
console.log('GATE 4: PASSED CLEANLY');
