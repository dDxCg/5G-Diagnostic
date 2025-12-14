from openai import OpenAI
import os
from dotenv import load_dotenv 

load_dotenv()

api_key = os.environ.get("OPENROUTER_API_KEY")
if not api_key:
    raise ValueError("OPENROUTER_API_KEY not set in environment")

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=api_key,
)

def response(messages):
    ans = client.chat.completions.create(
        model="google/gemma-3n-e4b-it:free",
        messages=messages,
        extra_body={"reasoning": {"enabled": True}}
    )
    return ans