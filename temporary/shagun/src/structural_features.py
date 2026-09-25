import os
import re
import sys
import pandas as pd

# Ensure local imports work reliably
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from text_normalizer import (
    clean_base_text,
    strip_legal_suffixes,
    expand_address_abbreviations,
)


def extract_numeric_tokens(address: str) -> str:
    """
    Extracts numeric sequences of length >= 3 (PINs, ZIPs, building/street IDs)
    into a deterministic, sorted, pipe-delimited string.
    """
    if not address:
        return ""
    nums = re.findall(r"\b\d{3,}\b", address)
    return "|".join(sorted(set(nums)))


def transform_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms input DataFrame by applying Unicode NFKD normalization,
    base cleaning, legal suffix removal, address abbreviation expansion,
    and generating numeric_tokens_str and composite_text.
    """
    # 1. Clean business name
    clean_names = [
        strip_legal_suffixes(clean_base_text(val))
        for val in df["business_name"].fillna("")
    ]
    df["clean_name"] = clean_names

    # 2. Clean address
    clean_addrs = [
        expand_address_abbreviations(clean_base_text(val))
        for val in df["business_address"].fillna("")
    ]
    df["clean_addr"] = clean_addrs

    # 3. Structural anchors (numeric tokens >= 3 digits)
    numeric_tokens = [extract_numeric_tokens(addr) for addr in clean_addrs]
    df["numeric_tokens_str"] = numeric_tokens
    df["numeric_tokens"] = numeric_tokens

    # 4. Composite representation
    df["composite_text"] = (df["clean_name"] + " " + df["clean_addr"]).str.strip()

    return df