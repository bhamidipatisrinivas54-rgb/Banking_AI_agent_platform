
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from database.connection import SessionLocal
from services.rag.src.rag_service import answer_question
from services.rag.src.retrieval.retrieval_service import search_documents
from services.rag.src.schemas.rag_schema import (
    RAGSearchRequest,
    RAGSearchResponse,
)


class RAGAnswerResponse(BaseModel):
    answer: str
    sources: list[dict]


app = FastAPI(
    title="Banking AI Platform - RAG Service",
    description="Semantic search and answer generation over banking policies",
    version="1.0.0",
)


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "rag"}


@app.post("/api/v1/rag/search", response_model=RAGSearchResponse)
def search(request: RAGSearchRequest):
    try:
        with SessionLocal() as db:
            results = search_documents(
                query=request.query,
                db=db,
                top_k=request.top_k,
            )

        return RAGSearchResponse(
            query=request.query,
            results=results,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="RAG search failed",
        ) from exc


@app.post("/api/v1/rag/answer", response_model=RAGAnswerResponse)
async def answer(request: RAGSearchRequest):
    try:
        with SessionLocal() as db:
            result = await answer_question(
                question=request.query,
                db=db,
                top_k=request.top_k,
            )

        return RAGAnswerResponse(**result)

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail="RAG answer generation failed",
        ) from exc
