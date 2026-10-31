import fs from 'fs';

const content = fs.readFileSync('tools/avatar_viewer/EnglishToISLTranslator.js', 'utf8');
const idx = content.indexOf("['seeing', 'SEE']");
console.log('Index of seeing, SEE:', idx);
if (idx !== -1) {
  console.log('Context:', JSON.stringify(content.substring(idx, idx + 100)));
}
