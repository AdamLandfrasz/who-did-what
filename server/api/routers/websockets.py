from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from server.api.repository import get_client_repository, ClientRepository


websockets_router = APIRouter()


@websockets_router.websocket("/connect")
async def websocket_endpoint(
    websocket: WebSocket,
    client_repository: ClientRepository = Depends(get_client_repository),
):
    await websocket.accept()
    client_repository.add_client(websocket.cookies["session_id"], websocket)
    try:
        while True:
            await websocket.receive_json()
    except WebSocketDisconnect:
        client_repository.delete_client(websocket.cookies["session_id"])
