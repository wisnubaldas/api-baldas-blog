"""Pusat dependency injection untuk service dan repository aplikasi."""

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repository.menu_repository import MenuRepository
from app.services.menu_service import MenuService


def get_menu_repository(db: Session = Depends(get_db)) -> MenuRepository:
    """Dependency provider: injeksi repository dengan Session database."""
    return MenuRepository(db)


def get_menu_service(
    repository: MenuRepository = Depends(get_menu_repository),
) -> MenuService:
    """Dependency provider: injeksi service dengan repository."""
    return MenuService(repository)
