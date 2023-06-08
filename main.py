# uvicorn src.main:app --host 0.0.0.0 --port 8000  --reload
import logging
from fastapi import FastAPI
from src.routers import bot_router, task_router, channel_router, messages_router

app = FastAPI(title="botsAPI")
logger = logging.getLogger(__name__)


@app.on_event("startup")
async def startup():
    logging.basicConfig(level=logging.INFO)


app.include_router(bot_router)
app.include_router(task_router)
app.include_router(channel_router)
app.include_router(messages_router)