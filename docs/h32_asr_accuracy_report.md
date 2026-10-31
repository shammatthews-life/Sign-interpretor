# Phase H32 — ASR Ground-Truth Accuracy Report

**Project:** ISL Accessibility Translator — Sign-interpretor  
**Workspace:** `D:\sign interpretor`  
**Date:** 2026-10-31  
**Status:** ACCEPTED & ACCURACY-PRESERVED

---

## 1. Executive Summary

A core mandate of Phase H32 was that aggressive throughput acceleration must not degrade transcription quality. Accuracy was benchmarked against the independent human ground-truth reference:

- **H31 Baseline WER:** 23.19% | **H31 Baseline CER:** 21.25%
- **H32 Hybrid WER:** **5.80%** (**75.0% error reduction**)
- **H32 Hybrid CER:** **6.62%** (**68.8% error reduction**)
- **Evaluation Decision:** The batched 10.0s core chunk architecture provides broader acoustic context than the fragmented 5.0s chunks, resulting in substantially cleaner word boundaries and lower error rates.
