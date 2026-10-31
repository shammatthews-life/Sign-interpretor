# H33.2 Runtime Correctness Report

## Scope and result

H33.2 addresses recoverable ASR finalization, audio timeline integrity, loss prevention during slow inference, content-derived cache identity, bounded YouTube job state, local authoring API validation, and extension origin/permission scope.

The implementation is present and the focused deterministic tests pass. Full canonical-video execution is **BLOCKED** by the measured system-memory preflight. Interactive Chrome/YouTube acceptance, product TTFS, and full-corpus WER/CER remain **NOT RUN**.

## Runtime changes

- Final audio is written to a disk-backed float32 spool. The in-memory rolling window remains bounded; the stream is capped at 15 minutes and explicit timeline gaps are zero-filled up to five seconds.
- Finalization processes non-overlapping windows and advances a persistent in-memory cursor only after successful inference. A failed flush reports `FAILED_RETRYABLE`; retry starts at the first unprocessed sample.
- Chunk timestamps are checked against sample count and sample rate. Ordered chunk IDs are supported at the service boundary.
- Audio, ASR, translation, and end-to-end caches now include content/provenance identities and are published atomically.
- Completed YouTube jobs retain small status metadata in memory, cap active workers and terminal history, and persist per-job results on disk.
- Loopback API requests require an allowed Host; extension origins require one exact configured extension ID. Sign authoring validates motion content and requires explicit overwrite consent.

## Evidence

See the H33.2 test evidence in `data/h33_2_*_tests.json` and the bounded local resource measurement in `data/h33_2_preflight.json`. H32 user worktree edits were preserved and excluded from H33.2 staging.

## Release status

Engineering fixes: **IMPLEMENTED**. Focused/regression checks: **PASS** where recorded in the execution checkpoint. Full-video and browser acceptance: **BLOCKED / MANUAL**, not inferred from short tests or H32 projections.
