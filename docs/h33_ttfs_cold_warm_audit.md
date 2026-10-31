# H33 TTFS Cold/Warm Audit

**Status:** NOT RUN for product TTFS.

H33 measured CUDA model load, a model warm-up, and ASR-only inference. These
measurements do not start at URL submission and do not end at the first visible
Aether animation frame. Therefore, H33 reports no cold or warm product TTFS
percentiles and does not reuse H32's reported values as new measurements.

Raw H33 model and inference timings are in
[`data/h33_nvidia_gpu_verification.json`](../data/h33_nvidia_gpu_verification.json).
Product trial fields remain explicitly empty in
[`data/h33_ttfs_cold_warm_results.json`](../data/h33_ttfs_cold_warm_results.json).
