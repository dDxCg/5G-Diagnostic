import asyncio
from typing import Dict, Any
from .preprocess import preprocess
from .gateway import in_gateway, fallback_llm
from .ml_interface import ml_predict
from .context import fall_back_context, post_ML_context
from .prompt import build_post_ml_prompt, build_fallback_prompt
from .llm_interface import response
from websocket.socket_manager import event_bus
from utils.format import clean_llm_json

async def log_consumer(queue: asyncio.Queue):
    while True:
        log_item: Dict[str, Any] = await queue.get()
        data = log_item['data']
        log_id = log_item['log_id']
        try:
            X_df, top_features_data, missing_fields = await preprocess(data)
            ml_valid = in_gateway(missing_fields)

            if ml_valid:
                result = await ml_predict(X_df)
                
                await event_bus.emit(
                    "job_done",
                    {
                        "event": "ML predict completed",
                        "log_id": log_id,
                        "result": result,
                    }
                )

                context = post_ML_context(result, top_features_data)
                prompt = build_post_ml_prompt(context)
            else:
                await event_bus.emit(
                    "job_failed",
                    {
                        "event": "ML skipped, fallback to LLM",
                        "log_id": log_id,
                        "result": result,
                    }
                )
                context = fall_back_context(data, missing_fields)
                prompt = build_fallback_prompt(context)
            
            # need_llm = False
            # if not ml_valid:
            #     need_llm = True
            # if result is not None:
            #     is_fallback = fallback_llm(result)
            # if is_fallback:
            #     need_llm = True
            
            # if need_llm:
            #     messages = [{"role": "user", "content": prompt}]
            #     ans = await response(messages)

            messages = [{"role": "user", "content": prompt}]
            ans = await response(messages)
            cleaned_ans = clean_llm_json(ans)
            
            await event_bus.emit(
                    "job_done",
                    {
                        "event": "LLM reasoning completed",
                        "log_id": log_id,
                        "result": cleaned_ans,
                    }
                )

        except Exception as e:
            print("Error processing log:", e)
        finally:
            queue.task_done()