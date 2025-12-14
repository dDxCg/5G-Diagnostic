from .schema import load_label

def convert_pred(pred):
    label_map = load_label()
    label = label_map[str(pred)]
    
    label_context = f"{label['name']} - {label['description']}"
    return label_context


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
        "raw_features": raw_features
    }

    return context