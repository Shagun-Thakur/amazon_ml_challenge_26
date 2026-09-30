# Comprehensive Exploratory Data Analysis & System Forensics Report
**Amazon ML Challenge 2026 — Track: Entity Resolution & Data Linkage**  
**Team:** Terminal Titans  
**Document Classification:** Technical Master Report & Forensics Baseline  
**Location:** `docs/comprehensive_eda_report.md`  
**Generated Date:** 2026-09-26  

---

## Executive Summary

This report synthesizes the end-to-end data forensics, structural profiling, cleaning impact analysis, candidate retrieval benchmarks, and matching risk evaluations conducted across the entire competition ecosystem.

Across the dataset, we analyzed **12,527,040 total business entity records** and **7,638,365 ground-truth linkage pairs**:
* **Source 1 (Query / Anchor):** 2,206,821 records (Reference entities)
* **Source 2 (Target Pool A):** 5,034,616 records
* **Source 3 (Target Pool B):** 5,285,603 records
* **Ground Truth Linkages:** 2,206,821 query evaluations yielding 7,638,365 true entity links

### Core Empirical Discoveries
1. **The 5.58% Singleton Population:** Exactly **123,247 S1 entities (5.5848%) have zero matches** in both Source 2 and Source 3. A naive top-$K$ model that always predicts candidates will fail catastrophically on these entities. The system must support empty match outputs.
2. **Cardinality Range (0 to 11):** While 5.58% of entities are singletons, non-empty S1 entities link to an average of **3.46 targets** (median: 3, max: 11). Over 80.48% of queries link across **both** Source 2 and Source 3 simultaneously.
3. **Cleaning Yields Massive Signal Gains:** V1 normalization collapsed noise without script corruption, boosting exact name equivalence from **4.77% to 21.43% (+16.66 pp in S2)** and exact address equivalence from **0.00% to 12.50% (+12.50 pp in S2)**.
4. **The "Exact Name" Risk Trap:** Exact name matching activates on **47.53% of hard negatives** (precision ratio 0.45). Relying on name match alone is disastrous; business addresses and numeric tokens provide the critical discriminative power (address token Jaccard averages **0.687 on positives vs 0.058 on hard negatives**).
5. **Retrieval Feasibility:** Character n-gram TF-IDF retrieval achieves **98.25% to 98.42% true pair recall at $K=25$**, with median true match rank between 1 and 2, proving that a two-stage retrieval + reranking pipeline is optimal.

---

## 1. Raw Dataset Profiling & Forensics

### 1.1 Dataset Cardinality & Geographic Breakdown
Each source was audited directly from disk without altering raw values:

| Metric | Source 1 (Reference) | Source 2 (Target Pool) | Source 3 (Target Pool) | Total Ecosystem |
| :--- | :---: | :---: | :---: | :---: |
| **Total Rows** | 2,206,821 | 5,034,616 | 5,285,603 | **12,527,040** |
| **Unique Entity IDs** | 2,206,821 | 5,034,616 | 5,285,603 | 12,527,040 (100% unique) |
| **Duplicate ID Rows** | 0 | 0 | 0 | 0 |
| **Unique Names** | 1,539,229 | 4,402,009 | 4,651,609 | 10,592,847 |
| **Unique Addresses** | 2,130,606 | 4,337,262 | 4,632,765 | 11,100,633 |
| **Empty Addresses** | 0 | 168,967 (3.36%) | 175,916 (3.33%) | 344,883 |
| **Non-ASCII Names** | 0 | 764,608 (15.19%) | 606,737 (11.48%) | 1,371,345 |
| **Non-ASCII Addresses** | 554 (0.025%) | 478,453 (9.50%) | 476,588 (9.02%) | 955,595 |
| **Exact Duplicate Rows** | 0 | 50,933 (1.01%) | 37,241 (0.70%) | 88,174 |
| **Country: United States (US)** | 1,323,633 (59.98%) | 3,016,817 (59.92%) | 3,170,056 (59.97%) | ~60.0% |
| **Country: India (IN)** | 883,188 (40.02%) | 2,017,799 (40.08%) | 2,115,547 (40.03%) | ~40.0% |

### 1.2 Noise Patterns & Linguistic Anomalies
Inspection revealed distinct corruption vectors across fields:
1. **Multilingual Script Divergence:** While Source 1 names are strictly ASCII, Sources 2 and 3 contain over 1.37 million non-ASCII names spanning Devanagari (`राम मार्केटिंग प्राइवेट लिमिटेड`), Tamil (`குளோபல் பிசினஸ் பிரைவேட் லிமிடெட்`), Gujarati (`શક્તિ અર્બન પ્રોડક્ટ્સ`), Telugu (`గుజరాత్ Logistics`), and Malayalam (`സിൽവർ കൺസൾട്ടൻസി`).
2. **OCR & Leet-Speak Typographic Substitutions:** Frequent digit-for-letter substitutions in names: `0` for `O` (`DIAM0ND BEACON`, `Ear N0se`), `1` for `l` (`marquezt0ken.com`, `Liverpoo1 Ltd`), `5` for `S` (`JEN ELWOOD ART5 CENTER`, `5uperior Co`), and `6` for `G` (`PEAK TRADIN6 NETWORKS`).
3. **Web Artifacts & Hash Pollution:** Injected URLs (`shivshakti.com`, `heassociates.com`), hashtags (`#centraleducation`, `#98825`), and trailing metadata IDs (`MW Management Private Limited - 2067865001`).
4. **Address Parsing Inconsistencies:** State/City prefixing (`OH, Columbus, 5559 Orville Avenue`), apartment/unit variations (`Unit APARTMENT G`), and complex multi-tier Indian addresses with landmarks (`Near Fortis Hospital, Mulund Goregaon Link Road`).
5. **Missing Addresses:** Over 344k records in Sources 2 & 3 have completely blank addresses, requiring the matcher to fall back to robust name and numeric token matching.

---

## 2. Ground Truth Topology & Target Distribution

### 2.1 Validation & Referential Integrity
Ground truth validation confirmed 100% structural integrity with zero dangling references:
* Ground truth rows evaluated: **2,206,821**
* Missing S1 references: **0**
* Missing Target references: **0**
* Duplicate link definitions: **0**

### 2.2 Cardinality Distribution (Matches per Query)
Analysis of the ground truth labels reveals the exact cardinality distribution:

| Matches per S1 Query | S1 Entity Count | Proportion (%) | Cumulative (%) | Engineering Implications |
| :---: | :---: | :---: | :---: | :--- |
| **0 (Singletons)** | **123,247** | **5.585%** | 5.585% | Must permit empty prediction strings |
| **1** | 119,157 | 5.399% | 10.984% | Strict 1-to-1 linkage |
| **2** | 375,212 | 17.002% | 27.986% | Dual match (often 1 in S2 + 1 in S3) |
| **3** | **530,841** | **24.055%** | 52.041% | Modal match cardinality |
| **4** | 484,115 | 21.937% | 73.978% | Multi-match linkage |
| **5** | 321,957 | 14.589% | 88.567% | High density linkage |
| **6** | 164,868 | 7.471% | 96.038% | Deep enterprise cluster |
| **7** | 63,968 | 2.899% | 98.937% | |
| **8** | 18,680 | 0.846% | 99.783% | |
| **9** | 4,205 | 0.191% | 99.974% | |
| **10** | 534 | 0.024% | 99.998% | |
| **11** | 37 | 0.002% | 100.000% | Hard maximum observed cardinality |

### 2.3 Cross-Source Linkage Topology
Analyzing where the matched entities reside relative to S1:
* **S1 $\to$ Both S2 and S3:** **1,776,047 rows (80.480%)** — The vast majority of queries have counterparts in both target pools.
* **S1 $\to$ S3 Only:** **164,498 rows (7.454%)**
* **S1 $\to$ S2 Only:** **143,029 rows (6.481%)**
* **S1 $\to$ Neither (Singletons):** **123,247 rows (5.585%)**

---

## 3. Data Normalization & V1 Cleaning Impact

### 3.1 Cleaning Transformation Rules
The V1 cleaning architecture applies conservative, collision-audited transformations:
* **NFKC Unicode Normalization:** Standardizes multi-byte accents and scripts without stripping native language characters.
* **Case Folding & Punctuation:** Converts text to lowercase; replaces delimiters (`-`, `/`, `,`, `.`) with clean token boundaries.
* **Ampersand Standardization:** Replaces `&` with `and` to bridge formal legal registrations with trade names.
* **Structural Feature Extraction:** Numeric address tokens (building numbers, plot numbers) and postal codes are isolated into dedicated structural features rather than lost in text stripping.

### 3.2 Signal Gains on True Positives (100k Sample Audit)
Comparing raw text versus cleaned text on true positive pairs demonstrates massive signal elevation:

| Target Source | Signal / Metric | Raw Pct (%) | Clean Pct (%) | Absolute Gain (pp) | Relative Increase |
| :---: | :--- | :---: | :---: | :---: | :---: |
| **S2** | **Exact Name Match** | 4.77% | **21.43%** | **+16.66 pp** | **+349%** |
| **S2** | **Exact Address Match** | 0.00% | **12.50%** | **+12.50 pp** | **Infinite** |
| **S2** | **Exact Name & Address** | 0.00% | **2.67%** | **+2.67 pp** | **Infinite** |
| **S3** | **Exact Name Match** | 4.56% | **22.08%** | **+17.51 pp** | **+384%** |
| **S3** | **Exact Address Match** | 4.33% | **4.34%** | +0.01 pp | Marginal |
| **S3** | **Exact Name & Address** | 0.00% | **0.001%** | +0.001 pp | S3 address diversity |

### 3.3 Textual Ambiguity & Collision Analysis
Normalizing text intentionally merges minor variants. We audited whether this creates false collisions:
* **Single Field Duplication:** Clean name duplication increased by 7.32 pp in S2 and 6.87 pp in S3 (as generic terms like `solutions`, `technologies` harmonize).
* **Composite Uniqueness:** When evaluating `clean_name + clean_address`, collisions remain negligible:
  * **Source 1:** 0 duplicate rows (100.0% uniquely identifiable)
  * **Source 2:** 1.33% duplicate rows (4,967,478 unique out of 5.03M)
  * **Source 3:** 0.95% duplicate rows (5,235,611 unique out of 5.28M)

> **Conclusion on Cleaning V1:** Composite entity evidence remains safely discriminative. Aggressive suffix stripping (e.g. discarding `Inc`, `LLC`, `Pvt Ltd`) was placed on hold because it risked over-collapsing distinct regional entities sharing root trade names.

---

## 4. Candidate Retrieval (Blocking) Benchmarks

A validation retrieval benchmark was executed on **20,000 S1 queries (69,150 true pairs)** against target pools of **133,180 S2 entities** and **135,970 S3 entities**:

### 4.1 Retrieval Performance Summary

| Target | Retrieval Architecture | Top-$K$ | Pair Recall (%) | S1 Any Recall (%) | S1 All Recall (%) | True Rank (Median) | True Rank (P90) | Vector Time (s) | Query Time (s) |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **S2** | Exact Structural Union | All | 84.01% | 89.43% | 77.12% | N/A | N/A | N/A | 2,220 cands/q |
| **S2** | **Char 3-gram TF-IDF** | **10** | 97.65% | 98.45% | 95.98% | **1** | **3** | 28.8s | 199.8s |
| **S2** | **Char 3-gram TF-IDF** | **25** | **98.25%** | **98.78%** | **97.02%** | **1** | **3** | 28.8s | 213.2s |
| **S2** | **Char 3-gram TF-IDF** | **50** | 98.66% | 99.09% | 97.71% | 1 | 3 | 28.8s | 208.8s |
| **S2** | **Char 3-gram TF-IDF** | **100** | 99.03% | 99.33% | 98.36% | 1 | 3 | 28.8s | 202.2s |
| **S2** | Char Hashing Vectorizer | 25 | 96.92% | 98.03% | 94.74% | 1 | 3 | 14.0s | 225.0s |
| **S3** | Exact Structural Union | All | 85.73% | 91.31% | 78.39% | N/A | N/A | N/A | 2,273 cands/q |
| **S3** | **Char 3-gram TF-IDF** | **10** | 97.67% | 98.97% | 95.87% | **2** | **3** | 30.6s | 203.6s |
| **S3** | **Char 3-gram TF-IDF** | **25** | **98.42%** | **99.30%** | **97.20%** | **2** | **3** | 30.6s | 204.4s |
| **S3** | **Char 3-gram TF-IDF** | **50** | 98.80% | 99.45% | 97.89% | 2 | 3 | 30.6s | 204.3s |
| **S3** | **Char 3-gram TF-IDF** | **100** | 99.08% | 99.60% | 98.37% | 2 | 3 | 30.6s | 206.0s |
| **S3** | Char Hashing Vectorizer | 25 | 97.01% | 98.55% | 94.82% | 2 | 3 | 13.0s | 232.6s |

### 4.2 Key Retrieval Insights
1. **Exceptional True Rank Distribution:** The median true match rank is **1 for S2** and **2 for S3**. 90% of all true matches appear within the **top 3 retrieved candidates**.
2. **Top-$K=25$ is the Optimal Efficiency Frontier:** Setting $K=25$ captures **98.25% (S2) and 98.42% (S3) of all true pairs**, leaving only ~1.6% recall loss while reducing the candidate space by orders of magnitude compared to exact rule unions.
3. **Hashing vs TF-IDF:** While hashing vectorization was twice as fast (13s vs 30s), it suffered a ~1.4% recall deficit across all $K$ thresholds due to hash collisions. TF-IDF remains the preferred retrieval backbone.

---

## 5. Matching Intelligence & Hard-Negative Risk Forensics

To test candidate discriminative power under adversarial conditions, we benchmarked matching signals against a diagnostic set of **44,658 curated hard-negative pairs** (pairs sharing strong name or address tokens but belonging to distinct entities).

### 5.1 Signal Separation: Positive Matches vs Hard Negatives

| Feature / Signal | Positive Mean | Positive Median | Hard Negative Mean | Hard Negative Median | Separation Quality |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Name Token Jaccard** | 0.610 | 0.667 | **0.666** | **0.667** | **Zero / Negative Separation** |
| **Name Token Containment** | 0.738 | 1.000 | **0.746** | **1.000** | **Zero Separation** |
| **Address Token Jaccard** | **0.687** | **0.714** | **0.059** | **0.000** | **Massive Separation (+0.628)** |
| **Address Token Containment**| **0.830** | **0.867** | **0.094** | **0.000** | **Massive Separation (+0.736)** |
| **Numeric Token Overlap** | **1.165** | **1.000** | **0.129** | **0.000** | **Massive Separation (+1.036)** |
| **Numeric Exact Match** | **0.584** | **1.000** | **0.056** | **0.000** | **High Precision Anchor** |

### 5.2 The "Name-Only" Vulnerability Analysis
* When matching by `exact_clean_name` alone:
  * Positive true-pair coverage: **21.43%**
  * Hard-negative false activation: **47.53%**
  * Positive-to-Negative Activation Ratio: **0.45** (More than 2 false positives for every true positive!)
* When matching by `exact_clean_address` alone:
  * Positive true-pair coverage: **12.50%**
  * Hard-negative false activation: **0.29%**
  * Positive-to-Negative Activation Ratio: **43.6**
* When combining both (`name_jaccard >= 0.70 AND address_jaccard >= 0.50`):
  * Positive coverage: **33.00%**
  * Hard-negative false activation: **0.047%**
  * Positive-to-Negative Activation Ratio: **701.7**

> **Critical Law of the Dataset:** In enterprise entity resolution, names are frequently duplicated across branches, franchises, and regional holding entities. **The address and numeric structure are the true discriminators.** Any classification model must penalize candidate pairs that have high name similarity but incompatible addresses or conflicting street numbers.

---

## 6. End-to-End System Recommendations

Based on the empirical findings across all audit reports, our production pipeline design adheres to the following four-stage architecture:

```
[Raw TSVs] 
     │
     ▼
[Stage 1: Normalization & Preprocessing]
  • Country partitioning (US vs India)
  • NFKC normalization, whitespace & token cleaning
  • Structural extraction: numeric street tokens & postal codes
     │
     ▼
[Stage 2: Candidate Blocking / Retrieval]
  • Country-isolated BM25 / Sparse TF-IDF (3-gram char)
  • Top-K candidate generation (K = 25 to 35 per source)
  • Retains ~98.4% true pair recall while filtering 99.99% negatives
     │
     ▼
[Stage 3: Pairwise Feature Engineering & Classification]
  • Name similarity: Jaccard, Levenshtein, Token Containment
  • Address similarity: Jaccard, Containment, City/State match
  • Structural signals: Numeric overlap, Exact numeric flag
  • Dual-source cross-compatibility features
  • LightGBM / XGBoost Ranker trained with hard negative samples
     │
     ▼
[Stage 4: Decision Post-Processing & Output Formulation]
  • Calibrated probability thresholding
  • Explicit empty-string output for singleton queries (5.58% prior)
  • Dynamic cardinality capping (max 11 targets)
  • Formatted TSV verified by validate_submission.py
```

---

## 7. Artifact & Audit Trail Reference Index

All underlying audit reports, CSV summaries, and forensic distributions are cataloged in the repository:

| Forensic Domain | Primary Markdown Report | Supporting Data / Charts |
| :--- | :--- | :--- |
| **Raw Data Profiling** | [`reports/data_profiling/raw_eda/raw_eda_report.md`](file:///d:/Projects/Machine_Learning%20Projects/Terminal_Titans_submission/reports/data_profiling/raw_eda/raw_eda_report.md) | `raw_summary.json`, `dataset_registry.csv` |
| **Cleaning Impact** | [`reports/data_profiling/processed_eda/processed_eda_report.md`](file:///d:/Projects/Machine_Learning%20Projects/Terminal_Titans_submission/reports/data_profiling/processed_eda/processed_eda_report.md) | `plots/cleaning_transformation_rates.png`, `csv/` |
| **Raw vs Clean Match** | [`reports/data_profiling/raw_vs_clean/raw_vs_clean_match_analysis.md`](file:///d:/Projects/Machine_Learning%20Projects/Terminal_Titans_submission/reports/data_profiling/raw_vs_clean/raw_vs_clean_match_analysis.md) | `csv/s2_positive_match_signals.csv` |
| **Ground Truth Validation** | [`reports/data_profiling/ground_truth_validation/ground_truth_validation_report.md`](file:///d:/Projects/Machine_Learning%20Projects/Terminal_Titans_submission/reports/data_profiling/ground_truth_validation/ground_truth_validation_report.md) | `ground_truth_topology.json` |
| **Retrieval Benchmarks** | [`reports/blocking/retrieval_benchmark/retrieval_benchmark_report.md`](file:///d:/Projects/Machine_Learning%20Projects/Terminal_Titans_submission/reports/blocking/retrieval_benchmark/retrieval_benchmark_report.md) | `csv/retrieval_benchmark_results.csv` |
| **Deterministic Coverage** | [`reports/matching/deterministic_coverage/deterministic_match_coverage.md`](file:///d:/Projects/Machine_Learning%20Projects/Terminal_Titans_submission/reports/matching/deterministic_coverage/deterministic_match_coverage.md) | `csv/deterministic_rule_coverage.csv` |
| **Deterministic Risk** | [`reports/matching/deterministic_risk/deterministic_candidate_risk.md`](file:///d:/Projects/Machine_Learning%20Projects/Terminal_Titans_submission/reports/matching/deterministic_risk/deterministic_candidate_risk.md) | `csv/signal_positive_vs_negative_distributions.csv` |
| **Cleaning Architecture** | [`reports/data_profiling/cleaning_design/cleaning_design_v1.json`](file:///d:/Projects/Machine_Learning%20Projects/Terminal_Titans_submission/reports/data_profiling/cleaning_design/cleaning_design_v1.json) | `transformation_catalogue.csv`, `collision_audit.csv` |
