from __future__ import annotations
from fastapi import WebSocket
from pydantic import BaseModel, ConfigDict, Field


class SuccessResponse(BaseModel):
    success: bool = True


class Player(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    session_id: str
    name: str
    websocket: WebSocket | None = None
    room: Room | None = None


class Room(BaseModel):
    id: str
    players: list[Player] = Field(default=list)

    def add_player(self, player: Player):
        self.players.append(player)

    def remove_player(self, player: Player):
        self.players.remove(player)
