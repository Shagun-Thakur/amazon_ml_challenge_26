# Data Profiling Analysis (`docs/analysis/data_profiling`)

This directory documents exploratory data analysis (EDA), statistical distributions, and dataset characteristics for Source 1, Source 2, Source 3, and ground truth tables.

---

## 1. Focus Areas
- **Entity Cardinality & Duplication:** Verification that Source 1 is deduplicated and that Source 2/Source 3 contain both matches and unlinked distractor records.
- **Length & Token Statistics:** Distributions of character length, word count, and token entropy for `business_name` and `business_address`.
- **Country Distribution & Open-Set Shift:** In train: India (54.5%), US (45.5%). In test: India (46.8%), US (38.3%), and **France (15.0%)**.
- **Ground Truth Topology:** Singletons account for 5.58% (123,247 entities); positive matches account for 94.42% (2,083,574 entities); maximum matches per entity is 11.

---

## 2. Primary References
- **Executive EDA Deep Dive:** [`docs/comprehensive_eda_report.md`](file:///d:/Projects/Machine_Learning%20Projects/Terminal_Titans_submission/docs/comprehensive_eda_report.md)
- **Detailed Audit & Profiling Reports:** [`reports/data_profiling/`](file:///d:/Projects/Machine_Learning%20Projects/Terminal_Titans_submission/reports/data_profiling/)
  - Raw EDA: [`reports/data_profiling/raw_eda/raw_eda_report.md`](file:///d:/Projects/Machine_Learning%20Projects/Terminal_Titans_submission/reports/data_profiling/raw_eda/raw_eda_report.md)
  - Processed EDA: [`reports/data_profiling/processed_eda/processed_eda_report.md`](file:///d:/Projects/Machine_Learning%20Projects/Terminal_Titans_submission/reports/data_profiling/processed_eda/processed_eda_report.md)
  - Raw vs Clean Match Analysis: [`reports/data_profiling/raw_vs_clean/raw_vs_clean_match_analysis.md`](file:///d:/Projects/Machine_Learning%20Projects/Terminal_Titans_submission/reports/data_profiling/raw_vs_clean/raw_vs_clean_match_analysis.md)
