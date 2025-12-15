from app.schemas.artifacts import label_map, feature_meaning, features

CANDIDATE_THRESHOLD = 0.05

def format_probs(probs):
    candidates = []

    for i, p in enumerate(probs):
        if p >= CANDIDATE_THRESHOLD:
            candidates.append({
                "label": label_map[str(i)]["name"],
                "prob": p,
                "description": label_map[str(i)]["description"]
            })
    # sort descending by prob
    candidates.sort(key=lambda x: x["prob"], reverse=True)
    return candidates


def fall_back_context(raw, missing_fields):
    if hasattr(raw, "to_dict"):
        raw_features = raw.to_dict()
    else:
        raw_features = dict(raw)

    context = {
        "issue": "ML skipped",
        "missing_features": missing_fields,
        "trust_level": "low",
        "reason": f"Skipped ML due to {len(missing_fields)} missing critical features",
        "raw_features": raw_features,
        "feature_explain": feature_meaning
    }

    return context


def post_ML_context(result, features):
    label = result['label']
    confident = result['confidence']
    probs = result['probs']

    prediction = {
        "label": label_map[str(label)]["name"],
        "confidence": confident,
        "description": label_map[str(label)]["description"]
    }

    context = {
        "prediction": prediction,
        "candidates": format_probs(probs),
        "top_features": features,
        "feature_explain": feature_meaning
    }

    return context