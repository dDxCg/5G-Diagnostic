import json
import pandas as pd
from pathlib import Path

def json_to_df(file_path: str | Path) -> pd.DataFrame:
    with open(file_path, "r") as f:
        data = json.load(f)
    return pd.DataFrame([data])