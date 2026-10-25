
from database.connection import SessionLocal
from services.rag.src.ingestion.ingestion_service import ingest_pdf

PDF_PATH = "data/documents/customer-rights-policy.pdf"


def main():
    with SessionLocal() as db:
        count = ingest_pdf(PDF_PATH, db)

        print(f"\nSuccessfully ingested {count} chunks!")
        print(f"Source document: {PDF_PATH}")


if __name__ == "__main__":
    main()
