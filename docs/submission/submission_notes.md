# Submission Protocol & Operational Notes

Operational checklist and guidelines for leaderboard uploads and final zip package generation.

## 1. Leaderboard Submission Protocol
- Upload file: `submission/output/matching_results.tsv`.
- Must contain exactly 2 columns separated by a tab (`\t`):
  `source1_entity_id\tmatched_entity_ids`
- Must include exactly one row per Source 1 entity in `test_source1.tsv`.
- No duplicate rows, no intra-list duplicates, no self-matches (`S1-*`).

## 2. Final Submission Package Checklist
Generate `<team_name>_submission.zip` containing:
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

## 3. Pre-Submission Local Validation
Always execute the official validator before uploading:
```bash
python src/business_entity_resolution/utils/validate_submission.py \
    --matching submission/output/matching_results.tsv \
    --candidate submission/output/candidate_pairs.tsv \
    --test-dir data/raw/test
```
Ensure it returns exit code 0 (`PASS`).
