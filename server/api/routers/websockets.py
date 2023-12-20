import asyncio
from typing import Annotated
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from server.api.repositories.player_repository import (
    player_repository,
    PlayerRepository,
)
from server.api.schemas import Player


websockets_router = APIRouter()


async def update_players(players: list[Player], host:Player):
    connected_players = [player for player in players if player.websocket]
    async with asyncio.TaskGroup() as tg:
        for player in connected_players:
            tg.create_task(
                player.websocket.send_json(
                    {
                        "messageType": "player_joined",
                        "playersJoined": [player.name for player in connected_players],
                        "host": host.name,
                    }
                )
            )


@websockets_router.websocket("/connect")
async def websocket_endpoint(
    websocket: WebSocket,
    player_repository: Annotated[PlayerRepository, Depends(player_repository)],
):
    await websocket.accept()
    current_player = player_repository.get_player(websocket.cookies["session_id"])
    current_player.websocket = websocket
    current_room = current_player.room
    await update_players(current_room.players, host=current_room.host)
    try:
        while True:
            await websocket.receive_json()
    except WebSocketDisconnect:
        current_player.websocket = None
        await update_players(current_room.players, host=current_room.host)
