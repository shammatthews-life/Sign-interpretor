# H33.2 Audio Timeline Integrity

## Input invariants

The service rejects malformed/non-finite samples and timestamps. The backend verifies that timestamp duration agrees with `sample_count / sample_rate` within the sample-clock tolerance and rejects backwards/overlapping intervals. The API accepts optional zero-based sequential `chunk_id` values and rejects gaps, duplicate IDs, and out-of-order IDs before changing accounting state.

VAD intentionally suppresses silence in the interactive speech-session path. To preserve its audio clock, the backend inserts zero samples for short forward gaps (at most five seconds); longer gaps require a flush instead of silently shifting timestamps. The standalone viewer sends ordered audio chunks through one promise chain.

## Verification and limits

Tests cover incorrect sample duration, overlapping chunks, zero-filled short gaps, excessive gaps, invalid chunk IDs, and exact final-window timestamps. The slow-inference fixture reconciles all 10 seconds of input across final windows. The tests use synthetic samples and do not claim acoustic or linguistic accuracy.
