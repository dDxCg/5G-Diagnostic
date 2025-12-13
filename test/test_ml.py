from ml.model import load_model
from ml.preprocess import preprocess_json
from ml.model import predict
from utils.convert import json_to_df   # hoặc copy hàm vào đây

MODEL_PATH = "models/lgbm_model.bin"
INPUT_JSON = "samples/sample_5.json"

def main():
    print("1. Preprocess")
    X_df, other_df = preprocess_json(INPUT_JSON)
    print(X_df)

    print("2. Load model")
    model = load_model(MODEL_PATH)

    print("3. Predict")
    result = predict(X_df, model)

    print("=== Prediction Result ===")
    print(result)

if __name__ == "__main__":
    main()
