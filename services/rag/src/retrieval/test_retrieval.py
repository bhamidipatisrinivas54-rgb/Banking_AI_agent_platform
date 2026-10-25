
from database.connection import SessionLocal
from services.rag.src.retrieval.retrieval_service import (
    search_documents,
)


def main():
    query = "What should I do if my banking complaint is not resolved?"

    with SessionLocal() as db:
        results = search_documents(
            query=query,
            db=db,
            top_k=3,
        )

    print(f"\nQuestion: {query}\n")

    for index, result in enumerate(results, start=1):
        print(f"--- Result {index} ---")
        print(f"Source: {result['source_name']}")
        print(f"Page: {result['metadata'].get('page_number')}")
        print(f"Similarity: {result['similarity_score']}")
        print(f"Content: {result['content']}\n")


if __name__ == "__main__":
    main()
