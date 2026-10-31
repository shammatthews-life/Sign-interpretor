/**
 * ISL Accessibility Translator - Content Script (Phase H6)
 * Injected into supported web pages (including YouTube).
 *
 * Safety & Privacy Guarantees:
 * - Does NOT scrape private or authenticated data.
 * - Does NOT intercept or alter user media without permission.
 * - Does NOT interfere with YouTube video controls or DOM playback elements.
 * - Operates entirely within an encapsulated Shadow DOM.
 */

(function () {
  'use strict';

  // Prevent multiple injections
  if (window.__ISL_EXTENSION_INJECTED__) return;
  window.__ISL_EXTENSION_INJECTED__ = true;

  const contract = window.ISLMessageContract;
  const overlayUI = window.ISLOverlay?.ISLOverlayUI;

  if (!contract || !overlayUI) {
    console.error('[ISL Content Script] Required dependencies missing from page context.');
    return;
  }

  function observeVideoElementChanges() {
    if (videoElementObserver || !document.documentElement) return;
    videoElementObserver = new MutationObserver(() => {
      if (!synchronizer) return;
      const currentVideo = getVideoElement();
      if (currentVideo !== synchronizer.video) synchronizer.rebind(currentVideo);
    });
    videoElementObserver.observe(document.documentElement, { childList: true, subtree: true });
  }

  let ui = null;
  let synchronizer = null;
  let currentVideoId = null;
  let activeCueJobId = null;
  const requestedCueJobs = new Map();
  const deliveredOccurrenceIds = new Set();
  const pendingAetherCommands = [];
  const inFlightAetherCommands = new Map();
  let videoElementObserver = null;
  const MAX_PENDING_AETHER_COMMANDS = 256;
  const MAX_IN_FLIGHT_AETHER_COMMANDS = 64;
  const MAX_AETHER_DELIVERY_ATTEMPTS = 20;
  const AETHER_ACK_TIMEOUT_MS = 1000;

  function getCurrentVideoId() {
    const result = contract.validateYouTubeUrl(window.location.href);
    return result.valid ? result.videoId : null;
  }

  function getVideoElement() {
    return document.querySelector('video.html5-main-video') || document.querySelector('video');
  }

  function sendRuntimeMessage(message) {
    return new Promise((resolve, reject) => {
      if (typeof chrome === 'undefined' || !chrome.runtime?.sendMessage) {
        reject(new Error('Extension messaging is unavailable.'));
        return;
      }
      chrome.runtime.sendMessage(message, response => {
        if (chrome.runtime.lastError) {
          reject(new Error(chrome.runtime.lastError.message));
          return;
        }
        resolve(response);
      });
    });
  }

  function sleep(delayMs) {
    return new Promise(resolve => setTimeout(resolve, delayMs));
  }

  function acknowledgeCueManifest(jobId, videoId, fingerprint) {
    sendRuntimeMessage(contract.createMessage(contract.MESSAGE_TYPES.YOUTUBE_CUES_ACK, {
      job_id: jobId, video_id: videoId, fingerprint
    })).then(ack => {
      if (!ack?.success) console.warn('[ISL Content Script] Cue acknowledgement was rejected:', ack?.error || 'unknown error');
    }).catch(error => {
      console.warn('[ISL Content Script] Cue acknowledgement failed:', error.message);
    });
  }

  function ensureSynchronizer() {
    if (synchronizer) {
      synchronizer.rebind(getVideoElement());
      return synchronizer;
    }
    const syncClass = window.ISLTimelineSynchronizer?.YouTubeTimelineSynchronizer;
    if (!syncClass) return null;

    synchronizer = new syncClass({
      videoElement: getVideoElement(),
      onDispatchSign: (signId, metadata = {}) => {
        const command = metadata.command === 'QUEUE_SIGN'
          ? contract.AETHER_COMMANDS.QUEUE_SIGN
          : contract.AETHER_COMMANDS.PLAY_SIGN;
        forwardAetherCommand({ ...metadata, command, signId });
      },
      onDispatchCommand: (command, payload = {}) => {
        forwardAetherCommand({ ...payload, command: contract.AETHER_COMMANDS[command] || command });
      },
      onFallback: (text) => {
        if (ui) ui.setUnavailableFallback(text, 0);
      },
      onClearFallback: () => {
        if (ui) ui.setUnavailableFallback(null);
      }
    });
    return synchronizer;
  }

  function initializeOverlay() {
    if (ui) return;
    observeVideoElementChanges();

    ui = new overlayUI({
      onAction: (actionType, payload) => {
        handleUserAction(actionType, payload);
      }
    });

    ui.mount(document);

    // Fetch initial state from service worker
    if (typeof chrome !== 'undefined' && chrome.runtime?.sendMessage) {
      chrome.runtime.sendMessage(
        contract.createMessage(contract.MESSAGE_TYPES.GET_STATE),
        (response) => {
          if (chrome.runtime.lastError) {
            console.debug('[ISL Content Script] Background service worker not ready:', chrome.runtime.lastError.message);
            // Default initial state
            ui.update(contract.createInitialState());
            return;
          }
          if (response?.success && response.payload) {
            ui.update(response.payload);
          }
        }
      );
    }
  }

  function handleUserAction(actionType, payload) {
    if (typeof chrome === 'undefined' || !chrome.runtime?.sendMessage) return;

    const msg = contract.createMessage(actionType, payload);
    chrome.runtime.sendMessage(msg, (response) => {
      if (chrome.runtime.lastError) {
        console.warn('[ISL Content Script] Error sending action:', chrome.runtime.lastError.message);
        return;
      }
      if (response?.payload) {
        ui.update(response.payload);
      }
    });

    // If action is an Aether command, postMessage to local iframe if present
    if (actionType === contract.MESSAGE_TYPES.AETHER_COMMAND) {
      forwardAetherCommand(payload);
    }
  }

  function showAetherDeliveryFailure(payload, reason) {
    const sign = payload.signId ? ` "${payload.signId}"` : '';
    const detail = reason ? ` (${reason})` : '';
    ui?.setUnavailableFallback(`Sign playback${sign} was not accepted${detail}. The source transcript is unchanged.`, 0);
    console.warn('[ISL Content Script] Aether command was not accepted:', {
      eventId: payload.eventId || null,
      signId: payload.signId || null,
      reason
    });
  }

  function queueAetherCommand(payload) {
    if (payload.eventId && (deliveredOccurrenceIds.has(payload.eventId)
      || inFlightAetherCommands.has(payload.eventId)
      || pendingAetherCommands.some(item => item.eventId === payload.eventId))) return;
    if (pendingAetherCommands.length >= MAX_PENDING_AETHER_COMMANDS) {
      showAetherDeliveryFailure(payload, 'Aether delivery queue is full');
      return;
    }
    pendingAetherCommands.push(payload);
  }

  function postAetherCommand(payload, iframe, origin, attempt = 1) {
    const eventId = payload.eventId;
    const entry = eventId ? inFlightAetherCommands.get(eventId) : null;
    if (entry) entry.attempts = attempt;
    try {
      iframe.contentWindow.postMessage({
        type: 'ISL_AETHER_COMMAND',
        parentOrigin: window.location.origin,
        command: payload.command,
        signId: payload.signId,
        cueId: payload.cueId,
        jobId: payload.jobId,
        occurrenceIndex: payload.occurrenceIndex,
        eventId,
        rate: payload.rate
      }, origin);
    } catch (error) {
      if (eventId) inFlightAetherCommands.delete(eventId);
      console.warn('[ISL Content Script] Unable to forward Aether command:', error.message);
      showAetherDeliveryFailure(payload, error.message);
      return;
    }
    if (!eventId) return;
    clearTimeout(entry.timer);
    entry.timer = setTimeout(() => {
      if (!inFlightAetherCommands.has(eventId)) return;
      if (entry.attempts < MAX_AETHER_DELIVERY_ATTEMPTS) {
        postAetherCommand(payload, iframe, origin, entry.attempts + 1);
        return;
      }
      inFlightAetherCommands.delete(eventId);
      showAetherDeliveryFailure(payload, 'Aether acknowledgement timed out');
      flushAetherCommands();
    }, AETHER_ACK_TIMEOUT_MS);
  }

  function forwardAetherCommand(payload = {}) {
    const command = payload.command;
    if (!Object.values(contract.AETHER_COMMANDS).includes(command)) {
      console.warn('[ISL Content Script] Ignoring invalid Aether command:', command);
      return;
    }
    if (payload.eventId && deliveredOccurrenceIds.has(payload.eventId)) return;
    if (command === contract.AETHER_COMMANDS.RESET_AVATAR) {
      for (const [eventId, entry] of inFlightAetherCommands) {
        clearTimeout(entry.timer);
        inFlightAetherCommands.delete(eventId);
      }
      for (let index = pendingAetherCommands.length - 1; index >= 0; index -= 1) {
        if (pendingAetherCommands[index].eventId) pendingAetherCommands.splice(index, 1);
      }
    } else if (command === contract.AETHER_COMMANDS.CUE_TRANSITION) {
      const isSignCommand = item => item.command === contract.AETHER_COMMANDS.PLAY_SIGN
        || item.command === contract.AETHER_COMMANDS.QUEUE_SIGN;
      const belongsToCue = item => item.jobId === payload.jobId && item.cueId === payload.cueId;
      for (let index = pendingAetherCommands.length - 1; index >= 0; index -= 1) {
        const pending = pendingAetherCommands[index];
        if (isSignCommand(pending) && !belongsToCue(pending)) {
          pendingAetherCommands.splice(index, 1);
          console.info('[ISL Content Script] Discarded an unaccepted sign from an expired cue:', pending.eventId);
        }
      }
      for (const [eventId, entry] of inFlightAetherCommands) {
        if (isSignCommand(entry.payload) && !belongsToCue(entry.payload)) {
          clearTimeout(entry.timer);
          inFlightAetherCommands.delete(eventId);
        }
      }
    }
    const iframe = ui?.elements?.aetherIframe;
    if (!iframe || !iframe.src || iframe.src === 'about:blank' || !iframe.contentWindow) {
      queueAetherCommand(payload);
      return;
    }
    let origin;
    try {
      origin = new URL(iframe.src).origin;
    } catch (error) {
      showAetherDeliveryFailure(payload, `invalid viewer URL: ${error.message}`);
      return;
    }
    if (payload.eventId) {
      if (inFlightAetherCommands.has(payload.eventId)) return;
      if (inFlightAetherCommands.size >= MAX_IN_FLIGHT_AETHER_COMMANDS) {
        queueAetherCommand(payload);
        return;
      }
      const entry = { payload, attempts: 0, timer: null };
      inFlightAetherCommands.set(payload.eventId, entry);
      postAetherCommand(payload, iframe, origin);
      return;
    }
    postAetherCommand(payload, iframe, origin);
  }

  function flushAetherCommands() {
    const iframe = ui?.elements?.aetherIframe;
    if (!iframe || !iframe.src || iframe.src === 'about:blank' || !iframe.contentWindow) return;
    while (pendingAetherCommands.length) {
      const next = pendingAetherCommands[0];
      if (next.eventId && inFlightAetherCommands.size >= MAX_IN_FLIGHT_AETHER_COMMANDS) return;
      pendingAetherCommands.shift();
      forwardAetherCommand(next);
    }
  }

  function handleAetherAck(event, iframe, expectedOrigin) {
    const data = event.data;
    if (event.source !== iframe.contentWindow || event.origin !== expectedOrigin) return false;
    if (data?.type === 'ISL_AETHER_LIFECYCLE') {
      console.info('[ISL Content Script] Aether playback lifecycle:', data.event);
      return true;
    }
    if (data?.type !== 'ISL_AETHER_ACK' || typeof data.eventId !== 'string') return false;
    const entry = inFlightAetherCommands.get(data.eventId);
    if (!entry) return true;
    if (data.status === 'retry' && entry.attempts < MAX_AETHER_DELIVERY_ATTEMPTS) {
      clearTimeout(entry.timer);
      entry.timer = setTimeout(() => {
        if (inFlightAetherCommands.has(data.eventId)) {
          postAetherCommand(entry.payload, iframe, expectedOrigin, entry.attempts + 1);
        }
      }, 300);
      return true;
    }
    clearTimeout(entry.timer);
    inFlightAetherCommands.delete(data.eventId);
    if (data.status === 'accepted') {
      deliveredOccurrenceIds.add(data.eventId);
      if (deliveredOccurrenceIds.size > 5000) {
        deliveredOccurrenceIds.delete(deliveredOccurrenceIds.values().next().value);
      }
    } else {
      showAetherDeliveryFailure(entry.payload, data.reason || 'Aether rejected the command');
    }
    flushAetherCommands();
    return true;
  }

  function bindAetherFrame() {
    const iframe = ui?.elements?.aetherIframe;
    if (iframe && !iframe.__islLoadBound) {
      iframe.__islLoadBound = true;
      iframe.addEventListener('load', flushAetherCommands);
    }
  }

  async function requestCueManifest(payload = {}) {
    const videoId = getCurrentVideoId();
    if (!videoId || payload.video_id !== videoId || !payload.job_id) return;
    if (activeCueJobId && activeCueJobId !== payload.job_id) return;
    const requestKey = `${payload.job_id}:${videoId}`;
    if (requestedCueJobs.has(requestKey)) return requestedCueJobs.get(requestKey);
    const request = (async () => {
      let response;
      let lastError;
      for (const delay of [0, 500, 1500]) {
        if (delay) await sleep(delay);
        if (getCurrentVideoId() !== videoId
          || (activeCueJobId && activeCueJobId !== payload.job_id)) return;
        try {
          response = await sendRuntimeMessage(contract.createMessage(
            contract.MESSAGE_TYPES.GET_YOUTUBE_CUES,
            { job_id: payload.job_id, video_id: videoId }
          ));
          if (response?.success) break;
          lastError = new Error(response?.error || 'The timestamped translation is unavailable.');
        } catch (error) {
          lastError = error;
        }
      }
      if (!response?.success) throw lastError || new Error('Unable to retrieve timestamped translation cues.');
      const manifest = response.payload;
      if (response.protocol_version !== 1 || response.job_id !== payload.job_id
        || response.video_id !== videoId || response.fingerprint !== payload.fingerprint
        || manifest?.job_id !== payload.job_id || manifest?.video_id !== videoId
        || manifest?.fingerprint !== payload.fingerprint || !manifest.playback_ready) {
        throw new Error('The timestamped cue manifest failed identity or integrity validation.');
      }
      if (getCurrentVideoId() !== videoId
        || (activeCueJobId && activeCueJobId !== payload.job_id)) return;
      const sync = ensureSynchronizer();
      if (!sync) throw new Error('YouTube timeline synchronization is unavailable.');
      if (sync.manifestFingerprint === manifest.fingerprint
        && sync.videoId === videoId && sync.activeJobId === payload.job_id) {
        acknowledgeCueManifest(payload.job_id, videoId, manifest.fingerprint);
        return;
      }
      sync.setCueManifest(manifest, videoId);
      currentVideoId = videoId;
      activeCueJobId = payload.job_id;
      deliveredOccurrenceIds.clear();
      acknowledgeCueManifest(payload.job_id, videoId, manifest.fingerprint);
    })().catch(async error => {
      if (getCurrentVideoId() === videoId
        && (!activeCueJobId || activeCueJobId === payload.job_id)) {
        forwardAetherCommand({ command: contract.AETHER_COMMANDS.RESET_AVATAR });
        ui?.setUnavailableFallback(`Video translation unavailable: ${error.message}`, 0);
        try {
          await sendRuntimeMessage(contract.createMessage(contract.MESSAGE_TYPES.YOUTUBE_CUES_ERROR, {
            job_id: payload.job_id,
            video_id: videoId,
            error: error.message
          }));
        } catch (reportError) {
          console.warn('[ISL Content Script] Unable to report cue error:', reportError.message);
        }
      }
      console.warn('[ISL Content Script] Unable to apply timestamped cues:', error.message);
      throw error;
    }).finally(() => requestedCueJobs.delete(requestKey));
    requestedCueJobs.set(requestKey, request);
    return request;
  }

  function notifyPageReady() {
    const videoId = getCurrentVideoId();
    if (!videoId) return;
    sendRuntimeMessage(contract.createMessage(contract.MESSAGE_TYPES.YOUTUBE_PAGE_READY, {
      protocol_version: 1,
      video_id: videoId
    })).then(response => {
      if (response?.success && response.job_id && response.video_id === getCurrentVideoId()) {
        activeCueJobId = response.job_id;
      }
    }).catch(error => {
      console.debug('[ISL Content Script] Unable to register YouTube page:', error.message);
    });
  }

  window.addEventListener('message', event => {
    const iframe = ui?.elements?.aetherIframe;
    if (!iframe || !iframe.src || iframe.src === 'about:blank') return;
    let expectedOrigin;
    try {
      expectedOrigin = new URL(iframe.src).origin;
    } catch {
      return;
    }
    if (handleAetherAck(event, iframe, expectedOrigin)) return;
    if (event.source !== iframe.contentWindow || event.origin !== expectedOrigin
      || event.data?.type !== 'ISL_AETHER_STATE') return;
    chrome.runtime.sendMessage(contract.createMessage(
      contract.MESSAGE_TYPES.AETHER_PLAYBACK_STATE,
      event.data.state || {}
    ), response => {
      if (chrome.runtime.lastError) console.warn('[ISL Content Script] Aether state relay failed:', chrome.runtime.lastError.message);
      else if (!response?.success) console.warn('[ISL Content Script] Aether state relay was rejected.');
    });
  });

  // Listen for messages from service worker
  if (typeof chrome !== 'undefined' && chrome.runtime?.onMessage) {
    chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
      if (!message || !message.type) return;

      if (message.type === contract.MESSAGE_TYPES.STATE_UPDATE && message.payload) {
        bindAetherFrame();
        if (ui) ui.update(message.payload);
        sendResponse({ received: true });
        return true;
      }

      if (message.type === contract.MESSAGE_TYPES.YOUTUBE_CUES_READY && message.payload) {
        const videoId = getCurrentVideoId();
        if (!videoId || message.payload.video_id !== videoId || !message.payload.job_id
          || !message.payload.fingerprint) {
          sendResponse({ received: false });
          return true;
        }
        sendResponse({ received: true });
        requestCueManifest(message.payload).catch(() => {});
        return true;
      }

      if (message.type === contract.MESSAGE_TYPES.YOUTUBE_JOB_CREATED && message.payload) {
        if (message.payload.video_id === getCurrentVideoId()) {
          activeCueJobId = message.payload.job_id || null;
          if (synchronizer) synchronizer.setSegments([], activeCueJobId);
          forwardAetherCommand({ command: contract.AETHER_COMMANDS.RESET_AVATAR });
          ui?.setUnavailableFallback('Video translation is processing; sign playback is paused.', 0);
        }
        sendResponse({ received: true });
        return true;
      }

      if (message.type === contract.MESSAGE_TYPES.AETHER_COMMAND && message.payload) {
        forwardAetherCommand(message.payload);
        sendResponse({ received: true });
        return true;
      }

      if (message.type === contract.MESSAGE_TYPES.UNAVAILABLE_FALLBACK && message.payload) {
        forwardAetherCommand({ command: contract.AETHER_COMMANDS.RESET_AVATAR });
        if (ui) ui.setUnavailableFallback(message.payload.originalWord || message.payload.text || message.payload.word);
        sendResponse({ received: true });
        return true;
      }

      if (message.type === contract.MESSAGE_TYPES.TOGGLE_OVERLAY) {
        if (ui) {
          if (ui.isVisible) ui.hide();
          else ui.show();
        }
        sendResponse({ success: true });
        return true;
      }
    });
  }

  // YouTube SPA navigation resilience (yt-navigate-finish / popstate)
  function handleNavigation() {
    const nextVideoId = getCurrentVideoId();
    if (nextVideoId !== currentVideoId) {
      currentVideoId = nextVideoId;
      activeCueJobId = null;
      requestedCueJobs.clear();
      deliveredOccurrenceIds.clear();
      if (synchronizer) synchronizer.setSegments([], null);
      if (ui) ui.setUnavailableFallback(null);
    }
    if (!document.getElementById('isl-accessibility-overlay-root')) {
      if (synchronizer) {
        synchronizer.detach();
        synchronizer = null;
      }
      if (ui) {
        ui.destroy();
        ui = null;
      }
      initializeOverlay();
    }
    if (synchronizer) synchronizer.rebind(getVideoElement());
    notifyPageReady();
  }

  window.addEventListener('yt-navigate-finish', handleNavigation);
  window.addEventListener('popstate', handleNavigation);

  // Initialize once DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeOverlay);
  } else {
    initializeOverlay();
  }
  notifyPageReady();

  // Clean teardown helper
  window.__ISL_EXTENSION_CLEANUP__ = function () {
    if (ui) {
      ui.destroy();
      ui = null;
    }
    window.removeEventListener('yt-navigate-finish', handleNavigation);
    window.removeEventListener('popstate', handleNavigation);
    videoElementObserver?.disconnect();
    videoElementObserver = null;
    if (synchronizer) {
      synchronizer.detach();
      synchronizer = null;
    }
    delete window.__ISL_EXTENSION_INJECTED__;
  };
})();
