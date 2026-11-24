import { EnglishToISLTranslator } from './avatar_viewer/EnglishToISLTranslator.js';

const translator = new EnglishToISLTranslator();

const testSentences = [
  { id: 'Seg 00', text: "This is public speaking for beginners, and the goal of this video is simple." },
  { id: 'Seg 01', text: "It's to help you overcome being uncertain, anxious, afraid," },
  { id: 'Seg 04', text: "What you're about to watch is a special compilation of a three-day public speaking challenge" },
  { id: 'Seg 09', text: "from the 110-step chart of excellence communication." },
  { id: 'Seg 10', text: "Hey, if we haven't met before, my name is David JP Phillips," },
  { id: 'Seg 14', text: "You see, I've studied over 5,000 speakers to pinpoint exactly what makes someone a great speaker." },
  { id: 'Seg 16', text: "Oh, and they have been put to practice. I've coached global giants like Oracle, Google," },
  { id: 'Seg 18', text: "attention. Now over the next two hours and 30 minutes, you'll discover the essential tools I've" },
  { id: 'Seg 19', text: "I've gathered during my 25 year career as a public speaker" }
];

testSentences.forEach(s => {
  const res = translator.translate(s.text);
  console.log(`\n=== ${s.id} ===`);
  console.log(`Input: "${s.text}"`);
  console.log(`Gloss: ${res.gloss_sequence.join(' ')}`);
  console.log(`Signs: [${res.sign_ids.join(', ')}]`);
  console.log(`Names: [${res.fingerspelled_terms.join(', ')}]`);
  console.log(`Rules: ${res.transformation_trace.filter(t => t.stage === 'restructure').map(t => t.rule_id || t.detail).join('; ')}`);
});
