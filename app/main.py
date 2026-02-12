"""Konfigurasi dan bootstrap utama aplikasi FastAPI.

File ini bertanggung jawab untuk:
- Membuat instance aplikasi FastAPI.
- Mengatur CORS origins dari environment variable.
- Memuat konfigurasi JWT untuk `fastapi-jwt-auth`.
- Mendaftarkan router API.
- Menyediakan endpoint dasar (`/`) dan health check (`/health`).
"""

import os
from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_jwt_auth import AuthJWT

from app.api import auth_router, menu_router
from app.core.config import JWTSettings


def _parse_cors_origins() -> list[str]:
    """Parse daftar origin CORS dari environment variable `CORS_ORIGINS`.

    Format nilai env:
    - Dipisahkan koma, contoh: `https://a.com,http://localhost:4321`.
    - Spasi ekstra akan di-trim.
    - Origin kosong akan diabaikan.
    """
    raw = os.getenv(
        "CORS_ORIGINS",
        "https://app.wisnubaldas.net,http://localhost:4321,http://127.0.0.1:4321",
    )
    return [origin.strip() for origin in raw.split(",") if origin.strip()]


app = FastAPI(
    title="API Baldas Blog",
    version="0.1.0",
    description=(
        "REST API untuk kebutuhan autentikasi dan layanan backend aplikasi Baldas Blog."
    ),
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=_parse_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(menu_router)


@AuthJWT.load_config
def get_jwt_config() -> list[tuple[str, Any]]:
    """Sediakan konfigurasi JWT ke `fastapi-jwt-auth`.

    `JWTSettings()` mengembalikan iterable pasangan key-value konfigurasi,
    kemudian dikonversi ke list agar sesuai dengan format yang diharapkan
    decorator `@AuthJWT.load_config`.
    """
    return list(JWTSettings())


@app.get("/")
def read_root() -> dict[str, str]:
    """Endpoint root untuk verifikasi cepat bahwa API aktif."""
    return {"message": "API Baldas Blog is running"}


@app.get("/health")
def health_check() -> dict[str, str]:
    """Health check sederhana untuk monitoring/liveness probe."""
    return {"status": "ok"}
