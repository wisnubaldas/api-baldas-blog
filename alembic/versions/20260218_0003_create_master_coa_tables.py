"""create master coa tables

Revision ID: 20260218_0003
Revises: 20260212_0002
Create Date: 2026-02-18 00:00:03.000000
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "20260218_0003"
down_revision = "20260212_0002"
branch_labels = None
depends_on = None


account_type_enum = sa.Enum(
    "ASSET",
    "LIABILITY",
    "EQUITY",
    "REVENUE",
    "EXPENSE",
    name="fin_coa_account_type_enum",
    native_enum=False,
)

normal_balance_enum = sa.Enum(
    "DEBIT",
    "CREDIT",
    name="fin_coa_normal_balance_enum",
    native_enum=False,
)

dimension_type_enum = sa.Enum(
    "COST_CENTER",
    "PROJECT",
    "BRANCH",
    name="fin_coa_dimension_type_enum",
    native_enum=False,
)


def upgrade() -> None:
    op.create_table(
        "fin_coa_accounts",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("code", sa.String(length=50), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("account_type", account_type_enum, nullable=False),
        sa.Column("category", sa.String(length=80), nullable=False),
        sa.Column("parent_id", sa.Integer(), nullable=True),
        sa.Column("level", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("path", sa.String(length=500), nullable=True),
        sa.Column(
            "is_postable", sa.Boolean(), nullable=False, server_default=sa.false()
        ),
        sa.Column("normal_balance", normal_balance_enum, nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.ForeignKeyConstraint(
            ["parent_id"], ["fin_coa_accounts.id"], ondelete="RESTRICT"
        ),
        sa.UniqueConstraint("code", name="uq_fin_coa_accounts_code"),
    )
    op.create_index(
        "ix_fin_coa_accounts_code", "fin_coa_accounts", ["code"], unique=False
    )
    op.create_index(
        "ix_fin_coa_accounts_parent_id", "fin_coa_accounts", ["parent_id"], unique=False
    )
    op.create_index(
        "ix_fin_coa_accounts_account_type",
        "fin_coa_accounts",
        ["account_type"],
        unique=False,
    )
    op.create_index(
        "ix_fin_coa_accounts_category", "fin_coa_accounts", ["category"], unique=False
    )

    op.create_table(
        "fin_coa_dimensions",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("code", sa.String(length=50), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("dimension_type", dimension_type_enum, nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.UniqueConstraint("code", name="uq_fin_coa_dimensions_code"),
    )
    op.create_index(
        "ix_fin_coa_dimensions_code", "fin_coa_dimensions", ["code"], unique=False
    )
    op.create_index(
        "ix_fin_coa_dimensions_dimension_type",
        "fin_coa_dimensions",
        ["dimension_type"],
        unique=False,
    )

    op.create_table(
        "fin_coa_account_settings",
        sa.Column("account_id", sa.Integer(), nullable=False),
        sa.Column(
            "require_cost_center",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false(),
        ),
        sa.Column(
            "require_vendor", sa.Boolean(), nullable=False, server_default=sa.false()
        ),
        sa.Column(
            "require_customer", sa.Boolean(), nullable=False, server_default=sa.false()
        ),
        sa.ForeignKeyConstraint(
            ["account_id"], ["fin_coa_accounts.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("account_id", name="pk_fin_coa_account_settings"),
    )


def downgrade() -> None:
    op.drop_table("fin_coa_account_settings")

    op.drop_index(
        "ix_fin_coa_dimensions_dimension_type", table_name="fin_coa_dimensions"
    )
    op.drop_index("ix_fin_coa_dimensions_code", table_name="fin_coa_dimensions")
    op.drop_table("fin_coa_dimensions")

    op.drop_index("ix_fin_coa_accounts_category", table_name="fin_coa_accounts")
    op.drop_index("ix_fin_coa_accounts_account_type", table_name="fin_coa_accounts")
    op.drop_index("ix_fin_coa_accounts_parent_id", table_name="fin_coa_accounts")
    op.drop_index("ix_fin_coa_accounts_code", table_name="fin_coa_accounts")
    op.drop_table("fin_coa_accounts")
