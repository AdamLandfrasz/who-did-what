import uuid
from typing import Annotated
from fastapi import APIRouter, Cookie, Depends, Path, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from server.api.repositories.player_repository import (
    PlayerRepository,
    player_repository,
)
from server.api.repositories.room_repository import RoomRepository, room_repository
from server.api.routers.websockets import send_update_to_room


site_router = APIRouter()


@site_router.get("/")
async def index(request: Request, session_id: Annotated[str | None, Cookie()] = None):
    templates = Jinja2Templates(directory="server/templates")
    response = templates.TemplateResponse("index.html", {"request": request})
    if not session_id:
        response.set_cookie("session_id", value=uuid.uuid4().hex)
    return response


@site_router.get("/joined")
async def joined(
    request: Request,
    player_repository: Annotated[PlayerRepository, Depends(player_repository)],
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


@site_router.get("/room/{room_id}")
async def render_lobby(
    request: Request,
    room_id: Annotated[str, Path()],
    player_repository: Annotated[PlayerRepository, Depends(player_repository)],
    room_repository: Annotated[RoomRepository, Depends(room_repository)],
    session_id: Annotated[str | None, Cookie()] = None,
):
    current_player = player_repository.get_player(session_id)
    current_room = room_repository.get_room(room_id)
    if not current_room:
        return RedirectResponse("/")
    if not current_player:
        return RedirectResponse(f"/?room_id={current_room.id}")

    if current_player not in current_room.players:
        if current_player.room:
            current_player.room.remove_player(current_player)
            await send_update_to_room(current_player.room)
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
