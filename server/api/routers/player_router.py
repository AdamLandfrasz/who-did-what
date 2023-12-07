from typing import Annotated
from fastapi import APIRouter, Cookie, Depends, HTTPException, status

from server.api.repositories.player_repository import (
    PlayerRepository,
    player_repository,
)
from server.api.schemas import ErrorResponse, SuccessResponse

player_router = APIRouter()


@player_router.get("/join", responses={200:{"model": SuccessResponse}, 400: {"model":ErrorResponse}})
async def add_player(
    player_name: str,
    player_repository: Annotated[PlayerRepository, Depends(player_repository)],
    session_id: Annotated[str | None, Cookie()] = None,
):
    if not session_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="session cookie is missing"
        )
    player_repository.add_player(session_id, player_name)
    print(f"Player {player_name} joined the server!")
    return {"success": True}
