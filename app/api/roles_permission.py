"""Endpoint CRUD role/permission dan relasi RBAC."""

from fastapi import APIRouter, Depends, Query, status

from app.models.roles_permission import (
    PermissionCreate,
    PermissionResponse,
    PermissionSummary,
    PermissionUpdate,
    RoleCreate,
    RolePermissionResponse,
    RoleResponse,
    RoleSummary,
    RoleUpdate,
    UserRoleResponse,
)
from app.service_container import get_rbac_service
from app.services.rbac_service import RBACService

router = APIRouter(prefix="/roles-permission", tags=["Roles & Permissions"])


@router.get("/roles", response_model=list[RoleResponse])
def list_roles(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
    service: RBACService = Depends(get_rbac_service),
) -> list[RoleResponse]:
    roles = service.list_roles(skip=skip, limit=limit)
    return [RoleResponse.from_orm(role) for role in roles]


@router.get("/roles/{role_id}", response_model=RoleResponse)
def get_role(role_id: int, service: RBACService = Depends(get_rbac_service)) -> RoleResponse:
    role = service.get_role(role_id)
    return RoleResponse.from_orm(role)


@router.post("/roles", response_model=RoleResponse, status_code=status.HTTP_201_CREATED)
def create_role(
    payload: RoleCreate, service: RBACService = Depends(get_rbac_service)
) -> RoleResponse:
    role = service.create_role(payload)
    return RoleResponse.from_orm(role)


@router.patch("/roles/{role_id}", response_model=RoleResponse)
def update_role(
    role_id: int,
    payload: RoleUpdate,
    service: RBACService = Depends(get_rbac_service),
) -> RoleResponse:
    role = service.update_role(role_id, payload)
    return RoleResponse.from_orm(role)


@router.delete("/roles/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_role(role_id: int, service: RBACService = Depends(get_rbac_service)) -> None:
    service.delete_role(role_id)


@router.get("/permissions", response_model=list[PermissionResponse])
def list_permissions(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
    service: RBACService = Depends(get_rbac_service),
) -> list[PermissionResponse]:
    permissions = service.list_permissions(skip=skip, limit=limit)
    return [PermissionResponse.from_orm(permission) for permission in permissions]


@router.get("/permissions/{permission_id}", response_model=PermissionResponse)
def get_permission(
    permission_id: int, service: RBACService = Depends(get_rbac_service)
) -> PermissionResponse:
    permission = service.get_permission(permission_id)
    return PermissionResponse.from_orm(permission)


@router.post(
    "/permissions",
    response_model=PermissionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_permission(
    payload: PermissionCreate,
    service: RBACService = Depends(get_rbac_service),
) -> PermissionResponse:
    permission = service.create_permission(payload)
    return PermissionResponse.from_orm(permission)


@router.patch("/permissions/{permission_id}", response_model=PermissionResponse)
def update_permission(
    permission_id: int,
    payload: PermissionUpdate,
    service: RBACService = Depends(get_rbac_service),
) -> PermissionResponse:
    permission = service.update_permission(permission_id, payload)
    return PermissionResponse.from_orm(permission)


@router.delete("/permissions/{permission_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_permission(
    permission_id: int, service: RBACService = Depends(get_rbac_service)
) -> None:
    service.delete_permission(permission_id)


@router.get("/users/{user_id}/roles", response_model=UserRoleResponse)
def get_user_roles(
    user_id: int, service: RBACService = Depends(get_rbac_service)
) -> UserRoleResponse:
    user = service.get_user_roles(user_id)
    return UserRoleResponse(
        user_id=user.id,
        roles=[RoleSummary.from_orm(role) for role in user.roles],
    )


@router.post("/users/{user_id}/roles/{role_id}", response_model=UserRoleResponse)
def assign_role_to_user(
    user_id: int,
    role_id: int,
    service: RBACService = Depends(get_rbac_service),
) -> UserRoleResponse:
    user = service.assign_role_to_user(user_id, role_id)
    return UserRoleResponse(
        user_id=user.id,
        roles=[RoleSummary.from_orm(role) for role in user.roles],
    )


@router.delete("/users/{user_id}/roles/{role_id}", response_model=UserRoleResponse)
def remove_role_from_user(
    user_id: int,
    role_id: int,
    service: RBACService = Depends(get_rbac_service),
) -> UserRoleResponse:
    user = service.remove_role_from_user(user_id, role_id)
    return UserRoleResponse(
        user_id=user.id,
        roles=[RoleSummary.from_orm(role) for role in user.roles],
    )


@router.get("/roles/{role_id}/permissions", response_model=RolePermissionResponse)
def get_role_permissions(
    role_id: int, service: RBACService = Depends(get_rbac_service)
) -> RolePermissionResponse:
    role = service.get_role_permissions(role_id)
    return RolePermissionResponse(
        role_id=role.id,
        permissions=[
            PermissionSummary.from_orm(permission) for permission in role.permissions
        ],
    )


@router.post(
    "/roles/{role_id}/permissions/{permission_id}",
    response_model=RolePermissionResponse,
)
def assign_permission_to_role(
    role_id: int,
    permission_id: int,
    service: RBACService = Depends(get_rbac_service),
) -> RolePermissionResponse:
    role = service.assign_permission_to_role(role_id, permission_id)
    return RolePermissionResponse(
        role_id=role.id,
        permissions=[
            PermissionSummary.from_orm(permission) for permission in role.permissions
        ],
    )


@router.delete(
    "/roles/{role_id}/permissions/{permission_id}",
    response_model=RolePermissionResponse,
)
def remove_permission_from_role(
    role_id: int,
    permission_id: int,
    service: RBACService = Depends(get_rbac_service),
) -> RolePermissionResponse:
    role = service.remove_permission_from_role(role_id, permission_id)
    return RolePermissionResponse(
        role_id=role.id,
        permissions=[
            PermissionSummary.from_orm(permission) for permission in role.permissions
        ],
    )
