from typing import Annotated
from fastapi import APIRouter, Cookie, Depends
from server.api.repositories.player_repository import (
    PlayerRepository,
    player_repository,
)
from server.api.repositories.room_repository import RoomRepository, room_repository
from server.api.schemas import RoomResponse

room_router = APIRouter()


@room_router.post("/create", response_model=RoomResponse)
async def create_room(
    player_name: str,
    player_repository: Annotated[PlayerRepository, Depends(player_repository)],
    room_repository: Annotated[RoomRepository, Depends(room_repository)],
    session_id: Annotated[str, Cookie()],
):
    host_player = player_repository.add_player(
        session_id=session_id, player_name=player_name
    )
    room_created = room_repository.add_room(host=host_player)
    room_created.add_player(host_player)
    host_player.room = room_created
    return room_created
