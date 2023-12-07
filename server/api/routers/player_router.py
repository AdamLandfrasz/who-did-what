from typing import Annotated
from fastapi import APIRouter, Cookie, Depends

from server.api.repositories.player_repository import (
    PlayerRepository,
    player_repository,
)
from server.api.schemas import SuccessResponse

player_router = APIRouter()


@player_router.get("/join", response_model=SuccessResponse)
async def add_player(
    player_name: str,
    session_id: Annotated[str, Cookie()],
    player_repository: Annotated[PlayerRepository, Depends(player_repository)],
):
    player_repository.add_player(session_id, player_name)
    return {"success": True}
