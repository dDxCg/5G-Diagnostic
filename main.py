from ml.model import load_model
from ml.preprocess import preprocess_json
from ml.model import predict
from ml.context import fall_back_context, post_ML_context
from ml.gateway import gateway_single
from utils.loader import load_json_file
from llm.prompt import build_fallback_prompt, build_post_ml_prompt
from llm.model import response
from utils.export import export_llm_res_to_json

MODEL_PATH = "models/lgbm_model.bin"
INPUT_JSON = "samples/sample_missing.json"

def main():
    print("<--- Preprocess --->")
    X_df, top_features_data = preprocess_json(INPUT_JSON)
    
    check, missing_fields = gateway_single(X_df)
    if check:
        print("<--- Load model --->")
        model = load_model(MODEL_PATH)

        print("<--- Predict --->")
        result = predict(X_df, model)

        context = post_ML_context(result, top_features_data)
        prompt = build_post_ml_prompt(context)
    else:
        print("<--- ML Skipped --->")
        context = fall_back_context(load_json_file(INPUT_JSON), missing_fields)
        prompt = build_fallback_prompt(context)

    print("<--- LLM reasoning --->")
    messages = [{"role": "user", "content": prompt}]
    ans = response(messages)
    export_llm_res_to_json(ans)

if __name__ == "__main__":
    main()
