# Phase F1 Audio Pipeline

## Internal representation

- **Sample rate:** 16,000 Hz
- **Channels:** mono
- **Sample type:** `Float32Array`, normalized to -1.0 to +1.0
- **Default output chunk:** 100 ms (1,600 samples), configurable through `format.chunkDurationMs`

Audio is downmixed and resampled once when it enters `StreamingAudioPipeline`; subsequent stages share that representation.

## Flow

`AudioSource` (microphone or file) → downmix/resample → `PCMChunker` → conservative passthrough preprocessor → adaptive energy VAD → `StreamingASRInput` queue.

The preprocessor intentionally does not alter samples in this phase. RMS, peak, clipping, near-silence, estimated adaptive noise floor, and an SNR-style diagnostic are emitted per chunk. The energy VAD is a baseline diagnostic, not a robust speech/noise classifier.

`MicrophoneSource` uses browser `getUserMedia`; localhost is treated as a secure context by modern browsers. `FileSource` accepts progressive PCM frames, and `decodeWav` supports PCM 16/32-bit RIFF/WAVE input.

`StreamingASRInput` is the future ASR boundary. It accepts only VAD-approved canonical chunks and does not implement transcription in F1.
