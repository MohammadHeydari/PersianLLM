import requests

OLLAMA_URL = "http://localhost:11434/api/chat"

MODEL_NAME = "gemma3:4b"


def stream_chat(messages):

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "messages": messages,
            "stream": True
        },
        stream=True
    )

    return response
