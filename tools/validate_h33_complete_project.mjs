#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
let passed = 0;
let failed = 0;
let blocked = 0;
let manual = 0;

function check(label, condition) {
  if (condition) {
    console.log(`[PASS] ${label}`);
    passed++;
  } else {
    console.error(`[FAIL] ${label}`);
    failed++;
  }
}

function blockedCheck(label, condition, status = 'BLOCKED') {
  if (condition) {
    console.warn(`[${status}] ${label}`);
    if (status === 'MANUAL ACCEPTANCE REQUIRED') manual++;
    else blocked++;
  } else {
    check(label, false);
  }
}

function readJson(relativePath) {
  try {
    return JSON.parse(fs.readFileSync(path.join(root, relativePath), 'utf8'));
  } catch (error) {
    console.error(`[FAIL] Unable to read ${relativePath}: ${error.message}`);
    failed++;
    return null;
  }
}

console.log('H33 CUDA and end-to-end acceptance evidence validator');
const verification = readJson('data/h33_nvidia_gpu_verification.json');
const telemetry = readJson('data/h33_nvidia_gpu_telemetry.json');
const memory = readJson('data/h33_system_memory_telemetry.json');
const repository = readJson('data/h33_repository_state.json');
const checkpoint = readJson('data/h33_execution_checkpoint.json');
const sourceManifest = readJson('data/h33_canonical_source_manifest.json');
const resourceUsage = readJson('data/h33_resource_usage.json');
const fullVideo = readJson('data/h33_full_video_asr_results.json');
const throughput = readJson('data/h33_throughput_observations.json');
const ttfs = readJson('data/h33_ttfs_cold_warm_results.json');
const accuracy = readJson('data/h33_asr_quality_comparison.json');
const dispatch = readJson('data/h33_dispatch_fallback_accounting.json');
const chrome = readJson('data/h33_chrome_acceptance_results.json');
const longSession = readJson('data/h33_long_session_results.json');
const islReview = readJson('data/h33_isl_review_readiness.json');
const finalReadiness = readJson('data/h33_final_release_readiness.json');

if (verification && telemetry) {
  const inference = verification.inference || {};
  const processPid = verification.host_pid;
  const processObserved = telemetry.compute_process_samples_during_inference
    ?.some(sample => sample.processes?.some(process => process.pid === processPid));
  const gpuSamples = telemetry.gpu_samples_during_inference || [];
  check('GPU diagnostic reports PASS', verification.status === 'PASS');
  check(
    'NVIDIA RTX 4050 is verified at CUDA index 0',
    verification.gpu_environment?.gpu_name === 'NVIDIA GeForce RTX 4050 Laptop GPU'
      && verification.gpu_environment?.device_index === 0
      && verification.gpu_environment?.cuda_device_count > 0
  );
  check(
    'Faster-Whisper model was configured for CUDA index 0 float16',
    verification.model?.status === 'PASS'
      && verification.model?.device === 'cuda'
      && verification.model?.device_index === 0
      && verification.model?.compute_type === 'float16'
  );
  check(
    'Fresh model inference completed successfully',
    inference.status === 'PASS'
      && inference.actual_cuda_inference_succeeded === true
      && Array.isArray(inference.observations)
      && inference.observations.length > 0
  );
  check(
    'CTranslate2 and Faster-Whisper versions are recorded',
    typeof verification.package_versions?.ctranslate2 === 'string'
      && typeof verification.package_versions?.faster_whisper === 'string'
  );
  check(
    'nvidia-smi observed the diagnostic Python PID during inference',
    Number.isInteger(processPid) && processObserved === true
  );
  check(
    'Active-inference telemetry contains NVIDIA GPU samples and memory readings',
    gpuSamples.length > 0
      && gpuSamples.every(sample => sample.device_index === 0
        && sample.gpu_name === 'NVIDIA GeForce RTX 4050 Laptop GPU'
        && Number.isFinite(sample.memory_used_mb))
  );
}

if (sourceManifest && verification) {
  check(
    'Canonical source manifest matches the hashed diagnostic audio',
    sourceManifest.audio_sha256 === verification.source_audio?.sha256
      && sourceManifest.video_id === 'MXKkXXYUxBc'
      && Math.abs(sourceManifest.audio_format?.duration_s - 8978.9010625) < 0.01
      && sourceManifest.fresh_full_video_asr_performed === false
  );
}

if (resourceUsage && verification) {
  check(
    'Resource summary is limited to the measured short diagnostic',
    resourceUsage.status === 'SHORT CUDA DIAGNOSTIC MEASURED; FULL VIDEO NOT RUN'
      && resourceUsage.gpu?.python_pid_observed_by_nvidia_smi === verification.host_pid
      && resourceUsage.full_video_peak_ram_mb === null
      && resourceUsage.full_video_peak_vram_mb === null
  );
}

if (memory && telemetry) {
  const processSamples = telemetry.memory_samples || [];
  check(
    'System and Python process RAM telemetry was captured',
    memory.status === 'MEASURED'
      && Number.isFinite(memory.total_system_ram_gib)
      && Number.isFinite(memory.during_diagnostic?.available_ram_min_gib)
      && processSamples.some(sample => Number.isFinite(sample.process?.working_set_mb))
  );
}

if (repository) {
  check(
    'H32/H31 checkpoint and target branch are recorded',
    repository.repository?.audit_head_sha === 'b0b11afde3c914a748a96aede43123e4d16a6a36'
      && repository.repository?.h32_commit_verified === true
      && repository.repository?.h31_commit_verified === true
      && repository.repository?.branch === 'r1-articulation-coverage-and-report'
  );
  check(
    'Pre-existing H32 worktree changes are inventoried',
    Array.isArray(repository.preexisting_worktree_changes_preserved)
      && repository.preexisting_worktree_changes_preserved.length > 0
  );
}

if (checkpoint) {
  check(
    'Machine-readable checkpoint records the GPU diagnostic as PASS',
    checkpoint.acceptance?.nvidia_cuda_short_inference === 'PASS'
  );
  blockedCheck(
    'Full canonical video result remains explicitly blocked, not projected as complete',
    checkpoint.acceptance?.full_canonical_video_asr === 'BLOCKED'
      && checkpoint.status === 'BLOCKED'
  );
  blockedCheck(
    'Full-corpus accuracy, product TTFS, and dispatch reconciliation remain not run',
    checkpoint.acceptance?.full_corpus_wer_cer === 'NOT RUN'
      && checkpoint.acceptance?.cold_warm_product_ttfs === 'NOT RUN'
      && checkpoint.acceptance?.occurrence_level_dispatch_reconciliation === 'NOT RUN'
  );
  blockedCheck(
    'Interactive Chrome acceptance is correctly classified as manual',
    checkpoint.acceptance?.interactive_chrome_acceptance === 'MANUAL ACCEPTANCE REQUIRED',
    'MANUAL ACCEPTANCE REQUIRED'
  );
}

if (fullVideo) {
  blockedCheck(
    'No full-video PASS is claimed without a completed full-duration run',
    fullVideo.status === 'BLOCKED' && fullVideo.full_video_asr_performed === false
  );
}
if (throughput) {
  blockedCheck(
    'Full-video throughput is not confused with the H32 slice projection',
    throughput.status === 'NOT RUN'
      && throughput.full_video_observations.length === 0
      && throughput.h32_reference.classification === 'SLICE MEASUREMENT WITH FULL-DURATION PROJECTION'
  );
}
if (ttfs && accuracy && dispatch && chrome && longSession && islReview && finalReadiness) {
  blockedCheck('Product TTFS and full-corpus accuracy remain NOT RUN', ttfs.status === 'NOT RUN'
    && ttfs.warm_ttfs_p50_ms === null
    && accuracy.status === 'NOT RUN'
    && accuracy.full_corpus_wer_pct === null);
  blockedCheck('Occurrence reconciliation and long-session tests remain NOT RUN',
    dispatch.status === 'NOT RUN'
      && dispatch.counts.generated_gloss === null
      && longSession.status === 'NOT RUN');
  blockedCheck('Linguistic review is not misrepresented as completed',
    islReview.status === 'NOT RUN'
      && islReview.linguistic_review_status === 'NOT REVIEWED IN H33'
      && islReview.approval_changes_made === false);
  blockedCheck('Release readiness remains blocked pending required acceptance',
    finalReadiness.status === 'BLOCKED'
      && finalReadiness.full_canonical_asr === 'BLOCKED'
      && finalReadiness.chrome_user_acceptance === 'MANUAL ACCEPTANCE REQUIRED');
}
if (chrome) {
  blockedCheck(
    'Interactive browser acceptance is explicitly not performed',
    chrome.status === 'MANUAL ACCEPTANCE REQUIRED'
      && chrome.interactive_installed_extension_tested === false,
    'MANUAL ACCEPTANCE REQUIRED'
  );
}

for (const requiredFile of [
  'docs/h33_repository_checkpoint_audit.md',
  'docs/h33_nvidia_gpu_execution_report.md',
  'docs/h33_full_canonical_execution_report.md',
  'docs/h33_throughput_reproducibility_report.md',
  'docs/h33_ttfs_cold_warm_audit.md',
  'docs/h33_asr_accuracy_validation.md',
  'docs/h33_token_dispatch_reconciliation.md',
  'docs/h33_chrome_user_acceptance.md',
  'docs/h33_long_session_reliability.md',
  'docs/h33_isl_review_readiness.md',
  'docs/h33_final_release_readiness.md',
  'tools/diagnose_nvidia_gpu.py',
  'data/h33_repository_state.json',
  'data/h33_nvidia_gpu_verification.json',
  'data/h33_nvidia_gpu_telemetry.json',
  'data/h33_system_memory_telemetry.json',
  'data/h33_canonical_source_manifest.json',
  'data/h33_full_video_asr_results.json',
  'data/h33_full_video_stage_timings.json',
  'data/h33_throughput_observations.json',
  'data/h33_ttfs_cold_warm_results.json',
  'data/h33_asr_quality_comparison.json',
  'data/h33_token_occurrence_reconciliation.json',
  'data/h33_dispatch_fallback_accounting.json',
  'data/h33_chrome_acceptance_results.json',
  'data/h33_resource_usage.json',
  'data/h33_execution_checkpoint.json',
  'data/h33_long_session_results.json',
  'data/h33_isl_review_readiness.json',
  'data/h33_final_release_readiness.json',
]) {
  check(`Required H33 GPU/checkpoint artifact exists: ${requiredFile}`, fs.existsSync(path.join(root, requiredFile)));
}

console.log(`\nPASS: ${passed} | FAIL: ${failed} | BLOCKED: ${blocked} | MANUAL: ${manual}`);
if (failed > 0) {
  console.error('H33 evidence validation: FAIL');
  process.exitCode = 1;
} else if (blocked > 0 || manual > 0) {
  console.warn('H33 overall acceptance: BLOCKED (GPU milestone passed; end-to-end work remains).');
  process.exitCode = 2;
} else {
  console.log('H33 evidence validation: PASS');
}
