/**
 * ISL Accessibility Translator - Extension Popup Script.
 */

document.addEventListener('DOMContentLoaded', () => {
  const contract = window.ISLMessageContract;
  if (!contract) return;

  const byId = id => document.getElementById(id);
  const input = byId('youtube-url');
  const processButton = byId('btn-youtube-process');
  const errorElement = byId('youtube-error');
  let currentYoutube = null;

  function sendMessage(type, payload = {}) {
    return new Promise((resolve, reject) => {
      chrome.runtime.sendMessage(contract.createMessage(type, payload), response => {
        if (chrome.runtime.lastError) {
          reject(new Error(`Local extension runtime unavailable: ${chrome.runtime.lastError.message}`));
          return;
        }
        if (!response?.success) {
          reject(new Error(response?.error || 'The extension could not complete the request.'));
          return;
        }
        resolve(response.payload);
      });
    });
  }

  function renderYoutube(youtube = {}, signingQueue = {}) {
    currentYoutube = { ...youtube, currentSign: signingQueue.currentSign || youtube.currentSign, queuedSigns: signingQueue.queuedSigns || youtube.queuedSigns };
    youtube = currentYoutube;
    const state = youtube.state || 'IDLE';
    const stateElement = byId('youtube-job-state');
    stateElement.textContent = state;
    stateElement.className = `status-badge ${state === 'READY' ? 'status-green' : state === 'ERROR' ? 'status-red' : state === 'IDLE' ? 'status-muted' : 'status-blue'}`;
    byId('youtube-job-id').textContent = youtube.jobId ? `Job ${youtube.jobId}` : 'No active job';
    byId('youtube-title').textContent = youtube.title || '';
    byId('youtube-stage').textContent = state === 'READY'
      ? `Complete${youtube.duration ? ` · video ${Number(youtube.duration).toFixed(0)} s` : ''}${youtube.audioDuration ? ` · audio ${Number(youtube.audioDuration).toFixed(1)} s` : ''}`
      : state === 'ERROR' ? 'Processing failed.'
        : state === 'IDLE' ? 'Enter a YouTube URL to begin.'
          : `${state} · ${Math.round((Number(youtube.progress) || 0) * 100)}%`;
    byId('youtube-transcript').textContent = youtube.segmentCount
      ? `Transcript: ${youtube.segmentCount} segments. Latest: ${youtube.latestSegment || '—'}`
      : '';
    const statusCounts = Object.entries(youtube.translationStatusCounts || {})
      .map(([status, count]) => `${status} ${count}`).join(', ');
    byId('youtube-translation').textContent = youtube.translationStatus && youtube.translationStatus !== 'IDLE'
      ? `${youtube.translationStatus}${statusCounts ? ` · ${statusCounts}` : ''}. Gloss concepts: ${(youtube.glosses || []).join(' ') || 'none'}.`
      : '';
    const signs = youtube.playableSigns || [];
    byId('youtube-signs').textContent = signs.length
      ? `Playable signs: ${signs.map(sign => sign.toUpperCase()).join(', ')}. Aether current: ${currentYoutube?.currentSign || 'pending'}; queue: ${(currentYoutube?.queuedSigns || [...new Set(signs)]).map(sign => sign.toUpperCase()).join(', ') || 'empty'}.`
      : state === 'READY' ? 'Playable signs: none.' : '';
    const unavailable = youtube.unavailableConcepts || [];
    byId('youtube-unavailable').textContent = unavailable.length
      ? `Unavailable (not played): ${[...new Set(unavailable.map(item => `${item.word.toUpperCase()} — ${item.reason || 'motion unavailable'}`))].join('; ')}`
      : '';
    errorElement.textContent = youtube.error || '';
    if (state === 'READY' || state === 'ERROR') {
      processButton.disabled = false;
      processButton.textContent = 'Process Video';
    }
  }

  function refreshState() {
    return sendMessage(contract.MESSAGE_TYPES.GET_STATE).then(state => {
      if (state.overlayVisible) {
        byId('pop-overlay-status').textContent = 'VISIBLE';
        byId('pop-overlay-status').className = 'status-badge status-green';
      } else {
        byId('pop-overlay-status').textContent = 'HIDDEN';
        byId('pop-overlay-status').className = 'status-badge status-muted';
      }
      if (state.runtimeAvailable) {
        byId('pop-runtime-status').textContent = 'CONNECTED';
        byId('pop-runtime-status').className = 'status-badge status-green';
      } else {
        byId('pop-runtime-status').textContent = 'DISCONNECTED';
        byId('pop-runtime-status').className = 'status-badge status-muted';
      }
      if (state.runtimeEndpoint) byId('pop-endpoint-text').textContent = state.runtimeEndpoint;
      renderYoutube(state.youtube, state.signingQueue);
    }).catch(error => {
      errorElement.textContent = error.message;
    });
  }

  byId('btn-toggle-overlay').addEventListener('click', () => {
    sendMessage(contract.MESSAGE_TYPES.TOGGLE_OVERLAY).then(refreshState).catch(error => { errorElement.textContent = error.message; });
  });
  byId('btn-probe-runtime').addEventListener('click', () => {
    byId('pop-runtime-status').textContent = 'CONNECTING...';
    sendMessage(contract.MESSAGE_TYPES.CONNECT_RUNTIME).then(refreshState).catch(error => { errorElement.textContent = error.message; });
  });
  byId('btn-open-viewer').addEventListener('click', () => {
    chrome.tabs.create({ url: 'http://localhost:8000/tools/avatar_viewer/index.html' });
  });
  byId('btn-pop-demo-greeting').addEventListener('click', () => {
    sendMessage(contract.MESSAGE_TYPES.DEMO_START, { scenario: 'greeting' }).then(refreshState);
  });
  byId('btn-pop-demo-missing').addEventListener('click', () => {
    sendMessage(contract.MESSAGE_TYPES.DEMO_START, { scenario: 'missing_concept' }).then(refreshState);
  });
  byId('btn-pop-demo-reset').addEventListener('click', () => {
    sendMessage(contract.MESSAGE_TYPES.DEMO_STOP).then(refreshState);
  });

  processButton.addEventListener('click', async () => {
    errorElement.textContent = '';
    const validation = contract.validateYouTubeUrl(input.value);
    if (!validation.valid) {
      errorElement.textContent = validation.error;
      input.setAttribute('aria-invalid', 'true');
      input.focus();
      return;
    }
    input.removeAttribute('aria-invalid');
    processButton.disabled = true;
    processButton.textContent = 'Submitting…';
    byId('youtube-stage').textContent = 'Connecting to local H7 runtime…';
    try {
      const job = await sendMessage(contract.MESSAGE_TYPES.YOUTUBE_PROCESS, { url: validation.canonicalUrl });
      renderYoutube({ ...currentYoutube, jobId: job.job_id, state: job.state, progress: 0, error: null });
      processButton.disabled = true;
      processButton.textContent = 'Processing…';
      await refreshState();
    } catch (error) {
      errorElement.textContent = error.message;
      processButton.disabled = false;
      processButton.textContent = 'Process Video';
    }
  });

  chrome.runtime.onMessage.addListener(message => {
    if (!message || message.version !== contract.CONTRACT_VERSION) return;
    if ([contract.MESSAGE_TYPES.STATE_UPDATE, contract.MESSAGE_TYPES.YOUTUBE_STATUS, contract.MESSAGE_TYPES.YOUTUBE_RESULT].includes(message.type)) {
      const youtube = message.type === contract.MESSAGE_TYPES.STATE_UPDATE
        ? message.payload?.youtube
        : message.payload;
      if (youtube) {
        renderYoutube(youtube, message.payload?.signingQueue);
        if (youtube.state !== 'READY' && youtube.state !== 'ERROR') {
          processButton.disabled = true;
          processButton.textContent = 'Processing…';
        }
      }
    } else if (message.type === contract.MESSAGE_TYPES.YOUTUBE_ERROR) {
      errorElement.textContent = message.payload?.error || 'YouTube processing failed.';
      processButton.disabled = false;
      processButton.textContent = 'Process Video';
    }
  });

  refreshState();
});
