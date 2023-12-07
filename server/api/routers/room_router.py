from typing import Annotated
from fastapi import APIRouter, Cookie, Depends, HTTPException, Path, status
from server.api.repositories.player_repository import (
    PlayerRepository,
    player_repository,
)
from server.api.repositories.room_repository import RoomRepository, room_repository
from server.api.schemas import RoomResponse, SuccessResponse

room_router = APIRouter()


@room_router.get("/create", response_model=RoomResponse)
async def create_room(
    session_id: Annotated[str, Cookie()],
    player_repository: Annotated[PlayerRepository, Depends(player_repository)],
    room_repository: Annotated[RoomRepository, Depends(room_repository)],
):
    host_player = player_repository.get_player(session_id=session_id)
    if not host_player:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="host player does not exist"
        )
    room_created = room_repository.add_room(host=host_player)
    host_player.room = room_created
    return room_created


@room_router.get("/join/{room_id}", response_model=SuccessResponse)
async def join_room(
    room_id: Annotated[str, Path()],
    session_id: Annotated[str, Cookie()],
    player_repository: Annotated[PlayerRepository, Depends(player_repository)],
    room_repository: Annotated[RoomRepository, Depends(room_repository)],
):
    joining_player = player_repository.get_player(session_id=session_id)
    if not joining_player:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="player does not exist"
        )
    room_being_joined = room_repository.get_room(room_id)
    if not joining_player:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"room {room_id} does not exist",
        )
    room_being_joined.add_player(joining_player)
    joining_player.room = room_being_joined
    return {"success": True}
