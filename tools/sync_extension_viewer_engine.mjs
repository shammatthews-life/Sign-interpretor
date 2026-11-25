import fs from 'fs';
import path from 'path';

const SRC_DIR = 'tools/avatar_viewer';
const DST_DIR = 'extension/viewer/engine';
const FILES = [
  'SignAnimationPlayer.js',
  'SignLibrary.js',
  'SignScheduler.js',
  'AvatarCameraView.mjs',
  'NonFiniteHelperBoneCorrection.mjs',
  'PendingAetherQueue.js',
  'ISLFingerspelling.js'
];

fs.mkdirSync(DST_DIR, { recursive: true });
for (const file of FILES) {
  let content = fs.readFileSync(path.join(SRC_DIR, file), 'utf8');
  if (file === 'SignAnimationPlayer.js') {
    content = content.replace(
      "import * as THREE from 'three';",
      "import * as THREE from '../../vendor/three/three.module.min.js';"
    );
  }
  fs.writeFileSync(path.join(DST_DIR, file), content, 'utf8');
}
console.log(`Synced ${FILES.length} viewer engine modules to ${DST_DIR}/`);
