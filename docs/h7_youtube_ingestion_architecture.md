# H7 YouTube Ingestion Architecture

## Purpose

H7 accepts a supported YouTube URL and produces timestamped English speech
segments for the existing ISL translation and playback pipeline. It does not
create sign motions or infer motion for unavailable concepts.

## Flow

```text
YouTube URL
  -> URL validation and canonical video ID
  -> yt-dlp audio-only download
  -> FFmpeg 16 kHz, mono, PCM WAV
  -> faster-whisper (base.en, CUDA, float16)
  -> timestamped transcript segments
  -> existing EnglishToISLTranslator bridge
  -> playable-sign filter
  -> existing SignScheduler / Aether
```

`tools/youtube_pipeline/youtube_ingest.py` owns URL validation, caching,
audio extraction, transcription, aggregate timing, and the background job
manager. `tools/youtube_pipeline/translate_segments.mjs` sends each genuine
ASR segment to the existing `EnglishToISLTranslator`; it does not introduce
new translation rules.

## Runtime artifacts

For a video ID, H7 stores its cache under `runtime/youtube/<video-id>/`:

- `audio_16k.wav`: validated 16 kHz mono PCM audio.
- `metadata.json`: source metadata and extraction timing.
- `transcript.json` and `transcript.txt`: genuine ASR output only.
- `translation.json`: per-segment translation result and aggregate counts.
- `pipeline_result.json`: full end-to-end result and benchmark values.

Each transcript segment must contain `start`, `end`, and `text`; `start` is
non-negative and `end` must be greater than `start`.

## Dependency contract

H7 requires `faster-whisper==1.1.1`, `av==18.0.0`, and `yt-dlp==2026.8.19`.
`faster-whisper==1.1.1` passes `metadata_errors="ignore"` to `av.open`;
PyAV 19.0.1 rejects that argument. PyAV 18.0.0 was selected because it is
compatible with that call and supplies a CPython 3.11 ABI3 Windows AMD64 wheel
for the project's Python 3.12 environment.

The verified local wheel is
`runtime/wheels/av-18.0.0-cp311-abi3-win_amd64.whl` (27,556,236 bytes),
SHA-256
`aaf4d354d2beaa6651e4f92e54409a578bde64f79c0beef9a30b388d06f7c629`.
The artifact is ignored with the local `runtime/` directory and is not
committed. The environment was verified with Python 3.12.10,
faster-whisper 1.1.1, PyAV 18.0.0, and yt-dlp 2026.8.19.

No site-packages edits, monkey patches, or ASR engine substitutions are part
of this compatibility contract.

## Verified H7 run

The cached 721.835-second WAV decoded with
`WhisperModel("base.en", device="cuda", compute_type="float16")`, returning
256 timestamped segments. The transcript JSON retains `start`, `end`, and
`text` for every segment. The existing translator resolved 242 concepts;
three occurrences were playable `good` signs, 239 were unavailable, and
2,442 terms were unknown. The three playable `good` occurrences reached the
existing SignLibrary, SignScheduler, and Aether viewer. No sign motion was
added or modified.

Measured stages were 142.981 s for the earlier audio download/extraction,
28.599 s for the fresh ASR decode, and 0.135 s for the fresh translation
(171.715 s summed stage time; ASR RTF 0.0396). ASR and translation were
produced from cached audio without redownloading the video. The existing H7
runner returned its older cached pipeline result (26.904 s ASR, 0.420 s
translation, and 0.463 s for that cached invocation); those cached values do
not replace the fresh decode timings. These are processing measurements,
not accuracy metrics.

## Availability and safety

The translator returns unknown terms and unavailable concepts explicitly.
Only its `playable_signs` are eligible for the pre-existing SignScheduler and
Aether playback path. Unavailable concepts are never converted into motion or
animation by H7.

## Extension boundary

The H7 pipeline provides the reusable ingestion/transcription service and
in-process job manager. The separate H8 integration connects this pipeline to
the local viewer API and H6 browser extension. See
[`h8_youtube_extension_integration.md`](h8_youtube_extension_integration.md)
for the current endpoints, message flow, and limitations; H6 shell
validation alone does not establish an H8 handoff.
