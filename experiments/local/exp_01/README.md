# Local Exp 01: Leak-Free Validation Split Design

## Owner
[team member]

## Platform
Local

## Objective
Design and verify a stratified, leak-free local validation split accurately reflecting the test set characteristics.

## Hypothesis
Splitting by reference entities (S1) with representative singleton ratios and country proportions will produce reliable local CV.

## Pipeline
Stratified Split Generation -> Entity Leakage Audit -> Singleton Distribution Verification

## Variables
Split methodology (pure random vs stratified by country and match cardinality).

## Fixed Controls
Ground truth dataset train_ground_truth.tsv.

## Metrics
- Candidate Recall
- Reduction Ratio
- Precision
- Recall
- Macro F0.5
- Runtime
- Memory / compute cost

## Expected Insight
Validation set variance and alignment with expected competition evaluation.

## Result
To be filled after experiment.

## Decision
PENDING (KEEP / REJECT / INVESTIGATE)

## Follow-up
What the result implies for the next experiment.
