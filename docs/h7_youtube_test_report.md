# H7 YouTube Test Report

## Test target

- URL: `https://youtu.be/y8tFSuOMAqQ?si=7EZre0QT87fXoK1_`
- Video ID: `y8tFSuOMAqQ`
- Title: `How to Vlog as a Beginner (without overthinking it)`
- Video duration: 722 s
- Cached audio: `runtime/youtube/y8tFSuOMAqQ/audio_16k.wav`

## PyAV compatibility and installation

`faster-whisper==1.1.1` passes `metadata_errors="ignore"` to `av.open` in its
audio decoder. PyAV 19.0.1 rejects that keyword with
`TypeError: open() got an unexpected keyword argument 'metadata_errors'`.
PyAV 18.0.0 was selected because it accepts the argument and publishes the
Windows x86-64 CPython 3.11 ABI3 wheel, which works with the project's Python
3.12 interpreter.

The official PyPI wheel was installed directly from the local runtime
artifact; the package index was not used:

```text
Wheel: av-18.0.0-cp311-abi3-win_amd64.whl
Local path: runtime/wheels/av-18.0.0-cp311-abi3-win_amd64.whl
Size: 27,556,236 bytes
SHA-256: aaf4d354d2beaa6651e4f92e54409a578bde64f79c0beef9a30b388d06f7c629
```

The wheel remains a local runtime artifact under the ignored `runtime/`
directory. No wheel or changes to site-packages, faster-whisper, or
`av.open` were committed.

| Component | Installed version |
| --- | --- |
| Python | 3.12.10 |
| faster-whisper | 1.1.1 |
| PyAV (`av`) | 18.0.0 |
| yt-dlp | 2026.8.19 |

## Real decoder and full-video result

The required smoke test instantiated
`WhisperModel("base.en", device="cuda", compute_type="float16")` and decoded
the existing 16 kHz mono PCM WAV. This was a real decode, not an import-only
check. The decoder returned 256 non-empty timestamped transcript segments.
No video or audio was downloaded again.

`transcript.json` contains all 256 original ASR segments, each with `start`,
`end`, and `text`; `transcript.txt` contains their unmodified joined text.
The transcript output was checked for required fields and non-empty content.

## Existing translation and Aether scheduling

The full transcript was passed through the existing
`EnglishToISLTranslator` using `TranslationBackend` and the existing
`translate_segments.mjs` bridge. The existing availability catalog and sign
assets were used; no signs or transcript content were fabricated.

| Result | Count |
| --- | ---: |
| Transcript segments | 256 |
| Resolved gloss/concept occurrences | 242 |
| Unique resolved concepts | 9 |
| Playable concept occurrences | 3 |
| Unavailable concept occurrences | 239 |
| Unknown-term occurrences | 2,442 |

The resolved concepts were `GOOD`, `HELP`, `HOW`, `I`, `ME`, `NEED`, `NOT`,
`THANK_YOU`, and `YOU`. All three playable occurrences resolved to the
existing `good` sign; unavailable concepts were not sent to the scheduler.

The actual Aether viewer loaded its rig and SignLibrary, then received the
three `good` occurrences from the real translation result through its
existing `SignScheduler`. The viewer displayed `GOOD` as the current sign,
queued the remaining `GOOD` signs, and emitted playback lifecycle events.
Thus a genuinely playable concept from the transcript reached Aether.

## Extension handoff at H7

This H7 core-pipeline report predates the H8 extension integration. At the
time of the H7 test, the H6 popup did not submit YouTube URLs and the local
runtime did not expose `POST /youtube/process`. H8 subsequently added the
development-mode URL handoff, asynchronous job API, and extension result
relay. See
[`h8_youtube_extension_integration.md`](h8_youtube_extension_integration.md)
and [`h8_youtube_extension_test_report.md`](h8_youtube_extension_test_report.md)
for the current H8 contract and its installed-extension limitation.

## Benchmark

These are processing timings, not accuracy metrics. Audio extraction time is
the recorded result from the earlier successful cached-video ingestion.
ASR and translation timings are from the fresh real decode and existing
translation bridge run in this verification.

| Measurement | Result |
| --- | ---: |
| Audio duration | 721.835 s |
| Download/extraction | 142.981 s |
| ASR decode (`base.en`, CUDA/float16) | 28.599 s |
| Translation bridge | 0.135 s |
| Total measured stage time (sum) | 171.715 s |
| ASR real-time factor (ASR time / audio duration) | 0.0396 |
| Transcript segments | 256 |
| Translated concept occurrences | 242 |
| Playable concept occurrences | 3 |
| Unavailable concept occurrences | 239 |

For transparency, the existing H7 runner returned its cached
`pipeline_result.json` on this rerun (26.904 s ASR, 0.420 s translation,
0.463 s cached invocation wall time). Those cached measurements predate the
fresh forced ASR decode above; they are not substituted for the fresh timings
in the benchmark table. The transcript and translation artifacts were
refreshed from the current real decode.

## Regression results

- H7 cached-audio pipeline and fresh real CUDA/float16 decode: **PASS**
- H6, H5, H4, H3, H2, H1 validators: **PASS**
- G3, G2, G1 validators: **PASS**
- Sign-library schema validation: **PASS** (13 dictionary entries; 13 visual
  assets remain missing as previously expected by the evidence gate)
- Actual H7 extension handoff: **BLOCKED** (URL UI and endpoint are absent)

Existing sign-motion definitions were not changed.
