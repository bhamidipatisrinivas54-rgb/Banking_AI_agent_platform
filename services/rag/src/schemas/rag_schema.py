
from pydantic import BaseModel, Field


class RAGSearchRequest(BaseModel):
    query: str = Field(min_length=1, max_length=5000)
    top_k: int = Field(default=3, ge=1, le=10)


class RetrievedChunk(BaseModel):
    source_name: str
    content: str
    metadata: dict
    similarity_score: float


class RAGSearchResponse(BaseModel):
    query: str
    results: list[RetrievedChunk]

class RAGAnswerResponse(BaseModel):
    answer: str
    sources: list[dict]
