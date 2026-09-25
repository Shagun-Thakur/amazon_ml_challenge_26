# SageMaker Exp 02: Deep Cross-Encoder Fine-Tuning & Distillation

## Owner
[team member]

## Platform
SageMaker

## Objective
Fine-tune DeBERTa-v3-base on hard negative pairs and explore knowledge distillation into a compact student model.

## Hypothesis
Hard-negative fine-tuning will resolve fine-grained address confusions, providing our highest single-model precision.

## Pipeline
Hard Negative Mining -> Transformer Fine-Tuning -> Model Checkpoint Export

## Variables
Hard negative ratio, learning rate, warm-up steps.

## Fixed Controls
Target architecture constraint (<= 8B parameters, MIT/Apache 2.0).

## Metrics
- Candidate Recall
- Reduction Ratio
- Precision
- Recall
- Macro F0.5
- Runtime
- Memory / compute cost

## Expected Insight
Pair classification accuracy, ROC-AUC, and distilled inference latency.

## Result
To be filled after experiment.

## Decision
PENDING (KEEP / REJECT / INVESTIGATE)

## Follow-up
What the result implies for the next experiment.
