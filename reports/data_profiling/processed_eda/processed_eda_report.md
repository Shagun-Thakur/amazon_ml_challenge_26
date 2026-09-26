# Processed EDA Report — Cleaning V1

## 1. Purpose
This report evaluates the V1 cleaned training datasets without modifying the cleaned outputs.

## 2. Processing Strategy
- Chunk size: 100,000 rows
- Chunked TSV processing
- uint64 fingerprints for scalable uniqueness analysis
- No pairwise matrices
- No giant Python sets

## 3. Source Summary

| Source | Rows | Raw Unique Names | Clean Unique Names | Raw Unique Addresses | Clean Unique Addresses | Raw Dup % | Clean Dup % |
|---|---:|---:|---:|---:|---:|---:|---:|
| source1 | 2,206,821 | 1,539,229 | 1,522,166 | 2,130,606 | 2,130,153 | 0.0000% | 0.0000% |
| source2 | 5,034,616 | 4,402,009 | 4,033,290 | 4,337,262 | 4,286,084 | 0.0000% | 0.0000% |
| source3 | 5,285,603 | 4,651,609 | 4,288,741 | 4,632,765 | 4,616,084 | 0.0000% | 0.0000% |

## 4. Cleaning Coverage

| Source | Name Changed % | Address Changed % | Numeric Available % | Postal Available % |
|---|---:|---:|---:|---:|
| source1 | 100.00% | 100.00% | 96.51% | 36.59% |
| source2 | 89.84% | 96.64% | 90.65% | 31.30% |
| source3 | 93.49% | 96.67% | 90.80% | 31.64% |

## 5. Length Statistics

### SOURCE1

- Raw name mean length: 24.034
- Clean name mean length: 23.905
- Raw address mean length: 52.066
- Clean address mean length: 48.685
- Clean name mean token count: 3.625
- Clean address mean token count: 8.512

### SOURCE2

- Raw name mean length: 25.104
- Clean name mean length: 24.650
- Raw address mean length: 46.226
- Clean address mean length: 43.088
- Clean name mean token count: 3.647
- Clean address mean token count: 7.804

### SOURCE3

- Raw name mean length: 25.202
- Clean name mean length: 24.749
- Raw address mean length: 46.714
- Clean address mean length: 43.575
- Clean name mean token count: 3.697
- Clean address mean token count: 7.643

## 6. Raw vs Clean Interpretation

The uniqueness changes indicate how much normalization collapses previously distinct textual representations.

Duplicate-rate changes should be monitored because cleaning can intentionally make records textually identical.

Numeric-token and postal-token availability are retained as structural matching features.

## 7. Methodological Note

Uniqueness and duplicate counts use 64-bit pandas fingerprints instead of retaining millions of Python strings in memory.

## 8. Output Files

- `/kaggle/working/reports/processed_eda/csv/processed_eda_summary.csv`
- `/kaggle/working/reports/processed_eda/csv/processed_country_distribution.csv`
- `/kaggle/working/reports/processed_eda/csv/processed_length_token_statistics.csv`
- `/kaggle/working/reports/processed_eda/csv/raw_vs_clean_changes.csv`
- `/kaggle/working/reports/processed_eda/processed_summary.json`
- `/kaggle/working/reports/processed_eda/plots`

Total runtime: 381.68 seconds