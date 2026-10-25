
from sqlalchemy.orm import Session

from services.rag.src.generation.llm_service import generate_answer
from services.rag.src.retrieval.retrieval_service import search_documents


async def answer_question(
    question: str,
    db: Session,
    top_k: int = 3,
) -> dict:
    # 1. Retrieve relevant passages from PostgreSQL.
    results = search_documents(
        query=question,
        db=db,
        top_k=top_k,
    )

    if not results:
        return {
            "answer": (
                "I couldn't find relevant information in the "
                "available banking policy documents."
            ),
            "sources": [],
        }

    # 2. Build context from the actual retrieved passages.
    context_parts = []

    for item in results:
        page = item.get("metadata", {}).get("page_number", "Unknown")
        context_parts.append(
            f"Source: {item['source_name']}, Page: {page}\n"
            f"{item['content']}"
        )

    context = "\n\n---\n\n".join(context_parts)

    # 3. Generate an answer grounded in that context.
    answer = await generate_answer(
        question=question,
        context=context,
    )

    # 4. Return the answer and its source references.
    sources = [
        {
            "source_name": item["source_name"],
            "page_number": item.get("metadata", {}).get("page_number"),
            "similarity_score": item["similarity_score"],
        }
        for item in results
    ]

    return {
        "answer": answer,
        "sources": sources,
    }
