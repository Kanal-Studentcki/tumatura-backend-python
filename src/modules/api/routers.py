from fastapi import APIRouter, Depends

from .auth import authenticate_dependency

routers = []


def register_router(prefix: str, *, require_auth: bool = True) -> APIRouter:
    router = APIRouter(prefix=prefix, dependencies=[Depends(authenticate_dependency)] if require_auth else [])
    routers.append(router)
    return router
