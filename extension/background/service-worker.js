/**
 * ISL Accessibility Translator - Service Worker (Phase H6)
 * Manifest V3 Background Coordinator
 */

try {
  importScripts(
    '../shared/message-contract.js',
    '../shared/demo-data.js',
    '../shared/youtube-cue-manifest.js',
    '../shared/aether-playback.js',
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
let storedJobsMutationTail = Promise.resolve();
let playbackMutationTail = Promise.resolve();
const playbackSnapshotsByTab = new Map();
const MAX_PLAYBACK_TABS = 20;
const PLAYBACK_STORAGE_KEY = 'islAetherPlaybackLedgerV1';
const MAX_PLAYBACK_OCCURRENCES = 5000;

function getSessionValue(key) {
  return new Promise((resolve, reject) => {
    if (!chrome.storage.session) {
      reject(new Error('Chrome session storage is required for reliable playback acknowledgements.'));
      return;
    }
    chrome.storage.session.get([key], result => {
      if (chrome.runtime.lastError) {
        reject(new Error(chrome.runtime.lastError.message));
        return;
      }
      resolve(result[key]);
    });
  });
}

function setSessionValue(key, value) {
  return new Promise((resolve, reject) => {
    if (!chrome.storage.session) {
      reject(new Error('Chrome session storage is required for reliable playback acknowledgements.'));
      return;
    }
    chrome.storage.session.set({ [key]: value }, () => {
      if (chrome.runtime.lastError) {
        reject(new Error(chrome.runtime.lastError.message));
        return;
      }
      resolve();
    });
  });
}

function recordPlaybackLifecycle(tabId, videoId, jobId, event) {
  const key = `${PLAYBACK_STORAGE_KEY}:${tabId}:${videoId}:${jobId}`;
  const scope = `${videoId}:${jobId}`;
  const operation = playbackMutationTail.then(async () => {
    const stored = await getSessionValue(key);
    const occurrences = stored === undefined ? [] : stored;
    if (!Array.isArray(occurrences)) throw new Error('Stored playback lifecycle ledger has an invalid format.');
    const ledger = new self.ISLAetherPlayback.AetherPlaybackLedger();
    for (const occurrence of occurrences) {
      if (!occurrence || typeof occurrence.eventId !== 'string' || !Array.isArray(occurrence.events)) {
        throw new Error('Stored playback lifecycle occurrence is malformed.');
      }
      for (const previousEvent of occurrence.events) {
        const restored = ledger.record(previousEvent, scope);
        if (!restored.valid) throw new Error(`Stored playback lifecycle history is invalid: ${restored.error}`);
      }
    }
    const result = ledger.record(event, scope);
    if (!result.valid) throw new Error(result.error);
    if (result.accepted) {
      let occurrence = occurrences.find(item => item.eventId === event.eventId);
      if (!occurrence) {
        occurrence = { eventId: event.eventId, events: [] };
        occurrences.push(occurrence);
      }
      occurrence.events.push(event);
      if (occurrences.length > MAX_PLAYBACK_OCCURRENCES) {
        occurrences.splice(0, occurrences.length - MAX_PLAYBACK_OCCURRENCES);
      }
      await setSessionValue(key, occurrences);
    }
    return result;
  });
  playbackMutationTail = operation.then(() => undefined, () => undefined);
  return operation;
}

function validPlaybackSnapshot(snapshot) {
  return snapshot && typeof snapshot === 'object' && !Array.isArray(snapshot)
    && (snapshot.current === null || (typeof snapshot.current === 'string' && /^[a-z0-9_]{1,80}$/.test(snapshot.current)))
    && Array.isArray(snapshot.queued)
    && snapshot.queued.length <= 512
    && snapshot.queued.every(signId => typeof signId === 'string' && /^[a-z0-9_]{1,80}$/.test(signId))
    && (snapshot.paused === undefined || typeof snapshot.paused === 'boolean')
    && (snapshot.currentTimeMs === undefined || snapshot.currentTimeMs === null
      || (Number.isFinite(snapshot.currentTimeMs) && snapshot.currentTimeMs >= 0));
}

async function handleAetherPlaybackState(message, sender) {
  const tabId = sender?.tab?.id;
  const videoId = videoIdFromPageUrl(sender?.tab?.url || '');
  const payload = message.payload || {};
  if (!Number.isInteger(tabId) || !videoId) {
    throw new Error('Playback state must come from an active YouTube tab.');
  }
  if (payload.video_id !== videoId) {
    throw new Error('Playback state does not match the sending YouTube tab.');
  }

  if (payload.kind === 'snapshot') {
    if (!validPlaybackSnapshot(payload.state)) throw new Error('Aether playback snapshot is malformed.');
    playbackSnapshotsByTab.set(tabId, {
      videoId,
      state: {
        current: payload.state.current,
        queued: [...payload.state.queued],
        paused: Boolean(payload.state.paused),
        currentTimeMs: Number.isFinite(payload.state.currentTimeMs) ? payload.state.currentTimeMs : null
      },
      receivedAt: Date.now()
    });
    while (playbackSnapshotsByTab.size > MAX_PLAYBACK_TABS) {
      playbackSnapshotsByTab.delete(playbackSnapshotsByTab.keys().next().value);
    }
    return { success: true, accepted: true, tab_id: tabId };
  }

  if (payload.protocol_version !== 1) throw new Error('Unsupported playback lifecycle protocol version.');
  const event = {
    type: payload.event_type,
    id: payload.sign_id,
    eventId: payload.event_id,
    jobId: payload.job_id,
    cueId: payload.cue_id,
    atMs: payload.at_ms,
    reason: payload.reason || undefined
  };
  const validation = self.ISLAetherPlayback.validateLifecycleEvent(event);
  if (!validation.valid) throw new Error(validation.error);
  if (event.jobId) {
    const jobs = await getConsistentStoredJobs();
    const record = jobs[event.jobId];
    if (!record || record.videoId !== videoId || record.tabId !== tabId) {
      throw new Error('Playback lifecycle event does not belong to this YouTube tab and job.');
    }
  }
  if (payload.cue_start_seconds !== null && payload.cue_start_seconds !== undefined
    && (!Number.isFinite(payload.cue_start_seconds) || payload.cue_start_seconds < 0)) {
    throw new Error('Playback lifecycle event has an invalid cue start timestamp.');
  }
  if (payload.cue_end_seconds !== null && payload.cue_end_seconds !== undefined
    && (!Number.isFinite(payload.cue_end_seconds) || payload.cue_end_seconds <= 0)) {
    throw new Error('Playback lifecycle event has an invalid cue end timestamp.');
  }
  if (payload.cue_start_seconds !== null && payload.cue_start_seconds !== undefined
    && payload.cue_end_seconds !== null && payload.cue_end_seconds !== undefined
    && payload.cue_end_seconds <= payload.cue_start_seconds) {
    throw new Error('Playback lifecycle event has an inverted cue interval.');
  }
  if (payload.video_time_seconds !== null && payload.video_time_seconds !== undefined
    && (!Number.isFinite(payload.video_time_seconds) || payload.video_time_seconds < 0)) {
    throw new Error('Playback lifecycle event has an invalid video timestamp.');
  }
  if (payload.timing_error_ms !== null && payload.timing_error_ms !== undefined
    && !Number.isFinite(payload.timing_error_ms)) {
    throw new Error('Playback lifecycle event has an invalid synchronization measurement.');
  }
  if (payload.video_paused !== null && payload.video_paused !== undefined && typeof payload.video_paused !== 'boolean') {
    throw new Error('Playback lifecycle event has an invalid video pause state.');
  }
  if (payload.playback_rate !== null && payload.playback_rate !== undefined
    && (!Number.isFinite(payload.playback_rate) || payload.playback_rate <= 0)) {
    throw new Error('Playback lifecycle event has an invalid playback rate.');
  }
  const cueBoundary = event.type === 'playback_start'
    ? payload.cue_start_seconds
    : event.type === 'playback_end' ? payload.cue_end_seconds : null;
  if (cueBoundary !== null && cueBoundary !== undefined && payload.video_time_seconds !== null
    && payload.video_time_seconds !== undefined) {
    const expectedTimingError = Math.round((payload.video_time_seconds - cueBoundary) * 1000);
    if (payload.timing_error_ms !== expectedTimingError) {
      throw new Error('Playback lifecycle synchronization error does not match its timestamps.');
    }
  } else if (payload.timing_error_ms !== null && payload.timing_error_ms !== undefined) {
    throw new Error('Playback lifecycle event cannot report timing error without a cue boundary.');
  }
  const lifecycleJobId = event.jobId || 'manual';
  const result = await recordPlaybackLifecycle(tabId, videoId, lifecycleJobId, event);
  return {
    success: true,
    accepted: result.accepted,
    duplicate: result.duplicate,
    status: result.status,
    tab_id: tabId,
    video_id: videoId,
    job_id: event.jobId,
    event_id: event.eventId,
    timing_error_ms: payload.timing_error_ms ?? null
  };
}

async function dispatchAetherCommand(message, sender) {
  const payload = message.payload;
  if (!payload || typeof payload !== 'object' || Array.isArray(payload)) {
    throw new Error('Aether command payload must be an object.');
  }
  const commands = self.ISLMessageContract.AETHER_COMMANDS;
  if (!Object.values(commands).includes(payload.command)) throw new Error('Unknown Aether command.');
  const tab = sender?.tab || await getActiveTab();
  const targetTabId = tab?.id;
  const videoId = videoIdFromPageUrl(tab?.url || '');
  if (!Number.isInteger(targetTabId) || !videoId) {
    throw new Error('Aether commands require an active YouTube tab.');
  }
  if (payload.jobId !== undefined && payload.jobId !== null) {
    if (typeof payload.jobId !== 'string' || !payload.jobId || payload.jobId.length > 256) {
      throw new Error('Aether command has an invalid job ID.');
    }
    const jobs = await getConsistentStoredJobs();
    const job = jobs[payload.jobId];
    if (!job || job.videoId !== videoId || job.tabId !== targetTabId) {
      throw new Error('Aether command job does not belong to the target YouTube tab.');
    }
  }
  if (payload.cueId !== undefined && payload.cueId !== null
    && (typeof payload.cueId !== 'string' || !payload.cueId || payload.cueId.length > 256)) {
    throw new Error('Aether command has an invalid cue ID.');
  }
  if (payload.cueId !== undefined && payload.cueId !== null && !payload.jobId) {
    throw new Error('Cue-scoped Aether commands require a job ID.');
  }
  if (payload.command === commands.QUEUE_SIGN || payload.command === commands.PLAY_SIGN) {
    if (!/^[a-z0-9_]{1,80}$/.test(payload.signId || '')
      || typeof payload.eventId !== 'string' || !payload.eventId || payload.eventId.length > 256) {
      throw new Error('Aether sign commands require valid sign and event IDs.');
    }
  }
  if (payload.command === commands.CUE_TRANSITION
    && (!payload.jobId || payload.cueId === undefined
      || typeof payload.eventId !== 'string' || !payload.eventId || payload.eventId.length > 256)) {
    throw new Error('Cue transitions require a job ID, cue ID or null, and event ID.');
  }
  if (payload.command === commands.CANCEL_JOB
    && (!payload.jobId || typeof payload.eventId !== 'string' || !payload.eventId || payload.eventId.length > 256)) {
    throw new Error('Job cancellation requires a job ID and event ID.');
  }
  if (payload.command === commands.CANCEL_EVENT
    && (typeof payload.targetEventId !== 'string' || !payload.targetEventId
      || typeof payload.eventId !== 'string' || !payload.eventId || payload.eventId.length > 256)) {
    throw new Error('Event cancellation requires a target event ID and event ID.');
  }
  if (payload.command === commands.SET_PLAYBACK_RATE
    && (!Number.isFinite(payload.rate) || payload.rate <= 0 || payload.rate > 16)) {
    throw new Error('Playback rate must be finite and between 0 and 16.');
  }
  const result = await sendTabMessage(
    targetTabId,
    self.ISLMessageContract.createMessage(self.ISLMessageContract.MESSAGE_TYPES.AETHER_COMMAND, payload)
  );
  if (result.error || !result.response?.received) {
    throw new Error(result.error || 'YouTube content script did not receive the Aether command.');
  }
  return { success: true, delivered: true, tab_id: targetTabId, video_id: videoId };
}

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

function updateStoredJobs(mutator) {
  const operation = storedJobsMutationTail.then(async () => {
    const jobs = await getStoredJobs();
    const result = await mutator(jobs);
    await setStoredJobs(jobs);
    return result;
  });
  storedJobsMutationTail = operation.then(() => undefined, () => undefined);
  return operation;
}

function getConsistentStoredJobs() {
  const operation = storedJobsMutationTail.then(() => getStoredJobs());
  storedJobsMutationTail = operation.then(() => undefined, () => undefined);
  return operation;
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
  return updateStoredJobs(jobs => {
    jobs[jobId] = {
      jobId,
      videoId,
      tabId: Number.isInteger(tabId) ? tabId : null,
      createdAt: Date.now(),
      acknowledgedAt: null
    };
    const sorted = Object.values(jobs).sort((left, right) => right.createdAt - left.createdAt);
    const retained = Object.fromEntries(sorted.slice(0, MAX_STORED_JOBS).map(job => [job.jobId, job]));
    for (const existingJobId of Object.keys(jobs)) delete jobs[existingJobId];
    Object.assign(jobs, retained);
    return retained[jobId];
  });
}

async function latestJobForVideo(videoId) {
  const jobs = Object.values(await getConsistentStoredJobs())
    .filter(job => job.videoId === videoId)
    .sort((left, right) => right.createdAt - left.createdAt);
  return jobs[0] || null;
}

async function announceCueManifestReady(youtube, attempt = 0) {
  const { jobId, videoId, cueCount, cueManifestFingerprint } = youtube || {};
  if (!jobId || !videoId || !cueManifestFingerprint) return;
  const jobs = await getConsistentStoredJobs();
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
  const jobs = await getConsistentStoredJobs();
  const record = message.payload?.job_id
    ? jobs[message.payload.job_id]
    : await latestJobForVideo(pageVideoId);
  if (!record || record.videoId !== pageVideoId) throw new Error('No completed translation is available for this video.');
  if (record.tabId !== null && record.tabId !== tabId) {
    throw new Error('This translation job is associated with a different YouTube tab.');
  }
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
  const currentRecord = await updateStoredJobs(currentJobs => {
    const current = currentJobs[record.jobId];
    const latestFromSnapshot = Object.values(currentJobs)
      .filter(job => job.videoId === pageVideoId)
      .sort((left, right) => right.createdAt - left.createdAt)[0];
    if (!current || current.videoId !== pageVideoId || latestFromSnapshot?.jobId !== record.jobId) {
      throw new Error('The YouTube job record changed while retrieving its cues.');
    }
    if (current.tabId !== null && current.tabId !== tabId) {
      throw new Error('This translation job is associated with a different YouTube tab.');
    }
    current.tabId = tabId;
    return current;
  });
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

if (typeof chrome !== 'undefined' && chrome.tabs?.onRemoved) {
  chrome.tabs.onRemoved.addListener(tabId => {
    playbackSnapshotsByTab.delete(tabId);
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
          const jobs = await getConsistentStoredJobs();
          const record = jobs[jobId];
          const latestFromSnapshot = Object.values(jobs)
            .filter(job => job.videoId === videoId)
            .sort((left, right) => right.createdAt - left.createdAt)[0];
          if (!record || record.videoId !== videoId || record.tabId !== sender.tab.id
            || latestFromSnapshot?.jobId !== jobId) {
            throw new Error('Cue acknowledgement does not match the stored video job.');
          }
          const manifest = await bridge.getYouTubeCueManifest(jobId, videoId);
          if (manifest.fingerprint !== fingerprint) {
            throw new Error('Cue acknowledgement fingerprint does not match the stored manifest.');
          }
          await updateStoredJobs(currentJobs => {
            const currentRecord = currentJobs[jobId];
            const currentLatest = Object.values(currentJobs)
              .filter(job => job.videoId === videoId)
              .sort((left, right) => right.createdAt - left.createdAt)[0];
            if (!currentRecord || currentRecord.videoId !== videoId || currentLatest?.jobId !== jobId) {
              throw new Error('Cue acknowledgement was superseded by a newer video job.');
            }
            currentRecord.acknowledgedAt = Date.now();
          });
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
          const record = await updateStoredJobs(jobs => {
            const latest = Object.values(jobs)
              .filter(job => job.videoId === videoId)
              .sort((left, right) => right.createdAt - left.createdAt)[0] || null;
            if (!latest) return { job: null, associated: false };
            const current = jobs[latest.jobId];
            if (current.tabId === null || current.tabId === sender.tab.id) {
              current.tabId = sender.tab.id;
              return { job: current, associated: true };
            }
            return { job: current, associated: false };
          });
          if (record.job && record.associated) {
            const youtubeState = bridge.getState().youtube;
            if (youtubeState?.jobId === record.job.jobId
              && youtubeState.state === 'READY'
              && youtubeState.cueManifestFingerprint) {
              await announceCueManifestReady(youtubeState);
            } else {
              bridge.trackYouTubeJob(record.job.jobId);
            }
          }
          sendResponse({
            success: true,
            video_id: videoId,
            job_id: record.job?.jobId || null,
            associated: record.associated
          });
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
        handleAetherPlaybackState(message, sender)
          .then(sendResponse)
          .catch(error => sendResponse({ success: false, error: error.message }));
        return true;

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
        dispatchAetherCommand(message, sender)
          .then(sendResponse)
          .catch(error => sendResponse({ success: false, error: error.message }));
        return true;

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
