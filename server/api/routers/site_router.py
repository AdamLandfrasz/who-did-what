from typing import Annotated
import uuid
from fastapi import APIRouter, Cookie, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


site_router = APIRouter()


@site_router.get("/", response_class=HTMLResponse)
async def index(request: Request, session_id: Annotated[str | None, Cookie()] = None):
    templates = Jinja2Templates(directory="server/templates")
    response = templates.TemplateResponse("index.html",{"request": request})
    if not session_id:
        response.set_cookie("session_id", value=uuid.uuid4())
    return response