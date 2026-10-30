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
      this.dragOffset = { x: 0, y: 0 };
      this.fallbackTimer = null;
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
      this.updateHostPageLayout();
    }

    buildDOM() {
      const container = document.createElement('div');
      container.innerHTML = `
        <!-- Floating Launcher Badge (for floating mode) -->
        <div id="isl-launcher-badge" class="hidden" title="Click to open ISL Accessibility Translator">
          <span>🤟 ISL Translator</span>
        </div>

        <!-- Right Edge Dock Toggle Handle (for collapsed sidebar) -->
        <div id="isl-sidebar-toggle-handle" class="hidden" title="Open ISL Accessibility Sidebar">
          <span class="isl-handle-icon">🤟</span>
          <span class="isl-handle-text">ISL BAR</span>
        </div>

        <!-- Main Container: Defaults to stunning right sidebar dock -->
        <div id="isl-overlay-container" class="sidebar-mode">
          <!-- Header Bar -->
          <div id="isl-header-bar">
            <div class="isl-title-group">
              <span class="isl-app-title">🤟 ISL Translator</span>
              <span id="isl-mode-badge" class="isl-version-tag">Right Sidebar</span>
            </div>
            <div class="isl-header-actions">
              <button id="btn-layout-mode" class="isl-icon-btn" title="Toggle Right Sidebar / Floating Window">◫</button>
              <button id="btn-minimize" class="isl-icon-btn" title="Collapse Sidebar">─</button>
              <button id="btn-close" class="isl-icon-btn" title="Close">✕</button>
            </div>
          </div>

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
          </div>

          <!-- Bottom-Right Anchored Section: Aether 3D Avatar Viewport -->
          <div id="isl-bottom-avatar-dock">
            <div class="isl-card-header" style="margin-bottom: 4px;">
              <span style="display: flex; align-items: center; gap: 6px;">
                <span class="isl-pulse-dot"></span>
                <span>Aether 3D Avatar</span>
              </span>
              <span id="aether-status-badge" class="isl-version-tag">Bottom-Right View</span>
            </div>
            <div id="isl-aether-container">
              <div class="isl-aether-hud-tag"><span class="isl-pulse-dot"></span> AETHER 3D • 60 FPS</div>
              <iframe id="isl-aether-iframe" src="about:blank" class="hidden"></iframe>
              <div id="isl-aether-fallback">
                <div class="isl-fallback-badge">Aether Localhost Dev Mode</div>
                <p style="font-size: 11px; margin-top: 4px;">Avatar loads via local server</p>
                <p style="font-size: 10px; color: #58a6ff;">http://localhost:8000</p>
              </div>
            </div>

            <!-- Unavailable Subtitle Fallback (Phase H13) -->
            <div id="isl-unavailable-subtitle" class="isl-unavailable-subtitle hidden">
              <div class="isl-unavailable-sub-header">ISL translation not available in this translator</div>
              <div id="isl-unavailable-sub-text" class="isl-unavailable-sub-text"></div>
            </div>

            <!-- Avatar Quick Controls -->
            <div class="isl-aether-controls">
              <button id="btn-avatar-hello" class="isl-btn" title="Play HELLO">HELLO</button>
              <button id="btn-avatar-good" class="isl-btn" title="Queue GOOD">+GOOD</button>
              <button id="btn-avatar-morning" class="isl-btn" title="Queue MORNING">+MORN</button>
              <button id="btn-avatar-pause" class="isl-btn" title="Pause/Resume">⏸</button>
              <button id="btn-avatar-reset" class="isl-btn isl-btn-danger" title="Reset Avatar">⏹</button>
            </div>
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

      // Cache DOM references
      this.elements = {
        launcher: this.shadowRoot.getElementById('isl-launcher-badge'),
        sidebarToggle: this.shadowRoot.getElementById('isl-sidebar-toggle-handle'),
        container: this.shadowRoot.getElementById('isl-overlay-container'),
        body: this.shadowRoot.getElementById('isl-overlay-body'),
        header: this.shadowRoot.getElementById('isl-header-bar'),
        modeBadge: this.shadowRoot.getElementById('isl-mode-badge'),
        btnLayoutMode: this.shadowRoot.getElementById('btn-layout-mode'),
        btnMinimize: this.shadowRoot.getElementById('btn-minimize'),
        btnClose: this.shadowRoot.getElementById('btn-close'),
        bottomAvatarDock: this.shadowRoot.getElementById('isl-bottom-avatar-dock'),

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
        btnAvatarPause: this.shadowRoot.getElementById('btn-avatar-pause'),
        btnAvatarReset: this.shadowRoot.getElementById('btn-avatar-reset'),

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
    }

    setupDragging() {
      const header = this.elements.header;
      const container = this.elements.container;

      const onMouseDown = (e) => {
        if (e.target.closest('button')) return;
        if (this.isSidebarMode) return; // In sidebar mode, bar stays docked to right edge

        this.isDragging = true;
        const rect = container.getBoundingClientRect();
        this.dragOffset.x = e.clientX - rect.left;
        this.dragOffset.y = e.clientY - rect.top;

        document.addEventListener('mousemove', onMouseMove);
        document.addEventListener('mouseup', onMouseUp);
      };

      const onMouseMove = (e) => {
        if (!this.isDragging) return;
        const left = Math.max(10, Math.min(window.innerWidth - container.offsetWidth - 10, e.clientX - this.dragOffset.x));
        const top = Math.max(10, Math.min(window.innerHeight - container.offsetHeight - 10, e.clientY - this.dragOffset.y));

        container.style.right = 'auto';
        container.style.left = `${left}px`;
        container.style.top = `${top}px`;
      };

      const onMouseUp = () => {
        this.isDragging = false;
        document.removeEventListener('mousemove', onMouseMove);
        document.removeEventListener('mouseup', onMouseUp);
      };

      header.addEventListener('mousedown', onMouseDown);
    }

    bindEvents() {
      const {
        btnMinimize, btnClose, launcher, sidebarToggle, btnLayoutMode,
        btnDemoStart, btnDemoStep, btnDemoStop, selectScenario,
        btnReconnect,
        btnAvatarHello, btnAvatarGood, btnAvatarMorning, btnAvatarPause, btnAvatarReset
      } = this.elements;

      btnMinimize.addEventListener('click', () => this.toggleMinimize());
      btnClose.addEventListener('click', () => this.hide());
      launcher.addEventListener('click', () => this.show());
      if (sidebarToggle) {
        sidebarToggle.addEventListener('click', () => this.expandSidebar());
      }
      if (btnLayoutMode) {
        btnLayoutMode.addEventListener('click', () => this.toggleLayoutMode());
      }

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
      btnAvatarPause.addEventListener('click', () => {
        this.dispatch('AETHER_COMMAND', { command: 'PAUSE' });
      });
      btnAvatarReset.addEventListener('click', () => {
        this.dispatch('AETHER_COMMAND', { command: 'RESET_AVATAR' });
      });
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
      this.elements.container.classList.toggle('minimized', this.isMinimized);

      if (this.isSidebarMode) {
        this.isCollapsed = this.isMinimized;
        this.elements.container.classList.toggle('sidebar-collapsed', this.isCollapsed);
        if (this.elements.sidebarToggle) {
          this.elements.sidebarToggle.classList.toggle('hidden', !this.isCollapsed);
        }
        this.elements.btnMinimize.textContent = this.isCollapsed ? '◀' : '─';
      } else {
        this.elements.btnMinimize.textContent = this.isMinimized ? '□' : '─';
      }
      this.updateHostPageLayout();
    }

    expandSidebar() {
      this.isCollapsed = false;
      this.elements.container.classList.remove('sidebar-collapsed');
      if (this.elements.sidebarToggle) {
        this.elements.sidebarToggle.classList.add('hidden');
      }
      this.elements.btnMinimize.textContent = '─';
      this.updateHostPageLayout();
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
      this.updateHostPageLayout();
    }

    show() {
      this.isVisible = true;
      this.elements.container.classList.remove('hidden');
      this.elements.launcher.classList.add('hidden');
      if (this.isSidebarMode && this.isCollapsed) {
        this.expandSidebar();
      }
      this.updateHostPageLayout();
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
      this.updateHostPageLayout();
    }

    updateHostPageLayout() {
      if (typeof document === 'undefined') return;
      try {
        const isDockedActive = this.isVisible && this.isSidebarMode && !this.isCollapsed;
        const root = document.documentElement;
        if (root && typeof root.setAttribute === 'function') {
          if (isDockedActive) {
            root.setAttribute('data-isl-sidebar-active', 'true');
          } else {
            root.removeAttribute('data-isl-sidebar-active');
          }
        }
        if (typeof document.querySelector === 'function') {
          const primary = document.querySelector('#primary') || document.querySelector('ytd-watch-flexy');
          if (primary && primary.style) {
            if (isDockedActive) {
              primary.style.transition = 'margin-right 0.32s cubic-bezier(0.16, 1, 0.3, 1)';
              primary.style.marginRight = '380px';
              primary.__islShifted = true;
            } else if (primary.__islShifted) {
              primary.style.marginRight = '';
              primary.__islShifted = false;
            }
          }
        }
      } catch (e) {
        // Safe silent degradation in mock DOM or restricted contexts
      }
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
      } else if (activeSignName) {
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
        el.txtRuntimeMsg.textContent = state.runtimeEndpoint ? `Connected: ${state.runtimeEndpoint}` : 'Localhost runtime online';
        el.txtRuntimeMsg.style.color = '#3fb950';

        const targetSrc = state.avatarViewerUrl || `${state.runtimeEndpoint || 'http://localhost:8000'}/tools/avatar_viewer/index.html?embed=1`;
        if (el.aetherIframe.src !== targetSrc) {
          el.aetherIframe.src = targetSrc;
          el.aetherIframe.classList.remove('hidden');
          el.aetherFallback.classList.add('hidden');
        }
      } else {
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

    destroy() {
      this.isVisible = false;
      this.updateHostPageLayout();
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
