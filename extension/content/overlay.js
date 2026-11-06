/**
 * ISL Accessibility Translator - Overlay UI Component (Phase H24 Stunning Right Sidebar Edition)
 * Encapsulated inside Shadow DOM for total isolation from host page styles.
 */

(function (root, factory) {
  if (typeof exports === 'object' && typeof module !== 'undefined') {
    module.exports = factory();
  } else {
    root.ISLOverlay = factory();
  }
})(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  class ISLOverlayUI {
    constructor({ onAction = null } = {}) {
      this.onAction = onAction;
      this.hostElement = null;
      this.shadowRoot = null;
      this.elements = {};
      this.isMinimized = false;
      this.isSidebarMode = true; // Default: Modern right sidebar view
      this.isCollapsed = false;
      this.isVisible = true;
      this.isDragging = false;
      this.isAvatarFloating = false;
      this.isAvatarDragEnabled = false;
      this.avatarDragPointerId = null;
      this.avatarPositionUserSet = false;
      this.avatarViewMode = 'half';
      this.avatarSizePreset = 'standard'; // 'compact' | 'standard' | 'large'
      this.dragOffset = { x: 0, y: 0 };
      this.fallbackTimer = null;
      this.autoReconnectTimer = null;
      this.autoReconnectDelayMs = 2000;
      this.autoReconnectMaxDelayMs = 10000;
      this.autoReconnectEnabled = true;
    }

    /**
     * Mounts the overlay into the given container or creates host in document.body
     */
    mount(targetDoc = document) {
      if (this.hostElement) return;

      this.hostElement = targetDoc.createElement('div');
      this.hostElement.id = 'isl-accessibility-overlay-root';
      this.shadowRoot = this.hostElement.attachShadow({ mode: 'open' });

      // Build shadow DOM structure
      this.buildDOM();
      this.setupDragging();
      this.bindEvents();

      targetDoc.body.appendChild(this.hostElement);
      this.setAvatarFloating(true);
      this.resizeHandler = () => this.handleAvatarViewportChange();
      this.targetWindow = targetDoc.defaultView;
      this.targetWindow?.addEventListener('resize', this.resizeHandler);
    }

    buildDOM() {
      const container = document.createElement('div');
      container.innerHTML = `
        <!-- Floating Launcher Badge (for floating mode) -->
        <button id="isl-launcher-badge" class="hidden" type="button" title="Open ISL Translator" aria-label="Open ISL Translator">
          <span aria-hidden="true">🤟</span>
        </button>

        <!-- Right Edge Dock Toggle Handle (for collapsed sidebar) -->
        <button id="isl-sidebar-toggle-handle" class="hidden" type="button" title="Open ISL Translator" aria-label="Open ISL Translator">
          <span class="isl-handle-icon" aria-hidden="true">‹</span>
        </button>

        <div id="isl-floating-avatar-surface" class="hidden"></div>

        <!-- Main Container: Defaults to stunning right sidebar dock -->
        <div id="isl-overlay-container" class="sidebar-mode">
          <!-- Header Bar -->
          <div id="isl-header-bar">
            <div class="isl-title-group">
              <span class="isl-brand-mark" aria-hidden="true">🤟</span>
              <span class="isl-app-title">Aether<span> / ISL</span></span>
              <span id="isl-mode-badge" class="isl-version-tag">YOUTUBE</span>
            </div>
            <div class="isl-header-actions">
              <button id="btn-minimize" class="isl-icon-btn" type="button" title="Collapse sidebar" aria-label="Collapse sidebar">‹</button>
              <button id="btn-close" class="isl-icon-btn" type="button" title="Hide translator" aria-label="Hide translator">×</button>
            </div>
          </div>

          <div id="isl-app-layout">
            <nav id="isl-app-rail" aria-label="Translator apps">
              <button id="btn-app-youtube" class="isl-app-nav-button active" type="button" aria-current="page" title="YouTube">
                <span class="isl-youtube-mark" aria-hidden="true">▶</span>
                <span>YouTube</span>
              </button>
              <span class="isl-nav-spacer"></span>
              <button id="btn-details-toggle" class="isl-app-nav-button isl-details-nav" type="button" aria-expanded="false" aria-controls="isl-details-panel" title="Translation details">
                <span aria-hidden="true">⌘</span>
                <span>Details</span>
              </button>
            </nav>

            <main id="isl-main-column">
              <details id="isl-details-panel">
                <summary><span class="isl-summary-dot"></span><span>Translation &amp; playback details</span><span class="isl-summary-chevron" aria-hidden="true">⌄</span></summary>

          <!-- Status Matrix Pills -->
          <div id="isl-status-matrix">
            <div class="isl-status-pill">
              <span class="isl-status-label">CONN</span>
              <span id="st-conn" class="isl-status-value status-muted">DISCONNECTED</span>
            </div>
            <div class="isl-status-pill">
              <span class="isl-status-label">AUDIO</span>
              <span id="st-audio" class="isl-status-value status-muted">IDLE</span>
            </div>
            <div class="isl-status-pill">
              <span class="isl-status-label">ASR</span>
              <span id="st-asr" class="isl-status-value status-muted">WAITING</span>
            </div>
            <div class="isl-status-pill">
              <span class="isl-status-label">TRANS</span>
              <span id="st-trans" class="isl-status-value status-muted">IDLE</span>
            </div>
            <div class="isl-status-pill">
              <span class="isl-status-label">SIGNING</span>
              <span id="st-sign" class="isl-status-value status-muted">IDLE</span>
            </div>
          </div>

          <!-- Scrollable Middle Section: Live YouTube Telemetry, Transcripts & Queue -->
          <div id="isl-overlay-body">
            <!-- YouTube Job & Sync Card -->
            <div class="isl-card" id="youtube-result-card">
              <div class="isl-card-header">
                <span>YouTube Synchronization</span>
                <span id="youtube-job-state" class="isl-sublabel">IDLE</span>
              </div>
              <div id="youtube-job-id" class="isl-sublabel">No video job</div>
              <div id="youtube-video-title" class="isl-youtube-title">—</div>
              <div id="youtube-job-progress" class="isl-youtube-progress">Waiting for video stream.</div>
              <div id="youtube-job-error" class="isl-youtube-error hidden"></div>
              <div class="isl-transcript-row">
                <span class="isl-sublabel">Latest ASR segment (<span id="youtube-segment-count">0</span> total)</span>
                <div id="youtube-latest-segment" class="isl-transcript-box">—</div>
              </div>
              <details class="isl-youtube-details">
                <summary>Transcript summary</summary>
                <div id="youtube-transcript-summary" class="isl-transcript-box">—</div>
              </details>
              <div class="isl-youtube-result-line">
                <span class="isl-sublabel">Current ISL Gloss Sequence</span>
                <span id="youtube-translation-status" class="isl-sublabel">IDLE</span>
              </div>
              <div id="youtube-glosses" class="isl-gloss-badge">No resolved concepts</div>
              <div class="isl-youtube-result-line">
                <span class="isl-sublabel">Playable signs</span>
                <span id="youtube-playable-signs" class="isl-youtube-playable">None</span>
              </div>
              <div class="isl-youtube-unavailable">
                <div class="isl-unavailable-title">Unavailable concepts (Transparent Fallback)</div>
                <div id="youtube-unavailable-concepts">None</div>
              </div>
            </div>

            <!-- Speech Audio & Transcripts Card -->
            <div class="isl-card">
              <div class="isl-card-header">
                <span>Speech Audio &amp; Transcripts</span>
              </div>
              <div class="isl-transcript-row">
                <span class="isl-sublabel">Partial Transcript</span>
                <div id="box-transcript-partial" class="isl-transcript-box"><i>Listening...</i></div>
              </div>
              <div class="isl-transcript-row" style="margin-top: 6px;">
                <span class="isl-sublabel">Latest Final Transcript</span>
                <div id="box-transcript-final" class="isl-transcript-box">—</div>
              </div>
            </div>

            <!-- ISL Representation & Grammar Transformation Card -->
            <div class="isl-card">
              <div class="isl-card-header">
                <span>ISL-Oriented Translation</span>
                <span id="badge-trans-status" class="isl-sublabel">—</span>
              </div>
              <div>
                <span id="box-gloss-sequence" class="isl-gloss-badge">—</span>
              </div>
              <div id="box-trace" class="isl-trace-list">No transformation trace.</div>
            </div>

            <!-- Sign Queue & Active Playback Card -->
            <div class="isl-card">
              <div class="isl-card-header">
                <span>Sign Playback &amp; Queue</span>
              </div>
              <div>
                <span class="isl-sublabel">Active Sign: </span>
                <span id="pill-active-sign" class="isl-sign-tag isl-sign-active" style="display: none;">NONE</span>
                <span id="pill-review-badge" class="isl-badge-review hidden">Pending Review</span>
                <span id="txt-no-active" style="color: #8b949e; font-size: 11px;">None</span>
              </div>
              <div style="margin-top: 6px;">
                <span class="isl-sublabel">Queue:</span>
                <div id="box-queued-signs" class="isl-queue-tags">
                  <span style="color: #8b949e; font-size: 11px;">Queue is empty</span>
                </div>
              </div>

              <!-- Unavailable Concepts Box -->
              <div id="box-unavailable-container" class="isl-unavailable-box hidden">
                <div class="isl-unavailable-title">⚠️ Unavailable Signs / Evidence Pending</div>
                <div id="list-unavailable-items"></div>
              </div>
            </div>

            <!-- Deterministic Demo Mode Controls Card -->
            <div class="isl-card">
              <div class="isl-card-header">
                <span>Deterministic Demo Mode</span>
                <span id="demo-step-indicator" class="isl-sublabel">Idle</span>
              </div>
              <div style="margin-bottom: 8px;">
                <select id="select-demo-scenario" class="isl-select">
                  <option value="greeting">Greeting: "Hello good morning"</option>
                  <option value="missing_concept">Missing Concept: "I need water"</option>
                  <option value="mixed_sentence">Mixed: "I want your dopamine"</option>
                </select>
              </div>
              <div class="isl-btn-row">
                <button id="btn-demo-start" class="isl-btn isl-btn-primary">▶ Start Demo</button>
                <button id="btn-demo-step" class="isl-btn">⏭ Next Step</button>
                <button id="btn-demo-stop" class="isl-btn isl-btn-danger">⏹ Reset</button>
              </div>
            </div>

            <!-- Diagnostics & Localhost Connection Card -->
            <div class="isl-card" style="padding: 8px 12px;">
              <div style="display: flex; justify-content: space-between; align-items: center;">
                <span id="txt-runtime-msg" style="font-size: 10.5px; color: #8b949e;">Localhost runtime offline</span>
                <button id="btn-reconnect" class="isl-btn" style="padding: 3px 8px; font-size: 10px;">🔄 Probe</button>
              </div>
            </div>
            <div class="isl-aether-controls">
              <button id="btn-avatar-hello" class="isl-btn" title="Play HELLO">HELLO</button>
              <button id="btn-avatar-good" class="isl-btn" title="Queue GOOD">+GOOD</button>
              <button id="btn-avatar-morning" class="isl-btn" title="Queue MORNING">+MORN</button>
              <button id="btn-avatar-water" class="isl-btn" title="Queue WATER technical motion; linguistic review pending" aria-label="Queue WATER technical motion; linguistic review pending">+WATER</button>
              <button id="btn-avatar-pause" class="isl-btn" title="Pause/Resume">⏸</button>
              <button id="btn-avatar-reset" class="isl-btn isl-btn-danger" title="Reset Avatar">⏹</button>
            </div>
          </div>
              </details>

          <!-- Bottom-Right Anchored Section: Aether 3D Avatar Viewport -->
          <div id="isl-bottom-avatar-dock">
            <div class="isl-card-header" style="margin-bottom: 4px;">
              <span style="display: flex; align-items: center; gap: 6px;">
                <span class="isl-pulse-dot"></span>
                <span>LIVE SIGN AVATAR</span>
              </span>
              <span class="isl-avatar-header-actions">
                <span id="aether-status-badge" class="isl-version-tag">READY WHEN CONNECTED</span>
              </span>
            </div>
            <div id="isl-aether-container">
              <div class="isl-aether-hud-tag"><span class="isl-pulse-dot"></span> AETHER 3D</div>
              <button id="btn-avatar-grip" class="isl-avatar-grip" type="button" title="Drag to move Aether" aria-label="Drag to move Aether">⠿</button>
              <iframe id="isl-aether-iframe" src="about:blank" class="hidden"></iframe>
              <div id="isl-aether-fallback">
                <div class="isl-fallback-orbit" aria-hidden="true"><span>🤟</span></div>
                <strong>Aether is getting ready</strong>
                <span>Connect the local viewer to see the signing avatar.</span>
              </div>
            </div>

            <!-- Unavailable Subtitle Fallback (Phase H13) -->
            <div id="isl-unavailable-subtitle" class="isl-unavailable-subtitle hidden">
              <div class="isl-unavailable-sub-header">ISL translation not available in this translator</div>
              <div id="isl-unavailable-sub-text" class="isl-unavailable-sub-text"></div>
            </div>

            <div class="isl-avatar-toolbar">
              <div class="isl-view-and-size-row">
                <div class="isl-view-switch" role="group" aria-label="Avatar framing">
                  <button id="btn-avatar-half" class="isl-view-button active" type="button" data-view-mode="half" aria-pressed="true">Half body</button>
                  <button id="btn-avatar-full" class="isl-view-button" type="button" data-view-mode="full" aria-pressed="false">Full body</button>
                </div>
                <div class="isl-size-switch" role="group" aria-label="Avatar scale">
                  <button id="btn-size-compact" class="isl-size-button" type="button" data-size="compact" aria-pressed="false" title="Compact size (240px)">S</button>
                  <button id="btn-size-standard" class="isl-size-button active" type="button" data-size="standard" aria-pressed="true" title="Standard size (320px)">M</button>
                  <button id="btn-size-large" class="isl-size-button" type="button" data-size="large" aria-pressed="false" title="Large size (400px)">L</button>
                </div>
              </div>
              <button id="btn-avatar-drag" class="isl-drag-toggle" type="button" aria-pressed="false" title="Float the avatar and enable drag mode">
                <span class="isl-drag-icon" aria-hidden="true">↗</span>
                <span class="isl-drag-copy"><strong>Move avatar</strong><small>Drag mode off</small></span>
                <span class="isl-drag-switch" aria-hidden="true"><span></span></span>
              </button>
              <button id="btn-avatar-dock" class="isl-dock-avatar hidden" type="button">Return avatar to panel</button>
            </div>

          </div>
              <div id="isl-avatar-detached-note" class="hidden">Avatar is floating over the video. Use Move avatar to reposition it.</div>
            </main>
          </div>
        </div>
      `;

      // Load CSS link into shadow root
      const link = document.createElement('link');
      link.rel = 'stylesheet';
      link.href = (typeof chrome !== 'undefined' && chrome.runtime?.getURL)
        ? chrome.runtime.getURL('content/overlay.css')
        : 'overlay.css';

      this.shadowRoot.appendChild(link);
      this.shadowRoot.appendChild(container);
      link.addEventListener('load', () => this.handleAvatarViewportChange());

      // Cache DOM references
      this.elements = {
        launcher: this.shadowRoot.getElementById('isl-launcher-badge'),
        sidebarToggle: this.shadowRoot.getElementById('isl-sidebar-toggle-handle'),
        container: this.shadowRoot.getElementById('isl-overlay-container'),
        floatingSurface: this.shadowRoot.getElementById('isl-floating-avatar-surface'),
        appYoutube: this.shadowRoot.getElementById('btn-app-youtube'),
        detailsPanel: this.shadowRoot.getElementById('isl-details-panel'),
        detailsToggle: this.shadowRoot.getElementById('btn-details-toggle'),
        detachedNote: this.shadowRoot.getElementById('isl-avatar-detached-note'),
        avatarGrip: this.shadowRoot.getElementById('btn-avatar-grip'),
        body: this.shadowRoot.getElementById('isl-overlay-body'),
        header: this.shadowRoot.getElementById('isl-header-bar'),
        modeBadge: this.shadowRoot.getElementById('isl-mode-badge'),
        btnMinimize: this.shadowRoot.getElementById('btn-minimize'),
        btnClose: this.shadowRoot.getElementById('btn-close'),

        // Status pills
        stConn: this.shadowRoot.getElementById('st-conn'),
        stAudio: this.shadowRoot.getElementById('st-audio'),
        stAsr: this.shadowRoot.getElementById('st-asr'),
        stTrans: this.shadowRoot.getElementById('st-trans'),
        stSign: this.shadowRoot.getElementById('st-sign'),

        // Aether
        aetherContainer: this.shadowRoot.getElementById('isl-aether-container'),
        aetherIframe: this.shadowRoot.getElementById('isl-aether-iframe'),
        aetherFallback: this.shadowRoot.getElementById('isl-aether-fallback'),
        unavailableSubtitle: this.shadowRoot.getElementById('isl-unavailable-subtitle'),
        unavailableSubText: this.shadowRoot.getElementById('isl-unavailable-sub-text'),
        btnAvatarHello: this.shadowRoot.getElementById('btn-avatar-hello'),
        btnAvatarGood: this.shadowRoot.getElementById('btn-avatar-good'),
        btnAvatarMorning: this.shadowRoot.getElementById('btn-avatar-morning'),
        btnAvatarWater: this.shadowRoot.getElementById('btn-avatar-water'),
        btnAvatarPause: this.shadowRoot.getElementById('btn-avatar-pause'),
        btnAvatarReset: this.shadowRoot.getElementById('btn-avatar-reset'),
        btnAvatarHalf: this.shadowRoot.getElementById('btn-avatar-half'),
        btnAvatarFull: this.shadowRoot.getElementById('btn-avatar-full'),
        btnSizeCompact: this.shadowRoot.getElementById('btn-size-compact'),
        btnSizeStandard: this.shadowRoot.getElementById('btn-size-standard'),
        btnSizeLarge: this.shadowRoot.getElementById('btn-size-large'),
        btnAvatarDrag: this.shadowRoot.getElementById('btn-avatar-drag'),
        btnAvatarDock: this.shadowRoot.getElementById('btn-avatar-dock'),

        // H7 YouTube job output
        youtubeJobState: this.shadowRoot.getElementById('youtube-job-state'),
        youtubeJobId: this.shadowRoot.getElementById('youtube-job-id'),
        youtubeVideoTitle: this.shadowRoot.getElementById('youtube-video-title'),
        youtubeJobProgress: this.shadowRoot.getElementById('youtube-job-progress'),
        youtubeJobError: this.shadowRoot.getElementById('youtube-job-error'),
        youtubeSegmentCount: this.shadowRoot.getElementById('youtube-segment-count'),
        youtubeLatestSegment: this.shadowRoot.getElementById('youtube-latest-segment'),
        youtubeTranscriptSummary: this.shadowRoot.getElementById('youtube-transcript-summary'),
        youtubeTranslationStatus: this.shadowRoot.getElementById('youtube-translation-status'),
        youtubeGlosses: this.shadowRoot.getElementById('youtube-glosses'),
        youtubePlayableSigns: this.shadowRoot.getElementById('youtube-playable-signs'),
        youtubeUnavailableConcepts: this.shadowRoot.getElementById('youtube-unavailable-concepts'),

        // Transcripts
        boxPartial: this.shadowRoot.getElementById('box-transcript-partial'),
        boxFinal: this.shadowRoot.getElementById('box-transcript-final'),

        // Translation
        badgeTransStatus: this.shadowRoot.getElementById('badge-trans-status'),
        boxGloss: this.shadowRoot.getElementById('box-gloss-sequence'),
        boxTrace: this.shadowRoot.getElementById('box-trace'),

        // Signing
        pillActiveSign: this.shadowRoot.getElementById('pill-active-sign'),
        pillReviewBadge: this.shadowRoot.getElementById('pill-review-badge'),
        txtNoActive: this.shadowRoot.getElementById('txt-no-active'),
        boxQueuedSigns: this.shadowRoot.getElementById('box-queued-signs'),
        boxUnavailable: this.shadowRoot.getElementById('box-unavailable-container'),
        listUnavailable: this.shadowRoot.getElementById('list-unavailable-items'),

        // Demo
        selectScenario: this.shadowRoot.getElementById('select-demo-scenario'),
        demoIndicator: this.shadowRoot.getElementById('demo-step-indicator'),
        btnDemoStart: this.shadowRoot.getElementById('btn-demo-start'),
        btnDemoStep: this.shadowRoot.getElementById('btn-demo-step'),
        btnDemoStop: this.shadowRoot.getElementById('btn-demo-stop'),

        // Runtime
        txtRuntimeMsg: this.shadowRoot.getElementById('txt-runtime-msg'),
        btnReconnect: this.shadowRoot.getElementById('btn-reconnect')
      };

      this.avatarViewportPlaceholder = document.createElement('div');
      this.avatarViewportPlaceholder.id = 'isl-aether-placeholder';
      this.avatarViewportPlaceholder.className = 'isl-aether-placeholder';
      this.avatarViewportPlaceholder.setAttribute('aria-hidden', 'true');
      this.elements.aetherContainer.parentNode.replaceChild(
        this.avatarViewportPlaceholder,
        this.elements.aetherContainer
      );
      // Keep the live iframe and its fallback subtitle pill in one DOM position so floating and docking never reload playback.
      this.elements.floatingSurface.appendChild(this.elements.aetherContainer);
      if (this.elements.unavailableSubtitle) {
        this.elements.floatingSurface.appendChild(this.elements.unavailableSubtitle);
      }
    }

    setupDragging() {
      const grip = this.elements.avatarGrip;
      const surface = this.elements.floatingSurface;

      const onPointerDown = (e) => {
        if (e.button !== 0 || !e.isPrimary
          || !this.isAvatarFloating || !this.isAvatarDragEnabled) return;

        this.isDragging = true;
        this.avatarDragPointerId = e.pointerId;
        const rect = surface.getBoundingClientRect();
        this.dragOffset.x = e.clientX - rect.left;
        this.dragOffset.y = e.clientY - rect.top;
        e.preventDefault();
        if (typeof grip.setPointerCapture === 'function') {
          grip.setPointerCapture(e.pointerId);
        }
      };

      const onPointerMove = (e) => {
        if (!this.isDragging || e.pointerId !== this.avatarDragPointerId
          || !this.isAvatarFloating || !this.isAvatarDragEnabled) return;
        const maxLeft = this.getMaxFloatingLeft(surface.offsetWidth);
        const maxTop = Math.max(8, window.innerHeight - surface.offsetHeight - 8);
        const left = Math.max(8, Math.min(maxLeft, e.clientX - this.dragOffset.x));
        const top = Math.max(8, Math.min(maxTop, e.clientY - this.dragOffset.y));
        surface.style.right = 'auto';
        surface.style.bottom = 'auto';
        surface.style.left = `${left}px`;
        surface.style.top = `${top}px`;
        this.avatarPositionUserSet = true;
      };

      const onPointerUp = (e) => {
        if (e.pointerId !== undefined && e.pointerId !== this.avatarDragPointerId) return;
        this.isDragging = false;
        this.avatarDragPointerId = null;
      };

      grip.addEventListener('pointerdown', onPointerDown);
      grip.addEventListener('pointermove', onPointerMove);
      grip.addEventListener('pointerup', onPointerUp);
      grip.addEventListener('pointercancel', onPointerUp);
      grip.addEventListener('lostpointercapture', onPointerUp);
    }

    bindEvents() {
      const {
        btnMinimize, btnClose, launcher, sidebarToggle, appYoutube, detailsPanel, detailsToggle,
        btnDemoStart, btnDemoStep, btnDemoStop, selectScenario,
        btnReconnect,
        btnAvatarHello, btnAvatarGood, btnAvatarMorning, btnAvatarWater, btnAvatarPause, btnAvatarReset,
        btnAvatarHalf, btnAvatarFull, btnAvatarDrag, btnAvatarDock,
        btnSizeCompact, btnSizeStandard, btnSizeLarge
      } = this.elements;

      btnMinimize.addEventListener('click', () => this.toggleMinimize());
      btnClose.addEventListener('click', () => this.hide());
      launcher.addEventListener('click', () => this.show());
      if (sidebarToggle) {
        sidebarToggle.addEventListener('click', () => this.show());
      }
      appYoutube.addEventListener('click', () => {
        detailsPanel.open = false;
        this.updateDetailsButton();
      });
      detailsToggle.addEventListener('click', () => {
        detailsPanel.open = !detailsPanel.open;
        this.updateDetailsButton();
      });
      detailsPanel.addEventListener('toggle', () => this.updateDetailsButton());

      btnDemoStart.addEventListener('click', () => {
        const scenario = selectScenario.value;
        this.dispatch('DEMO_START', { scenario });
      });

      btnDemoStep.addEventListener('click', () => {
        this.dispatch('DEMO_STEP', {});
      });

      btnDemoStop.addEventListener('click', () => {
        this.dispatch('DEMO_STOP', {});
      });

      selectScenario.addEventListener('change', () => {
        this.dispatch('DEMO_SET_SCENARIO', { scenario: selectScenario.value });
      });

      btnReconnect.addEventListener('click', () => {
        this.stopAutoReconnect();
        this.dispatch('CONNECT_RUNTIME', {});
      });

      // Aether Bridge Commands (Task H6-E)
      btnAvatarHello.addEventListener('click', () => {
        this.dispatch('AETHER_COMMAND', { command: 'PLAY_SIGN', signId: 'hello' });
      });
      btnAvatarGood.addEventListener('click', () => {
        this.dispatch('AETHER_COMMAND', { command: 'QUEUE_SIGN', signId: 'good' });
      });
      btnAvatarMorning.addEventListener('click', () => {
        this.dispatch('AETHER_COMMAND', { command: 'QUEUE_SIGN', signId: 'morning' });
      });
      btnAvatarWater.addEventListener('click', () => {
        this.dispatch('AETHER_COMMAND', { command: 'QUEUE_SIGN', signId: 'water' });
      });
      btnAvatarPause.addEventListener('click', () => {
        this.dispatch('AETHER_COMMAND', { command: 'PAUSE' });
      });
      btnAvatarReset.addEventListener('click', () => {
        this.dispatch('AETHER_COMMAND', { command: 'RESET_AVATAR' });
      });
      btnAvatarHalf.addEventListener('click', () => this.setAvatarView('half'));
      btnAvatarFull.addEventListener('click', () => this.setAvatarView('full'));
      if (btnSizeCompact) btnSizeCompact.addEventListener('click', () => this.setAvatarSize('compact'));
      if (btnSizeStandard) btnSizeStandard.addEventListener('click', () => this.setAvatarSize('standard'));
      if (btnSizeLarge) btnSizeLarge.addEventListener('click', () => this.setAvatarSize('large'));
      btnAvatarDrag.addEventListener('click', () => this.toggleAvatarDrag());
      btnAvatarDock.addEventListener('click', () => this.setAvatarFloating(false));
    }

    updateDetailsButton() {
      const open = this.elements.detailsPanel.open;
      this.elements.detailsToggle.setAttribute('aria-expanded', String(open));
      this.elements.detailsToggle.classList.toggle('active', open);
      this.syncAvatarSurface();
    }

    setAvatarView(mode) {
      if (mode !== 'half' && mode !== 'full') {
        throw new TypeError(`Unsupported avatar view: ${mode}`);
      }
      this.avatarViewMode = mode;
      for (const button of [this.elements.btnAvatarHalf, this.elements.btnAvatarFull]) {
        const selected = button.dataset.viewMode === mode;
        button.classList.toggle('active', selected);
        button.setAttribute('aria-pressed', String(selected));
      }
      this.dispatch('AETHER_COMMAND', {
        command: 'SET_AVATAR_VIEW',
        viewMode: mode
      });
    }

    setAvatarSize(size) {
      if (size !== 'compact' && size !== 'standard' && size !== 'large') {
        throw new TypeError(`Unsupported avatar size: ${size}`);
      }
      this.avatarSizePreset = size;
      const buttons = [
        { btn: this.elements.btnSizeCompact, size: 'compact' },
        { btn: this.elements.btnSizeStandard, size: 'standard' },
        { btn: this.elements.btnSizeLarge, size: 'large' }
      ];
      for (const { btn, size: btnSize } of buttons) {
        if (!btn) continue;
        const selected = btnSize === size;
        btn.classList.toggle('active', selected);
        btn.setAttribute('aria-pressed', String(selected));
      }
      const surface = this.elements.floatingSurface;
      if (surface) {
        surface.classList.remove('size-compact', 'size-standard', 'size-large');
        surface.classList.add(`size-${size}`);
      }
      this.handleAvatarViewportChange();
    }

    toggleAvatarDrag() {
      this.isAvatarDragEnabled = !this.isAvatarDragEnabled;
      if (this.isAvatarDragEnabled && !this.isAvatarFloating) this.setAvatarFloating(true);
      const button = this.elements.btnAvatarDrag;
      button.setAttribute('aria-pressed', String(this.isAvatarDragEnabled));
      button.classList.toggle('active', this.isAvatarDragEnabled);
      button.querySelector('small').textContent = this.isAvatarDragEnabled
        ? 'Drag mode on'
        : 'Drag mode off';
      this.elements.floatingSurface.classList.toggle('drag-enabled', this.isAvatarDragEnabled);
      if (!this.isAvatarDragEnabled) {
        this.isDragging = false;
        this.avatarDragPointerId = null;
      }
      this.syncAvatarSurface();
    }

    setAvatarFloating(floating) {
      if (this.isAvatarFloating === floating) return;
      this.isAvatarFloating = floating;
      this.elements.container.classList.toggle('avatar-detached', floating);
      if (floating) {
        this.floatingPositionInitialized = false;
        this.avatarPositionUserSet = false;
        this.elements.floatingSurface.style.cssText = '';
        this.elements.detachedNote.classList.remove('hidden');
        this.elements.btnAvatarDock.classList.remove('hidden');
        this.elements.floatingSurface.classList.add('avatar-floating', `size-${this.avatarSizePreset}`);
        this.elements.floatingSurface.classList.remove('avatar-docked', 'hidden');
      } else {
        this.floatingPositionInitialized = false;
        this.elements.detachedNote.classList.add('hidden');
        this.elements.btnAvatarDock.classList.add('hidden');
        this.isAvatarDragEnabled = false;
        this.elements.btnAvatarDrag.setAttribute('aria-pressed', 'false');
        this.elements.btnAvatarDrag.classList.remove('active');
        this.elements.btnAvatarDrag.querySelector('small').textContent = 'Drag mode off';
        this.elements.floatingSurface.classList.remove('avatar-floating', 'drag-enabled', 'size-compact', 'size-standard', 'size-large');
        this.elements.floatingSurface.classList.add('avatar-docked');
        this.elements.floatingSurface.style.cssText = '';
        this.isDragging = false;
        this.avatarDragPointerId = null;
      }
      this.syncAvatarSurface();
    }

    handleAvatarViewportChange() {
      if (this.isAvatarFloating && !this.avatarPositionUserSet) {
        this.floatingPositionInitialized = false;
      }
      this.syncAvatarSurface({ clampFloating: true });
    }

    getMaxFloatingLeft(avatarWidth) {
      return Math.max(8, window.innerWidth - avatarWidth - 8);
    }

    syncAvatarSurface({ clampFloating = false } = {}) {
      const { floatingSurface, container } = this.elements;
      if (!floatingSurface || !this.avatarViewportPlaceholder) return;

      if (this.isAvatarFloating) {
        floatingSurface.classList.remove('hidden', 'avatar-docked');
        floatingSurface.classList.add('avatar-floating');
        if (this.isDragging) return;

        const rect = floatingSurface.getBoundingClientRect();
        const maxLeft = this.getMaxFloatingLeft(rect.width);
        const maxTop = Math.max(8, window.innerHeight - rect.height - 8);
        if (!this.floatingPositionInitialized) {
          const panelWidth = this.isVisible && this.isSidebarMode && !this.isCollapsed
            ? container.getBoundingClientRect().width
            : 0;
          const desiredRight = panelWidth + 24;
          const right = desiredRight + rect.width + 8 <= window.innerWidth ? desiredRight : 24;
          const left = Math.max(8, Math.min(maxLeft, window.innerWidth - right - rect.width));
          const top = Math.max(8, Math.min(maxTop, window.innerHeight - 26 - rect.height));
          floatingSurface.style.left = `${left}px`;
          floatingSurface.style.top = `${top}px`;
          floatingSurface.style.right = 'auto';
          floatingSurface.style.bottom = 'auto';
          this.floatingPositionInitialized = true;
        } else if (clampFloating) {
          const left = Math.max(8, Math.min(maxLeft, rect.left));
          const top = Math.max(8, Math.min(maxTop, rect.top));
          floatingSurface.style.left = `${left}px`;
          floatingSurface.style.top = `${top}px`;
        }
        return;
      }

      floatingSurface.classList.remove('avatar-floating');
      floatingSurface.classList.add('avatar-docked');
      const dockVisible = this.isVisible && this.isSidebarMode && !this.isCollapsed;
      floatingSurface.classList.toggle('hidden', !dockVisible);
      if (!dockVisible) return;

      const rect = this.avatarViewportPlaceholder.getBoundingClientRect();
      if (rect.width <= 0 || rect.height <= 0) return;
      floatingSurface.style.left = `${rect.left}px`;
      floatingSurface.style.top = `${rect.top}px`;
      floatingSurface.style.right = 'auto';
      floatingSurface.style.bottom = 'auto';
      floatingSurface.style.width = `${rect.width}px`;
      floatingSurface.style.height = `${rect.height}px`;
    }

    dispatch(type, payload = {}) {
      if (typeof this.onAction === 'function') {
        this.onAction(type, payload);
      }
    }

    setUnavailableFallback(originalWord = null, durationMs = 2500) {
      if (!this.elements.unavailableSubtitle || !this.elements.unavailableSubText) return;
      if (this.fallbackTimer) {
        clearTimeout(this.fallbackTimer);
        this.fallbackTimer = null;
      }
      if (originalWord) {
        this.elements.unavailableSubText.textContent = String(originalWord);
        this.elements.unavailableSubtitle.classList.remove('hidden');
        if (durationMs > 0) {
          this.fallbackTimer = setTimeout(() => {
            if (this.elements.unavailableSubtitle) {
              this.elements.unavailableSubtitle.classList.add('hidden');
              this.elements.unavailableSubText.textContent = '';
            }
            this.fallbackTimer = null;
          }, durationMs);
        }
      } else {
        this.elements.unavailableSubtitle.classList.add('hidden');
        this.elements.unavailableSubText.textContent = '';
      }
    }

    toggleMinimize() {
      this.isMinimized = !this.isMinimized;
      if (this.isSidebarMode) {
        this.isCollapsed = this.isMinimized;
        this.elements.container.classList.toggle('sidebar-collapsed', this.isCollapsed);
        if (this.elements.sidebarToggle) {
          this.elements.sidebarToggle.classList.toggle('hidden', !this.isCollapsed);
        }
        this.elements.btnMinimize.textContent = this.isCollapsed ? '›' : '‹';
        this.elements.btnMinimize.setAttribute(
          'aria-label',
          this.isCollapsed ? 'Expand sidebar' : 'Collapse sidebar'
        );
        this.elements.btnMinimize.title = this.isCollapsed ? 'Expand sidebar' : 'Collapse sidebar';
      } else {
        this.elements.btnMinimize.textContent = this.isMinimized ? '□' : '─';
      }
      this.syncAvatarSurface();
    }

    expandSidebar() {
      this.isCollapsed = false;
      this.isMinimized = false;
      this.elements.container.classList.remove('sidebar-collapsed');
      if (this.elements.sidebarToggle) {
        this.elements.sidebarToggle.classList.add('hidden');
      }
      this.elements.btnMinimize.textContent = '‹';
      this.elements.btnMinimize.setAttribute('aria-label', 'Collapse sidebar');
      this.elements.btnMinimize.title = 'Collapse sidebar';
      this.syncAvatarSurface();
    }

    toggleLayoutMode() {
      this.isSidebarMode = !this.isSidebarMode;
      const c = this.elements.container;
      if (this.isSidebarMode) {
        c.classList.remove('floating-mode');
        c.classList.add('sidebar-mode');
        c.style.left = '';
        c.style.top = '';
        c.style.right = '';
        c.style.bottom = '';
        if (this.elements.modeBadge) this.elements.modeBadge.textContent = 'Right Sidebar';
        if (this.elements.btnLayoutMode) this.elements.btnLayoutMode.textContent = '◫';
        if (this.elements.sidebarToggle) {
          this.elements.sidebarToggle.classList.toggle('hidden', !this.isCollapsed);
        }
        this.elements.launcher.classList.add('hidden');
      } else {
        c.classList.remove('sidebar-mode');
        c.classList.add('floating-mode');
        c.classList.remove('sidebar-collapsed');
        if (this.elements.modeBadge) this.elements.modeBadge.textContent = 'Floating Window';
        if (this.elements.btnLayoutMode) this.elements.btnLayoutMode.textContent = '▥';
        if (this.elements.sidebarToggle) this.elements.sidebarToggle.classList.add('hidden');
      }
      this.syncAvatarSurface();
    }

    show() {
      this.isVisible = true;
      this.elements.container.classList.remove('hidden');
      this.elements.launcher.classList.add('hidden');
      this.elements.sidebarToggle?.classList.add('hidden');
      if (this.isSidebarMode && this.isCollapsed) {
        this.expandSidebar();
      }
      this.syncAvatarSurface();
    }

    hide() {
      this.isVisible = false;
      this.elements.container.classList.add('hidden');
      if (this.isSidebarMode) {
        if (this.elements.sidebarToggle) {
          this.elements.sidebarToggle.classList.remove('hidden');
        }
      } else {
        this.elements.launcher.classList.remove('hidden');
      }
      this.syncAvatarSurface();
    }

    /**
     * Update all UI elements safely according to the state model
     */
    update(state) {
      if (!state) return;
      const el = this.elements;

      // 1. Connection Matrix (Task H6-C)
      this.setStatusPill(el.stConn, state.connection);
      this.setStatusPill(el.stAudio, state.audio);
      this.setStatusPill(el.stAsr, state.asr);
      this.setStatusPill(el.stTrans, state.translation);
      this.setStatusPill(el.stSign, state.signing);

      // 2. Transcripts
      const transcript = state.transcript || {};
      el.boxPartial.textContent = transcript.partial || '—';
      el.boxFinal.textContent = transcript.final || '—';

      const youtube = state.youtube || {};
      el.youtubeJobState.textContent = youtube.state || 'IDLE';
      el.youtubeJobId.textContent = youtube.jobId ? `Job ${youtube.jobId}` : 'No video job';
      el.youtubeVideoTitle.textContent = youtube.title || '—';
      el.youtubeSegmentCount.textContent = String(youtube.segmentCount || 0);
      el.youtubeLatestSegment.textContent = youtube.latestSegment || '—';
      el.youtubeTranscriptSummary.textContent = youtube.transcriptSummary || '—';
      el.youtubeTranslationStatus.textContent = youtube.translationStatus || 'IDLE';
      const statusCounts = Object.entries(youtube.translationStatusCounts || {})
        .map(([status, count]) => `${status} ${count}`).join(', ');
      el.youtubeGlosses.textContent = youtube.glosses?.length
        ? `${youtube.glosses.join(' ')}${statusCounts ? ` · ${statusCounts}` : ''}`
        : 'No resolved concepts';
      el.youtubePlayableSigns.textContent = youtube.playableSigns?.length
        ? [...new Set(youtube.playableSigns)].map(sign => sign.toUpperCase()).join(', ')
        : 'None';
      el.youtubeUnavailableConcepts.textContent = youtube.unavailableConcepts?.length
        ? [...new Set(youtube.unavailableConcepts.map(item => `${String(item.word).toUpperCase()} — ${item.reason || 'motion unavailable'}`))].join('; ')
        : 'None';
      if (youtube.wordCoverage) {
        const coverage = youtube.wordCoverage;
        const summary = `Cue coverage (occurrences): ${coverage.playableSignOccurrences || 0} playable signs; `
          + `${coverage.unavailableConceptOccurrences || 0} unavailable signs; `
          + `${coverage.unknownTermOccurrences || 0} words not in catalog; `
          + `${coverage.sourceTextMismatches || 0} source mismatches `
          + `(${coverage.sourceMismatchFallbackOccurrences || 0} transcript words withheld). `;
        el.youtubeUnavailableConcepts.textContent = `${summary}${el.youtubeUnavailableConcepts.textContent}`;
      }
      const progress = Number(youtube.progress);
      el.youtubeJobProgress.textContent = youtube.state === 'READY'
        ? `Complete${youtube.duration ? ` · video ${Number(youtube.duration).toFixed(0)} s` : ''}${youtube.audioDuration ? ` · audio ${Number(youtube.audioDuration).toFixed(1)} s` : ''}`
        : youtube.state === 'ERROR' ? 'Processing failed.'
          : youtube.state && youtube.state !== 'IDLE'
            ? `${youtube.state} · ${Number.isFinite(progress) ? `${Math.round(progress * 100)}%` : 'progress unavailable'}`
            : 'Waiting for a YouTube job.';
      el.youtubeJobError.textContent = youtube.error || '';
      el.youtubeJobError.classList.toggle('hidden', !youtube.error);

      // 3. ISL Representation
      const rep = state.representation || {};
      el.badgeTransStatus.textContent = rep.status || '—';
      el.boxGloss.textContent = rep.glossSequence?.length
        ? rep.glossSequence.join(' ')
        : '—';
      el.boxTrace.textContent = rep.trace?.length
        ? rep.trace.join(' -> ')
        : 'No transformation trace.';

      // 4. Signing & Queue State
      const queue = state.signingQueue || {};
      const activeSignName = queue.currentSign || queue.activeSign;
      if (activeSignName) {
        el.pillActiveSign.textContent = activeSignName.toUpperCase();
        el.pillActiveSign.style.display = 'inline-block';
        el.txtNoActive.style.display = 'none';

        if (el.pillReviewBadge) {
          const isVerified = queue.currentSignVerified === true || queue.isUnderReview === false;
          el.pillReviewBadge.textContent = isVerified ? 'Verified' : 'Pending Review';
          el.pillReviewBadge.className = isVerified ? 'isl-badge-review verified' : 'isl-badge-review';
          el.pillReviewBadge.classList.remove('hidden');
        }
      } else {
        el.pillActiveSign.style.display = 'none';
        el.txtNoActive.style.display = 'inline';
        if (el.pillReviewBadge) {
          el.pillReviewBadge.classList.add('hidden');
        }
      }

      const queueList = queue.queuedSigns || queue.queue;
      if (queueList && queueList.length > 0) {
        el.boxQueuedSigns.innerHTML = '';
        queueList.forEach((item) => {
          const tag = document.createElement('span');
          tag.className = 'isl-sign-tag isl-sign-queued';
          tag.textContent = typeof item === 'string' ? item.toUpperCase() : (item.id || item.word || '').toUpperCase();
          el.boxQueuedSigns.appendChild(tag);
        });
      } else {
        el.boxQueuedSigns.innerHTML = '<span style="color: #8b949e; font-size: 11px;">Queue is empty</span>';
      }

      // 5. Unavailable Concepts (Evidence / Motion Pending)
      if (queue.unavailableConcepts && queue.unavailableConcepts.length > 0) {
        el.boxUnavailable.classList.remove('hidden');
        el.listUnavailable.innerHTML = queue.unavailableConcepts
          .map(item => `<div class="isl-unavailable-item">✕ <b>${(typeof item === 'string' ? item : item.word || '').toUpperCase()}:</b> ${typeof item === 'string' ? 'Pending evidence' : (item.reason || 'Pending evidence')}</div>`)
          .join('');
      } else {
        el.boxUnavailable.classList.add('hidden');
        el.listUnavailable.innerHTML = '';
      }

      // 5b. Unavailable Subtitle Fallback directly below Aether (Phase H13)
      const fallbackWord = queue.unavailableFallback || state.youtube?.unavailableFallback;
      if (fallbackWord) {
        this.setUnavailableFallback(fallbackWord);
      } else if (activeSignName && this.fallbackTimer) {
        this.setUnavailableFallback(null);
      }

      // 6. Demo Indicator
      const demo = state.demo || {};
      if (demo.active) {
        el.demoIndicator.textContent = `Step ${demo.step} / ${demo.totalSteps}`;
        el.demoIndicator.style.color = '#58a6ff';
        if (el.selectScenario && el.selectScenario.value !== demo.scenario && demo.scenario) {
          el.selectScenario.value = demo.scenario;
        }
      } else {
        el.demoIndicator.textContent = demo.step || 'Idle';
        el.demoIndicator.style.color = '#8b949e';
      }

      // 7. Aether Bridge Runtime Status
      if (state.runtimeAvailable || state.runtimeActive) {
        this.stopAutoReconnect();
        el.txtRuntimeMsg.textContent = state.runtimeEndpoint ? `Connected: ${state.runtimeEndpoint}` : 'Localhost runtime online';
        el.txtRuntimeMsg.style.color = '#3fb950';

        const targetSrc = state.avatarViewerUrl || `${state.runtimeEndpoint || 'http://localhost:8000'}/tools/avatar_viewer/index.html?embed=1`;
        if (el.aetherIframe.src !== targetSrc) {
          el.aetherIframe.src = targetSrc;
          el.aetherIframe.classList.remove('hidden');
          el.aetherFallback.classList.add('hidden');
        }
      } else {
        this.scheduleAutoReconnect();
        el.txtRuntimeMsg.textContent = state.runtimeError || 'Localhost runtime offline';
        el.txtRuntimeMsg.style.color = '#8b949e';
        el.aetherIframe.classList.add('hidden');
        el.aetherFallback.classList.remove('hidden');
      }

      // 8. Visibility
      if (state.overlayVisible === false && this.isVisible) {
        this.hide();
      } else if (state.overlayVisible === true && !this.isVisible) {
        this.show();
      }
      this.syncAvatarSurface();
    }

    setStatusPill(element, value) {
      if (!element) return;
      element.textContent = value || '—';
      element.className = 'isl-status-value';

      const upper = String(value || '').toUpperCase();
      if (['CONNECTED', 'PLAYING', 'SUPPORTED', 'FINAL'].includes(upper)) {
        element.classList.add('status-green');
      } else if (['CONNECTING', 'LISTENING', 'PARTIAL', 'TRANSLATING'].includes(upper)) {
        element.classList.add('status-blue');
      } else if (['HEURISTIC', 'QUEUED', 'PAUSED'].includes(upper)) {
        element.classList.add('status-amber');
      } else if (['ERROR', 'UNAVAILABLE', 'UNCERTAIN'].includes(upper)) {
        element.classList.add('status-red');
      } else {
        element.classList.add('status-muted');
      }
    }

    scheduleAutoReconnect() {
      if (!this.autoReconnectEnabled || this.autoReconnectTimer) return;
      this.autoReconnectTimer = setTimeout(() => {
        this.autoReconnectTimer = null;
        this.autoReconnectDelayMs = Math.min(this.autoReconnectMaxDelayMs, Math.round(this.autoReconnectDelayMs * 1.5));
        this.dispatch('CONNECT_RUNTIME', {});
      }, this.autoReconnectDelayMs);
    }

    stopAutoReconnect() {
      if (this.autoReconnectTimer) {
        clearTimeout(this.autoReconnectTimer);
        this.autoReconnectTimer = null;
      }
      this.autoReconnectDelayMs = 2000;
    }

    destroy() {
      this.isVisible = false;
      this.stopAutoReconnect();
      if (this.resizeHandler) this.targetWindow?.removeEventListener('resize', this.resizeHandler);
      if (this.fallbackTimer) clearTimeout(this.fallbackTimer);
      if (this.hostElement && this.hostElement.parentNode) {
        this.hostElement.parentNode.removeChild(this.hostElement);
      }
      this.hostElement = null;
      this.shadowRoot = null;
      this.elements = {};
    }
  }

  return {
    ISLOverlayUI
  };
});
