from fastapi import FastAPI

from server.api.router import router
from server.config import get_settings


def get_application() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title=settings.project_name, version=settings.project_version)
    app.include_router(router)
    return app

app = get_application()