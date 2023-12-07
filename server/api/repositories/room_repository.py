from functools import lru_cache
import uuid
from server.api.schemas import Player, Room

RoomId = str


class RoomRepository:
    def __init__(self) -> None:
        self._rooms: dict[RoomId, Room] = {}

    def get_room(self, room_id: RoomId) -> Room | None:
        return self._rooms.get(room_id)

    def add_room(self, host: Player) -> Room:
        new_room_id = uuid.uuid4().hex[:5]
        new_room = Room(
            id=new_room_id,
            host=host,
        )
        new_room.add_player(host)
        self._rooms[new_room_id] = new_room
        return new_room


@lru_cache(maxsize=1)
def room_repository() -> RoomRepository:
    return RoomRepository()
