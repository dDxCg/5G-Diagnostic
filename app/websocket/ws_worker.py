import asyncio
from app.websocket.socket_manager import ws_manager

WS_QUEUE = asyncio.Queue()

async def ws_worker():
    while True:
        event, payload = await WS_QUEUE.get()
        for ws in list(ws_manager.connections):
            try:
                asyncio.create_task(ws.send_json({"event": event, "payload": payload}))
            except:
                ws_manager.disconnect(ws)
        WS_QUEUE.task_done()

# Emit từ ML/LLM
async def emit_event(event_name, payload):
    await WS_QUEUE.put((event_name, payload))

