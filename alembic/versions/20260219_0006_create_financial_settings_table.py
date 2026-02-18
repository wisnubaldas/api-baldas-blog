"""create financial settings table

Revision ID: 20260219_0006
Revises: 20260219_0005
Create Date: 2026-02-19 00:00:06.000000
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "20260219_0006"
down_revision = "20260219_0005"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "fin_settings",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("ar_control_account_id", sa.Integer(), nullable=True),
        sa.Column("ap_control_account_id", sa.Integer(), nullable=True),
        sa.Column(
            "default_currency",
            sa.String(length=3),
            nullable=False,
            server_default="IDR",
        ),
        sa.Column(
            "default_payment_terms_days",
            sa.Integer(),
            nullable=False,
            server_default="0",
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
            ["ar_control_account_id"], ["fin_coa_accounts.id"], ondelete="SET NULL"
        ),
        sa.ForeignKeyConstraint(
            ["ap_control_account_id"], ["fin_coa_accounts.id"], ondelete="SET NULL"
        ),
    )


def downgrade() -> None:
    op.drop_table("fin_settings")
