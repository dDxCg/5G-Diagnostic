import asyncio
from fastapi import Request, HTTPException

def get_log_queue(request: Request) -> asyncio.Queue:
    queue = getattr(request.app.state, "log_queue", None)
    if queue is None:
        raise HTTPException(503, "Queue not ready")
    return queue

def get_executor(request: Request):
    executor = getattr(request.app.state, "executor", None)
    if executor is None:
        raise HTTPException(503, "Executor not ready")
    return executor