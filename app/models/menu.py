"""Model request/response untuk fitur menu."""

from datetime import datetime

from pydantic import BaseModel, Field


class MenuBase(BaseModel):
    """Properti umum menu yang dipakai create dan update."""

    # Kunci unik menu sebagai identitas fungsional (contoh: dashboard.main).
    menu_key: str = Field(min_length=1, max_length=255)
    # Grup section sidebar/menu (contoh: Main, Others).
    section_title: str = Field(min_length=1, max_length=80)
    # Parent untuk membuat menu bertingkat, boleh kosong untuk root.
    parent_id: int | None = None
    # Label teks yang tampil di UI.
    label: str = Field(min_length=1, max_length=120)
    # Link tujuan saat menu diklik, boleh kosong jika hanya parent.
    href: str | None = Field(default=None, max_length=255)
    # Nama icon (misal material icon key), opsional.
    icon: str | None = Field(default=None, max_length=80)
    # ID list di frontend (opsional, untuk kebutuhan toggle/show more).
    list_id: str | None = Field(default=None, max_length=120)
    # Teks badge kecil pada menu (opsional).
    badge_text: str | None = Field(default=None, max_length=50)
    # Class CSS badge (opsional).
    badge_class_name: str | None = None
    # Flag status aktif menu.
    is_active: bool = False
    # Flag sembunyikan item menu.
    is_hidden: bool = False
    # Flag tampilkan tombol show more.
    show_more_toggle: bool = False
    # Flag submenu terbuka saat render awal.
    initially_open: bool = False
    # Level kedalaman menu (root=0, child=1, dst).
    depth: int = Field(default=0, ge=0)
    # Urutan tampil menu dalam section/parent yang sama.
    sort_order: int = Field(default=0, ge=0)


class MenuCreate(MenuBase):
    """Payload request untuk membuat menu baru."""


class MenuUpdate(BaseModel):
    """Payload request untuk update menu (partial update)."""

    # Semua field opsional agar endpoint bisa dipakai sebagai PATCH.
    menu_key: str | None = Field(default=None, min_length=1, max_length=255)
    section_title: str | None = Field(default=None, min_length=1, max_length=80)
    parent_id: int | None = None
    label: str | None = Field(default=None, min_length=1, max_length=120)
    href: str | None = Field(default=None, max_length=255)
    icon: str | None = Field(default=None, max_length=80)
    list_id: str | None = Field(default=None, max_length=120)
    badge_text: str | None = Field(default=None, max_length=50)
    badge_class_name: str | None = None
    is_active: bool | None = None
    is_hidden: bool | None = None
    show_more_toggle: bool | None = None
    initially_open: bool | None = None
    depth: int | None = Field(default=None, ge=0)
    sort_order: int | None = Field(default=None, ge=0)


class MenuResponse(MenuBase):
    """Representasi response menu dari database."""

    # ID integer auto-increment dari tabel menus.
    id: int
    # Waktu pembuatan baris data menu.
    created_at: datetime
    # Waktu terakhir pembaruan baris data menu.
    updated_at: datetime

    class Config:
        # Mengizinkan Pydantic membaca atribut langsung dari objek ORM SQLAlchemy.
        orm_mode = True
