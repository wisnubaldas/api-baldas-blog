"""Endpoint CRUD user berbasis FastAPI."""

from fastapi import APIRouter, Depends, Query, status

from app.models.user import UserCreate, UserResponse, UserUpdate
from app.service_container import get_user_service
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
