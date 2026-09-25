# Repository Migration Notes

**Date:** 2026-09-25  
**Auditor / Architect:** Antigravity  

This document logs all path adjustments, deferred refactorings, and operational notes arising from the migration of the initial competition resource bundle into the standardized architecture.

---

## 1. Relocated Files & Default Path Impacts

### A. Official Validator (`validate_submission.py`)
- **Original Location:** `code/business_entity_resolution/src/utils/validate_submission.py`
- **New Primary Location:** `src/business_entity_resolution/utils/validate_submission.py`
- **Submission Mirror:** `submission/code/business_entity_resolution/src/utils/validate_submission.py`
- **Path Reference Note:**
  The script's default CLI arguments in `validate_submission.py` were:
  - `--matching output/matching_results.tsv`
  - `--candidate output/candidate_pairs.tsv`
  - `--test-dir dataset/test`
  In our repository, those defaults correspond to:
  - `--matching submission/output/matching_results.tsv`
  - `--candidate submission/output/candidate_pairs.tsv`
  - `--test-dir data/raw/test`
  *Action:* When invoking the validator from the project root, always supply the explicit paths or pass `--matching submission/output/matching_results.tsv --candidate submission/output/candidate_pairs.tsv --test-dir data/raw/test`. Do not modify the original script logic.

---

## 2. Raw Dataset Relocation

- **Original Location:** `code/business_entity_resolution/src/dataset/{train,test}/*.tsv`
- **New Location:** `data/raw/{train,test}/*.tsv`
- **Git Status:** Excluded via `.gitignore` (`data/raw/` and `*.tsv`).
- **Path Reference Note:** All data loaders in `src/business_entity_resolution/data/` or exploratory notebooks in `notebooks/analysis/` must point to `data/raw/train` and `data/raw/test`.

---

## 3. Submission Bundle Structure

- The competition submission zip expects:
  ```
  <team_name>_submission.zip
  ├── output/
  │   ├── matching_results.tsv
  │   └── candidate_pairs.tsv
  ├── code/
  │   └── business_entity_resolution/
  │       ├── src/
  │       ├── README.md
  │       └── requirements.txt
  └── Documentation_template.md
  ```
- All files required for this zip reside in the `submission/` directory:
  - `submission/output/`
  - `submission/code/business_entity_resolution/`
  - `submission/Documentation_template.md`
- Generating the final submission archive will simply compress the contents of `submission/`.

---

## 4. Deferred Implementation Modules
The following directories in `src/business_entity_resolution/` currently contain only `__init__.py` and `README.md` architectural specifications. Implementations will be built in subsequent phases under strict governance:
- `data/`
- `normalization/`
- `features/`
- `blocking/`
- `retrieval/`
- `matching/`
- `decision/`
- `postprocessing/`
- `evaluation/`
- `pipeline/`
- `utils/`
