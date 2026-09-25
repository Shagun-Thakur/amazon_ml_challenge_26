# Challenge Strategy — Business Entity Resolution

## 1. Problem Formulation
- **Objective:** For every deduplicated reference entity in Source 1 ($S_1$), retrieve and resolve all true matching records from independent noisy sources ($S_2$ and $S_3$).
- **Multiplicity:** An $S_1$ entity matches zero, one, or multiple records across $S_2$ and $S_3$.
- **Distractors:** $S_2$ and $S_3$ contain numerous distractor records that do not correspond to any $S_1$ entity.
- **Metric Formulation:** Macro $F_{0.5}$ per $S_1$ entity.
  $$F_{0.5} = \frac{1.25 \times \text{Precision} \times \text{Recall}}{0.25 \times \text{Precision} + \text{Recall}}$$
  - Precision is weighted 2× as heavily as recall.
  - Correct identification of singletons (entities with zero matches) awards a perfect 1.0; false merges on singletons severely penalize the macro score to 0.0.

---

## 2. Multi-Tier Resolution Funnel

1. **Tier 1: Preprocessing & Normalization**
   - Address normalization (road/street, numbers, missing PINs).
   - Legal suffix stripping/standardization (Corp, Pvt Ltd, LLC).
   - Character standardization and punctuation cleaning.

2. **Tier 2: Multi-Pass Blocking / Candidate Generation**
   - Candidate generation sets the strict recall ceiling: any true pair missed here cannot be matched.
   - Reduction ratio must achieve > 99.9% comparison space pruning while maintaining > 95% candidate recall.
   - Stratified blocking: Country-partitioned lexical passes (BM25 / inverted index), phonetic keys (Double Metaphone / Soundex), and dense embedding retrieval.

3. **Tier 3: Pairwise Matching & Reranking**
   - High-precision gradient boosted decision trees (LightGBM/CatBoost/XGBoost) and fine-tuned cross-encoders.
   - Comprehensive similarity features: token overlap, Jaccard, fuzzy Levenshtein, Jaro-Winkler, coordinate/location indicators, embedding cosine.

4. **Tier 4: Global Decision, Calibration & Singleton Gate**
   - Optimal threshold calibration specifically tuned for Macro $F_{0.5}$ objective.
   - Explicit Singleton Classifier to aggressively prune doubtful candidate sets to empty (`""`).

---

## 3. Generalization & Open-Set Constraint
- **Train Set:** Contains entities from `US` and `India`.
- **Test Set:** Contains `US`, `India`, and `France` (unseen country during training).
- **Rule:** Feature extraction and blocking must generalize without relying on fixed country-specific lookup dictionaries or closed categorical one-hot encodings.
- **External Data Rule:** Strictly zero external lookups, geocoding APIs, or web scraping allowed. All models must be <= 8B parameters with permissive licenses (Apache 2.0 / MIT).
