# Outputs Directory (`outputs`)

This directory stores ephemeral execution artifacts, intermediate candidate pairs, prediction scores, model weights, logs, and evaluation metrics generated during local and distributed runs.

---

## 1. Directory Structure

| Subdirectory | Purpose | Retention Policy |
|---|---|---|
| [`candidates/`](file:///d:/Projects/Machine_Learning%20Projects/Terminal_Titans_submission/outputs/candidates/) | Generated candidate pair sets (`candidate_pairs.tsv`) | Gitignored; reproducible via blocking scripts |
| [`predictions/`](file:///d:/Projects/Machine_Learning%20Projects/Terminal_Titans_submission/outputs/predictions/) | Pairwise probability scores and calibrated match decisions | Gitignored |
| [`models/`](file:///d:/Projects/Machine_Learning%20Projects/Terminal_Titans_submission/outputs/models/) | Checkpoints, GBDT JSON models, and tokenizer weights | Gitignored |
| [`metrics/`](file:///d:/Projects/Machine_Learning%20Projects/Terminal_Titans_submission/outputs/metrics/) | Quantitative evaluation run summaries and validation logs | Lightweight summaries may be tracked |
| [`figures/`](file:///d:/Projects/Machine_Learning%20Projects/Terminal_Titans_submission/outputs/figures/) | Generated plots, precision-recall curves, and calibration plots | Tracked in reports when finalized |
| [`logs/`](file:///d:/Projects/Machine_Learning%20Projects/Terminal_Titans_submission/outputs/logs/) | Standard output and execution error logs | Ephemeral |

---

## 2. Policy
Large binary files and candidate pair TSVs (>100 MB) must never be committed to Git. Production-ready submission deliverables should be placed in [`submission/output/`](file:///d:/Projects/Machine_Learning%20Projects/Terminal_Titans_submission/submission/output/).
