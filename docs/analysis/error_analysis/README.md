# Error Analysis (`docs/analysis/error_analysis`)

Post-inference diagnostic studies investigating model failures, false positives (erroneous merges), and false negatives (missed matches).

---

## 1. Objectives
- **Precision Penalty Mitigation:** Precision is weighted 2× as heavily as recall in Macro $F_{0.5}$. False merges heavily penalize scores, especially on singletons (which score 0 upon any false merge).
- **Distractor Analysis:** Trace false positives back to common patterns (e.g. entities with identical names in different postal codes, or identical postal codes with distinct business names).
- **Failure Stage Attribution:** Determine whether a false negative occurred during candidate blocking (recall loss) or downstream classification/thresholding (scoring loss).

---

## 2. Relevant Reports
- Deterministic candidate risk: [`reports/matching/deterministic_risk/deterministic_candidate_risk.md`](file:///d:/Projects/Machine_Learning%20Projects/Terminal_Titans_submission/reports/matching/deterministic_risk/deterministic_candidate_risk.md)
- Hard negative summary: [`reports/matching/hard_negative_summary.json`](file:///d:/Projects/Machine_Learning%20Projects/Terminal_Titans_submission/reports/matching/hard_negative_summary.json)
