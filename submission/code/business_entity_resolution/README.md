# Submission Code Package — Business Entity Resolution

This folder contains the complete, self-contained, reproducible pipeline for the Amazon ML Challenge 2026.

## Structure
```
code/business_entity_resolution/
├── src/
│   ├── utils/
│   │   └── validate_submission.py
│   └── (pipeline code)
├── README.md
└── requirements.txt
```

## How to Reproduce Submission Outputs
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run end-to-end inference over the test dataset:
   ```bash
   python src/run_pipeline.py --test-dir /path/to/test --output-dir ../../output
   ```
3. Validate output files:
   ```bash
   python src/utils/validate_submission.py \
       --matching ../../output/matching_results.tsv \
       --candidate ../../output/candidate_pairs.tsv \
       --test-dir /path/to/test
   ```
