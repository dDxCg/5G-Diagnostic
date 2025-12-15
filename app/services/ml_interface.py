import lightgbm as lgb
import numpy as np
import asyncio
from concurrent.futures import ThreadPoolExecutor

ml_thread = ThreadPoolExecutor(max_workers=10)
model_path = "models/lgbm_model.bin"
model = lgb.Booster(model_file=model_path)

def predict(df, model):
    y_pred_prob = model.predict(df)

    if y_pred_prob.ndim == 1:
        prob_pos = float(y_pred_prob[0])
        label = int(prob_pos >= 0.5)
        confidence = prob_pos if label == 1 else 1 - prob_pos
        probs = [1 - prob_pos, prob_pos]
    else:
        probs = y_pred_prob[0].tolist()
        label = int(np.argmax(probs))
        confidence = float(np.max(probs))

    return {"label": label, "confidence": confidence, "probs": probs}

async def ml_predict(X_df):
    loop = asyncio.get_running_loop()
    try:
        return await loop.run_in_executor(ml_thread, predict, X_df, model)
    except Exception as e:
        print(f"[ML] Prediction error: {e}")
        raise e
