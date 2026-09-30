# Data Profiling Reports (`reports/data_profiling`)

This directory houses formal exploratory data analysis (EDA), quality audits, topological profiles, and schema validation reports across raw and processed datasets.

---

## 1. Directory Contents

| Directory / File | Description | Key Findings & Content |
|---|---|---|
| [`data_audit_report.json`](file:///d:/Projects/Machine_Learning%20Projects/Terminal_Titans_submission/reports/data_profiling/data_audit_report.json) | Comprehensive schema & quality audit of all 7 train/test TSV tables. | Zero duplicate IDs; 0 regex format violations; identifies empty address counts. |
| [`ground_truth_topology.json`](file:///d:/Projects/Machine_Learning%20Projects/Terminal_Titans_submission/reports/data_profiling/ground_truth_topology.json) | Match cardinality and singleton distribution metadata. | 5.5848% singletons (123,247 entities); max matches per S1 is 11; mean matches: 3.4613. |
| [`ground_truth_validation/`](file:///d:/Projects/Machine_Learning%20Projects/Terminal_Titans_submission/reports/data_profiling/ground_truth_validation/) | Ground truth topological validation and report. | [`ground_truth_validation_report.md`](file:///d:/Projects/Machine_Learning%20Projects/Terminal_Titans_submission/reports/data_profiling/ground_truth_validation/ground_truth_validation_report.md), validation JSON. |
| [`raw_eda/`](file:///d:/Projects/Machine_Learning%20Projects/Terminal_Titans_submission/reports/data_profiling/raw_eda/) | In-depth EDA on raw input data. | [`raw_eda_report.md`](file:///d:/Projects/Machine_Learning%20Projects/Terminal_Titans_submission/reports/data_profiling/raw_eda/raw_eda_report.md), summaries per source, sample extracts. |
| [`processed_eda/`](file:///d:/Projects/Machine_Learning%20Projects/Terminal_Titans_submission/reports/data_profiling/processed_eda/) | EDA on normalized and tokenized datasets (`data/processed/`). | [`processed_eda_report.md`](file:///d:/Projects/Machine_Learning%20Projects/Terminal_Titans_submission/reports/data_profiling/processed_eda/processed_eda_report.md), processed summary JSONs. |
| [`raw_vs_clean/`](file:///d:/Projects/Machine_Learning%20Projects/Terminal_Titans_submission/reports/data_profiling/raw_vs_clean/) | Comparative analysis before and after normalization pipeline. | [`raw_vs_clean_match_analysis.md`](file:///d:/Projects/Machine_Learning%20Projects/Terminal_Titans_submission/reports/data_profiling/raw_vs_clean/raw_vs_clean_match_analysis.md), comparison JSON, distribution plots. |
| [`cleaning_design/`](file:///d:/Projects/Machine_Learning%20Projects/Terminal_Titans_submission/reports/data_profiling/cleaning_design/) | Normalization rules, suffix standardizations, regex mappings. | `cleaning_design_v1.json` specifications. |

---

## 2. Cross References
- High-level overview: [`docs/comprehensive_eda_report.md`](file:///d:/Projects/Machine_Learning%20Projects/Terminal_Titans_submission/docs/comprehensive_eda_report.md)
- Pipeline generator: [`experiments/baseline/pipeline_clean.py`](file:///d:/Projects/Machine_Learning%20Projects/Terminal_Titans_submission/experiments/baseline/pipeline_clean.py)
