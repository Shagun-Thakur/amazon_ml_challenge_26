# Amazon ML Challenge 2026 — Business Entity Resolution
**Team:** Terminal Titans  

---

## 1. Challenge Overview
The **Amazon ML Challenge 2026** focuses on **Business Entity Resolution (ER)** across large-scale commercial datasets. Business identity records arrive from three independent data sources ($S_1$, $S_2$, and $S_3$) containing partial, noisy, and unstandardized information without shared common keys. The objective is to identify which records across noisy sources refer to the exact same real-world business entity.

---

## 2. Problem Formulation
- **Reference Source ($S_1$):** Deduplicated reference dataset. Every entity in $S_1$ must be evaluated.
- **Noisy Sources ($S_2$ and $S_3$):** Independent, noisy sources containing true matches as well as distractor records.
- **Match Multiplicity:** An $S_1$ entity can match zero (singleton), one, or multiple records from $S_2$ and $S_3$.
- **Evaluation Metric:** Macro $F_{0.5}$ score averaged over all $S_1$ entities:
  $$F_{0.5} = \frac{1.25 \times \text{Precision} \times \text{Recall}}{0.25 \times \text{Precision} + \text{Recall}}$$
  - Precision is weighted 2× as heavily as recall to strongly penalize false merges.
  - Singletons (no true matches) score 1.0 if correctly predicted as empty, and 0.0 upon any false merge.
- **Open-Set Generalization:** The training data contains records from `US` and `India`. The test data introduces an unseen third country, `France`.
- **Fair Play Constraints:** Zero external data lookups, geocoding APIs, or web scraping allowed. Maximum model size: 8 Billion parameters, permissive open-source license (MIT/Apache 2.0).

---

## 3. Repository Architecture

```
amazon-ml-2026/
├── README.md                          # Main project & architectural documentation
├── LICENSE                            # Open-source license (MIT / Apache 2.0)
├── requirements.txt                   # Top-level dependencies for environment setup
├── .gitignore                         # Hardened git ignore (excludes raw data & weights)
├── CONTRIBUTING.md                    # Engineering guidelines & PR workflows
├── REPOSITORY_MAP.md                  # Comprehensive mapping of all directories and files
│
├── docs/                              # Problem statement, strategies, and notes
│   ├── problem_statement.md           # Official challenge statement & rules
│   ├── strategy/                      # Technical roadmaps and architectural plans
│   ├── analysis/                      # In-depth EDA and error investigations
│   └── submission/                    # Methodology and operational submission notes
│
├── data/                              # Data governance & specifications
│   ├── README.md                      # Data policy, layout rules, and schemas
│   ├── raw/                           # Raw competition TSV files (gitignored)
│   ├── processed/                     # Preprocessed features and cache (gitignored)
│   ├── samples/                       # Micro-samples for testing and CI smoke tests
│   └── schemas/                       # Formal schema definitions and contracts
│
├── notebooks/                         # Interactive exploratory & visualization notebooks
│   ├── analysis/                      # Exploratory data profiling notebooks
│   ├── experiments/                   # Rapid prototyping notebooks
│   └── visualization/                 # Performance and trade-off visualization
│
├── src/business_entity_resolution/    # Core ML system package
│   ├── data/                          # Streaming data loaders & sampling
│   ├── normalization/                 # Name, address, and country standardizers
│   ├── features/                      # String similarity & cross-source features
│   ├── blocking/                      # Multi-pass candidate generation & pruning
│   ├── retrieval/                     # BM25, TF-IDF, and dense vector search
│   ├── matching/                      # GBDT and deep transformer classifiers
│   ├── decision/                      # Macro F0.5 calibration & singleton gating
│   ├── postprocessing/                # Format validation & TSV serializing
│   ├── evaluation/                    # Macro F0.5 evaluator & subgroup metrics
│   ├── utils/                         # Validation script & logging utilities
│   └── pipeline/                      # End-to-end execution orchestrators
│
├── configs/                           # Declarative configurations
│   ├── data/                          # Data path and sampling configurations
│   ├── features/                      # Feature extraction settings
│   ├── blocking/                      # Candidate generation parameters
│   ├── models/                        # Hyperparameters for ML models
│   └── experiments/                   # End-to-end experiment pipelines
│
├── experiments/                       # 15 Parallel experiment tracks
│   ├── kaggle/ (exp_01 - exp_06)      # GPU/TPU candidate generation & deep models
│   ├── colab/ (exp_01 - exp_03)       # Interactive ablation & model benchmarking
│   ├── local/ (exp_01 - exp_03)       # Fast CPU baselines & smoke tests
│   └── sagemaker/ (exp_01 - exp_03)   # Distributed indexing & full inference
│
├── outputs/                           # Ephemeral run artifacts (gitignored)
│   ├── candidates/                    # Generated candidate pair sets
│   ├── predictions/                   # Pairwise probability predictions
│   ├── models/                        # Serialized model checkpoints
│   ├── metrics/                       # Evaluation summaries and reports
│   ├── figures/                       # Plots and performance curves
│   └── logs/                          # Execution logs
│
├── reports/                           # Synthesized research reports
│   ├── data_profiling/                # EDA and schema reports
│   ├── blocking/                      # Candidate recall vs reduction ratio studies
│   ├── matching/                      # Model comparison & ablation reports
│   ├── experiments/                   # Experiment synthesis summaries
│   └── final/                         # Final consolidated write-up
│
├── submission/                        # Official submission package structure
│   ├── output/                        # matching_results.tsv & candidate_pairs.tsv
│   ├── code/business_entity_resolution/ # Standalone runnable pipeline & requirements
│   └── Documentation_template.md      # Official contest methodology write-up
│
└── team/                              # Team governance and tracking
    ├── experiment_registry.md         # Master experiment tracking ledger
    ├── experiment_assignments.md      # Task assignments and deliverables
    ├── insight_registry.md            # Empirical findings & architectural decisions
    ├── decisions.md                   # Architectural Decision Records (ADR)
    └── ownership.md                   # Module ownership and lead roles
```

---

## 4. Experiment Strategy & Governance
We manage **15 parallel experiment tracks** distributed across platforms:
- **Kaggle (6 tracks):** High-speed lexical blocking, phonetic indexing, dense vector retrieval, cross-encoder rerankers, hybrid candidate union, and F0.5 calibration.
- **Google Colab (3 tracks):** Preprocessing ablation, feature importance studies, and GBDT framework comparisons.
- **Local (3 tracks):** Leak-free CV split design, low-memory CPU blocking, and end-to-end validation smoke testing.
- **SageMaker (3 tracks):** Corpus-scale dense indexing, cross-encoder distillation, and full test inference.

All experiments are registered and tracked in [`team/experiment_registry.md`](file:///d:/Projects/Machine_Learning%20Projects/Terminal_Titans_submission/team/experiment_registry.md).

---

## 5. Where Key Assets Live
- **Problem & Requirements:** [`docs/problem_statement.md`](file:///d:/Projects/Machine_Learning%20Projects/Terminal_Titans_submission/docs/problem_statement.md)
- **EDA & Profiling:** [`docs/analysis/`](file:///d:/Projects/Machine_Learning%20Projects/Terminal_Titans_submission/docs/analysis/) and [`reports/data_profiling/`](file:///d:/Projects/Machine_Learning%20Projects/Terminal_Titans_submission/reports/data_profiling/)
- **Source Code:** [`src/business_entity_resolution/`](file:///d:/Projects/Machine_Learning%20Projects/Terminal_Titans_submission/src/business_entity_resolution/)
- **Final Submission Package:** [`submission/`](file:///d:/Projects/Machine_Learning%20Projects/Terminal_Titans_submission/submission/)

---

## 6. Data Policy
Raw competition data exceeds 2.5 GB and is strictly excluded from Git. Expected layout and schemas are documented in [`data/README.md`](file:///d:/Projects/Machine_Learning%20Projects/Terminal_Titans_submission/data/README.md).

---

## 7. Reproducibility Philosophy
- Pure deterministic execution with fixed random seeds (`seed=42`).
- Modular architecture with clear decoupling between candidate blocking, pairwise matching, and decisioning.
- Pre-submission validation enforced locally via [`src/business_entity_resolution/utils/validate_submission.py`](file:///d:/Projects/Machine_Learning%20Projects/Terminal_Titans_submission/src/business_entity_resolution/utils/validate_submission.py).
