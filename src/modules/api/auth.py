import os

from fastapi import HTTPException, Request

REQUEST_HEADER_KEY_NAME = "x-api-key"


async def authenticate_dependency(request: Request) -> None:
    auth_key = request.headers.get(REQUEST_HEADER_KEY_NAME)

    if not auth_key or auth_key != os.getenv("AUTH_KEY_SECRET"):
        raise HTTPException(status_code=401)
