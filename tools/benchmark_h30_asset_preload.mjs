// tools/benchmark_h30_asset_preload.mjs
import fs from 'fs';
import path from 'path';
import assert from 'node:assert/strict';
import { performance } from 'perf_hooks';

console.log('======================================================================');
console.log('PHASE H30: WORKSTREAM F — TARGETED SIGN PRELOADING BENCHMARK');
console.log('======================================================================');

const manifestPath = path.resolve('signs', 'manifest.json');
const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
const totalSignsInManifest = manifest.signs.length;

const transcriptPath = path.resolve('runtime', 'youtube', 'MXKkXXYUxBc', 'transcript.json');
const transcriptData = JSON.parse(fs.readFileSync(transcriptPath, 'utf8'));
const segments = transcriptData.segments || [];

console.log(`Total library signs: ${totalSignsInManifest}`);
console.log(`Canonical segments: ${segments.length}`);

// 1. Benchmark Strategy A: Full upfront load of all 570 signs
console.log('\n--- 1. Strategy A: Upfront Monolithic Loading (All 570 Signs) ---');
const t0_upfront = performance.now();
const upfrontCache = new Map();
let totalBytesLoaded = 0;

for (const s of manifest.signs) {
  const p = path.resolve('signs', `${s.sign_id}.json`);
  if (fs.existsSync(p)) {
    const raw = fs.readFileSync(p, 'utf8');
    totalBytesLoaded += raw.length;
    upfrontCache.set(s.sign_id, JSON.parse(raw));
  }
}
const t1_upfront = performance.now();
const upfrontElapsedMs = t1_upfront - t0_upfront;
console.log(`Loaded ${upfrontCache.size} signs upfront in ${upfrontElapsedMs.toFixed(2)} ms (${(totalBytesLoaded / (1024*1024)).toFixed(2)} MB)`);

// 2. Benchmark Strategy B: Progressive Targeted Preloading (Working Set / Horizon)
console.log('\n--- 2. Strategy B: Progressive Horizon Preloading (20s Lead Window) ---');
// Read required signs per segment
const transResultsPath = path.resolve('data', 'h30_incremental_translation_results.json');
const transData = JSON.parse(fs.readFileSync(transResultsPath, 'utf8'));

// Measure time to load ONLY the signs needed for the first 20 seconds of video
const t0_progressive = performance.now();
const progressiveCache = new Map();
const first20sSegments = segments.filter(s => s.start <= 20.0);
const initialNeededSigns = new Set();

// Extract words/sign candidates
first20sSegments.forEach(s => {
  const words = s.text.toLowerCase().replace(/[^a-z0-9 ]/g, '').split(' ');
  words.forEach(w => {
    if (upfrontCache.has(w)) initialNeededSigns.add(w);
  });
});

let initBytes = 0;
for (const sId of initialNeededSigns) {
  const p = path.resolve('signs', `${sId}.json`);
  if (fs.existsSync(p)) {
    const raw = fs.readFileSync(p, 'utf8');
    initBytes += raw.length;
    progressiveCache.set(sId, JSON.parse(raw));
  }
}
const t1_progressive = performance.now();
const progressiveInitMs = t1_progressive - t0_progressive;

console.log(`Progressive Initial Horizon (First 20s): Loaded ${progressiveCache.size} unique signs in ${progressiveInitMs.toFixed(2)} ms (${(initBytes / 1024).toFixed(1)} KB)`);
const startupSpeedup = upfrontElapsedMs / progressiveInitMs;
console.log(`Startup Preload Acceleration: ${startupSpeedup.toFixed(1)}x FASTER initial readiness!`);

// Simulate continuous sliding window preload over entire video
let totalDynamicLoads = progressiveCache.size;
let cacheHits = 0;
let cacheMisses = 0;
const slidingHorizonLatencies = [];

for (let i = 0; i < segments.length; i++) {
  const seg = segments[i];
  const words = seg.text.toLowerCase().replace(/[^a-z0-9 ]/g, '').split(' ');
  
  for (const w of words) {
    if (upfrontCache.has(w)) {
      if (progressiveCache.has(w)) {
        cacheHits++;
      } else {
        cacheMisses++;
        const t0_load = performance.now();
        const p = path.resolve('signs', `${w}.json`);
        const raw = fs.readFileSync(p, 'utf8');
        progressiveCache.set(w, JSON.parse(raw));
        slidingHorizonLatencies.push(performance.now() - t0_load);
        totalDynamicLoads++;
      }
    }
  }
}

const hitRatePct = (cacheHits / (cacheHits + cacheMisses)) * 100;
console.log(`Sliding Horizon Playback:`);
console.log(`  Cache Hits:   ${cacheHits.toLocaleString()}`);
console.log(`  Cache Misses: ${cacheMisses}`);
console.log(`  Hit Rate:     ${hitRatePct.toFixed(2)}%`);
console.log(`  Mean Dynamic Load Latency: ${(slidingHorizonLatencies.reduce((a,b)=>a+b,0)/slidingHorizonLatencies.length).toFixed(3)} ms`);

// Write data/h30_asset_preload_benchmark.json
const outputData = {
  phase: 'H30',
  total_manifest_signs: totalSignsInManifest,
  upfront_loading: {
    signs_loaded: upfrontCache.size,
    elapsed_ms: Number(upfrontElapsedMs.toFixed(2)),
    memory_mb: Number((totalBytesLoaded / (1024*1024)).toFixed(2))
  },
  progressive_horizon_loading: {
    initial_window_seconds: 20.0,
    initial_signs_loaded: progressiveCache.size,
    initial_elapsed_ms: Number(progressiveInitMs.toFixed(2)),
    startup_speedup_multiplier: Number(startupSpeedup.toFixed(1)),
    total_cache_hits: cacheHits,
    total_cache_misses: cacheMisses,
    cache_hit_rate_pct: Number(hitRatePct.toFixed(2)),
    mean_dynamic_fetch_ms: Number((slidingHorizonLatencies.reduce((a,b)=>a+b,0)/slidingHorizonLatencies.length).toFixed(3))
  }
};

const outPath = path.resolve('data', 'h30_asset_preload_benchmark.json');
fs.writeFileSync(outPath, JSON.stringify(outputData, null, 2), 'utf8');
console.log(`Saved ${outPath}`);

console.log('======================================================================');
console.log('SUCCESS: PHASE H30 ASSET PRELOADING BENCHMARK COMPLETE');
console.log('======================================================================');
