# Colab Exp 01: Preprocessing & Legal Suffix Normalization

## Owner
[team member]

## Platform
Colab

## Objective
Quantify the performance gain from cleaning business legal suffixes, punctuation, and address abbreviations.

## Hypothesis
Standardizing corporate suffixes (Pvt Ltd, LLC, Corp) will dramatically reduce false mismatches in lexical matching.

## Pipeline
Raw Text vs Standardized Text -> Lexical Inverted Index -> Pairwise Feature Similarity

## Variables
Normalization regex patterns, legal suffix dictionary, address expansion maps.

## Fixed Controls
Fixed blocking rules and classifier.

## Metrics
- Candidate Recall
- Reduction Ratio
- Precision
- Recall
- Macro F0.5
- Runtime
- Memory / compute cost

## Expected Insight
Net change in token overlap scores across true match pairs.

## Result
To be filled after experiment.

## Decision
PENDING (KEEP / REJECT / INVESTIGATE)

## Follow-up
What the result implies for the next experiment.
