
from database.connection import SessionLocal
from database.models import ChatHistory

# Open a database session
db = SessionLocal()

try:
    # Create a sample chat record
    chat = ChatHistory(
        user_message="What is my account balance?",
        agent_response="Please authenticate to check your account balance.",
    )

    # Save it to PostgreSQL
    db.add(chat)
    db.commit()
    db.refresh(chat)

    print("Chat saved successfully!")
    print("Record ID:", chat.id)

    # Retrieve chat history
    chats = db.query(ChatHistory).order_by(ChatHistory.id.desc()).all()

    print("\nSaved chat records:")
    for item in chats:
        print("ID:", item.id)
        print("User:", item.user_message)
        print("Agent:", item.agent_response)
        print("Created:", item.created_at)
        print("-" * 40)

except Exception:
    db.rollback()
    raise

finally:
    db.close()
