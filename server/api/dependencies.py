from typing import Annotated

from fastapi import Cookie, HTTPException, status


async def require_session_cookie(session_id: Annotated[str | None, Cookie()] = None):
    if not session_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="session cookie is missing"
        )
