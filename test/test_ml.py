from ml.model import load_model
from ml.preprocess import preprocess_json
from ml.model import predict
from ml.context import fall_back_context, post_ML_context
from ml.gateway import gateway_single
from utils.loader import load_json_file

MODEL_PATH = "models/lgbm_model.bin"
INPUT_JSON = "samples/sample_testing_1.json"

def main():
    print("1. Preprocess")
    X_df, top_features_data = preprocess_json(INPUT_JSON)
    print(X_df)
    
    check, missing_fields = gateway_single(X_df)
    if check:
        print("2. Load model")
        model = load_model(MODEL_PATH)

        print("3. Predict")
        result = predict(X_df, model)

        print("=== Prediction Result ===")
        print (post_ML_context(result, top_features_data))
    else:
        print(fall_back_context(load_json_file(INPUT_JSON), missing_fields))

if __name__ == "__main__":
    main()
