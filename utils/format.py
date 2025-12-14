import re
import json

def clean_llm_json(raw):
    raw_dict = raw.to_dict()
    msg = raw_dict["choices"][0]["message"]
    if isinstance(msg, dict) and "content" in msg:
        content = msg["content"]
    else:
        content = msg

    # Remove ```json ``` hoặc ``` nếu có
    content = re.sub(r"```json|```", "", content).strip()

    # Convert escaped \n và quotes 
    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        content_fixed = content.replace("'", '"')
        data = json.loads(content_fixed)

    return data