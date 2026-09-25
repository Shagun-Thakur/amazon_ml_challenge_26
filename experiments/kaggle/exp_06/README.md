# Kaggle Exp 06: Macro F0.5 Calibration & Dynamic Singleton Gating

## Owner
[team member]

## Platform
Kaggle

## Objective
Calibrate decision thresholds and develop dedicated singleton gating to optimize the Macro F0.5 objective.

## Hypothesis
Aggressive singleton gating and threshold tuning favoring precision will lift Macro F0.5 by >= 0.04 over default 0.5 threshold.

## Pipeline
Pair Probabilities -> Isotonic Calibration -> Dynamic Per-Entity Thresholding -> Singleton Gate

## Variables
Probability threshold values, singleton confidence thresholds.

## Fixed Controls
Predicted probabilities from best matching model.

## Metrics
- Candidate Recall
- Reduction Ratio
- Precision
- Recall
- Macro F0.5
- Runtime
- Memory / compute cost

## Expected Insight
Optimal operating threshold for precision-weighted F0.5.

## Result
To be filled after experiment.

## Decision
PENDING (KEEP / REJECT / INVESTIGATE)

## Follow-up
What the result implies for the next experiment.
