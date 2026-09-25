# Colab Exp 02: Feature Ablation Study

## Owner
[team member]

## Platform
Colab

## Objective
Ablate individual feature groups (string metrics, token sets, n-gram TF-IDF, numeric PIN matches) to identify top signal drivers.

## Hypothesis
Combined token Jaccard and Levenshtein will provide 70% of feature importance, while numeric postal matches prevent false merges.

## Pipeline
Systematic Feature Group Drop -> LightGBM Training -> Validation Performance Evaluation

## Variables
Active feature subset in model training.

## Fixed Controls
Candidate pairs, model hyperparameters, evaluation split.

## Metrics
- Candidate Recall
- Reduction Ratio
- Precision
- Recall
- Macro F0.5
- Runtime
- Memory / compute cost

## Expected Insight
Feature importance ranking and minimal high-performing feature set.

## Result
To be filled after experiment.

## Decision
PENDING (KEEP / REJECT / INVESTIGATE)

## Follow-up
What the result implies for the next experiment.
