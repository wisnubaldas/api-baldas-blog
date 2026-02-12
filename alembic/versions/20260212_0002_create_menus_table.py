"""create menus table

Revision ID: 20260212_0002
Revises: 20260212_0001
Create Date: 2026-02-12 00:00:02.000000
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "20260212_0002"
down_revision = "20260212_0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "menus",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("menu_key", sa.String(length=255), nullable=False),
        sa.Column("section_title", sa.String(length=80), nullable=False),
        sa.Column("parent_id", sa.Integer(), nullable=True),
        sa.Column("label", sa.String(length=120), nullable=False),
        sa.Column("href", sa.String(length=255), nullable=True),
        sa.Column("icon", sa.String(length=80), nullable=True),
        sa.Column("list_id", sa.String(length=120), nullable=True),
        sa.Column("badge_text", sa.String(length=50), nullable=True),
        sa.Column("badge_class_name", sa.Text(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("is_hidden", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("show_more_toggle", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("initially_open", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("depth", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("sort_order", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(["parent_id"], ["menus.id"], ondelete="CASCADE"),
        sa.UniqueConstraint("menu_key", name="uq_menus_menu_key"),
    )
    op.create_index("ix_menus_menu_key", "menus", ["menu_key"], unique=False)
    op.create_index("ix_menus_parent_id", "menus", ["parent_id"], unique=False)
    op.create_index("ix_menus_section_title", "menus", ["section_title"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_menus_section_title", table_name="menus")
    op.drop_index("ix_menus_parent_id", table_name="menus")
    op.drop_index("ix_menus_menu_key", table_name="menus")
    op.drop_table("menus")

