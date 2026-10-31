import fs from 'fs';
import path from 'path';
import { EnglishToISLTranslator } from './avatar_viewer/EnglishToISLTranslator.js';

const manifest = JSON.parse(fs.readFileSync('signs/manifest.json', 'utf8'));
const t = new EnglishToISLTranslator();

const missingInLexicon = [];
for (const sign of manifest.signs) {
  const id = sign.sign_id.toLowerCase();
  if (!t.lexicon.has(id)) {
    missingInLexicon.push(id);
  }
}

console.log(`Total signs in manifest: ${manifest.signs.length}`);
console.log(`Signs in manifest but missing in this.lexicon: ${missingInLexicon.length}`);
console.log('List of missing signs:', missingInLexicon);
