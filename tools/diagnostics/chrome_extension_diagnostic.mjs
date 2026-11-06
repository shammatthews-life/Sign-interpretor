#!/usr/bin/env node

import { execFileSync } from 'node:child_process';
import { existsSync, readdirSync, readFileSync, statSync } from 'node:fs';
import path from 'node:path';
import process from 'node:process';
import { fileURLToPath, pathToFileURL } from 'node:url';

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const projectRoot = path.resolve(scriptDir, '..', '..');

function parseArguments(argv) {
  const options = {
    extensionDir: path.join(projectRoot, 'extension'),
    debuggingUrl: process.env.CHROME_REMOTE_DEBUGGING_URL || 'http://127.0.0.1:9222',
    output: null
  };
  for (let index = 0; index < argv.length; index += 1) {
    const argument = argv[index];
    if (argument === '--extension-dir') options.extensionDir = argv[++index];
    else if (argument === '--debugging-url') options.debuggingUrl = argv[++index];
    else if (argument === '--output') options.output = argv[++index];
    else if (argument === '--help') {
      console.log('Usage: node tools/diagnostics/chrome_extension_diagnostic.mjs [--extension-dir PATH] [--debugging-url URL] [--output PATH]');
      process.exit(0);
    } else {
      throw new Error(`Unknown argument: ${argument}`);
    }
  }
  return options;
}

function findChromeExecutable() {
  const candidates = [
    process.env.CHROME_PATH,
    process.env.PROGRAMFILES && path.join(process.env.PROGRAMFILES, 'Google', 'Chrome', 'Application', 'chrome.exe'),
    process.env['PROGRAMFILES(X86)'] && path.join(process.env['PROGRAMFILES(X86)'], 'Google', 'Chrome', 'Application', 'chrome.exe'),
    process.env.LOCALAPPDATA && path.join(process.env.LOCALAPPDATA, 'Google', 'Chrome', 'Application', 'chrome.exe'),
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    '/usr/bin/google-chrome',
    '/usr/bin/chromium',
    '/usr/bin/chromium-browser'
  ].filter(Boolean);
  return candidates.find(candidate => existsSync(candidate)) || null;
}

function chromeFileVersion(executable) {
  if (!executable || process.platform !== 'win32') return null;
  const escapedPath = executable.replaceAll("'", "''");
  try {
    return execFileSync('powershell.exe', [
      '-NoProfile',
      '-NonInteractive',
      '-Command',
      `(Get-Item -LiteralPath '${escapedPath}').VersionInfo.ProductVersion`
    ], { encoding: 'utf8', timeout: 5000, windowsHide: true }).trim() || null;
  } catch {
    return null;
  }
}

function listFiles(root, relative = '') {
  const directory = path.join(root, relative);
  if (!existsSync(directory) || !statSync(directory).isDirectory()) return [];
  return readdirSync(directory, { withFileTypes: true }).flatMap(entry => {
    const child = path.join(relative, entry.name);
    return entry.isDirectory() ? listFiles(root, child) : [child.split(path.sep).join('/')];
  });
}

function resolveExtensionPath(root, relative) {
  const normalized = relative.replaceAll('\\', '/');
  if (normalized.startsWith('/') || /^[a-z][a-z0-9+.-]*:/i.test(normalized)) return null;
  const resolved = path.resolve(root, normalized);
  return resolved === root || resolved.startsWith(`${root}${path.sep}`) ? resolved : null;
}

function globToRegExp(pattern) {
  const escaped = pattern.replace(/[.+^${}()|[\]\\]/g, '\\$&')
    .replaceAll('**', '\u0000')
    .replaceAll('*', '[^/]*')
    .replaceAll('\u0000', '.*');
  return new RegExp(`^${escaped}$`);
}

export function validMatchPattern(pattern) {
  if (typeof pattern !== 'string') return false;
  const match = pattern.match(/^(\*|https?|file|ftp|urn):\/\/([^/]+)(\/.*)$/);
  if (!match) return false;
  const [, scheme, host] = match;
  if (host.includes(':')) return false;
  if (scheme === '*' && host === '*') return true;
  if (scheme === 'file') return host === '';
  if (host === '*') return scheme === 'http' || scheme === 'https' || scheme === '*';
  return /^[a-z0-9*.-]+$/i.test(host)
    && !host.startsWith('.')
    && !host.endsWith('.')
    && !host.includes('**');
}

export function inspectManifest(extensionDir) {
  const result = {
    directory: extensionDir,
    directoryExists: existsSync(extensionDir) && statSync(extensionDir).isDirectory(),
    manifestExists: false,
    manifestValidJson: false,
    manifestVersion: null,
    name: null,
    backgroundServiceWorker: null,
    popupPage: null,
    permissions: [],
    hostPermissions: [],
    contentScriptMatches: [],
    contentScriptResources: [],
    staticReferencedResources: [],
    webAccessibleResources: [],
    invalidMatchPatterns: [],
    missingResources: [],
    pathTraversalResources: [],
    csp: null
  };
  if (!result.directoryExists) return result;

  const manifestPath = path.join(extensionDir, 'manifest.json');
  result.manifestExists = existsSync(manifestPath);
  if (!result.manifestExists) return result;

  let manifest;
  try {
    manifest = JSON.parse(readFileSync(manifestPath, 'utf8'));
    result.manifestValidJson = true;
  } catch (error) {
    result.manifestError = error.message;
    return result;
  }

  result.manifestVersion = manifest.manifest_version ?? null;
  result.name = manifest.name ?? null;
  result.backgroundServiceWorker = manifest.background?.service_worker ?? null;
  result.popupPage = manifest.action?.default_popup || manifest.options_ui?.page || manifest.options_page || null;
  result.permissions = Array.isArray(manifest.permissions) ? manifest.permissions : [];
  result.hostPermissions = Array.isArray(manifest.host_permissions) ? manifest.host_permissions : [];
  result.csp = manifest.content_security_policy ?? null;

  const references = [];
  const addReference = (resource, kind) => {
    if (typeof resource === 'string') references.push({ resource, kind });
  };
  addReference(manifest.background?.service_worker, 'background.service_worker');
  addReference(manifest.action?.default_popup, 'action.default_popup');
  for (const [size, resource] of Object.entries(manifest.icons || {})) {
    addReference(resource, `icons.${size}`);
  }
  for (const script of manifest.content_scripts || []) {
    const matches = Array.isArray(script.matches) ? script.matches : [];
    result.contentScriptMatches.push(...matches);
    for (const pattern of matches) {
      if (!validMatchPattern(pattern)) result.invalidMatchPatterns.push({ surface: 'content_scripts.matches', pattern });
    }
    for (const resource of script.js || []) {
      result.contentScriptResources.push(resource);
      addReference(resource, 'content_scripts.js');
    }
    for (const resource of script.css || []) addReference(resource, 'content_scripts.css');
  }
  for (const pattern of result.hostPermissions) {
    if (!validMatchPattern(pattern)) result.invalidMatchPatterns.push({ surface: 'host_permissions', pattern });
  }

  const files = listFiles(extensionDir);
  for (const { resource, kind } of references) {
    const resolved = resolveExtensionPath(extensionDir, resource);
    if (!resolved) {
      result.pathTraversalResources.push({ resource, kind });
      continue;
    }
    result.staticReferencedResources.push({ resource, kind, exists: existsSync(resolved) });
    if (!existsSync(resolved)) result.missingResources.push({ resource, kind });
  }

  for (const group of manifest.web_accessible_resources || []) {
    for (const pattern of group.resources || []) {
      const regex = globToRegExp(pattern);
      const matches = files.filter(file => regex.test(file));
      result.webAccessibleResources.push({ pattern, matches: matches.length, matchExamples: matches.slice(0, 3) });
      if (!matches.length) result.missingResources.push({ resource: pattern, kind: 'web_accessible_resources' });
    }
    for (const pattern of group.matches || []) {
      if (!validMatchPattern(pattern)) result.invalidMatchPatterns.push({ surface: 'web_accessible_resources.matches', pattern });
    }
  }

  const importedResources = new Set();
  for (const file of files) {
    if (!/\.(?:js|html|css)$/i.test(file)) continue;
    const content = readFileSync(path.join(extensionDir, file), 'utf8');
    const imports = file.endsWith('.js')
      ? [...content.matchAll(/\bimportScripts\s*\(([^)]*)\)/gs)]
        .flatMap(match => [...match[1].matchAll(/['"]([^'"]+)['"]/g)].map(item => item[1]))
      : [];
    for (const imported of imports) {
      const resolved = path.resolve(extensionDir, path.dirname(file), imported);
      const safe = resolved.startsWith(`${extensionDir}${path.sep}`);
      const relative = path.relative(extensionDir, resolved).split(path.sep).join('/');
      importedResources.add(relative);
      if (!safe) result.pathTraversalResources.push({ resource: imported, kind: `${file} importScripts` });
      else if (!existsSync(resolved)) result.missingResources.push({ resource: relative, kind: `${file} importScripts` });
    }

    if (file.endsWith('.html')) {
      for (const match of content.matchAll(/(?:src|href)\s*=\s*["']([^"']+)["']/gi)) {
        const resource = match[1];
        if (/^(?:[a-z]+:|#|\/\/)/i.test(resource)) continue;
        const resolved = path.resolve(extensionDir, path.dirname(file), resource.split(/[?#]/, 1)[0]);
        const safe = resolved.startsWith(`${extensionDir}${path.sep}`);
        const relative = path.relative(extensionDir, resolved).split(path.sep).join('/');
        if (!safe) result.pathTraversalResources.push({ resource, kind: `${file} href/src` });
        else if (!existsSync(resolved)) result.missingResources.push({ resource: relative, kind: `${file} href/src` });
      }
    }
  }

  result.importScriptsResources = [...importedResources];
  result.manifestStructurallyValid = result.manifestVersion === 3
    && typeof result.name === 'string'
    && typeof result.backgroundServiceWorker === 'string'
    && result.missingResources.length === 0
    && result.pathTraversalResources.length === 0
    && result.invalidMatchPatterns.length === 0;
  return result;
}

class CdpConnection {
  constructor(socket) {
    this.socket = socket;
    this.nextId = 0;
    this.pending = new Map();
    socket.addEventListener('message', event => {
      const message = JSON.parse(event.data);
      if (!message.id || !this.pending.has(message.id)) return;
      const pending = this.pending.get(message.id);
      this.pending.delete(message.id);
      if (message.error) pending.reject(new Error(message.error.message));
      else pending.resolve(message.result);
    });
  }

  static async connect(url) {
    const socket = new WebSocket(url);
    await new Promise((resolve, reject) => {
      socket.addEventListener('open', resolve, { once: true });
      socket.addEventListener('error', () => reject(new Error('Could not connect to Chrome DevTools Protocol.')), { once: true });
    });
    return new CdpConnection(socket);
  }

  send(method, params = {}) {
    const id = ++this.nextId;
    return new Promise((resolve, reject) => {
      const timer = setTimeout(() => {
        this.pending.delete(id);
        reject(new Error(`Chrome DevTools Protocol timed out: ${method}`));
      }, 5000);
      this.pending.set(id, {
        resolve: value => { clearTimeout(timer); resolve(value); },
        reject: error => { clearTimeout(timer); reject(error); }
      });
      this.socket.send(JSON.stringify({ id, method, params }));
    });
  }

  close() {
    this.socket.close();
  }
}

export function summarizeServiceWorkerState({ registrations, workerTargets, extensionId, workerPath }) {
  const expectedScriptUrl = new URL(workerPath, `chrome-extension://${extensionId}/`).href;
  const expectedScope = `chrome-extension://${extensionId}/`;
  return {
    serviceWorkerTargetObserved: workerTargets.some(target => {
      try {
        return new URL(target.url).href === expectedScriptUrl;
      } catch {
        return false;
      }
    }),
    serviceWorkerRegistered: registrations === null
      ? null
      : registrations.some(registration =>
        registration.scope === expectedScope && registration.activeScriptUrl === expectedScriptUrl
      )
  };
}

export function isExtensionInstalled(registryItems, expectedName) {
  return registryItems.some(item => item.name === expectedName && Boolean(item.id) && item.enabled === true);
}

async function evaluateTarget(target, expression) {
  const connection = await CdpConnection.connect(target.webSocketDebuggerUrl);
  try {
    await connection.send('Runtime.enable');
    const response = await connection.send('Runtime.evaluate', {
      expression,
      awaitPromise: true,
      returnByValue: true
    });
    return response.result?.value ?? null;
  } finally {
    connection.close();
  }
}

async function inspectChrome(debuggingUrl, manifest) {
  const browser = {
    debuggingEndpoint: debuggingUrl,
    reachable: false,
    version: null,
    userAgent: null,
    targets: [],
    extensionId: null,
    installed: false,
    sourcePath: null,
    sourcePathMatches: null,
    installLocation: null,
    registryStatus: null,
    serviceWorkerRegistered: null,
    serviceWorkerTargetObserved: false,
    serviceWorkerRegistrations: [],
    serviceWorkerTargets: [],
    extensionRegistryItems: [],
    loadingErrors: [],
    youtubeTabs: [],
    contentScriptExecutions: [],
    inspectionErrors: []
  };

  let version;
  try {
    const response = await fetch(new URL('/json/version', debuggingUrl));
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    version = await response.json();
    browser.reachable = true;
    browser.version = version.Browser || null;
    browser.userAgent = version['User-Agent'] || null;
  } catch (error) {
    browser.inspectionErrors.push(`Chrome debugging endpoint unavailable: ${error.message}`);
    return browser;
  }

  let connection;
  try {
    connection = await CdpConnection.connect(version.webSocketDebuggerUrl);
    const targets = await connection.send('Target.getTargets');
    const listedTargets = await fetch(new URL('/json/list', debuggingUrl)).then(response => {
      if (!response.ok) throw new Error(`Chrome target list returned HTTP ${response.status}`);
      return response.json();
    });
    const targetDetails = new Map(listedTargets.map(target => [target.id, target]));
    const targetInfos = (targets.targetInfos || []).map(target => ({
      ...target,
      webSocketDebuggerUrl: targetDetails.get(target.targetId)?.webSocketDebuggerUrl
    }));
    browser.targets = targetInfos.map(target => ({
      id: target.targetId,
      type: target.type,
      title: target.title,
      url: target.url
    }));

    const workerTargets = targetInfos.filter(target =>
      target.type === 'service_worker'
      && /^chrome-extension:\/\/[a-p]{32}\/background\/service-worker\.js(?:[?#].*)?$/i.test(target.url)
    );

    let extensionsPage = targetInfos.find(target =>
      target.type === 'page' && target.url.startsWith('chrome://extensions')
    );
    if (!extensionsPage) {
      const created = await connection.send('Target.createTarget', { url: 'chrome://extensions/' });
      await new Promise(resolve => setTimeout(resolve, 300));
      const refreshed = await fetch(new URL('/json/list', debuggingUrl)).then(response => response.json());
      extensionsPage = refreshed.find(target => target.id === created.targetId);
      if (extensionsPage) extensionsPage.targetId = extensionsPage.id;
    }
    if (extensionsPage?.webSocketDebuggerUrl) {
      const registry = await evaluateTarget(extensionsPage, `(() => {
        const found = [];
        const visit = root => {
          if (!root || !root.querySelectorAll) return;
          for (const element of root.querySelectorAll('*')) {
            if (element.localName === 'extensions-item') {
              const data = element.data || {};
              const errors = Array.isArray(data.errors) ? data.errors.map(error => ({
                message: error.message || error,
                source: error.source || null,
                type: error.type || null
              })) : [];
              found.push({
                id: data.id || element.id || null,
                name: data.name || null,
                version: data.version || null,
                enabled: data.state === 'ENABLED' || data.enabled === true,
                state: data.state || null,
                errors,
                text: (element.shadowRoot?.textContent || element.textContent || '').trim().slice(0, 2000)
              });
            }
            if (element.shadowRoot) visit(element.shadowRoot);
          }
        };
        visit(document);
        const manager = document.querySelector('extensions-manager');
        return {
          items: found,
          managerPresent: Boolean(manager),
          pageText: (document.body?.innerText || '').slice(0, 3000)
        };
      })()`);
      browser.extensionRegistryItems = registry?.items || [];
      const matching = browser.extensionRegistryItems.find(item => item.name === manifest.name);
      if (matching?.id) browser.extensionId = matching.id;
      browser.installed = isExtensionInstalled(browser.extensionRegistryItems, manifest.name);
      browser.loadingErrors = browser.extensionRegistryItems
        .filter(item => item.name === manifest.name || item.errors?.length)
        .flatMap(item => item.errors.map(error => ({
          extensionId: item.id,
          name: item.name,
          message: String(error.message)
        })));
    }

    if (browser.extensionId && manifest.backgroundServiceWorker) {
      const expectedWorkerUrl = new URL(manifest.backgroundServiceWorker, `chrome-extension://${browser.extensionId}/`).href;
      browser.serviceWorkerTargets = workerTargets
        .filter(target => {
          try {
            return new URL(target.url).href === expectedWorkerUrl;
          } catch {
            return false;
          }
        })
        .map(target => ({ id: target.targetId, url: target.url, extensionId: browser.extensionId }));
      const workerState = summarizeServiceWorkerState({
        registrations: null,
        workerTargets: browser.serviceWorkerTargets,
        extensionId: browser.extensionId,
        workerPath: manifest.backgroundServiceWorker
      });
      browser.serviceWorkerTargetObserved = workerState.serviceWorkerTargetObserved;

      const internalsExpression = `(() => {
        try {
          const records = JSON.parse(document.body.innerText);
          const extension = records.find(record => record.id === ${JSON.stringify(browser.extensionId)});
          return extension ? {
            path: extension.path || null,
            location: extension.location || null,
            registryStatus: extension.registry_status || null
          } : null;
        } catch {
          return null;
        }
      })()`;
      try {
        const internals = await evaluateTemporaryTarget(
          connection,
          debuggingUrl,
          'chrome://extensions-internals/',
          internalsExpression
        );
        if (internals) {
          browser.sourcePath = internals.path;
          browser.sourcePathMatches = Boolean(internals.path)
            && path.resolve(internals.path) === path.resolve(manifest.directory);
          browser.installLocation = internals.location;
          browser.registryStatus = internals.registryStatus;
        }
      } catch (error) {
        browser.inspectionErrors.push(`Unable to inspect Chrome's extension registry details: ${error.message}`);
      }

      const registrationExpression = `navigator.serviceWorker
        ? navigator.serviceWorker.getRegistrations().then(registrations => registrations.map(registration => ({
          scope: registration.scope,
          activeScriptUrl: registration.active?.scriptURL || null
        })))
        : null`;
      if (manifest.popupPage) {
        try {
          const registrations = await evaluateTemporaryTarget(
            connection,
            debuggingUrl,
            `chrome-extension://${browser.extensionId}/${manifest.popupPage}`,
            registrationExpression
          );
          browser.serviceWorkerRegistrations = Array.isArray(registrations) ? registrations : [];
          const workerState = summarizeServiceWorkerState({
            registrations: Array.isArray(registrations) ? registrations : null,
            workerTargets: browser.serviceWorkerTargets,
            extensionId: browser.extensionId,
            workerPath: manifest.backgroundServiceWorker
          });
          browser.serviceWorkerRegistered = workerState.serviceWorkerRegistered;
          browser.serviceWorkerTargetObserved = workerState.serviceWorkerTargetObserved;
        } catch (error) {
          browser.inspectionErrors.push(`Unable to confirm service-worker registration: ${error.message}`);
        }
      } else {
        browser.inspectionErrors.push('Cannot confirm service-worker registration: no extension page is declared in the manifest.');
      }
    }

    const youtubeTargets = targetInfos.filter(target =>
      target.type === 'page' && /^https:\/\/(?:www\.)?youtube\.com\/watch(?:\?|$)/i.test(target.url)
    );
    browser.youtubeTabs = youtubeTargets.map(target => ({ id: target.targetId, url: target.url, title: target.title }));
    if (browser.extensionId) {
      for (const target of youtubeTargets) {
        try {
          const connectionToTab = await CdpConnection.connect(target.webSocketDebuggerUrl);
          const contexts = [];
          connectionToTab.socket.addEventListener('message', event => {
            const message = JSON.parse(event.data);
            if (message.method === 'Runtime.executionContextCreated') contexts.push(message.params.context);
          });
          await connectionToTab.send('Runtime.enable');
          await new Promise(resolve => setTimeout(resolve, 300));
          const isolatedContexts = contexts.filter(context =>
            context.auxData?.isDefault === false && context.origin === `chrome-extension://${browser.extensionId}`
          );
          const executions = [];
          for (const context of isolatedContexts) {
            const response = await connectionToTab.send('Runtime.evaluate', {
              expression: `(() => {
                const root = document.getElementById('isl-accessibility-overlay-root');
                const panel = root?.shadowRoot?.getElementById('isl-overlay-container');
                const bounds = panel?.getBoundingClientRect();
                const iframe = root?.shadowRoot?.getElementById('isl-aether-iframe');
                const video = document.querySelector('video.html5-main-video') || document.querySelector('video');
                return {
                  initialized: Boolean(window.__ISL_EXTENSION_INJECTED__),
                  cleanupRegistered: typeof window.__ISL_EXTENSION_CLEANUP__ === 'function',
                  overlayMounted: Boolean(root),
                  overlayVisible: Boolean(panel && bounds.width > 0 && bounds.height > 0 && getComputedStyle(panel).display !== 'none'),
                  overlayBounds: bounds ? { x: bounds.x, y: bounds.y, width: bounds.width, height: bounds.height } : null,
                  iframeUrl: iframe?.src || null,
                  iframeVisible: Boolean(iframe && !iframe.classList.contains('hidden')),
                  videoPresent: Boolean(video),
                  videoReadyState: video?.readyState ?? null,
                  videoPaused: video?.paused ?? null
                };
              })()`,
              contextId: context.id,
              returnByValue: true
            });
            const details = response.result?.value || {};
            executions.push({
              contextId: context.id,
              name: context.name || null,
              ...details
            });
          }
          browser.contentScriptExecutions.push({
            tabId: target.targetId,
            url: target.url,
            extensionId: browser.extensionId,
            contexts: executions,
            executed: executions.some(context => context.initialized)
          });
          connectionToTab.close();
        } catch (error) {
          browser.inspectionErrors.push(`Unable to inspect YouTube tab ${target.url}: ${error.message}`);
        }
      }
    }
  } catch (error) {
    browser.inspectionErrors.push(`Chrome inspection failed: ${error.message}`);
  } finally {
    connection?.close();
  }
  return browser;
}

async function evaluateTemporaryTarget(connection, debuggingUrl, url, expression) {
  const { targetId } = await connection.send('Target.createTarget', { url });
  try {
    for (let attempt = 0; attempt < 20; attempt += 1) {
      const response = await fetch(new URL('/json/list', debuggingUrl));
      if (!response.ok) throw new Error(`Chrome target list returned HTTP ${response.status}`);
      const targets = await response.json();
      const target = targets.find(item => item.id === targetId);
      if (target?.webSocketDebuggerUrl) return await evaluateTarget(target, expression);
      await new Promise(resolve => setTimeout(resolve, 100));
    }
    throw new Error(`Chrome did not expose a DevTools target for ${url}`);
  } finally {
    await connection.send('Target.closeTarget', { targetId });
  }
}

async function inspectBackend() {
  const backend = {
    endpoint: 'http://localhost:8000',
    reachable: false,
    asrStatus: null,
    errors: []
  };
  try {
    const response = await fetch(`${backend.endpoint}/asr/status`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: '{}',
      signal: AbortSignal.timeout(3000)
    });
    backend.reachable = response.ok;
    if (response.ok) backend.asrStatus = await response.json();
    else backend.errors.push(`POST /asr/status returned HTTP ${response.status}`);
  } catch (error) {
    backend.errors.push(error.message);
  }
  return backend;
}

async function main() {
  const options = parseArguments(process.argv.slice(2));
  const extensionDir = path.resolve(options.extensionDir);
  const manifest = inspectManifest(extensionDir);
  const chromeExecutable = findChromeExecutable();
  const [browser, backend] = await Promise.all([
    inspectChrome(options.debuggingUrl, manifest),
    inspectBackend()
  ]);
  const output = {
    generatedAt: new Date().toISOString(),
    chrome: {
      executable: chromeExecutable,
      executableExists: Boolean(chromeExecutable),
      executableVersion: chromeFileVersion(chromeExecutable),
      ...browser
    },
    extension: manifest,
    backend
  };
  const text = `${JSON.stringify(output, null, 2)}\n`;
  if (options.output) {
    const outputPath = path.resolve(options.output);
    await import('node:fs/promises').then(fs => fs.writeFile(outputPath, text, 'utf8'));
  }
  process.stdout.write(text);
}

if (process.argv[1] && import.meta.url === pathToFileURL(path.resolve(process.argv[1])).href) {
  main().catch(error => {
    console.error(JSON.stringify({ error: error.message }));
    process.exitCode = 2;
  });
}
