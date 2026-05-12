from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import requests
import json
import uuid

app = FastAPI()

# Static files
app.mount("../app/web/static", StaticFiles(directory="static"), name="static")

# Templates folder
templates = Jinja2Templates(directory="templates")

# In‑memory session storage
chat_sessions = {}

OLLAMA_URL = "http://localhost:11434/api/chat"


# -----------------------------
# Home Page
# -----------------------------
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )


# -----------------------------
# Chat Endpoint (Streaming)
# -----------------------------
@app.post("/chat")
async def chat(request: Request):

    data = await request.json()

    user_message = data.get("message")
    session_id = data.get("session_id")

    # Create new session if needed
    if not session_id or session_id not in chat_sessions:
        session_id = str(uuid.uuid4())
        chat_sessions[session_id] = []

    # Add user message
    chat_sessions[session_id].append({
        "role": "user",
        "content": user_message
    })

    payload = {
        "model": "gemma3:4b",
        "messages": chat_sessions[session_id],
        "stream": True
    }

    def generate():

        response = requests.post(
            OLLAMA_URL,
            json=payload,
            stream=True
        )

        assistant_reply = ""
        first_chunk = True

        for line in response.iter_lines():

            if line:
                json_line = json.loads(line.decode("utf-8"))

                if "message" in json_line:
                    content = json_line["message"]["content"]
                    assistant_reply += content

                    if first_chunk:
                        first_chunk = False
                        yield json.dumps({
                            "session_id": session_id,
                            "content": content
                        }) + "\n"
                    else:
                        yield json.dumps({
                            "content": content
                        }) + "\n"

        # Save model response into memory
        chat_sessions[session_id].append({
            "role": "assistant",
            "content": assistant_reply
        })

    return StreamingResponse(generate(), media_type="application/json")
