/**
 * H49 Phase 6: Independent File-Level Local vs. Remote (origin/main) Verification Script.
 * Compares all local files in D:\sign interpretor against git ls-tree -r origin/main
 * and git lfs ls-files, classifying every single local-only file with exact byte sizes.
 */

import fs from 'node:fs';
import path from 'node:path';
import { execSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '..');

function walk(dir, out = []) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (entry.name === '.git') continue;
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) walk(full, out);
    else if (entry.isFile()) {
      const rel = path.relative(ROOT, full).replace(/\\/g, '/');
      out.push({ rel, bytes: fs.statSync(full).size });
    }
  }
  return out;
}

const localFiles = walk(ROOT);
const remoteListRaw = execSync('git ls-tree -r --name-only origin/main', { cwd: ROOT, encoding: 'utf8', maxBuffer: 64 * 1024 * 1024 });
const remoteSet = new Set(remoteListRaw.split(/\r?\n/).filter(Boolean));

const lfsListRaw = execSync('git lfs ls-files -n', { cwd: ROOT, encoding: 'utf8', maxBuffer: 16 * 1024 * 1024 });
const lfsSet = new Set(lfsListRaw.split(/\r?\n/).filter(Boolean));

let matched = 0;
let matchedBytes = 0;
const excludedBuckets = {
  GITHUB_QUOTA_ARTIFACTS_RAW_MEDIA: { count: 0, bytes: 0 },
  GITHUB_LIMIT_AND_REPRODUCIBLE_VENV: { count: 0, bytes: 0 },
  GITHUB_LIMIT_AND_REPRODUCIBLE_RUNTIME_MEDIA_OR_BROWSERS: { count: 0, bytes: 0 },
  SECURITY_EXCLUDED_BROWSER_PROFILES: { count: 0, bytes: 0 },
  SECURITY_EXCLUDED_ENV: { count: 0, bytes: 0 },
  LICENSE_EXCLUDED_AVATAR_PROPRIETARY: { count: 0, bytes: 0 },
  PYTHON_BYTECODE_CACHE: { count: 0, bytes: 0 },
  OTHER_LOCAL_ONLY: { count: 0, bytes: 0 }
};

for (const f of localFiles) {
  if (remoteSet.has(f.rel)) {
    matched++;
    matchedBytes += f.bytes;
    continue;
  }
  let bucket = 'OTHER_LOCAL_ONLY';
  if (f.rel === '.env') bucket = 'SECURITY_EXCLUDED_ENV';
  else if (f.rel.startsWith('Avatar_Boy_Gun_AetherShadow/')) bucket = 'LICENSE_EXCLUDED_AVATAR_PROPRIETARY';
  else if (f.rel.startsWith('.venv/')) bucket = 'GITHUB_LIMIT_AND_REPRODUCIBLE_VENV';
  else if (f.rel.startsWith('artifacts/')) bucket = 'GITHUB_QUOTA_ARTIFACTS_RAW_MEDIA';
  else if (/^runtime\/(chrome_|edge_|test_ext_).*profile\//.test(f.rel)) bucket = 'SECURITY_EXCLUDED_BROWSER_PROFILES';
  else if (f.rel.startsWith('runtime/')) bucket = 'GITHUB_LIMIT_AND_REPRODUCIBLE_RUNTIME_MEDIA_OR_BROWSERS';
  else if (f.rel.includes('__pycache__/')) bucket = 'PYTHON_BYTECODE_CACHE';

  excludedBuckets[bucket].count++;
  excludedBuckets[bucket].bytes += f.bytes;
}

const summary = {
  local_root: ROOT,
  remote_branch: 'origin/main',
  local_files_total: localFiles.length,
  remote_files_total: remoteSet.size,
  matched_files: matched,
  matched_mb: Number((matchedBytes / 1048576).toFixed(2)),
  lfs_tracked_files: lfsSet.size,
  local_only_files: localFiles.length - matched,
  excluded_breakdown: Object.fromEntries(
    Object.entries(excludedBuckets).map(([k, v]) => [k, { count: v.count, mb: Number((v.bytes / 1048576).toFixed(2)) }])
  )
};

fs.mkdirSync(path.join(ROOT, 'artifacts/h49'), { recursive: true });
fs.writeFileSync(path.join(ROOT, 'artifacts/h49/h49_local_vs_remote_audit.json'), JSON.stringify(summary, null, 2) + '\n', 'utf8');
console.log(JSON.stringify(summary, null, 2));
