def build_fallback_prompt(context: dict) -> str:
    prompt = f"""
You are a 5G network audit reasoning assistant. You are performing reasoning for a 5G network flow audit. Use the following context:

Case context:
- Issue: {context['issue']}
- Trust level: {context['trust_level']}
- Reason: {context['reason']}

Raw network features (numeric/categorical):
{context['raw_features']}

Feature explanations:
{context['feature_explain']}

Instructions:
1. Focus primarily on reasoning from the raw_features.
2. Consider missing ML features only as contextual information, but do not let them dominate your judgment.
3. Predict whether the flow is normal or indicates a type of attack.
4. If uncertain, list plausible candidate labels with approximate confidence.
5. Provide a detailed explanation referencing the raw feature values, highlighting which features suggest your prediction.

Output JSON format:
{{
    "prediction": "<predicted label or 'unknown'>",
    "confidence": <0.0-1.0>,
    "candidate_labels": [
        {{"label": "<label_name>", "reasoning": "<why plausible>"}}
    ],
    "reasoning": "<detailed explanation using raw_features>"
}}
"""
    return prompt.strip()


def build_post_ml_prompt(post_ml_context: dict) -> str:
    prediction = post_ml_context.get("prediction")
    candidates = post_ml_context.get("candidates", [])
    top_features = post_ml_context.get("top_features", {})
    feature_explain = post_ml_context.get("feature_explain", {})

    prompt = f"""
You are a 5G network audit reasoning assistant. You are performing reasoning for a 5G network flow audit. Use the following context:

Predicted label: {prediction}
Candidates: {candidates}

Top features of this flow:
{top_features}

Feature explanations: {feature_explain}

Instructions:
1. Focus on reasoning based on the raw top_features and their meanings.
2. If the ML prediction confidence is low or no single label dominates, treat this as audit-worthy.
3. Explain why this flow may be normal or some type of attack, referencing feature values.
4. If uncertain, list plausible labels with approximate confidence.
5. When audit-worthy, prioritize reasoning based on the top_features and their meanings rather than relying on ML predictions.

Provide a detailed reasoning output.
Output JSON format:
{{
    "prediction": "<predicted label or 'unknown'>",
    "confidence": <0.0-1.0>,
    "candidate_labels": [
        {{"label": "<label_name>", "reasoning": "<why plausible>"}}
    ],
    "reasoning": "<detailed explanation using raw_features>"
}}
"""
    return prompt.strip()
