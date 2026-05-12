import json

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from sqlmodel import Session

from app.core.database import get_session

from app.models.schemas import ChatRequest

from app.services.chat_service import (
    create_chat_session,
    get_messages,
    save_message
)

from app.core.ollama_client import stream_chat


router = APIRouter()


@router.post("/")
def chat(
    request: ChatRequest,
    db: Session = Depends(get_session)
):

    session_id = request.session_id

    if not session_id:

        session = create_chat_session(db)

        session_id = session.id

    save_message(
        db,
        session_id,
        "user",
        request.message
    )

    previous_messages = get_messages(db, session_id)

    messages = []

    for msg in previous_messages:
        messages.append({
            "role": msg.role,
            "content": msg.content
        })

    response = stream_chat(messages)

    def generate():

        assistant_response = ""

        first_chunk = True

        for line in response.iter_lines():

            if line:

                data = json.loads(line)

                if "message" in data:

                    content = data["message"]["content"]

                    assistant_response += content

                    payload = {
                        "content": content
                    }

                    if first_chunk:
                        payload["session_id"] = session_id
                        first_chunk = False

                    yield json.dumps(payload) + "\n"

        save_message(
            db,
            session_id,
            "assistant",
            assistant_response
        )

    return StreamingResponse(
        generate(),
        media_type="application/x-ndjson"
    )