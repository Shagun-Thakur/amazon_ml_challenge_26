# Subsystem Ownership & Roles

Mapping of technical modules and competition responsibilities across team roles.

| Subsystem Area | Lead Role / Assignee | Core Responsibilities |
|---|---|---|
| **Data Ingestion & Integrity** | [Team Member 1] | Schema validation, streaming TSV parsers, sample fixtures, dataset policies |
| **Validation & Evaluation** | [Team Member 2] | Leak-free stratified validation split, Macro F0.5 local evaluator, candidate recall metrics |
| **Blocking & Candidate Generation** | [Team Member 3] | Country partitioning, phonetic keys (Metaphone), BM25, and hybrid candidate union |
| **Retrieval & Vector Search** | [Team Member 4] | Bi-encoder fine-tuning, embedding cache generation, FAISS ANN vector index |
| **Matching & Feature Engineering** | [Team Member 1] | Tabular similarity features (Levenshtein, Jaccard, n-gram TF-IDF), GBDT models |
| **Advanced Neural Modeling** | [Team Member 2] | Cross-encoder architectures (DeBERTa-v3), hard-negative mining, distillation |
| **Infrastructure & Compute** | [Team Member 3] | Kaggle / Colab / SageMaker environment configurations, GPU utilization, distributed scripts |
| **Submission & Compliance** | [Team Member 4] | Submission package builder, validate_submission.py runner, format compliance |
| **Documentation & Governance** | [Repository Architect] | Architecture governance, READMEs, ADR maintenance, experiment registry oversight |
