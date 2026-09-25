# Modeling Arsenal & Methodological Toolkit

This document catalogs the candidate algorithmic methods, feature extractors, and architectural components under consideration.

## 1. Candidate Generation & Blocking
- **Exact & Partition Blocking:** Country-level partitioning ($Country_{S1} == Country_{S2/3}$), postal code / state prefix blocking.
- **Phonetic & Hash Keys:** Double Metaphone, Soundex, NYSIIS on dominant business name tokens.
- **Lexical Inverted Indexing & BM25:** BM25 retrieval over concatenated `business_name` + `business_address` tokens.
- **Dense Embedding Retrieval:** Bi-encoders (e.g., Sentence-Transformers, BGE-small, E5) indexing vector embeddings via FAISS (HNSW / FlatIP).
- **Hybrid Multi-Channel Union:** Union of multiple sparse and dense candidate pools, capped at top-$k$ per $S_1$ entity.

## 2. Feature Engineering Suite
- **String Distance Metrics:** Levenshtein, Damerau-Levenshtein, Jaro-Winkler, Longest Common Subsequence (LCS).
- **Token Set Metrics:** Jaccard similarity, Sørensen-Dice, Overlap coefficient, Monge-Elkan.
- **Phonetic Overlaps:** Phonetic token intersection ratio.
- **TF-IDF & Character N-Gram Cosine:** Character 3-gram and 4-gram cosine similarities.
- **Numeric & Address Specific:** Address house/unit number matching, postal code match status, digit sequence equality.
- **Dense Semantic Similarity:** Cosine similarity of bi-encoder embeddings.

## 3. Pair Scoring & Classification
- **GBDT Classifiers:** LightGBM, CatBoost, XGBoost trained on pairwise feature vectors.
- **Cross-Encoder Rerankers:** Transformer cross-encoders (e.g., DeBERTa-v3-small/base) scoring $(S_1, S_2/3)$ pairs directly.
- **Calibrated Probability Estimation:** Isotonic regression or Platt scaling to align predicted probabilities.

## 4. Post-Processing & Set Selection
- **Macro $F_{0.5}$ Dynamic Thresholding:** Threshold tuning on validation splits.
- **Precision Guardrail:** High threshold filter prioritizing precision over recall.
- **Graph Consistency / Sanity Checks:** Ensure matched entities strictly originate from test $S_2$ and $S_3$.
