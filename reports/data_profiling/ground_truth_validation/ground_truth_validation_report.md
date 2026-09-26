# Ground Truth Validation Report

Generated: 2026-09-26T09:12:06.361562

## 1. Basic statistics

- Ground truth rows: 2,206,821
- Unique S1 IDs in GT: 2,206,821
- Empty-match rows: 123,247 (5.585%)
- Non-empty-match rows: 2,083,574 (94.415%)
- Total matched IDs: 7,638,365
- Mean cardinality: 3.4613
- Median cardinality: 3.0
- Maximum cardinality: 11

## 2. Cardinality distribution

| Matches per S1 | Rows | Percentage |
|---:|---:|---:|
| 0 | 123,247 | 5.585% |
| 1 | 119,157 | 5.399% |
| 2 | 375,212 | 17.002% |
| 3 | 530,841 | 24.055% |
| 4 | 484,115 | 21.937% |
| 5 | 321,957 | 14.589% |
| 6 | 164,868 | 7.471% |
| 7 | 63,968 | 2.899% |
| 8 | 18,680 | 0.846% |
| 9 | 4,205 | 0.191% |
| 10 | 534 | 0.024% |
| 11 | 37 | 0.002% |

## 3. S1 relationship topology

| Relationship | Rows | Percentage |
|---|---:|---:|
| S1 -> S2 only | 143,029 | 6.481% |
| S1 -> S3 only | 164,498 | 7.454% |
| S1 -> S2 + S3 | 1,776,047 | 80.480% |
| S1 -> neither | 0 | 0.000% |

## 4. Referential integrity

- Missing S1 IDs: 0
- Missing matched IDs: 0
- Duplicate GT S1 rows: 0
- Rows containing duplicate matched IDs: 0
- Duplicate matched-ID occurrences: 0

## 5. Format validation

- Malformed/empty S1 rows: 0
- Malformed matched IDs: 0

## 6. Interpretation

Ground truth is validated structurally rather than linguistically normalized. Business names and addresses remain untouched because the ground truth contains entity IDs.
The matching problem must preserve one-to-many relationships and explicit zero-match S1 records.
