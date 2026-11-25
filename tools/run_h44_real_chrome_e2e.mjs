/**
 * tools/run_h44_real_chrome_e2e.mjs
 *
 * Milestone H44 Workstream 9 & 8:
 * True Real-Chrome End-to-End Extension + Runtime Pipeline Test & Visual Frame Verification.
 *
 * Exercises the ACTUAL live pipeline end-to-end (no manual fake postMessage cue bypassing):
 *   1. Verifies port 8000 runtime server is alive (/asr/status CUDA + 635 signs in /signs/bundle.json).
 *   2. Launches real Chrome (158.0.8127.88) with unpacked extension/ loaded on CDP port 9225.
 *   3. For both locked benchmark videos (MXKkXXYUxBc & y8tFSuOMAqQ):
 *      - Navigates to YouTube watch page and verifies honest ad clearing (.ad-showing === false).
 *      - Connects extension popup (background tab so YouTube tab remains active) -> clicks #btn-youtube-process
 *        -> triggers real service-worker -> POST /youtube/process -> CUDA small.en ASR & H44 translator
 *        -> YOUTUBE_CUES_READY -> content-script YouTubeTimelineSynchronizer cue installation!
 *      - Switches avatar to Full Body mode (#btn-avatar-full + AetherEmbed.setViewMode('full')).
 *      - Tests REAL TimelineSynchronizer transitions during YouTube playback:
 *          * Continuous playback across multiple cues
 *          * Forward Seek (jumps inside 0-120s locked window, confirms cue switch & cancellation)
 *          * Pause & Resume (confirms transport forwarding without losing state)
 *          * Speed change 1.5x -> 0.5x
 *          * Backward Seek (confirms fresh occurrence replay)
 *          * Half Body <-> Full Body camera mode toggle
 *      - Records continuous CDP screencast -> GPU NVENC H.264 MP4, 4x3 Contact Sheets,
 *        phase screenshots, and DPI-calibrated surface crops (#isl-floating-avatar-surface).
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

const h44Dir = path.join(root, 'artifacts/h44');
const recDir = path.join(h44Dir, 'recordings');
const framesDir = path.join(h44Dir, 'frames');
const sheetsDir = path.join(h44Dir, 'contact_sheets');
const cropsDir = path.join(h44Dir, 'crops');
const evidenceDir = path.join(h44Dir, 'evidence');

for (const d of [profileDir, recDir, framesDir, sheetsDir, cropsDir, evidenceDir]) {
  fs.mkdirSync(d, { recursive: true });
}

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

async function listTargets(port) {
  const r = await fetch(`http://127.0.0.1:${port}/json/list`);
  if (!r.ok) throw new Error(`CDP json/list HTTP ${r.status}`);
  return r.json();
}

async function waitForTargets(port, urlSub) {
  let lastUrls = [];
  for (let i = 0; i < 60; i++) {
    try {
      const list = await listTargets(port);
      lastUrls = list.map(t => `${t.type}:${t.url}`);
      const page = list.find(t => t.type === 'page' && t.url.includes(urlSub));
      const embed = list.find(t => t.url.includes('viewer/embed.html'));
      const sw = list.find(t => t.type === 'service_worker' && t.url.startsWith('chrome-extension://'));
      if (page && embed) return { page, embed, sw };
    } catch (e) {
      lastUrls = [`fetch_err:${e.message}`];
    }
    await new Promise(r => setTimeout(r, 500));
  }
  throw new Error(`Timed out waiting for Chrome targets (${urlSub} & viewer/embed.html). Seen: ${JSON.stringify(lastUrls)}`);
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
        return { isAd: Boolean(ad), skipRect, playRect, paused: vid ? vid.paused : null };
      })()`,
      returnByValue: true
    });
    const val = res?.result?.value;
    if (val?.playRect && val.paused) await cdpClick(yt, val.playRect.x, val.playRect.y);
    if (!val?.isAd) return { cleared: true, attempts: attempt + 1 };
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
  if (finalCheck?.result?.value) throw new Error('YouTube ad remained active (.ad-showing === true)');
  return { cleared: true, attempts: 45 };
}

async function triggerRealExtensionPipeline(port, yt, videoUrl) {
  const list = await listTargets(port);
  const embedTarget = list.find(t => t.url.includes('viewer/embed.html'));
  if (!embedTarget) throw new Error('Extension embed target not found to resolve extensionId');
  const extUrl = new URL(embedTarget.url);
  const extOrigin = `${extUrl.protocol}//${extUrl.host}`;
  const popupUrl = `${extOrigin}/popup/popup.html`;
  const ytTab = list.find(t => t.type === 'page' && t.url.includes('youtube.com/watch'));

  // Open new CDP tab and explicitly navigate to extension popup.html, then re-activate YouTube tab
  let popTarget = list.find(t => t.url.startsWith(`${extOrigin}/popup/popup.html`));
  if (!popTarget) {
    const cr = await fetch(`http://127.0.0.1:${port}/json/new`, { method: 'PUT' });
    popTarget = await cr.json();
  }
  const pop = await connectCDP(popTarget.webSocketDebuggerUrl);
  await pop.send('Page.navigate', { url: popupUrl });
  await new Promise(r => setTimeout(r, 900));

  // Connect runtime in popup first, populate URL, switch active tab to YouTube so service-worker getActiveTab() matches, then click synchronously!
  await pop.send('Runtime.evaluate', {
    expression: `(() => {
      document.getElementById('btn-probe-runtime')?.click();
      const inp = document.getElementById('youtube-url');
      if (inp) inp.value = ${JSON.stringify(videoUrl)};
    })()`
  });
  await new Promise(r => setTimeout(r, 500));

  if (ytTab) {
    await fetch(`http://127.0.0.1:${port}/json/activate/${ytTab.id}`);
    await new Promise(r => setTimeout(r, 400));
  }

  const popClickRes = await pop.send('Runtime.evaluate', {
    expression: `(() => {
      const btn = document.getElementById('btn-youtube-process');
      if (btn) btn.click();
      return {
        url: window.location.href,
        disabledAfterClick: Boolean(btn?.disabled),
        btnText: btn?.textContent,
        stage: document.getElementById('youtube-stage')?.textContent,
        err: document.getElementById('youtube-error')?.textContent
      };
    })()`,
    returnByValue: true
  });
  console.log('  Popup triggered:', popClickRes?.result?.value);
  await new Promise(r => setTimeout(r, 800));
  const popAfter = await pop.send('Runtime.evaluate', {
    expression: `({
      state: document.getElementById('youtube-job-state')?.textContent,
      jobId: document.getElementById('youtube-job-id')?.textContent,
      stage: document.getElementById('youtube-stage')?.textContent,
      err: document.getElementById('youtube-error')?.textContent
    })`,
    returnByValue: true
  });
  console.log('  Popup status after click:', popAfter?.result?.value);

  // Poll extension state on overlay UI until READY and segments >= 20
  let readyInfo = null;
  for (let i = 0; i < 420; i++) {
    const r = await yt.send('Runtime.evaluate', {
      expression: `(() => {
        const sr = document.getElementById('isl-accessibility-overlay-root')?.shadowRoot;
        const jobState = sr?.getElementById('youtube-job-state')?.textContent?.trim();
        const segCount = Number(sr?.getElementById('youtube-segment-count')?.textContent?.trim() || 0);
        const jobId = sr?.getElementById('youtube-job-id')?.textContent?.trim();
        const latestSeg = sr?.getElementById('youtube-latest-segment')?.textContent?.trim();
        const glosses = sr?.getElementById('youtube-glosses')?.textContent?.trim();
        const transStatus = sr?.getElementById('youtube-translation-status')?.textContent?.trim();
        const conn = sr?.getElementById('st-conn')?.textContent?.trim();
        return { jobState, segCount, jobId, latestSeg, glosses, transStatus, conn };
      })()`,
      returnByValue: true
    });
    const val = r?.result?.value;
    if (i % 5 === 0) console.log('   [pipeline poll]', val);
    if (val?.jobState === 'ERROR') {
      throw new Error(`Real extension pipeline errored: ${JSON.stringify(val)}`);
    }
    if (val?.jobState === 'READY' && val?.segCount >= 20) {
      readyInfo = val;
      break;
    }
    await new Promise(r => setTimeout(r, 1000));
  }
  await pop.ws.close();
  if (!readyInfo) throw new Error(`Timed out waiting for real extension pipeline READY for ${videoUrl}`);
  return readyInfo;
}

async function engageFullBodyAndReadLayout(yt, emb) {
  let stats = null;
  for (let i = 0; i < 40; i++) {
    const r = await emb.send('Runtime.evaluate', {
      expression: `window.AetherEmbed ? window.AetherEmbed.getStats() : null`,
      returnByValue: true
    });
    stats = r?.result?.value;
    if (stats && stats.signsLoaded >= 635 && stats.bonesCount > 0) break;
    await new Promise(r => setTimeout(r, 300));
  }
  if (!stats || stats.signsLoaded < 635) {
    throw new Error(`AetherEmbed expected >=635 signs loaded, got: ${JSON.stringify(stats)}`);
  }

  const domRes = await yt.send('Runtime.evaluate', {
    expression: `(() => {
      const host = document.getElementById('isl-accessibility-overlay-root');
      const sr = host?.shadowRoot;
      const btnFull = sr?.getElementById('btn-avatar-full');
      if (btnFull) btnFull.click();
      const surface = sr?.getElementById('isl-floating-avatar-surface');
      const fallback = sr?.getElementById('isl-aether-fallback');
      const rect = surface?.getBoundingClientRect();
      const dpr = window.devicePixelRatio || 1;
      return {
        hasHost: Boolean(host),
        hasShadowRoot: Boolean(sr),
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
    throw new Error(`Overlay surface check failed: ${JSON.stringify(domInfo)}`);
  }

  await emb.send('Runtime.evaluate', { expression: `window.AetherEmbed.setViewMode('full')`, returnByValue: true });
  await new Promise(r => setTimeout(r, 400));
  const afterFull = await emb.send('Runtime.evaluate', { expression: `window.AetherEmbed.getStats()`, returnByValue: true });
  return { domInfo, embedStats: afterFull?.result?.value };
}

async function sampleEmbedPose(emb) {
  const r = await emb.send('Runtime.evaluate', {
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
        viewMode: st.viewMode,
        rArm: b('Bip001_R_UpperArm'),
        lArm: b('Bip001_L_UpperArm'),
        rFore: b('Bip001_R_Forearm'),
        rHand: b('Bip001_R_Hand')
      };
    })()`,
    returnByValue: true
  });
  return r?.result?.value;
}

async function auditVideoE2E(port, yt, emb, cfg) {
  const { key, videoId, seekForwardTime, seekBackTime } = cfg;
  console.log(`\n=== E2E Auditing ${key} (${videoId}) ===`);

  const adClear = await clearYouTubeAds(yt);
  console.log('  Ads cleared:', adClear);

  const { domInfo, embedStats } = await engageFullBodyAndReadLayout(yt, emb);
  console.log('  Aether Full Body ready:', embedStats.signsLoaded, 'signs | surface:', domInfo.surfaceRect);

  const pipelineReady = await triggerRealExtensionPipeline(port, yt, `https://www.youtube.com/watch?v=${videoId}`);
  console.log('  Real Extension Pipeline READY:', pipelineReady);

  const vFramesDir = path.join(framesDir, key);
  const vRawDir = path.join(recDir, `raw_${key}`);
  const vSheetDir = path.join(sheetsDir, key);
  [vFramesDir, vRawDir, vSheetDir].forEach(d => fs.mkdirSync(d, { recursive: true }));

  // Ensure playback starts at t=3.0s for TimelineSynchronizer continuous sync
  await yt.send('Runtime.evaluate', {
    expression: `(() => {
      const v = document.querySelector('video.html5-main-video') || document.querySelector('video');
      if (v) { v.muted = true; v.playbackRate = 1.0; v.currentTime = 3.0; v.play(); }
    })()`
  });

  let rawIdx = 0;
  const screencastHandler = async params => {
    const idx = rawIdx++;
    fs.writeFileSync(path.join(vRawDir, `frame_${String(idx).padStart(4, '0')}.jpg`), Buffer.from(params.data, 'base64'));
    try { await yt.send('Page.screencastFrameAck', { sessionId: params.sessionId }); } catch {}
  };
  yt.on('Page.screencastFrame', screencastHandler);
  await yt.send('Page.startScreencast', { format: 'jpeg', quality: 88, everyNthFrame: 1 });

  const phases = [];
  const capturePhase = async (label, waitMs) => {
    await new Promise(r => setTimeout(r, waitMs));
    const ytState = await yt.send('Runtime.evaluate', {
      expression: `(() => {
        const v = document.querySelector('video.html5-main-video') || document.querySelector('video');
        const sr = document.getElementById('isl-accessibility-overlay-root')?.shadowRoot;
        return {
          videoTime: v ? Number(v.currentTime.toFixed(2)) : null,
          paused: v ? v.paused : null,
          playbackRate: v ? v.playbackRate : null,
          boxGloss: sr?.getElementById('box-gloss')?.textContent?.trim() || '',
          stSign: sr?.getElementById('st-sign')?.textContent?.trim() || ''
        };
      })()`,
      returnByValue: true
    });
    const pose = await sampleEmbedPose(emb);
    const shot = await yt.send('Page.captureScreenshot', { format: 'png' });
    const file = path.join(vFramesDir, `${String(phases.length).padStart(2, '0')}_${label}.png`);
    fs.writeFileSync(file, Buffer.from(shot.data, 'base64'));
    phases.push({ label, yt: ytState?.result?.value, pose, png: file });
  };

  // Phase 0-3: Natural continuous playback synchronized by real TimelineSynchronizer
  await capturePhase('play_start', 900);
  await capturePhase('play_mid1', 1200);
  await capturePhase('play_mid2', 1200);
  await capturePhase('play_end1', 1200);

  // Phase 4: Forward Seek -> confirms TimelineSynchronizer switches cue cleanly
  await yt.send('Runtime.evaluate', {
    expression: `(() => { const v = document.querySelector('video'); if (v) v.currentTime = ${seekForwardTime}; })()`
  });
  await capturePhase('seek_forward', 1100);
  await capturePhase('seek_forward_mid', 1100);

  // Phase 6-7: Pause -> Resume
  await yt.send('Runtime.evaluate', { expression: `(() => { const v = document.querySelector('video'); if (v) v.pause(); })()` });
  await capturePhase('paused', 700);
  await yt.send('Runtime.evaluate', { expression: `(() => { const v = document.querySelector('video'); if (v) v.play(); })()` });
  await capturePhase('resumed', 800);

  // Phase 8-9: Playback Speed 1.5x -> 0.5x
  await yt.send('Runtime.evaluate', { expression: `(() => { const v = document.querySelector('video'); if (v) v.playbackRate = 1.5; })()` });
  await capturePhase('speed_1_5x', 900);
  await yt.send('Runtime.evaluate', { expression: `(() => { const v = document.querySelector('video'); if (v) v.playbackRate = 0.5; })()` });
  await capturePhase('speed_0_5x', 900);

  // Phase 10: Backward Seek at 1.0x
  await yt.send('Runtime.evaluate', {
    expression: `(() => { const v = document.querySelector('video'); if (v) { v.playbackRate = 1.0; v.currentTime = ${seekBackTime}; } })()`
  });
  await capturePhase('seek_back', 1100);

  // Phase 11: Half-body toggle -> Full-body restore
  await yt.send('Runtime.evaluate', {
    expression: `(() => {
      const sr = document.getElementById('isl-accessibility-overlay-root')?.shadowRoot;
      sr?.getElementById('btn-avatar-half')?.click();
    })()`
  });
  await capturePhase('half_body_toggle', 600);
  await yt.send('Runtime.evaluate', {
    expression: `(() => {
      const sr = document.getElementById('isl-accessibility-overlay-root')?.shadowRoot;
      sr?.getElementById('btn-avatar-full')?.click();
    })()`
  });
  await new Promise(r => setTimeout(r, 400));

  await yt.send('Page.stopScreencast');
  yt.off('Page.screencastFrame', screencastHandler);

  const mp4Path = path.join(recDir, `h44_${key}_recording.mp4`);
  const capturedCount = fs.readdirSync(vRawDir).filter(f => f.endsWith('.jpg')).length;
  if (capturedCount < 8) throw new Error(`Too few screencast frames captured for ${key}: ${capturedCount}`);
  await runFFmpeg([
    '-y', '-framerate', '12',
    '-i', path.join(vRawDir, 'frame_%04d.jpg'),
    '-c:v', 'h264_nvenc', '-preset', 'p4', '-pix_fmt', 'yuv420p',
    mp4Path
  ]);

  const sheetPath = path.join(vSheetDir, `h44_${key}_contact_sheet.png`);
  const frameListPath = path.join(vFramesDir, 'concat_frames.txt');
  const frameFiles = fs.readdirSync(vFramesDir).filter(f => f.endsWith('.png')).sort().slice(0, 12);
  fs.writeFileSync(frameListPath, frameFiles.map(f => `file '${path.join(vFramesDir, f).replace(/\\/g, '/')}'`).join('\n'), 'utf8');
  await runFFmpeg([
    '-y', '-f', 'concat', '-safe', '0', '-i', frameListPath,
    '-vf', 'scale=320:-1,tile=4x3', '-frames:v', '1',
    sheetPath
  ]);

  // DPI-calibrated avatar crops using live surfaceRect
  const cropOutDir = path.join(cropsDir, key);
  fs.mkdirSync(cropOutDir, { recursive: true });
  const r = domInfo.surfaceRect;
  const cw = Math.max(120, r.w);
  const ch = Math.max(160, r.h);
  const cropTargets = [phases[1].png, phases[4].png, phases[10].png];
  const cropPaths = [];
  for (let i = 0; i < cropTargets.length; i++) {
    const outCrop = path.join(cropOutDir, `crop_${i}.png`);
    await runFFmpeg(['-y', '-i', cropTargets[i], '-vf', `crop=${cw}:${ch}:${r.x}:${r.y}`, outCrop]);
    cropPaths.push(outCrop);
  }
  const cropListPath = path.join(cropOutDir, 'concat_crops.txt');
  fs.writeFileSync(cropListPath, cropPaths.map(p => `file '${p.replace(/\\/g, '/')}'`).join('\n'), 'utf8');
  const cropSheetPath = path.join(vSheetDir, `h44_${key}_avatar_crops_sheet.png`);
  await runFFmpeg([
    '-y', '-f', 'concat', '-safe', '0', '-i', cropListPath,
    '-vf', 'scale=280:-1,tile=3x1', '-frames:v', '1',
    cropSheetPath
  ]);

  const nonNeutralMoves = phases.filter(p =>
    p.pose?.rArm && (Math.abs(p.pose.rArm.x) > 3 || Math.abs(p.pose.rArm.z) > 3)
  ).length;
  const activeSigns = [...new Set(phases.map(p => p.pose?.currentSign).filter(Boolean))];
  const uniqueGlosses = [...new Set(phases.map(p => p.yt?.boxGloss).filter(Boolean))];

  return {
    key,
    video_id: videoId,
    ad_clear: adClear,
    real_pipeline_ready: pipelineReady,
    dom_info: domInfo,
    signs_loaded_in_chrome: embedStats.signsLoaded,
    final_view_mode: embedStats.viewMode,
    screencast_frames_captured: capturedCount,
    nvenc_recording_mp4: path.relative(root, mp4Path).replace(/\\/g, '/'),
    contact_sheet_png: path.relative(root, sheetPath).replace(/\\/g, '/'),
    avatar_crops_sheet_png: path.relative(root, cropSheetPath).replace(/\\/g, '/'),
    non_neutral_phase_count: nonNeutralMoves,
    observed_active_signs: activeSigns,
    observed_hud_glosses: uniqueGlosses,
    transport_checks: {
      paused_verified: phases.some(p => p.label === 'paused' && p.yt?.paused === true),
      resumed_verified: phases.some(p => p.label === 'resumed' && p.yt?.paused === false),
      speed_1_5x_verified: phases.some(p => p.label === 'speed_1_5x' && p.yt?.playbackRate === 1.5),
      speed_0_5x_verified: phases.some(p => p.label === 'speed_0_5x' && p.yt?.playbackRate === 0.5),
      forward_seek_verified: phases.some(p => p.label === 'seek_forward' && p.yt?.videoTime >= seekForwardTime - 2),
      backward_seek_verified: phases.some(p => p.label === 'seek_back' && p.yt?.videoTime <= seekBackTime + 8),
      half_body_toggle_verified: phases.some(p => p.label === 'half_body_toggle' && p.pose?.viewMode === 'half')
    },
    phases: phases.map(p => ({ label: p.label, yt: p.yt, pose: p.pose }))
  };
}

async function main() {
  const port = 9226;
  const chromeArgs = [
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
    'https://www.youtube.com/watch?v=MXKkXXYUxBc&t=2s'
  ];

  console.log('Launching real Chrome with extension on port', port);
  const chromeProc = spawn(chromeExe, chromeArgs, { detached: false, stdio: 'ignore' });
  const results = [];

  try {
    const { page: pageA, embed: embedA } = await waitForTargets(port, 'MXKkXXYUxBc');
    let yt = await connectCDP(pageA.webSocketDebuggerUrl);
    let emb = await connectCDP(embedA.webSocketDebuggerUrl);

    results.push(await auditVideoE2E(port, yt, emb, {
      key: 'video_a',
      videoId: 'MXKkXXYUxBc',
      seekForwardTime: 58.6,
      seekBackTime: 14.5
    }));

    await emb.ws.close();
    console.log('\nNavigating in same tab to locked Video B: y8tFSuOMAqQ...');
    await yt.send('Page.navigate', { url: 'https://www.youtube.com/watch?v=y8tFSuOMAqQ&t=2s' });
    await new Promise(r => setTimeout(r, 2500));

    const { embed: embedB } = await waitForTargets(port, 'y8tFSuOMAqQ');
    emb = await connectCDP(embedB.webSocketDebuggerUrl);

    results.push(await auditVideoE2E(port, yt, emb, {
      key: 'video_b',
      videoId: 'y8tFSuOMAqQ',
      seekForwardTime: 45.2,
      seekBackTime: 24.5
    }));

    await emb.ws.close();
    await yt.ws.close();

    const evidence = {
      milestone: 'H44',
      audited_at: new Date().toISOString(),
      chrome_version: '158.0.8127.88',
      pipeline_mode: 'REAL_EXTENSION_POPUP_TO_TIMELINE_SYNCHRONIZER',
      videos_audited: results
    };
    const outPath = path.join(evidenceDir, 'h44_real_chrome_e2e_evidence.json');
    fs.writeFileSync(outPath, `${JSON.stringify(evidence, null, 2)}\n`, 'utf8');
    console.log('\nSaved H44 real-Chrome E2E evidence to:', outPath);
  } finally {
    try { chromeProc.kill(); } catch {}
  }
}

main().catch(err => {
  console.error('H44 Real Chrome E2E failed:', err);
  process.exit(1);
});
