/**
 * ISL Accessibility Translator - Overlay UI Component (Phase H6)
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
      this.isVisible = true;
      this.isDragging = false;
      this.dragOffset = { x: 0, y: 0 };
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
    }

    buildDOM() {
      const container = document.createElement('div');
      container.innerHTML = `
        <div id="isl-launcher-badge" class="hidden" title="Click to open ISL Accessibility Translator">
          <span>🤟 ISL Translator</span>
        </div>

        <div id="isl-overlay-container">
          <!-- Header -->
          <div id="isl-header-bar">
            <div class="isl-title-group">
              <span class="isl-app-title">🤟 ISL Translator</span>
              <span class="isl-version-tag">H8 YouTube</span>
            </div>
            <div class="isl-header-actions">
              <button id="btn-minimize" class="isl-icon-btn" title="Minimize">─</button>
              <button id="btn-close" class="isl-icon-btn" title="Close">✕</button>
            </div>
          </div>

          <!-- Status Matrix (Task H6-C) -->
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

          <!-- Body -->
          <div id="isl-overlay-body">
            <!-- Development-mode H7 YouTube job result -->
            <div class="isl-card" id="youtube-result-card">
              <div class="isl-card-header">
                <span>YouTube processing</span>
                <span id="youtube-job-state" class="isl-sublabel">IDLE</span>
              </div>
              <div id="youtube-job-id" class="isl-sublabel">No video job</div>
              <div id="youtube-video-title" class="isl-youtube-title">—</div>
              <div id="youtube-job-progress" class="isl-youtube-progress">Waiting for a job.</div>
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
                <span class="isl-sublabel">Prototype gloss (not full ISL translation)</span>
                <span id="youtube-translation-status" class="isl-sublabel">IDLE</span>
              </div>
              <div id="youtube-glosses" class="isl-gloss-badge">No resolved concepts</div>
              <div class="isl-youtube-result-line">
                <span class="isl-sublabel">Playable signs</span>
                <span id="youtube-playable-signs" class="isl-youtube-playable">None</span>
              </div>
              <div class="isl-youtube-unavailable">
                <div class="isl-unavailable-title">Unavailable concepts (not played)</div>
                <div id="youtube-unavailable-concepts">None</div>
              </div>
            </div>

            <!-- Aether Avatar Integration (Task H6-E) -->
            <div class="isl-card">
              <div class="isl-card-header">
                <span>Aether 3D Avatar</span>
                <span id="aether-status-badge" class="isl-version-tag">Localhost Bridge</span>
              </div>
              <div id="isl-aether-container">
                <iframe id="isl-aether-iframe" src="about:blank" class="hidden"></iframe>
                <div id="isl-aether-fallback">
                  <div class="isl-fallback-badge">Aether Localhost Dev Mode</div>
                  <p style="font-size: 11px; margin-top: 4px;">Avatar loads via local server</p>
                  <p style="font-size: 10px; color: #58a6ff;">http://localhost:8000</p>
                </div>
              </div>
              <div class="isl-aether-controls">
                <button id="btn-avatar-hello" class="isl-btn" title="Play HELLO">HELLO</button>
                <button id="btn-avatar-good" class="isl-btn" title="Queue GOOD">+GOOD</button>
                <button id="btn-avatar-morning" class="isl-btn" title="Queue MORNING">+MORN</button>
                <button id="btn-avatar-pause" class="isl-btn" title="Pause/Resume">⏸</button>
                <button id="btn-avatar-reset" class="isl-btn isl-btn-danger" title="Reset Avatar">⏹</button>
              </div>
            </div>

            <!-- Transcripts Card -->
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

            <!-- ISL Representation Card -->
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

            <!-- Sign Queue & Unavailable Concepts Card -->
            <div class="isl-card">
              <div class="isl-card-header">
                <span>Sign Playback &amp; Queue</span>
              </div>
              <div>
                <span class="isl-sublabel">Active Sign: </span>
                <span id="pill-active-sign" class="isl-sign-tag isl-sign-active" style="display: none;">NONE</span>
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

            <!-- Demo Mode Controls Card (Task H6-D) -->
            <div class="isl-card">
              <div class="isl-card-header">
                <span>Deterministic Demo Mode</span>
                <span id="demo-step-indicator" class="isl-sublabel">Idle</span>
              </div>
              <div style="margin-bottom: 8px;">
                <select id="select-demo-scenario" class="isl-select">
                  <option value="greeting">Greeting: "Hello good morning"</option>
                  <option value="missing_concept">Missing Concept: "I need water"</option>
                </select>
              </div>
              <div class="isl-btn-row">
                <button id="btn-demo-start" class="isl-btn isl-btn-primary">▶ Start Demo</button>
                <button id="btn-demo-step" class="isl-btn">⏭ Next Step</button>
                <button id="btn-demo-stop" class="isl-btn isl-btn-danger">⏹ Reset</button>
              </div>
            </div>

            <!-- Diagnostics & Localhost Connection -->
            <div class="isl-card" style="padding: 8px 12px;">
              <div style="display: flex; justify-content: space-between; align-items: center;">
                <span id="txt-runtime-msg" style="font-size: 10.5px; color: #8b949e;">Localhost runtime offline</span>
                <button id="btn-reconnect" class="isl-btn" style="padding: 3px 8px; font-size: 10px;">🔄 Probe</button>
              </div>
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
        container: this.shadowRoot.getElementById('isl-overlay-container'),
        body: this.shadowRoot.getElementById('isl-overlay-body'),
        header: this.shadowRoot.getElementById('isl-header-bar'),
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
        btnMinimize, btnClose, launcher,
        btnDemoStart, btnDemoStep, btnDemoStop, selectScenario,
        btnReconnect,
        btnAvatarHello, btnAvatarGood, btnAvatarMorning, btnAvatarPause, btnAvatarReset
      } = this.elements;

      btnMinimize.addEventListener('click', () => this.toggleMinimize());
      btnClose.addEventListener('click', () => this.hide());
      launcher.addEventListener('click', () => this.show());

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

    toggleMinimize() {
      this.isMinimized = !this.isMinimized;
      this.elements.container.classList.toggle('minimized', this.isMinimized);
      this.elements.btnMinimize.textContent = this.isMinimized ? '□' : '─';
    }

    show() {
      this.isVisible = true;
      this.elements.container.classList.remove('hidden');
      this.elements.launcher.classList.add('hidden');
    }

    hide() {
      this.isVisible = false;
      this.elements.container.classList.add('hidden');
      this.elements.launcher.classList.remove('hidden');
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
      el.boxGloss.textContent = rep.gloss || (rep.glossSequence?.length ? rep.glossSequence.join(' ') : '—');

      if (rep.trace && rep.trace.length) {
        el.boxTrace.innerHTML = rep.trace.map(t => `<div>• <b>${t.stage}:</b> ${t.detail}</div>`).join('');
      } else {
        el.boxTrace.textContent = 'No transformation trace.';
      }

      // 4. Signing Queue & Current Sign
      const queue = state.signingQueue || {};
      if (queue.currentSign) {
        el.pillActiveSign.style.display = 'inline-block';
        el.pillActiveSign.textContent = queue.currentSign.toUpperCase();
        el.txtNoActive.style.display = 'none';
      } else {
        el.pillActiveSign.style.display = 'none';
        el.txtNoActive.style.display = 'inline';
      }

      if (queue.queuedSigns && queue.queuedSigns.length) {
        el.boxQueuedSigns.innerHTML = queue.queuedSigns
          .map(s => `<span class="isl-sign-tag isl-sign-queued">${s.toUpperCase()}</span>`)
          .join('');
      } else {
        el.boxQueuedSigns.innerHTML = '<span style="color: #8b949e; font-size: 11px;">Queue is empty</span>';
      }

      // 5. Unavailable Concepts (Crucial: transparent missing-sign indication)
      if (queue.unavailableConcepts && queue.unavailableConcepts.length) {
        el.boxUnavailable.classList.remove('hidden');
        el.listUnavailable.innerHTML = queue.unavailableConcepts
          .map(item => `<div class="isl-unavailable-item">✕ <b>${(item.word || item).toUpperCase()}:</b> ${item.reason || 'Pending evidence'}</div>`)
          .join('');
      } else {
        el.boxUnavailable.classList.add('hidden');
        el.listUnavailable.innerHTML = '';
      }

      // 6. Demo mode state
      const demo = state.demo || {};
      if (demo.active) {
        el.demoIndicator.textContent = `Step ${demo.step} / ${demo.totalSteps}`;
        el.demoIndicator.style.color = '#58a6ff';
        if (el.selectScenario.value !== demo.scenario && demo.scenario) {
          el.selectScenario.value = demo.scenario;
        }
      } else {
        el.demoIndicator.textContent = 'Idle';
        el.demoIndicator.style.color = '#8b949e';
      }

      // 7. Runtime Status & Aether Embed
      if (state.runtimeAvailable) {
        el.txtRuntimeMsg.textContent = `Connected: ${state.runtimeEndpoint}`;
        el.txtRuntimeMsg.style.color = '#3fb950';

        // Load iframe if not already loaded
        const targetSrc = `${state.runtimeEndpoint}/tools/avatar_viewer/index.html?embed=1`;
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
