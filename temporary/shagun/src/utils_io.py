import os
import pandas as pd


def resolve_project_paths():
    """
    Dynamically resolves project root, dataset, cleaned output, and report directories.
    Searches upwards from both the current working directory and this file's location.
    """
    candidate_anchors = [os.getcwd(), os.path.dirname(os.path.abspath(__file__))]
    project_root = None

    for anchor in candidate_anchors:
        curr = os.path.abspath(anchor)
        while True:
            # Check for project markers
            if (
                os.path.exists(os.path.join(curr, "AGENT.md"))
                or os.path.exists(os.path.join(curr, "student_resource"))
                or os.path.exists(os.path.join(curr, "data_cleaned"))
            ):
                project_root = curr
                break
            parent = os.path.dirname(curr)
            if parent == curr:
                break
            curr = parent
        if project_root is not None:
            break

    if project_root is None:
        project_root = os.getcwd()

    # Search for dataset train and test directories
    possible_dataset_roots = [
        os.path.join(project_root, "student_resource", "dataset"),
        os.path.join(project_root, "dataset"),
    ]

    train_dir = None
    test_dir = None
    dataset_dir = None

    for d_root in possible_dataset_roots:
        cand_train = os.path.join(d_root, "train")
        if os.path.exists(os.path.join(cand_train, "train_source1.tsv")):
            dataset_dir = d_root
            train_dir = cand_train
            test_dir = os.path.join(d_root, "test")
            break

    # Fallback to searching recursively if still not found
    if train_dir is None:
        for root, _, files in os.walk(project_root):
            if "train_source1.tsv" in files:
                train_dir = root
                dataset_dir = os.path.dirname(train_dir)
                test_dir = os.path.join(dataset_dir, "test")
                break

    if train_dir is None:
        raise FileNotFoundError(
            f"Could not locate train_source1.tsv starting from {project_root}."
        )

    cleaned_dir = os.path.join(project_root, "data_cleaned")
    reports_dir = os.path.join(project_root, "reports")
    code_dir = os.path.join(project_root, "business_entity_resolution", "code", "src")

    return {
        "project_root": project_root,
        "base_dir": project_root,
        "dataset_dir": dataset_dir,
        "train_dir": train_dir,
        "test_dir": test_dir,
        "cleaned_dir": cleaned_dir,
        "cleaned_train_dir": os.path.join(cleaned_dir, "train"),
        "cleaned_test_dir": os.path.join(cleaned_dir, "test"),
        "reports_dir": reports_dir,
        "code_dir": code_dir,
    }


def load_tsv_safe(filepath: str) -> pd.DataFrame:
    """Safe TSV reader: preserves postal zeroes and empty strings."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    return pd.read_csv(
        filepath,
        sep="\t",
        dtype=str,
        keep_default_na=False,
        encoding="utf-8",
    )


def save_tsv_safe(df: pd.DataFrame, filepath: str) -> None:
    """Saves DataFrame as TSV with parent directory creation."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    df.to_csv(filepath, sep="\t", index=False, encoding="utf-8")