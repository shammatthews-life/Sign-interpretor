/**
 * Builds the H46 60-segment independent sentence audit ledger across Videos A & B,
 * capturing glosses, playable signs, NMMs, spatial_plan (loci, directional verbs, role shifts),
 * and translation status.
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { EnglishToISLTranslator } from './avatar_viewer/EnglishToISLTranslator.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '..');

const refs = JSON.parse(
  fs.readFileSync(path.join(ROOT, 'artifacts/h44/h44_verified_references_ab.json'), 'utf8')
);
const translator = new EnglishToISLTranslator();
const outDir = path.join(ROOT, 'artifacts/h46');
fs.mkdirSync(outDir, { recursive: true });

const ledger = {
  milestone: 'H46',
  generated_at: new Date().toISOString(),
  total_segments: 0,
  nmm_segments: 0,
  spatial_plan_segments: 0,
  videos: {}
};

for (const [videoId, vData] of Object.entries(refs.videos)) {
  const entries = [];
  for (const seg of vData.segments) {
    const rep = translator.translate(seg.text);
    const hasNmm = (rep.non_manual_markers || []).length > 0;
    const sp = rep.spatial_plan || { locus_assignments: [], directional_inflections: [], role_shifts: [] };
    const hasSpatial = sp.locus_assignments.length > 0 || sp.directional_inflections.length > 0 || sp.role_shifts.length > 0;
    if (hasNmm) ledger.nmm_segments++;
    if (hasSpatial) ledger.spatial_plan_segments++;
    ledger.total_segments++;

    entries.push({
      id: seg.id,
      start: seg.start,
      end: seg.end,
      english: seg.text,
      isl_gloss: (rep.gloss_sequence || []).join(' '),
      playable_signs: rep.sign_ids || [],
      unknown_terms: rep.unknown_terms || [],
      non_manual_markers: rep.non_manual_markers || [],
      spatial_plan: sp,
      status: rep.status
    });
  }
  ledger.videos[videoId] = {
    title: vData.title,
    segment_count: entries.length,
    segments: entries
  };
}

const outPath = path.join(outDir, 'h46_sentence_audit_ledger.json');
fs.writeFileSync(outPath, JSON.stringify(ledger, null, 2) + '\n', 'utf8');
console.log(`Saved H46 60-segment audit ledger (${ledger.total_segments} segments, ${ledger.nmm_segments} with NMMs, ${ledger.spatial_plan_segments} with spatial plans) to ${outPath}`);
