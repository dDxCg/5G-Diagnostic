import json
import pandas as pd
from pathlib import Path

def json_to_df(file_path: str | Path) -> pd.DataFrame:
    with open(file_path, "r") as f:
        data = json.load(f)
    return pd.DataFrame([data])

def load_json_file(path: str | Path) -> dict:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"JSON file not found at {path}")
    
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
