# H33.2 Cache Provenance Report

## Cache identities

- Downloaded audio cache hits verify WAV format, video ID, and the stored SHA-256 of the current file.
- Transcript cache identity includes the source-audio SHA-256, model/device/compute/execution settings, Faster-Whisper/CTranslate2 versions, Python version, valid transcript shape, and matching text sidecar.
- Translation cache identity includes the transcript segments and hashes of the translation bridge, translator implementation, and sorted sign JSON content.
- Pipeline results carry audio, transcript, ASR implementation, execution, and translation identities. A result is reused only when its referenced audio and transcript artifacts verify.

Cache writes use same-directory temporary files and atomic replacement. Corrupt, partial, mismatched, or legacy cache entries are logged and recomputed rather than trusted.

## Verification

Focused tests confirm matching transcript and translation inputs hit cache; changed audio and sign-catalog identity miss; stale CPU-mode pipeline results do not bypass `GPU_REQUIRED`. These tests use small temporary files and mocks, not a downloaded video.
