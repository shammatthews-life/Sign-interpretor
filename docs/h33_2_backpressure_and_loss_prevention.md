# H33.2 Backpressure and Loss Prevention

## Policy

Partial recognition retains its bounded rolling window and may collapse stale partial decode requests; this affects preview cadence only. All accepted audio is separately appended to a disk-backed utterance spool and is never removed by rolling-window trimming. The spool is capped at 15 minutes per utterance; hitting the cap returns an explicit error and requires a flush.

Finalization walks the spool in bounded windows. Its cursor advances only when inference succeeds, so a failed window is retryable without replaying already-finalized intervals. The interactive client serializes HTTP chunk submissions and flush waits for the send chain.

## Verification

A deterministic fake model blocks its first partial decode while ten seconds of audio arrive. Tests confirm the resident sample array remains at or below the four-second rolling limit, all 160,000 samples remain in the spool, and final windows exactly cover 0–10 seconds without gaps or duplicate finals.

No disk-full simulation or browser-level network throttling was performed. A spool write failure is surfaced to the caller; full product behavior under prolonged local-disk failure remains an acceptance check.
