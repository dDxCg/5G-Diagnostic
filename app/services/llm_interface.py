from openai import OpenAI
import os
from dotenv import load_dotenv 
import asyncio
from concurrent.futures import ProcessPoolExecutor

llm_thread = ProcessPoolExecutor(max_workers=15)
LLM_SEMAPHORE = asyncio.Semaphore(10)

load_dotenv()

api_key = os.environ.get("OPENROUTER_API_KEY")
if not api_key:
    raise ValueError("OPENROUTER_API_KEY not set in environment")

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=api_key,
)

def _sync_llm_call(messages):
    return client.chat.completions.create(
        model="google/gemma-3n-e4b-it:free",
        messages=messages,
        extra_body={"reasoning": {"enabled": True}},
    )

async def response(messages):
    async with LLM_SEMAPHORE:
        loop = asyncio.get_running_loop()
        try:
            return await loop.run_in_executor(llm_thread, _sync_llm_call, messages)
        except Exception as e:
            print(f"[LLM] Error: {e}")
            raise