import uuid
from typing import Annotated
from fastapi import APIRouter, Cookie, Depends, Path, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from server.api.exceptions import MissingSessionCookieException

from server.api.repositories.player_repository import (
    PlayerRepository,
    player_repository,
)
from server.api.repositories.room_repository import RoomRepository, room_repository


site_router = APIRouter()


async def require_session_cookie(session_id: Annotated[str | None, Cookie()] = None):
    if not session_id:
        raise MissingSessionCookieException("session cookie is missing")


@site_router.get("/")
async def index(request: Request, session_id: Annotated[str | None, Cookie()] = None):
    templates = Jinja2Templates(directory="server/templates")
    response = templates.TemplateResponse("index.html", {"request": request})
    if not session_id:
        response.set_cookie("session_id", value=uuid.uuid4().hex)
    return response


@site_router.get(
    "/joined",
    dependencies=[Depends(require_session_cookie)],
)
async def joined(
    request: Request,
    player_repository: Annotated[PlayerRepository, Depends(player_repository)],
    session_id: Annotated[str, Cookie()],
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


@site_router.get(
    "/room/{room_id}",
    dependencies=[Depends(require_session_cookie)],
)
async def render_lobby(
    request: Request,
    room_id: Annotated[str, Path()],
    session_id: Annotated[str, Cookie()],
    player_repository: Annotated[PlayerRepository, Depends(player_repository)],
    room_repository: Annotated[RoomRepository, Depends(room_repository)],
):
    current_player = player_repository.get_player(session_id)
    current_room = room_repository.get_room(room_id)
    if not (current_player and current_room):
        return RedirectResponse("/")
    if current_player not in current_room.players:
        current_room.add_player(current_player)
        current_player.room = current_room
    templates = Jinja2Templates(directory="server/templates")
    return templates.TemplateResponse(
        "lobby.html",
        {
            "request": request,
            "current_player": current_player,
            "room_host": current_room.host,
        },
    )
