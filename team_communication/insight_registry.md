# Insight Registry

Chronological knowledge base documenting verified empirical insights and theoretical discoveries.

| Insight ID | Source Experiment | Finding | Evidence | Confidence | Architectural Consequence |
|---|---|---|---|---|---|
| INS-001 | Official Specs / EDA | Metric is Macro F0.5 per S1 entity; precision is weighted 2x over recall. Singletons must be empty to receive score 1.0. | Competition problem statement & F0.5 formula | VERY HIGH | Post-processing must incorporate an aggressive precision threshold and dedicated singleton gate to prevent false merges. |
| INS-002 | Official Specs / EDA | Test set includes France (open-set country) not present in training data (US, India only). | Official problem description | VERY HIGH | Normalization and feature extractors must NOT hardcode fixed country one-hot encodings or country-specific closed lists. |
| INS-003 | Official Specs / EDA | S1 is deduplicated reference source; S2/S3 contain distractors. Matches can be 0, 1, or many. | Problem statement & dataset schema | VERY HIGH | Models must treat resolution as 1-to-many retrieval/matching, not 1-to-1 bipartite matching. Distractor filtering is mandatory. |
| INS-004 | Official Validator | Validator checks that matches in matching_results.tsv are a subset of candidate_pairs.tsv. | utils/validate_submission.py code audit | VERY HIGH | candidate_pairs.tsv must strictly reflect the candidate set fed directly into the matching classifier. |
| INS-005 | Official Rules | Strictly zero external data lookup, geocoding, or web scraping allowed; models <= 8B parameters with permissive licenses. | Official competition rules | VERY HIGH | All entity resolution logic must rely strictly on internal features computed from provided TSV files. |
