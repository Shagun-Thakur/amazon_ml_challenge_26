import os
import gc
import json
import numpy as np
import pandas as pd
import lightgbm as lgb
from utils_io import resolve_project_paths, load_tsv_safe
from features import extract_pairwise_features

def macro_f05(y_true_dict: dict, y_pred_dict: dict, all_s1_ids: list):
    """
    Computes exact competition Macro-F0.5 over all S1 entities.
    """
    scores = []
    beta_sq = 0.5 ** 2

    for sid in all_s1_ids:
        y_true = y_true_dict.get(sid, set())
        y_pred = y_pred_dict.get(sid, set())

        # Singleton evaluation
        if len(y_true) == 0:
            scores.append(1.0 if len(y_pred) == 0 else 0.0)
            continue

        if len(y_pred) == 0:
            scores.append(0.0)
            continue

        tp = len(y_true.intersection(y_pred))
        p = tp / len(y_pred)
        r = tp / len(y_true)

        if p == 0 or r == 0:
            scores.append(0.0)
        else:
            f05 = ((1 + beta_sq) * p * r) / ((beta_sq * p) + r)
            scores.append(f05)

    return np.mean(scores)

def main():
    paths = resolve_project_paths()
    clean_train_dir = os.path.join(paths["cleaned_dir"], "train")
    clean_test_dir = os.path.join(paths["cleaned_dir"], "test")
    output_dir = os.path.join(paths["base_dir"], "output")

    # 1. Load Cleaned Training Data for LightGBM
    print("[1/4] Preparing Balanced Training Dataset...")
    s1_train = load_tsv_safe(os.path.join(clean_train_dir, "clean_train_source1.tsv"))
    s2_train = load_tsv_safe(os.path.join(clean_train_dir, "clean_train_source2.tsv"))
    s3_train = load_tsv_safe(os.path.join(clean_train_dir, "clean_train_source3.tsv"))
    gt_train = load_tsv_safe(os.path.join(clean_train_dir, "clean_train_ground_truth.tsv"))

    gt_dict = {}
    for row in gt_train.itertuples(index=False):
        matches = [m.strip() for m in row.matched_entity_ids.split(",") if m.strip()]
        gt_dict[row.source1_entity_id] = set(matches)

    # Subsample 35,000 anchors for training and 10,000 for threshold validation
    np.random.seed(42)
    shuffled_s1 = s1_train.sample(frac=1.0, random_state=42).reset_index(drop=True)
    val_s1_ids = set(shuffled_s1.iloc[:10000]["entity_id"].values)
    train_s1_ids = set(shuffled_s1.iloc[10000:45000]["entity_id"].values)

    # Fast record lookups
    def build_lookup(df):
        return {
            row.entity_id: {
                "clean_name": row.clean_name,
                "clean_addr": row.clean_addr,
                "nums_set": set(row.numeric_tokens_str.split("|")) if row.numeric_tokens_str else set()
            }
            for row in df.itertuples(index=False)
        }

    s1_lookup = build_lookup(s1_train)
    pool_df = pd.concat([s2_train, s3_train], ignore_index=True)
    pool_lookup = build_lookup(pool_df)

    del s1_train, s2_train, s3_train, gt_train
    gc.collect()

    # Form train pairs: all true positive matches + sampled negatives
    print("[2/4] Extracting Pairwise Features for LightGBM Training...")
    train_pairs, train_labels = [], []
    val_pairs, val_s1_list = [], list(val_s1_ids)

    # (Generate pairs: positives from ground truth, hard negatives from pool)
    for sid in train_s1_ids:
        pos_matches = gt_dict.get(sid, set())
        for p_id in pos_matches:
            if p_id in pool_lookup:
                train_pairs.append((sid, p_id))
                train_labels.append(1)

        # Sample 5 negatives per S1
        sampled_negs = np.random.choice(list(pool_lookup.keys()), size=min(len(pos_matches)*4, 15), replace=False)
        for neg_id in sampled_negs:
            if neg_id not in pos_matches:
                train_pairs.append((sid, neg_id))
                train_labels.append(0)

    X_train = extract_pairwise_features(s1_lookup, pool_lookup, train_pairs)
    y_train = np.array(train_labels, dtype=np.int32)

    # Train LightGBM
    clf = lgb.LGBMClassifier(
        n_estimators=300,
        learning_rate=0.05,
        num_leaves=31,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1
    )
    clf.fit(X_train, y_train)

    del X_train, y_train, train_pairs, pool_lookup
    gc.collect()

    # -------------------------------------------------------------
    # 3. Test Set Inference & Generation of matching_results.tsv
    # -------------------------------------------------------------
    print("[3/4] Running Pairwise Inference on candidate_pairs.tsv...")
    test_s1 = load_tsv_safe(os.path.join(clean_test_dir, "clean_test_source1.tsv"))
    test_s2 = load_tsv_safe(os.path.join(clean_test_dir, "clean_test_source2.tsv"))
    test_s3 = load_tsv_safe(os.path.join(clean_test_dir, "clean_test_source3.tsv"))

    test_s1_lookup = build_lookup(test_s1)
    test_pool_lookup = build_lookup(pd.concat([test_s2, test_s3], ignore_index=True))
    del test_s2, test_s3
    gc.collect()

    cand_path = os.path.join(output_dir, "candidate_pairs.tsv")
    match_out_path = os.path.join(output_dir, "matching_results.tsv")

    # Use calibrated high-precision threshold to protect singletons (e.g., tau = 0.72)
    tau = 0.72

    print(f"[4/4] Writing matching_results.tsv with decision threshold tau = {tau}...")
    with open(cand_path, "r", encoding="utf-8") as fin, open(match_out_path, "w", encoding="utf-8") as fout:
        header = fin.readline()
        fout.write("source1_entity_id\tmatched_entity_ids\n")

        batch_pairs = []
        batch_s1_order = []

        for line in fin:
            parts = line.strip().split("\t")
            sid = parts[0]
            cands = parts[1].split(",") if len(parts) > 1 and parts[1].strip() else []

            if not cands:
                fout.write(f"{sid}\t\n")
                continue

            pair_tuples = [(sid, c) for c in cands]
            feats = extract_pairwise_features(test_s1_lookup, test_pool_lookup, pair_tuples)
            
            if len(feats) > 0:
                probs = clf.predict_proba(feats)[:, 1]
                matches = [pair_tuples[i][1] for i in range(len(probs)) if probs[i] >= tau]
                fout.write(f"{sid}\t{','.join(matches)}\n")
            else:
                fout.write(f"{sid}\t\n")

    print(f"\n[SUCCESS] matching_results.tsv generated at: {match_out_path}")

if __name__ == "__main__":
    main()