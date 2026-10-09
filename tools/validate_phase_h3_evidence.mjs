import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const reportPath = path.join(root, 'docs', 'h3_official_visual_reference_recovery_report.json');
const report = JSON.parse(await fs.readFile(reportPath, 'utf8'));
const required = ['YOU', 'WATER', 'I', 'ME'];
if (report.phase !== 'H3') throw new Error('H3 report phase is missing.');
for (const concept of required) {
  const candidate = report.candidates.find(value => value.concept === concept);
  if (!candidate) throw new Error(`Missing H3 candidate: ${concept}`);
  if (candidate.eligible_for_h4_authoring) throw new Error(`${concept} cannot be H4-eligible without an inspected official visual reference.`);
  if (candidate.actual_video_inspected) throw new Error(`${concept} must not claim video inspection in this evidence-recovery result.`);
}
for (const scenario of Object.values(report.coverage_simulation)) {
  if (scenario.covered_concept_occurrences !== 10 || scenario.total_concept_occurrences !== 110 || scenario.technical_motion_coverage_percent !== 9.09) {
    throw new Error('H3 coverage must remain the evidence-gated 10/110 (9.09%).');
  }
}
console.log('PASS: H3 candidate evidence states, H4 gate, and 10/110 coverage simulation are consistent.');
