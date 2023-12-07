from typing import Annotated
from fastapi import APIRouter, Cookie, Depends

from server.api.repositories.player_repository import (
    PlayerRepository,
    player_repository,
)
from server.api.schemas import ErrorResponse, SuccessResponse

player_router = APIRouter()


@player_router.get("/join", response_model=SuccessResponse)
async def add_player(
    player_name: str,
    player_repository: Annotated[PlayerRepository, Depends(player_repository)],
    session_id: Annotated[str, Cookie()],
):
    player_repository.add_player(session_id, player_name)
    return {"success": True}
