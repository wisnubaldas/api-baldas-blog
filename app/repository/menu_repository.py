"""Lapisan akses data (repository) untuk entitas menu."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Menu as MenuEntity
from app.models.menu import MenuCreate, MenuUpdate


class MenuRepository:
    """Repository untuk operasi database tabel menus."""

    def __init__(self, db: Session) -> None:
        # Simpan session database hasil injeksi Depends(get_db).
        self.db = db

    def list(self, skip: int, limit: int) -> list[MenuEntity]:
        # Ambil daftar menu berurutan berdasarkan section -> parent -> sort -> id.
        query = (
            select(MenuEntity)
            .order_by(
                MenuEntity.section_title,
                MenuEntity.parent_id,
                MenuEntity.sort_order,
                MenuEntity.id,
            )
            .offset(skip)
            .limit(limit)
        )
        # Jalankan query dan kembalikan semua baris hasil.
        return list(self.db.scalars(query).all())

    def get_by_id(self, menu_id: int) -> MenuEntity | None:
        # Ambil satu menu berdasarkan primary key id.
        return self.db.get(MenuEntity, menu_id)

    def get_by_key(self, menu_key: str) -> MenuEntity | None:
        # Cari menu berdasarkan nilai unik menu_key.
        return self.db.scalar(
            select(MenuEntity).where(MenuEntity.menu_key == menu_key)
        )

    def create(self, payload: MenuCreate) -> MenuEntity:
        # Buat objek model Menu dari payload request.
        menu = MenuEntity(**payload.dict())
        # Tambahkan objek ke session agar ditandai untuk insert.
        self.db.add(menu)
        # Commit transaksi agar data benar-benar tersimpan.
        self.db.commit()
        # Refresh objek untuk mengambil nilai terbaru dari DB (id/timestamp).
        self.db.refresh(menu)
        # Kembalikan objek menu yang sudah tersimpan.
        return menu

    def update(self, menu: MenuEntity, payload: MenuUpdate) -> MenuEntity:
        # Ambil hanya field yang benar-benar dikirim client.
        changes = payload.dict(exclude_unset=True)
        # Terapkan setiap perubahan ke instance menu existing.
        for field_name, value in changes.items():
            setattr(menu, field_name, value)
        # Commit transaksi update.
        self.db.commit()
        # Refresh agar nilai terbaru sinkron dari DB.
        self.db.refresh(menu)
        # Kembalikan menu yang sudah diperbarui.
        return menu

    def delete(self, menu: MenuEntity) -> None:
        # Tandai objek menu untuk dihapus.
        self.db.delete(menu)
        # Commit transaksi delete.
        self.db.commit()
