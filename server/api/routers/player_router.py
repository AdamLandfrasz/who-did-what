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
            tg.create_task(
                client.websocket.send_json({"messageType": "ping", "message": message})
            )


@player_router.get("/join")
async def player_join(
    player_name: str,
    client_repository: Annotated[ClientRepository, Depends(get_client_repository)],
    session_id: Annotated[str | None, Cookie()] = None,
):
    client_repository.add_client(session_id, player_name)
    print(f"Player {player_name} joined the server!")
