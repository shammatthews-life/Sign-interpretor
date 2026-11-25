/** Reusable, preloading sign-motion library. */
export class SignLibraryError extends Error {
  constructor(message, code = 'SIGN_LIBRARY_ERROR') {
    super(message);
    this.name = 'SignLibraryError';
    this.code = code;
  }
}

export class SignLibrary {
  static MAX_PRELOAD_CONCURRENCY = 8;

  constructor({ basePath = '/signs', fetchImpl = null } = {}) {
    this.basePath = basePath.replace(/\/$/, '');
    // Do not detach Window.fetch: Chromium validates its Window receiver.
    this.fetchImpl = fetchImpl || ((url, options) => window.fetch(url, options));
    this.cache = new Map();
  }

  async loadSign(id) {
    const normalizedId = String(id).trim().toLowerCase();
    if (this.cache.has(normalizedId)) return this.cache.get(normalizedId);

    if (normalizedId.startsWith('fs_')) {
      return this._loadFingerspelling(normalizedId);
    }

    let response;
    try {
      response = await this.fetchImpl(`${this.basePath}/${normalizedId}.json`);
    } catch (error) {
      throw new SignLibraryError(`Unable to load sign '${normalizedId}': ${error.message}`, 'LOAD_FAILED');
    }
    if (!response.ok) throw new SignLibraryError(`Sign '${normalizedId}' was not found.`, 'NOT_FOUND');

    let definition;
    try {
      definition = await response.json();
    } catch {
      throw new SignLibraryError(`Sign '${normalizedId}' contains malformed JSON.`, 'MALFORMED_JSON');
    }
    this.validateDefinition(definition, normalizedId);
    this.cache.set(normalizedId, definition);
    return definition;
  }

  async _ensureFingerspeller() {
    if (!this._composeFingerspelling) {
      const mod = await import('./ISLFingerspelling.js');
      this._composeFingerspelling = mod.composeFingerspellingMotion;
    }
    return this._composeFingerspelling;
  }

  _buildFingerspellingDefinition(normalizedId, composeFn) {
    const word = normalizedId.slice(3).replace(/[^a-z0-9]/g, '');
    if (!word) {
      throw new SignLibraryError(`Sign '${normalizedId}' was not found.`, 'NOT_FOUND');
    }
    const definition = composeFn(word);
    if (!definition) {
      throw new SignLibraryError(`Sign '${normalizedId}' could not be synthesized.`, 'NOT_FOUND');
    }
    this.validateDefinition(definition, normalizedId);
    this.cache.set(normalizedId, definition);
    return definition;
  }

  async _loadFingerspelling(normalizedId) {
    const composeFn = await this._ensureFingerspeller();
    return this._buildFingerspellingDefinition(normalizedId, composeFn);
  }

  async preloadBundle(bundleUrl = `${this.basePath}/bundle.json`, manifestUrl = `${this.basePath}/manifest.json`) {
    await this._ensureFingerspeller().catch(() => null);
    try {
      const response = await this.fetchImpl(bundleUrl);
      if (response.ok) {
        const payload = await response.json();
        const signs = payload && typeof payload === 'object' ? (payload.signs || payload) : null;
        if (signs && typeof signs === 'object') {
          let loaded = 0;
          const failed = [];
          for (const [rawId, definition] of Object.entries(signs)) {
            const normalizedId = String(rawId).trim().toLowerCase();
            try {
              this.validateDefinition(definition, normalizedId);
              this.cache.set(normalizedId, definition);
              loaded += 1;
            } catch (error) {
              failed.push({ id: normalizedId, reason: error.message });
            }
          }
          if (loaded > 0) {
            return { source: 'bundle', loaded, failed, total: this.cache.size };
          }
        }
      }
    } catch {
      // Fall back to manifest-based preloading below.
    }

    const manifestResp = await this.fetchImpl(manifestUrl);
    if (!manifestResp.ok) {
      throw new SignLibraryError(`Unable to load signs manifest from '${manifestUrl}'.`, 'LOAD_FAILED');
    }
    const manifest = await manifestResp.json();
    const rawSigns = manifest && manifest.signs;
    const ids = Array.isArray(rawSigns)
      ? rawSigns.map(entry => (typeof entry === 'string' ? entry : entry?.sign_id)).filter(Boolean)
      : Object.keys(rawSigns || {});
    const results = await this.preload(ids);
    const failed = results.filter(r => r.status === 'rejected').map(r => ({ id: r.id, reason: r.reason?.message || 'failed' }));
    return { source: 'manifest', loaded: ids.length - failed.length, failed, total: this.cache.size };
  }

  async preload(ids) {
    await this._ensureFingerspeller().catch(() => null);
    const results = [];
    for (let offset = 0; offset < ids.length; offset += SignLibrary.MAX_PRELOAD_CONCURRENCY) {
      const batch = ids.slice(offset, offset + SignLibrary.MAX_PRELOAD_CONCURRENCY);
      results.push(...await Promise.allSettled(batch.map(id => this.loadSign(id))));
    }
    return results.map((result, index) => ({ id: ids[index], ...result }));
  }

  getPlayable(id, bonesMap) {
    const normalizedId = String(id).trim().toLowerCase();
    let definition = this.cache.get(normalizedId);
    if (!definition && normalizedId.startsWith('fs_') && this._composeFingerspelling) {
      definition = this._buildFingerspellingDefinition(normalizedId, this._composeFingerspelling);
    }
    if (!definition) throw new SignLibraryError(`Sign '${id}' has not been preloaded.`, 'NOT_PRELOADED');
    const { metadata, motion } = definition;
    if (motion.status !== 'playable') {
      throw new SignLibraryError(`Sign '${metadata.display_name}' is not playable: ${motion.unavailable_reason}`, 'MOTION_INCOMPLETE');
    }
    const missingBones = motion.involved_bones.filter(name => !bonesMap.has(name));
    if (missingBones.length) throw new SignLibraryError(`Sign '${metadata.display_name}' references missing bones: ${missingBones.join(', ')}`, 'INVALID_BONE');
    return { ...motion, sign_id: definition.sign_id, gloss: metadata.gloss, display_name: metadata.display_name };
  }

  validateDefinition(definition, expectedId) {
    if (!definition || typeof definition !== 'object') throw new SignLibraryError(`Sign '${expectedId}' is not an object.`, 'INVALID_DEFINITION');
    if (definition.schema_version !== '2.0.0') throw new SignLibraryError(`Sign '${expectedId}' has an unsupported schema version.`, 'INVALID_SCHEMA');
    if (definition.sign_id !== expectedId) throw new SignLibraryError(`Sign file '${expectedId}' has mismatched sign_id '${definition.sign_id}'.`, 'INVALID_ID');
    if (!definition.metadata || !definition.metadata.gloss || !definition.metadata.display_name) throw new SignLibraryError(`Sign '${expectedId}' is missing linguistic metadata.`, 'MISSING_METADATA');
    if (!definition.motion || !definition.motion.status) throw new SignLibraryError(`Sign '${expectedId}' is missing motion metadata.`, 'MISSING_MOTION');
    if (definition.motion.status !== 'playable') return;

    const motion = definition.motion;
    if (!Number.isFinite(motion.duration_ms) || motion.duration_ms <= 0) throw new SignLibraryError(`Sign '${expectedId}' has an invalid duration.`, 'INVALID_DURATION');
    if (!Array.isArray(motion.involved_bones) || motion.involved_bones.length === 0) throw new SignLibraryError(`Sign '${expectedId}' has no involved bones.`, 'INVALID_BONES');
    if (!Array.isArray(motion.keyframes) || motion.keyframes.length < 2) throw new SignLibraryError(`Sign '${expectedId}' needs at least two keyframes.`, 'INVALID_KEYFRAMES');
    if (motion.keyframes[0].time_ms !== 0 || motion.keyframes.at(-1).time_ms !== motion.duration_ms) throw new SignLibraryError(`Sign '${expectedId}' keyframes must span 0 to duration.`, 'INVALID_KEYFRAMES');
    motion.keyframes.forEach((frame, index) => {
      if (!Number.isFinite(frame.time_ms) || (index && frame.time_ms <= motion.keyframes[index - 1].time_ms)) throw new SignLibraryError(`Sign '${expectedId}' has an invalid keyframe at index ${index}.`, 'INVALID_KEYFRAME');
      if (!frame.rotations || typeof frame.rotations !== 'object') throw new SignLibraryError(`Sign '${expectedId}' keyframe ${index} has no rotations.`, 'INVALID_KEYFRAME');
    });
  }
}
