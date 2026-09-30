# Competition Submission Package (`submission`)

This directory contains the exact deliverables required for packaging into the final competition submission ZIP for the Amazon ML Challenge 2026.

---

## 1. Submission Package Structure

```
submission/
├── output/
│   ├── matching_results.tsv           # Scored entity match predictions (Leaderboard upload)
│   └── candidate_pairs.tsv            # Candidate pair blocking pool
├── code/
│   └── business_entity_resolution/
│       ├── src/
│       │   └── utils/
│       │       └── validate_submission.py  # Standalone validator copy
│       ├── README.md                  # Self-contained reproduction instructions
│       └── requirements.txt           # Minimal runtime dependencies
└── Documentation_template.md          # Official contest methodology write-up
```

---

## 2. Validation Before Submission

Always run the official submission validator prior to compressing and uploading:

```bash
python src/utils/validate_submission.py \
    --matching submission/output/matching_results.tsv \
    --candidate submission/output/candidate_pairs.tsv \
    --test-dir data/raw/test
```

Exit code `0` confirms the files adhere to all schema and formatting constraints.

---

## 3. Creating the Submission Archive

From the root of this repository:

```bash
# Example ZIP generation
cd submission && zip -r ../Terminal_Titans_submission.zip .
```
