from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# from app.api.chat import router as chat_router
from app.api.ws import router as ws_router

from app.core.database import create_db

from app.api.chat import router as chat_router

app = FastAPI()

app.include_router(ws_router)
app.include_router(chat_router, prefix="/api/chat")

# static
app.mount("/static", StaticFiles(directory="app/web/static"), name="static")

# templates
templates = Jinja2Templates(directory="app/web/templates")


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        name="index.html",
        request=request
    )


# routers
app.include_router(chat_router, prefix="/api/chat")

# db
create_db()
