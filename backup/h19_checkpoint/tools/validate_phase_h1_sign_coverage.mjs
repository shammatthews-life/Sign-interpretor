import fs from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url';

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, '..');
const readJson = async file => JSON.parse(await fs.readFile(path.join(root, file), 'utf8'));
const g3 = await readJson('docs/g3_translation_evaluation_report.json');
const dictionary = await readJson('isl_accessibility/data/sign_dictionary.json');
const fast = (await readJson('tools/asr/benchmark_phase_f2_5.json')).benchmarks.find(x => x.model === 'base.en' && x.device === 'cuda' && x.compute_type === 'float16').results.find(x => x.fixture === 'fast');
const currentPlayable = new Set(['hello', 'good', 'morning']);
const officialDirectory = {
  i: { term: 'I, Me', url: 'https://divyangjan.depwd.gov.in/islrtc/listpage.php?type=I', status: 'DIRECTORY_LISTED_POSE_NOT_INSPECTED' },
  you: { term: 'You', url: 'https://divyangjan.depwd.gov.in/islrtc/search.php?search=You', status: 'PROJECT_CATALOG_SOURCE_ONLY' },
  water: { term: 'Water', url: 'https://divyangjan.depwd.gov.in/islrtc/listpage.php?type=W', status: 'DIRECTORY_LISTED_POSE_NOT_INSPECTED' },
  help: { term: 'Help', url: 'https://divyangjan.depwd.gov.in/islrtc/search.php?search=Help', status: 'PROJECT_CATALOG_SOURCE_ONLY' },
  me: { term: 'I, Me', url: 'https://divyangjan.depwd.gov.in/islrtc/listpage.php?type=I', status: 'DIRECTORY_LISTED_POSE_NOT_INSPECTED' },
  need: { term: 'Need', url: 'https://divyangjan.depwd.gov.in/islrtc/search.php?search=Need', status: 'NEEDS_REVIEW' },
  drink: { term: 'Drink', url: 'https://divyangjan.depwd.gov.in/islrtc/search.php?search=Drink', status: 'NEEDS_REVIEW' },
  tomorrow: { term: 'Tomorrow', url: 'https://divyangjan.depwd.gov.in/islrtc/search.php?search=Tomorrow', status: 'PROJECT_CATALOG_SOURCE_ONLY' },
  not: { term: 'Not', url: 'https://divyangjan.depwd.gov.in/islrtc/search.php?search=Not', status: 'NEEDS_REVIEW' },
  thank_you: { term: 'Thank you', url: 'https://divyangjan.depwd.gov.in/islrtc/search.php?search=Thank%20you', status: 'PROJECT_CATALOG_SOURCE_ONLY' },
};
const phraseBonus = { thank_you: 8 };
const termId = value => String(value).toLowerCase().replace(/\s+/g, '_');
const unavailable = g3.sign_coverage.missing_motion_frequency;
const allCandidateOccurrences = g3.sentences.flatMap(sentence => [
  ...sentence.sign_ids,
  ...sentence.unavailable_signs.map(x => x.sign_id),
]);
const concepts = (await Promise.all(Object.entries(unavailable).map(async ([id, frequency]) => {
  const dictionaryEntry = dictionary[id] || dictionary[id.replace(/_/g, ' ')];
  const motionPath = path.join(root, 'signs', `${id}.json`);
  let motion = null;
  try { motion = JSON.parse(await fs.readFile(motionPath, 'utf8')); } catch { /* absent is a state */ }
  const reference = officialDirectory[id] || { term: id, url: null, status: 'NEEDS_REVIEW' };
  const sentencesUnlocked = g3.sentences.filter(s => [...s.unavailable_signs.map(x => x.sign_id)].includes(id)).length;
  const isIncomplete = motion?.motion?.status === 'incomplete';
  const state = reference.status === 'DIRECTORY_LISTED_POSE_NOT_INSPECTED'
    ? 'B. MOTION_INCOMPLETE + reference available'
    : 'C. MOTION_INCOMPLETE + reference unavailable';
  // Transparent score: 10*frequency + 3*distinct affected sentences + 5*local
  // dictionary entry + 4*existing incomplete schema + 8*phrase value.  No inferred
  // “feasibility” or linguistic-quality points are awarded.
  const score_parts = { frequency: frequency * 10, sentence_unlock: sentencesUnlocked * 3, local_dictionary: dictionaryEntry ? 5 : 0, incomplete_motion_schema: isIncomplete ? 4 : 0, phrase_value: phraseBonus[id] || 0 };
  const priority_score = Object.values(score_parts).reduce((a, b) => a + b, 0);
  return { id, concept: id.toUpperCase(), frequency, sentencesUnlocked, state, priority_score, score_parts, dictionary_entry: Boolean(dictionaryEntry), dictionary_source: dictionaryEntry?.source || null, reference, motion_status: motion?.motion?.status || 'NO_MOTION_FILE', recommended_action: reference.status === 'DIRECTORY_LISTED_POSE_NOT_INSPECTED' ? 'Request/inspect the official entry before motion authoring.' : 'Locate and inspect an authoritative video reference before motion authoring.' };
}))).sort((a, b) => b.priority_score - a.priority_score || b.frequency - a.frequency || a.id.localeCompare(b.id));
const top5 = concepts.slice(0, 5), top10 = concepts.slice(0, 10);
const coverage = ids => {
  const available = new Set([...currentPlayable, ...ids]);
  const covered = allCandidateOccurrences.filter(id => available.has(id)).length;
  return { covered_concept_occurrences: covered, total_concept_occurrences: allCandidateOccurrences.length, technical_motion_coverage_percent: Number((covered / allCandidateOccurrences.length * 100).toFixed(2)) };
};
const tokenize = text => text.toLowerCase().match(/[a-z]+/g) || [];
const fastTokens = tokenize(fast.hypothesis);
const fastOverlap = concepts.map(c => ({ concept: c.id, occurrences: fastTokens.filter(t => t === c.id).length })).filter(x => x.occurrences);
const report = {
  phase: 'H1', generated_from: ['docs/g3_translation_evaluation_report.json', 'isl_accessibility/data/sign_dictionary.json', 'tools/asr/benchmark_phase_f2_5.json'],
  scoring_formula: '10*G3 corpus frequency + 3*distinct affected sentences + 5*local dictionary entry + 4*existing incomplete motion schema + 8*phrase value; no unmeasured feasibility score.',
  current_coverage: { total_linguistic_concepts: g3.sign_coverage.total_linguistic_concepts, playable: g3.sign_coverage.technically_playable, incomplete_or_not_authored: g3.sign_coverage.incomplete_or_not_authored, unavailable_occurrences: Object.values(unavailable).reduce((a, b) => a + b, 0) },
  ranked_candidates: concepts, coverage_simulation: { current: coverage([]), plus_top_5: coverage(top5.map(x => x.id)), plus_top_10: coverage(top10.map(x => x.id)) },
  realistic_speech: { fixture: 'fast.wav', model: 'base.en CUDA float16', recorded_hypothesis: fast.hypothesis, catalog_overlap: fastOverlap, note: 'This fixture is out of domain for the small G3 vocabulary. Only exact token overlap is reported; no speech frequency is inferred beyond the recorded hypothesis.' },
  first_authoring_batch: top5.filter(x => x.reference.status === 'DIRECTORY_LISTED_POSE_NOT_INSPECTED').slice(0, 5).map(x => x.id),
  limitation: 'Directory listing/catalog provenance is not a visual motion reference. No candidate may be animated until its official reference video is inspected and its intake record completed.'
};
await fs.writeFile(path.join(root, 'docs', 'h1_sign_coverage_priorities.json'), JSON.stringify(report, null, 2) + '\n');
const rows = concepts.map((x, index) => `| ${index + 1} | ${x.concept} | ${x.frequency} | ${x.priority_score} | ${x.state} | ${x.dictionary_entry ? 'yes' : 'no'} | ${x.reference.status} | ${x.motion_status} |`).join('\n');
const sim = report.coverage_simulation;
const md = `# H1 Sign Coverage Priorities\n\nThis is an evidence-based authoring roadmap, not a linguistic validation or motion specification.\n\n## Transparent scoring\n\n\`${report.scoring_formula}\`\n\nThe score intentionally awards no points for unmeasured authoring feasibility or uninspected gesture details.\n\n## Current coverage\n\n- Linguistic concepts: ${report.current_coverage.total_linguistic_concepts}\n- Playable: ${report.current_coverage.playable}\n- Incomplete/not authored: ${report.current_coverage.incomplete_or_not_authored}\n- G3 unavailable concept occurrences: ${report.current_coverage.unavailable_occurrences}\n\n## Top candidates\n\n| Rank | Concept | Frequency | Score | State | Local dictionary | Reference state | Motion state |\n| --- | --- | ---: | ---: | --- | --- | --- | --- |\n${rows}\n\n## Technical motion coverage simulation\n\nThis is concept-occurrence coverage in the G3 corpus, not linguistic accuracy.\n\n| Vocabulary | Covered / total occurrences | Coverage |\n| --- | --- | ---: |\n| Current | ${sim.current.covered_concept_occurrences}/${sim.current.total_concept_occurrences} | ${sim.current.technical_motion_coverage_percent}% |\n| Current + top 5 | ${sim.plus_top_5.covered_concept_occurrences}/${sim.plus_top_5.total_concept_occurrences} | ${sim.plus_top_5.technical_motion_coverage_percent}% |\n| Current + top 10 | ${sim.plus_top_10.covered_concept_occurrences}/${sim.plus_top_10.total_concept_occurrences} | ${sim.plus_top_10.technical_motion_coverage_percent}% |\n\n## Realistic speech fixture\n\nThe recorded base.en CUDA float16 fast-fixture hypothesis was: \`${fast.hypothesis}\`. Exact overlap with the current non-playable concept catalog: ${fastOverlap.map(x => `${x.concept.toUpperCase()} (${x.occurrences})`).join(', ') || 'none'}. This does not validate the G3 corpus as representative; it demonstrates a substantial out-of-domain vocabulary gap.\n\n## Recommended first authoring batch\n\n${report.first_authoring_batch.map(id => `- ${id.toUpperCase()}: high corpus frequency and an official directory entry has been located, but the pose is still uninspected.`).join('\n') || '- No candidate is cleared for authoring yet; inspect official video references first.'}\n\nDo not create motion files from this report. The next phase must first inspect the corresponding official ISLRTC video entries and complete technical reference intake.\n`;
await fs.writeFile(path.join(root, 'docs', 'h1_sign_coverage_priorities.md'), md);
console.log(JSON.stringify({ top10: concepts.slice(0, 10).map(x => [x.id, x.frequency, x.priority_score]), coverage: report.coverage_simulation, first_batch: report.first_authoring_batch }, null, 2));
console.log('PASS: H1 evidence-only prioritization report generated.');
