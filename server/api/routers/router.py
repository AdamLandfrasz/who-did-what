from fastapi import APIRouter
from server.api.schemas import SuccessResponse
from server.api.routers.websockets import websockets_router
from server.api.routers.site_router import site_router


api_router = APIRouter()
api_router.include_router(websockets_router, prefix="/ws", include_in_schema=False)
api_router.include_router(site_router, prefix="", include_in_schema=False)


@api_router.get("/ping", tags=["ping"], response_model=SuccessResponse)
async def ping():
    return {"success": True}
