from typing import Annotated
from fastapi import APIRouter, Cookie, Depends, HTTPException, status

from server.api.repository import PlayerRepository, get_player_repository

player_router = APIRouter()


@player_router.get("/join")
async def add_player(
    player_name: str,
    player_repository: Annotated[PlayerRepository, Depends(get_player_repository)],
    session_id: Annotated[str | None, Cookie()] = None,
):
    if not session_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="session cookie is missing"
        )
    player_repository.add_player(session_id, player_name)
    print(f"Player {player_name} joined the server!")
