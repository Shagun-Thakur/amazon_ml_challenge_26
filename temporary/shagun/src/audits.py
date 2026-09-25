import re
import pandas as pd


def audit_schema_and_quality(df: pd.DataFrame, expected_cols: list, prefix: str) -> dict:
    """
    Runs data quality diagnostics:
    - schema validity & missing columns
    - null counts (isna)
    - empty string counts ("")
    - whitespace-only string counts ("   ")
    - duplicate entity_ids
    - invalid entity_id format matching prefix (e.g. S1-12345)
    - country distribution
    """
    total_rows = len(df)
    cols_present = list(df.columns)
    missing_cols = [col for col in expected_cols if col not in cols_present]
    schema_ok = len(missing_cols) == 0

    null_counts = {col: int(df[col].isna().sum()) for col in cols_present}
    empty_counts = {col: int((df[col] == "").sum()) for col in cols_present}
    whitespace_counts = {
        col: int(((df[col].str.strip() == "") & (df[col] != "")).sum())
        for col in cols_present
    }

    dup_ids = int(df["entity_id"].duplicated().sum()) if "entity_id" in df.columns else 0
    clean_prefix = prefix.rstrip("-")
    id_pattern = rf"^{clean_prefix}-\d+$"
    invalid_ids = (
        int((~df["entity_id"].str.match(id_pattern, na=False)).sum())
        if "entity_id" in df.columns
        else 0
    )
    country_dist = df["country"].value_counts().to_dict() if "country" in df.columns else {}

    return {
        "total_rows": total_rows,
        "schema_valid": schema_ok,
        "missing_columns": missing_cols,
        "null_counts": null_counts,
        "empty_string_counts": empty_counts,
        "whitespace_only_counts": whitespace_counts,
        "duplicate_entity_ids": dup_ids,
        "invalid_id_format_count": invalid_ids,
        "country_distribution": country_dist,
    }


def audit_ground_truth_schema(gt_df: pd.DataFrame) -> dict:
    """
    Validates schema and missing values specifically for train_ground_truth.tsv.
    Expected columns: ["source1_entity_id", "matched_entity_ids"]
    """
    expected_cols = ["source1_entity_id", "matched_entity_ids"]
    total_rows = len(gt_df)
    cols_present = list(gt_df.columns)
    missing_cols = [col for col in expected_cols if col not in cols_present]
    schema_ok = len(missing_cols) == 0

    null_counts = {col: int(gt_df[col].isna().sum()) for col in cols_present}
    empty_counts = {col: int((gt_df[col] == "").sum()) for col in cols_present}
    whitespace_counts = {
        col: int(((gt_df[col].str.strip() == "") & (gt_df[col] != "")).sum())
        for col in cols_present
    }

    dup_s1 = (
        int(gt_df["source1_entity_id"].duplicated().sum())
        if "source1_entity_id" in gt_df.columns
        else 0
    )
    invalid_s1_format = (
        int((~gt_df["source1_entity_id"].str.match(r"^S1-\d+$", na=False)).sum())
        if "source1_entity_id" in gt_df.columns
        else 0
    )

    return {
        "total_rows": total_rows,
        "schema_valid": schema_ok,
        "missing_columns": missing_cols,
        "null_counts": null_counts,
        "empty_string_counts": empty_counts,
        "whitespace_only_counts": whitespace_counts,
        "duplicate_source1_entity_ids": dup_s1,
        "invalid_source1_id_format_count": invalid_s1_format,
    }