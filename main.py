from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates

import requests
import json

app = FastAPI()

templates = Jinja2Templates(directory="templates")

OLLAMA_URL = "http://localhost:11434/api/generate"

MODEL_NAME = "gemma3:4b"

SYSTEM_PROMPT = """
تو یک دستیار فارسی حرفه‌ای هستی.
همیشه فارسی پاسخ بده.
"""

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )

@app.post("/chat")
async def chat(request: Request):

    data = await request.json()

    user_message = data["message"]

    prompt = f"""
{SYSTEM_PROMPT}

کاربر:
{user_message}

دستیار:
"""

    def generate():

        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": True
            },
            stream=True
        )

        for line in response.iter_lines():

            if line:

                decoded = line.decode("utf-8")

                try:

                    json_data = json.loads(decoded)

                    if "response" in json_data:
                        yield json_data["response"]

                except:
                    pass

    return StreamingResponse(
        generate(),
        media_type="text/plain"
    )
