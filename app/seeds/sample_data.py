import re
from typing import Any

from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Menu, Permission, Role, User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

MENU_SECTIONS: list[dict[str, Any]] = [
    {
        "title": "Main",
        "items": [
            {
                "label": "Dashboard",
                "icon": "dashboard",
                "badge": {
                    "text": "30",
                    "className": "rounded-full font-medium inline-block text-center w-[20px] h-[20px] text-[11px] leading-[20px] text-orange-500 bg-orange-50 dark:bg-[#ffffff14] ltr:ml-auto rtl:mr-auto",
                },
                "listId": "dashboardItemsList",
                "showMoreToggle": True,
                "children": [
                    {"label": "Blank Page", "href": "/", "active": False},
                    {"label": "Dashboard Pengunjung", "href": "/dashboard-contoh"},
                    {"label": "eCommerce", "href": "#"},
                    {"label": "CRM", "href": "#"},
                    {"label": "Project Management", "href": "#"},
                    {"label": "LMS", "href": "#"},
                    {
                        "label": "HelpDesk",
                        "href": "#",
                        "badge": {
                            "text": "Hot",
                            "className": "text-[10px] font-medium py-[1px] px-[8px] ltr:ml-[8px] rtl:mr-[8px] text-orange-500 bg-orange-100 dark:bg-[#ffffff14] inline-block rounded-sm",
                        },
                    },
                    {"label": "Analytics", "href": "#"},
                    {"label": "Crypto", "href": "#"},
                    {"label": "Sales", "href": "#"},
                    {"label": "Hospital", "href": "#"},
                    {"label": "HRM", "href": "#", "hidden": True},
                    {"label": "School", "href": "#", "hidden": True},
                    {
                        "label": "Call Center",
                        "href": "#",
                        "hidden": True,
                        "badge": {
                            "text": "Popular",
                            "className": "text-[10px] font-medium py-[1px] px-[8px] ltr:ml-[8px] rtl:mr-[8px] text-success-600 bg-success-100 dark:bg-[#ffffff14] inline-block rounded-sm",
                        },
                    },
                    {
                        "label": "Real Estate",
                        "href": "#",
                        "hidden": True,
                        "badge": {
                            "text": "Top",
                            "className": "text-[10px] font-medium py-[1px] px-[8px] ltr:ml-[8px] rtl:mr-[8px] text-purple-500 bg-purple-100 dark:bg-[#ffffff14] inline-block rounded-sm",
                        },
                    },
                ],
            },
            {
                "label": "Extra Pages",
                "icon": "content_copy",
                "active": True,
                "initiallyOpen": True,
                "children": [
                    {"label": "Pricing", "href": "#"},
                    {"label": "Timeline", "href": "#"},
                    {"label": "FAQ", "href": "#"},
                    {"label": "Gallery", "href": "#"},
                    {"label": "Testimonials", "href": "#"},
                    {"label": "Search", "href": "#"},
                    {"label": "Coming Soon", "href": "#"},
                ],
            },
            {
                "label": "Errors",
                "icon": "error",
                "children": [
                    {"label": "404 Error Page", "href": "#"},
                    {"label": "Internal Error", "href": "#"},
                ],
            },
            {"label": "Widgets", "icon": "widgets", "href": "#"},
            {"label": "Maps", "icon": "map", "href": "#"},
            {"label": "Notifications", "icon": "notifications", "href": "#"},
            {"label": "Members", "icon": "people", "href": "#"},
        ],
    },
    {
        "title": "Others",
        "items": [
            {"label": "My Profile", "icon": "account_circle", "href": "#"},
            {
                "label": "Settings",
                "icon": "settings",
                "children": [
                    {"label": "Account Settings", "href": "#"},
                    {"label": "Change Password", "href": "#"},
                    {"label": "Connections", "href": "#"},
                    {"label": "Privacy Policy", "href": "#"},
                    {"label": "Terms & Conditions", "href": "#"},
                ],
            },
            {"label": "Logout", "icon": "logout", "href": "#"},
        ],
    },
]


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


def _slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def _upsert_menu(
    db: Session,
    *,
    menu_key: str,
    section_title: str,
    parent_id: int | None,
    label: str,
    href: str | None,
    icon: str | None,
    list_id: str | None,
    badge_text: str | None,
    badge_class_name: str | None,
    is_active: bool,
    is_hidden: bool,
    show_more_toggle: bool,
    initially_open: bool,
    depth: int,
    sort_order: int,
) -> Menu:
    menu = db.scalar(select(Menu).where(Menu.menu_key == menu_key))
    if not menu:
        menu = Menu(
            menu_key=menu_key,
            section_title=section_title,
            parent_id=parent_id,
            label=label,
            href=href,
            icon=icon,
            list_id=list_id,
            badge_text=badge_text,
            badge_class_name=badge_class_name,
            is_active=is_active,
            is_hidden=is_hidden,
            show_more_toggle=show_more_toggle,
            initially_open=initially_open,
            depth=depth,
            sort_order=sort_order,
        )
        db.add(menu)
    else:
        menu.section_title = section_title
        menu.parent_id = parent_id
        menu.label = label
        menu.href = href
        menu.icon = icon
        menu.list_id = list_id
        menu.badge_text = badge_text
        menu.badge_class_name = badge_class_name
        menu.is_active = is_active
        menu.is_hidden = is_hidden
        menu.show_more_toggle = show_more_toggle
        menu.initially_open = initially_open
        menu.depth = depth
        menu.sort_order = sort_order

    db.flush()
    return menu


def _seed_menu_items(
    db: Session,
    *,
    section_title: str,
    items: list[dict[str, Any]],
    key_prefix: str,
    parent_id: int | None = None,
    depth: int = 0,
) -> None:
    for index, item in enumerate(items):
        badge = item.get("badge") or {}
        label = item["label"]
        item_slug = _slugify(label)
        menu_key = f"{key_prefix}.{index}-{item_slug}"

        menu = _upsert_menu(
            db,
            menu_key=menu_key,
            section_title=section_title,
            parent_id=parent_id,
            label=label,
            href=item.get("href"),
            icon=item.get("icon"),
            list_id=item.get("listId"),
            badge_text=badge.get("text"),
            badge_class_name=badge.get("className"),
            is_active=bool(item.get("active", False)),
            is_hidden=bool(item.get("hidden", False)),
            show_more_toggle=bool(item.get("showMoreToggle", False)),
            initially_open=bool(item.get("initiallyOpen", False)),
            depth=depth,
            sort_order=index,
        )

        children = item.get("children") or []
        if children:
            _seed_menu_items(
                db,
                section_title=section_title,
                items=children,
                key_prefix=menu_key,
                parent_id=menu.id,
                depth=depth + 1,
            )


def _seed_menus(db: Session) -> None:
    for section in MENU_SECTIONS:
        section_title = section["title"]
        _seed_menu_items(
            db,
            section_title=section_title,
            items=section["items"],
            key_prefix=_slugify(section_title),
        )


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
    writer_role.permissions = [
        permission_map["posts.read"],
        permission_map["posts.create"],
    ]

    admin_user = _get_or_create_user(db, "Admin Baldas", "admin@baldas.dev", "admin123")
    editor_user = _get_or_create_user(
        db, "Editor Baldas", "editor@baldas.dev", "editor123"
    )
    writer_user = _get_or_create_user(
        db, "Writer Baldas", "writer@baldas.dev", "writer123"
    )

    admin_user.roles = [admin_role]
    editor_user.roles = [editor_role]
    writer_user.roles = [writer_role]

    _seed_menus(db)

    db.commit()
