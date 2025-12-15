import asyncio
import threading
from app.services.comsumer import LLM_QUEUE, handle_llm_task

def start_llm_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    async def worker():
        while True:
            log_item, result, top_features, missing_fields = await LLM_QUEUE.get()
            try:
                await handle_llm_task(log_item, result, top_features, missing_fields)
            finally:
                LLM_QUEUE.task_done()

    loop.create_task(worker())
    loop.run_forever()

def run_llm_worker_in_thread():
    threading.Thread(target=start_llm_loop, daemon=True).start()
