from functools import lru_cache
from server.api.schemas import Player

SessionId = str


class PlayerRepository:
    def __init__(self) -> None:
        self._players: dict[SessionId, Player] = {}

    def get_player(self, session_id: SessionId) -> Player | None:
        return self._players.get(session_id)

    def get_players(self) -> list[Player]:
        return [*self._players.values()]

    def add_player(self, session_id: SessionId, player_name: str) -> Player:
        self._players[session_id] = Player(session_id=session_id, name=player_name)
        return self._players[session_id]

    def delete_player(self, session_id: SessionId):
        del self._players[session_id]


@lru_cache(maxsize=1)
def get_player_repository() -> PlayerRepository:
    return PlayerRepository()
