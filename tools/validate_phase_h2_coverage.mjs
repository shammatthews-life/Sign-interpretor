/** H2 evidence-only coverage evaluator. It derives coverage from the current
 * translator catalog and asserts that no visually unverified candidate became playable. */
import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { RuleBasedISLTranslator } from './avatar_viewer/EnglishToISLTranslator.js';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const corpus = JSON.parse(await fs.readFile(path.join(root, 'tools/fixtures/g3_translation_corpus.json'), 'utf8'));
const translator = new RuleBasedISLTranslator();
const requiredIncomplete = ['water', 'i', 'me'];
const playable = Object.entries(translator.motionCatalog).filter(([, value]) => value.playable).map(([id]) => id).sort();
const candidateIds = corpus.flatMap(({ text }) => translator.translate(text).motion_candidate_sign_ids);
const covered = candidateIds.filter(id => translator.motionCatalog[id]?.playable).length;
const missing = candidateIds.filter(id => !translator.motionCatalog[id]?.playable);
const frequency = Object.fromEntries([...new Set(missing)].sort().map(id => [id, missing.filter(value => value === id).length]));

for (const id of requiredIncomplete) {
  if (translator.motionCatalog[id]?.playable) throw new Error(`${id} is marked playable without a completed H2 visual reference intake.`);
}
if (candidateIds.length !== 110 || covered !== 10 || missing.length !== 100) {
  throw new Error(`Unexpected H2 coverage: ${covered}/${candidateIds.length}, missing ${missing.length}.`);
}
console.log(JSON.stringify({ phase: 'H2', playable, covered_concept_occurrences: covered, total_concept_occurrences: candidateIds.length, technical_motion_coverage_percent: Number((covered / candidateIds.length * 100).toFixed(2)), remaining_missing_frequency: frequency }, null, 2));
console.log('PASS: H2 preserved the evidence gate; no unverified sign was made playable.');
