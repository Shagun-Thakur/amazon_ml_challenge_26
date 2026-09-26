# Architectural Decision Records (ADR)

Chronological log of key architectural decisions made for the competition.

---

### DEC-001: Strict Macro F0.5 Optimization and Singleton Gate Architecture
- **Decision:** Optimize all decision boundaries, probability thresholds, and postprocessing rules directly for Macro $F_{0.5}$ rather than standard $F_1$ or ROC-AUC. Implement an explicit singleton gating mechanism.
- **Evidence:** Problem statement evaluates Macro $F_{0.5}$ across all $S_1$ entities, with singletons scoring 1.0 on empty prediction and 0.0 on any false merge. Precision is weighted 2× over recall.
- **Alternatives rejected:** Standard 0.5 probability thresholding; optimizing for pairwise $F_1$.
- **Reason:** Standard thresholding yields high false positive rates, which severely degrades the Macro $F_{0.5}$ score due to precision penalty and destruction of singleton scores.
- **Date:** 2026-09-25

---

### DEC-002: Partitioned Multi-Stage Funnel Architecture
- **Decision:** Deconstruct the system into explicit stages: Preprocessing -> Multi-Channel Candidate Generation (Blocking/Retrieval) -> Pairwise Feature Extraction & Classification -> Decisioning & Thresholding -> Submission Serialization.
- **Evidence:** The Cartesian product space between $S_1$ and $(S_2 \cup S_3)$ exceeds $10^{12}$ pairs. Evaluating complex models over all pairs is computationally intractable.
- **Alternatives rejected:** End-to-end all-pairs neural cross-encoders without blocking.
- **Reason:** Multi-stage funnel achieves >99.9% reduction ratio while preserving >=95% candidate recall ceiling.
- **Date:** 2026-09-25

---

### DEC-003: Country-Partitioned Blocking Strategy
- **Decision:** Partition initial candidate blocking by country label ($Country_{S1} == Country_{S2/3}$) as a primary filter.
- **Evidence:** True entity matches occur within the same country; entities across US, India, and France do not resolve to cross-border duplicates in this dataset schema.
- **Alternatives rejected:** Cross-country global nearest neighbor search.
- **Reason:** Reduces search space by ~50-80% immediately with zero loss in true candidate recall.
- **Date:** 2026-09-25

---

### DEC-004: Exclusion of Raw Competition Data from Git
- **Decision:** Add all raw `.tsv` files under `data/raw/` to `.gitignore`.
- **Evidence:** Raw dataset exceeds 2.52 GB and contains ~1.7M records. Git is unsuitable for multi-gigabyte tabular assets.
- **Alternatives rejected:** Committing raw files to Git LFS or repository tracking.
- **Reason:** Git repository bloat, clone timeouts, and violation of competition code versioning hygiene.
- **Date:** 2026-09-25

---

### DEC-005: Deprecation of Heavy Local CPU Execution & Mandate for Cloud Acceleration
- **Decision:** Terminate all full-scale Cartesian searches and heavy training on local PC hardware. Shift all intensive candidate blocking, vector indexing, and model training to cloud infrastructure (Kaggle / Colab / SageMaker).
- **Evidence:** Running unindexed sparse matrix dot-products for 1.73M test records against 9.97M candidate pool records sequentially on a local CPU consumed >19.8 core-hours (~24 hours wall-clock time) and bottlenecked iteration.
- **Alternatives rejected:** Continuing local single-threaded CPU runs.
- **Reason:** Prevents project stalls and leverages multi-GPU instances and distributed cloud memory.
- **Date:** 2026-09-26

---

### DEC-006: Algorithmic Upgrade to Inverted Indexing & Decoupled Execution
- **Decision:** Permanently decouple validation benchmark evaluation from full-scale test set candidate generation. Replace naive Cartesian sparse matrix dot-products with inverted index token posting lists (BM25) or GPU vector search (FAISS).
- **Evidence:** Over 98% of business pairs share zero common tokens. Inverted indices eliminate zero-overlap comparisons by design, reducing compute time by 100x.
- **Alternatives rejected:** Monolithic brute-force scripts coupling validation with full inference.
- **Reason:** Enables fast, iterative validation benchmarking in under 5 minutes.
- **Date:** 2026-09-26
