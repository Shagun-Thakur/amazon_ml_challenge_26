# Kaggle Exp 01: Fast Lexical Baseline

## Owner
[team member]

## Platform
Kaggle

## Objective
Establish end-to-end baseline pipeline using country-partitioned lexical blocking and LightGBM pair scoring.

## Hypothesis
Country-partitioned lexical blocking will achieve >90% reduction ratio with fast runtime, establishing our initial validation Macro F0.5 benchmark.

## Pipeline
Country Filter -> Token Overlap Candidate Generation -> Basic String Features -> LightGBM Classifier -> Fixed Threshold (0.5)

## Variables
Initial baseline features and default LightGBM hyperparameters.

## Fixed Controls
Fixed validation split, raw TSV training inputs, official F0.5 metric.

## Metrics
- Candidate Recall
- Reduction Ratio
- Precision
- Recall
- Macro F0.5
- Runtime
- Memory / compute cost

## Expected Insight
Baseline candidate recall, baseline macro F0.5, pipeline runtime on Kaggle CPU/GPU.

## Result
To be filled after experiment.

## Decision
PENDING (KEEP / REJECT / INVESTIGATE)

## Follow-up
What the result implies for the next experiment.
