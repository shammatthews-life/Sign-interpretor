import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const schema = JSON.parse(await fs.readFile(path.join(root, 'docs/h5_evidence_intake_schema.json'), 'utf8'));
const metadataDir = path.join(root, schema.capture_metadata_directory);
const allowed = new Set(schema.allowed_visual_values);
const statuses = new Set(schema.evidence_status_values);
const expectedConcepts = new Set(['YOU', 'WATER', 'I', 'ME', 'HELP', 'NEED', 'DRINK']);
const files = (await fs.readdir(metadataDir)).filter(file => file.endsWith('.json'));

const fail = message => { throw new Error(message); };
for (const file of files) {
  const record = JSON.parse(await fs.readFile(path.join(metadataDir, file), 'utf8'));
  for (const field of schema.required_fields) if (!(field in record)) fail(`${file}: missing required field '${field}'.`);
  if (!expectedConcepts.has(record.concept)) fail(`${file}: unsupported concept '${record.concept}'.`);
  if (!/^\d{4}-\d{2}-\d{2}$/.test(record.capture_date)) fail(`${file}: capture_date must be YYYY-MM-DD.`);
  if (!record.capture_filename || !record.platform || !record.app_name || !record.dictionary_result_label || !record.variant_label) fail(`${file}: capture identity fields must be non-empty.`);
  if (!record.source_provenance || typeof record.source_provenance !== 'object') fail(`${file}: source_provenance must be an object.`);
  for (const field of schema.source_provenance_required_fields) if (!record.source_provenance[field]) fail(`${file}: missing provenance '${field}'.`);
  if (!statuses.has(record.evidence_status)) fail(`${file}: invalid evidence_status.`);
  if (!Array.isArray(record.uncertainties)) fail(`${file}: uncertainties must be an array.`);
  for (const field of schema.motion_parameter_required_fields) if (!allowed.has(record.motion_parameters?.[field])) fail(`${file}: invalid motion parameter '${field}'.`);
  for (const field of ['video_complete', 'signer_visible', 'start_pose_visible', 'movement_visible', 'end_pose_visible', 'hands_visible', 'face_visible', 'motion_parameters_observable', 'human_review_required', 'authoring_eligible']) {
    if (typeof record[field] !== 'boolean') fail(`${file}: '${field}' must be boolean.`);
  }
  if (record.authoring_eligible) {
    for (const field of schema.authoring_gate.required_for_true) if (!record[field]) fail(`${file}: authoring_eligible requires ${field}: true.`);
    if (record.evidence_status !== schema.authoring_gate.required_evidence_status) fail(`${file}: authoring_eligible requires VERIFIED_VISUAL_REFERENCE.`);
  }
}
console.log(`PASS: H5 intake schema is valid; ${files.length} captured-evidence metadata record(s) checked. No linguistic correctness was inferred.`);
