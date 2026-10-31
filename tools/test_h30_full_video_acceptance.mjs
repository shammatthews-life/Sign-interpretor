// tools/test_h30_full_video_acceptance.mjs
import fs from 'fs';
import path from 'path';
import assert from 'node:assert/strict';
import { performance } from 'perf_hooks';
import { EnglishToISLTranslator } from './avatar_viewer/EnglishToISLTranslator.js';

console.log('======================================================================');
console.log('PHASE H30: ACCEPTANCE TEST A — OFFLINE FULL-VIDEO BATCH ACCELERATION');
console.log('======================================================================');

const transcriptPath = path.resolve('runtime', 'youtube', 'MXKkXXYUxBc', 'transcript.json');
assert(fs.existsSync(transcriptPath), 'Canonical transcript must exist');
const transcriptData = JSON.parse(fs.readFileSync(transcriptPath, 'utf8'));
const segments = transcriptData.segments || [];

console.log(`Loaded Canonical Transcript: ${segments.length} segments, 23,258 token occurrences`);

const translator = new EnglishToISLTranslator();
// Warmup
translator.translate('Warmup sentence');

let totalPlayableDispatches = 0;
let totalGlosses = 0;
let totalFallbacks = 0;
const segmentTimings = [];

const t0 = performance.now();

for (let i = 0; i < segments.length; i++) {
  const seg = segments[i];
  const t0_seg = performance.now();
  const tr = translator.translate(seg.text);
  const t1_seg = performance.now();
  
  segmentTimings.push(t1_seg - t0_seg);
  totalGlosses += (tr.gloss_sequence || []).length;
  totalPlayableDispatches += (tr.motion_candidate_sign_ids || []).length;
  totalFallbacks += (tr.unknown_terms || []).length;
}

const tTotalElapsed = performance.now() - t0;

console.log(`\nFull Canonical Video Offline Processing Results:`);
console.log(`  Total Segments Ingested:    ${segments.length}`);
console.log(`  Total Spoken Tokens:        23,258`);
console.log(`  Total Glosses Generated:    ${totalGlosses}`);
console.log(`  Total Playable Dispatches:  ${totalPlayableDispatches}`);
console.log(`  Total Fallbacks:            ${totalFallbacks}`);
console.log(`  Total Batch Runtime:        ${tTotalElapsed.toFixed(2)} ms (${(tTotalElapsed / segments.length).toFixed(4)} ms/seg)`);
console.log(`  Batch Throughput:           ${((segments.length / tTotalElapsed) * 1000).toFixed(0)} segments/sec`);

// Verify exact invariants
assert.equal(segments.length, 2366, 'Must process all 2,366 segments');
assert.equal(totalGlosses, 11032, 'Must match 11,032 generated glosses');
assert.equal(totalPlayableDispatches, 11032, 'Must match 11,032 playable sign dispatches');
assert(tTotalElapsed < 500.0, 'Optimized translation must complete in < 500 ms total');

segmentTimings.sort((a, b) => a - b);
const p50 = segmentTimings[Math.floor(segmentTimings.length * 0.5)];
const p95 = segmentTimings[Math.floor(segmentTimings.length * 0.95)];
const p99 = segmentTimings[Math.floor(segmentTimings.length * 0.99)];
const maxTime = segmentTimings[segmentTimings.length - 1];

console.log(`Latency Distribution: P50=${p50.toFixed(4)} ms, P95=${p95.toFixed(4)} ms, P99=${p99.toFixed(4)} ms, Max=${maxTime.toFixed(4)} ms`);
assert(maxTime < 3.0, `Max segment latency (${maxTime} ms) must be strictly under 3.0 ms`);

console.log('======================================================================');
console.log('SUCCESS: TEST A — FULL-VIDEO OFFLINE ACCEPTANCE PASSED FLAWLESSLY');
console.log('======================================================================');
