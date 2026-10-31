# H33.2 Local API Security Report

The viewer remains bound to `127.0.0.1`. API request validation now checks the HTTP `Host` against loopback and the selected server port; browser origins are restricted to the same local origin or the exact extension ID supplied by `--extension-id` / `SIGN_ALLOWED_EXTENSION_ID`. An arbitrary 32-character extension ID is no longer accepted. Requests without an Origin are accepted only with a valid loopback Host. Cross-origin OPTIONS remains denied and no permissive CORS headers are added.

`/save_sign` validates the complete sign motion shape, finite/ranged pose values, ordered keyframe times, declared bones, and payload size before saving. A same-directory temporary file is atomically linked for new signs; replacing an existing sign requires the authoring UI's explicit overwrite header and uses atomic replacement. Errors are surfaced as HTTP errors.

Tests cover exact extension IDs, hostile Host/origin rejection, loopback callers, every existing playable project sign schema, non-finite motion rejection, and no-overwrite/explicit-overwrite behavior. Definitions without `motion.status: "playable"` are excluded, matching the viewer's playback eligibility. The exact extension ID is a local operator setting, not a secret or authentication credential; the API is intentionally loopback-only.
