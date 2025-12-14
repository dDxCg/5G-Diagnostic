from schemas.artifacts import features, top_features
from typing import Dict, Any
import pandas as pd

async def preprocess(log: Dict[str, Any]):
    raw_df = pd.DataFrame([log])

    # Ensure ML features are present, missing -> NaN
    X_df = raw_df.reindex(columns=features)
    X_df = X_df.apply(pd.to_numeric, errors="coerce")

    # Extract top features
    top_features_data = {
        f: float(X_df.iloc[0][f]) if pd.notna(X_df.iloc[0][f]) else None
        for f in top_features
    }

    row = X_df.iloc[0]
    missing_fields = [f for f in top_features if f not in row or pd.isna(row[f])]

    return X_df, top_features_data, missing_fields

