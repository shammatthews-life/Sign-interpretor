# H33 Full Canonical Execution Report

**Status:** BLOCKED — full canonical ASR was not run.

The local source is the 16 kHz mono PCM WAV for YouTube video
`MXKkXXYUxBc`, duration `8,978.9010625` seconds. Its SHA-256 is recorded in
[`data/h33_canonical_source_manifest.json`](../data/h33_canonical_source_manifest.json).
Only a five-second prefix was used for fresh CUDA diagnostics.

The H32 benchmark reports a 300-second canonical slice and projects a
full-video duration. That projection is not a full-video measurement. No
H33 full transcript, interval accounting, or full-run stage timings were
produced. See
[`data/h33_full_video_asr_results.json`](../data/h33_full_video_asr_results.json)
and [`data/h33_full_video_stage_timings.json`](../data/h33_full_video_stage_timings.json).

Before attempting the requested run, implement and validate a bounded
progressive scheduler that preserves the 2-second prefix lane and performs
10-second core processing with 0.25-second boundary context. The H32 report
does not substitute for that implementation or validation.
