# H8 YouTube Extension Integration

## Scope

H8 connects the existing H7 YouTube pipeline to the H6 extension popup and
Shadow DOM overlay. It adds no downloader, ASR engine, translator, sign
catalog, or motion. Translation remains the existing G2/G3
`EnglishToISLTranslator` bridge, and only its existing `playable_signs` are
sent through the existing Aether `PLAY_SIGN` / `QUEUE_SIGN` interface.

This is a development-mode localhost integration. It is not complete
YouTube-to-ISL translation and does not imply broad sign-motion coverage.

## Architecture and message flow

```text
Extension popup
  -> versioned YOUTUBE_PROCESS message
  -> service worker / RuntimeBridge
  -> POST /youtube/process
  -> YouTubeJobManager background thread
  -> existing H7 cache / audio / faster-whisper / translation pipeline
  -> GET /youtube/status/<job_id> polling
  -> GET /youtube/result/<job_id>
  -> YOUTUBE_STATUS / YOUTUBE_RESULT events + STATE_UPDATE
  -> popup and content-script Shadow DOM overlay
  -> playable signs only: AETHER_COMMAND PLAY_SIGN, then QUEUE_SIGN
  -> embedded Aether viewer -> SignScheduler -> SignLibrary
```

The service worker records the active tab when the popup submits a job. It
targets that tab with Aether commands; the content script forwards commands
only to its localhost Aether iframe. Unavailable signs are rendered as
unavailable, never scheduled. The embedded viewer reports actual current and
queued signs back through the content script and RuntimeBridge.

## Local HTTP API

All API responses use JSON and permit localhost development CORS requests.

### `POST /youtube/process`

Request body:

```json
{"url":"https://youtu.be/y8tFSuOMAqQ"}
```

The URL is validated before a worker thread is started. The request returns
HTTP 202 without waiting for processing:

```json
{"job_id":"yt_y8tFSuOMAqQ_<unique-id>","state":"QUEUED"}
```

Invalid JSON, non-object bodies, and unsupported/invalid URLs return HTTP 400.

### `GET /youtube/status/<job_id>`

Returns the job ID, video ID, canonical URL, current stage, progress, start
and completion timestamps, error, and (when known) title. Stages exposed to
clients are `QUEUED`, `DOWNLOADING`, `EXTRACTING_AUDIO`, `TRANSCRIBING`,
`TRANSLATING`, `READY`, and `ERROR`.

Unknown IDs return HTTP 404.

### `GET /youtube/result/<job_id>`

Before completion, returns HTTP 409. Once ready, returns
`{"job_id":"...","state":"READY","result":...}`. The result contains the
existing H7 metadata, timestamped transcript, translation, and processing
timings. Failed jobs return their `ERROR` state and message.

Jobs are held in memory for this development server process; restarting the
server loses its job table. Existing H7 on-disk cache files remain available.

## Extension contract and UI

The versioned contract keeps schema version `1.0.0` and adds
`YOUTUBE_PROCESS`, `YOUTUBE_JOB_CREATED`, `YOUTUBE_STATUS`, `YOUTUBE_RESULT`,
`YOUTUBE_ERROR`, and `AETHER_PLAYBACK_STATE` message types. URL validation is
shared between the popup and backend; the Python H7 validator remains
authoritative.

The popup accepts a user-entered YouTube URL, validates it, submits it, and
shows the job ID, stage/progress, title and duration, transcript segment
count/latest segment, resolved glosses and status, playable signs, and
unavailable concepts. The overlay mirrors those results and additionally
shows the transcript summary and Aether current/queued signs. All dynamic
content is rendered as text; unavailable entries are explicitly labeled
“not played.”

The service worker polls at 1.2-second intervals with request timeouts and a
30-minute overall timeout. Invalid input, offline runtime, malformed JSON or
payloads, HTTP errors, job failure, and timeout are surfaced in the popup and
overlay without breaking their normal controls. A zero-playable result is
shown as such and dispatches no Aether sign commands.

## Aether command handling

On a valid result, the worker sends the first playable occurrence with
`PLAY_SIGN` and all remaining occurrences with `QUEUE_SIGN`, addressed to
the submitting tab. The content script queues commands until its Aether
iframe loads, validates the command name, and forwards it to that iframe.
The viewer uses its existing `SignScheduler`; it reports current and queued
sign IDs back to the overlay. No Aether model is packaged in the extension.

## Limitations

- The result is a limited English ASR transcript and an ISL-oriented
  prototype gloss. It is not a claim of complete or linguistically complete
  ISL translation.
- Only currently playable signs are animated. Unknown and unavailable
  concepts remain visible and are not inferred into motions.
- H7 jobs/statuses are in-memory; no cross-server-restart job persistence is
  provided.
- Extension integration requires the local viewer server at the configured
  localhost endpoint and the extension installed with its localhost host
  permissions.
- Browser integration validation in this environment used the actual popup,
  content script, local backend and embedded Aether viewer with a shim for
  Chrome extension messaging. The service-worker listener was separately
  executed against the real local API. A packaged, installed Chrome extension
  session on a live YouTube tab was not available for this run.
