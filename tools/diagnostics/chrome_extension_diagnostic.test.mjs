import assert from 'node:assert/strict';
import { mkdtempSync, mkdirSync, rmSync, writeFileSync } from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import test from 'node:test';

import {
  inspectManifest,
  isExtensionInstalled,
  summarizeServiceWorkerState,
  validMatchPattern
} from './chrome_extension_diagnostic.mjs';

const temporaryDirectories = [];

function createExtensionFixture(manifest, files = {}) {
  const directory = mkdtempSync(path.join(os.tmpdir(), 'isl-chrome-diagnostic-'));
  temporaryDirectories.push(directory);
  writeFileSync(path.join(directory, 'manifest.json'), JSON.stringify(manifest), 'utf8');
  for (const [relativePath, contents] of Object.entries(files)) {
    const filePath = path.join(directory, relativePath);
    mkdirSync(path.dirname(filePath), { recursive: true });
    writeFileSync(filePath, contents, 'utf8');
  }
  return directory;
}

test.after(() => {
  for (const directory of temporaryDirectories) {
    rmSync(directory, { recursive: true, force: true });
  }
});

test('accepts port-independent localhost match patterns and rejects wildcard ports', () => {
  assert.equal(validMatchPattern('http://localhost/*'), true);
  assert.equal(validMatchPattern('http://127.0.0.1/*'), true);
  assert.equal(validMatchPattern('http://localhost:*/*'), false);
  assert.equal(validMatchPattern('https://*.youtube.com/*'), true);
});

test('validates manifest resources and rejects missing files and invalid match patterns', () => {
  const directory = createExtensionFixture({
    manifest_version: 3,
    name: 'Diagnostic fixture',
    background: { service_worker: 'background/service-worker.js' },
    action: { default_popup: 'popup.html' },
    icons: { 16: 'icon.png' },
    host_permissions: ['http://localhost:*/*'],
    content_scripts: [{
      matches: ['https://*.youtube.com/*'],
      js: ['content.js'],
      css: ['missing.css']
    }],
    web_accessible_resources: [{
      resources: ['assets/*'],
      matches: ['https://*.youtube.com/*']
    }]
  }, {
    'background/service-worker.js': '',
    'popup.html': '',
    'icon.png': '',
    'content.js': '',
    'assets/avatar.bin': ''
  });

  const manifest = inspectManifest(directory);
  assert.equal(manifest.manifestValidJson, true);
  assert.equal(manifest.popupPage, 'popup.html');
  assert.equal(manifest.manifestStructurallyValid, false);
  assert.deepEqual(manifest.invalidMatchPatterns, [{
    surface: 'host_permissions',
    pattern: 'http://localhost:*/*'
  }]);
  assert.deepEqual(manifest.missingResources, [{
    resource: 'missing.css',
    kind: 'content_scripts.css'
  }]);
  assert.equal(manifest.webAccessibleResources[0].matches, 1);
});

test('validates that all referenced manifest resources exist', () => {
  const directory = createExtensionFixture({
    manifest_version: 3,
    name: 'Diagnostic fixture',
    background: { service_worker: 'background/service-worker.js' },
    action: { default_popup: 'popup.html' },
    content_scripts: [{
      matches: ['https://*.youtube.com/*'],
      js: ['content.js'],
      css: ['content.css']
    }],
    web_accessible_resources: [{
      resources: ['assets/*'],
      matches: ['https://*.youtube.com/*']
    }]
  }, {
    'background/service-worker.js': '',
    'popup.html': '',
    'content.js': '',
    'content.css': '',
    'assets/avatar.bin': ''
  });

  const manifest = inspectManifest(directory);
  assert.equal(manifest.manifestStructurallyValid, true);
  assert.deepEqual(manifest.missingResources, []);
  assert.deepEqual(manifest.invalidMatchPatterns, []);
  assert.deepEqual(manifest.pathTraversalResources, []);
});

test('distinguishes confirmed service-worker registration from a running target', () => {
  const extensionId = 'abcdefghijklmnopabcdefghijklmnop';
  const scriptUrl = `chrome-extension://${extensionId}/background/service-worker.js`;
  const registration = {
    scope: `chrome-extension://${extensionId}/`,
    activeScriptUrl: scriptUrl
  };

  assert.deepEqual(summarizeServiceWorkerState({
    registrations: [registration],
    workerTargets: [],
    extensionId,
    workerPath: 'background/service-worker.js'
  }), {
    serviceWorkerTargetObserved: false,
    serviceWorkerRegistered: true
  });

  assert.deepEqual(summarizeServiceWorkerState({
    registrations: null,
    workerTargets: [{ url: scriptUrl }],
    extensionId,
    workerPath: 'background/service-worker.js'
  }), {
    serviceWorkerTargetObserved: true,
    serviceWorkerRegistered: null
  });

  assert.deepEqual(summarizeServiceWorkerState({
    registrations: [],
    workerTargets: [{ url: scriptUrl }],
    extensionId,
    workerPath: 'background/service-worker.js'
  }), {
    serviceWorkerTargetObserved: true,
    serviceWorkerRegistered: false
  });
});

test('requires Chrome registry confirmation to report the extension installed', () => {
  assert.equal(isExtensionInstalled([], 'ISL Translator'), false);
  assert.equal(isExtensionInstalled([
    { id: 'abcdefghijklmnopabcdefghijklmnop', name: 'ISL Translator', enabled: false }
  ], 'ISL Translator'), false);
  assert.equal(isExtensionInstalled([
    { id: 'abcdefghijklmnopabcdefghijklmnop', name: 'ISL Translator', enabled: true }
  ], 'ISL Translator'), true);
});
