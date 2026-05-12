from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime
import uuid


class ChatSession(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)

    title: str = "New Chat"

    created_at: datetime = Field(default_factory=datetime.utcnow)


class Message(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    session_id: str = Field(index=True)

    role: str

    content: str

    created_at: datetime = Field(default_factory=datetime.utcnow)
