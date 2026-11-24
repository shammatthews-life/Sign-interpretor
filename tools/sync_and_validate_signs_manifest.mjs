import fs from 'fs';
import path from 'path';

const signsDir = 'signs';
const manifestPath = path.join(signsDir, 'manifest.json');

const files = fs.readdirSync(signsDir).filter(f => f.endsWith('.json') && f !== 'manifest.json');
console.log(`Discovered ${files.length} sign JSON files in ${signsDir}/`);

const manifestSigns = [];
let validCount = 0;
const errors = [];

for (const file of files) {
  const filePath = path.join(signsDir, file);
  try {
    const data = JSON.parse(fs.readFileSync(filePath, 'utf8'));
    
    // Schema 2.0.0 validation checks
    if (!data.schema_version || data.schema_version !== '2.0.0') {
      errors.push(`${file}: invalid schema_version (${data.schema_version})`);
      continue;
    }
    if (!data.sign_id) {
      errors.push(`${file}: missing sign_id`);
      continue;
    }
    if (!data.motion || !data.motion.keyframes || !Array.isArray(data.motion.keyframes) || data.motion.keyframes.length === 0) {
      errors.push(`${file}: missing or empty motion.keyframes`);
      continue;
    }
    if (!data.motion.involved_bones || !Array.isArray(data.motion.involved_bones) || data.motion.involved_bones.length === 0) {
      errors.push(`${file}: missing or empty motion.involved_bones`);
      continue;
    }

    manifestSigns.push({
      sign_id: data.sign_id,
      display_name: data.metadata?.display_name || data.sign_id,
      gloss: data.metadata?.gloss || data.sign_id.toUpperCase(),
      lexical_type: data.metadata?.lexical_type || 'ISL Lexical Sign',
      duration_ms: data.motion?.duration_ms || 1200,
      dominant_hand: data.motion?.dominant_hand || 'right',
      validation_status: data.metadata?.validation_status || 'IMPLEMENTATION_PENDING_LINGUISTIC_REVIEW',
      source: data.metadata?.source || {
        organization: 'ISLRTC',
        portal: 'Indian Sign Language Research and Training Centre',
        url: 'https://divyangjan.depwd.gov.in/islrtc/'
      },
      file_name: file,
      involved_bones_count: data.motion.involved_bones.length,
      keyframe_count: data.motion.keyframes.length
    });

    validCount++;
  } catch (err) {
    errors.push(`${file}: JSON parse error (${err.message})`);
  }
}

if (errors.length > 0) {
  console.error(`Validation found ${errors.length} errors:`);
  errors.forEach(e => console.error(`  - ${e}`));
  process.exit(1);
}

// Sort manifest signs alphabetically by sign_id
manifestSigns.sort((a, b) => a.sign_id.localeCompare(b.sign_id));

const newManifest = {
  manifest_version: '2.5.0',
  schema_version: '2.0.0',
  generated_at: new Date().toISOString(),
  phase: 'H38',
  total_signs: manifestSigns.length,
  total_playable_signs: manifestSigns.length,
  signs: manifestSigns
};

fs.writeFileSync(manifestPath, JSON.stringify(newManifest, null, 2), 'utf8');
console.log(`Successfully verified and updated ${manifestPath}:`);
console.log(`  Total Valid Signs: ${validCount}`);
console.log(`  Manifest Version:  2.5.0 (Phase H38)`);
