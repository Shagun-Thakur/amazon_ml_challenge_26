# Data Management & Storage Policy — Amazon ML Challenge 2026

## 1. Overview & Data Policy
The dataset for the Amazon ML Challenge 2026 (Business Entity Resolution) comprises approximately 2.52 GB of tab-separated records across three sources, plus ground truth annotations. 

**Strict Version Control Policy:**
- **Raw competition dataset files must NEVER be committed to Git.**
- All `.tsv` files under `data/raw/` are strictly ignored by `.gitignore`.
- Only minimal, anonymized schema verification samples (<= 100 rows) or schema definitions in `data/schemas/` and `data/samples/` may be tracked if necessary.

---

## 2. Expected Dataset Directory Layout

Raw datasets must be placed in the local directory structure as follows:

```
data/
├── README.md                          # This policy & specification document
├── raw/
│   ├── train/
│   │   ├── train_source1.tsv          # Source 1 reference records (~210 MB)
│   │   ├── train_source2.tsv          # Source 2 noisy records (~489 MB)
│   │   ├── train_source3.tsv          # Source 3 noisy records (~504 MB)
│   │   └── train_ground_truth.tsv     # Ground truth matches (~127 MB)
│   └── test/
│       ├── test_source1.tsv           # Source 1 reference test records (~175 MB)
│       ├── test_source2.tsv           # Source 2 noisy test records (~509 MB)
│       └── test_source3.tsv           # Source 3 noisy test records (~506 MB)
├── processed/                         # Processed/normalized cache (gitignored)
├── samples/                           # Tiny representative samples for smoke tests
└── schemas/                           # Strict schema definitions (types, nulls, constraints)
```

---

## 3. Data Schemas

All files are Tab-Separated Values (`.tsv`) with UTF-8 encoding. Tab separators are strictly required because address fields and entity lists contain commas.

### Source Files (`*_source1.tsv`, `*_source2.tsv`, `*_source3.tsv`)
| Column Name | Type | Description | Notes |
|---|---|---|---|
| `entity_id` | String | Unique identifier for the record | Prefix indicates source (`S1-`, `S2-`, `S3-`) |
| `business_name` | String | Name of the business entity | Contains abbreviations, legal suffixes, typos, transliterations |
| `business_address` | String | Address of the business | Contains partial addresses, landmark references, missing PIN codes |
| `country` | String | Country of origin | Train: `US`, `India`. Test: `US`, `India`, `France` (open-set!) |

### Ground Truth File (`train_ground_truth.tsv`)
| Column Name | Type | Description | Notes |
|---|---|---|---|
| `source1_entity_id` | String | The reference `entity_id` of Source 1 | Maps 1-to-1 with training Source 1 entities |
| `matched_entity_ids` | String | Comma-separated list of matching IDs | Matches from S2 and/or S3. Empty for singletons |

---

## 4. Reading Data Correctly in Python

Always specify `sep="\t"` and explicit encoding `utf-8`:

```python
import pandas as pd
from pathlib import Path

DATA_DIR = Path("data/raw")

# Training data
df_s1_train = pd.read_csv(DATA_DIR / "train" / "train_source1.tsv", sep="\t", dtype=str, keep_default_na=False)
df_gt_train = pd.read_csv(DATA_DIR / "train" / "train_ground_truth.tsv", sep="\t", dtype=str, keep_default_na=False)

# Test data
df_s1_test = pd.read_csv(DATA_DIR / "test" / "test_source1.tsv", sep="\t", dtype=str, keep_default_na=False)
```

---

## 5. Environment Path Configuration
To configure dataset paths across various execution environments (Local, Kaggle, Colab, SageMaker), set environment variables or use the dynamic project path resolver in `experiments/baseline/utils_io.py` (`resolve_project_paths`):

```bash
# Environment variable overrides
export DATA_RAW_DIR="./data/raw"
export DATA_PROCESSED_DIR="./data/processed"
```

Default search mappings:
- **Local:** `./data/raw`
- **Kaggle:** `/kaggle/input/amazon-ml-challenge-2026/data/raw`
- **Colab:** `/content/drive/MyDrive/amazon-ml-2026/data/raw`
- **SageMaker:** `/opt/ml/input/data/raw`

