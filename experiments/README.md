# Experiments Directory (`experiments`)

This directory houses the baseline implementation and the **15 parallel experiment tracks** distributed across local and cloud environments for the Amazon ML Challenge 2026.

---

## 1. Directory Structure

```
experiments/
├── README.md                      # This overview document
├── baseline/                      # Fully functional end-to-end baseline pipeline
│   ├── pipeline_clean.py          # Stage 1 Ingestion, Audit, Normalization
│   ├── blocking.py                # Dual-channel TF-IDF n-gram candidate blocker
│   ├── features.py                # Pairwise feature extraction
│   ├── train_and_predict.py       # Baseline classifier training and scoring
│   ├── text_normalizer.py         # Unicode, legal suffix, address normalization
│   ├── structural_features.py     # Numeric token and composite string extraction
│   ├── gt_profiler.py             # Ground truth topology analysis
│   ├── audits.py                  # Table-level schema and quality audits
│   └── utils_io.py                # Environment-aware TSV I/O utilities
│
├── kaggle/                        # Kaggle GPU/TPU tracks (exp_01 to exp_06)
│   ├── exp_01/                    # High-speed lexical blocking (BM25 / inverted index)
│   ├── exp_02/                    # Phonetic indexing & country-partitioned hashing
│   ├── exp_03/                    # Dense vector retrieval (Bi-Encoder embeddings)
│   ├── exp_04/                    # Cross-encoder neural rerankers
│   ├── exp_05/                    # Multi-pass hybrid candidate set union
│   └── exp_06/                    # Post-processing & Macro F0.5 calibration
│
├── colab/                         # Google Colab interactive tracks (exp_01 to exp_03)
│   ├── exp_01/                    # Preprocessing & text normalization ablation
│   ├── exp_02/                    # Feature importance & ablation studies
│   └── exp_03/                    # GBDT model exploration (LightGBM, XGBoost, CatBoost)
│
├── local/                         # Local CPU development tracks (exp_01 to exp_03)
│   ├── exp_01/                    # Leak-free CV split design & evaluation harness
│   ├── exp_02/                    # Memory-constrained CPU candidate generation
│   └── exp_03/                    # End-to-end integration & submission smoke testing
│
└── sagemaker/                     # AWS SageMaker distributed tracks (exp_01 to exp_03)
    ├── exp_01/                    # Corpus-scale FAISS dense index construction
    ├── exp_02/                    # Knowledge distillation from transformer cross-encoders
    └── exp_03/                    # Full test corpus inference & submission packaging
```

---

## 2. Experiment Tracking & Governance

Every experiment follows a strict protocol registered in [`team_communication/experiment_registry.md`](file:///d:/Projects/Machine_Learning%20Projects/Terminal_Titans_submission/team_communication/experiment_registry.md):

1. **Pre-Run:** Register hypothesis, variable changes, and fixed controls in the track README (`experiments/<platform>/<exp_id>/README.md`).
2. **Execution:** Record runtime, memory usage, and primary competition metric (Macro $F_{0.5}$).
3. **Post-Run:** Update `team_communication/experiment_registry.md` with status (`KEEP`, `REJECT`, or `INVESTIGATE`) and synthesize key findings into [`team_communication/insight_registry.md`](file:///d:/Projects/Machine_Learning%20Projects/Terminal_Titans_submission/team_communication/insight_registry.md).

For the runnable baseline code and reproduction instructions, see [`experiments/baseline/README.md`](file:///d:/Projects/Machine_Learning%20Projects/Terminal_Titans_submission/experiments/baseline/README.md).
