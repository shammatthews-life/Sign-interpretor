/**
 * ISL Accessibility Translator - Service Worker (Phase H6)
 * Manifest V3 Background Coordinator
 */

try {
  importScripts(
    '../shared/message-contract.js',
    '../shared/demo-data.js',
    '../shared/youtube-cue-manifest.js',
    './runtime-bridge.js'
  );
} catch (e) {
  console.warn('[ISL Service Worker] importScripts fallback:', e);
}

const bridge = new (self.ISLRuntimeBridge.RuntimeBridge)({
  defaultEndpoint: 'http://localhost:8000',
  onStateUpdate: (state) => {
    broadcastStateUpdate(state);
    broadcastYouTubeEvent(self.ISLMessageContract.MESSAGE_TYPES.YOUTUBE_STATUS, state.youtube);
    if (state.youtube?.state === 'READY') {
      broadcastYouTubeEvent(self.ISLMessageContract.MESSAGE_TYPES.YOUTUBE_RESULT, {
        job_id: state.youtube.jobId,
        video_id: state.youtube.videoId,
        state: state.youtube.state,
        cue_count: state.youtube.cueCount,
        cue_manifest_fingerprint: state.youtube.cueManifestFingerprint,
        word_coverage: state.youtube.wordCoverage
      });
      announceCueManifestReady(state.youtube).catch(error => {
        console.warn('[ISL Service Worker] Unable to notify YouTube tab:', error.message);
      });
    } else if (state.youtube?.state === 'ERROR') {
      broadcastYouTubeEvent(self.ISLMessageContract.MESSAGE_TYPES.YOUTUBE_ERROR, {
        job_id: state.youtube.jobId,
        error: state.youtube.error
      });
    }
  }
});

const STORAGE_KEY = 'islYoutubeJobsV1';
const MAX_STORED_JOBS = 30;
const MAX_CUE_READY_RETRIES = 3;

function broadcastYouTubeEvent(type, payload) {
  const message = self.ISLMessageContract.createMessage(type, payload || {});
  if (typeof chrome !== 'undefined' && chrome.runtime?.sendMessage) {
    chrome.runtime.sendMessage(message, () => {
      if (chrome.runtime.lastError) { /* No popup is currently open. */ }
    });
  }
}

function getStoredJobs() {
  return new Promise((resolve, reject) => {
    chrome.storage.local.get([STORAGE_KEY], result => {
      if (chrome.runtime.lastError) {
        reject(new Error(chrome.runtime.lastError.message));
        return;
      }
      const jobs = result[STORAGE_KEY];
      if (jobs === undefined) {
        resolve({});
      } else if (jobs && typeof jobs === 'object' && !Array.isArray(jobs)) {
        resolve(jobs);
      } else {
        reject(new Error('Stored YouTube job index has an invalid format.'));
      }
    });
  });
}

function setStoredJobs(jobs) {
  return new Promise((resolve, reject) => {
    chrome.storage.local.set({ [STORAGE_KEY]: jobs }, () => {
      if (chrome.runtime.lastError) {
        reject(new Error(chrome.runtime.lastError.message));
        return;
      }
      resolve();
    });
  });
}

function getTab(tabId) {
  return new Promise((resolve, reject) => {
    chrome.tabs.get(tabId, tab => {
      if (chrome.runtime.lastError) {
        reject(new Error(chrome.runtime.lastError.message));
        return;
      }
      resolve(tab || null);
    });
  });
}

function sendTabMessage(tabId, message) {
  return new Promise(resolve => {
    chrome.tabs.sendMessage(tabId, message, response => {
      resolve({
        response,
        error: chrome.runtime.lastError?.message || null
      });
    });
  });
}

function getActiveTab() {
  return new Promise(resolve => {
    chrome.tabs.query({ active: true, lastFocusedWindow: true }, tabs => {
      resolve(chrome.runtime.lastError ? null : tabs?.[0] || null);
    });
  });
}

function videoIdFromPageUrl(url) {
  const parsed = self.ISLMessageContract.validateYouTubeUrl(url);
  return parsed.valid ? parsed.videoId : null;
}

async function saveYouTubeJob(jobId, videoId, tabId) {
  const jobs = await getStoredJobs();
  jobs[jobId] = {
    jobId,
    videoId,
    tabId: Number.isInteger(tabId) ? tabId : null,
    createdAt: Date.now(),
    acknowledgedAt: null
  };
  const sorted = Object.values(jobs).sort((left, right) => right.createdAt - left.createdAt);
  const retained = Object.fromEntries(sorted.slice(0, MAX_STORED_JOBS).map(job => [job.jobId, job]));
  await setStoredJobs(retained);
  return retained[jobId];
}

async function latestJobForVideo(videoId) {
  const jobs = Object.values(await getStoredJobs())
    .filter(job => job.videoId === videoId)
    .sort((left, right) => right.createdAt - left.createdAt);
  return jobs[0] || null;
}

async function announceCueManifestReady(youtube, attempt = 0) {
  const { jobId, videoId, cueCount, cueManifestFingerprint } = youtube || {};
  if (!jobId || !videoId || !cueManifestFingerprint) return;
  const jobs = await getStoredJobs();
  const target = jobs[jobId];
  if (!target || target.videoId !== videoId || !Number.isInteger(target.tabId)) return;
  let tab;
  try {
    tab = await getTab(target.tabId);
  } catch {
    tab = null;
  }
  if (!tab || videoIdFromPageUrl(tab.url) !== videoId) return;
  const message = self.ISLMessageContract.createMessage(
    self.ISLMessageContract.MESSAGE_TYPES.YOUTUBE_CUES_READY,
    { protocol_version: 1, job_id: jobId, video_id: videoId, cue_count: cueCount, fingerprint: cueManifestFingerprint }
  );
  const result = await sendTabMessage(target.tabId, message);
  if ((!result.response?.received || result.error) && attempt < MAX_CUE_READY_RETRIES) {
    setTimeout(() => {
      announceCueManifestReady(youtube, attempt + 1).catch(error => {
        console.warn('[ISL Service Worker] Cue-ready retry failed:', error.message);
      });
    }, 250 * (attempt + 1));
  } else if (result.error) {
    console.warn('[ISL Service Worker] Cue-ready delivery exhausted retries:', result.error);
  }
}

async function handleCueManifestRequest(message, sender) {
  const tabId = sender?.tab?.id;
  const pageVideoId = videoIdFromPageUrl(sender?.tab?.url || '');
  const requestedVideoId = message.payload?.video_id;
  if (!Number.isInteger(tabId) || !pageVideoId || requestedVideoId !== pageVideoId) {
    throw new Error('Cue requests must come from the matching YouTube video tab.');
  }
  const jobs = await getStoredJobs();
  const record = message.payload?.job_id
    ? jobs[message.payload.job_id]
    : await latestJobForVideo(pageVideoId);
  if (!record || record.videoId !== pageVideoId) throw new Error('No completed translation is available for this video.');
  const latest = await latestJobForVideo(pageVideoId);
  if (!latest || latest.jobId !== record.jobId) throw new Error('A newer translation job superseded these cues.');
  const manifest = await bridge.getYouTubeCueManifest(record.jobId, pageVideoId);
  if (manifest.job_id !== record.jobId || manifest.video_id !== pageVideoId) {
    throw new Error('The saved cue manifest does not match the requested video job.');
  }
  const latestAfterRetrieval = await latestJobForVideo(pageVideoId);
  if (!latestAfterRetrieval || latestAfterRetrieval.jobId !== record.jobId) {
    throw new Error('A newer translation job superseded these cues.');
  }
  const currentJobs = await getStoredJobs();
  const currentRecord = currentJobs[record.jobId];
  const latestFromSnapshot = Object.values(currentJobs)
    .filter(job => job.videoId === pageVideoId)
    .sort((left, right) => right.createdAt - left.createdAt)[0];
  if (!currentRecord || currentRecord.videoId !== pageVideoId
    || latestFromSnapshot?.jobId !== record.jobId) {
    throw new Error('The YouTube job record changed while retrieving its cues.');
  }
  return { record: currentRecord, manifest };
}

function broadcastStateUpdate(state) {
  const msg = self.ISLMessageContract.createMessage(
    self.ISLMessageContract.MESSAGE_TYPES.STATE_UPDATE,
    state
  );
  if (typeof chrome !== 'undefined' && chrome.tabs && chrome.tabs.query) {
    chrome.tabs.query({}, (tabs) => {
      if (chrome.runtime.lastError) return;
      tabs.forEach((tab) => {
        if (!tab.id) return;
        chrome.tabs.sendMessage(tab.id, msg, () => {
          // Ignore errors for tabs without active content script
          if (chrome.runtime.lastError) { /* quiet */ }
        });
      });
    });
  }
}

// Extension installation lifecycle
if (typeof chrome !== 'undefined' && chrome.runtime && chrome.runtime.onInstalled) {
  chrome.runtime.onInstalled.addListener(() => {
    console.log('[ISL Service Worker] Extension installed/updated.');
    // Attempt initial passive health probe to localhost
    bridge.pingRuntime();
  });
}

// Message Dispatcher
if (typeof chrome !== 'undefined' && chrome.runtime && chrome.runtime.onMessage) {
  chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    const { MESSAGE_TYPES } = self.ISLMessageContract;

    if (!message || !message.type) {
      sendResponse({ success: false, error: 'Invalid message payload' });
      return true;
    }

    switch (message.type) {
      case MESSAGE_TYPES.GET_STATE:
        sendResponse({ success: true, payload: bridge.getState() });
        break;

      case MESSAGE_TYPES.CONNECT_RUNTIME:
        bridge.pingRuntime(message.payload?.endpoint).then((state) => {
          sendResponse({ success: true, payload: state });
        });
        return true; // async response

      case MESSAGE_TYPES.YOUTUBE_PROCESS:
        if (typeof message.payload?.url !== 'string') {
          sendResponse({ success: false, error: 'A YouTube URL string is required.' });
          break;
        }
        (async () => {
          const validation = self.ISLMessageContract.validateYouTubeUrl(message.payload.url);
          if (!validation.valid) throw new Error(validation.error);
          let targetTab = sender?.tab || null;
          if (videoIdFromPageUrl(targetTab?.url || '') !== validation.videoId) {
            const activeTab = await getActiveTab();
            targetTab = videoIdFromPageUrl(activeTab?.url || '') === validation.videoId ? activeTab : null;
          }
          const job = await bridge.submitYouTube(validation.canonicalUrl, { deferPolling: true });
          await saveYouTubeJob(job.job_id, validation.videoId, targetTab?.id);
          if (Number.isInteger(targetTab?.id)) {
            const created = self.ISLMessageContract.createMessage(MESSAGE_TYPES.YOUTUBE_JOB_CREATED, {
              protocol_version: 1,
              job_id: job.job_id,
              video_id: validation.videoId
            });
            await sendTabMessage(targetTab.id, created);
          }
          bridge.trackYouTubeJob(job.job_id);
          sendResponse({ success: true, payload: { ...job, video_id: validation.videoId } });
          broadcastYouTubeEvent(MESSAGE_TYPES.YOUTUBE_JOB_CREATED, {
            job_id: job.job_id,
            video_id: validation.videoId
          });
        })().catch(error => {
          bridge.setYouTubeError(error);
          broadcastYouTubeEvent(MESSAGE_TYPES.YOUTUBE_ERROR, { error: error.message });
          sendResponse({ success: false, error: error.message });
        });
        return true;

      case MESSAGE_TYPES.GET_YOUTUBE_CUES:
        handleCueManifestRequest(message, sender).then(({ record, manifest }) => {
          if (!manifest.playback_ready) {
            sendResponse({
              success: false,
              error: 'Timestamped translation cues failed validation; playback was stopped.',
              validation_errors: manifest.validation_errors
            });
            return;
          }
          sendResponse({
            success: true,
            protocol_version: 1,
            job_id: record.jobId,
            video_id: record.videoId,
            fingerprint: manifest.fingerprint,
            payload: manifest
          });
        }).catch(error => sendResponse({ success: false, error: error.message }));
        return true;

      case MESSAGE_TYPES.YOUTUBE_CUES_ACK:
        (async () => {
          const videoId = videoIdFromPageUrl(sender?.tab?.url || '');
          const { job_id: jobId, video_id: acknowledgedVideoId, fingerprint } = message.payload || {};
          if (!Number.isInteger(sender?.tab?.id) || !videoId || videoId !== acknowledgedVideoId) {
            throw new Error('Cue acknowledgement must come from the matching YouTube tab.');
          }
          const jobs = await getStoredJobs();
          const record = jobs[jobId];
          const latestFromSnapshot = Object.values(jobs)
            .filter(job => job.videoId === videoId)
            .sort((left, right) => right.createdAt - left.createdAt)[0];
          if (!record || record.videoId !== videoId || latestFromSnapshot?.jobId !== jobId) {
            throw new Error('Cue acknowledgement does not match the stored video job.');
          }
          const manifest = await bridge.getYouTubeCueManifest(jobId, videoId);
          if (manifest.fingerprint !== fingerprint) {
            throw new Error('Cue acknowledgement fingerprint does not match the stored manifest.');
          }
          const currentJobs = await getStoredJobs();
          const currentRecord = currentJobs[jobId];
          const currentLatest = Object.values(currentJobs)
            .filter(job => job.videoId === videoId)
            .sort((left, right) => right.createdAt - left.createdAt)[0];
          if (!currentRecord || currentRecord.videoId !== videoId || currentLatest?.jobId !== jobId) {
            throw new Error('Cue acknowledgement was superseded by a newer video job.');
          }
          currentRecord.acknowledgedAt = Date.now();
          currentRecord.tabId = sender.tab.id;
          await setStoredJobs(currentJobs);
          sendResponse({ success: true, acknowledged: true });
        })().catch(error => sendResponse({ success: false, error: error.message }));
        return true;

      case MESSAGE_TYPES.YOUTUBE_PAGE_READY:
        (async () => {
          const videoId = videoIdFromPageUrl(sender?.tab?.url || '');
          if (!videoId || message.payload?.video_id !== videoId || !Number.isInteger(sender?.tab?.id)) {
            sendResponse({ success: false, error: 'Page-ready message does not match the sending YouTube tab.' });
            return;
          }
          const jobs = await getStoredJobs();
          const record = Object.values(jobs)
            .filter(job => job.videoId === videoId)
            .sort((left, right) => right.createdAt - left.createdAt)[0] || null;
          if (record) {
            jobs[record.jobId].tabId = sender.tab.id;
            await setStoredJobs(jobs);
            const youtubeState = bridge.getState().youtube;
            if (youtubeState?.jobId === record.jobId
              && youtubeState.state === 'READY'
              && youtubeState.cueManifestFingerprint) {
              await announceCueManifestReady(youtubeState);
            } else {
              bridge.trackYouTubeJob(record.jobId);
            }
          }
          sendResponse({ success: true, video_id: videoId, job_id: record?.jobId || null });
        })().catch(error => {
          console.warn('[ISL Service Worker] Unable to associate YouTube page:', error.message);
          sendResponse({ success: false, error: error.message });
        });
        return true;

      case MESSAGE_TYPES.YOUTUBE_CUES_ERROR:
        console.warn('[ISL Service Worker] YouTube cues were rejected:', message.payload?.error || 'unknown error');
        sendResponse({ success: true });
        break;

      case MESSAGE_TYPES.AETHER_PLAYBACK_STATE:
        bridge.updateAetherPlayback(message.payload || {});
        sendResponse({ success: true });
        break;

      case MESSAGE_TYPES.DISCONNECT_RUNTIME:
        bridge.disconnectRuntime();
        sendResponse({ success: true, payload: bridge.getState() });
        break;

      case MESSAGE_TYPES.DEMO_START:
        bridge.startDemo(message.payload?.scenario || 'greeting');
        sendResponse({ success: true, payload: bridge.getState() });
        break;

      case MESSAGE_TYPES.DEMO_STEP:
        bridge.stepDemo();
        sendResponse({ success: true, payload: bridge.getState() });
        break;

      case MESSAGE_TYPES.DEMO_STOP:
        bridge.stopDemo();
        sendResponse({ success: true, payload: bridge.getState() });
        break;

      case MESSAGE_TYPES.DEMO_SET_SCENARIO:
        bridge.startDemo(message.payload?.scenario || 'greeting');
        sendResponse({ success: true, payload: bridge.getState() });
        break;

      case MESSAGE_TYPES.TOGGLE_OVERLAY:
        const visible = bridge.toggleOverlay();
        sendResponse({ success: true, payload: { overlayVisible: visible } });
        break;

      case MESSAGE_TYPES.SET_OVERLAY_VISIBLE:
        bridge.setOverlayVisible(message.payload?.visible);
        sendResponse({ success: true, payload: bridge.getState() });
        break;

      case MESSAGE_TYPES.AETHER_COMMAND:
        // Broadcast Aether commands directly to active tabs or viewer frames
        broadcastStateUpdate(bridge.getState());
        sendResponse({ success: true, command: message.payload });
        break;

      case MESSAGE_TYPES.PING:
        sendResponse({ success: true, pong: Date.now() });
        break;

      default:
        sendResponse({ success: false, error: `Unhandled message type: ${message.type}` });
        break;
    }

    return true;
  });
}
