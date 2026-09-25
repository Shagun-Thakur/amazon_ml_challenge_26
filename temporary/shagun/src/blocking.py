import os
import gc
import json
import numpy as np
import pandas as pd
from scipy.sparse import vstack
from sklearn.feature_extraction.text import TfidfVectorizer
from tqdm.auto import tqdm
from utils_io import resolve_project_paths, load_tsv_safe, save_tsv_safe

def run_tfidf_retrieval(s1_df: pd.DataFrame, pool_df: pd.DataFrame, text_col: str, top_k: int = 35, chunk_size: int = 10000):
    """
    Computes sparse character n-gram cosine similarities in memory-safe chunks.
    Returns: dict mapping s1_id -> set of candidate pool IDs.
    """
    if len(s1_df) == 0 or len(pool_df) == 0:
        return {}

    vectorizer = TfidfVectorizer(
        ngram_range=(3, 4),
        analyzer="char_wb",
        min_df=2,
        sublinear_tf=True
    )
    
    # Fit vectorizer on target pool
    pool_matrix = vectorizer.fit_transform(pool_df[text_col])
    pool_ids = pool_df["entity_id"].values
    
    results = {sid: set() for sid in s1_df["entity_id"].values}
    
    for start_idx in range(0, len(s1_df), chunk_size):
        end_idx = min(start_idx + chunk_size, len(s1_df))
        s1_chunk = s1_df.iloc[start_idx:end_idx]
        
        s1_matrix = vectorizer.transform(s1_chunk[text_col])
        sims = s1_matrix.dot(pool_matrix.T)  # Sparse dot product
        
        for i in range(sims.shape[0]):
            s1_id = s1_chunk.iloc[i]["entity_id"]
            row = sims.getrow(i)
            if row.nnz > 0:
                data = row.data
                indices = row.indices
                if len(data) > top_k:
                    # Partial sort for top-K speed
                    top_part = np.argpartition(data, -top_k)[-top_k:]
                    selected_indices = indices[top_part]
                else:
                    selected_indices = indices
                
                results[s1_id].update(pool_ids[selected_indices])
                
    return results

def block_country_partition(s1_df: pd.DataFrame, s2_df: pd.DataFrame, s3_df: pd.DataFrame, top_k: int = 35):
    """
    Executes dual-channel blocking per country partition.
    """
    candidates_by_s1 = {sid: set() for sid in s1_df["entity_id"].values}
    countries = s1_df["country"].unique()
    
    # Pool S2 and S3 together
    pool_all = pd.concat([s2_df, s3_df], ignore_index=True)
    
    for country in countries:
        sub_s1 = s1_df[s1_df["country"] == country].reset_index(drop=True)
        sub_pool = pool_all[pool_all["country"] == country].reset_index(drop=True)
        
        if len(sub_s1) == 0 or len(sub_pool) == 0:
            continue
            
        print(f"  [Country: {country}] S1: {len(sub_s1):,} | Candidate Pool (S2+S3): {len(sub_pool):,}")
        
        # Channel A: Primary composite matching (Clean Name + Clean Address)
        cand_map_a = run_tfidf_retrieval(sub_s1, sub_pool, text_col="composite_text", top_k=top_k)
        for sid, cands in cand_map_a.items():
            candidates_by_s1[sid].update(cands)
            
        # Channel B: Fallback name-only matching for missing-address records
        missing_addr_pool = sub_pool[sub_pool["clean_addr"] == ""].reset_index(drop=True)
        if len(missing_addr_pool) > 0:
            cand_map_b = run_tfidf_retrieval(sub_s1, missing_addr_pool, text_col="clean_name", top_k=10)
            for sid, cands in cand_map_b.items():
                candidates_by_s1[sid].update(cands)
                
    return candidates_by_s1

def evaluate_blocking_recall(s1_val_df: pd.DataFrame, candidates_map: dict, gt_df: pd.DataFrame):
    """
    Calculates validation candidate recall on non-singleton entities.
    """
    gt_map = {}
    for row in gt_df.itertuples(index=False):
        matches = [m.strip() for m in row.matched_entity_ids.split(",") if m.strip()]
        if matches:
            gt_map[row.source1_entity_id] = set(matches)
            
    total_true_positives = 0
    retrieved_true_positives = 0
    
    for sid in s1_val_df["entity_id"].values:
        if sid in gt_map:
            true_set = gt_map[sid]
            cand_set = candidates_map.get(sid, set())
            total_true_positives += len(true_set)
            retrieved_true_positives += len(true_set.intersection(cand_set))
            
    recall = (retrieved_true_positives / total_true_positives) if total_true_positives > 0 else 0.0
    return {
        "validation_true_matches": total_true_positives,
        "retrieved_true_matches": retrieved_true_positives,
        "blocking_recall": round(recall * 100, 2)
    }

def main():
    paths = resolve_project_paths()
    cleaned_train_dir = os.path.join(paths["cleaned_dir"], "train")
    cleaned_test_dir = os.path.join(paths["cleaned_dir"], "test")
    output_dir = os.path.join(paths["base_dir"], "output")
    os.makedirs(output_dir, exist_ok=True)
    
    # -------------------------------------------------------------
    # 1. Validation Benchmark on Sampled Training Data
    # -------------------------------------------------------------
    print("[1/2] Benchmarking Blocking Recall on Training Validation Split...")
    s1_train = load_tsv_safe(os.path.join(cleaned_train_dir, "clean_train_source1.tsv"))
    s2_train = load_tsv_safe(os.path.join(cleaned_train_dir, "clean_train_source2.tsv"))
    s3_train = load_tsv_safe(os.path.join(cleaned_train_dir, "clean_train_source3.tsv"))
    gt_train = load_tsv_safe(os.path.join(cleaned_train_dir, "clean_train_ground_truth.tsv"))
    
    # Sample 20,000 S1 entities stratified across country
    s1_val_sample = s1_train.groupby("country", group_keys=False).apply(
        lambda g: g.sample(min(len(g), 10000), random_state=42)
    ).reset_index(drop=True)
    
    # Run blocking on the validation subset against pooled training records
    # Subsample pool to fit comfortably in RAM
    s2_train_pool = s2_train.sample(min(len(s2_train), 400000), random_state=42)
    s3_train_pool = s3_train.sample(min(len(s3_train), 400000), random_state=42)
    
    # Make sure true ground-truth targets for sampled S1 are included in pool
    val_gt_ids = set()
    val_s1_set = set(s1_val_sample["entity_id"].values)
    for row in gt_train.itertuples(index=False):
        if row.source1_entity_id in val_s1_set:
            val_gt_ids.update([m.strip() for m in row.matched_entity_ids.split(",") if m.strip()])
            
    s2_needed = s2_train[s2_train["entity_id"].isin(val_gt_ids)]
    s3_needed = s3_train[s3_train["entity_id"].isin(val_gt_ids)]
    s2_eval_pool = pd.concat([s2_train_pool, s2_needed]).drop_duplicates(subset=["entity_id"]).reset_index(drop=True)
    s3_eval_pool = pd.concat([s3_train_pool, s3_needed]).drop_duplicates(subset=["entity_id"]).reset_index(drop=True)
    
    val_candidates = block_country_partition(s1_val_sample, s2_eval_pool, s3_eval_pool, top_k=35)
    recall_stats = evaluate_blocking_recall(s1_val_sample, val_candidates, gt_train)
    print(f"\n  ---> VALIDATION BLOCKING RECALL: {recall_stats['blocking_recall']}%")
    print(f"       ({recall_stats['retrieved_true_matches']:,} / {recall_stats['validation_true_matches']:,} true links retrieved)\n")
    
    # Release memory before test blocking
    del s1_train, s2_train, s3_train, gt_train, s1_val_sample, s2_eval_pool, s3_eval_pool, val_candidates
    gc.collect()
    
    # -------------------------------------------------------------
    # 2. Candidate Generation for Full Test Set
    # -------------------------------------------------------------
    print("[2/2] Generating candidate_pairs.tsv on Full Test Set (1.73M S1 entities)...")
    test_s1 = load_tsv_safe(os.path.join(cleaned_test_dir, "clean_test_source1.tsv"))
    test_s2 = load_tsv_safe(os.path.join(cleaned_test_dir, "clean_test_source2.tsv"))
    test_s3 = load_tsv_safe(os.path.join(cleaned_test_dir, "clean_test_source3.tsv"))
    
    test_candidates = block_country_partition(test_s1, test_s2, test_s3, top_k=35)
    
    print("\nFormatting output/candidate_pairs.tsv...")
    out_rows = []
    for sid in test_s1["entity_id"].values:
        cands = sorted(test_candidates.get(sid, []))[:40]  # Cap at top 40 candidates
        out_rows.append({
            "source1_entity_id": sid,
            "candidate_entity_ids": ",".join(cands)
        })
        
    cand_df = pd.DataFrame(out_rows)
    cand_out_path = os.path.join(output_dir, "candidate_pairs.tsv")
    cand_df.to_csv(cand_out_path, sep="\t", index=False)
    print(f"[SUCCESS] Saved {len(cand_df):,} rows to {cand_out_path}")

if __name__ == "__main__":
    main()