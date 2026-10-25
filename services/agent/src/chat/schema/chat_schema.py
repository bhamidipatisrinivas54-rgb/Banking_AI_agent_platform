from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

class ChatRequest(BaseModel):
    message: str = Field(
        ...,
        min_length=1,
        description="User message",
    )


class ChatResponse(BaseModel):
    response: str

class ChatHistoryItem(BaseModel):
    id: int
    user_message: str
    agent_response: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)