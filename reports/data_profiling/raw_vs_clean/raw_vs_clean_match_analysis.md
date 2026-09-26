# Raw vs Clean Match Analysis

- Positive S1 sample: 100,000

- Random seed: 42

- Analysis uses sampled positive ground-truth pairs for pair-level signal comparison.

- Ambiguity statistics are source-wide.


## 1. Exact-match comparison

| source   | signal                 |     raw_pct |   clean_pct |   gain_percentage_points |
|:---------|:-----------------------|------------:|------------:|-------------------------:|
| S2       | exact_name             | 4.77231     | 21.432      |             16.6597      |
| S2       | exact_address          | 0           | 12.5015     |             12.5015      |
| S2       | exact_name_and_address | 0           |  2.67351    |              2.67351     |
| S3       | exact_name             | 4.56281     | 22.0752     |             17.5124      |
| S3       | exact_address          | 4.33427     |  4.34112    |              0.00684553  |
| S3       | exact_name_and_address | 0.000526579 |  0.00105316 |              0.000526579 |


## 2. Token and numeric signals

| source   | signal                 |     mean |   median |      p10 |      p25 |      p75 |      p90 |   nonzero_pct |
|:---------|:-----------------------|---------:|---------:|---------:|---------:|---------:|---------:|--------------:|
| S2       | name_token_jaccard     | 0.610426 | 0.666667 | 0        | 0.5      | 1        | 1        |       83.8113 |
| S2       | addr_token_jaccard     | 0.686864 | 0.714286 | 0.363636 | 0.5      | 0.888889 | 1        |       95.4908 |
| S2       | name_token_containment | 0.738464 | 1        | 0        | 0.666667 | 1        | 1        |       83.8113 |
| S2       | addr_token_containment | 0.829799 | 0.866667 | 0.6      | 0.8      | 1        | 1        |       95.4908 |
| S2       | numeric_overlap        | 1.16532  | 1        | 0        | 1        | 1        | 2        |       78.8931 |
| S3       | name_token_jaccard     | 0.624613 | 0.666667 | 0        | 0.5      | 1        | 1        |       87.2563 |
| S3       | addr_token_jaccard     | 0.528895 | 0.5      | 0.222222 | 0.363636 | 0.714286 | 0.857143 |       95.602  |
| S3       | name_token_containment | 0.772474 | 1        | 0        | 0.666667 | 1        | 1        |       87.2563 |
| S3       | addr_token_containment | 0.706057 | 0.75     | 0.4      | 0.6      | 0.857143 | 0.944444 |       95.602  |
| S3       | numeric_overlap        | 1.19125  | 1        | 0        | 1        | 2        | 2        |       80.5787 |


## 3. Raw vs clean ambiguity

| source   | feature   |   raw_unique |   clean_unique |   raw_duplicate_rows |   clean_duplicate_rows |   raw_duplicate_row_pct |   clean_duplicate_row_pct |   duplicate_row_pct_change |
|:---------|:----------|-------------:|---------------:|---------------------:|-----------------------:|------------------------:|--------------------------:|---------------------------:|
| S1       | name      |      1539229 |        1522166 |               667592 |                 684655 |                30.2513  |                  31.0245  |                  0.773194  |
| S1       | address   |      2130606 |        2130153 |                76215 |                  76668 |                 3.45361 |                   3.47414 |                  0.0205273 |
| S2       | name      |      4402009 |        4033290 |               632607 |                1001326 |                12.5651  |                  19.8888  |                  7.32368   |
| S2       | address   |      4337262 |        4286084 |               697354 |                 748532 |                13.8512  |                  14.8677  |                  1.01652   |
| S3       | name      |      4651609 |        4288741 |               633994 |                 996862 |                11.9947  |                  18.8599  |                  6.86521   |
| S3       | address   |      4632765 |        4616084 |               652838 |                 669519 |                12.3512  |                  12.6668  |                  0.315593  |


## 4. Clean name + address ambiguity

| source   | feature                       |    rows |   unique |   duplicate_rows |   duplicate_row_pct |
|:---------|:------------------------------|--------:|---------:|-----------------:|--------------------:|
| S1       | clean_name_plus_clean_address | 2206821 |  2206821 |                0 |            0        |
| S2       | clean_name_plus_clean_address | 5034616 |  4967478 |            67138 |            1.33353  |
| S3       | clean_name_plus_clean_address | 5285603 |  5235611 |            49992 |            0.945815 |


## 5. Interpretation


### S2

- Positive pairs analyzed: 177,482

- Raw exact name: 4.772%

- Clean exact name: 21.432%

- Raw exact address: 0.000%

- Clean exact address: 12.502%

- Raw exact name + address: 0.000%

- Clean exact name + address: 2.674%

- Mean name token Jaccard: 0.6104

- Mean address token Jaccard: 0.6869

- Mean numeric-token overlap: 1.1653

- Numeric overlap > 0: 78.893%


### S3

- Positive pairs analyzed: 189,905

- Raw exact name: 4.563%

- Clean exact name: 22.075%

- Raw exact address: 4.334%

- Clean exact address: 4.341%

- Raw exact name + address: 0.001%

- Clean exact name + address: 0.001%

- Mean name token Jaccard: 0.6246

- Mean address token Jaccard: 0.5289

- Mean numeric-token overlap: 1.1913

- Numeric overlap > 0: 80.579%


## 6. Important methodological note

Pair-level raw-vs-clean measurements are based on a deterministic 100k-S1 positive sample to avoid materializing all 7.6M positive pairs in RAM. Ambiguity statistics are computed source-wide using uint64 fingerprints.
