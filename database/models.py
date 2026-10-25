from datetime import datetime

from sqlalchemy import Column, Integer, Text, DateTime, String, func
from database.connection import Base


class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)
    user_message = Column(Text, nullable=False)
    agent_response = Column(Text, nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    status = Column(
        String(20),
        nullable=False,
        default="completed",
        server_default="completed",
    )