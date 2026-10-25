from fastapi import FastAPI

from .chat.chat_router import router as chat_router


app = FastAPI(
    title="Banking AI Agent Platform - Agent",
    version="0.1.0",
)

app.include_router(chat_router)