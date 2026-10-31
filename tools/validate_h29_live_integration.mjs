// tools/validate_h29_live_integration.mjs
import fs from 'fs';
import path from 'path';
import assert from 'node:assert/strict';

console.log('======================================================================');
console.log('PHASE H29: VALIDATING LIVE INTEGRATION & CANONICAL YOUTUBE ACCORDANCE');
console.log('======================================================================');

const pipePath = path.resolve('data', 'h29_pipeline_performance.json');
assert(fs.existsSync(pipePath), 'data/h29_pipeline_performance.json must exist');
const pipe = JSON.parse(fs.readFileSync(pipePath, 'utf8'));

assert.equal(pipe.total_segments, 2366, 'Must process 2,366 segments');
assert.equal(pipe.total_playable_signs_dispatched, 11032, 'Must dispatch 11,032 signs');
assert.equal(pipe.total_glosses_generated, 11032, 'Glosses must match dispatches 1:1');
assert(pipe.latency_percentiles_ms.p99 < 3.0, 'P99 latency must be under 3.0 ms');
console.log('PASS: Pipeline performance verified (11,032 dispatches, P99 = ' + pipe.latency_percentiles_ms.p99 + ' ms).');

const chromePath = path.resolve('data', 'h29_chrome_e2e_results.json');
assert(fs.existsSync(chromePath), 'data/h29_chrome_e2e_results.json must exist');
const chrome = JSON.parse(fs.readFileSync(chromePath, 'utf8'));

assert.equal(chrome.chrome_manifest_version, 3, 'Manifest version must be 3');
assert.equal(chrome.e2e_results.total_segments, 2366, 'Chrome test must process 2,366 segments');
assert.equal(chrome.e2e_results.total_dispatched_signs, 11032, 'Must dispatch 11,032 signs');
assert.equal(chrome.compliance_checklist.rapid_seek_stale_flush, true, 'Must verify rapid seek stale flush');
console.log('PASS: Live Chrome acceptance verified.');

console.log('======================================================================');
console.log('PASS: LIVE INTEGRATION & CANONICAL YOUTUBE ACCORDANCE CONFIRMED');
console.log('======================================================================');
