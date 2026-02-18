"""Model package exports.

Modul ini menjadi pintu masuk tunggal untuk import seluruh model SQLAlchemy
yang dipakai di aplikasi, misalnya:
`from app.models import User, Role, Menu, Vendor, Customer`.
"""

from app.models.coa import COAAccount, COAAccountSettings, COADimension
from app.models.customer import Customer
from app.models.fin_settings import FinancialSettings
from app.models.rbac import Menu, Permission, Role, RolePermission, User, UserRole
from app.models.vendor import Vendor

# Batasi simbol yang diexport saat memakai `from app.models import *`.
__all__ = [
    # RBAC
    "User",
    "Role",
    "Permission",
    "RolePermission",
    "UserRole",
    "Menu",
    # Finance - COA
    "COAAccount",
    "COADimension",
    "COAAccountSettings",
    # Finance - Master Data
    "Vendor",
    "Customer",
    "FinancialSettings",
]
