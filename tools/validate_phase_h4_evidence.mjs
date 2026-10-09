import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const report = JSON.parse(await fs.readFile(path.join(root, 'docs/h4_signlearn_evidence_report.json'), 'utf8'));
const allowed = new Set(['OBSERVED', 'UNCLEAR', 'NOT_APPLICABLE', 'NOT_INSPECTED']);
const visualKeys = ['start_pose', 'handshape', 'palm_orientation', 'wrist_orientation', 'arm_position', 'movement_direction', 'movement_path', 'contact_point', 'repetition', 'end_pose', 'non_manual_features'];
const expected = ['YOU', 'WATER', 'I', 'ME', 'HELP', 'NEED', 'DRINK'];
if (report.phase !== 'H4' || report.motion_authoring !== 'NONE') throw new Error('H4 must be evidence-only.');
for (const concept of expected) {
  const item = report.candidate_intake_schema.records.find(value => value.concept === concept);
  if (!item) throw new Error(`Missing H4 intake: ${concept}`);
  if (item.authoring_eligible || item.video_actually_inspected) throw new Error(`${concept} must remain gated until footage is inspected.`);
  for (const key of visualKeys) if (!allowed.has(item[key])) throw new Error(`${concept}.${key} is not an allowed evidence value.`);
}
if (report.coverage.after !== '10/110 = 9.09%') throw new Error('H4 must not claim a coverage increase without authored motion.');
console.log('PASS: H4 Sign Learn intake uses the evidence gate; no uninspected candidate is authoring-eligible.');
