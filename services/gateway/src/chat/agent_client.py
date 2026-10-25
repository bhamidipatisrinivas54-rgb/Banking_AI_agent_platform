
import httpx
from fastapi import HTTPException

from ..config import settings
from .schema.chat_schema import ChatRequest, ChatResponse


class AgentClient:

    async def chat(self, request: ChatRequest) -> ChatResponse:
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(
                    f"{settings.agent_service_url}/api/v1/chat",
                    json=request.model_dump(),
                )
                response.raise_for_status()

        except httpx.ConnectError as exc:
            raise HTTPException(
                status_code=503,
                detail="Agent service is unavailable",
            ) from exc

        except httpx.TimeoutException as exc:
            raise HTTPException(
                status_code=504,
                detail="Agent service timed out",
            ) from exc

        except httpx.HTTPStatusError as exc:
            raise HTTPException(
                status_code=502,
                detail="Agent service returned an error",
            ) from exc

        return ChatResponse(**response.json())
