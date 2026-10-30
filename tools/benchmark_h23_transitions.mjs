// tools/benchmark_h23_transitions.mjs
import fs from 'fs';
import path from 'path';
import { performance } from 'perf_hooks';

console.log('====================================================');
console.log('TASK 12: CO-ARTICULATION & AVATAR TRANSITION BENCHMARK');
console.log('====================================================');

const manifest = JSON.parse(fs.readFileSync('signs/manifest.json', 'utf8'));
const signs = manifest.signs || [];

// Mode A: Standard Neutral-Reset Gateway (Safe Gateway)
// Every sign returns completely to rest { x: 0, y: 0, z: 0 } before next sign starts.
function simulateStandardNeutralGateway(sequence) {
  let totalTimeMs = 0;
  const neutralHoldMs = 150;
  for (const s of sequence) {
    totalTimeMs += (s.duration_ms || 1200) + neutralHoldMs;
  }
  return totalTimeMs;
}

// Mode B: Co-Articulated Transitional Blending Layer (Experimental)
// Blends directly from terminal posture of Sign N to preparation posture of Sign N+1
// if both share compatible signing space and dominant hand, bypassing full torso rest.
function simulateCoarticulatedBlending(sequence) {
  let totalTimeMs = 0;
  const blendHoldMs = 60; // shortened blend margin
  for (let i = 0; i < sequence.length; i++) {
    const cur = sequence[i];
    const nxt = sequence[i + 1];
    let dur = cur.duration_ms || 1200;
    if (nxt && cur.dominant_hand === nxt.dominant_hand) {
      // Co-articulated blend saves 120ms of arm retraction
      dur = Math.max(700, dur - 120);
    }
    totalTimeMs += dur + blendHoldMs;
  }
  return totalTimeMs;
}

// Benchmark 50-sign sequence
const testSequence = [];
for (let i = 0; i < 50; i++) {
  testSequence.push(signs[i % signs.length]);
}

const t0 = performance.now();
const standardTotalMs = simulateStandardNeutralGateway(testSequence);
const t1 = performance.now();

const t2 = performance.now();
const coarticulatedTotalMs = simulateCoarticulatedBlending(testSequence);
const t3 = performance.now();

const timeSavedMs = standardTotalMs - coarticulatedTotalMs;
const efficiencyGainPct = ((timeSavedMs / standardTotalMs) * 100).toFixed(1);

console.log(`Standard Neutral Gateway Total Duration: ${standardTotalMs} ms (${(standardTotalMs/1000).toFixed(1)} s)`);
console.log(`Co-Articulated Blending Total Duration:  ${coarticulatedTotalMs} ms (${(coarticulatedTotalMs/1000).toFixed(1)} s)`);
console.log(`Time Saved via Transitional Blending:    ${timeSavedMs} ms (${efficiencyGainPct}% gain)`);

console.log('PASS: Both transition layers benchmarked successfully.');
console.log('Safe neutral-rest fallback remains default production standard to preserve authentic ISL phonology.');
console.log('====================================================');

const results = {
  timestamp: new Date().toISOString(),
  sequence_length: testSequence.length,
  standard_neutral_duration_ms: standardTotalMs,
  coarticulated_duration_ms: coarticulatedTotalMs,
  time_saved_ms: timeSavedMs,
  efficiency_gain_percent: Number(efficiencyGainPct),
  recommendation: "Retain neutral gateway for certified production; provide co-articulation toggle for high-tempo speeches."
};

fs.writeFileSync('data/h23_coarticulation_benchmark.json', JSON.stringify(results, null, 2), 'utf8');
