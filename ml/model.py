import lightgbm as lgb
import numpy as np

def load_model(model_path="models/lgbm_model.bin"):
    model = lgb.Booster(model_file=model_path)
    return model

def predict(df, model):
    """
    Predict label + confidence from a LightGBM multiclass model.

    Args:
        df (pd.DataFrame): preprocessed input, đúng feature order
        model (lgb.Booster): loaded LightGBM model

    Returns:
        dict:
            {
              "label": int,
              "confidence": float,
              "probs": list[float]
            }
    """
    # LightGBM returns:
    # - multiclass: shape (n_samples, num_class)
    # - binary: shape (n_samples,)
    y_pred_prob = model.predict(df)

    if y_pred_prob.ndim == 1:
        # binary fallback
        prob_pos = float(y_pred_prob[0])
        label = int(prob_pos >= 0.5)
        confidence = prob_pos if label == 1 else 1 - prob_pos
        probs = [1 - prob_pos, prob_pos]
    else:
        probs = y_pred_prob[0].tolist()
        label = int(np.argmax(probs))
        confidence = float(np.max(probs))

    return {
        "label": label,
        "confidence": confidence,
        "probs": probs
    }