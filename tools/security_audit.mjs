import fs from 'node:fs';
import path from 'node:path';
import { execSync } from 'node:child_process';

const root = path.resolve('.');

const files = execSync('git status --porcelain', { cwd: root, encoding: 'utf8' })
  .split(/\r?\n/)
  .map(l => l.slice(3).trim())
  .filter(Boolean);

const patterns = [
  { name: 'API Key', regex: /api[_-]?key\s*[:=]\s*["'][a-zA-Z0-9_\-]{16,}["']/i },
  { name: 'Generic Secret', regex: /secret\s*[:=]\s*["'][a-zA-Z0-9_\-]{16,}["']/i },
  { name: 'Bearer Token', regex: /bearer\s+[a-zA-Z0-9_\-\.]{20,}/i },
  { name: 'GitHub Token', regex: /ghp_[a-zA-Z0-9]{36}/ },
  { name: 'AWS Access Key', regex: /AKIA[0-9A-Z]{16}/ },
  { name: 'Hardcoded Password', regex: /password\s*[:=]\s*["'][^\s"']{6,}["']/i }
];

let issues = 0;
for (const rel of files) {
  const full = path.join(root, rel);
  if (!fs.existsSync(full)) continue;
  if (!fs.statSync(full).isFile()) continue;

  const ext = path.extname(rel).toLowerCase();
  if (['.js', '.mjs', '.py', '.json', '.html', '.css', '.md', '.ps1'].includes(ext)) {
    const content = fs.readFileSync(full, 'utf8');
    for (const p of patterns) {
      if (p.regex.test(content)) {
        console.warn(`[ALERT] Potential secret in ${rel}: Matched ${p.name}`);
        issues++;
      }
    }
  }
}

if (issues === 0) {
  console.log('[PASS] Security Audit Clean: Zero credentials, tokens, or private secrets found!');
} else {
  console.warn(`[WARN] Found ${issues} potential items to review.`);
}
