from sqlmodel import Session, select

from app.models.db_models import (
    ChatSession,
    Message
)

from app.core.ollama_client import stream_chat


def create_chat_session(db: Session):

    session = ChatSession()

    db.add(session)
    db.commit()
    db.refresh(session)

    return session


def get_messages(db: Session, session_id: str):

    statement = select(Message).where(
        Message.session_id == session_id
    )

    messages = db.exec(statement).all()

    return messages


def save_message(
    db: Session,
    session_id: str,
    role: str,
    content: str
):

    message = Message(
        session_id=session_id,
        role=role,
        content=content
    )

    db.add(message)
    db.commit()

    return message

def get_all_sessions(db):
    return db.exec(
        select(ChatSession)
    ).all()