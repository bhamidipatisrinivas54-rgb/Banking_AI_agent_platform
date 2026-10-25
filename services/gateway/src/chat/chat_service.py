from .agent_client import AgentClient
from .schema.chat_schema import ChatRequest, ChatResponse


class ChatService:

    def __init__(self):
        self.agent_client = AgentClient()

    async def chat(self, request: ChatRequest) -> ChatResponse:
        return await self.agent_client.chat(request)