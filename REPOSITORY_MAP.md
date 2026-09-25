# Repository Map — Amazon ML Challenge 2026

**Team:** Terminal Titans  
**Last Updated:** 2026-09-25  

This document provides a comprehensive structural guide to the repository and records the complete file migration history from the initial raw archive to the target architecture.

---

## 1. Complete Repository Tree

```
amazon-ml-2026/
├── README.md                                          # Architectural & project overview
├── LICENSE                                            # MIT Open-source license
├── requirements.txt                                   # Pinned development environment dependencies
├── .gitignore                                         # Hardened exclusions for datasets & weights
├── CONTRIBUTING.md                                    # Development workflow & experiment rules
├── REPOSITORY_MAP.md                                  # This master file map
├── repository_audit.md                                # Phase 0 audit report
├── repository_migration_notes.md                      # Detailed notes on paths & deferred refactoring
│
├── docs/                                              # Problem & strategic documentation
│   ├── problem_statement.md                           # Official problem description, schemas, rules
│   ├── strategy/
│   │   ├── challenge_strategy.md                      # High-level resolution funnel & F0.5 formulation
│   │   ├── arsenal.md                                 # Technical methods, distance metrics, algorithms
│   │   └── action_plan.md                             # Phased execution milestones
│   ├── analysis/
│   │   ├── data_profiling/README.md                   # EDA & data distribution analysis notes
│   │   ├── match_intelligence/README.md               # Qualitative noise & variation patterns
│   │   ├── blocking_analysis/README.md                # Candidate recall & reduction ratio reports
│   │   ├── error_analysis/README.md                   # False positive/negative failure diagnosis
│   │   └── experiment_reports/README.md               # Cross-track synthesized findings
│   └── submission/
│       ├── methodology.md                             # Final technical paper drafts
│       └── submission_notes.md                        # Submission guidelines & operational checklist
│
├── data/                                              # Data storage & governance
│   ├── README.md                                      # Data layout policy, schemas & guidelines
│   ├── raw/                                           # Excluded from git (contains raw ~2.52 GB TSVs)
│   │   ├── train/
│   │   │   ├── train_source1.tsv                      # Reference entities (~210 MB)
│   │   │   ├── train_source2.tsv                      # Noisy source 2 (~489 MB)
│   │   │   ├── train_source3.tsv                      # Noisy source 3 (~504 MB)
│   │   │   └── train_ground_truth.tsv                 # Ground truth matches (~127 MB)
│   │   └── test/
│   │       ├── test_source1.tsv                       # Reference test entities (~175 MB)
│   │       ├── test_source2.tsv                       # Noisy test source 2 (~509 MB)
│   │       └── test_source3.tsv                       # Noisy test source 3 (~506 MB)
│   ├── processed/README.md                            # Preprocessed / cached intermediate data
│   ├── samples/README.md                              # Micro-samples for fast CI/testing
│   └── schemas/README.md                              # Data schemas and contract definitions
│
├── notebooks/                                         # Interactive Jupyter research
│   ├── analysis/README.md                             # Exploratory analysis & profiling
│   ├── experiments/README.md                          # Prototyping & interactive modeling
│   └── visualization/README.md                        # Plots, calibration curves, distributions
│
├── src/business_entity_resolution/                    # Production ML codebase
│   ├── __init__.py / README.md                        # Package entry
│   ├── data/                                          # Data loading, generators, sampling
│   ├── normalization/                                 # Name, address, country normalizers
│   ├── features/                                      # Pairwise string, token, semantic features
│   ├── blocking/                                      # Exact, rule, phonetic, hybrid candidate generation
│   ├── retrieval/                                     # BM25, TF-IDF, dense FAISS indexing
│   ├── matching/                                      # GBDT and Transformer pairwise classifiers
│   ├── decision/                                      # F0.5 threshold optimization & singleton gate
│   ├── postprocessing/                                # Format validation & TSV generation
│   ├── evaluation/                                    # Exact Macro F0.5 & candidate recall metrics
│   ├── pipeline/                                      # End-to-end orchestration workflows
│   └── utils/
│       ├── validate_submission.py                     # Official submission validator
│       └── README.md                                  # Utilities documentation
│
├── configs/                                           # Declarative YAML configurations
│   ├── README.md
│   ├── data/README.md                                 # File paths, sampling, split fractions
│   ├── features/README.md                             # Distance metrics, tokenizers, n-grams
│   ├── blocking/README.md                             # Candidate generation keys & top-k thresholds
│   ├── models/README.md                               # GBDT, Cross-Encoder hyperparameters
│   └── experiments/README.md                          # Complete experiment configurations
│
├── experiments/                                       # 15 Parallel Experiment Tracks
│   ├── kaggle/                                        # Kaggle GPU/TPU tracks (exp_01 to exp_06)
│   ├── colab/                                         # Colab interactive tracks (exp_01 to exp_03)
│   ├── local/                                         # Local CPU baseline tracks (exp_01 to exp_03)
│   └── sagemaker/                                     # SageMaker distributed tracks (exp_01 to exp_03)
│
├── outputs/                                           # Ephemeral outputs (gitignored)
│   ├── candidates/README.md                           # Generated candidate pair sets
│   ├── predictions/README.md                          # Scored prediction files
│   ├── models/README.md                               # Checkpoints & weights
│   ├── metrics/README.md                              # Metric summaries
│   ├── figures/README.md                              # Evaluation graphs
│   └── logs/README.md                                 # Runtime logs
│
├── reports/                                           # Research synthesis reports
│   ├── data_profiling/README.md                       # Comprehensive data profiling reports
│   ├── blocking/README.md                             # Blocking performance benchmarks
│   ├── matching/README.md                             # Model comparison reports
│   ├── experiments/README.md                          # Experiment milestone summaries
│   └── final/README.md                                # Final solution report
│
├── submission/                                        # Exact bundle required for submission zip
│   ├── output/
│   │   ├── matching_results.tsv                       # Leaderboard upload (final matches)
│   │   └── candidate_pairs.tsv                        # Final candidate generation set
│   ├── code/business_entity_resolution/
│   │   ├── src/
│   │   │   └── utils/
│   │   │       └── validate_submission.py             # Validator copy for self-contained reproduction
│   │   ├── README.md                                  # Reproduction guide
│   │   └── requirements.txt                           # Pinned execution dependencies
│   └── Documentation_template.md                      # Official filled methodology report
│
└── team/                                              # Governance and tracking
    ├── experiment_registry.md                         # 15-track experiment registry
    ├── experiment_assignments.md                      # Research question assignments
    ├── insight_registry.md                            # Empirically verified findings
    ├── decisions.md                                   # Architectural Decision Records (ADRs)
    └── ownership.md                                   # Component ownership matrix
```

---

## 2. Complete File Migration Ledger

| Original Path | New Path | Action | Reason |
|---|---|---|---|
| `Documentation_template.md` | `submission/Documentation_template.md` | Moved | Required root file in final competition submission bundle. |
| `code/business_entity_resolution/src/dataset/README.md` | `docs/problem_statement.md` | Copied | Official problem statement, rules, schemas, and metric specification preserved. |
| `code/business_entity_resolution/src/utils/validate_submission.py` | `src/business_entity_resolution/utils/validate_submission.py` | Copied | Core repository validation utility for automated checks. |
| `code/business_entity_resolution/src/utils/validate_submission.py` | `submission/code/business_entity_resolution/src/utils/validate_submission.py` | Copied | Preserved inside standalone submission bundle for independent evaluation. |
| `code/business_entity_resolution/src/dataset/train/train_source1.tsv` | `data/raw/train/train_source1.tsv` | Moved | Raw training data reference source relocated to dedicated store (gitignored). |
| `code/business_entity_resolution/src/dataset/train/train_source2.tsv` | `data/raw/train/train_source2.tsv` | Moved | Raw training noisy source 2 relocated to dedicated store (gitignored). |
| `code/business_entity_resolution/src/dataset/train/train_source3.tsv` | `data/raw/train/train_source3.tsv` | Moved | Raw training noisy source 3 relocated to dedicated store (gitignored). |
| `code/business_entity_resolution/src/dataset/train/train_ground_truth.tsv` | `data/raw/train/train_ground_truth.tsv` | Moved | Raw training ground truth relocated to dedicated store (gitignored). |
| `code/business_entity_resolution/src/dataset/test/test_source1.tsv` | `data/raw/test/test_source1.tsv` | Moved | Raw test reference source relocated to dedicated store (gitignored). |
| `code/business_entity_resolution/src/dataset/test/test_source2.tsv` | `data/raw/test/test_source2.tsv` | Moved | Raw test noisy source 2 relocated to dedicated store (gitignored). |
| `code/business_entity_resolution/src/dataset/test/test_source3.tsv` | `data/raw/test/test_source3.tsv` | Moved | Raw test noisy source 3 relocated to dedicated store (gitignored). |
| `output/matching_results.tsv` | `submission/output/matching_results.tsv` | Moved | Submission output placeholder moved into submission package. |
| `output/candidate_pairs.tsv` | `submission/output/candidate_pairs.tsv` | Moved | Submission output placeholder moved into submission package. |
| `code/business_entity_resolution/README.md` | `submission/code/business_entity_resolution/README.md` | Moved | Submission code reproduction README. |
| `code/business_entity_resolution/requirements.txt` | `submission/code/business_entity_resolution/requirements.txt` | Moved | Submission code runtime requirements. |
| `code/business_entity_resolution/src/.DS_Store` | *Deleted* | Removed | OS-specific temporary cache artifact. |
| `code/business_entity_resolution/src/dataset/.DS_Store` | *Deleted* | Removed | OS-specific temporary cache artifact. |
| `code/` (root legacy folder) | *Deleted* | Cleaned | Consolidated into target `src/` and `submission/code/`. |
| `output/` (root legacy folder) | *Deleted* | Cleaned | Consolidated into target `outputs/` and `submission/output/`. |
