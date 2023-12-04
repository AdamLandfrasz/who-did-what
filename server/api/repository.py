from functools import lru_cache
from fastapi import WebSocket

from server.utils import Singleton

SessionId = str

class ClientRepository():
    def __init__(self) -> None:
        self._client_sessions: dict[SessionId, WebSocket] = {}

    def get_clients(self) -> list[WebSocket]:
        return [*self._client_sessions.copy().values()]

    def add_client(self, session_id:SessionId, websocket: WebSocket):
        self._client_sessions[session_id] = websocket

    def delete_client(self, session_id:SessionId):
        del self._client_sessions[session_id]

@lru_cache(maxsize=1)
def get_client_repository() -> ClientRepository:
    return ClientRepository()