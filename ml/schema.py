# ml/schema.py
import json
from pathlib import Path

ML_DIR = Path(__file__).resolve().parent
FEATURES = ML_DIR / "artifacts" / "features.json"
LABEL_MAP = ML_DIR / "artifacts" / "label_map.json"
FEATURES_EXPLAIN = ML_DIR / "artifacts" / "features_meaning.json"

def load_features() -> list[str]:
    if not FEATURES.exists():
        raise FileNotFoundError(f"features.json not found at {FEATURES}")

    with open(FEATURES, "r") as f:
        return json.load(f)["features"]

def load_label():
    if not LABEL_MAP.exists():
        raise FileNotFoundError(f"label_map.json not found at {LABEL_MAP}")
    
    with open(LABEL_MAP, "r") as f:
        return json.load(f)

def load_features_explain():
    if not FEATURES_EXPLAIN.exists():
        raise FileNotFoundError(f"label_map.json not found at {FEATURES_EXPLAIN}")
    
    with open(FEATURES_EXPLAIN, "r") as f:
        return json.load(f)
    

TOP_CUT = 14
top_features = load_features()[:TOP_CUT]