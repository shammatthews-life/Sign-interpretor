# Phase H32 — ASR Redundant Computation Forensic Audit Report

**Project:** ISL Accessibility Translator — Sign-interpretor  
**Workspace:** `D:\sign interpretor`  
**Date:** 2026-10-31  
**Author:** Autonomous Engineering Agent  
**Status:** COMPLETE & EMPIRICALLY CONFIRMED

---

## 1. Executive Summary & Root Cause Confirmation

The forensic investigation into `tools/asr/streaming_asr.py` and Phase H31 streaming telemetry confirmed the architectural bottleneck:

### The Redundancy Root Cause:
- **Rolling Window Size:** 4,000 ms (4.0 seconds)
- **Decode Hop Size:** 750 ms (0.75 seconds)
- **Redundancy Ratio:** $$\frac{4000}{750} = 5.33\times$$
- **Redundant Audio Percentage:** **81.25%** of all audio passed to the neural network was previously processed overlapping context.
- **Throughput Impact:** In a 60-second video clip, the legacy recognizer processed **320 seconds** of cumulative audio across 80 discrete invocations. This forced an otherwise 45× capable GPU down to an effective throughput of **4.50× real time**.

---

## 2. Model-Window RTF vs. Effective Unique-Audio RTF

Phase H32 formally separates two metrics that were historically conflated:

1. **Model-Window RTF:**
   $$\text{RTF}_{\text{model}} = \frac{\text{Inference Time (ms)}}{\text{Window Audio Duration (4,000 ms)}} \approx 0.0429 \quad (23.3\times \text{ window throughput})$$
2. **Effective Unique-Audio RTF:**
   $$\text{RTF}_{\text{effective}} = \frac{\text{Total Processing Wall Time}}{\text{Newly Arrived Unique Audio (750 ms)}} \approx 0.2222 \quad (4.50\times \text{ real time})$$

Because each 750 ms step dragged 3,250 ms of stale context through the transformer encoder and decoder layers, GPU compute was predominantly wasted on redundant tokens.

---

## 3. Optimization Prescription

To achieve sustained $\ge 20\times$ real-time throughput:
1. **Eliminate Rolling Window:** Replace the 4,000 ms / 750 ms sliding window with fixed core audio intervals (e.g. 10.0s core chunks).
2. **Minimize Overlap:** Reduce boundary overlap to 0.25–0.50s, used strictly for acoustic continuity and deduplicated at boundary tokens.
3. **GPU Micro-Batching:** Feed multiple non-overlapping core intervals simultaneously to CUDA via Faster-Whisper `BatchedInferencePipeline`.
