from fastapi import APIRouter

from .chat_service import ChatService
from .schema.chat_schema import ChatRequest, ChatResponse, ChatHistoryItem
from database.models import ChatHistory
from database.connection import SessionLocal

from database.dependencies import get_db
from fastapi import Query,Depends
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/api/v1/chat",
    tags=["Chat"],
)

chat_service = ChatService()


@router.post(
    "",
    response_model=ChatResponse,
)
async def chat(request: ChatRequest) -> ChatResponse:
    return await chat_service.chat(request)



@router.get("/history", response_model=list[ChatHistoryItem])
async def get_chat_history(
    limit: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    records = (
        db.query(ChatHistory)
        .order_by(ChatHistory.id.desc())
        .limit(limit)
        .all()
    )
    return records
