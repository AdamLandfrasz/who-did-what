import asyncio
from typing import Annotated
from fastapi import APIRouter, Cookie, Depends

from server.api.repository import PlayerRepository, get_player_repository

player_router = APIRouter()


@player_router.get("/ping")
async def ping_websockets(
    message: str,
    player_repository: PlayerRepository = Depends(get_player_repository),
):
    async with asyncio.TaskGroup() as tg:
        for player in player_repository.get_players():
            tg.create_task(
                player.websocket.send_json({"messageType": "ping", "message": message})
            )


@player_router.get("/join")
async def player_join(
    player_name: str,
    player_repository: Annotated[PlayerRepository, Depends(get_player_repository)],
    session_id: Annotated[str | None, Cookie()] = None,
):
    player_repository.add_player(session_id, player_name)
    print(f"Player {player_name} joined the server!")
