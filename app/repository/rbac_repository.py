"""Lapisan akses data (repository) untuk entitas RBAC."""

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models import Permission as PermissionEntity
from app.models import Role as RoleEntity
from app.models import User as UserEntity
from app.models.roles_permission import (
    PermissionCreate,
    PermissionUpdate,
    RoleCreate,
    RoleUpdate,
)


class RBACRepository:
    """Repository untuk operasi database Role, Permission, dan relasinya."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def list_roles(self, skip: int, limit: int) -> list[RoleEntity]:
        query = (
            select(RoleEntity)
            .options(selectinload(RoleEntity.permissions))
            .order_by(RoleEntity.id)
            .offset(skip)
            .limit(limit)
        )
        return list(self.db.scalars(query).all())

    def get_role_by_id(self, role_id: int) -> RoleEntity | None:
        query = (
            select(RoleEntity)
            .where(RoleEntity.id == role_id)
            .options(selectinload(RoleEntity.permissions))
        )
        return self.db.scalar(query)

    def get_role_by_name(self, name: str) -> RoleEntity | None:
        return self.db.scalar(select(RoleEntity).where(RoleEntity.name == name))

    def create_role(self, payload: RoleCreate) -> RoleEntity:
        role = RoleEntity(**payload.dict())
        self.db.add(role)
        self.db.commit()
        self.db.refresh(role)
        return self.get_role_by_id(role.id)  # type: ignore[return-value]

    def update_role(self, role: RoleEntity, payload: RoleUpdate) -> RoleEntity:
        changes = payload.dict(exclude_unset=True)
        for field_name, value in changes.items():
            setattr(role, field_name, value)
        self.db.commit()
        return self.get_role_by_id(role.id)  # type: ignore[return-value]

    def delete_role(self, role: RoleEntity) -> None:
        self.db.delete(role)
        self.db.commit()

    def list_permissions(self, skip: int, limit: int) -> list[PermissionEntity]:
        query = (
            select(PermissionEntity)
            .options(selectinload(PermissionEntity.roles))
            .order_by(PermissionEntity.id)
            .offset(skip)
            .limit(limit)
        )
        return list(self.db.scalars(query).all())

    def get_permission_by_id(self, permission_id: int) -> PermissionEntity | None:
        query = (
            select(PermissionEntity)
            .where(PermissionEntity.id == permission_id)
            .options(selectinload(PermissionEntity.roles))
        )
        return self.db.scalar(query)

    def get_permission_by_code(self, code: str) -> PermissionEntity | None:
        return self.db.scalar(
            select(PermissionEntity).where(PermissionEntity.code == code)
        )

    def create_permission(self, payload: PermissionCreate) -> PermissionEntity:
        permission = PermissionEntity(**payload.dict())
        self.db.add(permission)
        self.db.commit()
        self.db.refresh(permission)
        return self.get_permission_by_id(permission.id)  # type: ignore[return-value]

    def update_permission(
        self, permission: PermissionEntity, payload: PermissionUpdate
    ) -> PermissionEntity:
        changes = payload.dict(exclude_unset=True)
        for field_name, value in changes.items():
            setattr(permission, field_name, value)
        self.db.commit()
        return self.get_permission_by_id(permission.id)  # type: ignore[return-value]

    def delete_permission(self, permission: PermissionEntity) -> None:
        self.db.delete(permission)
        self.db.commit()

    def get_user_with_roles(self, user_id: int) -> UserEntity | None:
        query = (
            select(UserEntity)
            .where(UserEntity.id == user_id)
            .options(selectinload(UserEntity.roles).selectinload(RoleEntity.permissions))
        )
        return self.db.scalar(query)

    def assign_role_to_user(self, user: UserEntity, role: RoleEntity) -> UserEntity:
        if role not in user.roles:
            user.roles.append(role)
            self.db.commit()
        return self.get_user_with_roles(user.id)  # type: ignore[return-value]

    def remove_role_from_user(self, user: UserEntity, role: RoleEntity) -> UserEntity:
        if role in user.roles:
            user.roles.remove(role)
            self.db.commit()
        return self.get_user_with_roles(user.id)  # type: ignore[return-value]

    def assign_permission_to_role(
        self, role: RoleEntity, permission: PermissionEntity
    ) -> RoleEntity:
        if permission not in role.permissions:
            role.permissions.append(permission)
            self.db.commit()
        return self.get_role_by_id(role.id)  # type: ignore[return-value]

    def remove_permission_from_role(
        self, role: RoleEntity, permission: PermissionEntity
    ) -> RoleEntity:
        if permission in role.permissions:
            role.permissions.remove(permission)
            self.db.commit()
        return self.get_role_by_id(role.id)  # type: ignore[return-value]
