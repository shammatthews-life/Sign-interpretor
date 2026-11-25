# Phase F2 Streaming ASR

## Backend boundary

`StreamingASRBackend` consumes canonical Phase F1 chunks and emits `TranscriptEvent` records. `FasterWhisperBackend` is the only class that imports or understands `WhisperModel`; `AudioPipeline`, sentence processing, and animation remain backend-agnostic.

## Buffered decode strategy

- F1 chunks: 100 ms at 16 kHz mono `Float32Array` / NumPy `float32`
- Minimum speech buffered before first decode: 1.0 s
- Decode hop: 0.75 s of newly received speech
- Rolling window: 4.0 s, bounded to prevent unbounded memory use
- Flush: decodes remaining buffer and emits a final transcript

Whisper is not treated as token-streaming. Consecutive rolling-window partials are stabilized: unchanged strings are suppressed; final events are independently marked so downstream command handling can act only on finals.

Each event records audio start/end, ASR start/end, emission time, compute time, and real-time factor (`compute_ms / audio_duration_ms`).

## Initial runtime choice

The first implementation uses `faster-whisper==1.1.1`, `device=cpu`, `compute_type=int8`. This Windows machine has an RTX 4050 Laptop GPU (6,141 MiB), but CPU int8 avoids assuming CUDA/CTranslate2 runtime libraries are correctly installed. GPU is a future measured option, not a fallback hidden in the pipeline.
