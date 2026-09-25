# Repository Audit Report — Amazon ML Challenge 2026

**Date:** 2026-09-25  
**Auditor:** Antigravity (Repository Architect)  
**Project:** Amazon ML Challenge 2026 — Business Entity Resolution  
**Team:** Terminal_Titans  

---

## 1. Executive Summary

This audit inspects the complete initial repository provided in `d:\Projects\Machine_Learning Projects\Terminal_Titans_submission`.
Prior to this audit, the repository contained the unpacked official competition resource bundle (consisting of the problem statement, submission template, official validation utility, submission output placeholders, and the full raw training/test TSV datasets (~2.52 GB total)).

No commits have been made yet on the `master` branch. All files are currently untracked. No ML modeling, training scripts, feature pipelines, or exploratory notebooks have been created or modified yet.

---

## 2. Current Directory Tree (Pre-Migration)

```
d:\Projects\Machine_Learning Projects\Terminal_Titans_submission\
├── .git/
├── Documentation_template.md                      (2,172 bytes)
├── code/
│   └── business_entity_resolution/
│       ├── README.md                              (0 bytes)
│       ├── requirements.txt                       (0 bytes)
│       └── src/
│           ├── .DS_Store                          (6,148 bytes)
│           ├── dataset/
│           │   ├── .DS_Store                      (6,148 bytes)
│           │   ├── README.md                      (14,130 bytes)
│           │   ├── test/
│           │   │   ├── test_source1.tsv           (175,022,086 bytes)
│           │   │   ├── test_source2.tsv           (509,456,422 bytes)
│           │   │   └── test_source3.tsv           (506,002,772 bytes)
│           │   └── train/
│           │       ├── train_ground_truth.tsv     (127,015,583 bytes)
│           │       ├── train_source1.tsv          (210,069,713 bytes)
│           │       ├── train_source2.tsv          (489,301,488 bytes)
│           │       └── train_source3.tsv          (503,705,637 bytes)
│           ├── processed_dataset/                 (empty directory)
│           └── utils/
│               └── validate_submission.py         (13,687 bytes)
└── output/
    ├── candidate_pairs.tsv                        (0 bytes)
    └── matching_results.tsv                       (0 bytes)
```

---

## 3. Comprehensive File Classification

| File Path | Size | Classification | Rationale & Status |
|---|---|---|---|
| `Documentation_template.md` | 2,172 B | DOCUMENTATION | Official submission write-up template required in final package. Must be preserved exactly. |
| `code/business_entity_resolution/README.md` | 0 B | DOCUMENTATION | Empty placeholder provided in the competition template. Reorganize into submission package and document. |
| `code/business_entity_resolution/requirements.txt` | 0 B | CONFIG | Empty placeholder provided in the competition template. Reorganize into submission package and root requirements. |
| `code/business_entity_resolution/src/.DS_Store` | 6,148 B | TEMPORARY / CACHE | macOS Finder metadata file. Safe to delete or ignore via `.gitignore`. |
| `code/business_entity_resolution/src/dataset/.DS_Store` | 6,148 B | TEMPORARY / CACHE | macOS Finder metadata file. Safe to delete or ignore via `.gitignore`. |
| `code/business_entity_resolution/src/dataset/README.md` | 14,130 B | DOCUMENTATION | Authoritative competition documentation containing problem statement, format specs, F0.5 formula, and rules. Must be preserved into `docs/problem_statement.md` and referenced in `data/README.md`. |
| `code/business_entity_resolution/src/dataset/test/test_source1.tsv` | 175 MB | DATA / DATA REFERENCE | Raw test Reference Source 1 records (~1.7M total entities). DO NOT COMMIT TO GIT. Move to `data/raw/test/`. |
| `code/business_entity_resolution/src/dataset/test/test_source2.tsv` | 509 MB | DATA / DATA REFERENCE | Raw test Source 2 records. DO NOT COMMIT TO GIT. Move to `data/raw/test/`. |
| `code/business_entity_resolution/src/dataset/test/test_source3.tsv` | 506 MB | DATA / DATA REFERENCE | Raw test Source 3 records. DO NOT COMMIT TO GIT. Move to `data/raw/test/`. |
| `code/business_entity_resolution/src/dataset/train/train_ground_truth.tsv` | 127 MB | DATA / DATA REFERENCE | Ground truth match mappings (S1 -> S2,S3). DO NOT COMMIT TO GIT. Move to `data/raw/train/`. |
| `code/business_entity_resolution/src/dataset/train/train_source1.tsv` | 210 MB | DATA / DATA REFERENCE | Raw training Source 1 reference records. DO NOT COMMIT TO GIT. Move to `data/raw/train/`. |
| `code/business_entity_resolution/src/dataset/train/train_source2.tsv` | 489 MB | DATA / DATA REFERENCE | Raw training Source 2 records. DO NOT COMMIT TO GIT. Move to `data/raw/train/`. |
| `code/business_entity_resolution/src/dataset/train/train_source3.tsv` | 504 MB | DATA / DATA REFERENCE | Raw training Source 3 records. DO NOT COMMIT TO GIT. Move to `data/raw/train/`. |
| `code/business_entity_resolution/src/processed_dataset/` | 0 B | DATA / DATA REFERENCE | Empty placeholder directory. Will be mirrored under `data/processed/`. |
| `code/business_entity_resolution/src/utils/validate_submission.py` | 13,687 B | UTILITY | Official validation tool for submission outputs. Must be preserved exactly in `src/business_entity_resolution/utils/` and submission bundle. |
| `output/candidate_pairs.tsv` | 0 B | OUTPUT | Official submission output placeholder for candidate pairs. Preserved under `submission/output/candidate_pairs.tsv`. |
| `output/matching_results.tsv` | 0 B | OUTPUT | Official submission output placeholder for final matches. Preserved under `submission/output/matching_results.tsv`. |

---

## 4. Existing Experiments & ML Approaches

- **Existing Experiments:** None active or recorded.
- **Existing ML Approaches:** None implemented yet.
- **Existing Analysis Already Performed:**
  - Authoritative data profiling extracted from the official README:
    - 3 independent sources: S1 (reference, deduplicated), S2/S3 (noisy independent sources).
    - Multi-match structure: 0, 1, or many matches from S2/S3 per S1 entity. S2/S3 have distractor entities.
    - Fields: `entity_id`, `business_name`, `business_address`, `country`.
    - Train countries: `US`, `India`.
    - Test countries: `US`, `India`, and `France` (open set generalization requirement!).
    - Evaluation: Macro F0.5 per S1 entity including singletons (correct prediction of no match for singleton scores 1.0; false merge scores 0.0). Precision weighted 2x over recall.
    - Strict constraints: No external data lookup / geocoding (instant disqualification); models <= 8B parameters, MIT/Apache 2.0 license.

---

## 5. File Disposition Strategy

### A. Files to Preserve Exactly
1. `code/business_entity_resolution/src/utils/validate_submission.py` -> Must remain untouched in logic, placed in `src/business_entity_resolution/utils/validate_submission.py` and `submission/code/business_entity_resolution/src/utils/validate_submission.py`.
2. `Documentation_template.md` -> Preserved in `submission/Documentation_template.md`.
3. `code/business_entity_resolution/src/dataset/README.md` -> Preserved as primary problem specification in `docs/problem_statement.md` and detailed schema in `data/README.md`.

### B. Files That Can Safely Be Reorganized
1. `code/business_entity_resolution/src/dataset/test/*.tsv` -> Move to `data/raw/test/*.tsv`.
2. `code/business_entity_resolution/src/dataset/train/*.tsv` -> Move to `data/raw/train/*.tsv`.
3. `output/matching_results.tsv` and `candidate_pairs.tsv` -> Move to `submission/output/`.
4. `code/business_entity_resolution/README.md` and `requirements.txt` -> Relocate/link to `submission/code/business_entity_resolution/`.

### C. Files That Must NOT Be Committed to Git
1. All raw `.tsv` data files (Total ~2.52 GB). Must be gitignored immediately.
2. `.DS_Store` files.
3. Model weights, embeddings, FAISS indexes, local cache, temporary logs.

---

## 6. Proposed Migration Mapping

| Current Path | Target Path | Reason |
|---|---|---|
| `Documentation_template.md` | `submission/Documentation_template.md` | Required location for final submission bundle. |
| `code/business_entity_resolution/src/dataset/README.md` | `docs/problem_statement.md` | Core challenge documentation and specification. |
| `code/business_entity_resolution/src/utils/validate_submission.py` | `src/business_entity_resolution/utils/validate_submission.py` | Relocate to main engineering source tree. |
| `code/business_entity_resolution/src/utils/validate_submission.py` | `submission/code/business_entity_resolution/src/utils/validate_submission.py` | Relocate copy to standalone submission code bundle. |
| `code/business_entity_resolution/src/dataset/train/train_source1.tsv` | `data/raw/train/train_source1.tsv` | Reorganize raw training data into dedicated data store (gitignored). |
| `code/business_entity_resolution/src/dataset/train/train_source2.tsv` | `data/raw/train/train_source2.tsv` | Reorganize raw training data into dedicated data store (gitignored). |
| `code/business_entity_resolution/src/dataset/train/train_source3.tsv` | `data/raw/train/train_source3.tsv` | Reorganize raw training data into dedicated data store (gitignored). |
| `code/business_entity_resolution/src/dataset/train/train_ground_truth.tsv` | `data/raw/train/train_ground_truth.tsv` | Reorganize raw training ground truth into dedicated data store (gitignored). |
| `code/business_entity_resolution/src/dataset/test/test_source1.tsv` | `data/raw/test/test_source1.tsv` | Reorganize raw test data into dedicated data store (gitignored). |
| `code/business_entity_resolution/src/dataset/test/test_source2.tsv` | `data/raw/test/test_source2.tsv` | Reorganize raw test data into dedicated data store (gitignored). |
| `code/business_entity_resolution/src/dataset/test/test_source3.tsv` | `data/raw/test/test_source3.tsv` | Reorganize raw test data into dedicated data store (gitignored). |
| `output/matching_results.tsv` | `submission/output/matching_results.tsv` | Reorganize submission artifact placeholder into submission package. |
| `output/candidate_pairs.tsv` | `submission/output/candidate_pairs.tsv` | Reorganize submission artifact placeholder into submission package. |
| `code/business_entity_resolution/README.md` | `submission/code/business_entity_resolution/README.md` | Preserved in submission code folder. |
| `code/business_entity_resolution/requirements.txt` | `submission/code/business_entity_resolution/requirements.txt` | Preserved in submission code folder. |
| `code/business_entity_resolution/src/.DS_Store` | *Delete / Ignore* | OS metadata file. |
| `code/business_entity_resolution/src/dataset/.DS_Store` | *Delete / Ignore* | OS metadata file. |

---

## 7. Migration Prerequisite Verification

Before moving, verify:
- Gitignore is constructed to strictly prevent any `.tsv` files > 1MB or `data/raw/` from being tracked.
- Data directory structure is prepared.
- Source architecture directories will have minimal README placeholders documenting purpose without fake implementations.
