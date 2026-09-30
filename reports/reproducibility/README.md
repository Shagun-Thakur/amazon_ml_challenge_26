# Reproducibility Reports (`reports/reproducibility`)

This directory documents independent replication and audit reports verifying baseline models, metric consistency, and pipeline throughput.

---

## 1. Directory Contents

| Document | Scope | Status |
|---|---|---|
| [`baseline_reproduction.md`](file:///d:/Projects/Machine_Learning%20Projects/Terminal_Titans_submission/reports/reproducibility/baseline_reproduction.md) | Full audit and execution log of the team's Stage 1 and Stage 2 baseline pipeline. | **Verified**: 100% byte-identical reproduction on Stage 1 ingestion, normalization, and ground-truth metrics. Detailed root-cause analysis of local CPU blocking bottleneck. |

---

## 2. Reproduction Standards
- Python environment specification and pinned package versions.
- Step-by-step commands to reproduce all intermediate and final outputs.
- Comparison matrix comparing newly generated numbers against legacy logs.
