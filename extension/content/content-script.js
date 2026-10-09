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

  let ui = null;
  const pendingAetherCommands = [];

  function initializeOverlay() {
    if (ui) return;

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

  function forwardAetherCommand(payload = {}) {
    const iframe = ui?.elements?.aetherIframe;
    if (!iframe || !iframe.src || iframe.src === 'about:blank') {
      pendingAetherCommands.push(payload);
      return;
    }
    const command = payload.command;
    if (!Object.values(contract.AETHER_COMMANDS).includes(command)) return;
    if (!iframe.contentWindow) {
      pendingAetherCommands.push(payload);
      return;
    }
    try {
      iframe.contentWindow.postMessage({
        type: 'ISL_AETHER_COMMAND',
        command,
        signId: payload.signId
      }, new URL(iframe.src).origin);
    } catch (error) {
      console.warn('[ISL Content Script] Unable to forward Aether command:', error.message);
    }

    function flushAetherCommands() {
      while (pendingAetherCommands.length) {
        const next = pendingAetherCommands.shift();
        forwardAetherCommand(next);
      }
    }
  }

  window.addEventListener('message', event => {
    const iframe = ui?.elements?.aetherIframe;
    if (!iframe || event.source !== iframe.contentWindow || event.data?.type !== 'ISL_AETHER_STATE') return;
    let expectedOrigin;
    try {
      expectedOrigin = new URL(iframe.src).origin;
    } catch {
      return;
    }
    if (event.origin !== expectedOrigin) return;
    chrome.runtime.sendMessage(contract.createMessage(
      contract.MESSAGE_TYPES.AETHER_PLAYBACK_STATE,
      event.data.state || {}
    ), response => {
      if (chrome.runtime.lastError) console.warn('[ISL Content Script] Aether state relay failed:', chrome.runtime.lastError.message);
      else if (!response?.success) console.warn('[ISL Content Script] Aether state relay was rejected.');
    });

    function bindAetherFrame() {
      const iframe = ui?.elements?.aetherIframe;
      if (iframe && !iframe.__islLoadBound) {
        iframe.__islLoadBound = true;
        iframe.addEventListener('load', flushAetherCommands);
      }
    }
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

      if (message.type === contract.MESSAGE_TYPES.AETHER_COMMAND && message.payload) {
        forwardAetherCommand(message.payload);
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
    if (!document.getElementById('isl-accessibility-overlay-root')) {
      if (ui) {
        ui.destroy();
        ui = null;
      }
      initializeOverlay();
    }
  }

  window.addEventListener('yt-navigate-finish', handleNavigation);
  window.addEventListener('popstate', handleNavigation);

  // Initialize once DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeOverlay);
  } else {
    initializeOverlay();
  }

  // Clean teardown helper
  window.__ISL_EXTENSION_CLEANUP__ = function () {
    if (ui) {
      ui.destroy();
      ui = null;
    }
    window.removeEventListener('yt-navigate-finish', handleNavigation);
    window.removeEventListener('popstate', handleNavigation);
    delete window.__ISL_EXTENSION_INJECTED__;
  };
})();
