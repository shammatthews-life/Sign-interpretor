# H33 NVIDIA GPU Execution Report

**Status:** PASS for short CUDA inference; full-video execution NOT RUN
**Device:** NVIDIA GeForce RTX 4050 Laptop GPU, CUDA index 0
**Model configuration:** Faster-Whisper `base.en`, CTranslate2 `float16`

## Verification

`tools/diagnose_nvidia_gpu.py` loaded the locally cached model explicitly with
`device="cuda"`, `device_index=0`, and `compute_type="float16"`. It transcribed
the first five seconds of the canonical PCM WAV ten times without CPU fallback.
The output was `This is public speaking` on each observation.

- CTranslate2: `4.8.2`
- Faster-Whisper: `1.1.1`
- NVIDIA driver: `592.82`
- CUDA devices reported by CTranslate2: `1`
- Model load: `1,227.44 ms`
- Warm-up inference: `424.37 ms`
- Measured five-second inference duration: `70.84–118.25 ms`
- Source WAV SHA-256: `67ff8eccd4caa269742395e1f1a45c1790d4d5982e4b95ccbe2167558561a512`
- Independent `nvidia-smi` active-process evidence: Python PID `21644`
- GPU utilization samples during inference: `3%`, `43%` (47% immediately after)
- Dedicated GPU memory samples during inference: `259–291 MiB` of `6,141 MiB`

A separate smoke test started the production `LocalASRService` without
overrides and emitted one transcript event. Its returned status identified
`device=cuda`, `device_index=0`, `compute_type=float16`, and
`execution_mode=GPU_REQUIRED`.

The raw verification and sampled telemetry are in
[`data/h33_nvidia_gpu_verification.json`](../data/h33_nvidia_gpu_verification.json)
and [`data/h33_nvidia_gpu_telemetry.json`](../data/h33_nvidia_gpu_telemetry.json).
System/process memory observations are in
[`data/h33_system_memory_telemetry.json`](../data/h33_system_memory_telemetry.json).

## Limits

This verifies short real inference and the production ASR service's enforced
CUDA configuration. It does not prove a full 8,979-second run, full-corpus
accuracy, first visible Aether frame latency, or browser WebGL renderer
selection. Those are not reported as passed.
