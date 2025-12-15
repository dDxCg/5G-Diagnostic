from fastapi import APIRouter, Depends, HTTPException
import asyncio

from typing import Dict, Any
import uuid

from datetime import datetime
from schemas.types import UserLog
from app.utils.get_state import get_log_queue

router = APIRouter(prefix="/gateway")


@router.post("/log")
async def post_log(
    log: UserLog,
    queue: asyncio.Queue = Depends(get_log_queue),
):
    if not log.log_id:
        log.log_id = str(uuid.uuid4())
    if not log.timestamp:
        log.timestamp = datetime.utcnow().isoformat()

    try:
        queue.put_nowait(log.model_dump())
    except asyncio.QueueFull:
        raise HTTPException(429, "Queue full")

    return {
        "status": "queued",
        "log_id": log.log_id,
        "timestamp": log.timestamp,
    }

