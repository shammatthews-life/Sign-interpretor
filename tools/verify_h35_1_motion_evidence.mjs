import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const framesDir = path.join(root, 'artifacts', 'h35_1', 'frames');

const segments = fs.readdirSync(framesDir).filter(d => d.startsWith('segment_')).sort();
console.log(`Auditing motion dynamics across ${segments.length} segment directories...`);

const motionLedger = [];

for (const seg of segments) {
  const segPath = path.join(framesDir, seg);
  const startFile = path.join(segPath, 'frame_start.png');
  const midFile = path.join(segPath, 'frame_mid.png');
  const endFile = path.join(segPath, 'frame_end.png');

  if (!fs.existsSync(startFile) || !fs.existsSync(midFile) || !fs.existsSync(endFile)) {
    motionLedger.push({ seg, status: 'MISSING_FRAMES' });
    continue;
  }

  const startStat = fs.statSync(startFile);
  const midStat = fs.statSync(midFile);
  const endStat = fs.statSync(endFile);

  // Compare file size variance as a first indicator
  const startBuf = fs.readFileSync(startFile);
  const midBuf = fs.readFileSync(midFile);
  
  // Quick byte difference check
  let diffBytes = 0;
  const minLen = Math.min(startBuf.length, midBuf.length);
  for (let i = 0; i < minLen; i += 64) {
    if (startBuf[i] !== midBuf[i]) diffBytes++;
  }
  const variancePct = ((diffBytes / (minLen / 64)) * 100).toFixed(1);

  motionLedger.push({
    segment: seg,
    startBytes: startStat.size,
    midBytes: midStat.size,
    endBytes: endStat.size,
    sampleVariancePct: `${variancePct}%`,
    motionObserved: diffBytes > 100
  });
}

const movingCount = motionLedger.filter(m => m.motionObserved).length;
console.log(`Verified motion in ${movingCount} / ${segments.length} segments.`);
console.log('Sample Segments:');
console.log(motionLedger.slice(0, 5));
console.log(motionLedger.slice(20, 25));
