# Kaggle Exp 05: Multi-Pass Hybrid Union Blocking

## Owner
[team member]

## Platform
Kaggle

## Objective
Construct an ensemble candidate generator unioning lexical, phonetic, and dense retrieval channels.

## Hypothesis
Hybrid union will achieve >= 96% candidate recall ceiling while pruning 99.9% of non-matching pairs.

## Pipeline
Lexical BM25 U Phonetic Keys U Dense FAISS -> Multi-Channel Fusion & Pruning -> Candidate TSV

## Variables
Per-channel candidate caps and fusion ranking thresholds.

## Fixed Controls
Standard evaluation ground truth, macro F0.5.

## Metrics
- Candidate Recall
- Reduction Ratio
- Precision
- Recall
- Macro F0.5
- Runtime
- Memory / compute cost

## Expected Insight
Optimal balance between candidate recall ceiling and inference budget.

## Result
To be filled after experiment.

## Decision
PENDING (KEEP / REJECT / INVESTIGATE)

## Follow-up
What the result implies for the next experiment.
