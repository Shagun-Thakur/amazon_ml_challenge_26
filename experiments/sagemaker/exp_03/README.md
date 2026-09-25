# SageMaker Exp 03: Full Test Set Inference & Candidate Pairs Scaling

## Owner
[team member]

## Platform
SageMaker

## Objective
Execute full-scale inference over complete test set to generate final competition submission files.

## Hypothesis
Distributed batch inference will successfully produce matching_results.tsv and candidate_pairs.tsv within memory limits.

## Pipeline
Test Set Partitioning -> Distributed Candidate Search -> Model Scoring -> Output Assembly

## Variables
Worker concurrency, stream chunk size.

## Fixed Controls
Exact competition test files.

## Metrics
- Candidate Recall
- Reduction Ratio
- Precision
- Recall
- Macro F0.5
- Runtime
- Memory / compute cost

## Expected Insight
Total test generation time, memory ceiling, final candidate set size.

## Result
To be filled after experiment.

## Decision
PENDING (KEEP / REJECT / INVESTIGATE)

## Follow-up
What the result implies for the next experiment.
