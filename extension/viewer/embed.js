import * as THREE from '../vendor/three/three.module.min.js';
import { OrbitControls } from '../vendor/three/addons/controls/OrbitControls.js';
import { FBXLoader } from '../vendor/three/addons/loaders/FBXLoader.js';
import { SignLibrary } from './engine/SignLibrary.js';
import { SignAnimationPlayer } from './engine/SignAnimationPlayer.js';
import { SignScheduler } from './engine/SignScheduler.js';
import { setAvatarCameraView } from './engine/AvatarCameraView.mjs';
import { correctNonFiniteHelperBoneRotations } from './engine/NonFiniteHelperBoneCorrection.mjs';
import { takePendingAetherEvent } from './engine/PendingAetherQueue.js';

const params = new URLSearchParams(window.location.search);
function resolveRuntimeEndpoint(raw) {
  try {
    const parsed = new URL(raw || 'http://localhost:8000');
    if (['http:', 'https:'].includes(parsed.protocol) && ['localhost', '127.0.0.1'].includes(parsed.hostname)) {
      return parsed.origin;
    }
  } catch {
    // Fallback below
  }
  return 'http://localhost:8000';
}

const RUNTIME_ENDPOINT = resolveRuntimeEndpoint(params.get('endpoint'));
const PARENT_ORIGIN = params.get('parentOrigin') || 'https://www.youtube.com';

const canvas = document.getElementById('viewer-canvas');
const statusOverlay = document.getElementById('embed-status');
const hud = document.getElementById('embed-hud');

const scene = new THREE.Scene();
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true, preserveDrawingBuffer: true });
renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.1;

const camera = new THREE.PerspectiveCamera(45, Math.max(1, window.innerWidth) / Math.max(1, window.innerHeight), 0.05, 50);
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.enablePan = false;
controls.minDistance = 0.4;
controls.maxDistance = 5.0;
setAvatarCameraView(camera, controls, 'half');

// Balanced 3-point lighting for WebGL avatar readability
scene.add(new THREE.AmbientLight(0xdbeafe, 1.35));
scene.add(new THREE.HemisphereLight(0xf0f9ff, 0x1e293b, 1.15));
const keyLight = new THREE.DirectionalLight(0xffffff, 2.0);
keyLight.position.set(1.6, 2.8, 2.4);
scene.add(keyLight);
const fillLight = new THREE.DirectionalLight(0x93c5fd, 0.9);
fillLight.position.set(-2.0, 1.5, 1.4);
scene.add(fillLight);
const rimLight = new THREE.DirectionalLight(0xe0f2fe, 0.85);
rimLight.position.set(0, 2.2, -2.5);
scene.add(rimLight);

function resizeRenderer() {
  const width = Math.max(1, window.innerWidth);
  const height = Math.max(1, window.innerHeight);
  camera.aspect = width / height;
  camera.updateProjectionMatrix();
  renderer.setSize(width, height, false);
  if (currentViewMode) {
    setAvatarCameraView(camera, controls, currentViewMode);
  }
}

let currentViewMode = 'half';
window.addEventListener('resize', resizeRenderer);
resizeRenderer();

const bonesMap = new Map();
const HandRig = {
  left: { hand: null, thumb: [], index: [], middle: [], ring: [], pinky: [] },
  right: { hand: null, thumb: [], index: [], middle: [], ring: [], pinky: [] }
};

function buildRigMaps(fbx) {
  bonesMap.clear();
  for (const side of ['left', 'right']) {
    HandRig[side].hand = null;
    for (const f of ['thumb', 'index', 'middle', 'ring', 'pinky']) HandRig[side][f] = [];
  }

  fbx.traverse(obj => {
    if (obj.isMesh) {
      obj.frustumCulled = false;
      const mats = Array.isArray(obj.material) ? obj.material : [obj.material];
      mats.forEach(m => {
        if (m) m.side = THREE.DoubleSide;
      });
    }
    if (obj.isBone) {
      obj.userData.initialRotation = obj.rotation.clone();
      bonesMap.set(obj.name, obj);
    }
  });

  const fingerSuffixes = {
    thumb: ['0', '01', '02'],
    index: ['1', '11', '12'],
    middle: ['2', '21', '22'],
    ring: ['3', '31', '32'],
    pinky: ['4', '41', '42']
  };
  for (const [side, code] of [['left', 'L'], ['right', 'R']]) {
    HandRig[side].hand = bonesMap.get(`Bip001_${code}_Hand`) || null;
    for (const [finger, suffixes] of Object.entries(fingerSuffixes)) {
      HandRig[side][finger] = suffixes
        .map(s => bonesMap.get(`Bip001_${code}_Finger${s}`))
        .filter(Boolean);
    }
  }
}

let signLibrary = null;
let signPlayer = null;
let signScheduler = null;
let viewerReady = false;
let expectedParentOrigin = PARENT_ORIGIN;
const pendingStartEvents = new Map();
const preReadyCommands = [];

function postToParent(payload) {
  if (!window.parent || window.parent === window) return;
  try {
    window.parent.postMessage(payload, expectedParentOrigin || '*');
  } catch {
    try {
      window.parent.postMessage(payload, '*');
    } catch {
      // Ignore cross-origin edge errors
    }
  }
}

function publishSchedulerState() {
  const schedState = signScheduler ? signScheduler.getState() : { current: null, queued: [], paused: false };
  const snapshot = {
    ...schedState,
    playbackSpeed: signPlayer?.playbackSpeed || 1.0,
    viewMode: currentViewMode
  };

  const activeId = snapshot.current;
  hud.textContent = activeId
    ? `Signing: ${String(activeId).toUpperCase()} (${currentViewMode})`
    : `Aether Ready (${signLibrary?.cache?.size || 0} signs · ${currentViewMode})`;

  postToParent({
    type: 'ISL_AETHER_STATE',
    state: snapshot
  });
}

function handleCommandMessage(data) {
  if (data.parentOrigin && /^https:\/\/([a-z0-9-]+\.)?youtube\.com$/i.test(data.parentOrigin)) {
    expectedParentOrigin = data.parentOrigin;
  }

  const eventId = data.eventId;
  if (!viewerReady || !signScheduler || !signPlayer) {
    if (data.command === 'SET_AVATAR_VIEW' && ['half', 'full'].includes(data.viewMode)) {
      currentViewMode = data.viewMode;
      setAvatarCameraView(camera, controls, currentViewMode);
    }
    if (eventId) {
      postToParent({ type: 'ISL_AETHER_ACK', eventId, status: 'retry', reason: 'Viewer initializing' });
    }
    if (preReadyCommands.length < 32 && ['CUE_TRANSITION', 'SET_AVATAR_VIEW', 'CANCEL_JOB', 'RESET_AVATAR'].includes(data.command)) {
      preReadyCommands.push(data);
    }
    return;
  }

  if (data.command === 'SET_AVATAR_VIEW') {
    if (['half', 'full'].includes(data.viewMode)) {
      currentViewMode = data.viewMode;
      setAvatarCameraView(camera, controls, currentViewMode);
      publishSchedulerState();
      if (eventId) postToParent({ type: 'ISL_AETHER_ACK', eventId, status: 'accepted' });
    } else if (eventId) {
      postToParent({ type: 'ISL_AETHER_ACK', eventId, status: 'rejected', reason: 'Invalid viewMode' });
    }
    return;
  }

  if (data.command === 'PAUSE') {
    signScheduler.pause();
    publishSchedulerState();
    if (eventId) postToParent({ type: 'ISL_AETHER_ACK', eventId, status: 'accepted' });
    return;
  }

  if (data.command === 'RESUME') {
    signScheduler.resume();
    publishSchedulerState();
    if (eventId) postToParent({ type: 'ISL_AETHER_ACK', eventId, status: 'accepted' });
    return;
  }

  if (data.command === 'SET_PLAYBACK_RATE') {
    const rate = Number(data.rate);
    if (Number.isFinite(rate) && rate > 0) {
      signPlayer.playbackSpeed = Math.max(0.5, Math.min(2.5, rate));
      publishSchedulerState();
      if (eventId) postToParent({ type: 'ISL_AETHER_ACK', eventId, status: 'accepted' });
    } else if (eventId) {
      postToParent({ type: 'ISL_AETHER_ACK', eventId, status: 'rejected', reason: 'Invalid playback rate' });
    }
    return;
  }

  if (data.command === 'RESET_AVATAR') {
    signScheduler.cancel();
    signPlayer.resetNeutral();
    pendingStartEvents.clear();
    publishSchedulerState();
    if (eventId) postToParent({ type: 'ISL_AETHER_ACK', eventId, status: 'accepted' });
    return;
  }

  if (data.command === 'CANCEL_JOB') {
    signScheduler.cancelJob(data.jobId);
    publishSchedulerState();
    if (eventId) postToParent({ type: 'ISL_AETHER_ACK', eventId, status: 'accepted' });
    return;
  }

  if (data.command === 'CANCEL_EVENT') {
    if (data.targetEventId) {
      signScheduler.cancelEvent(data.targetEventId);
    }
    publishSchedulerState();
    if (eventId) postToParent({ type: 'ISL_AETHER_ACK', eventId, status: 'accepted' });
    return;
  }

  if (data.command === 'CUE_TRANSITION') {
    if (typeof signScheduler.advanceCue === 'function') {
      signScheduler.advanceCue(data.jobId, data.cueId);
    }
    publishSchedulerState();
    if (eventId) postToParent({ type: 'ISL_AETHER_ACK', eventId, status: 'accepted' });
    return;
  }

  if (data.command === 'PLAY_SIGN' || data.command === 'QUEUE_SIGN') {
    const signId = String(data.signId || '').trim().toLowerCase();
    if (!signId) {
      if (eventId) postToParent({ type: 'ISL_AETHER_ACK', eventId, status: 'rejected', reason: 'Missing signId' });
      return;
    }

    if (eventId) {
      pendingStartEvents.set(eventId, {
        eventId,
        signId,
        cueId: data.cueId ?? null,
        jobId: data.jobId ?? null,
        occurrenceIndex: data.occurrenceIndex ?? null
      });
    }

    if (data.command === 'PLAY_SIGN') {
      signScheduler.cancel();
    }

    const res = signScheduler.enqueue(
      signId,
      eventId ?? null,
      data.cueId ?? null,
      data.jobId ?? null,
      {
        cueStartSeconds: Number.isFinite(data.cueStartSeconds) ? data.cueStartSeconds : null,
        cueEndSeconds: Number.isFinite(data.cueEndSeconds) ? data.cueEndSeconds : null,
        nonManualMarkers: Array.isArray(data.nonManualMarkers) ? data.nonManualMarkers : [],
        spatialYawDeg: Number.isFinite(data.spatialYawDeg) ? data.spatialYawDeg : 0
      }
    );

    if (!res?.accepted) {
      takePendingAetherEvent(pendingStartEvents, eventId);
      if (eventId) postToParent({ type: 'ISL_AETHER_ACK', eventId, status: 'rejected', reason: res?.reason || `Sign '${signId}' rejected` });
    } else if (eventId) {
      postToParent({ type: 'ISL_AETHER_ACK', eventId, status: 'accepted' });
    }
    publishSchedulerState();
  }
}

window.addEventListener('message', event => {
  if (event.source !== window.parent) return;
  const data = event.data;
  if (!data || data.type !== 'ISL_AETHER_COMMAND') return;
  handleCommandMessage(data);
});

async function initializeEmbedViewer() {
  try {
    statusOverlay.textContent = 'Loading Aether 3D rig & ISL lexicon...';
    signLibrary = new SignLibrary({
      basePath: `${RUNTIME_ENDPOINT}/signs`,
      fetchImpl: (url, opts) => window.fetch(url, opts)
    });

    const fbxLoader = new FBXLoader();
    fbxLoader.setPath(`${RUNTIME_ENDPOINT}/Avatar_Boy_Gun_AetherShadow/`);
    fbxLoader.setResourcePath(`${RUNTIME_ENDPOINT}/Avatar_Boy_Gun_AetherShadow/`);

    const [bundleSummary, fbx] = await Promise.all([
      signLibrary.preloadBundle(`${RUNTIME_ENDPOINT}/signs/bundle.json`, `${RUNTIME_ENDPOINT}/signs/manifest.json`),
      fbxLoader.loadAsync('Avatar_Boy_Gun_AetherShadow.fbx')
    ]);

    // Normalize scale & ground placement to match calibrated camera rig (height ~1.7m, feet at y=0)
    const rawBox = new THREE.Box3().setFromObject(fbx);
    const rawSize = new THREE.Vector3();
    rawBox.getSize(rawSize);
    if (rawSize.y > 5) {
      const scale = 1.72 / rawSize.y;
      fbx.scale.multiplyScalar(scale);
      fbx.updateMatrixWorld(true);
    }
    const groundedBox = new THREE.Box3().setFromObject(fbx);
    const center = new THREE.Vector3();
    groundedBox.getCenter(center);
    fbx.position.x -= center.x;
    fbx.position.z -= center.z;
    fbx.position.y -= groundedBox.min.y;
    scene.add(fbx);

    buildRigMaps(fbx);
    const protectedBones = [
      HandRig.left.hand,
      HandRig.right.hand,
      ...['thumb', 'index', 'middle', 'ring', 'pinky'].flatMap(f => [...HandRig.left[f], ...HandRig.right[f]])
    ].filter(Boolean);
    correctNonFiniteHelperBoneRotations({ model: fbx, protectedBones });

    signPlayer = new SignAnimationPlayer(fbx, bonesMap, HandRig);
    signScheduler = new SignScheduler(
      signPlayer,
      signLibrary,
      bonesMap,
      () => publishSchedulerState(),
      evt => {
        if (evt.type === 'playback_start' && evt.eventId) {
          takePendingAetherEvent(pendingStartEvents, evt.eventId);
        }
        postToParent({ type: 'ISL_AETHER_LIFECYCLE', event: evt });
        publishSchedulerState();
      }
    );

    setAvatarCameraView(camera, controls, currentViewMode);
    viewerReady = true;
    statusOverlay.classList.add('hidden');
    hud.textContent = `Aether Ready (${bundleSummary.loaded} signs · ${currentViewMode})`;

    window.AetherEmbed = {
      fbx,
      bonesMap,
      HandRig,
      signLibrary,
      signPlayer,
      signScheduler,
      camera,
      controls,
      getViewMode: () => currentViewMode,
      setViewMode: mode => {
        currentViewMode = mode;
        setAvatarCameraView(camera, controls, mode);
        publishSchedulerState();
      },
      getStats: () => ({
        signsLoaded: signLibrary.cache.size,
        bonesCount: bonesMap.size,
        currentSign: signScheduler.getState().current,
        queuedCount: signScheduler.queue?.length || 0,
        viewMode: currentViewMode
      })
    };

    postToParent({
      type: 'ISL_AETHER_READY',
      signsLoaded: bundleSummary.loaded,
      viewMode: currentViewMode
    });
    publishSchedulerState();

    while (preReadyCommands.length) {
      handleCommandMessage(preReadyCommands.shift());
    }
  } catch (error) {
    console.error('[Aether Embed] Initialization failed:', error);
    statusOverlay.textContent = `Avatar load error: ${error.message}`;
    postToParent({
      type: 'ISL_AETHER_ERROR',
      error: error.message
    });
  }
}

let lastTime = performance.now();
function animate(now) {
  requestAnimationFrame(animate);
  const deltaMs = Math.min(50, Math.max(0, now - lastTime));
  lastTime = now;
  if (signPlayer) {
    signPlayer.update(deltaMs);
  }
  controls.update();
  renderer.render(scene, camera);
}

requestAnimationFrame(animate);
initializeEmbedViewer();
