# Kaggle Exp 02: Phonetic & Character N-Gram Blocking

## Owner
[team member]

## Platform
Kaggle

## Objective
Evaluate phonetic encodings (Double Metaphone) and character 3-grams to recover typo-corrupted business names.

## Hypothesis
Phonetic and character n-gram blocking will increase Candidate Recall by >= 5 percentage points over token matching alone.

## Pipeline
Country Filter -> Phonetic Keys + Char 3-gram Inverted Index -> Union Candidate Pool -> LightGBM Pair Scorer

## Variables
Blocking key generation strategies (Metaphone, n-gram sizes).

## Fixed Controls
Identical pair classifier, evaluation split, and hardware environment.

## Metrics
- Candidate Recall
- Reduction Ratio
- Precision
- Recall
- Macro F0.5
- Runtime
- Memory / compute cost

## Expected Insight
Candidate Recall gain versus candidate pool size expansion.

## Result
To be filled after experiment.

## Decision
PENDING (KEEP / REJECT / INVESTIGATE)

## Follow-up
What the result implies for the next experiment.
