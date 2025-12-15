import asyncio
from typing import Dict, Any
from .preprocess import preprocess
from .gateway import in_gateway, fallback_llm
from .ml_interface import ml_predict, ml_thread 
from .context import fall_back_context, post_ML_context
from .prompt import build_post_ml_prompt, build_fallback_prompt
from .llm_interface import response, LLM_SEMAPHORE
from app.utils.format import clean_llm_json
from app.schemas.artifacts import label_map
from app.websocket.ws_worker import emit_event

ML_QUEUE = asyncio.Queue()
LLM_QUEUE = asyncio.Queue()

# ---------------- ML ----------------
async def handle_ml_task(log_item: Dict[str, Any]):
    loop = asyncio.get_running_loop()
    result = None  
    top_features_data = {}
    missing_fields = []

    try:
        # preprocess + in_gateway trong thread pool
        X_df, top_features_data, missing_fields = await loop.run_in_executor(
            ml_thread, preprocess, log_item['data']
        )
        ml_valid = await loop.run_in_executor(
            ml_thread, in_gateway, missing_fields
        )

        if ml_valid:
            result = await ml_predict(X_df)
            label = label_map[str(result['label'])]["name"]
            print(f"[ML] Log {log_item['log_id']}: Prediction={label}")

            # Emit ML event ngay
            asyncio.create_task(emit_event("ml_finish", {
                "event": "ML prediction completed",
                "log_id": log_item['log_id'],
                "result": result,
            }))
        else:
            print(f"[ML] Log {log_item['log_id']}: Skipped (missing {len(missing_fields)} features)")
            asyncio.create_task(emit_event("ml_finish", {
                "event": "ML skipped",
                "log_id": log_item['log_id'],
                "missing_fields": missing_fields,
                "result": None,
            }))
    except Exception as e:
        print(f"[ML] Log {log_item.get('log_id')}: Error: {e}")
        asyncio.create_task(emit_event("ml_finish", {
            "event": "ML error",
            "log_id": log_item.get('log_id'),
            "result": None,
            "error": str(e),
        }))

    # Push tiếp vào LLM queue để xử lý LLM nhưng không block ML
    await LLM_QUEUE.put((log_item, result, top_features_data, missing_fields))


async def ml_consumer():
    while True:
        log_item = await ML_QUEUE.get()
        try:
            asyncio.create_task(handle_ml_task(log_item))
        finally:
            ML_QUEUE.task_done()

# ---------------- LLM ----------------
async def handle_llm_task(log_item: Dict[str, Any], result: Any, top_features_data: Dict, missing_fields: list):
    async with LLM_SEMAPHORE:
        try:
            if result is not None:
                context = post_ML_context(result, top_features_data)
                prompt = build_post_ml_prompt(context)
            else:
                context = fall_back_context(log_item['data'], missing_fields)
                prompt = build_fallback_prompt(context)

            messages = [{"role": "user", "content": prompt}]
            print(f"[LLM] Log {log_item['log_id']}: Calling LLM...")
            ans = await response(messages)
            cleaned_ans = clean_llm_json(ans)

            print(f"[LLM] Log {log_item['log_id']}: Completed")
            asyncio.create_task(emit_event("llm_finish", {
                "event": "LLM completed",
                "log_id": log_item['log_id'],
                "result": cleaned_ans,
            }))
        except Exception as e:
            print(f"[LLM] Log {log_item.get('log_id')}: Error: {e}")
            asyncio.create_task(emit_event("llm_finish", {
                "event": "LLM error",
                "log_id": log_item.get('log_id'),
                "error": str(e),
            }))

# ---------------- Log Consumer ----------------
async def log_consumer(queue: asyncio.Queue) -> None:
    print("[Log Consumer] Started")
    while True:
        log_item = await queue.get()
        print(f"[Log Consumer] Got log {log_item.get('log_id')} from incoming queue")
        await ML_QUEUE.put(log_item)
        queue.task_done()
