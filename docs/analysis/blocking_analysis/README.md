# Blocking & Candidate Generation Analysis (`docs/analysis/blocking_analysis`)

Evaluations of candidate generation filters, blocking strategies, and retrieval recall trade-offs.

---

## 1. Key Evaluation Metrics
- **Pair Completeness (Candidate Recall):**
  $$\text{Recall} = \frac{|\text{True Matches in Candidates}|}{|\text{Total True Matches}|}$$
- **Reduction Ratio (RR):**
  $$\text{RR} = 1 - \frac{|\text{Candidates}|}{|S_1| \times (|S_2| + |S_3|)}$$
- **Candidate Size:** Mean/median candidate pool size per $S_1$ entity (target: $\le 50$ candidates per entity).

---

## 2. Empirical Benchmark Findings
- **Character TF-IDF N-grams (3,4):** Achieves **>98.6% candidate recall** on validation sets with $top\_k=50$, outperforming exact structural blocking by +13–14% absolute recall.
- **Inverted Index Requirement:** Dense brute-force pairwise dot products locally take $O(N \times M)$ CPU time (~71k seconds); sparse inverted indexing or GPU FAISS vector search is required for scaling across the full 1.73M test set.

---

## 3. Related Reports & Scripts
- Retrieval benchmark report: [`reports/blocking/retrieval_benchmark/retrieval_benchmark_report.md`](file:///d:/Projects/Machine_Learning%20Projects/Terminal_Titans_submission/reports/blocking/retrieval_benchmark/retrieval_benchmark_report.md)
- Benchmark implementation: [`experiments/baseline/blocking.py`](file:///d:/Projects/Machine_Learning%20Projects/Terminal_Titans_submission/experiments/baseline/blocking.py)
