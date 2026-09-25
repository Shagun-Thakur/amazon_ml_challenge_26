# Business Entity Resolution Package

Core ML system architecture for Amazon ML Challenge 2026.
Modules:
- data: Data ingestion, schema validation, and sampling.
- normalization: Name, address, and country text normalization.
- features: Pairwise similarity and cross-source feature engineering.
- blocking: Multi-pass candidate generation and pruning.
- retrieval: BM25, TF-IDF, dense retrieval, and ANN indexing.
- matching: Pairwise classification and neural ranking models.
- decision: Macro F0.5 threshold optimization and singleton gating.
- postprocessing: Integrity constraints and TSV formatting.
- evaluation: Macro F0.5, candidate recall, and reduction ratio metrics.
- pipeline: End-to-end execution orchestrators.
- utils: Validation, config, and logging utilities.
