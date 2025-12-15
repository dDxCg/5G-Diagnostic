import asyncio
from typing import Dict, Set, Any
from fastapi import APIRouter, WebSocket

class EventBus:
    def __init__(self):
        self._handlers: Dict[str, list] = {}

    def on(self, event: str, handler):
        self._handlers.setdefault(event, []).append(handler)

    async def emit(self, event: str, data: Any):
        for handler in self._handlers.get(event, []):
            await handler(data)

class WebSocketManager:
    def __init__(self):
        self.connections: Set[WebSocket] = set()

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.connections.add(ws)

    def disconnect(self, ws: WebSocket):
        self.connections.discard(ws)

    async def broadcast(self, payload: dict):
        for ws in list(self.connections):
            try:
                await ws.send_json(payload)
            except Exception:
                self.disconnect(ws)


event_bus = EventBus()
ws_manager = WebSocketManager()


async def _broadcast_event(payload: dict):
    await ws_manager.broadcast(payload)


event_bus.on("job_done", _broadcast_event)
event_bus.on("job_failed", _broadcast_event)


router = APIRouter()
@router.websocket("/ws")
async def ws_endpoint(ws: WebSocket):
    await ws_manager.connect(ws)
    try:
        while True:
            await ws.receive_text()
    except Exception:
        ws_manager.disconnect(ws)