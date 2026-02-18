"""create master vendor table

Revision ID: 20260219_0004
Revises: 20260218_0003
Create Date: 2026-02-19 00:00:04.000000
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "20260219_0004"
down_revision = "20260218_0003"
branch_labels = None
depends_on = None

vendor_entity_type_enum = sa.Enum(
    "COMPANY",
    "INDIVIDUAL",
    name="vendor_entity_type",
    native_enum=False,
)


def upgrade() -> None:
    op.create_table(
        "fin_vendors",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("code", sa.String(length=50), nullable=False, unique=True),
        sa.Column("legal_name", sa.String(length=255), nullable=False),
        sa.Column(
            "entity_type",
            vendor_entity_type_enum,
            nullable=False,
            server_default="COMPANY",
        ),
        sa.Column("tax_id", sa.String(length=50), nullable=True, unique=True),
        sa.Column("is_pkp", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("contact_person", sa.String(length=120), nullable=True),
        sa.Column("email", sa.String(length=255), nullable=True),
        sa.Column("phone", sa.String(length=20), nullable=True),
        sa.Column("website", sa.String(length=255), nullable=True),
        sa.Column("street_address", sa.String(length=255), nullable=True),
        sa.Column("city", sa.String(length=100), nullable=True),
        sa.Column("province", sa.String(length=100), nullable=True),
        sa.Column(
            "country", sa.String(length=100), nullable=True, server_default="Indonesia"
        ),
        sa.Column("postal_code", sa.String(length=20), nullable=True),
        sa.Column(
            "default_currency",
            sa.String(length=3),
            nullable=False,
            server_default="IDR",
        ),
        sa.Column(
            "payment_terms_days", sa.Integer(), nullable=False, server_default="0"
        ),
        sa.Column("payment_methods", sa.String(length=255), nullable=True),
        sa.Column("bank_account", sa.String(length=50), nullable=True),
        sa.Column("bank_name", sa.String(length=120), nullable=True),
        sa.Column("ap_control_account_id", sa.Integer(), nullable=True),
        sa.Column(
            "tax_withholding_pct", sa.Numeric(precision=5, scale=2), nullable=True
        ),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column(
            "is_blacklist", sa.Boolean(), nullable=False, server_default=sa.false()
        ),
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
            ["ap_control_account_id"], ["fin_coa_accounts.id"], ondelete="SET NULL"
        ),
    )
    op.create_index("ix_fin_vendors_code", "fin_vendors", ["code"], unique=False)
    op.create_index("ix_fin_vendors_email", "fin_vendors", ["email"], unique=False)
    op.create_index(
        "ix_fin_vendors_is_active", "fin_vendors", ["is_active"], unique=False
    )


def downgrade() -> None:
    op.drop_index("ix_fin_vendors_is_active", table_name="fin_vendors")
    op.drop_index("ix_fin_vendors_email", table_name="fin_vendors")
    op.drop_index("ix_fin_vendors_code", table_name="fin_vendors")
    op.drop_table("fin_vendors")
