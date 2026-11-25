/** Reusable, preloading sign-motion library. */
export class SignLibraryError extends Error {
  constructor(message, code = 'SIGN_LIBRARY_ERROR') {
    super(message);
    this.name = 'SignLibraryError';
    this.code = code;
  }
}

export class SignLibrary {
  constructor({ basePath = '/signs', fetchImpl = null } = {}) {
    this.basePath = basePath.replace(/\/$/, '');
    // Do not detach Window.fetch: Chromium validates its Window receiver.
    this.fetchImpl = fetchImpl || ((url, options) => window.fetch(url, options));
    this.cache = new Map();
  }

  async loadSign(id) {
    const normalizedId = String(id).trim().toLowerCase();
    if (this.cache.has(normalizedId)) return this.cache.get(normalizedId);

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

  async preload(ids) {
    const results = await Promise.allSettled(ids.map(id => this.loadSign(id)));
    return results.map((result, index) => ({ id: ids[index], ...result }));
  }

  getPlayable(id, bonesMap) {
    const definition = this.cache.get(String(id).trim().toLowerCase());
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
