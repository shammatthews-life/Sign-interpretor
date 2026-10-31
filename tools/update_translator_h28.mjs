import fs from 'fs';

let content = fs.readFileSync('tools/avatar_viewer/EnglishToISLTranslator.js', 'utf8');

// 1. Replace unmapped glosses in multiwordPhrases
content = content.replace("['going to', ['GOING_TO']]", "['going to', ['WILL']]");
content = content.replace("['as well as', ['AND', 'ALSO']]", "['as well as', ['MORE']]");
content = content.replace("[\"i'm going to show\", ['I', 'GOING_TO', 'SHOW']]", "[\"i'm going to show\", ['I', 'WILL', 'SHOW']]");
content = content.replace("['going to show you', ['GOING_TO', 'SHOW', 'YOU']]", "['going to show you', ['WILL', 'SHOW', 'YOU']]");
content = content.replace("[\"i'm going to give\", ['I', 'GOING_TO', 'GIVE']]", "[\"i'm going to give\", ['I', 'WILL', 'GIVE']]");
content = content.replace("['going to give you', ['GOING_TO', 'GIVE', 'YOU']]", "['going to give you', ['WILL', 'GIVE', 'YOU']]");
content = content.replace("['in order to', ['FOR']]", "['in order to', ['REASON']]");
content = content.replace("['have to', ['MUST']]", "['have to', ['NEED']]");
content = content.replace('["i\'m going to", ["I", "GOING_TO"]]', '["i\'m going to", ["I", "WILL"]]');
content = content.replace('["every single", ["ALL", "ONE"]]', '["every single", ["ONE"]]');
content = content.replace('["going to show", ["GOING_TO", "SHOW"]]', '["going to show", ["WILL", "SHOW"]]');
content = content.replace('["we\'re going to", ["WE", "GOING_TO"]]', '["we\'re going to", ["WE", "WILL"]]');
content = content.replace('["going to give", ["GOING_TO", "GIVE"]]', '["going to give", ["WILL", "GIVE"]]');
content = content.replace('["over and over", ["AGAIN", "MORE"]]', '["over and over", ["MORE"]]');
content = content.replace('["over and over again", ["AGAIN", "MORE"]]', '["over and over again", ["MORE"]]');

// 2. Add 13 missing signs to this.lexicon
const missingEntries = `\r\n      // Phase H28 Production Sign Integration (13 Manifest Signs & Inflections)\r\n` +
`      ['complain', 'COMPLAIN'], ['complains', 'COMPLAIN'], ['complained', 'COMPLAIN'], ['complaining', 'COMPLAIN'],\r\n` +
`      ['control', 'CONTROL'], ['controls', 'CONTROL'], ['controlled', 'CONTROL'], ['controlling', 'CONTROL'],\r\n` +
`      ['excuse', 'EXCUSE'], ['excuses', 'EXCUSE'], ['excused', 'EXCUSE'], ['excusing', 'EXCUSE'],\r\n` +
`      ['gossip', 'GOSSIP'], ['gossips', 'GOSSIP'], ['gossiped', 'GOSSIP'], ['gossiping', 'GOSSIP'],\r\n` +
`      ['honesty', 'HONESTY'], ['honest', 'HONESTY'], ['honestly', 'HONESTY'],\r\n` +
`      ['integrity', 'INTEGRITY'],\r\n` +
`      ['judge', 'JUDGE'], ['judges', 'JUDGE'], ['judged', 'JUDGE'], ['judging', 'JUDGE'], ['judgment', 'JUDGE'],\r\n` +
`      ['negative', 'NEGATIVE'], ['negatively', 'NEGATIVE'], ['negativity', 'NEGATIVE'],\r\n` +
`      ['pitch', 'PITCH'], ['pitches', 'PITCH'], ['pitched', 'PITCH'], ['pitching', 'PITCH'],\r\n` +
`      ['protect', 'PROTECT'], ['protects', 'PROTECT'], ['protected', 'PROTECT'], ['protecting', 'PROTECT'], ['protection', 'PROTECT'],\r\n` +
`      ['tomorrow', 'TOMORROW'],\r\n` +
`      ['tone', 'TONE'], ['tones', 'TONE'],\r\n` +
`      ['warmup', 'WARMUP'], ['warmups', 'WARMUP'], ['warm-up', 'WARMUP'], ['warming up', 'WARMUP'],`;

const anchor = "['seeing', 'SEE'],";
const targetIdx = content.indexOf(anchor);
if (targetIdx === -1) {
  console.error("Anchor not found!");
} else {
  const insertPos = targetIdx + anchor.length;
  content = content.slice(0, insertPos) + missingEntries + content.slice(insertPos);
  fs.writeFileSync('tools/avatar_viewer/EnglishToISLTranslator.js', content, 'utf8');
  console.log("Updated EnglishToISLTranslator.js successfully!");
}
