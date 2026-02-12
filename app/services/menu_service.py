"""Lapisan business logic untuk operasi CRUD menu."""

from fastapi import HTTPException, status

from app.models import Menu as MenuEntity
from app.models.menu import MenuCreate, MenuUpdate
from app.repository.menu_repository import MenuRepository


class MenuService:
    """Service untuk validasi dan orkestrasi operasi menu."""

    def __init__(self, repository: MenuRepository) -> None:
        # Injeksi repository agar service tidak bergantung langsung ke Session.
        self.repository = repository

    def list_menus(self, skip: int, limit: int) -> list[MenuEntity]:
        # Delegasi ke repository untuk mengambil daftar menu.
        return self.repository.list(skip=skip, limit=limit)

    def get_menu(self, menu_id: int) -> MenuEntity:
        # Ambil menu berdasarkan id.
        menu = self.repository.get_by_id(menu_id)
        # Jika tidak ditemukan, lempar 404.
        if not menu:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Menu not found"
            )
        # Kembalikan menu yang valid.
        return menu

    def create_menu(self, payload: MenuCreate) -> MenuEntity:
        # Validasi menu_key harus unik sebelum insert.
        if self.repository.get_by_key(payload.menu_key):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="menu_key already exists",
            )

        # Jika parent_id diisi, pastikan parent menu ada.
        if payload.parent_id is not None and not self.repository.get_by_id(
            payload.parent_id
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="parent_id is invalid",
            )

        # Simpan data baru lewat repository.
        return self.repository.create(payload)

    def update_menu(self, menu_id: int, payload: MenuUpdate) -> MenuEntity:
        # Pastikan data target update ada.
        menu = self.get_menu(menu_id)

        # Ambil perubahan parsial dari payload.
        changes = payload.dict(exclude_unset=True)

        # Validasi duplikasi menu_key jika field itu ikut diubah.
        new_key = changes.get("menu_key")
        if new_key:
            existing = self.repository.get_by_key(new_key)
            if existing and existing.id != menu_id:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="menu_key already exists",
                )

        # Validasi parent_id tidak boleh menunjuk dirinya sendiri.
        if "parent_id" in changes:
            parent_id = changes["parent_id"]
            if parent_id == menu_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="parent_id cannot reference itself",
                )
            if parent_id is not None and not self.repository.get_by_id(parent_id):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="parent_id is invalid",
                )

        # Proses update data di repository.
        return self.repository.update(menu, payload)

    def delete_menu(self, menu_id: int) -> None:
        # Pastikan data yang akan dihapus ada.
        menu = self.get_menu(menu_id)
        # Hapus data lewat repository.
        self.repository.delete(menu)
