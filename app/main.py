from typing import Any

from fastapi import FastAPI
from fastapi_jwt_auth import AuthJWT

from app.api import auth_router
from app.core.config import JWTSettings

app = FastAPI(title="API Baldas Blog", version="0.1.0")
app.include_router(auth_router)


@AuthJWT.load_config
def get_jwt_config() -> list[tuple[str, Any]]:
    return list(JWTSettings())


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "API Baldas Blog is running"}


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
