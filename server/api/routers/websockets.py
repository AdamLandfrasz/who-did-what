import asyncio
from typing import Annotated
from fastapi import APIRouter, Cookie, Depends, Request, WebSocket, WebSocketDisconnect
from server.api.repository import get_client_repository, ClientRepository


websockets_router = APIRouter()


@websockets_router.websocket("/connect")
async def websocket_endpoint(
    websocket: WebSocket,
    client_repository:ClientRepository = Depends(get_client_repository)
):
    await websocket.accept()
    client_repository.add_client(websocket.cookies["session_id"], websocket)
    try:
        while True:
            await websocket.receive_json()
    except WebSocketDisconnect:
        client_repository.delete_client(websocket.cookies["session_id"])


@websockets_router.get("/ping")
async def ping_websockets(
    name:str, 
    session_id: Annotated[str | None, Cookie()] = None,
    client_repository:ClientRepository = Depends(get_client_repository)
):
    filtered_clients = [
        client 
        for sid, client in client_repository.get_clients().items() 
        if sid != session_id
    ]
    async with asyncio.TaskGroup() as tg:
        for client in filtered_clients:
            tg.create_task(client.send_json({"message": f"{name} joined the game!"}))