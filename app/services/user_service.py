"""Lapisan business logic untuk operasi CRUD user."""

from fastapi import HTTPException, status
from passlib.context import CryptContext

from app.models import User as UserEntity
from app.models.user import UserCreate, UserUpdate
from app.repository.user_repository import UserRepository

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    """Service untuk validasi dan orkestrasi operasi user."""

    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    def list_users(self, skip: int, limit: int) -> list[UserEntity]:
        return self.repository.list(skip=skip, limit=limit)

    def get_user(self, user_id: int) -> UserEntity:
        user = self.repository.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        return user

    def create_user(self, payload: UserCreate) -> UserEntity:
        if self.repository.get_by_email(str(payload.email)):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email is already registered",
            )

        password_hash = pwd_context.hash(payload.password)
        return self.repository.create(payload=payload, password_hash=password_hash)

    def update_user(self, user_id: int, payload: UserUpdate) -> UserEntity:
        user = self.get_user(user_id)
        changes = payload.dict(exclude_unset=True)

        new_email = changes.get("email")
        if new_email:
            existing = self.repository.get_by_email(str(new_email))
            if existing and existing.id != user_id:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Email is already registered",
                )
            changes["email"] = str(new_email)

        new_password = changes.pop("password", None)
        if new_password:
            changes["password_hash"] = pwd_context.hash(new_password)

        return self.repository.update(user=user, changes=changes)

    def delete_user(self, user_id: int) -> None:
        user = self.get_user(user_id)
        self.repository.delete(user)
