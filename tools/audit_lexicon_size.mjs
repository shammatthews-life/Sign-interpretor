import { EnglishToISLTranslator } from './avatar_viewer/EnglishToISLTranslator.js';
const t = new EnglishToISLTranslator();
for (const word of ['gossip', 'honesty', 'integrity', 'warmup']) {
  console.log(`In this.lexicon: ${word} -> ${t.lexicon.has(word)}`);
  console.log(`In this.motionCatalog: ${word} -> ${Boolean(t.motionCatalog[word])}`);
}
