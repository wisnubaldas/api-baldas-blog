"""Lapisan akses data (repository) untuk entitas user."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import User as UserEntity
from app.models.user import UserCreate


class UserRepository:
    """Repository untuk operasi database tabel users."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def list(self, skip: int, limit: int) -> list[UserEntity]:
        query = select(UserEntity).order_by(UserEntity.id).offset(skip).limit(limit)
        return list(self.db.scalars(query).all())

    def get_by_id(self, user_id: int) -> UserEntity | None:
        return self.db.get(UserEntity, user_id)

    def get_by_email(self, email: str) -> UserEntity | None:
        return self.db.scalar(select(UserEntity).where(UserEntity.email == email))

    def create(self, payload: UserCreate, password_hash: str) -> UserEntity:
        user = UserEntity(
            full_name=payload.full_name,
            email=str(payload.email),
            password_hash=password_hash,
            is_active=payload.is_active,
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update(self, user: UserEntity, changes: dict[str, object]) -> UserEntity:
        for field_name, value in changes.items():
            setattr(user, field_name, value)
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete(self, user: UserEntity) -> None:
        self.db.delete(user)
        self.db.commit()
