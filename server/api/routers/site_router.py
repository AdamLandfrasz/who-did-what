from typing import Annotated
import uuid
from fastapi import APIRouter, Cookie, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from server.api.repository import PlayerRepository, get_player_repository


site_router = APIRouter()


@site_router.get("/", response_class=HTMLResponse)
async def index(request: Request, session_id: Annotated[str | None, Cookie()] = None):
    templates = Jinja2Templates(directory="server/templates")
    response = templates.TemplateResponse("index.html", {"request": request})
    if not session_id:
        response.set_cookie("session_id", value=uuid.uuid4())
    return response


@site_router.get("/joined", response_class=HTMLResponse)
async def index(
    request: Request,
    player_repository: Annotated[PlayerRepository, Depends(get_player_repository)],
    session_id: Annotated[str | None, Cookie()] = None,
):
    current_player = player_repository.get_player(session_id)
    if not current_player:
        return RedirectResponse("/")
    templates = Jinja2Templates(directory="server/templates")
    return templates.TemplateResponse(
        "joined.html",
        {
            "request": request,
            "current_player": current_player,
        },
    )
