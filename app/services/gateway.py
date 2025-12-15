from app.schemas.artifacts import top_features
from math import ceil
import pandas as pd

MISSING_RATIO_THRESHOLD = 0.25
CANDIDATE_THRESHOLD = 0.1
CONFIDENT_THRESHOLD = 0.8

def in_gateway(missing_fields):

    threshold = ceil(len(top_features) * MISSING_RATIO_THRESHOLD)
    
    can_run_ml = len(missing_fields) < threshold

    return can_run_ml

def fallback_llm(result):
    flag = (
        # low confidence
        result["confidence"] < CONFIDENT_THRESHOLD or  
        len([p for p in result["probs"] if p >= CANDIDATE_THRESHOLD]) > 1  
        # multiple plausible
    )
    return flag