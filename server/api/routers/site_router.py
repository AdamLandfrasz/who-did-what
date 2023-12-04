import uuid
from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse

site_router = APIRouter()


@site_router.get("/")
async def index(request: Request):
    response = JSONResponse({"success":True}, status_code=status.HTTP_200_OK)
    if "session_id" not in request.cookies:
        response.set_cookie("session_id", value=uuid.uuid4())
    return response