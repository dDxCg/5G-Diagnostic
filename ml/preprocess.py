import pandas as pd
from utils.convert import json_to_df
from .schema import load_features
from pathlib import Path

def preprocess_json(
    file_path: str | Path,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Input JSON -> (X_df, other_df)

    X_df     : only ML features (missing allowed, NaN kept)
    other_df : remaining raw fields
    """
    features = load_features()
    print(features)

    raw_df = json_to_df(file_path)

    # ML input (force feature list, missing -> NaN)
    X_df = raw_df.reindex(columns=features)
    X_df = X_df.apply(pd.to_numeric, errors="coerce")
    
    # Everything else
    other_cols = [c for c in raw_df.columns if c not in features]
    other_df = raw_df[other_cols].copy()

    return X_df, other_df

