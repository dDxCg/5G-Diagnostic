from pydantic import BaseModel, Field
from typing import Dict, Any
from datetime import datetime

class UserLog(BaseModel):
    log_id: str | None = None
    timestamp: str | None = None
    data: Dict[str, Any]