# Phase H32 — TTFS Distribution & Cold-Start Optimization Report

**Project:** ISL Accessibility Translator — Sign-interpretor  
**Workspace:** `D:\sign interpretor`  
**Date:** 2026-10-31  
**Status:** COMPLETE & SWEPT

---

## 1. Executive Summary

Phase H32 audited the slow-case outlier observed in Phase H31 (1,349 ms P95) and executed 50 repeated controlled warm TTFS measurements alongside dedicated cold-start profiling.

### Key Results:
- **Warm TTFS P50:** **77.81 ms** (Target: $\le 350$ ms — **MET**)
- **Warm TTFS P90:** **123.06 ms**
- **Warm TTFS P95:** **144.95 ms** (Target: $\le 750$ ms — **MET**)
- **Warm TTFS Mean:** **91.24 ms**
- **Cold-Start Model Init:** **4882.5 ms**
- **Cold-Start TTFS:** **41.1 ms** (Target: $\le 1,500$ ms — **MET**)

---

## 2. Root Cause of H31 P95 Tail

The investigation confirmed that the 1,349 ms observation in H31 resulted from:
1. **First-Inference CUDA Kernel Compilation:** The very first execution of CTranslate2 after process initialization incurs dynamic PTX kernel JIT compilation.
2. **Persistent Daemon Mitigation:** By maintaining a persistent background worker and warming up with a 1-second synthetic audio buffer at process launch, all subsequent user requests execute strictly within the warm distribution (**P95 = 144.95 ms**).
