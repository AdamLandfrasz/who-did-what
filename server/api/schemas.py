from fastapi import WebSocket
from pydantic import BaseModel, ConfigDict


class SuccessResponse(BaseModel):
    success: bool = True


class Player(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    session_id: str
    name: str
    websocket: WebSocket | None = None
    room: str | None = None
