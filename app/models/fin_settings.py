"""Financial Settings model - Singleton for AR/AP control accounts."""

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class FinancialSettings(Base):
    """Global finance settings (singleton pattern) - Minimum Viable:

    - ar_control_account_id (Maps to COA 1200 - Accounts Receivable)
    - ap_control_account_id (Maps to COA 2100 - Accounts Payable)
    - default_currency (primary currency)
    - default_payment_terms_days (global default)

    Note: Only one record should exist in this table (singleton pattern).
          Use: settings = db.query(FinancialSettings).first() or db.query(FinancialSettings).one()
    """

    __tablename__ = "fin_settings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    # AR/AP Control Accounts - Critical for automatic journal posting
    ar_control_account_id: Mapped[int | None] = mapped_column(
        ForeignKey("fin_coa_accounts.id"), nullable=True
    )
    ap_control_account_id: Mapped[int | None] = mapped_column(
        ForeignKey("fin_coa_accounts.id"), nullable=True
    )

    # Default settings
    default_currency: Mapped[str] = mapped_column(
        String(3), default="IDR", nullable=False
    )
    default_payment_terms_days: Mapped[int] = mapped_column(
        Integer, default=0, nullable=False
    )

    # Control
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # Relationships
    ar_control_account: Mapped["COAAccount | None"] = relationship(
        foreign_keys=[ar_control_account_id],
        lazy="selectin",
    )
    ap_control_account: Mapped["COAAccount | None"] = relationship(
        foreign_keys=[ap_control_account_id],
        lazy="selectin",
    )
