import gc
import json
import os
import sys
import time

# Ensure project root and src are on sys.path
src_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
project_root = os.path.dirname(src_dir)
for p in (project_root, src_dir):
    if p not in sys.path:
        sys.path.insert(0, p)

try:
    from utils.utils_io import resolve_project_paths, load_tsv_safe, save_tsv_safe
    from data.audits import audit_schema_and_quality, audit_ground_truth_schema
    from features.structural_features import transform_dataframe
    from evaluation.gt_profiler import audit_ground_truth
except ImportError:
    from src.utils.utils_io import resolve_project_paths, load_tsv_safe, save_tsv_safe
    from src.data.audits import audit_schema_and_quality, audit_ground_truth_schema
    from src.features.structural_features import transform_dataframe
    from src.evaluation.gt_profiler import audit_ground_truth


def safe_link_or_copy(src_path: str, dst_path: str) -> None:
    """Creates a hardlink to avoid duplicating disk space, falls back to copy."""
    if os.path.abspath(src_path) == os.path.abspath(dst_path):
        return
    if os.path.exists(dst_path):
        return
    try:
        os.link(src_path, dst_path)
    except (OSError, NotImplementedError):
        import shutil
        shutil.copy2(src_path, dst_path)


def run_pipeline():
    start_time = time.time()
    print("=" * 70)
    print("STARTING STAGE 1: INGESTION, AUDIT & NORMALIZATION PIPELINE")
    print("=" * 70)

    paths = resolve_project_paths()
    project_root = paths["project_root"]
    cleaned_train_dir = paths["cleaned_train_dir"]
    cleaned_test_dir = paths["cleaned_test_dir"]
    reports_dir = paths["reports_dir"]

    os.makedirs(cleaned_train_dir, exist_ok=True)
    os.makedirs(cleaned_test_dir, exist_ok=True)
    os.makedirs(reports_dir, exist_ok=True)

    print(f"Project Root: {project_root}")
    print(f"Raw Train Dir: {paths['train_dir']}")
    print(f"Raw Test Dir:  {paths['test_dir']}")
    print(f"Cleaned Dir:   {paths['cleaned_dir']}")
    print(f"Reports Dir:   {reports_dir}\n")

    report = {
        "metadata": {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "pipeline": "Stage 1 Ingestion, Audit & Normalization",
        },
        "ground_truth": {},
        "train": {},
        "test": {},
    }

    expected_source_cols = ["entity_id", "business_name", "business_address", "country"]

    # -------------------------------------------------------------
    # 1. Ground Truth Ingestion, Audit & Profiling
    # -------------------------------------------------------------
    gt_file = "train_ground_truth.tsv"
    gt_raw_path = os.path.join(paths["train_dir"], gt_file)
    if os.path.exists(gt_raw_path):
        print(f"[1/3] Processing Ground Truth: {gt_file}...")
        t0 = time.time()
        gt_df = load_tsv_safe(gt_raw_path)
        schema_audit = audit_ground_truth_schema(gt_df)
        gt_profile = audit_ground_truth(gt_df)

        report["ground_truth"] = {
            "schema_audit": schema_audit,
            "profiling": gt_profile,
        }

        clean_gt_path = os.path.join(cleaned_train_dir, "clean_train_ground_truth.tsv")
        save_tsv_safe(gt_df, clean_gt_path)
        safe_link_or_copy(clean_gt_path, os.path.join(cleaned_train_dir, gt_file))

        print(
            f"  -> Profiled {len(gt_df):,} ground truth anchors in {time.time() - t0:.2f}s "
            f"(Singletons: {gt_profile['singleton_count']:,} [{gt_profile['singleton_percentage']}%], "
            f"Linked matches: {gt_profile['total_matches_linked']:,})"
        )

        del gt_df
        gc.collect()
    else:
        print(f"[WARN] Ground truth file not found at {gt_raw_path}")

    # -------------------------------------------------------------
    # 2. Train Sources Ingestion, Audit & Cleaning
    # -------------------------------------------------------------
    print("\n[2/3] Processing Training Sources...")
    train_sources = [
        ("train_source1.tsv", "S1", "clean_train_source1.tsv"),
        ("train_source2.tsv", "S2", "clean_train_source2.tsv"),
        ("train_source3.tsv", "S3", "clean_train_source3.tsv"),
    ]

    for filename, prefix, out_name in train_sources:
        raw_path = os.path.join(paths["train_dir"], filename)
        if not os.path.exists(raw_path):
            print(f"  [WARN] Missing training file: {raw_path}")
            continue

        t0 = time.time()
        print(f"  Ingesting {filename}...")
        df = load_tsv_safe(raw_path)
        row_count = len(df)

        # Audit
        audit_res = audit_schema_and_quality(df, expected_source_cols, prefix)
        report["train"][filename] = audit_res

        # Normalization and Feature Engineering
        print(f"  Transforming {filename} ({row_count:,} records)...")
        df = transform_dataframe(df)

        # Output serialization
        clean_out_path = os.path.join(cleaned_train_dir, out_name)
        save_tsv_safe(df, clean_out_path)
        safe_link_or_copy(clean_out_path, os.path.join(cleaned_train_dir, filename))

        elapsed = time.time() - t0
        print(
            f"  -> Finished {out_name}: {row_count:,} rows written in {elapsed:.2f}s "
            f"({row_count / max(elapsed, 0.001):,.0f} rows/s)"
        )

        # Explicit garbage collection to keep RAM strictly bounded
        del df
        gc.collect()

    # -------------------------------------------------------------
    # 3. Test Sources Ingestion, Audit & Cleaning
    # -------------------------------------------------------------
    print("\n[3/3] Processing Test Sources...")
    test_sources = [
        ("test_source1.tsv", "S1", "clean_test_source1.tsv"),
        ("test_source2.tsv", "S2", "clean_test_source2.tsv"),
        ("test_source3.tsv", "S3", "clean_test_source3.tsv"),
    ]

    for filename, prefix, out_name in test_sources:
        raw_path = os.path.join(paths["test_dir"], filename)
        if not os.path.exists(raw_path):
            print(f"  [WARN] Missing test file: {raw_path}")
            continue

        t0 = time.time()
        print(f"  Ingesting {filename}...")
        df = load_tsv_safe(raw_path)
        row_count = len(df)

        # Audit
        audit_res = audit_schema_and_quality(df, expected_source_cols, prefix)
        report["test"][filename] = audit_res

        # Normalization and Feature Engineering
        print(f"  Transforming {filename} ({row_count:,} records)...")
        df = transform_dataframe(df)

        # Output serialization
        clean_out_path = os.path.join(cleaned_test_dir, out_name)
        save_tsv_safe(df, clean_out_path)
        safe_link_or_copy(clean_out_path, os.path.join(cleaned_test_dir, filename))

        elapsed = time.time() - t0
        print(
            f"  -> Finished {out_name}: {row_count:,} rows written in {elapsed:.2f}s "
            f"({row_count / max(elapsed, 0.001):,.0f} rows/s)"
        )

        # Explicit garbage collection to keep RAM strictly bounded
        del df
        gc.collect()

    # -------------------------------------------------------------
    # Save Final Audit Report
    # -------------------------------------------------------------
    total_pipeline_time = time.time() - start_time
    report["metadata"]["duration_seconds"] = round(total_pipeline_time, 2)

    report_path = os.path.join(reports_dir, "data_audit_report.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    print("\n" + "=" * 70)
    print(f"PIPELINE COMPLETE in {total_pipeline_time / 60:.2f} minutes ({total_pipeline_time:.1f}s)")
    print(f"Audit report successfully written to: {report_path}")
    print("=" * 70)


if __name__ == "__main__":
    run_pipeline()
