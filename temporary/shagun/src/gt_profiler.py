import pandas as pd


def audit_ground_truth(gt_df: pd.DataFrame) -> dict:
    """
    Analyzes ground truth match cardinality, singleton rate, and S2 vs S3 origin distribution.
    Optimized for high-scale memory efficiency.
    """
    total_anchors = len(gt_df)
    if total_anchors == 0:
        return {
            "total_source1_anchors": 0,
            "singleton_count": 0,
            "singleton_percentage": 0.0,
            "total_matches_linked": 0,
            "s2_matches_linked": 0,
            "s3_matches_linked": 0,
            "s2_match_percentage": 0.0,
            "s3_match_percentage": 0.0,
            "match_cardinality_distribution": {},
            "positive_match_distribution": {},
        }

    # Identify non-empty matched_entity_ids
    matched_col = gt_df["matched_entity_ids"].fillna("").astype(str)
    is_non_empty = (matched_col.str.strip() != "")

    # Calculate match count per S1 row: 0 for empty string, 1 + comma count for non-empty
    match_counts = is_non_empty.astype(int) + (matched_col.str.count(",") * is_non_empty)

    singletons = int((match_counts == 0).sum())
    singleton_rate = round((singletons / total_anchors) * 100, 4)
    positive_anchors = total_anchors - singletons

    # Fast vectorized prefix count
    s2_count = int(matched_col.str.count("S2-").sum())
    s3_count = int(matched_col.str.count("S3-").sum())
    total_matches = s2_count + s3_count

    s2_pct = round((s2_count / total_matches) * 100, 2) if total_matches > 0 else 0.0
    s3_pct = round((s3_count / total_matches) * 100, 2) if total_matches > 0 else 0.0

    cardinality_dist = {
        int(k): int(v) for k, v in match_counts.value_counts().sort_index().items()
    }
    positive_dist = {k: v for k, v in cardinality_dist.items() if k > 0}

    return {
        "total_source1_anchors": total_anchors,
        "singleton_count": singletons,
        "singleton_percentage": singleton_rate,
        "positive_anchors_count": positive_anchors,
        "positive_anchors_percentage": round((positive_anchors / total_anchors) * 100, 4),
        "total_matches_linked": total_matches,
        "s2_matches_linked": s2_count,
        "s3_matches_linked": s3_count,
        "s2_match_percentage": s2_pct,
        "s3_match_percentage": s3_pct,
        "max_matches_per_anchor": int(match_counts.max()) if total_anchors > 0 else 0,
        "mean_matches_per_anchor": round(float(match_counts.mean()), 4) if total_anchors > 0 else 0.0,
        "match_cardinality_distribution": cardinality_dist,
        "positive_match_distribution": positive_dist,
    }