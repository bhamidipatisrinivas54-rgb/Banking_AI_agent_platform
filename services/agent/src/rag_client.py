
import os

import httpx
from dotenv import load_dotenv

load_dotenv()

RAG_SERVICE_URL = os.getenv(
    "RAG_SERVICE_URL",
    "http://127.0.0.1:8002",
)


async def search_rag(query: str, top_k: int = 3) -> dict:
    url = f"{RAG_SERVICE_URL}/api/v1/rag/answer"

    try:
        timeout = httpx.Timeout(
            timeout=180.0,
            connect=10.0,
)

        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(
                url,
                json={
                    "query": query,
                    "top_k": top_k,
                },
            )
            response.raise_for_status()
            return response.json()

    except httpx.TimeoutException as exc:
        raise RuntimeError("RAG answer generation timed out") from exc

    except httpx.HTTPStatusError as exc:
        raise RuntimeError(
            f"RAG service returned HTTP {exc.response.status_code}"
        ) from exc

    except httpx.RequestError as exc:
        raise RuntimeError(
            "Could not connect to RAG service"
        ) from exc
