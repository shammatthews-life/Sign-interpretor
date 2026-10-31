// tools/test_h30_extension_latency.mjs
import fs from 'fs';
import path from 'path';
import assert from 'node:assert/strict';
import { performance } from 'perf_hooks';

console.log('======================================================================');
console.log('PHASE H30: WORKSTREAM H — BROWSER MESSAGE & EXTENSION LATENCY BENCHMARK');
console.log('======================================================================');

const transcriptPath = path.resolve('runtime', 'youtube', 'MXKkXXYUxBc', 'transcript.json');
const transcriptData = JSON.parse(fs.readFileSync(transcriptPath, 'utf8'));
const segments = transcriptData.segments || [];

// Simulate Chrome Extension Manifest V3 Messaging Bus
class MockMessagePort {
  constructor(name) {
    this.name = name;
    this.listeners = [];
  }
  addListener(fn) { this.listeners.push(fn); }
  postMessage(msg) {
    const serialized = JSON.stringify(msg);
    const deserialized = JSON.parse(serialized);
    for (const fn of this.listeners) {
      fn(deserialized);
    }
  }
}

// Strategy A: Granular token-by-token messaging (Unoptimized Legacy)
console.log('\n--- 1. Strategy A: Granular Per-Token Messaging ---');
const legacyPort = new MockMessagePort('legacy-stream');
let legacyReceivedCount = 0;
legacyPort.addListener(msg => { legacyReceivedCount++; });

const t0_legacy = performance.now();
for (let i = 0; i < 500; i++) {
  const seg = segments[i];
  const words = seg.text.split(' ');
  for (const w of words) {
    legacyPort.postMessage({
      type: 'DISPATCH_SIGN_COMMAND',
      segment_id: seg.segment_id,
      sign_id: w.toLowerCase(),
      timestamp: seg.start
    });
  }
}
const legacyElapsedMs = performance.now() - t0_legacy;
console.log(`Dispatched ${legacyReceivedCount} individual token messages in ${legacyElapsedMs.toFixed(2)} ms (${(legacyElapsedMs / legacyReceivedCount).toFixed(4)} ms/msg)`);

// Strategy B: Segment-Level Batched Command Payloads (H30 Optimized)
console.log('\n--- 2. Strategy B: Segment-Level Ordered Payload Streaming (H30) ---');
const optimizedPort = new MockMessagePort('h30-stream');
let optReceivedCount = 0;
let optReceivedSignsCount = 0;
const messageLatencies = [];

optimizedPort.addListener(payload => {
  optReceivedCount++;
  optReceivedSignsCount += payload.signs.length;
});

const t0_opt = performance.now();
for (let i = 0; i < 500; i++) {
  const seg = segments[i];
  const words = seg.text.split(' ');
  
  const t0_msg = performance.now();
  optimizedPort.postMessage({
    type: 'DISPATCH_SEGMENT_PAYLOAD',
    segment_id: seg.segment_id,
    start: seg.start,
    end: seg.end,
    signs: words.map((w, idx) => ({ id: w.toLowerCase(), order: idx })),
    fallbacks: []
  });
  messageLatencies.push(performance.now() - t0_msg);
}
const optElapsedMs = performance.now() - t0_opt;
console.log(`Dispatched ${optReceivedCount} segment payloads (${optReceivedSignsCount} signs) in ${optElapsedMs.toFixed(2)} ms (${(optElapsedMs / optReceivedCount).toFixed(4)} ms/payload)`);

const throughputGain = legacyElapsedMs / optElapsedMs;
console.log(`IPC Throughput Gain: ${throughputGain.toFixed(1)}x faster message handling!`);

messageLatencies.sort((a, b) => a - b);
const p50 = messageLatencies[Math.floor(messageLatencies.length * 0.5)];
const p90 = messageLatencies[Math.floor(messageLatencies.length * 0.9)];
const p95 = messageLatencies[Math.floor(messageLatencies.length * 0.95)];
const p99 = messageLatencies[Math.floor(messageLatencies.length * 0.99)];

console.log(`Latency Percentiles: P50=${p50.toFixed(4)} ms, P95=${p95.toFixed(4)} ms, P99=${p99.toFixed(4)} ms`);

// Write data/h30_extension_latency_results.json
const outputData = {
  phase: 'H30',
  segments_evaluated: 500,
  legacy_granular: {
    messages_sent: legacyReceivedCount,
    elapsed_ms: Number(legacyElapsedMs.toFixed(2)),
    ms_per_message: Number((legacyElapsedMs / legacyReceivedCount).toFixed(4))
  },
  optimized_batched: {
    messages_sent: optReceivedCount,
    signs_carried: optReceivedSignsCount,
    elapsed_ms: Number(optElapsedMs.toFixed(2)),
    ms_per_payload: Number((optElapsedMs / optReceivedCount).toFixed(4)),
    latency_p50_ms: Number(p50.toFixed(4)),
    latency_p90_ms: Number(p90.toFixed(4)),
    latency_p95_ms: Number(p95.toFixed(4)),
    latency_p99_ms: Number(p99.toFixed(4))
  },
  speedup_multiplier: Number(throughputGain.toFixed(1))
};

const outPath = path.resolve('data', 'h30_extension_latency_results.json');
fs.writeFileSync(outPath, JSON.stringify(outputData, null, 2), 'utf8');
console.log(`Saved ${outPath}`);

console.log('======================================================================');
console.log('SUCCESS: PHASE H30 EXTENSION LATENCY BENCHMARK COMPLETE');
console.log('======================================================================');
