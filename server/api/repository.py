from functools import lru_cache
from fastapi import WebSocket

from server.api.schemas import Player

SessionId = str


class ClientRepository:
    def __init__(self) -> None:
        self._client_sessions: dict[SessionId, Player] = {}

    def get_client(self, session_id: SessionId) -> Player:
        return self._client_sessions[session_id]

    def get_clients(self) -> list[Player]:
        return [*self._client_sessions.values()]

    def add_client(self, session_id: SessionId, websocket: WebSocket):
        self._client_sessions[session_id] = Player(
            session_id=session_id, websocket=websocket
        )

    def delete_client(self, session_id: SessionId):
        del self._client_sessions[session_id]


@lru_cache(maxsize=1)
def get_client_repository() -> ClientRepository:
    return ClientRepository()
