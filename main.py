from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
import requests
import json

app = FastAPI()

templates = Jinja2Templates(directory="templates")

# حافظه مکالمه
chat_history = []

OLLAMA_URL = "http://localhost:11434/api/chat"

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )

@app.post("/chat")
async def chat(request: Request):

    data = await request.json()
    user_message = data.get("message")

    # ذخیره پیام کاربر
    chat_history.append({
        "role": "user",
        "content": user_message
    })

    payload = {
        "model": "gemma3:4b",
        "messages": chat_history,
        "stream": True
    }

    def generate():

        response = requests.post(
            OLLAMA_URL,
            json=payload,
            stream=True
        )

        assistant_message = ""

        for line in response.iter_lines():

            if line:

                decoded_line = line.decode("utf-8")
                json_data = json.loads(decoded_line)

                if "message" in json_data:
                    content = json_data["message"]["content"]

                    assistant_message += content

                    yield content

        # ذخیره پاسخ مدل
        chat_history.append({
            "role": "assistant",
            "content": assistant_message
        })

    return StreamingResponse(
        generate(),
        media_type="text/plain"
    )
