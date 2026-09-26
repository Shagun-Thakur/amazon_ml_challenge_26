import numpy as np
import pandas as pd
from rapidfuzz import distance, fuzz

def extract_pairwise_features(s1_records: dict, pool_records: dict, pairs: list):
    """
    Computes pairwise feature vectors for a list of (s1_id, pool_id) tuples.
    Returns: NumPy 2D array of features.
    """
    rows = []
    for s1_id, pool_id in pairs:
        s1 = s1_records.get(s1_id)
        cand = pool_records.get(pool_id)
        if not s1 or not cand:
            continue

        s1_name, s1_addr, s1_nums = s1["clean_name"], s1["clean_addr"], s1["nums_set"]
        cand_name, cand_addr, cand_nums = cand["clean_name"], cand["clean_addr"], cand["nums_set"]

        # 1. Lexical Name Similarities
        lev_sim = distance.Levenshtein.normalized_similarity(s1_name, cand_name)
        jw_sim = distance.JaroWinkler.similarity(s1_name, cand_name)
        token_sort = fuzz.token_sort_ratio(s1_name, cand_name) / 100.0

        # 2. Address & Numeric Features
        missing_cand_addr = 1.0 if len(cand_addr) == 0 else 0.0
        
        # Token Jaccard on address
        s1_addr_tokens = set(s1_addr.split()) if s1_addr else set()
        cand_addr_tokens = set(cand_addr.split()) if cand_addr else set()
        union_len = len(s1_addr_tokens.union(cand_addr_tokens))
        addr_jaccard = (len(s1_addr_tokens.intersection(cand_addr_tokens)) / union_len) if union_len > 0 else 0.0

        # Numeric Token Overlap & Conflict
        num_inter = len(s1_nums.intersection(cand_nums))
        num_conflict = 1.0 if (len(s1_nums) > 0 and len(cand_nums) > 0 and num_inter == 0) else 0.0

        rows.append([
            lev_sim,
            jw_sim,
            token_sort,
            addr_jaccard,
            float(num_inter),
            num_conflict,
            missing_cand_addr
        ])

    return np.array(rows, dtype=np.float32)