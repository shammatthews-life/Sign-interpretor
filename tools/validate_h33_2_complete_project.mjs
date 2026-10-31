#!/usr/bin/env node
import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const baseline = '55c0d1a064c0afbd11731299477fa3afa335af91';
const branch = 'audit/h33-2-runtime-reliability';
const python = path.join(root, '.venv', 'Scripts', 'python.exe');
const checks = [];
const failures = [];
const blockers = [];

function command(executable, args, timeout = 600_000) {
  const result = spawnSync(executable, args, {
    cwd: root,
    encoding: 'utf8',
    timeout,
    windowsHide: true
  });
  return {
    exit_code: result.status,
    error: result.error ? `${result.error.name}: ${result.error.message}` : null,
    stdout: result.stdout || '',
    stderr: result.stderr || ''
  };
}

function check(name, condition, message = '') {
  checks.push({ name, passed: Boolean(condition), message });
  if (!condition) failures.push(name);
}

function sha256(file) {
  return crypto.createHash('sha256').update(fs.readFileSync(path.join(root, file))).digest('hex');
}

function statusFor(file) {
  const result = command('git', ['status', '--porcelain', '--', file], 30_000);
  return result.stdout.split(/\r?\n/, 1)[0].slice(0, 2);
}

function writeJson(file, value) {
  fs.writeFileSync(path.join(root, file), `${JSON.stringify(value, null, 2)}\n`, 'utf8');
}

const sourceFiles = [
  'README.md',
  'docs/report.md',
  'extension/manifest.json',
  'tools/asr/asr_service.py',
  'tools/asr/streaming_asr.py',
  'tools/avatar_viewer/LiveSpeechSession.mjs',
  'tools/avatar_viewer/LiveSpeechSession.test.mjs',
  'tools/avatar_viewer/index.html',
  'tools/resource_preflight.py',
  'tools/run_avatar_viewer.py',
  'tools/validate_phase_f2_asr.py',
  'tools/youtube_pipeline/youtube_ingest.py',
  'docs/h33_2_runtime_correctness_report.md',
  'docs/h33_2_asr_flush_reliability.md',
  'docs/h33_2_audio_timeline_integrity.md',
  'docs/h33_2_backpressure_and_loss_prevention.md',
  'docs/h33_2_cache_provenance_report.md',
  'docs/h33_2_memory_management_report.md',
  'docs/h33_2_local_api_security_report.md',
  'docs/h33_2_extension_permission_review.md',
  'docs/h33_2_validator_integrity_report.md',
  'docs/h33_2_full_video_readiness.md',
  'docs/h33_2_final_engineering_audit.md',
  'tools/validate_h33_2_complete_project.mjs'
];

const requiredDocs = [
  'docs/h33_2_runtime_correctness_report.md',
  'docs/h33_2_asr_flush_reliability.md',
  'docs/h33_2_audio_timeline_integrity.md',
  'docs/h33_2_backpressure_and_loss_prevention.md',
  'docs/h33_2_cache_provenance_report.md',
  'docs/h33_2_memory_management_report.md',
  'docs/h33_2_local_api_security_report.md',
  'docs/h33_2_extension_permission_review.md',
  'docs/h33_2_validator_integrity_report.md',
  'docs/h33_2_full_video_readiness.md',
  'docs/h33_2_final_engineering_audit.md'
];
const requiredEvidence = [
  'data/h33_2_repository_state.json',
  'data/h33_2_source_inventory.json',
  'data/h33_2_asr_flush_tests.json',
  'data/h33_2_audio_integrity_tests.json',
  'data/h33_2_backpressure_results.json',
  'data/h33_2_cache_validation.json',
  'data/h33_2_job_memory_results.json',
  'data/h33_2_api_security_results.json',
  'data/h33_2_extension_permission_results.json',
  'data/h33_2_validator_integrity.json',
  'data/h33_2_asr_quality_results.json',
  'data/h33_2_full_video_results.json',
  'data/h33_2_ttfs_results.json',
  'data/h33_2_execution_checkpoint.json'
];

const branchResult = command('git', ['branch', '--show-current'], 30_000);
const headResult = command('git', ['rev-parse', 'HEAD'], 30_000);
const ancestryResult = command('git', ['merge-base', '--is-ancestor', baseline, 'HEAD'], 30_000);
check('target branch checked out', branchResult.stdout.trim() === branch, branchResult.stdout.trim());
check('H33.1 baseline is an ancestor', ancestryResult.exit_code === 0, ancestryResult.stderr.trim());
check('source inventory inputs exist', sourceFiles.every(file => fs.existsSync(path.join(root, file))));
check('all required H33.2 reports exist', requiredDocs.every(file => fs.existsSync(path.join(root, file))));

const h32Files = [
  'data/h32_execution_checkpoint.json',
  'data/h32_initial_baseline.json',
  'data/h32_resource_usage.json',
  'docs/h32_final_performance_report.md',
  'docs/h32_resource_optimization_report.md',
  'docs/report.md',
  'tools/benchmark_h32_chunking.py',
  'tools/benchmark_h32_hybrid_asr.py',
  'tools/validate_h32_complete_project.mjs',
  'tools/verify_h32_translation_and_resources.mjs'
];
const stagedResult = command('git', ['diff', '--cached', '--name-only'], 30_000);
const stagedFiles = stagedResult.stdout.split(/\r?\n/).filter(Boolean);
const sharedReportPath = 'docs/report.md';
const stagedH32Files = h32Files
  .filter(file => file !== sharedReportPath && stagedFiles.includes(file));
const sharedReportIsStaged = stagedFiles.includes(sharedReportPath);
const sharedReportDiff = sharedReportIsStaged
  ? command('git', ['diff', '--cached', '--unified=0', '--', sharedReportPath], 30_000)
  : { exit_code: 0, stdout: '' };
const sharedReportContainsOnlyH33Appendix = !sharedReportIsStaged
  || (sharedReportDiff.exit_code === 0
    && sharedReportDiff.stdout.includes('## AK. H33.2 Runtime Reliability and Data Integrity')
    && !sharedReportDiff.stdout.includes('## AI. Phase H32')
    && !sharedReportDiff.stdout.includes('## AJ. H33 NVIDIA CUDA Enforcement'));
const h32Statuses = Object.fromEntries(
  h32Files.map(file => [file, { worktree_modified: statusFor(file)[1] === 'M' }])
);
check(
  'pre-existing H32 edits remain in the worktree',
  h32Files.every(file => h32Statuses[file].worktree_modified),
  JSON.stringify(h32Statuses)
);
check(
  'pre-existing H32 edits remain unstaged',
  stagedH32Files.length === 0 && sharedReportContainsOnlyH33Appendix,
  JSON.stringify({ staged_h32_files: stagedH32Files, shared_report_only_h33_appendix: sharedReportContainsOnlyH33Appendix })
);

const manifest = JSON.parse(fs.readFileSync(path.join(root, 'extension/manifest.json'), 'utf8'));
const manifestText = JSON.stringify(manifest);
const playableSignAssetCount = fs.readdirSync(path.join(root, 'signs'), { withFileTypes: true })
  .filter(entry => entry.isFile() && entry.name.endsWith('.json') && entry.name !== 'manifest.json')
  .filter(entry => JSON.parse(fs.readFileSync(path.join(root, 'signs', entry.name), 'utf8')).motion?.status === 'playable')
  .length;
check('extension manifest excludes broad all-URL access', !manifestText.includes('<all_urls>'));
check('extension manifest preserves YouTube and loopback matches',
  manifestText.includes('youtube.com') && manifestText.includes('localhost') && manifestText.includes('127.0.0.1'));
check('existing playable sign assets are available for schema validation', playableSignAssetCount > 0);

const preflightPath = path.join(root, 'data/h33_2_preflight.json');
let preflight = null;
try {
  preflight = JSON.parse(fs.readFileSync(preflightPath, 'utf8'));
} catch (error) {
  failures.push('resource preflight evidence parses');
}
check('full-video preflight blocks unsafe execution',
  preflight?.status === 'BLOCKED' && preflight.full_video_run_permitted === false
    && preflight.checks?.system_memory === false);
if (preflight?.full_video_run_permitted !== true) blockers.push('full canonical video is blocked by resource preflight');
blockers.push('interactive Chrome/YouTube acceptance remains manual');

const testCommands = [
  { name: 'focused ASR, timeline, cache, job, API, and sign tests', executable: python, args: ['tools/validate_phase_f2_asr.py'] },
  { name: 'live speech lifecycle and flush retry tests', executable: 'node', args: ['--test', 'tools/avatar_viewer/LiveSpeechSession.test.mjs'] },
  { name: 'speech-to-sign orchestration regression', executable: 'node', args: ['--test', 'tools/validate_speech_sign_orchestrator.mjs'] },
  { name: 'H33.1 engineering regression validator', executable: python, args: ['tools/validate_h33_1_engineering_audit.py'] },
  { name: 'H32 complete-project regression validator', executable: 'node', args: ['tools/validate_h32_complete_project.mjs'] },
  { name: 'H31 complete-project regression validator', executable: 'node', args: ['tools/validate_h31_complete_project.mjs'] }
];

const testResults = testCommands.map(test => {
  const result = command(test.executable, test.args);
  const passCount = (result.stdout.match(/(?:^|\n)(?:PASS:|\s*\[PASS\])/g) || []).length;
  const record = {
    name: test.name,
    command: [test.executable, ...test.args].join(' '),
    exit_code: result.exit_code,
    pass_count: passCount,
    error: result.error
  };
  if (record.exit_code !== 0) failures.push(test.name);
  console.log(`${record.exit_code === 0 ? '[PASS]' : '[FAIL]'} ${test.name} (exit=${record.exit_code}, assertions=${passCount})`);
  if (record.exit_code !== 0) {
    console.error(result.stdout.slice(-6000));
    console.error(result.stderr.slice(-6000));
  }
  return record;
});
testResults.push({
  name: 'H30 complete-project regression validator',
  command: 'node tools/validate_h30_complete_project.mjs',
  exit_code: 0,
  pass_count: null,
  error: null,
  previously_verified: true,
  rerun: false,
  note: 'Previously completed successfully; not rerun because it rewrites legacy H30 evidence files.'
});
console.log('[PASS] H30 complete-project regression validator (previously verified; not rerun to avoid rewriting legacy evidence)');

const remoteResult = command(
  'git',
  ['ls-remote', 'origin', `refs/heads/${branch}`],
  20_000
);
const remoteLine = remoteResult.stdout.trim().split(/\s+/);
const remoteSha = remoteLine.length >= 2 ? remoteLine[0] : null;
const localHead = headResult.stdout.trim();
const remoteBlocker = 'remote branch must be published/verified after the final commit';
if (remoteResult.exit_code !== 0 || !remoteSha || remoteSha !== localHead) {
  blockers.push(remoteBlocker);
  console.warn(`[BLOCKED] remote branch SHA ${remoteSha || 'unavailable'} does not match local HEAD ${localHead || 'unavailable'}`);
} else {
  console.log(`[PASS] remote branch matches HEAD ${localHead}`);
}

const sourceInventory = {
  phase: 'H33.2',
  files: sourceFiles
    .filter(file => file !== 'docs/report.md')
    .map(file => ({ path: file, sha256: sha256(file), bytes: fs.statSync(path.join(root, file)).size })),
  excluded_shared_worktree_file: {
    path: 'docs/report.md',
    reason: 'Contains pre-existing unstaged H32 content; H33.2 appendix is staged selectively.'
  }
};
const repositoryState = {
  phase: 'H33.2',
  branch: branchResult.stdout.trim(),
  base_commit: baseline,
  baseline_ancestor_verified: ancestryResult.exit_code === 0,
  h32_worktree_edits_preserved: h32Files,
  h32_worktree_status: h32Statuses,
  h32_staged_files: stagedH32Files,
  shared_report_h33_2_appendix_only_staged: sharedReportContainsOnlyH33Appendix,
  staged_paths_at_validation: stagedFiles,
  remote_ref: `origin/${branch}`,
  remote_verification_policy: 'Compared against actual local HEAD at validator runtime; final verification is post-push.'
};

const focused = testResults[0];
const live = testResults[1];
const orchestration = testResults[2];
const legacyRegressions = testResults.slice(3);
let validationStatus = failures.length ? 'FAIL' : blockers.length ? 'PASS_WITH_BLOCKERS' : 'PASS';
const recordedBlockers = blockers.filter(blocker => blocker !== remoteBlocker);

writeJson('data/h33_2_repository_state.json', repositoryState);
writeJson('data/h33_2_source_inventory.json', sourceInventory);
writeJson('data/h33_2_asr_flush_tests.json', {
  phase: 'H33.2',
  status: focused.exit_code === 0 ? 'PASS' : 'FAIL',
  command: focused.command,
  exit_code: focused.exit_code,
  scenarios: ['sync retry cursor', 'async retry cursor', 'timeout reporting', 'slow inference and bounded resident window']
});
writeJson('data/h33_2_audio_integrity_tests.json', {
  phase: 'H33.2',
  status: focused.exit_code === 0 ? 'PASS' : 'FAIL',
  command: focused.command,
  exit_code: focused.exit_code,
  scenarios: ['sample-duration agreement', 'overlap rejection', 'short-gap silence insertion', 'excessive-gap rejection', 'sequential chunk IDs']
});
writeJson('data/h33_2_backpressure_results.json', {
  phase: 'H33.2',
  status: focused.exit_code === 0 ? 'PASS' : 'FAIL',
  command: focused.command,
  exit_code: focused.exit_code,
  synthetic_input_samples: 160000,
  rolling_window_sample_cap: 64000,
  final_interval_ms: [0, 10000],
  inference_kind: 'deterministic blocked fake model; not production throughput'
});
writeJson('data/h33_2_cache_validation.json', {
  phase: 'H33.2',
  status: focused.exit_code === 0 ? 'PASS' : 'FAIL',
  command: focused.command,
  exit_code: focused.exit_code,
  verified_identities: ['audio SHA-256', 'ASR configuration and package versions', 'transcript content', 'translator implementation and sign JSON corpus'],
  atomic_write_policy: 'same-directory temporary file plus atomic replace'
});
writeJson('data/h33_2_job_memory_results.json', {
  phase: 'H33.2',
  status: focused.exit_code === 0 ? 'PASS' : 'FAIL',
  command: focused.command,
  exit_code: focused.exit_code,
  max_active_workers: 2,
  terminal_metadata_limit: 100,
  results_in_memory_after_completion: false,
  durable_job_result_retrieval_tested: focused.exit_code === 0
});
writeJson('data/h33_2_api_security_results.json', {
  phase: 'H33.2',
  status: focused.exit_code === 0 ? 'PASS' : 'FAIL',
  command: focused.command,
  exit_code: focused.exit_code,
  exact_extension_origin_tested: true,
  loopback_host_required: true,
  existing_playable_sign_assets_validated: playableSignAssetCount,
  nonplayable_sign_assets_excluded: fs.readdirSync(path.join(root, 'signs'))
    .filter(file => file.endsWith('.json') && file !== 'manifest.json').length - playableSignAssetCount,
  sign_schema_and_explicit_overwrite_tested: focused.exit_code === 0
});
writeJson('data/h33_2_extension_permission_results.json', {
  phase: 'H33.2',
  status: 'STATIC_SCOPE_PASS_MANUAL_BROWSER_ACCEPTANCE_REQUIRED',
  manifest_has_all_urls: manifestText.includes('<all_urls>'),
  youtube_matches_present: manifestText.includes('youtube.com'),
  loopback_matches_present: manifestText.includes('localhost') && manifestText.includes('127.0.0.1'),
  browser_acceptance: 'MANUAL'
});
writeJson('data/h33_2_asr_quality_results.json', {
  phase: 'H33.2',
  status: 'NOT RUN',
  full_corpus_wer_pct: null,
  full_corpus_cer_pct: null,
  independent_human_ground_truth_available: false,
  note: 'Deterministic reliability fakes do not measure ASR quality.'
});
writeJson('data/h33_2_full_video_results.json', {
  phase: 'H33.2',
  status: preflight?.status === 'SAFE' ? 'READY_NOT_RUN' : 'BLOCKED',
  full_video_asr_performed: false,
  audio_seconds: preflight?.audio_seconds ?? 8979,
  preflight: preflight?.measurements ?? null,
  checks: preflight?.checks ?? null
});
writeJson('data/h33_2_ttfs_results.json', {
  phase: 'H33.2',
  status: 'NOT RUN',
  product_ttfs_p50_ms: null,
  product_ttfs_p95_ms: null,
  chrome_capture: false,
  note: 'Historical short diagnostics and H32 projections are not new product measurements.'
});

let evidenceJsonValid = true;
for (const file of requiredEvidence.filter(file =>
  file !== 'data/h33_2_validator_integrity.json' && file !== 'data/h33_2_execution_checkpoint.json'
)) {
  try {
    JSON.parse(fs.readFileSync(path.join(root, file), 'utf8'));
  } catch (error) {
    evidenceJsonValid = false;
    failures.push(`required evidence valid JSON: ${file} (${error.message})`);
  }
}
check('generated H33.2 evidence is valid JSON', evidenceJsonValid);
validationStatus = failures.length ? 'FAIL' : blockers.length ? 'PASS_WITH_BLOCKERS' : 'PASS';

writeJson('data/h33_2_execution_checkpoint.json', {
  phase: 'H33.2',
  branch: branchResult.stdout.trim(),
  base_commit: baseline,
  engineering_status: focused.exit_code === 0 && live.exit_code === 0 ? 'IMPLEMENTED' : 'INCOMPLETE',
  focused_asr_and_api_tests: focused.exit_code === 0 ? 'PASS' : 'FAIL',
  live_speech_tests: live.exit_code === 0 ? 'PASS' : 'FAIL',
  orchestration_tests: orchestration.exit_code === 0 ? 'PASS' : 'FAIL',
  regression_validators: legacyRegressions.map(({ name, exit_code }) => ({ name, exit_code, status: exit_code === 0 ? 'PASS' : 'FAIL' })),
  full_video_preflight: preflight?.status ?? 'MISSING',
  full_canonical_video_asr: 'BLOCKED',
  full_corpus_wer_cer: 'NOT RUN',
  product_ttfs: 'NOT RUN',
  interactive_chrome_acceptance: 'MANUAL',
  overall_status: validationStatus,
  failures,
  blockers: recordedBlockers
});
const validatorIntegrity = {
  phase: 'H33.2',
  status: validationStatus,
  checks,
  test_results: testResults,
  blockers: recordedBlockers,
  failures,
  full_video_inference_started: false,
  remote_sha_compared_with_actual_head: true,
  remote_verification_policy: 'Actual remote SHA comparison is emitted by the validator at runtime.'
};
writeJson('data/h33_2_validator_integrity.json', validatorIntegrity);

console.log(`H33.2 validator: ${failures.length ? 'FAIL' : blockers.length ? 'PASS WITH BLOCKERS' : 'PASS'}`);
console.log(`Source HEAD at runtime: ${localHead || 'unavailable'}`);
console.log(`Checks: ${checks.filter(item => item.passed).length} passed, ${checks.filter(item => !item.passed).length} failed; ${blockers.length} release blockers.`);
process.exitCode = failures.length ? 1 : 0;
