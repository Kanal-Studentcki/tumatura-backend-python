import os
from importlib import import_module
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse
from starlette.status import HTTP_401_UNAUTHORIZED

from .routers import routers

ROOT_PATH = ""

app = FastAPI(root_path=f"/{ROOT_PATH}")

# Load all routers
for file in os.listdir(Path(__file__).parent / "endpoints"):
    if file not in ["__init__.py", "helpers.py"]:
        import_module(f"src.modules.api.endpoints.{file.replace('.py', '')}")

for router in routers:
    app.include_router(router, prefix="/v1")


@app.exception_handler(HTTP_401_UNAUTHORIZED)
async def http401_error_handler(request: Request, exception: HTTPException) -> JSONResponse:
    return JSONResponse({"error": "unauthorized"}, status_code=HTTP_401_UNAUTHORIZED)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    msg = "Request validation failed:"
    for error in exc.errors():
        loc_parts = (str(part) for part in error["loc"])
        field = ".".join(loc_parts).removeprefix("body.")

        if field.endswith("__root__"):
            msg += f"\n{error['msg']}"
        else:
            msg += f"\n{field}: {error['msg']}"

    return JSONResponse({"error": msg}, status_code=400)


def run() -> None:
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
