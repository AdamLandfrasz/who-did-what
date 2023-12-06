import asyncio
from typing import Annotated
from fastapi import APIRouter, Cookie, Depends

from server.api.repository import ClientRepository, get_client_repository

player_router = APIRouter()


@player_router.get("/ping")
async def ping_websockets(
    message: str,
    client_repository: ClientRepository = Depends(get_client_repository),
):
    async with asyncio.TaskGroup() as tg:
        for client in client_repository.get_clients():
            tg.create_task(client.websocket.send_json({"message": message}))


@player_router.get("/join")
async def player_join(
    player_name: str,
    client_repository: Annotated[ClientRepository, Depends(get_client_repository)],
    session_id: Annotated[str | None, Cookie()] = None,
):
    player = client_repository.get_client(session_id)
    player.name = player_name
    player.joined = True
    print(f"Player {player_name} joined the server!")

    joined_players = [
        player for player in client_repository.get_clients() if player.joined
    ]

    async with asyncio.TaskGroup() as tg:
        for player in joined_players:
            tg.create_task(
                player.websocket.send_json(
                    {
                        "messageType": "player_joined",
                        "playersJoined": [player.name for player in joined_players],
                    }
                )
            )
