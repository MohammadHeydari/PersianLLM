import json

from fastapi import APIRouter, WebSocket
from sqlmodel import Session

from app.core.database import get_session
from app.services.chat_service import (
    create_chat_session,
    get_messages,
    save_message
)
from app.core.ollama_client import stream_chat

router = APIRouter()

@router.websocket("/ws/chat")
async def chat_ws(websocket: WebSocket):
    await websocket.accept()

    db: Session = next(get_session())
    # db_gen = get_session()
    # db = next(db_gen)

    while True:

        data = await websocket.receive_text()
        payload = json.loads(data)

        message = payload.get("message")
        session_id = payload.get("session_id")

        if not message:
            continue

        # create session if needed
        if not session_id:
            session = create_chat_session(db)
            session_id = session.id

        save_message(db, session_id, "user", message)

        history = get_messages(db, session_id)

        messages = [
            {"role": m.role, "content": m.content}
            for m in history
        ]

        response = stream_chat(messages)

        assistant_text = ""

        for line in response.iter_lines():

            if not line:
                continue

            try:
                data = json.loads(line)

                if "message" in data:

                    content = data["message"]["content"]
                    assistant_text += content

                    await websocket.send_text(json.dumps({
                        "type": "token",
                        "content": content,
                        "session_id": session_id
                    }))

            except Exception as e:
                print("WS error:", e)

        save_message(db, session_id, "assistant", assistant_text)

        await websocket.send_text(json.dumps({
            "type": "done"
        }))

###
# db_gen.close()