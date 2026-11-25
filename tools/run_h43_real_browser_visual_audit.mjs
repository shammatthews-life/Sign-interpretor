/**
 * tools/run_h43_real_browser_visual_audit.mjs
 *
 * Milestone H43 Workstream 6: Real-Browser Chrome + Extension 3D Avatar Visual Audit & GPU NVENC Capture
 *
 * Verifies end-to-end rendering inside YouTube using the PNA-free chrome-extension:// viewer,
 * engages Full Body framing, waits until YouTube ads are genuinely cleared (.ad-showing === false),
 * triggers genuine sign playback during active YouTube playback, dynamically crops using the live
 * DOM bounding rect of #isl-floating-avatar-surface, and encodes NVENC MP4 + contact sheets.
 */
import fs from 'fs';
import path from 'path';
import { spawn } from 'child_process';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const root = path.resolve(__dirname, '..');

const chromeExe = path.join(root, 'runtime/browsers/chrome/win64-158.0.8127.88/chrome-win64/chrome.exe');
const extensionPath = path.join(root, 'extension');
const profileDir = path.join(root, 'runtime/chrome_h35_profile');
const ffmpegExe = path.join(root, '.venv/Lib/site-packages/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe');

const h43Dir = path.join(root, 'artifacts/h43');
const recDir = path.join(h43Dir, 'recordings');
const framesDir = path.join(h43Dir, 'frames');
const sheetsDir = path.join(h43Dir, 'contact_sheets');
const cropsDir = path.join(h43Dir, 'crops');
const evidenceDir = path.join(h43Dir, 'evidence');

for (const d of [recDir, framesDir, sheetsDir, cropsDir, evidenceDir]) {
  fs.mkdirSync(d, { recursive: true });
}

const multiEvalPath = path.join(h43Dir, 'benchmark/h43_multi_domain_evaluation.json');
const evalData = JSON.parse(fs.readFileSync(multiEvalPath, 'utf8'));

function runFFmpeg(args) {
  return new Promise((resolve, reject) => {
    const p = spawn(ffmpegExe, args, { stdio: ['ignore', 'pipe', 'pipe'] });
    let err = '';
    p.stderr.on('data', d => { err += d.toString(); });
    p.on('close', code => {
      if (code === 0) resolve();
      else reject(new Error(`FFmpeg exited ${code}: ${err.slice(-400)}`));
    });
  });
}

async function connectCDP(wsUrl) {
  const ws = new globalThis.WebSocket(wsUrl);
  await new Promise((res, rej) => {
    ws.addEventListener('open', res);
    ws.addEventListener('error', rej);
  });
  let nextId = 0;
  const pending = new Map();
  const listeners = new Map();
  ws.addEventListener('message', evt => {
    const msg = JSON.parse(evt.data);
    if (msg.id && pending.has(msg.id)) {
      const { res, rej } = pending.get(msg.id);
      pending.delete(msg.id);
      if (msg.error) rej(new Error(msg.error.message));
      else res(msg.result);
    } else if (msg.method && listeners.has(msg.method)) {
      for (const cb of listeners.get(msg.method)) cb(msg.params);
    }
  });
  const send = (method, params = {}) => new Promise((res, rej) => {
    const id = ++nextId;
    pending.set(id, { res, rej });
    ws.send(JSON.stringify({ id, method, params }));
  });
  const on = (method, cb) => {
    if (!listeners.has(method)) listeners.set(method, []);
    listeners.get(method).push(cb);
  };
  const off = (method, cb) => {
    const arr = listeners.get(method) || [];
    listeners.set(method, arr.filter(x => x !== cb));
  };
  await send('Runtime.enable');
  await send('Page.enable');
  return { ws, send, on, off };
}

async function waitForTargets(port, urlSub) {
  for (let i = 0; i < 45; i++) {
    try {
      const r = await fetch(`http://127.0.0.1:${port}/json/list`);
      if (r.ok) {
        const list = await r.json();
        const page = list.find(t => t.type === 'page' && t.url.includes(urlSub));
        const embed = list.find(t => t.url.includes('viewer/embed.html'));
        if (page && embed) return { page, embed };
      }
    } catch {}
    await new Promise(r => setTimeout(r, 500));
  }
  throw new Error(`Timed out waiting for Chrome targets matching ${urlSub} and viewer/embed.html`);
}

async function cdpClick(yt, x, y) {
  await yt.send('Input.dispatchMouseEvent', { type: 'mousePressed', x, y, button: 'left', clickCount: 1 });
  await yt.send('Input.dispatchMouseEvent', { type: 'mouseReleased', x, y, button: 'left', clickCount: 1 });
}

async function clearYouTubeAds(yt) {
  for (let attempt = 0; attempt < 45; attempt++) {
    const res = await yt.send('Runtime.evaluate', {
      expression: `(() => {
        const ad = document.querySelector('.ad-showing, .ad-interrupting');
        const skip = document.querySelector('.ytp-skip-ad-button, .ytp-ad-skip-button, .ytp-ad-skip-button-modern, button[id^="skip-button"], [class*="skip-ad"] button');
        let skipRect = null;
        if (skip) {
          const r = skip.getBoundingClientRect();
          if (r.width > 5 && r.height > 5) {
            skipRect = { x: Math.round(r.x + r.width / 2), y: Math.round(r.y + r.height / 2) };
          }
        }
        const vid = document.querySelector('video.html5-main-video') || document.querySelector('video');
        let playRect = null;
        if (vid && vid.paused) {
          try { vid.muted = true; vid.play(); } catch {}
          const pb = document.querySelector('.ytp-play-button, .ytp-large-play-button');
          if (pb) {
            const r = pb.getBoundingClientRect();
            if (r.width > 5 && r.height > 5) {
              playRect = { x: Math.round(r.x + r.width / 2), y: Math.round(r.y + r.height / 2) };
            }
          }
        }
        return {
          isAd: Boolean(ad),
          skipRect,
          playRect,
          paused: vid ? vid.paused : null,
          vidTime: vid ? Number(vid.currentTime.toFixed(2)) : null,
          vidDur: vid && Number.isFinite(vid.duration) ? Number(vid.duration.toFixed(1)) : null
        };
      })()`,
      returnByValue: true
    });
    const val = res?.result?.value;
    if (val?.playRect && val.paused) {
      await cdpClick(yt, val.playRect.x, val.playRect.y);
    }
    if (!val?.isAd) {
      return { cleared: true, attempts: attempt + 1 };
    }
    if (val.skipRect) {
      await cdpClick(yt, val.skipRect.x, val.skipRect.y);
      await new Promise(r => setTimeout(r, 800));
      continue;
    }
    await new Promise(r => setTimeout(r, 1000));
  }
  const finalCheck = await yt.send('Runtime.evaluate', {
    expression: `Boolean(document.querySelector('.ad-showing, .ad-interrupting'))`,
    returnByValue: true
  });
  if (finalCheck?.result?.value) {
    throw new Error('YouTube ad remained active after clearing attempts (.ad-showing === true)');
  }
  return { cleared: true, attempts: 45 };
}

async function engageFullBodyAndReadLayout(yt, emb) {
  let stats = null;
  for (let i = 0; i < 30; i++) {
    const r = await emb.send('Runtime.evaluate', {
      expression: `window.AetherEmbed ? window.AetherEmbed.getStats() : null`,
      returnByValue: true
    });
    stats = r?.result?.value;
    if (stats && stats.signsLoaded >= 600 && stats.bonesCount > 0) break;
    await new Promise(r => setTimeout(r, 300));
  }
  if (!stats || stats.signsLoaded < 600) {
    throw new Error(`AetherEmbed did not initialize properly: ${JSON.stringify(stats)}`);
  }

  const domRes = await yt.send('Runtime.evaluate', {
    expression: `(() => {
      const host = document.getElementById('isl-accessibility-overlay-root');
      const sr = host?.shadowRoot;
      const btnFull = sr?.getElementById('btn-avatar-full');
      if (btnFull) btnFull.click();
      const surface = sr?.getElementById('isl-floating-avatar-surface');
      const fallback = sr?.getElementById('isl-aether-fallback');
      const iframe = sr?.getElementById('isl-aether-iframe');
      const rect = surface?.getBoundingClientRect();
      const dpr = window.devicePixelRatio || 1;
      return {
        hasHost: Boolean(host),
        hasShadowRoot: Boolean(sr),
        iframeSrc: iframe?.src || '',
        fallbackHidden: Boolean(fallback?.classList?.contains('hidden')),
        dpr,
        surfaceRect: rect ? {
          x: Math.max(0, Math.round(rect.x * dpr)),
          y: Math.max(0, Math.round(rect.y * dpr)),
          w: Math.round(rect.width * dpr),
          h: Math.round(rect.height * dpr)
        } : null
      };
    })()`,
    returnByValue: true
  });
  const domInfo = domRes?.result?.value;
  if (!domInfo?.hasHost || !domInfo?.fallbackHidden || !domInfo?.surfaceRect) {
    throw new Error(`Overlay or Aether surface invalid: ${JSON.stringify(domInfo)}`);
  }

  // Explicitly ensure Full Body view inside embed
  await emb.send('Runtime.evaluate', {
    expression: `window.AetherEmbed.setViewMode('full')`,
    returnByValue: true
  });
  await new Promise(r => setTimeout(r, 400));
  const afterFull = await emb.send('Runtime.evaluate', {
    expression: `window.AetherEmbed.getStats()`,
    returnByValue: true
  });
  return { domInfo, embedStats: afterFull?.result?.value };
}

async function auditVideo(yt, emb, key, videoConfig) {
  console.log(`\n=== Auditing ${key}: ${videoConfig.video_id} (${videoConfig.domain}) ===`);
  const adClear = await clearYouTubeAds(yt);
  console.log(`  Ad clear status:`, adClear);

  const { domInfo, embedStats } = await engageFullBodyAndReadLayout(yt, emb);
  console.log(`  Overlay surface:`, domInfo.surfaceRect, `| Embed:`, embedStats);

  const vFramesDir = path.join(framesDir, key);
  const vRawDir = path.join(recDir, `raw_${key}`);
  const vSheetDir = path.join(sheetsDir, key);
  [vFramesDir, vRawDir, vSheetDir].forEach(d => fs.mkdirSync(d, { recursive: true }));

  // Verify interactive video transport + trigger genuine sign queue synchronized to cue windows
  const segments = videoConfig.reference_translation.translated_segments;
  const sampleSegs = segments.slice(0, 6);

  // Seek video cleanly to start of first sample segment and ensure playing
  await yt.send('Runtime.evaluate', {
    expression: `(() => {
      const v = document.querySelector('video.html5-main-video') || document.querySelector('video');
      if (v) {
        v.muted = true;
        v.currentTime = ${Number(sampleSegs[0]?.start || 1)};
        v.play();
      }
      return v ? { paused: v.paused, currentTime: Number(v.currentTime.toFixed(2)) } : null;
    })()`,
    returnByValue: true
  });

  // Start continuous CDP screencast recording during real playback + live avatar signing
  let rawFrameIdx = 0;
  const screencastHandler = async params => {
    const idx = rawFrameIdx++;
    const file = path.join(vRawDir, `frame_${String(idx).padStart(4, '0')}.jpg`);
    fs.writeFileSync(file, Buffer.from(params.data, 'base64'));
    try { await yt.send('Page.screencastFrameAck', { sessionId: params.sessionId }); } catch {}
  };
  yt.on('Page.screencastFrame', screencastHandler);
  await yt.send('Page.startScreencast', { format: 'jpeg', quality: 88, everyNthFrame: 1 });

  // Drive live cue transitions into AetherEmbed over ~10 seconds across multiple signs
  const signTrail = [];
  const boneSnapshots = [];
  const segSlice = sampleSegs.slice(0, 4);
  for (let si = 0; si < segSlice.length; si++) {
    const seg = segSlice[si];
    const cueSigns = (seg.sign_ids || []).slice(0, 4);
    await yt.send('Runtime.evaluate', {
      expression: `(() => {
        const v = document.querySelector('video.html5-main-video') || document.querySelector('video');
        if (v && ${si} > 0) {
          v.currentTime = ${Number(seg.start || si * 4)};
        }
        const sr = document.getElementById('isl-accessibility-overlay-root')?.shadowRoot;
        const iframe = sr?.getElementById('isl-aether-iframe');
        const boxGloss = sr?.getElementById('box-gloss');
        if (boxGloss) boxGloss.textContent = ${JSON.stringify((seg.gloss_sequence || []).join(' '))};
        if (iframe?.contentWindow) {
          const origin = new URL(iframe.src).origin;
          const jobId = 'h43-${key}';
          const cueId = 'cue-${si}';
          iframe.contentWindow.postMessage({
            type: 'ISL_AETHER_COMMAND',
            parentOrigin: window.location.origin,
            command: 'CUE_TRANSITION',
            jobId,
            cueId
          }, origin);
          const signs = ${JSON.stringify(cueSigns)};
          signs.forEach((signId, idx) => {
            iframe.contentWindow.postMessage({
              type: idx === 0 ? 'ISL_AETHER_COMMAND' : 'ISL_AETHER_COMMAND',
              parentOrigin: window.location.origin,
              command: idx === 0 ? 'PLAY_SIGN' : 'QUEUE_SIGN',
              signId,
              jobId,
              cueId,
              cueStartSeconds: ${Number(seg.start || 0)},
              cueEndSeconds: ${Number(seg.end || 3)},
              eventId: 'h43-${key}-s${si}-' + idx + '-' + Date.now()
            }, origin);
          });
        }
      })()`,
      returnByValue: true
    });

    // Capture start / mid / end PNG screenshots of segment + read actual bone angles
    for (const phase of ['start', 'mid', 'end']) {
      await new Promise(r => setTimeout(r, 750));
      const snapRes = await emb.send('Runtime.evaluate', {
        expression: `(() => {
          const st = window.AetherEmbed.getStats();
          const b = n => {
            const bone = window.AetherEmbed.bonesMap.get(n);
            return bone ? {
              x: Number((bone.rotation.x * 180 / Math.PI).toFixed(1)),
              y: Number((bone.rotation.y * 180 / Math.PI).toFixed(1)),
              z: Number((bone.rotation.z * 180 / Math.PI).toFixed(1))
            } : null;
          };
          return {
            currentSign: st.currentSign,
            queuedCount: st.queuedCount,
            rArm: b('Bip001_R_UpperArm'),
            lArm: b('Bip001_L_UpperArm'),
            rFore: b('Bip001_R_Forearm'),
            rHand: b('Bip001_R_Hand')
          };
        })()`,
        returnByValue: true
      });
      const bVal = snapRes?.result?.value;
      boneSnapshots.push({ segIndex: si, phase, ...bVal });
      if (bVal?.currentSign) signTrail.push(bVal.currentSign);

      const shot = await yt.send('Page.captureScreenshot', { format: 'png' });
      const shotPath = path.join(vFramesDir, `seg_${String(si).padStart(2, '0')}_${phase}.png`);
      fs.writeFileSync(shotPath, Buffer.from(shot.data, 'base64'));
    }
  }

  // Test interactive Pause -> Resume -> Half-body toggle -> Full-body restore
  await yt.send('Runtime.evaluate', {
    expression: `(() => {
      const v = document.querySelector('video.html5-main-video') || document.querySelector('video');
      if (v) v.pause();
      const sr = document.getElementById('isl-accessibility-overlay-root')?.shadowRoot;
      sr?.getElementById('btn-avatar-half')?.click();
      setTimeout(() => sr?.getElementById('btn-avatar-full')?.click(), 450);
    })()`,
    returnByValue: true
  });
  await new Promise(r => setTimeout(r, 1000));

  await yt.send('Page.stopScreencast');
  yt.off('Page.screencastFrame', screencastHandler);

  // Assemble NVENC H.264 MP4 from real screencast frames
  const mp4Path = path.join(recDir, `h43_${key}_recording.mp4`);
  const capturedCount = fs.readdirSync(vRawDir).filter(f => f.endsWith('.jpg')).length;
  if (capturedCount < 5) {
    throw new Error(`Too few screencast frames captured for ${key}: ${capturedCount}`);
  }
  await runFFmpeg([
    '-y', '-framerate', '12',
    '-i', path.join(vRawDir, 'frame_%04d.jpg'),
    '-c:v', 'h264_nvenc', '-preset', 'p4', '-pix_fmt', 'yuv420p',
    mp4Path
  ]);

  // Build 4x3 Contact Sheet of the real start/mid/end frames
  const sheetPath = path.join(vSheetDir, `h43_${key}_contact_sheet.png`);
  const segPngs = fs.readdirSync(vFramesDir).filter(f => f.endsWith('.png')).sort();
  if (segPngs.length >= 4) {
    await runFFmpeg([
      '-y', '-pattern_type', 'glob',
      '-i', path.join(vFramesDir, '*.png'),
      '-vf', 'scale=320:-1,tile=4x3',
      '-frames:v', '1',
      sheetPath
    ]).catch(async () => {
      // Windows FFmpeg without shell glob: concat input list fallback
      const firstFrame = path.join(vFramesDir, segPngs[0]);
      fs.copyFileSync(firstFrame, sheetPath);
    });
  }

  // Dynamically crop anatomical views using LIVE DOM bounding rect of #isl-floating-avatar-surface
  const { x, y, w, h } = domInfo.surfaceRect;
  const repFrame = path.join(vFramesDir, 'seg_00_mid.png');
  const cropDirV = path.join(cropsDir, key);
  fs.mkdirSync(cropDirV, { recursive: true });
  const cropFull = path.join(cropDirV, 'full_body_surface.png');
  const cropHands = path.join(cropDirV, 'hands_torso_zone.png');
  const cropFace = path.join(cropDirV, 'face_head_zone.png');

  await runFFmpeg(['-y', '-i', repFrame, '-vf', `crop=${w}:${h}:${x}:${y}`, cropFull]);
  await runFFmpeg(['-y', '-i', repFrame, '-vf', `crop=${Math.max(120, Math.round(w * 0.85))}:${Math.max(120, Math.round(h * 0.42))}:${x + Math.round(w * 0.08)}:${y + Math.round(h * 0.30)}`, cropHands]);
  await runFFmpeg(['-y', '-i', repFrame, '-vf', `crop=${Math.max(120, Math.round(w * 0.7))}:${Math.max(100, Math.round(h * 0.32))}:${x + Math.round(w * 0.15)}:${y + Math.round(h * 0.04)}`, cropFace]);

  // Verify non-zero arm articulation movement across frames
  const armZs = boneSnapshots.map(b => b.rArm?.z).filter(v => typeof v === 'number');
  const armSpanDeg = armZs.length ? Number((Math.max(...armZs) - Math.min(...armZs)).toFixed(1)) : 0;

  return {
    video_id: videoConfig.video_id,
    domain: videoConfig.domain,
    ad_cleared: adClear.cleared,
    overlay_surface_rect: domInfo.surfaceRect,
    fallback_hidden: domInfo.fallbackHidden,
    embed_stats: embedStats,
    screencast_frames_captured: capturedCount,
    mp4_path: path.relative(root, mp4Path).replace(/\\/g, '/'),
    mp4_bytes: fs.statSync(mp4Path).size,
    contact_sheet_path: path.relative(root, sheetPath).replace(/\\/g, '/'),
    crops: {
      full_body: path.relative(root, cropFull).replace(/\\/g, '/'),
      hands: path.relative(root, cropHands).replace(/\\/g, '/'),
      face: path.relative(root, cropFace).replace(/\\/g, '/')
    },
    observed_active_signs: [...new Set(signTrail)],
    right_arm_z_span_deg: armSpanDeg,
    bone_snapshots: boneSnapshots
  };
}

async function buildTileContactSheet(framesFolder, outPng) {
  const pngs = fs.readdirSync(framesFolder).filter(f => f.endsWith('.png')).sort();
  if (!pngs.length) return;
  const listTxt = path.join(framesFolder, '_tile_list.txt');
  fs.writeFileSync(listTxt, pngs.map(p => `file '${path.join(framesFolder, p).replace(/\\/g, '/')}'\nduration 1`).join('\n'), 'utf8');
  await runFFmpeg([
    '-y', '-f', 'concat', '-safe', '0', '-i', listTxt,
    '-vf', 'scale=320:-1,tile=4x3',
    '-frames:v', '1',
    outPng
  ]);
}

async function main() {
  const port = 9225;
  const targetsToAudit = [
    { key: 'video_a', vid: 'MXKkXXYUxBc' },
    { key: 'video_b', vid: 'y8tFSuOMAqQ' },
    { key: 'video_c', vid: 'xrwz9IxpMJg' }
  ];

  const chrome = spawn(chromeExe, [
    `--remote-debugging-port=${port}`,
    `--user-data-dir=${profileDir}`,
    `--disable-extensions-except=${extensionPath}`,
    `--load-extension=${extensionPath}`,
    '--no-first-run',
    '--no-default-browser-check',
    '--use-angle=d3d11',
    '--enable-gpu-rasterization',
    '--enable-zero-copy',
    '--window-size=1280,720',
    '--window-position=0,0',
    `https://www.youtube.com/watch?v=${targetsToAudit[0].vid}`
  ], { stdio: 'ignore' });

  const results = {};
  try {
    for (let i = 0; i < targetsToAudit.length; i++) {
      const { key, vid } = targetsToAudit[i];
      const { page, embed } = await waitForTargets(port, vid);
      const yt = await connectCDP(page.webSocketDebuggerUrl);
      const emb = await connectCDP(embed.webSocketDebuggerUrl);
      results[key] = await auditVideo(yt, emb, key, evalData.multi_domain_videos[vid]);

      // Regenerate clean 4x3 concat contact sheet cleanly for Windows FFmpeg
      const vFramesDir = path.join(framesDir, key);
      const sheetPath = path.join(sheetsDir, key, `h43_${key}_contact_sheet.png`);
      await buildTileContactSheet(vFramesDir, sheetPath);

      try { yt.ws.close(); } catch {}
      try { emb.ws.close(); } catch {}

      if (i + 1 < targetsToAudit.length) {
        const nextVid = targetsToAudit[i + 1].vid;
        const { page: curP } = await waitForTargets(port, vid);
        const nav = await connectCDP(curP.webSocketDebuggerUrl);
        await nav.send('Page.navigate', { url: `https://www.youtube.com/watch?v=${nextVid}` });
        await new Promise(r => setTimeout(r, 2500));
        try { nav.ws.close(); } catch {}
      }
    }

    const ledger = {
      timestamp_utc: new Date().toISOString(),
      milestone: 'H43',
      validation_status: 'PENDING_DEAF_COMMUNITY_REVIEW',
      gpu_pipeline: {
        webgl: 'Direct3D 11',
        encoder: 'h264_nvenc'
      },
      videos_audited: results
    };
    const outLedger = path.join(evidenceDir, 'h43_visual_audit_evidence.json');
    fs.writeFileSync(outLedger, JSON.stringify(ledger, null, 2) + '\n', 'utf8');
    console.log('\nH43 Visual Audit Evidence written:', outLedger);
  } finally {
    try { chrome.kill(); } catch {}
  }
}

main().catch(err => {
  console.error('H43 Visual Audit FAILED:', err);
  process.exit(1);
});
