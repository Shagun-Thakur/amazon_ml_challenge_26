# Matching Reports (`reports/matching`)

This directory contains evaluation reports and analysis on pairwise matching models, deterministic coverage, false positive risks, hard negative mining, and positive match intelligence.

---

## 1. Directory Contents

| Directory / File | Description | Key Findings |
|---|---|---|
| [`deterministic_coverage/`](file:///d:/Projects/Machine_Learning%20Projects/Terminal_Titans_submission/reports/matching/deterministic_coverage/) | Coverage analysis of exact and deterministic matching heuristics. | [`deterministic_match_coverage.md`](file:///d:/Projects/Machine_Learning%20Projects/Terminal_Titans_submission/reports/matching/deterministic_coverage/deterministic_match_coverage.md), JSON summary, and CSV data. |
| [`deterministic_risk/`](file:///d:/Projects/Machine_Learning%20Projects/Terminal_Titans_submission/reports/matching/deterministic_risk/) | Risk evaluation of deterministic rules on singletons and false positive generation. | [`deterministic_candidate_risk.md`](file:///d:/Projects/Machine_Learning%20Projects/Terminal_Titans_submission/reports/matching/deterministic_risk/deterministic_candidate_risk.md), JSON, and CSV metrics. |
| [`hard_negative_summary.json`](file:///d:/Projects/Machine_Learning%20Projects/Terminal_Titans_submission/reports/matching/hard_negative_summary.json) | Summary of hard negative distractor patterns across sources. | Analyzes high-similarity false matches sharing postal codes, franchise names, or partial addresses. |
| [`positive_match_intelligence.json`](file:///d:/Projects/Machine_Learning%20Projects/Terminal_Titans_submission/reports/matching/positive_match_intelligence.json) | Ground-truth match signal analysis. | Identifies feature strengths across name edit distance, token Jaccard, and numeric address tokens. |
| Additional CSV Artifacts | Detailed breakdown data tables. | `hard_negative_family_summary.csv`, `hard_negative_threshold_analysis.csv`, `positive_match_signal_summary.csv`, `positive_vs_hard_negative.csv`. |

---

## 2. Key Insights
- **Singleton Vulnerability:** Relaxed deterministic rules (e.g. name-only or address-only match) trigger high false positive rates that severely degrade Macro $F_{0.5}$ on singletons.
- **Combined Signal Requirement:** Reliable matching requires composite name + address + numeric postal verification or supervised probabilistic classification with threshold calibration ($\tau \approx 0.84$).
