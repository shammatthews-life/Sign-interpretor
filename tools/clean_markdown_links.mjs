import fs from 'node:fs';
import path from 'node:path';

const root = path.resolve('.');

function findMarkdownFiles(dir) {
  let results = [];
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  for (const entry of entries) {
    if (entry.name === '.git' || entry.name === '.venv' || entry.name === 'node_modules') continue;
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      results = results.concat(findMarkdownFiles(full));
    } else if (entry.isFile() && entry.name.endsWith('.md')) {
      results.push(full);
    }
  }
  return results;
}

const mdFiles = findMarkdownFiles(root);
let totalReplacements = 0;
let filesModified = 0;

for (const file of mdFiles) {
  let content = fs.readFileSync(file, 'utf8');
  const fileDir = path.dirname(file);
  let modified = false;

  // Pattern matches: file:///d:/sign%20interpretor/PATH or file:///D:/sign%20interpretor/PATH
  const regex = /file:\/\/\/[dD]:\/sign(?:%20|\s)interpretor\/([^)"'\s#]+)(#[^)"'\s]*)?/g;

  const newContent = content.replace(regex, (match, targetPath, hash) => {
    // Decode URI component (e.g. %20 -> space)
    const decodedTargetPath = decodeURIComponent(targetPath);
    const absTarget = path.resolve(root, decodedTargetPath);
    let relTarget = path.relative(fileDir, absTarget).replace(/\\/g, '/');
    if (!relTarget.startsWith('.')) {
      relTarget = './' + relTarget;
    }
    const finalLink = relTarget + (hash || '');
    totalReplacements++;
    modified = true;
    return finalLink;
  });

  if (modified) {
    fs.writeFileSync(file, newContent, 'utf8');
    filesModified++;
    console.log(`Cleaned: ${path.relative(root, file)}`);
  }
}

console.log(`\nReplaced ${totalReplacements} machine-specific file:/// links across ${filesModified} markdown files.`);
