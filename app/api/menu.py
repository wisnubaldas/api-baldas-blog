"""Endpoint CRUD menu berbasis FastAPI."""

from fastapi import APIRouter, Depends, Query, status

from app.models.menu import MenuCreate, MenuResponse, MenuUpdate
from app.service_container import get_menu_service
from app.services.menu_service import MenuService

# Router utama untuk semua endpoint menu.
router = APIRouter(prefix="/menu", tags=["Menu"])


@router.get("/", response_model=list[MenuResponse])
def list_menus(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
    service: MenuService = Depends(get_menu_service),
) -> list[MenuResponse]:
    """Ambil daftar menu dengan pagination sederhana."""
    # Route hanya mengatur input query + memanggil service.
    # Output tetap mengikuti response_model (MenuResponse).
    menus = service.list_menus(skip=skip, limit=limit)
    return [MenuResponse.from_orm(menu) for menu in menus]


@router.get("/all", response_model=list[MenuResponse])
def get_all_menus(service: MenuService = Depends(get_menu_service)) -> list[MenuResponse]:
    """Endpoint kompatibilitas untuk rute lama `/menu/all`."""
    # Route kompatibilitas agar endpoint lama tetap jalan.
    menus = service.list_menus(skip=0, limit=500)
    return [MenuResponse.from_orm(menu) for menu in menus]


@router.get("/{menu_id}", response_model=MenuResponse)
def get_menu(
    menu_id: int, service: MenuService = Depends(get_menu_service)
) -> MenuResponse:
    """Ambil detail satu menu berdasarkan id."""
    # `menu_id` diteruskan ke service untuk validasi + ambil data.
    menu = service.get_menu(menu_id)
    return MenuResponse.from_orm(menu)


@router.post("/", response_model=MenuResponse, status_code=status.HTTP_201_CREATED)
def create_menu(
    payload: MenuCreate,
    service: MenuService = Depends(get_menu_service),
) -> MenuResponse:
    """Buat menu baru."""
    # `payload` divalidasi oleh Pydantic sebelum masuk ke service.
    menu = service.create_menu(payload)
    return MenuResponse.from_orm(menu)


@router.patch("/{menu_id}", response_model=MenuResponse)
def update_menu(
    menu_id: int,
    payload: MenuUpdate,
    service: MenuService = Depends(get_menu_service),
) -> MenuResponse:
    """Update menu secara parsial berdasarkan id."""
    # Update parsial: hanya field yang dikirim client yang diproses.
    menu = service.update_menu(menu_id, payload)
    return MenuResponse.from_orm(menu)


@router.delete("/{menu_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_menu(
    menu_id: int, service: MenuService = Depends(get_menu_service)
) -> None:
    """Hapus menu berdasarkan id."""
    service.delete_menu(menu_id)
