from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    roles: Mapped[list["Role"]] = relationship(
        secondary="user_roles", back_populates="users", lazy="selectin"
    )


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80), unique=True, nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    users: Mapped[list[User]] = relationship(
        secondary="user_roles", back_populates="roles", lazy="selectin"
    )
    permissions: Mapped[list["Permission"]] = relationship(
        secondary="role_permissions", back_populates="roles", lazy="selectin"
    )


class Permission(Base):
    __tablename__ = "permissions"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(120), unique=True, nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    roles: Mapped[list[Role]] = relationship(
        secondary="role_permissions", back_populates="permissions", lazy="selectin"
    )


class RolePermission(Base):
    __tablename__ = "role_permissions"

    role_id: Mapped[int] = mapped_column(
        ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True
    )
    permission_id: Mapped[int] = mapped_column(
        ForeignKey("permissions.id", ondelete="CASCADE"), primary_key=True
    )


class UserRole(Base):
    __tablename__ = "user_roles"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    role_id: Mapped[int] = mapped_column(
        ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True
    )


class Menu(Base):
    __tablename__ = "menus"

    id: Mapped[int] = mapped_column(primary_key=True)
    menu_key: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    section_title: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    parent_id: Mapped[int | None] = mapped_column(
        ForeignKey("menus.id", ondelete="CASCADE"), nullable=True, index=True
    )
    label: Mapped[str] = mapped_column(String(120), nullable=False)
    href: Mapped[str | None] = mapped_column(String(255), nullable=True)
    icon: Mapped[str | None] = mapped_column(String(80), nullable=True)
    list_id: Mapped[str | None] = mapped_column(String(120), nullable=True)
    badge_text: Mapped[str | None] = mapped_column(String(50), nullable=True)
    badge_class_name: Mapped[str | None] = mapped_column(String, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_hidden: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    show_more_toggle: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    initially_open: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    depth: Mapped[int] = mapped_column(default=0, nullable=False)
    sort_order: Mapped[int] = mapped_column(default=0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )
