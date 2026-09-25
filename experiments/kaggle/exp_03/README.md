# Kaggle Exp 03: Dense Vector Bi-Encoder Retrieval

## Owner
[team member]

## Platform
Kaggle

## Objective
Test semantic vector candidate generation using Sentence-Transformers (BGE-small / MiniLM) with FAISS.

## Hypothesis
Dense bi-encoder retrieval will capture semantic address variations and landmark descriptions missed by lexical rules.

## Pipeline
Bi-Encoder Embedding -> FAISS Indexing -> Top-k Nearest Neighbor Retrieval -> LightGBM Scoring

## Variables
Embedding model architecture, cosine similarity cutoff, top-k candidate threshold.

## Fixed Controls
Validation set, downstream classifier features.

## Metrics
- Candidate Recall
- Reduction Ratio
- Precision
- Recall
- Macro F0.5
- Runtime
- Memory / compute cost

## Expected Insight
Complementarity of dense candidate set compared to lexical candidates.

## Result
To be filled after experiment.

## Decision
PENDING (KEEP / REJECT / INVESTIGATE)

## Follow-up
What the result implies for the next experiment.
