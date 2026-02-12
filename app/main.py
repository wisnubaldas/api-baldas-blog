import os
from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_jwt_auth import AuthJWT

from app.api import auth_router
from app.core.config import JWTSettings


def _parse_cors_origins() -> list[str]:
    raw = os.getenv(
        "CORS_ORIGINS",
        "https://app.wisnubaldas.net,http://localhost:4321,http://127.0.0.1:4321",
    )
    return [origin.strip() for origin in raw.split(",") if origin.strip()]


app = FastAPI(title="API Baldas Blog", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=_parse_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
