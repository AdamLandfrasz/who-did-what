import asyncio
from typing import Annotated
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from server.api.repositories.player_repository import (
    player_repository,
    PlayerRepository,
)
from server.api.schemas import Player


websockets_router = APIRouter()


async def update_players(players: list[Player]):
    connected_players = [player for player in players if player.websocket]
    async with asyncio.TaskGroup() as tg:
        for player in connected_players:
            tg.create_task(
                player.websocket.send_json(
                    {
                        "messageType": "player_joined",
                        "playersJoined": [player.name for player in connected_players],
                    }
                )
            )


@websockets_router.websocket("/connect")
async def websocket_endpoint(
    websocket: WebSocket,
    player_repository: Annotated[PlayerRepository, Depends(player_repository)],
):
    await websocket.accept()
    player_repository.get_player(websocket.cookies["session_id"]).websocket = websocket
    await update_players(player_repository.get_players())
    try:
        while True:
            await websocket.receive_json()
    except WebSocketDisconnect:
        player_repository.get_player(websocket.cookies["session_id"]).websocket = None
        await update_players(player_repository.get_players())
