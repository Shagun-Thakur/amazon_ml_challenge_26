# Blocking Reports (`reports/blocking`)

This directory contains benchmark reports, reduction ratio analyses, and recall evaluations for candidate blocking algorithms.

---

## 1. Directory Contents

| Directory / File | Description | Key Findings |
|---|---|---|
| [`retrieval_benchmark/`](file:///d:/Projects/Machine_Learning%20Projects/Terminal_Titans_submission/reports/blocking/retrieval_benchmark/) | Systematic candidate retrieval benchmark on 20,000 $S_1$ validation records against $S_2$ and $S_3$. | [`retrieval_benchmark_report.md`](file:///d:/Projects/Machine_Learning%20Projects/Terminal_Titans_submission/reports/blocking/retrieval_benchmark/retrieval_benchmark_report.md) and [`retrieval_benchmark_metadata.json`](file:///d:/Projects/Machine_Learning%20Projects/Terminal_Titans_submission/reports/blocking/retrieval_benchmark/retrieval_benchmark_metadata.json) |

### Key Benchmark Takeaways
- **Character TF-IDF (3,4) N-grams ($top\_k=50$):**
  - $S_2$: 98.66% pair recall, 99.09% $S_1$-any recall, 97.71% $S_1$-all recall (runtime: 208s).
  - $S_3$: 98.80% pair recall, 99.45% $S_1$-any recall, 97.89% $S_1$-all recall (runtime: 204s).
- **Exact Structural Union:**
  - $S_2$: 84.01% pair recall (avg 2,220 candidates/S1).
  - $S_3$: 85.73% pair recall (avg 2,273 candidates/S1).
- **Conclusion:** Character TF-IDF provides superior candidate recall while reducing candidate pool size from >2,200 to 50 candidates per entity.

---

## 2. Generator Code
- Benchmark runner: [`experiments/baseline/blocking.py`](file:///d:/Projects/Machine_Learning%20Projects/Terminal_Titans_submission/experiments/baseline/blocking.py) (`python experiments/baseline/blocking.py --mode benchmark`)
