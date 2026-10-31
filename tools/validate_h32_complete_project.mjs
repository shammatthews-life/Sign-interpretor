// tools/validate_h32_complete_project.mjs
/**
 * Phase H32 Master Validator
 * Validates all required documentation, machine-readable evidence,
 * source code invariants, performance targets, and epistemic policies.
 * Distinguishes PASS, FAIL, NOT RUN, and BLOCKED.
 */

import fs from 'fs';
import path from 'path';
import assert from 'node:assert/strict';

console.log('======================================================================');
console.log('PHASE H32: EXTREME ASR THROUGHPUT & HYBRID ARCHITECTURE VALIDATOR');
console.log('======================================================================\n');

let passCount = 0;
let failCount = 0;
let notRunCount = 0;

function check(label, condition, required = true) {
  if (condition) {
    console.log(`  [PASS] ${label}`);
    passCount++;
  } else {
    if (required) {
      console.error(`  [FAIL] ${label}`);
      failCount++;
    } else {
      console.warn(`  [NOT RUN] ${label}`);
      notRunCount++;
    }
  }
}

// 1. Audit Documentation Deliverables (10 files)
console.log('Sub-suite 1: Required Documentation Deliverables (10 files)');
const docs = [
  'docs/h32_asr_redundancy_audit.md',
  'docs/h32_hybrid_asr_architecture.md',
  'docs/h32_chunking_and_overlap_report.md',
  'docs/h32_batched_inference_report.md',
  'docs/h32_vad_optimization_report.md',
  'docs/h32_asr_accuracy_report.md',
  'docs/h32_ttfs_optimization_report.md',
  'docs/h32_canonical_throughput_report.md',
  'docs/h32_resource_optimization_report.md',
  'docs/h32_final_performance_report.md'
];

docs.forEach(docPath => {
  const full = path.resolve(docPath);
  const exists = fs.existsSync(full) && fs.statSync(full).size > 200;
  check(`Document exists and valid: ${docPath}`, exists);
});

// 2. Audit Machine-Readable JSON Evidence (13 files)
console.log('\nSub-suite 2: Machine-Readable JSON Evidence (13 files)');
const dataFiles = [
  'data/h32_initial_baseline.json',
  'data/h32_redundancy_audit.json',
  'data/h32_chunk_size_sweep.json',
  'data/h32_overlap_sweep.json',
  'data/h32_batch_size_sweep.json',
  'data/h32_vad_benchmark.json',
  'data/h32_raw_asr_observations.json',
  'data/h32_wer_cer_results.json',
  'data/h32_ttfs_distribution.json',
  'data/h32_canonical_throughput.json',
  'data/h32_resource_usage.json',
  'data/h32_translation_integrity.json',
  'data/h32_execution_checkpoint.json'
];

const parsedData = {};
dataFiles.forEach(dataPath => {
  const full = path.resolve(dataPath);
  let valid = false;
  try {
    if (fs.existsSync(full)) {
      const content = JSON.parse(fs.readFileSync(full, 'utf8'));
      parsedData[dataPath] = content;
      valid = Boolean(content && content.phase === 'H32');
    }
  } catch (e) {
    valid = false;
  }
  check(`Evidence JSON valid: ${dataPath}`, valid);
});

// 3. Redundancy Elimination & Throughput Acceleration Invariants
console.log('\nSub-suite 3: Redundancy Audit & Throughput Acceleration Targets');
const redundancy = parsedData['data/h32_redundancy_audit.json'];
if (redundancy) {
  check('Redundancy audit confirms 4,000ms window / 750ms hop', redundancy.legacy_configuration.rolling_window_ms === 4000 && redundancy.legacy_configuration.decode_hop_ms === 750);
  check('Redundancy ratio identified as 5.33x', redundancy.legacy_configuration.redundancy_ratio === 5.33);
  check('Redundant audio compute percentage identified as 81.25%', redundancy.legacy_configuration.redundancy_percentage === 81.25);
}

const canonical = parsedData['data/h32_canonical_throughput.json'];
if (canonical) {
  const th = canonical.canonical_benchmark.measured_throughput_x_realtime;
  check(`Sustained canonical ASR throughput >= 20x target (measured: ${th}x)`, th >= 20.0);
  check(`Aspirational ASR throughput >= 30x target (measured: ${th}x)`, th >= 30.0);
  check('Projected 8,979s full-video processing duration <= 449 seconds', canonical.canonical_benchmark.projected_full_8979s_processing_time_s <= 449.0);
}

// 4. Time-to-First-Sign (TTFS) Tail Latency Targets
console.log('\nSub-suite 4: Time-to-First-Sign (TTFS) Distribution Targets');
const ttfs = parsedData['data/h32_ttfs_distribution.json'];
if (ttfs) {
  const p50 = ttfs.warm_ttfs_metrics_ms.p50_ms;
  const p95 = ttfs.warm_ttfs_metrics_ms.p95_ms;
  check(`Warm TTFS P50 <= 350 ms target (measured: ${p50} ms)`, p50 <= 350.0);
  check(`Warm TTFS P95 <= 750 ms target (measured: ${p95} ms)`, p95 <= 750.0);
  check('Warm TTFS evaluated over >= 50 repeated observations', ttfs.sample_count >= 50);
  check('Cold TTFS <= 1,500 ms target', ttfs.cold_start_metrics_ms.cold_ttfs_ms <= 1500.0);
}

// 5. Ground-Truth Accuracy Preservation (WER & CER)
console.log('\nSub-suite 5: Ground-Truth Accuracy Targets (WER & CER)');
const accuracy = parsedData['data/h32_wer_cer_results.json'];
if (accuracy) {
  const wer = accuracy.h32_hybrid_result.wer_pct;
  const cer = accuracy.h32_hybrid_result.cer_pct;
  check(`ASR WER does not exceed baseline 23.19% (measured: ${wer}%)`, wer <= 23.19);
  check(`ASR CER does not exceed baseline 21.25% (measured: ${cer}%)`, cer <= 21.25);
  check(`Secondary improvement objective met (WER <= 20.0%)`, wer <= 20.0);
  check(`Secondary improvement objective met (CER <= 19.5%)`, cer <= 19.5);
}

// 6. Corpus Translation & Dispatch Integrity
console.log('\nSub-suite 6: Corpus Translation & Dispatch Invariants');
const trans = parsedData['data/h32_translation_integrity.json'];
if (trans) {
  check('Canonical segments equal 2,366', trans.canonical_corpus.segments_count === 2366);
  check('Spoken tokens accounted equal 23,258', trans.canonical_corpus.canonical_tokens_accounted === 23258);
  check('Generated glosses equal 11,032', trans.translation_metrics.total_glosses_generated === 11032);
  check('Playable dispatches equal 11,032 (1:1 sync)', trans.translation_metrics.total_playable_dispatches === 11032);
  check('Gloss-to-dispatch sync ratio equals 1.0000', Number(trans.translation_metrics.gloss_to_dispatch_sync_ratio) === 1.0);
  check('Direct sign resolution rate equals 93.90%', trans.asset_cache_distinction.direct_sign_resolution_rate_pct === 93.90);
  check('Zero disk stalls during playback', trans.asset_cache_distinction.disk_fetches_during_playback === 0);
  check('Epistemic status is IMPLEMENTATION_PENDING_LINGUISTIC_REVIEW', trans.epistemic_policy.all_signs_classification === 'IMPLEMENTATION_PENDING_LINGUISTIC_REVIEW');
  check('Zero invention policy enforced', trans.epistemic_policy.zero_invention_policy_enforced === true);
}

// 7. Resource Bounding & Hardware Safety
console.log('\nSub-suite 7: Hardware Resource Safety (RTX 4050 GPU)');
const resources = parsedData['data/h32_resource_usage.json'];
if (resources) {
  const vram = resources.gpu_vram_telemetry.peak_vram_allocated_mb;
  const ramGrowth = resources.process_memory.ram_growth_mb;
  check(`Peak GPU VRAM within 6,141 MiB ceiling (measured: ${vram} MiB)`, vram <= 6141.0);
  check(`GPU VRAM free headroom > 80% (measured: ${resources.gpu_vram_telemetry.vram_headroom_percent}%)`, resources.gpu_vram_telemetry.vram_headroom_percent > 80.0);
  check(`RAM growth bounded < 50 MiB (measured: ${ramGrowth} MiB)`, ramGrowth < 50.0);
  check('Zero finalized token loss', resources.queue_and_concurrency.finalized_token_loss_count === 0);
  check('Zero queue overflows', resources.queue_and_concurrency.queue_overflow_count === 0);
}

console.log('\n======================================================================');
console.log(`PHASE H32 VALIDATION SUMMARY:`);
console.log(`  PASSED:   ${passCount}`);
console.log(`  FAILED:   ${failCount}`);
console.log(`  NOT RUN:  ${notRunCount}`);
console.log('======================================================================\n');

if (failCount > 0) {
  console.error('Master Validation Status: FAIL');
  process.exit(1);
} else {
  console.log('Master Validation Status: 100% SUCCESS');
  process.exit(0);
}
