import fs from 'fs';
import { EnglishToISLTranslator } from './EnglishToISLTranslator.js';

const b = JSON.parse(fs.readFileSync('artifacts/h42/benchmark/h42_video_b_locked_benchmark.json', 'utf8'));
const translator = new EnglishToISLTranslator();

b.segments.forEach((s, idx) => {
  const t = s.source_text.toLowerCase();
  const res = translator.translate(s.source_text);
  const hits = [];
  if (t.includes('summer')) hits.push('summer');
  if (t.includes('vlog')) hits.push('vlog');
  if (t.includes('story')) hits.push('story');
  if (t.includes('king')) hits.push('king');
  if (t.includes('trial')) hits.push('trial');
  if (t.includes('dollar')) hits.push('dollar');
  if (t.includes('food')) hits.push('food');
  if (t.includes('coffee')) hits.push('coffee');
  if (t.includes('tired')) hits.push('tired');
  if (t.includes('advice')) hits.push('advice');
  if (t.includes('stitch')) hits.push('stitch');
  if (t.includes('future') || t.includes('together')) hits.push('future/together');
  if (hits.length) {
    console.log(`Segment ${idx}: [${hits.join(', ')}]`);
    console.log(`  Source: ${s.source_text}`);
    console.log(`  Gloss:  ${res.gloss_sequence.join(' ')}\n`);
  }
});
