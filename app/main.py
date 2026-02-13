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

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException

from app.api import auth_router, menu_router, user_router, roles_permission_router
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


PUBLIC_PATHS = {
    "/auth/register",
    "/auth/login",
    "/auth/refresh",
    "/docs",
    "/redoc",
    "/openapi.json",
    "/health",
    "/",
}


@app.middleware("http")
async def require_authenticated_user(request: Request, call_next):
    """Middleware autentikasi global berbasis JWT access token.

    Perilaku:
    - Semua endpoint private wajib membawa access token yang valid.
    - Endpoint yang ada di `PUBLIC_PATHS` dibiarkan lewat tanpa token.
    - Jika token tidak ada/tidak valid, request dihentikan dengan HTTP 401.
    - Jika token valid, request diteruskan dan response asli endpoint dikembalikan.

    Catatan:
    - Karena validasi dilakukan *sebelum* endpoint dieksekusi, route private tidak
      akan memproses logic bisnis ketika user belum login.
    """
    path = request.url.path
    if request.method == "OPTIONS" or path in PUBLIC_PATHS:
        return await call_next(request)

    try:
        AuthJWT(req=request).jwt_required()
    except AuthJWTException:
        return JSONResponse(status_code=401, content={"detail": "Unauthorized"})

    return await call_next(request)


app.include_router(auth_router)
app.include_router(menu_router)
app.include_router(user_router)
app.include_router(roles_permission_router)


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
