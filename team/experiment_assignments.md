# Experiment Assignments

Operational task assignments mapping research questions to experiment tracks and owners.

| Experiment | Platform | Owner | Exact Question | Deliverable |
|---|---|---|---|---|
| kaggle-exp_01 | Kaggle | [Team Member 1] | What baseline Macro F0.5 can be achieved with simple country-partitioned lexical blocking and LightGBM? | Baseline metrics table & execution script |
| kaggle-exp_02 | Kaggle | [Team Member 2] | How much does Double Metaphone and char 3-gram indexing increase candidate recall? | Candidate recall vs reduction ratio trade-off curve |
| kaggle-exp_03 | Kaggle | [Team Member 3] | Can lightweight dense embeddings (BGE-small / MiniLM) recover semantic address variations missed by BM25? | Recall uplift report & FAISS index script |
| kaggle-exp_04 | Kaggle | [Team Member 4] | Does a DeBERTa-v3 cross-encoder reranker outperform GBDT on pairwise precision? | Model checkpoint, precision/recall curves, latency report |
| kaggle-exp_05 | Kaggle | [Team Member 1] | What is the optimal union configuration of lexical, phonetic, and dense candidate generators? | Multi-channel union blocking module & candidate set evaluation |
| kaggle-exp_06 | Kaggle | [Team Member 2] | What probability threshold and singleton gating rule maximizes Macro F0.5 on the validation split? | Threshold calibration curves & singleton gate policy |
| colab-exp_01 | Colab | [Team Member 3] | What is the quantitative impact of standardizing corporate suffixes and address abbreviations? | Ablation report on string similarity distributions |
| colab-exp_02 | Colab | [Team Member 4] | Which features are the strongest positive contributors to Macro F0.5 in GBDT models? | Feature importance ranking & pruned feature config |
| colab-exp_03 | Colab | [Team Member 1] | How do LightGBM, CatBoost, and XGBoost compare in F0.5 score, RAM, and training time? | Comparative benchmarking report |
| local-exp_01 | Local | [Team Member 2] | How can we construct a local validation split that avoids entity leakage and mirrors test set properties? | Stratified validation split generator script & distribution report |
| local-exp_02 | Local | [Team Member 3] | Can a sparse token inverted index achieve >90% candidate recall on CPU in <5 minutes with <2GB RAM? | Lightweight CPU blocking module & profiling benchmark |
| local-exp_03 | Local | [Team Member 4] | Does the end-to-end pipeline run cleanly from input TSVs to submission TSVs passing validate_submission.py? | Smoke test harness & validation verification log |
| sagemaker-exp_01 | SageMaker | [Team Member 1] | Can we embed and index all 1.7M+ entities on multi-GPU instances in under 2 hours? | Distributed embedding pipeline & FAISS index export |
| sagemaker-exp_02 | SageMaker | [Team Member 2] | How much does hard negative mining improve cross-encoder discrimination on ambiguous pairs? | Fine-tuned weights, student distillation checkpoint |
| sagemaker-exp_03 | SageMaker | [Team Member 3] | Can the complete test inference run reliably end-to-end generating compliant matching_results.tsv and candidate_pairs.tsv? | Full test submission artifacts & validator pass confirmation |
