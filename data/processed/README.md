# Processed Data Directory

This directory stores intermediate artifacts, cached tokenizations, cleaned records, and engineered feature tables.

## Rules:
- All generated processed artifacts are ephemeral and excluded from git via `.gitignore`.
- Files stored here are deterministically regenerable using `experiments/baseline/pipeline_clean.py` or the modular pipelines in `src/normalization/` and `src/features/`.
