from fastapi import FastAPI

from services.gateway.src.chat.chat_router import router as chat_router
from .health.health_router import router as health_router

app = FastAPI(
    title="Banking AI agent platform- Gateway",
    version="1.0.0",
)
app.include_router(health_router)
app.include_router(chat_router)