# Experiment Registry

Central tracking table for all parallel research tracks across Kaggle, Colab, Local, and SageMaker platforms.

| ID | Platform | Owner | Hypothesis | Pipeline | Status | F0.5 | Candidate Recall | Reduction Ratio | Decision |
|---|---|---|---|---|---|---|---|---|---|
| kaggle-exp_01 | Kaggle | [Team Member 1] | Country-partitioned lexical blocking + LightGBM establishes fast baseline | Country Filter -> Token Overlap -> LightGBM -> Fixed 0.5 Cutoff | SKELETON | TBD | TBD | TBD | PENDING |
| kaggle-exp_02 | Kaggle | [Team Member 2] | Phonetic keys + 3-grams increase candidate recall by >=5% | Country Filter -> Double Metaphone + Char 3-gram Index -> LightGBM | SKELETON | TBD | TBD | TBD | PENDING |
| kaggle-exp_03 | Kaggle | [Team Member 3] | Dense bi-encoder embeddings (BGE/MiniLM) capture semantic address variations | Bi-Encoder -> FAISS ANN Index -> Top-k Retrieval -> LightGBM | SKELETON | TBD | TBD | TBD | PENDING |
| kaggle-exp_04 | Kaggle | [Team Member 4] | DeBERTa cross-encoder reranker improves pairwise precision on tricky pairs | Top Candidates -> DeBERTa-v3 Cross-Encoder -> Threshold Tuning | SKELETON | TBD | TBD | TBD | PENDING |
| kaggle-exp_05 | Kaggle | [Team Member 1] | Hybrid union of lexical, phonetic, and dense candidates achieves >=96% recall ceiling | Lexical BM25 U Phonetic U Dense FAISS -> Top-k Fusion -> LightGBM | SKELETON | TBD | TBD | TBD | PENDING |
| kaggle-exp_06 | Kaggle | [Team Member 2] | Dynamic singleton gating & precision-tuned calibration lifts Macro F0.5 by >=0.04 | Probabilities -> Isotonic Calibration -> F0.5 Dynamic Cutoff -> Singleton Gate | SKELETON | TBD | TBD | TBD | PENDING |
| colab-exp_01 | Colab | [Team Member 3] | Legal suffix stripping & address normalization reduces false token mismatches | Normalization Rules -> Lexical Inverted Index -> Pairwise Features | SKELETON | TBD | TBD | TBD | PENDING |
| colab-exp_02 | Colab | [Team Member 4] | Feature ablation highlights Jaccard, Levenshtein, and numeric postal matches | Systematic Feature Group Drop -> LightGBM -> Val F0.5 | SKELETON | TBD | TBD | TBD | PENDING |
| colab-exp_03 | Colab | [Team Member 1] | CatBoost provides superior handling of categorical/country features over LightGBM | Identical Feature Matrix -> LightGBM vs CatBoost vs XGBoost | SKELETON | TBD | TBD | TBD | PENDING |
| local-exp_01 | Local | [Team Member 2] | Stratified S1 split with singleton & country parity produces leak-free local CV | Stratified S1 Train/Val Split -> Entity Leak Audit -> Evaluation Metric | SKELETON | TBD | TBD | TBD | PENDING |
| local-exp_02 | Local | [Team Member 3] | Sparse token inverted index achieves 90% recall under 2GB RAM on CPU | Country Partition -> Sparse Token Matrix -> Cosine Cutoff | SKELETON | TBD | TBD | TBD | PENDING |
| local-exp_03 | Local | [Team Member 4] | End-to-end pipeline passes all strict rules in validate_submission.py | Ingestion -> Blocking -> Inference -> Output TSVs -> Validator | SKELETON | TBD | TBD | TBD | PENDING |
| sagemaker-exp_01 | SageMaker | [Team Member 1] | Multi-GPU batched bi-encoder embeds entire 1.7M corpus in under 2 hours | Sharded Ingestion -> Distributed Bi-Encoder -> FAISS HNSW Index | SKELETON | TBD | TBD | TBD | PENDING |
| sagemaker-exp_02 | SageMaker | [Team Member 2] | Cross-encoder fine-tuned with hard negatives yields maximum single-model precision | Hard Negative Mining -> DeBERTa-v3-base Tuning -> Distillation | SKELETON | TBD | TBD | TBD | PENDING |
| sagemaker-exp_03 | SageMaker | [Team Member 3] | Distributed chunked pipeline scales to generate full competition test submission | Partitioned Test -> Distributed Search & Score -> TSV Assembly | SKELETON | TBD | TBD | TBD | PENDING |
