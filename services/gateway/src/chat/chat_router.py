from fastapi import APIRouter
from .chat_service import ChatService
from .schema.chat_schema import ChatRequest, ChatResponse

router = APIRouter(
    prefix="/api/v1/chat",
    tags=["Chat"],
)
chat_service = ChatService()

@router.post("/chat", response_model=ChatResponse)
async def send_chat_message(request: ChatRequest):
    return await chat_service.chat(request)