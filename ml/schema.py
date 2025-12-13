# ml/schema.py
import json
from pathlib import Path

ML_DIR = Path(__file__).resolve().parent
FEATURES_PATH = ML_DIR / "artifacts" / "features.json"

def load_features() -> list[str]:
    if not FEATURES_PATH.exists():
        raise FileNotFoundError(f"features.json not found at {FEATURES_PATH}")

    with open(FEATURES_PATH, "r") as f:
        return json.load(f)["features"]
