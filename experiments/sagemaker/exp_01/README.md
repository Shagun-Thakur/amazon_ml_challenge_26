# SageMaker Exp 01: Full-Scale Dense Corpus Indexing

## Owner
[team member]

## Platform
SageMaker

## Objective
Scale dense embedding generation across all ~1.7M entities using multi-GPU instances.

## Hypothesis
Batched GPU inference can embed the complete entity corpus in under 2 hours, generating high-quality FAISS index.

## Pipeline
Sharded Text Ingestion -> Multi-GPU Bi-Encoder Inference -> FAISS HNSW Index Construction

## Variables
Batch size, FP16 precision, FAISS index parameters (M, efSearch).

## Fixed Controls
Full training and test dataset records.

## Metrics
- Candidate Recall
- Reduction Ratio
- Precision
- Recall
- Macro F0.5
- Runtime
- Memory / compute cost

## Expected Insight
Embedding throughput (entities/sec) and vector recall.

## Result
To be filled after experiment.

## Decision
PENDING (KEEP / REJECT / INVESTIGATE)

## Follow-up
What the result implies for the next experiment.
