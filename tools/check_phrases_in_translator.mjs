import fs from 'fs';
import { EnglishToISLTranslator } from './avatar_viewer/EnglishToISLTranslator.js';

const t = new EnglishToISLTranslator();
const phrasesData = JSON.parse(fs.readFileSync('data/h27_phrase_inventory.json', 'utf8'));
const phrases = phrasesData.phrases || [];

console.log(`Total phrases in data/h27_phrase_inventory.json: ${phrases.length}`);
console.log(`Total phrases in this.phrases: ${t.phrases.size}`);

let missingInTranslator = 0;
const missingList = [];
for (const p of phrases) {
  const expr = p.expression.toLowerCase();
  if (!t.phrases.has(expr)) {
    missingInTranslator++;
    missingList.push(expr);
  }
}

console.log(`Phrases missing in this.phrases: ${missingInTranslator}`);
if (missingList.length > 0) {
  console.log('First 20 missing:', missingList.slice(0, 20));
}
