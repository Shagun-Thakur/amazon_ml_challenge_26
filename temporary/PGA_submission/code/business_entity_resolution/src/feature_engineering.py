# ==============================================================================
# AUTHORITATIVE FEATURE ENGINEERING MODULE (PGA MATCHER)
# Exact runtime implementation serialized directly from Phase-2 pipeline
# ==============================================================================
import numpy as np
import pandas as pd
from rapidfuzz import fuzz, distance

FEATURE_NAMES = [
    "name_levenshtein_similarity",
    "name_jaro_winkler",
    "name_token_sort_ratio",
    "name_token_set_ratio",
    "name_token_jaccard",
    "name_containment",
    "name_length_ratio",
    "addr_token_jaccard",
    "addr_containment",
    "addr_levenshtein_similarity",
    "addr_length_ratio",
    "addr_exact",
    "numeric_overlap_count",
    "numeric_jaccard",
    "numeric_exact_match",
    "numeric_conflict",
    "s1_missing_address",
    "target_missing_address",
    "both_missing_address",
    "same_country",
    "target_source",
    "candidate_rank",
    "normalized_candidate_rank",
    "reciprocal_candidate_rank",
    "candidate_count_for_s1"
]

def cache_records_for_ids(tsv_path, active_ids):
    rec_dict = {}
    for chunk in pd.read_csv(tsv_path, sep="\t", dtype=str, keep_default_na=False, chunksize=100000):
        matched = chunk[chunk['entity_id'].isin(active_ids)]
        for _, r in matched.iterrows():
            eid = r['entity_id']
            c_name = str(r.get('clean_name', '')).strip()
            c_addr = str(r.get('clean_addr', '')).strip()
            nums = set(str(r.get('numeric_tokens_str', '')).split()) - {''}
            rec_dict[eid] = {
                'clean_name': c_name,
                'clean_addr': c_addr,
                'country': str(r.get('country', '')).strip(),
                'name_tokens': set(c_name.split()),
                'addr_tokens': set(c_addr.split()),
                'num_tokens': nums
            }
    return rec_dict


def extract_features_chunk(pairs_df, s1_dict, target_dict):
    n = len(pairs_df)
    feats = np.zeros((n, len(FEATURE_NAMES)), dtype=np.float32)
    
    s1_ids = pairs_df['source1_entity_id'].values
    cand_ids = pairs_df['candidate_entity_id'].values
    ranks = pairs_df['candidate_rank'].values.astype(np.float32)
    cand_counts = pairs_df['candidate_count'].values.astype(np.float32)

    for i in range(n):
        s1 = s1_dict.get(s1_ids[i])
        tgt = target_dict.get(cand_ids[i])
        if s1 is None or tgt is None:
            continue
            
        # Name Metrics
        s1_n, tgt_n = s1['clean_name'], tgt['clean_name']
        s1_n_tok, tgt_n_tok = s1['name_tokens'], tgt['name_tokens']
        len_s1_n, len_tgt_n = len(s1_n), len(tgt_n)
        
        feats[i, 6] = min(len_s1_n, len_tgt_n) / max(1, max(len_s1_n, len_tgt_n))
        
        # Jaccard / Containment (Name)
        n_inter = len(s1_n_tok.intersection(tgt_n_tok))
        n_union = len(s1_n_tok.union(tgt_n_tok))
        feats[i, 4] = float(n_inter) / n_union if n_union > 0 else 0.0
        min_n = min(len(s1_n_tok), len(tgt_n_tok))
        feats[i, 5] = float(n_inter) / min_n if min_n > 0 else 0.0
        
        if DEP_STATUS["rapidfuzz"]:
            feats[i, 0] = fuzz.ratio(s1_n, tgt_n) / 100.0
            feats[i, 1] = distance.JaroWinkler.similarity(s1_n, tgt_n)
            feats[i, 2] = fuzz.token_sort_ratio(s1_n, tgt_n) / 100.0
            feats[i, 3] = fuzz.token_set_ratio(s1_n, tgt_n) / 100.0
        else:
            eq = 1.0 if s1_n == tgt_n else 0.0
            feats[i, 0] = eq; feats[i, 1] = eq; feats[i, 2] = feats[i, 4]; feats[i, 3] = feats[i, 5]

        # Address Metrics
        s1_a, tgt_a = s1['clean_addr'], tgt['clean_addr']
        s1_a_tok, tgt_a_tok = s1['addr_tokens'], tgt['addr_tokens']
        len_s1_a, len_tgt_a = len(s1_a), len(tgt_a)
        
        feats[i, 11] = 1.0 if s1_a and s1_a == tgt_a else 0.0
        feats[i, 10] = min(len_s1_a, len_tgt_a) / max(1, max(len_s1_a, len_tgt_a))
        
        a_inter = len(s1_a_tok.intersection(tgt_a_tok))
        a_union = len(s1_a_tok.union(tgt_a_tok))
        feats[i, 7] = float(a_inter) / a_union if a_union > 0 else 0.0
        min_a = min(len(s1_a_tok), len(tgt_a_tok))
        feats[i, 8] = float(a_inter) / min_a if min_a > 0 else 0.0
        
        if DEP_STATUS["rapidfuzz"]:
            feats[i, 9] = fuzz.ratio(s1_a, tgt_a) / 100.0
        else:
            feats[i, 9] = feats[i, 11]

        # Numeric Metrics
        s1_num, tgt_num = s1['num_tokens'], tgt['num_tokens']
        num_inter = len(s1_num.intersection(tgt_num))
        num_union = len(s1_num.union(tgt_num))
        feats[i, 12] = float(num_inter)
        feats[i, 13] = float(num_inter) / num_union if num_union > 0 else 0.0
        feats[i, 14] = 1.0 if s1_num and s1_num == tgt_num else 0.0
        feats[i, 15] = 1.0 if len(s1_num) > 0 and len(tgt_num) > 0 and num_inter == 0 else 0.0

        # Missingness
        m_s1 = 1.0 if len(s1_a) == 0 else 0.0
        m_tgt = 1.0 if len(tgt_a) == 0 else 0.0
        feats[i, 16] = m_s1
        feats[i, 17] = m_tgt
        feats[i, 18] = 1.0 if m_s1 and m_tgt else 0.0

        # Structural & Retrieval Rank
        feats[i, 19] = 1.0 if s1['country'] == tgt['country'] else 0.0
        feats[i, 20] = 1.0 if cand_ids[i].startswith('S2-') else 2.0
        feats[i, 21] = ranks[i]
        feats[i, 22] = ranks[i] / max(1.0, cand_counts[i])
        feats[i, 23] = 1.0 / ranks[i]
        feats[i, 24] = cand_counts[i]

    return feats

