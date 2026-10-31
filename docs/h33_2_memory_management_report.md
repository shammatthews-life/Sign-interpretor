# H33.2 Memory Management Report

## Bounded runtime state

The streaming backend keeps only the configured rolling window in RAM and spools the complete utterance to a temporary file, with an explicit 15-minute limit. YouTube job management allows at most two active workers and keeps at most 100 terminal metadata records; large results are not retained in the in-memory job map and are written to per-job result files.

`tools/resource_preflight.py` is a read-only check for available system RAM, output-volume free space, and CUDA device/free VRAM. It does not allocate a model, alter the page file, terminate processes, or start inference.

## Full-video preflight

For the 8,979-second canonical duration, the measured preflight recorded 2.102 GiB available system RAM, 70.569 GiB free disk, and 5,920 MiB free of 6,141 MiB CUDA memory. The required available-RAM threshold is 6 GiB; therefore the full run is **BLOCKED**. No full-video inference was started.

The synthetic 10-second slow-inference test verifies the ASR resident rolling-buffer bound and spool coverage. It is not a measurement of peak full-pipeline RAM.
