"""Model package exports.

Modul ini menjadi pintu masuk tunggal untuk import seluruh model SQLAlchemy
yang dipakai di aplikasi, misalnya:
`from app.models import User, Role, Menu`.
"""

from app.models.rbac import Menu, Permission, Role, RolePermission, User, UserRole

# Batasi simbol yang diexport saat memakai `from app.models import *`.
__all__ = ["User", "Role", "Permission", "RolePermission", "UserRole", "Menu"]
