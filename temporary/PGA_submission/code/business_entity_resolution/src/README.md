# Business Entity Resolution Pipeline — Generator A + Downstream Matcher

## Overview
This package contains the authoritative supervised entity matcher and test predictions.
- **Candidate Pool Source:** Generator A (`candidate_pairs.tsv`) produced via fine-tuned `all-MiniLM-L6-v2` (MNRL objective) and high-fidelity country-partitioned FAISS ANN.
- **Scope Notice:** This packaged codebase reproduces pairwise feature extraction, candidate scoring, and final matching directly from `candidate_pairs.tsv`. (Candidate generation was executed in Phase-1 using the separate FAISS/GPU dense index).

## Candidate Statistics
- Total S1 Queries Evaluated: 1,732,544
- Total Candidate Pairs Scored: 86,384,410
- Mean Candidates per S1: 49.86

## Matcher & Feature Engineering
- **Model:** XGBoost
- **Feature Count:** 25 authentic pairwise features.
- **Decision Threshold:** tau = 0.84
- **Entity Macro-F0.5 (Validation):** 0.9700
- **Singleton Accuracy (Validation):** 85.65%

## Execution & Scoring
```bash
pip install -r requirements.txt
python feature_engineering.py
```
Output matches are written to `output/matching_results.tsv`.
