"""Lapisan business logic untuk operasi RBAC."""

from fastapi import HTTPException, status

from app.models import Permission as PermissionEntity
from app.models import Role as RoleEntity
from app.models import User as UserEntity
from app.models.roles_permission import (
    PermissionCreate,
    PermissionUpdate,
    RoleCreate,
    RoleUpdate,
)
from app.repository.rbac_repository import RBACRepository


class RBACService:
    """Service untuk validasi dan orkestrasi operasi RBAC."""

    def __init__(self, repository: RBACRepository) -> None:
        self.repository = repository

    def list_roles(self, skip: int, limit: int) -> list[RoleEntity]:
        return self.repository.list_roles(skip=skip, limit=limit)

    def get_role(self, role_id: int) -> RoleEntity:
        role = self.repository.get_role_by_id(role_id)
        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Role not found"
            )
        return role

    def create_role(self, payload: RoleCreate) -> RoleEntity:
        if self.repository.get_role_by_name(payload.name):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Role name already exists",
            )
        return self.repository.create_role(payload)

    def update_role(self, role_id: int, payload: RoleUpdate) -> RoleEntity:
        role = self.get_role(role_id)
        changes = payload.dict(exclude_unset=True)
        new_name = changes.get("name")
        if new_name:
            existing = self.repository.get_role_by_name(new_name)
            if existing and existing.id != role_id:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Role name already exists",
                )
        return self.repository.update_role(role, payload)

    def delete_role(self, role_id: int) -> None:
        role = self.get_role(role_id)
        self.repository.delete_role(role)

    def list_permissions(self, skip: int, limit: int) -> list[PermissionEntity]:
        return self.repository.list_permissions(skip=skip, limit=limit)

    def get_permission(self, permission_id: int) -> PermissionEntity:
        permission = self.repository.get_permission_by_id(permission_id)
        if not permission:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Permission not found"
            )
        return permission

    def create_permission(self, payload: PermissionCreate) -> PermissionEntity:
        if self.repository.get_permission_by_code(payload.code):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Permission code already exists",
            )
        return self.repository.create_permission(payload)

    def update_permission(
        self, permission_id: int, payload: PermissionUpdate
    ) -> PermissionEntity:
        permission = self.get_permission(permission_id)
        changes = payload.dict(exclude_unset=True)
        new_code = changes.get("code")
        if new_code:
            existing = self.repository.get_permission_by_code(new_code)
            if existing and existing.id != permission_id:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Permission code already exists",
                )
        return self.repository.update_permission(permission, payload)

    def delete_permission(self, permission_id: int) -> None:
        permission = self.get_permission(permission_id)
        self.repository.delete_permission(permission)

    def get_user_roles(self, user_id: int) -> UserEntity:
        user = self.repository.get_user_with_roles(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        return user

    def assign_role_to_user(self, user_id: int, role_id: int) -> UserEntity:
        user = self.get_user_roles(user_id)
        role = self.get_role(role_id)
        return self.repository.assign_role_to_user(user, role)

    def remove_role_from_user(self, user_id: int, role_id: int) -> UserEntity:
        user = self.get_user_roles(user_id)
        role = self.get_role(role_id)
        if role not in user.roles:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Role assignment not found for user",
            )
        return self.repository.remove_role_from_user(user, role)

    def get_role_permissions(self, role_id: int) -> RoleEntity:
        return self.get_role(role_id)

    def assign_permission_to_role(self, role_id: int, permission_id: int) -> RoleEntity:
        role = self.get_role(role_id)
        permission = self.get_permission(permission_id)
        return self.repository.assign_permission_to_role(role, permission)

    def remove_permission_from_role(
        self, role_id: int, permission_id: int
    ) -> RoleEntity:
        role = self.get_role(role_id)
        permission = self.get_permission(permission_id)
        if permission not in role.permissions:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Permission assignment not found for role",
            )
        return self.repository.remove_permission_from_role(role, permission)
