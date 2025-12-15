import asyncio
from typing import Dict, Any
from .preprocess import preprocess
from .gateway import in_gateway, fallback_llm
from .ml_interface import ml_predict
from .context import fall_back_context, post_ML_context
from .prompt import build_post_ml_prompt, build_fallback_prompt
from .llm_interface import response
from app.websocket.socket_manager import event_bus
from app.utils.format import clean_llm_json
from app.schemas.artifacts import label_map

async def handle_ml(log_item: Dict[str, Any]):
    result = None  
    top_features_data = None
    missing_fields = None

    try:
        X_df, top_features_data, missing_fields = await preprocess(log_item['data'])
        ml_valid = in_gateway(missing_fields)

        if ml_valid:
            result = await ml_predict(X_df)
            label = label_map[str(result['label'])]["name"]
            await event_bus.emit(
                "job_done",
                {
                    "event": "ML predict completed",
                    "log_id": log_item['log_id'],
                    "prediction": label,
                    "result": result,
                }
            )
        else:
            await event_bus.emit(
                "job_failed",
                {
                    "event": "ML skipped",
                    "log_id": log_item['log_id'],
                    "result": None,
                }
            )
    except Exception as e:
        print("Error in ML:", e)
        await event_bus.emit(
            "job_failed",
            {
                "event": "ML error",
                "log_id": log_item.get('log_id'),
                "result": None,
                "error": str(e)
            }
        )

    return result, top_features_data, missing_fields

async def handle_llm(log_item, result, top_features_data, missing_fields):
    try:
        if result is not None:
            context = post_ML_context(result, top_features_data)
            prompt = build_post_ml_prompt(context)
        else:
            context = fall_back_context(log_item['data'], missing_fields)
            prompt = build_fallback_prompt(context)

        messages = [{"role": "user", "content": prompt}]
        ans = await response(messages)
        cleaned_ans = clean_llm_json(ans)

        await event_bus.emit(
            "job_done",
            {"event": "LLM reasoning completed", "log_id": log_item['log_id'], "result": cleaned_ans}
        )
    except Exception as e:
        print("Error in LLM:", e)
        await event_bus.emit(
            "job_failed",
            {
                "event": "LLM error",
                "log_id": log_item.get('log_id'),
                "result": None,
                "error": str(e)
            }
        )

async def process_log(log_item, queue):
    result = None  
    top_features_data = None
    missing_fields = None
    try:
        result, top_features_data, missing_fields = await handle_ml(log_item)
        asyncio.create_task(handle_llm(log_item, result, top_features_data, missing_fields))
    except Exception as e:
        print("Error processing log:", e)
    finally:
        queue.task_done()

async def log_consumer(queue: asyncio.Queue):
    while True:
        log_item = await queue.get()
        asyncio.create_task(process_log(log_item, queue))