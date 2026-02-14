"""Endpoint CRUD user berbasis FastAPI."""

from fastapi import APIRouter, Depends, Query, Request, status
from sqlalchemy import select

from app.models import User as UserEntity
from app.models.user import UserCreate, UserResponse, UserUpdate
from app.service_container import get_datatables_service, get_user_service
from app.services.datatables_service import DataTablesService
from app.services.user_service import UserService

router = APIRouter(prefix="/user", tags=["User"])


@router.get("/", response_model=list[UserResponse])
def list_users(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
    service: UserService = Depends(get_user_service),
) -> list[UserResponse]:
    users = service.list_users(skip=skip, limit=limit)
    return [UserResponse.from_orm(user) for user in users]


@router.get("/datatables")
def list_users_datatables(
    request: Request,
    datatables_service: DataTablesService = Depends(get_datatables_service),
) -> dict:
    base_query = select(UserEntity)

    searchable_columns = {
        "id": UserEntity.id,
        "full_name": UserEntity.full_name,
        "email": UserEntity.email,
        "is_active": UserEntity.is_active,
        "created_at": UserEntity.created_at,
    }
    orderable_columns = {
        "id": UserEntity.id,
        "full_name": UserEntity.full_name,
        "email": UserEntity.email,
        "is_active": UserEntity.is_active,
        "created_at": UserEntity.created_at,
    }

    return datatables_service.build_response(
        base_query=base_query,
        query_params=request.query_params,
        searchable_columns=searchable_columns,
        orderable_columns=orderable_columns,
        default_order_column="id",
        default_order_direction="desc",
        row_mapper=lambda row: {
            "id": row.id,
            "full_name": row.full_name,
            "email": row.email,
            "is_active": row.is_active,
            "created_at": row.created_at.isoformat() if row.created_at else None,
        },
    )


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int, service: UserService = Depends(get_user_service)
) -> UserResponse:
    user = service.get_user(user_id)
    return UserResponse.from_orm(user)


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    payload: UserCreate,
    service: UserService = Depends(get_user_service),
) -> UserResponse:
    user = service.create_user(payload)
    return UserResponse.from_orm(user)


@router.patch("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    payload: UserUpdate,
    service: UserService = Depends(get_user_service),
) -> UserResponse:
    user = service.update_user(user_id, payload)
    return UserResponse.from_orm(user)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int, service: UserService = Depends(get_user_service)
) -> None:
    service.delete_user(user_id)
