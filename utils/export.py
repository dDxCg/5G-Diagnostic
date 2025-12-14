import json
from datetime import datetime
from pathlib import Path
import json
import re

def clean_llm_json(raw):
    """
    Convert LLM response with ```json ... ``` or string escapes into actual JSON dict.
    """
    if isinstance(raw, dict) and "content" in raw:
        content = raw["content"]
    else:
        content = raw

    # Remove ```json ``` hoặc ``` nếu có
    content = re.sub(r"```json|```", "", content).strip()

    # Convert escaped \n và quotes nếu cần
    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        # Nếu vẫn lỗi, thử fix quotes kiểu single -> double
        content_fixed = content.replace("'", '"')
        data = json.loads(content_fixed)

    return data

def export_llm_res_to_json(ans):
    ans_dict = ans.to_dict()
    assistant_msg = ans_dict["choices"][0]["message"]

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = f"temp/res_{timestamp}.json"

    clean_data = clean_llm_json(assistant_msg)
    
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(clean_data, f, indent=2)
    
    return file_path