# Baseline Pipeline (`experiments/baseline`)

This directory contains the complete, reproducible Stage 1 and Stage 2 baseline pipeline code for the Amazon ML Challenge 2026.

---

## 1. Module Overview

| Script | Purpose | Key Functions / Classes |
|---|---|---|
| [`pipeline_clean.py`](file:///d:/Projects/Machine_Learning%20Projects/Terminal_Titans_submission/experiments/baseline/pipeline_clean.py) | **Stage 1 Orchestrator**: Ingestion, schema audit, text normalization, and structural feature generation. | `run_stage1_pipeline()` |
| [`blocking.py`](file:///d:/Projects/Machine_Learning%20Projects/Terminal_Titans_submission/experiments/baseline/blocking.py) | **Stage 2 Candidate Blocking**: Country-partitioned dual-channel TF-IDF character (3,4) n-gram retrieval. Supports `--mode {benchmark, test, all}`. | `run_blocking_benchmark()`, `generate_test_candidates()` |
| [`text_normalizer.py`](file:///d:/Projects/Machine_Learning%20Projects/Terminal_Titans_submission/experiments/baseline/text_normalizer.py) | Text normalization: Unicode NFKD, diacritics removal, French ligatures (`œ` -> `oe`), legal suffix stripping, and address expansion. | `normalize_text()`, `clean_business_name()`, `clean_address()` |
| [`structural_features.py`](file:///d:/Projects/Machine_Learning%20Projects/Terminal_Titans_submission/experiments/baseline/structural_features.py) | Structural tokens: numeric PIN/ZIP extraction ($\ge 3$ digits) and composite text generation (`clean_name + " " + clean_addr`). | `extract_numeric_tokens()`, `build_composite_text()` |
| [`features.py`](file:///d:/Projects/Machine_Learning%20Projects/Terminal_Titans_submission/experiments/baseline/features.py) | Pairwise feature extraction: token Jaccard, character overlap, numeric token matches. | `extract_pairwise_features()` |
| [`train_and_predict.py`](file:///d:/Projects/Machine_Learning%20Projects/Terminal_Titans_submission/experiments/baseline/train_and_predict.py) | Supervised baseline model training and test prediction scoring. | `train_baseline_matcher()`, `predict()` |
| [`audits.py`](file:///d:/Projects/Machine_Learning%20Projects/Terminal_Titans_submission/experiments/baseline/audits.py) | Quality audits: schema completeness, null detection, whitespace trimming, regex ID validation (`^S[123]-\d+$`). | `run_table_audit()` |
| [`gt_profiler.py`](file:///d:/Projects/Machine_Learning%20Projects/Terminal_Titans_submission/experiments/baseline/gt_profiler.py) | Ground truth profiling: singleton rates, match cardinality distributions, and source attribution ($S_2$ vs $S_3$). | `profile_ground_truth()` |
| [`utils_io.py`](file:///d:/Projects/Machine_Learning%20Projects/Terminal_Titans_submission/experiments/baseline/utils_io.py) | File I/O utilities: dynamic path resolution across environments (`resolve_project_paths`), atomic safe TSV reader/writer preserving string postal codes. | `load_tsv_safe()`, `save_tsv_safe()`, `resolve_project_paths()` |

---

## 2. Reproduction & Execution

### Prerequisites
- Python 3.11+
- Requirements installed: `pip install -r requirements.txt`
- Raw data placed in `data/raw/` (`train/` and `test/` TSVs)

### Stage 1: Ingestion, Normalization & Quality Audit
```bash
python experiments/baseline/pipeline_clean.py
```
- Reads from: `data/raw/{train,test}/*.tsv`
- Writes normalized tables to: `data/processed/{train,test}/clean_*.tsv`
- Writes audit report to: `reports/data_profiling/data_audit_report.json`
- Throughput: ~22,500 rows/sec (~18 minutes total runtime).

### Stage 2: Candidate Blocking Benchmark
```bash
# Fast recall evaluation on 20,000 validation records
python experiments/baseline/blocking.py --mode benchmark

# Full test candidate generation
python experiments/baseline/blocking.py --mode test
```
- Outputs candidate pairs to: `submission/output/candidate_pairs.tsv` and `outputs/candidates/candidate_pairs.tsv`

### Stage 3: Supervised Matcher Training & Prediction
```bash
python experiments/baseline/train_and_predict.py
```
- Outputs final predictions to: `submission/output/matching_results.tsv`

---

## 3. Benchmark & Verification Status

Detailed reproduction audits and metrics are documented in [`reports/reproducibility/baseline_reproduction.md`](file:///d:/Projects/Machine_Learning%20Projects/Terminal_Titans_submission/reports/reproducibility/baseline_reproduction.md).

- **Stage 1 Normalization & Ground Truth Profiling:** 100% verified, byte-identical reproduction.
  - Total $S_1$ Anchors: 2,206,821
  - Singletons: 123,247 (5.5848%)
  - Total Ground Truth Matches: 7,638,365
- **Stage 2 Local CPU Blocking:** Due to the $O(N \times M)$ brute-force n-gram dot product computation on 1.73M queries against ~10M pool entities, large-scale indexing is delegated to cloud tracks (Kaggle/Colab/SageMaker) with inverted indices and GPU/FAISS acceleration.
