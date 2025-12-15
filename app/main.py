from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from app.services.comsumer import log_consumer
from app.routes.gateway import router as gateway_router
from app.websocket.socket_manager import router as websocket_router
import asyncio
from concurrent.futures import ThreadPoolExecutor

app = FastAPI(title="5G Diagnostic", version="1.0.0")
api_router = APIRouter()
app.include_router(gateway_router)
app.include_router(websocket_router)

# Allow CORS from any origin (dev)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    app.state.log_queue = asyncio.Queue(maxsize=1000)
    app.state.executor = ThreadPoolExecutor(max_workers=20)

    asyncio.create_task(log_consumer(app.state.log_queue))

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
