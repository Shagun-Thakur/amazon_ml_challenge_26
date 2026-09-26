import gc
import os
import sys
import time
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

# Ensure local imports within business_entity_resolution/code/src/
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from utils_io import resolve_project_paths


def evaluate_validation_blocking(
    train_dir: str,
    sample_size: int = 2000,
    k_name: int = 12,
    k_comp: int = 12,
) -> float:
    """
    Evaluates blocking recall on a sampled slice of the training set.
    Tests dual-channel TF-IDF retrieval against a target pool of true matches + 50k distractors.
    """
    print("\n" + "=" * 70)
    print("STEP 1: EVALUATING VALIDATION BLOCKING RECALL (SAMPLED TRAIN SET)")
    print("=" * 70)

    t0 = time.time()
    gt_path = os.path.join(train_dir, "train_ground_truth.tsv")
    print(f"Loading ground truth from {gt_path}...")
    gt = pd.read_csv(
        gt_path,
        sep="\t",
        dtype=str,
        keep_default_na=False,
        nrows=sample_size * 2,
    )
    gt_pos = gt[gt["matched_entity_ids"] != ""].iloc[:sample_size].reset_index(drop=True)
    true_matches = {
        row["source1_entity_id"]: set(row["matched_entity_ids"].split(","))
        for _, row in gt_pos.iterrows()
    }

    s1_set = set(true_matches.keys())
    needed_s2 = {m for mids in true_matches.values() for m in mids if m.startswith("S2-")}
    needed_s3 = {m for mids in true_matches.values() for m in mids if m.startswith("S3-")}

    print(f"Selected {len(s1_set):,} positive S1 anchors with {len(needed_s2) + len(needed_s3):,} true matches.")

    # 1. Load S1 queries
    s1_rows = []
    with open(os.path.join(train_dir, "train_source1.tsv"), "r", encoding="utf-8") as f:
        h = f.readline()
        for line in f:
            if line.split("\t", 1)[0] in s1_set:
                s1_rows.append(line)
    import io
    s1_df = pd.read_csv(io.StringIO(h + "".join(s1_rows)), sep="\t", dtype=str, keep_default_na=False)

    # 2. Load S2 targets + distractors
    s2_rows, d_s2 = [], []
    with open(os.path.join(train_dir, "train_source2.tsv"), "r", encoding="utf-8") as f:
        h = f.readline()
        for line in f:
            eid = line.split("\t", 1)[0]
            if eid in needed_s2:
                s2_rows.append(line)
            elif len(d_s2) < 25000:
                d_s2.append(line)
    s2_df = pd.read_csv(io.StringIO(h + "".join(s2_rows + d_s2)), sep="\t", dtype=str, keep_default_na=False)

    # 3. Load S3 targets + distractors
    s3_rows, d_s3 = [], []
    with open(os.path.join(train_dir, "train_source3.tsv"), "r", encoding="utf-8") as f:
        h = f.readline()
        for line in f:
            eid = line.split("\t", 1)[0]
            if eid in needed_s3:
                s3_rows.append(line)
            elif len(d_s3) < 25000:
                d_s3.append(line)
    s3_df = pd.read_csv(io.StringIO(h + "".join(s3_rows + d_s3)), sep="\t", dtype=str, keep_default_na=False)

    targets_df = pd.concat([s2_df, s3_df], ignore_index=True)
    del s2_df, s3_df
    gc.collect()

    print(
        f"Validation Pool constructed in {time.time() - t0:.2f}s: "
        f"{len(s1_df):,} queries vs {len(targets_df):,} targets."
    )

    total_hits = 0
    total_possible = sum(len(v) for v in true_matches.values())

    for c in ["US", "India"]:
        s1_c = s1_df[s1_df["country"] == c].reset_index(drop=True)
        t_c = targets_df[targets_df["country"] == c].reset_index(drop=True)
        t_ids = t_c["entity_id"].values

        # Channel 1: Name TF-IDF (max_features=50000, dtype=np.float32)
        vec_name = TfidfVectorizer(
            analyzer="char_wb",
            ngram_range=(3, 3),
            min_df=2,
            max_df=0.01,
            max_features=50000,
            dtype=np.float32,
        )
        X_t_name = vec_name.fit_transform(t_c["clean_name"])
        X_q_name = vec_name.transform(s1_c["clean_name"])

        # Channel 2: Composite TF-IDF (max_features=50000, dtype=np.float32)
        vec_comp = TfidfVectorizer(
            analyzer="char_wb",
            ngram_range=(3, 3),
            min_df=2,
            max_df=0.01,
            max_features=50000,
            dtype=np.float32,
        )
        X_t_comp = vec_comp.fit_transform(t_c["composite_text"])
        X_q_comp = vec_comp.transform(s1_c["composite_text"])

        sim_name = X_q_name.dot(X_t_name.T)
        sim_comp = X_q_comp.dot(X_t_comp.T)

        ptr_n, ind_n, d_n = sim_name.indptr, sim_name.indices, sim_name.data
        ptr_c, ind_c, d_c = sim_comp.indptr, sim_comp.indices, sim_comp.data

        hits_c = 0
        total_c = 0

        for i in range(len(s1_c)):
            s1_id = s1_c.loc[i, "entity_id"]
            mids = true_matches[s1_id]
            total_c += len(mids)

            # Direct buffer access for Channel 1
            sn, en = ptr_n[i], ptr_n[i + 1]
            top_n = []
            if en > sn:
                d = d_n[sn:en]
                k = min(k_name, en - sn)
                part = np.argpartition(d, -k)[-k:]
                top_n = ind_n[sn:en][part[np.argsort(-d[part])]].tolist()

            # Direct buffer access for Channel 2
            sc, ec = ptr_c[i], ptr_c[i + 1]
            top_c = []
            if ec > sc:
                d = d_c[sc:ec]
                k = min(k_comp, ec - sc)
                part = np.argpartition(d, -k)[-k:]
                top_c = ind_c[sc:ec][part[np.argsort(-d[part])]].tolist()

            cand_indices = list(dict.fromkeys(top_n + top_c))
            cand_ids = set(t_ids[cand_indices])
            hits_c += len(mids.intersection(cand_ids))

        total_hits += hits_c
        c_recall = (hits_c / total_c) * 100 if total_c > 0 else 0.0
        print(f"  -> Country {c}: Recall = {c_recall:.2f}% ({hits_c:,} / {total_c:,} true links captured)")

    overall_recall = (total_hits / total_possible) * 100 if total_possible > 0 else 0.0
    print(f"\n>>> OVERALL VALIDATION BLOCKING RECALL: {overall_recall:.2f}% ({total_hits:,} / {total_possible:,})")
    print(f">>> Target Status (>= 90% - 95%): {'PASSED' if overall_recall >= 90.0 else 'FAILED'}")

    del s1_df, targets_df
    gc.collect()
    return overall_recall


def run_full_test_blocking(
    cleaned_test_dir: str,
    output_path: str,
    k_name: int = 12,
    k_comp: int = 12,
):
    """
    Executes country-partitioned dual-channel TF-IDF retrieval for all 1,732,544 test S1 entities.
    Employs direct buffer access (indptr, indices, data) and streams lines directly to disk.
    Prints execution velocity updates every 50,000 entities.
    Resumes incrementally if partitions are already written to output/candidate_pairs.tsv.
    """
    print("\n" + "=" * 70)
    print("STEP 2: FULL TEST CANDIDATE BLOCKING (1,732,544 S1 ENTITIES)")
    print("=" * 70)

    start_time = time.time()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # 1. Ingest S1 test queries with usecols
    t0 = time.time()
    print("Ingesting test_source1.tsv queries...")
    s1_df = pd.read_csv(
        os.path.join(cleaned_test_dir, "test_source1.tsv"),
        sep="\t",
        dtype=str,
        keep_default_na=False,
        usecols=["entity_id", "country", "clean_name", "composite_text"],
    )
    total_test_s1 = len(s1_df)
    print(f"  Loaded {total_test_s1:,} queries in {time.time() - t0:.2f}s.")

    # 2. Check existing progress in output file
    already_written_ids = set()
    if os.path.exists(output_path):
        with open(output_path, "r", encoding="utf-8") as f:
            header = f.readline()
            for line in f:
                if line.strip():
                    already_written_ids.add(line.split("\t", 1)[0])
        print(f"  Detected existing output: {len(already_written_ids):,} entities already written.")
    else:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("source1_entity_id\tcandidate_entity_ids\n")

    # If completely done, verify and return
    if len(already_written_ids) == total_test_s1:
        print("  All 1,732,544 entities already present in output file!")
        return

    # 3. Ingest S2 and S3 test targets with usecols
    t0 = time.time()
    print("Ingesting test_source2.tsv and test_source3.tsv targets...")
    s2_df = pd.read_csv(
        os.path.join(cleaned_test_dir, "test_source2.tsv"),
        sep="\t",
        dtype=str,
        keep_default_na=False,
        usecols=["entity_id", "country", "clean_name", "composite_text"],
    )
    s3_df = pd.read_csv(
        os.path.join(cleaned_test_dir, "test_source3.tsv"),
        sep="\t",
        dtype=str,
        keep_default_na=False,
        usecols=["entity_id", "country", "clean_name", "composite_text"],
    )
    targets_all = pd.concat([s2_df, s3_df], ignore_index=True)
    del s2_df, s3_df
    gc.collect()
    print(f"  Loaded {len(targets_all):,} total target records in {time.time() - t0:.2f}s.")

    # 4. Country Partitioned Retrieval with Direct Buffer Access & Streaming
    countries = ["France", "US", "India"]
    total_processed_global = len(already_written_ids)

    with open(output_path, "a", encoding="utf-8") as out_file:
        for country in countries:
            c_t0 = time.time()
            print(f"\n--- Processing Country Partition: {country} ---")

            s1_mask = s1_df["country"] == country
            q_subset = s1_df[s1_mask].reset_index(drop=True)

            # Filter out queries already written to file
            if already_written_ids:
                unprocessed_mask = ~q_subset["entity_id"].isin(already_written_ids)
                q_subset = q_subset[unprocessed_mask].reset_index(drop=True)

            q_ids = q_subset["entity_id"].values
            n_queries = len(q_subset)

            t_mask = targets_all["country"] == country
            t_subset = targets_all[t_mask].reset_index(drop=True)
            t_ids = t_subset["entity_id"].values
            n_targets = len(t_subset)

            print(f"  Remaining Queries (S1): {n_queries:,} | Targets (S2+S3): {n_targets:,}")

            if n_queries == 0:
                print(f"  Partition {country} already fully completed, skipping.")
                continue

            # Tuned settings per country scale:
            # India has 4.7M targets; tighter max_df avoids 1.8B non-zero allocations
            if country == "India":
                chunk_size = 2500
                max_df_name = 0.005
                min_df_comp = 10
                max_df_comp = 0.003
            else:
                chunk_size = 5000
                max_df_name = 0.01
                min_df_comp = 5
                max_df_comp = 0.01

            # Channel 1: Name TF-IDF (max_features=50000, dtype=np.float32)
            v0 = time.time()
            print(f"  Fitting Channel 1 (clean_name char_wb (3,3), max_df={max_df_name}, max_features=50,000)...")
            vec_name = TfidfVectorizer(
                analyzer="char_wb",
                ngram_range=(3, 3),
                min_df=5,
                max_df=max_df_name,
                max_features=50000,
                dtype=np.float32,
            )
            X_target_name = vec_name.fit_transform(t_subset["clean_name"])
            X_query_name = vec_name.transform(q_subset["clean_name"])
            print(f"  Channel 1 fitted in {time.time() - v0:.2f}s (Vocabulary: {X_target_name.shape[1]:,})")

            # Channel 2: Composite TF-IDF (max_features=50000, dtype=np.float32)
            v0 = time.time()
            print(f"  Fitting Channel 2 (composite_text char_wb (3,3), max_df={max_df_comp}, max_features=50,000)...")
            vec_comp = TfidfVectorizer(
                analyzer="char_wb",
                ngram_range=(3, 3),
                min_df=min_df_comp,
                max_df=max_df_comp,
                max_features=50000,
                dtype=np.float32,
            )
            X_target_comp = vec_comp.fit_transform(t_subset["composite_text"])
            X_query_comp = vec_comp.transform(q_subset["composite_text"])
            print(f"  Channel 2 fitted in {time.time() - v0:.2f}s (Vocabulary: {X_target_comp.shape[1]:,})")

            # Free raw string data to keep RAM minimal
            del t_subset, q_subset
            gc.collect()

            # Chunked Sparse Processing with Direct CSR Buffer Slicing
            print(f"  Streaming Retrieval (chunk_size={chunk_size:,})...")
            num_chunks = int(np.ceil(n_queries / chunk_size))
            country_processed = 0

            for chunk_idx in range(num_chunks):
                ch_start = chunk_idx * chunk_size
                ch_end = min((chunk_idx + 1) * chunk_size, n_queries)
                current_chunk_len = ch_end - ch_start

                # Multiply chunk
                sim_name = X_query_name[ch_start:ch_end].dot(X_target_name.T)
                sim_comp = X_query_comp[ch_start:ch_end].dot(X_target_comp.T)

                # Direct internal buffer pointers (no getrow / no slice object allocations)
                ptr_n, ind_n, d_n = sim_name.indptr, sim_name.indices, sim_name.data
                ptr_c, ind_c, d_c = sim_comp.indptr, sim_comp.indices, sim_comp.data

                # Stream rows directly to disk
                lines_buffer = []
                for local_i in range(current_chunk_len):
                    s1_id = q_ids[ch_start + local_i]

                    # Fast buffer slice for Channel 1
                    sn, en = ptr_n[local_i], ptr_n[local_i + 1]
                    top_n = []
                    if en > sn:
                        d = d_n[sn:en]
                        k = min(k_name, en - sn)
                        part = np.argpartition(d, -k)[-k:]
                        top_n = ind_n[sn:en][part[np.argsort(-d[part])]].tolist()

                    # Fast buffer slice for Channel 2
                    sc, ec = ptr_c[local_i], ptr_c[local_i + 1]
                    top_c = []
                    if ec > sc:
                        d = d_c[sc:ec]
                        k = min(k_comp, ec - sc)
                        part = np.argpartition(d, -k)[-k:]
                        top_c = ind_c[sc:ec][part[np.argsort(-d[part])]].tolist()

                    # Merge & deduplicate
                    cand_indices = list(dict.fromkeys(top_n + top_c))
                    if cand_indices:
                        cand_ids = [t_ids[idx] for idx in cand_indices]
                        cand_str = ",".join(cand_ids)
                    else:
                        cand_str = ""

                    lines_buffer.append(f"{s1_id}\t{cand_str}\n")

                out_file.writelines(lines_buffer)
                out_file.flush()

                country_processed += current_chunk_len
                total_processed_global += current_chunk_len

                # Print progress updates every 50,000 entities
                if total_processed_global % 50000 < chunk_size or total_processed_global == total_test_s1:
                    overall_elapsed = max(time.time() - start_time, 0.001)
                    vel = total_processed_global / overall_elapsed
                    print(
                        f"  [Progress] Processed {total_processed_global:,} / {total_test_s1:,} entities "
                        f"({vel:,.0f} entities/s, Elapsed: {overall_elapsed:.1f}s)"
                    )

                del sim_name, sim_comp, lines_buffer

            print(f"  Partition {country} complete in {(time.time() - c_t0) / 60:.2f} mins.")

            # Free partition variables and matrix buffers
            del X_target_name, X_query_name, X_target_comp, X_query_comp
            del vec_name, vec_comp, q_ids, t_ids
            gc.collect()

    del targets_all, s1_df
    gc.collect()

    # 5. Verification of output row count
    print(f"\nVerifying generated output: {output_path}...")
    with open(output_path, "r", encoding="utf-8") as f:
        header = f.readline()
        n_rows = sum(1 for _ in f)

    print(f"Header: {header.strip()}")
    print(f"Total entity rows: {n_rows:,} (Expected: {total_test_s1:,})")
    assert n_rows == total_test_s1, f"Mismatch in row count: {n_rows} != {total_test_s1}"

    # Also link/copy to student_resource/output/ for validate_submission.py
    student_out = os.path.join(
        os.path.dirname(os.path.dirname(cleaned_test_dir)),
        "student_resource",
        "output",
        "candidate_pairs.tsv",
    )
    try:
        os.makedirs(os.path.dirname(student_out), exist_ok=True)
        if os.path.abspath(output_path) != os.path.abspath(student_out):
            if os.path.exists(student_out):
                os.remove(student_out)
            os.link(output_path, student_out)
            print(f"Linked candidate pairs to: {student_out}")
    except Exception as e:
        print(f"Note: Could not link to student_resource/output: {e}")

    total_time = time.time() - start_time
    print("\n" + "=" * 70)
    print(f"BLOCKING PIPELINE COMPLETE in {total_time / 60:.2f} minutes ({total_time:.1f}s)")
    print(f"Output confirmed: {output_path} with exactly {n_rows:,} rows.")
    print("=" * 70)


def main():
    paths = resolve_project_paths()
    cleaned_train_dir = paths["cleaned_train_dir"]
    cleaned_test_dir = paths["cleaned_test_dir"]
    project_root = paths["project_root"]
    output_path = os.path.join(project_root, "output", "candidate_pairs.tsv")

    # Step 1: Validation Blocking Recall Benchmark
    val_recall = evaluate_validation_blocking(
        train_dir=cleaned_train_dir,
        sample_size=2000,
        k_name=12,
        k_comp=12,
    )

    # Step 2: Full Test Candidate Generation
    run_full_test_blocking(
        cleaned_test_dir=cleaned_test_dir,
        output_path=output_path,
        k_name=12,
        k_comp=12,
    )


if __name__ == "__main__":
    main()