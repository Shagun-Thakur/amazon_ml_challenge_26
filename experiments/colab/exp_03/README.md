# Colab Exp 03: Model Family Benchmarking

## Owner
[team member]

## Platform
Colab

## Objective
Benchmark LightGBM, CatBoost, and XGBoost on identical tabular pairwise feature sets.

## Hypothesis
CatBoost will perform best on categorical/country interactions, while LightGBM will offer 5x faster training speed.

## Pipeline
Extracted Feature Matrix -> LightGBM vs CatBoost vs XGBoost -> Metric & Speed Comparison

## Variables
Model algorithm and loss functions (binary logloss vs pairwise ranker).

## Fixed Controls
Identical train/val feature tables.

## Metrics
- Candidate Recall
- Reduction Ratio
- Precision
- Recall
- Macro F0.5
- Runtime
- Memory / compute cost

## Expected Insight
F0.5 comparison, training duration, and RAM consumption across libraries.

## Result
To be filled after experiment.

## Decision
PENDING (KEEP / REJECT / INVESTIGATE)

## Follow-up
What the result implies for the next experiment.
