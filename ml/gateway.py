from .schema import load_features
from math import ceil
import pandas as pd

TOP_CUT = 14
MISSING_RATIO_THRESHOLD = 0.25

def gateway_single(X_df):
    row = X_df.iloc[0]
    top_features = load_features()[:TOP_CUT]
    threshold = ceil(len(top_features) * MISSING_RATIO_THRESHOLD)
    
    missing_fields = [f for f in top_features if f not in row or pd.isna(row[f])]
    
    can_run_ml = len(missing_fields) < threshold

    return can_run_ml, missing_fields

def gateway_batch(X_df):
    pass