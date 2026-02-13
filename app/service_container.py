"""Pusat dependency injection untuk service dan repository aplikasi."""

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repository.menu_repository import MenuRepository
from app.repository.rbac_repository import RBACRepository
from app.repository.user_repository import UserRepository
from app.services.menu_service import MenuService
from app.services.rbac_service import RBACService
from app.services.user_service import UserService


def get_menu_repository(db: Session = Depends(get_db)) -> MenuRepository:
    """Dependency provider: injeksi repository dengan Session database."""
    return MenuRepository(db)


def get_menu_service(
    repository: MenuRepository = Depends(get_menu_repository),
) -> MenuService:
    """Dependency provider: injeksi service dengan repository."""
    return MenuService(repository)


def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    """Dependency provider: injeksi repository user dengan Session database."""
    return UserRepository(db)


def get_user_service(
    repository: UserRepository = Depends(get_user_repository),
) -> UserService:
    """Dependency provider: injeksi service user dengan repository."""
    return UserService(repository)


def get_rbac_repository(db: Session = Depends(get_db)) -> RBACRepository:
    """Dependency provider: injeksi repository RBAC dengan Session database."""
    return RBACRepository(db)


def get_rbac_service(
    repository: RBACRepository = Depends(get_rbac_repository),
) -> RBACService:
    """Dependency provider: injeksi service RBAC dengan repository."""
    return RBACService(repository)
