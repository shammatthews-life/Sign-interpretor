import fs from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url';
import { RuleBasedISLTranslator } from './avatar_viewer/EnglishToISLTranslator.js';
import { SpeechSignOrchestrator } from './avatar_viewer/SpeechSignOrchestrator.js';
import { SentenceProcessor } from './avatar_viewer/SentenceProcessor.js';

const here = path.dirname(fileURLToPath(import.meta.url));
const corpus = JSON.parse(await fs.readFile(path.join(here, 'fixtures', 'g3_translation_corpus.json'), 'utf8'));
const translator = new RuleBasedISLTranslator();
const baseline = new RuleBasedISLTranslator({ enableG3Improvements: false });
const countBy = (items, key) => Object.fromEntries([...new Set(items.map(key))].map(k => [k, items.filter(x => key(x) === k).length]));
const sum = values => values.reduce((a, b) => a + b, 0);
const classifyFailure = (item, result) => {
  const causes = [];
  if (result.unknown_terms.length) {
    if (item.category === 'unknown_proper_technical' || item.category === 'mixed_known_unknown') causes.push('unknown vocabulary');
    else if (item.category === 'time_expressions') causes.push('temporal ordering');
    else if (item.category === 'negation') causes.push('negation handling');
    else if (item.category === 'questions') causes.push('question handling');
    else causes.push('lexical gap');
  }
  if (result.unavailable_signs.length) causes.push('missing sign motion');
  if (item.category === 'time_expressions') causes.push('temporal ordering', 'insufficient linguistic evidence');
  if (item.category === 'longer_sentences' || item.category === 'function_word_heavy') causes.push('grammar gap');
  if (item.category === 'questions') causes.push('question handling');
  if (item.category === 'negation') causes.push('negation handling');
  return [...new Set(causes)];
};
const rows = corpus.map(item => {
  const result = translator.translate(item.text);
  const evaluation = result.status === 'TRANSLATION_SUPPORTED' ? 'SUPPORTED' : result.status === 'TRANSLATION_HEURISTIC' ? 'HEURISTIC' : result.gloss_sequence.length ? 'UNCERTAIN' : 'FAILURE';
  return { ...item, evaluation, failure_causes: classifyFailure(item, result), result };
});
const phraseCases = rows.filter(r => ['multi_word_phrases'].includes(r.category));
const phraseRecognized = phraseCases.filter(r => r.result.transformation_trace.some(x => x.stage === 'phrase_detection')).length;
const allCandidates = sum(rows.map(r => r.result.motion_candidate_sign_ids.length));
const unavailable = sum(rows.map(r => r.result.unavailable_signs.length));
const beforeUnknown = sum(corpus.map(x => baseline.translate(x.text).unknown_terms.length));
const afterUnknown = sum(rows.map(r => r.result.unknown_terms.length));
const categorySummary = Object.fromEntries([...new Set(rows.map(r => r.category))].map(category => {
  const group = rows.filter(r => r.category === category);
  return [category, { total: group.length, evaluations: countBy(group, r => r.evaluation), unknown_terms: sum(group.map(r => r.result.unknown_terms.length)), unavailable_signs: sum(group.map(r => r.result.unavailable_signs.length)), mean_translation_ms: Number((sum(group.map(r => sum(Object.values(r.result.timings_ms)))) / group.length).toFixed(3)) }];
}));
const conceptIds = Object.keys(translator.motionCatalog);
const coverage = {
  total_linguistic_concepts: conceptIds.length,
  technically_playable: conceptIds.filter(id => translator.motionCatalog[id].playable).length,
  incomplete_or_not_authored: conceptIds.filter(id => !translator.motionCatalog[id].playable).length,
  no_sign_entry_terms_in_corpus: [...new Set(rows.flatMap(r => r.result.unknown_terms))].sort(),
  missing_motion_frequency: countBy(rows.flatMap(r => r.result.unavailable_signs.map(x => x.sign_id)), x => x),
};
const summary = {
  total_sentences: rows.length,
  evaluations: countBy(rows, r => r.evaluation),
  phrase_recognition_rate: `${phraseRecognized}/${phraseCases.length}`,
  unknown_term_rate: `${afterUnknown}/${sum(rows.map(r => r.result.normalized_text.split(' ').filter(Boolean).length))}`,
  unavailable_sign_rate: `${unavailable}/${allCandidates}`,
  mean_translation_compute_ms: Number((sum(rows.map(r => sum(Object.values(r.result.timings_ms)))) / rows.length).toFixed(3)),
  failure_categories: countBy(rows.flatMap(r => r.failure_causes), x => x),
  before_after: { baseline_unknown_terms: beforeUnknown, improved_unknown_terms: afterUnknown, delta: afterUnknown - beforeUnknown },
};
// Deterministic live-pipeline probe: T0 is the first stable ASR text. This does
// not measure ASR; it isolates whether G2 adds queueing latency after text exists.
const schedulerProbe = {
  bonesMap: new Map(), onLifecycleEvent: null, enqueue(id) { this.onLifecycleEvent?.({ type: 'playback_start', id, atMs: performance.now() }); },
  getState() { return { queued: [], current: null }; }, pause() {}, resume() {}, cancel() {},
};
const t0 = performance.now();
const probe = new SpeechSignOrchestrator({ sentenceProcessor: new SentenceProcessor(), translator, signScheduler: schedulerProbe });
probe.start(t0);
probe.handleTranscriptEvent({ kind: 'FINAL_TRANSCRIPT', text: 'hello good morning', audio_start_ms: t0 });
const probeTiming = probe.getDiagnostics().timings;
summary.pipeline_latency_probe_ms = {
  t1_translation_complete_minus_t0: Number(sum(Object.values(translator.translate('hello good morning').timings_ms)).toFixed(3)),
  t2_first_sign_commit_minus_t0: Number(probeTiming.firstCommitLatencyMs.toFixed(3)),
  t3_aether_playback_minus_t0: Number(probeTiming.speechToAetherLatencyMs.toFixed(3)),
  queue_depth: probe.getDiagnostics().queueCount,
};
const report = { phase: 'G3', summary, category_summary: categorySummary, sign_coverage: coverage, failure_list: rows.filter(r => r.failure_causes.length).map(r => ({ id: r.id, source: r.text, causes: r.failure_causes })), sentences: rows.map(({ result, ...row }) => ({ ...row, normalized_english: result.normalized_text, transformation_trace: result.transformation_trace, gloss_sequence: result.gloss_sequence, sign_ids: result.sign_ids, unknown_terms: result.unknown_terms, unavailable_signs: result.unavailable_signs, translation_status: result.status, timing_ms: result.timings_ms })) };
const reportDir = path.resolve(here, '..', 'docs');
await fs.writeFile(path.join(reportDir, 'g3_translation_evaluation_report.json'), JSON.stringify(report, null, 2) + '\n');
const md = [`# G3 Translation Evaluation Report`, '', `Generated deterministically from ${rows.length} corpus sentences. This evaluates rule behavior; it is not a linguistic gold-standard score.`, '', `- Phrase recognition: ${summary.phrase_recognition_rate}`, `- Unknown-term rate: ${summary.unknown_term_rate}`, `- Unavailable-sign rate: ${summary.unavailable_sign_rate}`, `- Mean translation compute: ${summary.mean_translation_compute_ms} ms`, `- Outcomes: ${JSON.stringify(summary.evaluations)}`, `- Failure taxonomy: ${JSON.stringify(summary.failure_categories)}`, `- G3 targeted improvements: baseline unknown terms ${beforeUnknown} -> ${afterUnknown}.`, '', `## Sign coverage`, '', `- Linguistic concepts: ${coverage.total_linguistic_concepts}`, `- Playable motions: ${coverage.technically_playable}`, `- Incomplete/not-authored: ${coverage.incomplete_or_not_authored}`, `- Missing motion frequency: ${JSON.stringify(coverage.missing_motion_frequency)}`, '', `## Decision evidence`, '', `The report shows whether the limiting factor is linguistic coverage or avatar motion coverage. The current corpus is expected to surface substantially more unavailable motion concepts than playable ones; do not infer an ML requirement from these rule/asset gaps alone.`].join('\n') + '\n';
await fs.writeFile(path.join(reportDir, 'g3_translation_evaluation_report.md'), md);
console.log(JSON.stringify(summary, null, 2));
console.log(`PASS: G3 evaluated ${rows.length} deterministic sentences and wrote docs/g3_translation_evaluation_report.{json,md}`);
