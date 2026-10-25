
from pathlib import Path

from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
from sqlalchemy.orm import Session

from database.document_models import DocumentChunk


# The model produces 384-dimensional embeddings.
_embedding_model = None


def get_embedding_model():
    global _embedding_model

    if _embedding_model is None:
        _embedding_model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2"
        )

    return _embedding_model


def split_text(text: str, chunk_size: int = 1000, overlap: int = 150):
    """Split text into overlapping character chunks."""
    text = " ".join(text.split())

    if not text:
        return []

    chunks = []
    start = 0

    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end == len(text):
            break

        start = end - overlap

    return chunks


def ingest_pdf(pdf_path: str, db: Session) -> int:
    """Extract, chunk, embed, and store a PDF in PostgreSQL."""
    path = Path(pdf_path)

    if not path.is_file():
        raise FileNotFoundError(f"PDF not found: {path}")

    reader = PdfReader(str(path))
    chunks = []

    for page_number, page in enumerate(reader.pages, start=1):
        page_text = page.extract_text() or ""

        for chunk_index, content in enumerate(split_text(page_text)):
            chunks.append(
                {
                    "content": content,
                    "chunk_index": chunk_index,
                    "page_number": page_number,
                }
            )

    if not chunks:
        raise ValueError(
            "No text could be extracted. The PDF may be empty or scanned."
        )

    model = get_embedding_model()
    embeddings = model.encode(
        [chunk["content"] for chunk in chunks],
        normalize_embeddings=True,
    )

    try:
        for chunk, embedding in zip(chunks, embeddings):
            db.add(
                DocumentChunk(
                    source_name=path.name,
                    chunk_index=chunk["chunk_index"],
                    content=chunk["content"],
                    embedding=embedding.tolist(),
                    chunk_metadata={"page_number": chunk["page_number"]},
                )
            )

        db.commit()
    except Exception:
        db.rollback()
        raise

    return len(chunks)
