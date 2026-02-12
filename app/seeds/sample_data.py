from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Permission, Role, User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def _get_or_create_role(db: Session, name: str, description: str) -> Role:
    role = db.scalar(select(Role).where(Role.name == name))
    if role:
        return role
    role = Role(name=name, description=description)
    db.add(role)
    db.flush()
    return role


def _get_or_create_permission(db: Session, code: str, description: str) -> Permission:
    permission = db.scalar(select(Permission).where(Permission.code == code))
    if permission:
        return permission
    permission = Permission(code=code, description=description)
    db.add(permission)
    db.flush()
    return permission


def _get_or_create_user(db: Session, full_name: str, email: str, password: str) -> User:
    user = db.scalar(select(User).where(User.email == email))
    if user:
        return user
    user = User(
        full_name=full_name,
        email=email,
        password_hash=pwd_context.hash(password),
        is_active=True,
    )
    db.add(user)
    db.flush()
    return user


def run_seed(db: Session) -> None:
    permissions = {
        "posts.read": "Read posts",
        "posts.create": "Create posts",
        "posts.update": "Update posts",
        "posts.delete": "Delete posts",
        "users.manage": "Manage users",
    }
    permission_map = {
        code: _get_or_create_permission(db, code, description)
        for code, description in permissions.items()
    }

    admin_role = _get_or_create_role(db, "admin", "Full system access")
    editor_role = _get_or_create_role(db, "editor", "Edit and publish content")
    writer_role = _get_or_create_role(db, "writer", "Write and manage own content")

    admin_role.permissions = list(permission_map.values())
    editor_role.permissions = [
        permission_map["posts.read"],
        permission_map["posts.create"],
        permission_map["posts.update"],
    ]
    writer_role.permissions = [permission_map["posts.read"], permission_map["posts.create"]]

    admin_user = _get_or_create_user(
        db, "Admin Baldas", "admin@baldas.dev", "admin123"
    )
    editor_user = _get_or_create_user(
        db, "Editor Baldas", "editor@baldas.dev", "editor123"
    )
    writer_user = _get_or_create_user(
        db, "Writer Baldas", "writer@baldas.dev", "writer123"
    )

    admin_user.roles = [admin_role]
    editor_user.roles = [editor_role]
    writer_user.roles = [writer_role]

    db.commit()

