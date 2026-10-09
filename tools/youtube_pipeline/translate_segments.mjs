/**
 * translate_segments.mjs
 *
 * Bridges ASR transcript segments to the existing EnglishToISLTranslator.
 * Uses the exact, untouched G2/G3 translation engine and rules.
 *
 * Input:
 *   JSON file or stdin: [ { "start": 0.0, "end": 2.5, "text": "..." }, ... ]
 *
 * Output:
 *   JSON file or stdout: [
 *     {
 *       "start": 0.0,
 *       "end": 2.5,
 *       "source_text": "...",
 *       "gloss": ["..."],
 *       "translation_status": "SUPPORTED" | "HEURISTIC" | "UNCERTAIN",
 *       "transformation_trace": [...],
 *       "candidate_sign_ids": [...],
 *       "playable_signs": [...],
 *       "unavailable_concepts": [...],
 *       "unknown_terms": [...]
 *     }, ...
 *   ]
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { EnglishToISLTranslator } from '../avatar_viewer/EnglishToISLTranslator.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

export function processSegments(segments, translator = null) {
  const trans = translator || new EnglishToISLTranslator();
  return segments.map((seg) => {
    const rawText = String(seg.text || '').trim();
    if (!rawText) {
      return {
        start: Number(seg.start || 0),
        end: Number(seg.end || 0),
        source_text: '',
        gloss: [],
        translation_status: 'IDLE',
        transformation_trace: [],
        candidate_sign_ids: [],
        playable_signs: [],
        unavailable_concepts: [],
        unknown_terms: []
      };
    }

    const rep = trans.translate(rawText);
    return {
      start: Number(seg.start || 0),
      end: Number(seg.end || 0),
      source_text: rawText,
      gloss: rep.gloss_sequence || [],
      translation_status: rep.status || 'UNCERTAIN',
      transformation_trace: rep.transformation_trace || [],
      candidate_sign_ids: rep.motion_candidate_sign_ids || [],
      playable_signs: rep.sign_ids || [],
      unavailable_concepts: rep.unavailable_signs || [],
      unknown_terms: rep.unknown_terms || []
    };
  });
}

// CLI usage: node translate_segments.mjs [inputFile] [outputFile]
if (process.argv[1] && path.resolve(process.argv[1]) === path.resolve(__filename)) {
  const inputFile = process.argv[2];
  const outputFile = process.argv[3];

  let inputData = '';
  if (inputFile && fs.existsSync(inputFile)) {
    inputData = fs.readFileSync(inputFile, 'utf8');
  } else {
    // Read from stdin if no file passed
    inputData = fs.readFileSync(0, 'utf8');
  }

  const segments = JSON.parse(inputData || '[]');
  const results = processSegments(segments);

  const jsonOut = JSON.stringify(results, null, 2);
  if (outputFile) {
    fs.writeFileSync(outputFile, jsonOut, 'utf8');
  } else {
    process.stdout.write(jsonOut + '\n');
  }
}
