import pandas as pd
from utils.loader import json_to_df
from .schema import load_features
from pathlib import Path
from .schema import top_features

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

    top_features_data = {
        f: float(X_df.iloc[0][f]) if pd.notna(X_df.iloc[0][f]) else None
        for f in top_features
    }

    return X_df, top_features_data

