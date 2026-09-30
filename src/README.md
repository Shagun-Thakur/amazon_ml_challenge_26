# Business Entity Resolution Package (`src`)

Modular production ML system architecture for Amazon ML Challenge 2026 (Business Entity Resolution).

---

## 1. Package Architecture

The package is partitioned into decoupled, single-responsibility modules:

| Submodule | Responsibility | Key Interfaces & Files |
|---|---|---|
| [`src/data/`](file:///d:/Projects/Machine_Learning%20Projects/Terminal_Titans_submission/src/data/) | Ingestion, safe TSV parsers, schema audits, train/val split generation | Schemas, data loaders, stratified sampling |
| [`src/normalization/`](file:///d:/Projects/Machine_Learning%20Projects/Terminal_Titans_submission/src/normalization/) | Text canonicalization, legal corporate suffix stripping, address expansions | Unicode NFKD, address lexicons |
| [`src/features/`](file:///d:/Projects/Machine_Learning%20Projects/Terminal_Titans_submission/src/features/) | Pairwise similarity metrics, token overlap, numeric matches | Jaccard, Levenshtein, Jaro-Winkler, TF-IDF cosine |
| [`src/blocking/`](file:///d:/Projects/Machine_Learning%20Projects/Terminal_Titans_submission/src/blocking/) | Candidate generation & search space reduction | Rule blocking, phonetic keys, TF-IDF character n-grams |
| [`src/retrieval/`](file:///d:/Projects/Machine_Learning%20Projects/Terminal_Titans_submission/src/retrieval/) | High-scale sparse and dense candidate indexing | BM25, FAISS ANN vector search, bi-encoders |
| [`src/matching/`](file:///d:/Projects/Machine_Learning%20Projects/Terminal_Titans_submission/src/matching/) | Supervised pairwise classification & neural ranking | GBDTs (XGBoost, LightGBM, CatBoost), cross-encoders |
| [`src/decision/`](file:///d:/Projects/Machine_Learning%20Projects/Terminal_Titans_submission/src/decision/) | Global decision policies & Macro F0.5 calibration | Singleton threshold gating ($\tau$), score calibration |
| [`src/postprocessing/`](file:///d:/Projects/Machine_Learning%20Projects/Terminal_Titans_submission/src/postprocessing/) | Submission formatting, duplicate elimination, integrity checks | Format validation, TSV serializing |
| [`src/evaluation/`](file:///d:/Projects/Machine_Learning%20Projects/Terminal_Titans_submission/src/evaluation/) | Competition metrics evaluation | Exact Macro $F_{0.5}$, candidate recall, reduction ratio |
| [`src/pipeline/`](file:///d:/Projects/Machine_Learning%20Projects/Terminal_Titans_submission/src/pipeline/) | End-to-end orchestration workflows | Multi-stage pipeline execution |
| [`src/utils/`](file:///d:/Projects/Machine_Learning%20Projects/Terminal_Titans_submission/src/utils/) | Validation scripts, seed controls, file I/O | [`validate_submission.py`](file:///d:/Projects/Machine_Learning%20Projects/Terminal_Titans_submission/src/utils/validate_submission.py) |

---

## 2. Baseline Implementation Notice

The initial operational baseline scripts authored by the team (including `pipeline_clean.py`, `blocking.py`, `features.py`, and `train_and_predict.py`) are located in [`experiments/baseline/`](file:///d:/Projects/Machine_Learning%20Projects/Terminal_Titans_submission/experiments/baseline/). As components mature through the experiment tracks, they are promoted into the modular `src/` modules above.

---

## 3. Submission Verification

To validate that generated submission files conform to official competition formatting rules:

```bash
python src/utils/validate_submission.py \
    --matching submission/output/matching_results.tsv \
    --candidate submission/output/candidate_pairs.tsv \
    --test-dir data/raw/test
```
