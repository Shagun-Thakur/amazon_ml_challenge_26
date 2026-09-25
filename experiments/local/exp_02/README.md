# Local Exp 02: Pure Lexical High-Speed Blocking

## Owner
[team member]

## Platform
Local

## Objective
Implement ultra-fast, memory-efficient sparse blocking capable of running on CPU in under 5 minutes.

## Hypothesis
Optimized sparse token inverted indices can achieve 90% candidate recall with < 2GB RAM usage.

## Pipeline
Country Partition -> Sparse Token Matrix -> Cosine Candidate Thresholding

## Variables
Minimum token length, stopword removal, candidate top-k limits.

## Fixed Controls
Local CPU hardware, RAM limit 8GB.

## Metrics
- Candidate Recall
- Reduction Ratio
- Precision
- Recall
- Macro F0.5
- Runtime
- Memory / compute cost

## Expected Insight
Throughput (records/sec) and peak memory usage.

## Result
To be filled after experiment.

## Decision
PENDING (KEEP / REJECT / INVESTIGATE)

## Follow-up
What the result implies for the next experiment.
