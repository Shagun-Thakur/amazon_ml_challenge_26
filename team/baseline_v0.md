# Baseline V0 Specification & Freeze Marker

**Frozen Date:** 2026-09-26  
**Status:** FROZEN (Stage 1 Complete, Local Compute Deprecated, Cloud Migration Active)  
**Authors:** Terminal Titans ML Team  

---

## 1. Exact Code Version & Components

The baseline codebase is established in `src/` under the following permanent modules:
- `src/utils/utils_io.py`: File I/O, path discovery, and strict TSV parsers
- `src/normalization/text_normalizer.py`: Text cleaning, NFKD normalization, corporate suffix stripping
- `src/features/structural_features.py`: Numeric token extraction & composite text construction
- `src/data/audits.py`: Schema quality, duplicate checking, and ID format verification
- `src/evaluation/gt_profiler.py`: Ground truth profiling and match cardinality analysis
- `src/pipeline/pipeline_clean.py`: Stage 1 end-to-end normalization and audit runner
- `src/blocking/blocking.py`: Dual-channel country-partitioned TF-IDF candidate retriever (decoupled with `--mode benchmark` / `--mode test`)

---

## 2. Dataset Paths & Versions

- **Training Reference:** `data/raw/train/train_source1.tsv` (2,206,821 records)
- **Training Source 2:** `data/raw/train/train_source2.tsv` (5,034,616 records)
- **Training Source 3:** `data/raw/train/train_source3.tsv` (5,285,603 records)
- **Training Ground Truth:** `data/raw/train/train_ground_truth.tsv` (2,206,821 rows, 7,638,365 links)
- **Test Reference:** `data/raw/test/test_source1.tsv` (1,732,544 records)
- **Test Source 2:** `data/raw/test/test_source2.tsv` (4,887,273 records)
- **Test Source 3:** `data/raw/test/test_source3.tsv` (5,082,316 records)
- **Normalized Data Cache:** `data/processed/{train, test}/clean_*.tsv`

---

## 3. Reproduced Baseline Metrics

All values independently reproduced and verified against `reports/data_profiling/data_audit_report.json`:

```yaml
ground_truth_profile:
  total_s1_records: 2206821
  singleton_count: 123247
  singleton_percentage: 5.5848%
  positive_s1_records: 2083574
  positive_s1_percentage: 94.4152%
  total_linked_matches: 7638365
  source_2_matches: 3693619 (48.36%)
  source_3_matches: 3944746 (51.64%)
  mean_matches_per_anchor: 3.4613
  max_matches_per_anchor: 11
  cardinality_mode: 3 matches (530,841 anchors)

data_quality_audit:
  schema_validity: 100% PASS
  null_count: 0
  empty_address_count:
    train_source2: 168967
    train_source3: 175916
    test_source2: 129408
    test_source3: 136098
  country_breakdown:
    train:
      US: 60%
      India: 40%
    test:
      India: 46.75%
      US: 38.27%
      France: 14.98% (Open-Set Country)
```

---

## 4. Key Lessons & Architectural Decisions

1. **ADR-005 (Cloud Compute Mandate):** Local PC execution of all-pairs Cartesian candidate generation across 1.73M $\times$ 10M records is strictly deprecated. All future heavy training and retrieval will be performed on cloud platforms (Kaggle / Colab / SageMaker).
2. **ADR-006 (Algorithmic Blocking Redesign):** Replace naive brute-force sparse matrix dot-products with inverted index token posting lists (e.g. BM25 / token inverted index) or GPU vector acceleration (FAISS), which skip zero-overlap pairs and execute in minutes rather than 20+ hours.
3. **Decoupled Architecture:** Validation recall benchmarking on stratified subsets is permanently decoupled from full test set generation.

---

## 5. Next Planned Action

Transition to the structured EDA & Modeling phases on Cloud:
```
RAW EDA  -->  PROCESSED EDA  -->  RAW vs NORMALIZED COMPARISON  -->  MATCH-INTELLIGENCE EDA  -->  CLOUD BLOCKING BENCHMARK
```
