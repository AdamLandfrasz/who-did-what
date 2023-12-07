from fastapi import Request
from fastapi.responses import RedirectResponse


class MissingSessionCookieException(Exception):
    def __init__(self, detail: str) -> None:
        self.detail = detail


async def handle_missing_session(request: Request, exc: MissingSessionCookieException):
    return RedirectResponse("/")
