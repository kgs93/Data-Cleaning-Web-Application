import pandas as pd
import numpy as np
from typing import Dict

def clean_dataframe(df: pd.DataFrame):
    """
    Mirrors your script's behavior:
    - Save duplicates (beyond first occurrence)
    - Drop duplicates
    - Fill numeric NaNs with mean
    - Drop rows that have missing values in non-numeric columns
    Returns stats + cleaned and duplicate DataFrames.
    """
    original_rows, original_cols = df.shape

    # Identify duplicates
    dup_mask = df.duplicated(keep="first")
    duplicate_rows = df[dup_mask].copy()

    # Drop duplicates
    df = df.drop_duplicates(keep="first").copy()

    # Missing values overview (before cleaning)
    total_missing = int(df.isna().sum().sum())
    missing_by_col: Dict[str, int] = {str(k): int(v) for k, v in df.isna().sum().items()}

    # Numeric vs non-numeric
    numeric_cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
    non_numeric_cols = [c for c in df.columns if c not in numeric_cols]

    # Fill numeric NaNs with mean
    for c in numeric_cols:
        if df[c].isna().any():
            df[c] = pd.to_numeric(df[c], errors="coerce")
            df[c] = df[c].fillna(df[c].mean())

    # Drop rows where non-numeric columns are missing
    for c in non_numeric_cols:
        if df[c].isna().any():
            df = df.dropna(subset=[c])

    cleaned_rows, _ = df.shape

    return {
        "originalRowCount": int(original_rows),
        "originalColumnCount": int(original_cols),
        "cleanedRowCount": int(cleaned_rows),
        "duplicateCount": int(len(duplicate_rows)),
        "missingValueTotal": int(total_missing),
        "missingByColumn": missing_by_col,
        "numericColumns": numeric_cols,
        "cleaned": df,
        "duplicates": duplicate_rows,
    }
