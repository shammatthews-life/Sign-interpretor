import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { EnglishToISLTranslator } from './avatar_viewer/EnglishToISLTranslator.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT = path.resolve(__dirname, '..');

function main() {
  const refs = JSON.parse(fs.readFileSync(path.join(ROOT, 'artifacts/h44/h44_verified_references_ab.json'), 'utf8'));
  const manifest = JSON.parse(fs.readFileSync(path.join(ROOT, 'signs/manifest.json'), 'utf8'));
  const signIdsOnDisk = new Set(manifest.signs.map(s => s.sign_id));
  const tr = new EnglishToISLTranslator();

  const tokenFreq = new Map();
  const bigramFreq = new Map();
  const trigramFreq = new Map();
  const nonExactMappings = new Map();
  const minedSuspicious = [];

  for (const vid of ['MXKkXXYUxBc', 'y8tFSuOMAqQ']) {
    for (const seg of refs.videos[vid].segments) {
      const norm = tr.normalize(seg.text);
      const toks = norm.split(' ').filter(Boolean);
      const out = tr.translate(seg.text);

      toks.forEach((t, i) => {
        tokenFreq.set(t, (tokenFreq.get(t) || 0) + 1);
        if (i + 1 < toks.length) {
          const bg = `${t} ${toks[i + 1]}`;
          bigramFreq.set(bg, (bigramFreq.get(bg) || 0) + 1);
        }
        if (i + 2 < toks.length) {
          const tg = `${t} ${toks[i + 1]} ${toks[i + 2]}`;
          trigramFreq.set(tg, (trigramFreq.get(tg) || 0) + 1);
        }
        const g = tr.lexicon.get(t);
        if (g && g !== t.toUpperCase()) {
          if (!nonExactMappings.has(t)) {
            nonExactMappings.set(t, { mapped_gloss: g, disk_sign_exists_for_source: signIdsOnDisk.has(t), contexts: [] });
          }
          const rec = nonExactMappings.get(t);
          if (rec.contexts.length < 4) rec.contexts.push(`${seg.id}: ${seg.text}`);
        }
      });

      // Automated heuristic error miners targeting structural/semantic flaws in passing sentences
      const gs = out.gloss_sequence;
      const flags = [];
      if (/\b(do|does)\s+(know|need|want|think|believe|feel)\b/i.test(seg.text) && gs.includes('DO')) {
        flags.push('SPURIOUS_EMPHATIC_DO_VERB');
      }
      if (/\byou\s+do\s+too\b/i.test(seg.text) && gs.includes('DO')) {
        flags.push('ELLIPTICAL_PRO_VERB_DO_UNRESOLVED');
      }
      if (/\binstead of\b/i.test(seg.text) && !gs.includes('NOT')) {
        flags.push('CONTRASTIVE_INSTEAD_OF_MISSING_NEGATION');
      }
      if ((seg.text.match(/\b(isn't|aren't|don't|doesn't|didn't|won't|can't|not|never)\b/gi) || []).length >= 2
        && gs.filter(x => x === 'NOT').length < 2) {
        flags.push('MULTI_CLAUSE_NEGATION_COLLAPSED');
      }
      if (/\bdon't know (how|what|why|where)\b/i.test(seg.text)) {
        const kIdx = gs.indexOf('KNOW');
        const whIdx = gs.findIndex(x => ['HOW', 'WHAT', 'WHY', 'WHERE'].includes(x));
        const nIdx = gs.indexOf('NOT');
        if (kIdx !== -1 && whIdx > kIdx && nIdx > whIdx) {
          flags.push('MATRIX_NEGATION_BLEED_PAST_EMBEDDED_CLAUSE');
        }
      }
      if (/\b(gotten|get)\s+(a lot\s+)?(easier|better|harder|worse|bigger)\b/i.test(seg.text) && (gs.includes('GET') || !gs.includes('MORE'))) {
        flags.push('INCHOATIVE_COMPARATIVE_MISSED');
      }
      if (/\bgoing on\b/i.test(seg.text) && gs.includes('GO')) {
        flags.push('IDIOM_GOING_ON_LITERAL_GO');
      }
      if (/\b(talks|view|delivered|things|something|probably|still|always|again|some|everybody)\b/i.test(seg.text)) {
        flags.push('HIGH_RISK_POLYSEMY_OR_COMPRESSION');
      }

      if (flags.length > 0) {
        minedSuspicious.push({
          segment_id: seg.id,
          flags,
          english: seg.text,
          current_gloss: gs.join(' ')
        });
      }
    }
  }

  const outReport = {
    milestone: 'H45',
    generated_at: new Date().toISOString(),
    unique_normalized_tokens_ab: tokenFreq.size,
    non_exact_lexicon_mappings_count: nonExactMappings.size,
    flagged_segments_count: minedSuspicious.length,
    flagged_segments: minedSuspicious,
    non_exact_mappings: Object.fromEntries([...nonExactMappings.entries()].sort((a, b) => a[0].localeCompare(b[0]))),
    top_bigrams: [...bigramFreq.entries()].sort((a, b) => b[1] - a[1]).slice(0, 40),
    top_trigrams: [...trigramFreq.entries()].sort((a, b) => b[1] - a[1]).slice(0, 30)
  };

  fs.mkdirSync(path.join(ROOT, 'artifacts/h45'), { recursive: true });
  fs.writeFileSync(path.join(ROOT, 'artifacts/h45/h45_error_mining_report.json'), `${JSON.stringify(outReport, null, 2)}\n`, 'utf8');
  console.log(`H45 Error Miner complete: ${tokenFreq.size} unique tokens, ${nonExactMappings.size} non-exact mappings, ${minedSuspicious.length}/60 segments flagged for semantic refinement.`);
  for (const m of minedSuspicious) {
    console.log(`  [${m.segment_id}] ${m.flags.join(', ')} -> "${m.current_gloss}"`);
  }
}

main();
