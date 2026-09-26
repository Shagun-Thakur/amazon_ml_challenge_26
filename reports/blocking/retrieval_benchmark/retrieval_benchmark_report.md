# Lightweight Retrieval Benchmark

## Validation Design

- Seed: 42
- S1 validation sample: 20,000
- Positive S1: 18,933
- Zero-match S1: 1,067
- Positive pairs: 69,150
- S2 target pool: 133,180
- S3 target pool: 135,970


## Retrieval Results

| source   | method                 |   top_k |   positive_s1 |   true_pairs |   pair_recall_pct |   s1_any_match_recall_pct |   s1_all_match_recall_pct |   avg_candidates_per_positive_s1 |   median_true_rank |   p90_true_rank |   runtime_sec |   vectorization_time_sec |
|:---------|:-----------------------|--------:|--------------:|-------------:|------------------:|--------------------------:|--------------------------:|---------------------------------:|-------------------:|----------------:|--------------:|-------------------------:|
| S2       | exact_structural_union |     nan |         17330 |        33180 |           84.0115 |                   89.4345 |                   77.1206 |                          2219.78 |                nan |             nan |       nan     |                 nan      |
| S2       | char_tfidf             |      10 |         17330 |        33180 |           97.6492 |                   98.4535 |                   95.9781 |                            10    |                  1 |               3 |       199.769 |                  28.7623 |
| S2       | char_tfidf             |      25 |         17330 |        33180 |           98.2459 |                   98.7767 |                   97.0225 |                            25    |                  1 |               3 |       213.213 |                  28.7623 |
| S2       | char_tfidf             |      50 |         17330 |        33180 |           98.6588 |                   99.0883 |                   97.7092 |                            50    |                  1 |               3 |       208.818 |                  28.7623 |
| S2       | char_tfidf             |     100 |         17330 |        33180 |           99.0325 |                   99.3306 |                   98.3555 |                           100    |                  1 |               3 |       202.226 |                  28.7623 |
| S2       | char_hashing           |      10 |         17330 |        33180 |           96.1181 |                   97.6053 |                   93.4045 |                            10    |                  1 |               3 |       230.28  |                  14.028  |
| S2       | char_hashing           |      25 |         17330 |        33180 |           96.9198 |                   98.0265 |                   94.7374 |                            25    |                  1 |               3 |       225.038 |                  14.028  |
| S2       | char_hashing           |      50 |         17330 |        33180 |           97.3538 |                   98.2804 |                   95.4934 |                            50    |                  1 |               3 |       224.521 |                  14.028  |
| S2       | char_hashing           |     100 |         17330 |        33180 |           97.8541 |                   98.592  |                   96.307  |                           100    |                  1 |               3 |       223.891 |                  14.028  |
| S3       | exact_structural_union |     nan |         17731 |        35970 |           85.727  |                   91.309  |                   78.3938 |                          2273.34 |                nan |             nan |       nan     |                 nan      |
| S3       | char_tfidf             |      10 |         17731 |        35970 |           97.6703 |                   98.9735 |                   95.8716 |                            10    |                  2 |               3 |       203.576 |                  30.6478 |
| S3       | char_tfidf             |      25 |         17731 |        35970 |           98.4153 |                   99.295  |                   97.197  |                            25    |                  2 |               3 |       204.431 |                  30.6478 |
| S3       | char_tfidf             |      50 |         17731 |        35970 |           98.8018 |                   99.4473 |                   97.8851 |                            50    |                  2 |               3 |       204.271 |                  30.6478 |
| S3       | char_tfidf             |     100 |         17731 |        35970 |           99.0826 |                   99.5996 |                   98.3701 |                           100    |                  2 |               3 |       205.95  |                  30.6478 |
| S3       | char_hashing           |      10 |         17731 |        35970 |           96.0912 |                   98.0994 |                   93.2322 |                            10    |                  2 |               3 |       230.579 |                  13.0054 |
| S3       | char_hashing           |      25 |         17731 |        35970 |           97.0086 |                   98.5506 |                   94.8226 |                            25    |                  2 |               3 |       232.553 |                  13.0054 |
| S3       | char_hashing           |      50 |         17731 |        35970 |           97.5646 |                   98.8495 |                   95.7701 |                            50    |                  2 |               3 |       232.864 |                  13.0054 |
| S3       | char_hashing           |     100 |         17731 |        35970 |           98.0484 |                   99.092  |                   96.5597 |                           100    |                  2 |               3 |       232.743 |                  13.0054 |


## Interpretation

This benchmark measures candidate retrieval recall, not final
entity-resolution precision.

The target pool contains all known true targets for the
validation S1 sample plus deterministic random negative targets.

Therefore:

- pair recall measures how many true S1→target links entered
  the retrieved top-K set;
- S1-any recall measures whether at least one true target was
  retrieved for an S1 entity;
- S1-all recall measures whether every known target for an S1
  entity was retrieved;
- average candidates per positive S1 measures retrieval-set size;
- true-match rank measures how early true targets appear.

The validation benchmark must be completed before scaling any
retrieval method toward the full competition test set.
