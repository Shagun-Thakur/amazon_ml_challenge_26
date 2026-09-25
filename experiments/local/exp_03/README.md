# Local Exp 03: End-to-End Pipeline Smoke Test & Validation

## Owner
[team member]

## Platform
Local

## Objective
Test full pipeline execution from data ingestion to submission file output and validate with validate_submission.py.

## Hypothesis
Pipeline runs end-to-end without errors and passes all strict validator checks with exit code 0.

## Pipeline
Data Ingestion -> Candidate Generation -> Pair Inference -> TSV Formatting -> validate_submission.py

## Variables
Batch sizes, output paths, file streaming parameters.

## Fixed Controls
Official validation script requirements.

## Metrics
- Candidate Recall
- Reduction Ratio
- Precision
- Recall
- Macro F0.5
- Runtime
- Memory / compute cost

## Expected Insight
Zero validation warnings/errors, clean exit code 0.

## Result
To be filled after experiment.

## Decision
PENDING (KEEP / REJECT / INVESTIGATE)

## Follow-up
What the result implies for the next experiment.
