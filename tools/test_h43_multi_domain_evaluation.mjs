/**
 * tools/test_h43_multi_domain_evaluation.mjs
 *
 * H43 Workstream 5: Multi-Domain & 44-Case Linguistic Evaluation Suite.
 * Evaluates all 5 real-world videos (Public Speaking, Vlogging, Indian English Robotics,
 * Neural Networks STEM, TED Cultural Storytelling) plus the 44 linguistic challenge cases
 * using strictly decoupled technical, lexical, syntactic, and provenance scoring.
 */
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { EnglishToISLTranslator } from './avatar_viewer/EnglishToISLTranslator.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const root = path.resolve(__dirname, '..');

const refsPath = path.join(root, 'artifacts/h43/benchmark/h43_multi_domain_references.json');
const challengePath = path.join(root, 'artifacts/h43/benchmark/h43_linguistic_challenge_dataset.json');
const asrResultsPath = path.join(root, 'artifacts/h43/asr/h43_asr_experiment_results.json');
const outPath = path.join(root, 'artifacts/h43/benchmark/h43_multi_domain_evaluation.json');

const refs = JSON.parse(fs.readFileSync(refsPath, 'utf8'));
const challenges = JSON.parse(fs.readFileSync(challengePath, 'utf8'));
const diskSigns = new Set(
  fs.readdirSync(path.join(root, 'signs'))
    .filter(f => f.endsWith('.json') && f !== 'manifest.json')
    .map(f => f.replace('.json', ''))
);

const translator = new EnglishToISLTranslator();

// Optional: load best ASR config per video if benchmark has already completed
let bestAsrByVideo = new Map();
if (fs.existsSync(asrResultsPath)) {
  const asrData = JSON.parse(fs.readFileSync(asrResultsPath, 'utf8'));
  for (const exp of asrData.experiments || []) {
    if (exp.config === 'small.en_b5_norm') {
      bestAsrByVideo.set(exp.video_id, exp);
    }
  }
}

function evaluateSegmentList(segments, useAsrContext = false) {
  let totalSourceWords = 0;
  let glossCount = 0;
  let playableSignsCount = 0;
  let lexicalPlayableCount = 0;
  let fsPlayableCount = 0;
  let verifiedOnDiskCount = 0;
  let unverifiedSignIds = [];
  let unavailableCount = 0;
  let unknownCount = 0;
  const translatedSegments = [];

  for (const seg of segments) {
    const text = seg.source_text || seg.text || '';
    const words = text.trim().split(/\s+/).filter(Boolean);
    totalSourceWords += words.length;
    const asrContext = useAsrContext && Number.isFinite(seg.asr_confidence)
      ? { confidence: seg.asr_confidence, avg_logprob: seg.avg_logprob }
      : null;
    const res = translator.translate(text, { asrContext });

    glossCount += res.gloss_sequence.length;
    playableSignsCount += res.sign_ids.length;
    unavailableCount += res.unavailable_signs.length;
    unknownCount += res.unknown_terms.length;

    for (const sid of res.sign_ids) {
      if (sid.startsWith('fs_')) {
        fsPlayableCount += 1;
        verifiedOnDiskCount += 1;
      } else if (diskSigns.has(sid)) {
        lexicalPlayableCount += 1;
        verifiedOnDiskCount += 1;
      } else {
        unverifiedSignIds.push(sid);
      }
    }

    translatedSegments.push({
      start: seg.start,
      end: seg.end,
      source_text: text,
      gloss_sequence: res.gloss_sequence,
      sign_ids: res.sign_ids,
      unknown_terms: res.unknown_terms,
      fingerspelled_terms: res.fingerspelled_terms,
      status: res.status,
      asr_confidence: res.asr_confidence,
      clauses: res.intermediate_semantic_representation.clause_count
    });
  }

  return {
    segment_count: segments.length,
    source_word_count: totalSourceWords,
    gloss_occurrence_count: glossCount,
    playable_sign_count: playableSignsCount,
    lexical_playable_count: lexicalPlayableCount,
    fingerspelled_playable_count: fsPlayableCount,
    technical_disk_playability_pct: playableSignsCount ? Number(((verifiedOnDiskCount / playableSignsCount) * 100).toFixed(2)) : 0,
    unverified_sign_ids: [...new Set(unverifiedSignIds)],
    unavailable_sign_count: unavailableCount,
    unknown_term_count: unknownCount,
    concept_resolution_rate_pct: (glossCount + unknownCount)
      ? Number(((glossCount / (glossCount + unknownCount)) * 100).toFixed(2))
      : 0,
    translated_segments: translatedSegments
  };
}

// 1. Evaluate 5 Multi-Domain Videos (Human Reference + End-to-End ASR if ready)
const videoEvaluations = {};
for (const [vid, vref] of Object.entries(refs.videos)) {
  const refEval = evaluateSegmentList(vref.segments, false);
  const asrExp = bestAsrByVideo.get(vid);
  const asrEval = asrExp ? evaluateSegmentList(asrExp.segments, true) : null;
  videoEvaluations[vid] = {
    video_id: vid,
    title: vref.title,
    domain: vref.domain,
    ground_truth_status: vref.ground_truth_status,
    linguistic_validation_status: 'PENDING_DEAF_COMMUNITY_REVIEW',
    reference_translation: refEval,
    asr_e2e_translation: asrEval
      ? {
          asr_config: asrExp.config,
          asr_wer_pct: asrExp.wer_metrics.wer_pct,
          asr_rtf: asrExp.rtf,
          ...asrEval
        }
      : null
  };
}

// 2. Evaluate 44-Case Linguistic Challenge Suite
const challengeResults = [];
let challengePassed = 0;

for (const c of challenges.cases) {
  const res = translator.translate(c.text, { asrContext: c.asrContext || null });
  const failures = [];
  const gloss = res.gloss_sequence;
  const signs = res.sign_ids;

  // Verify every emitted sign_id is genuinely playable on disk or valid fs_
  for (const sid of signs) {
    if (!sid.startsWith('fs_') && !diskSigns.has(sid)) {
      failures.push(`Unplayable sign_id '${sid}' not found in signs/`);
    }
  }

  for (const g of c.mustInclude || []) {
    if (!gloss.includes(g)) failures.push(`Missing gloss '${g}' in [${gloss.join(' ')}]`);
  }
  for (const g of c.mustExclude || []) {
    if (gloss.includes(g)) failures.push(`Forbidden gloss '${g}' present in [${gloss.join(' ')}]`);
  }
  for (const [g, limit] of Object.entries(c.maxCount || {})) {
    const cnt = gloss.filter(x => x === g).length;
    if (cnt > limit) failures.push(`Gloss '${g}' count ${cnt} exceeded max ${limit}`);
  }
  for (const [a, b] of c.before || []) {
    const ia = gloss.indexOf(a);
    const ib = gloss.indexOf(b);
    if (ia === -1 || ib === -1 || ia >= ib) {
      failures.push(`Ordering failed: expected ${a}(${ia}) before ${b}(${ib}) in [${gloss.join(' ')}]`);
    }
  }
  for (const sid of c.mustIncludeSignIds || []) {
    if (!signs.includes(sid)) failures.push(`Missing sign_id '${sid}' in [${signs.join(' ')}]`);
  }
  for (const sid of c.mustExcludeSignIds || []) {
    if (signs.includes(sid)) failures.push(`Unexpected sign_id '${sid}' in [${signs.join(' ')}]`);
  }
  for (const unk of c.mustIncludeUnknown || []) {
    if (!res.unknown_terms.includes(unk)) failures.push(`Missing unknown_term '${unk}'`);
  }
  for (const m of c.mustContainMarker || []) {
    if (!res.non_manual_markers.includes(m)) failures.push(`Missing marker '${m}'`);
  }
  if (c.expectedStatus && res.status !== c.expectedStatus) {
    failures.push(`Status mismatch: got ${res.status}, expected ${c.expectedStatus}`);
  }

  const passed = failures.length === 0;
  if (passed) challengePassed += 1;
  challengeResults.push({
    id: c.id,
    category: c.category,
    passed,
    gloss_sequence: gloss,
    sign_ids: signs,
    unknown_terms: res.unknown_terms,
    status: res.status,
    failures
  });
}

const report = {
  milestone: 'H43',
  linguistic_validation_status: 'PENDING_DEAF_COMMUNITY_REVIEW',
  library_disk_sign_count: diskSigns.size,
  challenge_suite: {
    total: challenges.cases.length,
    passed: challengePassed,
    failed: challenges.cases.length - challengePassed,
    pass_rate_pct: Number(((challengePassed / challenges.cases.length) * 100).toFixed(2)),
    failures: challengeResults.filter(r => !r.passed),
    results: challengeResults
  },
  multi_domain_videos: videoEvaluations
};

fs.writeFileSync(outPath, JSON.stringify(report, null, 2) + '\n', 'utf8');

console.log('=== H43 44-CASE LINGUISTIC CHALLENGE SUITE ===');
console.log(`Passed: ${challengePassed}/${challenges.cases.length} (${report.challenge_suite.pass_rate_pct}%)`);
if (report.challenge_suite.failed > 0) {
  console.log('Failures:', JSON.stringify(report.challenge_suite.failures, null, 2));
}
console.log('\n=== H43 5-VIDEO MULTI-DOMAIN EVALUATION (REFERENCE) ===');
for (const [vid, ev] of Object.entries(videoEvaluations)) {
  const r = ev.reference_translation;
  console.log(`  ${vid} (${ev.domain}): segs=${r.segment_count}, words=${r.source_word_count}, playableSigns=${r.playable_sign_count} (lex=${r.lexical_playable_count}, fs=${r.fingerspelled_playable_count}), conceptRes=${r.concept_resolution_rate_pct}%, diskPlayable=${r.technical_disk_playability_pct}%, unknown=${r.unknown_term_count}`);
}
