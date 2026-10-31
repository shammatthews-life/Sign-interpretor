// tools/validate_h29_asr_performance.mjs
import fs from 'fs';
import path from 'path';
import assert from 'node:assert/strict';

console.log('======================================================================');
console.log('PHASE H29: VALIDATING ASR BENCHMARK & HARDWARE ACCELERATION');
console.log('======================================================================');

const asrPath = path.resolve('data', 'h29_asr_benchmark.json');
assert(fs.existsSync(asrPath), 'data/h29_asr_benchmark.json must exist');
const data = JSON.parse(fs.readFileSync(asrPath, 'utf8'));

console.log(`Hardware: ${data.hardware}`);
console.log(`Faster-Whisper: v${data.faster_whisper_version}`);
console.log(`CTranslate2: v${data.ctranslate2_version}`);
console.log(`Total benchmark trials: ${data.benchmarks.length}`);

assert(data.benchmarks.length >= 7, 'Must evaluate at least 7 model configurations');

// Find CUDA float16 base.en
const cudaBase = data.benchmarks.find(b => b.model === 'base.en' && b.device === 'cuda' && b.compute_type === 'float16' && b.vad_filter === true);
assert(cudaBase, 'Must have CUDA float16 base.en trial');

console.log(`\nCUDA Float16 base.en Results:`);
console.log(`  Inference Time: ${cudaBase.transcription_ms} ms (for ${cudaBase.audio_duration_s}s audio)`);
console.log(`  Real-Time Factor: ${cudaBase.real_time_factor}`);
console.log(`  Speedup: ${cudaBase.speedup_multiplier}x real time`);
console.log(`  Latency P50: ${cudaBase.latency_percentiles_ms.p50} ms`);
console.log(`  Latency P99: ${cudaBase.latency_percentiles_ms.p99} ms`);

assert(cudaBase.real_time_factor < 0.05, 'RTF must be strictly under 0.05 (at least 20x realtime)');
assert(cudaBase.speedup_multiplier >= 25.0, 'Speedup multiplier must be >= 25x realtime');

// Find CPU comparison
const cpuBase = data.benchmarks.find(b => b.model === 'base.en' && b.device === 'cpu');
if (cpuBase) {
  const speedupRatio = (cpuBase.transcription_ms / cudaBase.transcription_ms).toFixed(1);
  console.log(`\nCPU comparison: CPU took ${cpuBase.transcription_ms} ms (${speedupRatio}x slower than GPU)`);
  assert(cudaBase.transcription_ms < cpuBase.transcription_ms, 'GPU must be faster than CPU');
}

console.log('======================================================================');
console.log('PASS: ASR BENCHMARK & HARDWARE ACCELERATION FULLY VERIFIED');
console.log('======================================================================');
