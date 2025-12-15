from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from app.services.comsumer import log_consumer, ml_consumer
from app.services.llm_worker import run_llm_worker_in_thread
from app.routes.gateway import router as gateway_router
from app.websocket.socket_manager import router as websocket_router
from app.websocket.ws_worker import ws_worker
import asyncio

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

    asyncio.create_task(log_consumer(app.state.log_queue))
    asyncio.create_task(ws_worker())
    asyncio.create_task(ml_consumer())
    run_llm_worker_in_thread()
    

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
