# utils Module

## Responsibility:
Shared repository utilities: official submission validator (`validate_submission.py`), path management, safe TSV serialization, logging, and deterministic random seed control.

---

## Submission Validator (`validate_submission.py`)

The official validation script verifies submission output files against all formatting and structural rules enforced by the challenge evaluation system before uploading.

### CLI Arguments:
- `--matching` (required): Path to `matching_results.tsv`. Defaults to `output/matching_results.tsv`.
- `--candidate` (optional): Path to `candidate_pairs.tsv`. Defaults to `output/candidate_pairs.tsv`.
- `--test-dir` (required): Path to directory containing test sources (must contain `test_source1.tsv`). Defaults to `dataset/test`.
- `--check-ids` (optional): Enable strict ID existence checks across `test_source2.tsv` and `test_source3.tsv` (memory-intensive).

### Usage from Repository Root:
```bash
python src/utils/validate_submission.py \
    --matching submission/output/matching_results.tsv \
    --candidate submission/output/candidate_pairs.tsv \
    --test-dir data/raw/test
```

### Exit Codes:
- `0`: Validation passed; files conform to submission standards.
- `1`: Validation failed; errors must be resolved prior to submission.
