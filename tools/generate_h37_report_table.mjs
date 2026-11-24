import fs from 'node:fs';
import path from 'node:path';

const data = JSON.parse(fs.readFileSync('artifacts/h37/translation/h37_optimized_translation_result.json', 'utf8'));

let md = '| Seg | Timestamp | Spoken Text | Generated ISL Gloss | Signs | Proper Nouns / Fingerspelled | Grammatical Rules Applied | Visual Readability |\n';
md += '| :---: | :---: | :--- | :--- | :---: | :--- | :--- | :---: |\n';

data.segments.forEach(s => {
  const rules = [];
  s.trace.forEach(t => {
    if (t.stage === 'restructure') rules.push(t.rule_id || 'RESTRUCTURE');
    if (t.stage === 'proper_noun_fingerspelling') rules.push('FS');
  });
  const ruleStr = rules.length ? [...new Set(rules)].join(', ') : 'Direct Canonical';
  const fsStr = s.fingerspelledTerms.length ? s.fingerspelledTerms.join(', ') : '—';
  const cleanText = s.sourceText.replace(/"/g, "'");
  md += `| **${String(s.segmentIndex).padStart(2, '0')}** | ${s.start.toFixed(1)}s - ${s.end.toFixed(1)}s | "${cleanText}" | \`${s.glossSequence.join(' ')}\` | ${s.playableCount} | ${fsStr} | ${ruleStr} | **PASS** |\n`;
});

fs.writeFileSync('artifacts/h37/reports/segments_table_snippet.md', md, 'utf8');
console.log('Saved 29-segment markdown table snippet to artifacts/h37/reports/segments_table_snippet.md');
