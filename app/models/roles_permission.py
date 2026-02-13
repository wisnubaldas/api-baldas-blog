"""Schema request/response untuk endpoint Role dan Permission."""

from datetime import datetime

from pydantic import BaseModel, Field


class RoleCreate(BaseModel):
    """Payload untuk membuat role baru."""

    name: str = Field(min_length=2, max_length=80)
    description: str | None = Field(default=None, max_length=255)


class RoleUpdate(BaseModel):
    """Payload untuk update role secara parsial."""

    name: str | None = Field(default=None, min_length=2, max_length=80)
    description: str | None = Field(default=None, max_length=255)


class PermissionCreate(BaseModel):
    """Payload untuk membuat permission baru."""

    code: str = Field(min_length=2, max_length=120)
    description: str | None = Field(default=None, max_length=255)


class PermissionUpdate(BaseModel):
    """Payload untuk update permission secara parsial."""

    code: str | None = Field(default=None, min_length=2, max_length=120)
    description: str | None = Field(default=None, max_length=255)


class RoleSummary(BaseModel):
    """Representasi ringkas role."""

    id: int
    name: str
    description: str | None = None

    class Config:
        orm_mode = True


class PermissionSummary(BaseModel):
    """Representasi ringkas permission."""

    id: int
    code: str
    description: str | None = None

    class Config:
        orm_mode = True


class RoleResponse(BaseModel):
    """Representasi role lengkap beserta daftar permission."""

    id: int
    name: str
    description: str | None = None
    created_at: datetime
    updated_at: datetime
    permissions: list[PermissionSummary] = []

    class Config:
        orm_mode = True


class PermissionResponse(BaseModel):
    """Representasi permission lengkap beserta daftar role."""

    id: int
    code: str
    description: str | None = None
    created_at: datetime
    roles: list[RoleSummary] = []

    class Config:
        orm_mode = True


class UserRoleResponse(BaseModel):
    """Representasi daftar role yang dimiliki user."""

    user_id: int
    roles: list[RoleSummary]


class RolePermissionResponse(BaseModel):
    """Representasi daftar permission yang dimiliki role."""

    role_id: int
    permissions: list[PermissionSummary]
