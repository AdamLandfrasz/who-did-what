from fastapi import APIRouter
from server.api.schemas import SuccessResponse
from server.api.routers.websockets import websockets_router
from server.api.routers.site_router import site_router
from server.api.routers.player_router import player_router
from server.api.routers.room_router import room_router


api_router = APIRouter()
api_router.include_router(player_router, prefix="/players", tags=["players"])
api_router.include_router(room_router, prefix="/rooms", tags=["rooms"])
api_router.include_router(websockets_router, prefix="/ws", include_in_schema=False)
api_router.include_router(site_router, prefix="", include_in_schema=False)


@api_router.get("/ping", tags=["ping"], response_model=SuccessResponse)
async def ping():
    return {"success": True}
