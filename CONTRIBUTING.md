# Contributing Guidelines — Amazon ML Challenge 2026

Welcome to the **Terminal Titans** Amazon ML Challenge 2026 development repository.

## 1. Golden Rules
1. **Never Commit Raw TSV Data:** The `data/raw/` directory and large TSV/model weight files are strictly gitignored.
2. **Never Implement ML Code Without Governance:** Register every experiment in `team/experiment_registry.md` before launching runs.
3. **Preserve Subgroup & Metric Integrity:** All validation must evaluate Macro $F_{0.5}$ including singleton credits/penalties.
4. **Zero External Lookup:** No external search APIs, web scrapers, or geocoding services. Doing so causes immediate disqualification.

## 2. Parallel Experiment Protocol
- Experiment slots are numbered across Kaggle (`exp_01` to `exp_06`), Colab (`exp_01` to `exp_03`), Local (`exp_01` to `exp_03`), and SageMaker (`exp_01` to `exp_03`).
- Each experiment directory contains `README.md`, `config.yaml`, `notes.md`, `results/`, and `artifacts/`.
- Update `team/experiment_registry.md` when starting, updating, or concluding an experiment.

## 3. Pre-Submission Checklist
- Run local validator:
  ```bash
  python src/business_entity_resolution/utils/validate_submission.py \
      --matching submission/output/matching_results.tsv \
      --candidate submission/output/candidate_pairs.tsv \
      --test-dir data/raw/test
  ```
- Ensure clean exit code 0 (`PASS`).
