"""Agregator router API.

Tujuan file ini:
1. Menyediakan satu pintu import router dari package `app.api`.
2. Memisahkan detail lokasi router (`app.api.auth`, dst) dari `app.main`.

Relasi dengan auth:
- `auth_router` di-import dari `app.api.auth` lalu diexport ulang.
- `app.main` cukup memanggil `from app.api import auth_router`,
  kemudian `app.include_router(auth_router)`.

Jika ingin tambah route menu:
1. Buat file `app/api/menu.py` yang memiliki `router = APIRouter(...)`.
2. Import di sini: `from app.api.menu import router as menu_router`.
3. Tambahkan ke `__all__` agar bisa di-import dari `app.api`.
4. Di `app/main.py`, include router baru: `app.include_router(menu_router)`.
"""

from app.api.auth import router as auth_router
from app.api.menu import router as menu_router
from app.api.user import router as user_router
from app.api.roles_permission import router as roles_permission_router

# Simbol resmi yang diexport saat `from app.api import *`.
__all__ = ["auth_router", "menu_router", "user_router", "roles_permission_router"]
