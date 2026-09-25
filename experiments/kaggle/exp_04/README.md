# Kaggle Exp 04: Cross-Encoder Transformer Reranker

## Owner
[team member]

## Platform
Kaggle

## Objective
Train a cross-encoder (DeBERTa-v3-small) on top-k candidates to capture complex non-linear cross-field interactions.

## Hypothesis
Cross-encoder scoring will increase pairwise precision, significantly lifting Macro F0.5.

## Pipeline
Multi-Pass Candidates -> DeBERTa-v3-small Cross-Encoder Reranker -> Threshold Optimization

## Variables
Transformer backbone, max sequence length, learning rate schedule.

## Fixed Controls
Pre-computed candidate pool from best blocking track.

## Metrics
- Candidate Recall
- Reduction Ratio
- Precision
- Recall
- Macro F0.5
- Runtime
- Memory / compute cost

## Expected Insight
Precision gain on tricky false positives and inference throughput (pairs/sec).

## Result
To be filled after experiment.

## Decision
PENDING (KEEP / REJECT / INVESTIGATE)

## Follow-up
What the result implies for the next experiment.
