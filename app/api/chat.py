import json

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlmodel import Session

from app.core.database import get_session
from app.models.schemas import ChatRequest
from app.services.chat_service import (
    create_chat_session,
    get_messages,
    save_message,
    get_all_sessions
)
from app.core.ollama_client import stream_chat

router = APIRouter()

# ----------------------------
# Create / stream chat
# ----------------------------
@router.post("/")
def chat(
    request: ChatRequest,
    db: Session = Depends(get_session)
):

    session_id = request.session_id

    # create session if needed
    if not session_id:
        session = create_chat_session(db)
        session_id = session.id

    # save user message
    save_message(
        db,
        session_id,
        "user",
        request.message
    )

    # build history
    previous_messages = get_messages(db, session_id)

    messages = [
        {"role": m.role, "content": m.content}
        for m in previous_messages
    ]

    response = stream_chat(messages)

    def generate():
        assistant_response = ""
        first_chunk = True

        for line in response.iter_lines():

            if not line:
                continue

            try:
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

            except Exception as e:
                print("stream error:", e)

        # save assistant response
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


# ----------------------------
# Sessions list (sidebar)
# ----------------------------
@router.get("/sessions")
def sessions(db: Session = Depends(get_session)):
    return get_all_sessions(db)


# ----------------------------
# Messages of a session
# ----------------------------
@router.get("/messages/{session_id}")
def messages(session_id: str, db: Session = Depends(get_session)):
    return get_messages(db, session_id)