/**
 * ISL Accessibility Translator - Service Worker (Phase H6)
 * Manifest V3 Background Coordinator
 */

try {
  importScripts(
    '../shared/message-contract.js',
    '../shared/demo-data.js',
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
      broadcastYouTubeEvent(self.ISLMessageContract.MESSAGE_TYPES.YOUTUBE_RESULT, state.youtube);
      dispatchPlayableSigns(state.youtube);
    } else if (state.youtube?.state === 'ERROR') {
      broadcastYouTubeEvent(self.ISLMessageContract.MESSAGE_TYPES.YOUTUBE_ERROR, {
        job_id: state.youtube.jobId,
        error: state.youtube.error
      });
    }
  }
});

let activeYoutubeTabId = null;
const dispatchedYoutubeJobs = new Set();

function broadcastYouTubeEvent(type, payload) {
  const message = self.ISLMessageContract.createMessage(type, payload || {});
  if (typeof chrome !== 'undefined' && chrome.runtime?.sendMessage) {
    chrome.runtime.sendMessage(message, () => {
      if (chrome.runtime.lastError) { /* No popup is currently open. */ }
    });
  }
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

function dispatchPlayableSigns(youtube) {
  if (!youtube?.jobId || !youtube.resultReady || dispatchedYoutubeJobs.has(youtube.jobId)) return;
  const signs = Array.isArray(youtube.playableSigns) ? youtube.playableSigns : [];
  dispatchedYoutubeJobs.add(youtube.jobId);
  if (!signs.length) return;

  const sendToTab = (tabId) => {
    if (!tabId) return;
    const commandFor = (command, signId) => self.ISLMessageContract.createMessage(
      self.ISLMessageContract.MESSAGE_TYPES.AETHER_COMMAND,
      { command, signId, source: 'youtube', jobId: youtube.jobId }
    );
    chrome.tabs.sendMessage(tabId, commandFor('PLAY_SIGN', signs[0]), () => {
      if (chrome.runtime.lastError) console.warn('[ISL Service Worker] Aether command could not reach active tab:', chrome.runtime.lastError.message);
    });
    signs.slice(1).forEach(signId => {
      chrome.tabs.sendMessage(tabId, commandFor('QUEUE_SIGN', signId), () => {
        if (chrome.runtime.lastError) console.warn('[ISL Service Worker] Aether queue command failed:', chrome.runtime.lastError.message);
      });
    });
  };

  if (activeYoutubeTabId) {
    sendToTab(activeYoutubeTabId);
    return;
  }
  chrome.tabs.query({ active: true, lastFocusedWindow: true }, tabs => {
    if (chrome.runtime.lastError) {
      console.warn('[ISL Service Worker] Unable to find active tab for Aether playback:', chrome.runtime.lastError.message);
      return;
    }
    sendToTab(tabs?.[0]?.id);
  });
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
        chrome.tabs.query({ active: true, lastFocusedWindow: true }, tabs => {
          activeYoutubeTabId = tabs?.[0]?.id || null;
          bridge.submitYouTube(message.payload.url).then((job) => {
            sendResponse({ success: true, payload: job });
            broadcastYouTubeEvent(MESSAGE_TYPES.YOUTUBE_JOB_CREATED, job);
          }).catch(error => {
            bridge.setYouTubeError(error);
            broadcastYouTubeEvent(MESSAGE_TYPES.YOUTUBE_ERROR, { error: error.message });
            sendResponse({ success: false, error: error.message });
          });
        });
        return true;

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
