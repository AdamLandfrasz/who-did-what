import asyncio
from typing import Annotated
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from server.api.repositories.player_repository import (
    player_repository,
    PlayerRepository,
)
from server.api.schemas import Room


websockets_router = APIRouter()


async def send_update_to_room(room: Room):
    connected_players = [player for player in room.players if player.websocket]
    async with asyncio.TaskGroup() as tg:
        for player in connected_players:
            tg.create_task(
                player.websocket.send_json(
                    {
                        "messageType": "player_joined",
                        "playersJoined": [
                            {
                                "name": player.name,
                                "sessionId": player.session_id,
                                "connected": player.websocket is not None,
                            }
                            for player in room.players
                        ],
                        "host": room.host.session_id,
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
    await send_update_to_room(current_room)
    try:
        while True:
            await websocket.receive_json()
    except WebSocketDisconnect:
        current_player.websocket = None
        await send_update_to_room(current_room)
