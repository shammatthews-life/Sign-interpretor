import assert from 'node:assert/strict';
import { createRequire } from 'node:module';
import { test } from 'node:test';

const require = createRequire(import.meta.url);
const { ISLOverlayUI } = require('./overlay.js');

function classList() {
  const classes = new Set();
  return {
    add(...names) {
      names.forEach(name => classes.add(name));
    },
    remove(...names) {
      names.forEach(name => classes.delete(name));
    },
    toggle(name, force) {
      const add = force === undefined ? !classes.has(name) : force;
      if (add) classes.add(name);
      else classes.delete(name);
      return add;
    },
    contains(name) {
      return classes.has(name);
    }
  };
}

function eventTarget() {
  return {
    classList: classList(),
    style: {},
    dataset: {},
    attributes: {},
    listeners: {},
    addEventListener(type, listener) {
      this.listeners[type] = listener;
    },
    setAttribute(name, value) {
      this.attributes[name] = String(value);
    },
    getAttribute(name) {
      return this.attributes[name];
    },
    querySelector() {
      return { textContent: '' };
    }
  };
}

test('avatar detachment state follows the floating surface in both directions', () => {
  const ui = new ISLOverlayUI();
  const containerClasses = classList();
  const floatingClasses = classList();
  const dragClasses = classList();
  const detachedClasses = classList();
  const dockClasses = classList();
  const dragLabel = { textContent: '' };
  ui.elements = {
    container: { classList: containerClasses },
    floatingSurface: { classList: floatingClasses, style: {} },
    detachedNote: { classList: detachedClasses },
    btnAvatarDock: { classList: dockClasses },
    btnAvatarDrag: {
      classList: dragClasses,
      setAttribute() {},
      querySelector: () => dragLabel
    }
  };
  ui.syncAvatarSurface = () => {};

  ui.setAvatarFloating(true);
  assert.equal(containerClasses.contains('avatar-detached'), true);

  ui.setAvatarFloating(false);
  assert.equal(containerClasses.contains('avatar-detached'), false);
  assert.equal(ui.isAvatarFloating, false);
});

test('viewport changes recalculate the default floating position but preserve a user position', () => {
  const ui = new ISLOverlayUI();
  ui.isAvatarFloating = true;
  ui.floatingPositionInitialized = true;
  ui.syncAvatarSurface = options => {
    ui.lastSyncOptions = options;
  };

  ui.handleAvatarViewportChange();
  assert.equal(ui.floatingPositionInitialized, false);
  assert.deepEqual(ui.lastSyncOptions, { clampFloating: true });

  ui.floatingPositionInitialized = true;
  ui.avatarPositionUserSet = true;
  ui.handleAvatarViewportChange();
  assert.equal(ui.floatingPositionInitialized, true);
});

test('viewport resize places the untouched floating avatar beside rather than over the sidebar', () => {
  const ui = new ISLOverlayUI();
  const surface = {
    classList: classList(),
    style: {},
    getBoundingClientRect: () => ({ left: 0, top: 0, width: 320, height: 400 })
  };
  ui.elements = {
    floatingSurface: surface,
    container: { getBoundingClientRect: () => ({ width: 200 }) }
  };
  ui.avatarViewportPlaceholder = {};
  ui.isAvatarFloating = true;
  ui.isVisible = true;
  ui.floatingPositionInitialized = true;

  const previousWindow = globalThis.window;
  globalThis.window = { innerWidth: 1000, innerHeight: 800 };
  try {
    ui.handleAvatarViewportChange();
    assert.equal(surface.style.left, '456px');
    assert.equal(surface.style.top, '374px');
  } finally {
    if (previousWindow === undefined) delete globalThis.window;
    else globalThis.window = previousWindow;
  }
});

test('drag bounds let the floating avatar move across the full viewport', () => {
  const ui = new ISLOverlayUI();
  ui.isAvatarFloating = true;

  const previousWindow = globalThis.window;
  globalThis.window = { innerWidth: 1036 };
  try {
    assert.ok(Math.abs(ui.getMaxFloatingLeft(310.8) - 717.2) < 1e-9);
  } finally {
    if (previousWindow === undefined) delete globalThis.window;
    else globalThis.window = previousWindow;
  }
});

test('overlay visibility and layout changes leave YouTube page layout untouched', () => {
  const ui = new ISLOverlayUI();
  const elementNames = ['container', 'sidebarToggle', 'launcher', 'btnMinimize'];
  ui.elements = Object.fromEntries(elementNames.map(name => [name, eventTarget()]));
  const primary = { style: { marginRight: '12px', transition: 'all 0.2s' } };
  const attributes = new Map();
  let hostPageAccesses = 0;
  const previousDocument = globalThis.document;
  globalThis.document = {
    documentElement: {
      setAttribute(name, value) {
        hostPageAccesses += 1;
        attributes.set(name, value);
      },
      removeAttribute(name) {
        hostPageAccesses += 1;
        attributes.delete(name);
      }
    },
    querySelector() {
      hostPageAccesses += 1;
      return primary;
    }
  };
  ui.syncAvatarSurface = () => {};

  try {
    ui.toggleMinimize();
    ui.hide();
    ui.show();
    ui.toggleLayoutMode();

    assert.equal(primary.style.marginRight, '12px');
    assert.equal(primary.style.transition, 'all 0.2s');
    assert.equal(attributes.has('data-isl-sidebar-active'), false);
    assert.equal(hostPageAccesses, 0);
  } finally {
    if (previousDocument === undefined) delete globalThis.document;
    else globalThis.document = previousDocument;
  }
});

test('drag mode locks movement when off and retains the chosen position when disabled', () => {
  const ui = new ISLOverlayUI();
  const grip = eventTarget();
  const surfaceClasses = classList();
  const surface = {
    classList: surfaceClasses,
    style: {},
    offsetWidth: 320,
    offsetHeight: 400,
    getBoundingClientRect: () => ({ left: 100, top: 80 })
  };
  const dragLabel = { textContent: '' };
  const dragButton = eventTarget();
  dragButton.querySelector = () => dragLabel;
  dragButton.setAttribute = () => {};
  grip.capturedPointerIds = [];
  grip.setPointerCapture = pointerId => grip.capturedPointerIds.push(pointerId);
  ui.elements = { avatarGrip: grip, floatingSurface: surface, btnAvatarDrag: dragButton };
  ui.isAvatarFloating = true;
  ui.syncAvatarSurface = () => {};

  const previousWindow = globalThis.window;
  globalThis.window = { innerWidth: 1000, innerHeight: 800 };
  try {
    ui.setupDragging();
    const pointerDown = (clientX, clientY) => ({
      button: 0,
      isPrimary: true,
      clientX,
      clientY,
      pointerId: 1,
      preventDefault() {}
    });

    grip.listeners.pointerdown(pointerDown(120, 100));
    grip.listeners.pointermove({ clientX: 180, clientY: 140 });
    assert.equal(ui.isDragging, false);
    assert.equal(surface.style.left, undefined);

    ui.toggleAvatarDrag();
    grip.listeners.pointerdown(pointerDown(120, 100));
    assert.deepEqual(grip.capturedPointerIds, [1]);

    grip.listeners.pointermove({ clientX: 900, clientY: 900, pointerId: 2 });
    assert.equal(surface.style.left, undefined);
    grip.listeners.pointerup({ pointerId: 2 });
    assert.equal(ui.isDragging, true);

    grip.listeners.pointermove({ clientX: 180, clientY: 140, pointerId: 1 });
    assert.equal(surface.style.left, '160px');
    assert.equal(surface.style.top, '120px');

    grip.listeners.pointerup({ pointerId: 1 });
    assert.equal(ui.isDragging, false);
    ui.toggleAvatarDrag();
    grip.listeners.pointerdown(pointerDown(180, 140));
    grip.listeners.pointermove({ clientX: 400, clientY: 400, pointerId: 1 });
    assert.equal(surface.style.left, '160px');
    assert.equal(surface.style.top, '120px');
    assert.equal(surfaceClasses.contains('drag-enabled'), false);
  } finally {
    if (previousWindow === undefined) delete globalThis.window;
    else globalThis.window = previousWindow;
  }
});

test('dragging clamps the floating avatar to the viewport and ends on pointer cancellation', () => {
  const ui = new ISLOverlayUI();
  const grip = eventTarget();
  const surface = {
    classList: classList(),
    style: {},
    offsetWidth: 200,
    offsetHeight: 200,
    getBoundingClientRect: () => ({ left: 100, top: 100 })
  };
  ui.elements = { avatarGrip: grip, floatingSurface: surface, btnAvatarDrag: eventTarget() };
  ui.isAvatarFloating = true;
  ui.isAvatarDragEnabled = true;
  ui.getMaxFloatingLeft = () => 292;

  const previousWindow = globalThis.window;
  globalThis.window = { innerWidth: 500, innerHeight: 400 };
  try {
    ui.setupDragging();
    grip.listeners.pointerdown({
      button: 0,
      isPrimary: true,
      clientX: 100,
      clientY: 100,
      pointerId: 7,
      preventDefault() {}
    });

    grip.listeners.pointermove({ clientX: 900, clientY: 900, pointerId: 7 });
    assert.equal(surface.style.left, '292px');
    assert.equal(surface.style.top, '192px');

    grip.listeners.pointermove({ clientX: 0, clientY: 0, pointerId: 7 });
    assert.equal(surface.style.left, '8px');
    assert.equal(surface.style.top, '8px');

    grip.listeners.pointercancel({ pointerId: 7 });
    assert.equal(ui.isDragging, false);
    assert.equal(ui.avatarDragPointerId, null);
  } finally {
    if (previousWindow === undefined) delete globalThis.window;
    else globalThis.window = previousWindow;
  }
});

test('closing the sidebar and clicking its reopen handle makes the controls visible again', () => {
  const ui = new ISLOverlayUI();
  const elementNames = [
    'container', 'btnMinimize', 'btnClose', 'launcher', 'sidebarToggle', 'appYoutube',
    'detailsPanel', 'detailsToggle', 'btnDemoStart', 'btnDemoStep',
    'btnDemoStop', 'selectScenario', 'btnReconnect', 'btnAvatarHello',
    'btnAvatarGood', 'btnAvatarMorning', 'btnAvatarWater', 'btnAvatarPause',
    'btnAvatarReset', 'btnAvatarHalf', 'btnAvatarFull', 'btnAvatarDrag',
    'btnAvatarDock'
  ];
  ui.elements = Object.fromEntries(elementNames.map(name => [name, eventTarget()]));
  ui.elements.selectScenario.value = 'greeting';
  ui.syncAvatarSurface = () => {};
  ui.bindEvents();

  ui.elements.btnClose.listeners.click();
  assert.equal(ui.isVisible, false);
  assert.equal(ui.elements.container.classList.contains('hidden'), true);
  assert.equal(ui.elements.sidebarToggle.classList.contains('hidden'), false);

  ui.elements.sidebarToggle.listeners.click();
  assert.equal(ui.isVisible, true);
  assert.equal(ui.elements.container.classList.contains('hidden'), false);
  assert.equal(ui.elements.sidebarToggle.classList.contains('hidden'), true);
});

test('avatar size presets switch classes and enforce supported sizing modes', () => {
  const ui = new ISLOverlayUI();
  const surface = {
    classList: classList(),
    style: {},
    getBoundingClientRect: () => ({ left: 0, top: 0, width: 320, height: 480 })
  };
  const compactBtn = eventTarget();
  const standardBtn = eventTarget();
  const largeBtn = eventTarget();
  compactBtn.dataset.size = 'compact';
  standardBtn.dataset.size = 'standard';
  largeBtn.dataset.size = 'large';

  ui.elements = {
    floatingSurface: surface,
    btnSizeCompact: compactBtn,
    btnSizeStandard: standardBtn,
    btnSizeLarge: largeBtn
  };
  ui.handleAvatarViewportChange = () => { ui.viewportChanged = true; };

  // Initial standard size
  assert.equal(ui.avatarSizePreset, 'standard');

  // Switch to compact
  ui.setAvatarSize('compact');
  assert.equal(ui.avatarSizePreset, 'compact');
  assert.equal(surface.classList.contains('size-compact'), true);
  assert.equal(surface.classList.contains('size-standard'), false);
  assert.equal(compactBtn.classList.contains('active'), true);
  assert.equal(compactBtn.attributes?.['aria-pressed'], 'true');
  assert.equal(standardBtn.classList.contains('active'), false);
  assert.equal(ui.viewportChanged, true);

  // Switch to large
  ui.setAvatarSize('large');
  assert.equal(ui.avatarSizePreset, 'large');
  assert.equal(surface.classList.contains('size-large'), true);
  assert.equal(surface.classList.contains('size-compact'), false);
  assert.equal(largeBtn.classList.contains('active'), true);
  assert.equal(largeBtn.attributes?.['aria-pressed'], 'true');

  // Rejects invalid size
  assert.throws(() => ui.setAvatarSize('enormous'), /Unsupported avatar size/);
});

test('auto-reconnect handles disconnected state and clears when connected', () => {
  const dispatched = [];
  const ui = new ISLOverlayUI({
    onAction: (type, payload) => dispatched.push({ type, payload })
  });

  const subClasses = classList();
  ui.elements = {
    stConn: eventTarget(),
    stAudio: eventTarget(),
    stAsr: eventTarget(),
    stTrans: eventTarget(),
    stSign: eventTarget(),
    boxPartial: { textContent: '' },
    boxFinal: { textContent: '' },
    youtubeJobState: { textContent: '' },
    youtubeJobId: { textContent: '' },
    youtubeVideoTitle: { textContent: '' },
    youtubeSegmentCount: { textContent: '' },
    youtubeLatestSegment: { textContent: '' },
    youtubeTranscriptSummary: { textContent: '' },
    youtubeTranslationStatus: { textContent: '' },
    youtubeGlosses: { textContent: '' },
    youtubePlayableSigns: { textContent: '' },
    youtubeUnavailableConcepts: { textContent: '' },
    youtubeJobProgress: { textContent: '' },
    youtubeJobError: { textContent: '', classList: classList() },
    badgeTransStatus: { textContent: '' },
    boxGloss: { textContent: '' },
    boxTrace: { textContent: '' },
    pillActiveSign: { textContent: '', style: {} },
    txtNoActive: { style: {} },
    pillReviewBadge: { classList: classList() },
    boxQueuedSigns: { innerHTML: '' },
    boxUnavailable: { classList: classList() },
    listUnavailable: { innerHTML: '' },
    demoIndicator: { textContent: '', style: {} },
    txtRuntimeMsg: { textContent: '', style: {} },
    aetherIframe: { src: '', classList: classList() },
    aetherFallback: { classList: classList() },
    unavailableSubtitle: { classList: subClasses },
    unavailableSubText: { textContent: '' }
  };
  ui.syncAvatarSurface = () => {};

  // Offline state schedules reconnect
  ui.update({ runtimeAvailable: false, runtimeError: 'Offline' });
  assert.ok(ui.autoReconnectTimer !== null);

  // Online state stops reconnect
  ui.update({ runtimeAvailable: true, runtimeEndpoint: 'http://localhost:8000' });
  assert.equal(ui.autoReconnectTimer, null);
  assert.equal(ui.autoReconnectDelayMs, 2000);

  // Cleanup stops reconnect
  ui.scheduleAutoReconnect();
  assert.ok(ui.autoReconnectTimer !== null);
  ui.destroy();
  assert.equal(ui.autoReconnectTimer, null);
});

test('unavailable subtitle fallback pill displays and clears cleanly', () => {
  const ui = new ISLOverlayUI();
  const subClasses = classList();
  const subText = { textContent: '' };
  ui.elements = {
    unavailableSubtitle: { classList: subClasses },
    unavailableSubText: subText
  };

  ui.setUnavailableFallback('quantum', 0);
  assert.equal(subText.textContent, 'quantum');
  assert.equal(subClasses.contains('hidden'), false);

  ui.setUnavailableFallback(null);
  assert.equal(subText.textContent, '');
  assert.equal(subClasses.contains('hidden'), true);
});
