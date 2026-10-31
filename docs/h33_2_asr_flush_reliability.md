# H33.2 ASR Flush Reliability

## Failure mode addressed

Previously, both synchronous and asynchronous flush paths could clear an utterance after failed inference. An asynchronous timeout could also leave the flush state permanently occupied. The caller could not distinguish a successful empty transcript from an inference failure.

## Implementation

`FasterWhisperBackend` keeps the utterance in a disk-backed spool and advances `_flush_cursor_samples` only after a window's inference call succeeds. Final decoding uses bounded, non-overlapping windows. `FlushResult` remains list-compatible for existing consumers while exposing `status` and `error`; a recoverable failure is reported as `FAILED_RETRYABLE`.

The asynchronous worker stores final events separately from partial events. Successful windows are returned once; retries resume at the failed window. Timeout retains the active operation until the worker finishes, after which the caller can collect the result or retry. Browser session teardown now preserves server-side audio after a failed final flush and permits a later stop to retry it.

## Verification

The focused validator injects synchronous and asynchronous mid-stream inference failures, retries, and checks exact audio interval coverage and event count. `LiveSpeechSession.test.mjs` checks that a failed flush does not reset ASR state and that a subsequent stop retries it. These are deterministic fake-model tests; they do not establish recognition quality.
