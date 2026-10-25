
from sentence_transformers import SentenceTransformer
from sqlalchemy.orm import Session

from database.document_models import DocumentChunk


_embedding_model = None


def get_embedding_model():
    global _embedding_model

    if _embedding_model is None:
        _embedding_model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2"
        )

    return _embedding_model


def search_documents(
    query: str,
    db: Session,
    top_k: int = 3,
) -> list[dict]:
    if not query.strip():
        raise ValueError("Search query cannot be empty")

    if top_k < 1:
        raise ValueError("top_k must be at least 1")

    # Convert the user's question into a vector.
    model = get_embedding_model()
    query_embedding = model.encode(
        query,
        normalize_embeddings=True,
    ).tolist()

    # Find the closest document vectors using cosine distance.
    distance = DocumentChunk.embedding.cosine_distance(
        query_embedding
    ).label("distance")

    results = (
        db.query(DocumentChunk, distance)
        .order_by(distance)
        .limit(top_k)
        .all()
    )

    return [
        {
            "source_name": chunk.source_name,
            "content": chunk.content,
            "metadata": chunk.chunk_metadata or {},
            "similarity_score": round(1 - float(score), 4),
        }
        for chunk, score in results
    ]
