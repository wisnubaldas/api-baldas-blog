"""Master Vendor model."""

from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Vendor(Base):
    """Master data untuk vendor/supplier - Minimum Viable:

    - code (unique identifier)
    - legal_name (business name)
    - entity_type (COMPANY/INDIVIDUAL)
    - tax_id & is_pkp (tax compliance)
    - contact_person, email, phone (primary contact)
    - street_address, city, province, country, postal_code (billing address)
    - payment_terms_days & payment_methods (payment config)
    - ap_control_account_id (AP integration)
    - is_active (status)
    """

    __tablename__ = "fin_vendors"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False, index=True
    )
    legal_name: Mapped[str] = mapped_column(String(255), nullable=False)
    entity_type: Mapped[str] = mapped_column(
        Enum("COMPANY", "INDIVIDUAL", name="vendor_entity_type"),
        default="COMPANY",
        nullable=False,
    )
    tax_id: Mapped[str | None] = mapped_column(String(50), nullable=True, unique=True)
    is_pkp: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Contact & Address
    contact_person: Mapped[str | None] = mapped_column(String(120), nullable=True)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    website: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # Address (main)
    street_address: Mapped[str | None] = mapped_column(String(255), nullable=True)
    city: Mapped[str | None] = mapped_column(String(100), nullable=True)
    province: Mapped[str | None] = mapped_column(String(100), nullable=True)
    country: Mapped[str | None] = mapped_column(
        String(100), default="Indonesia", nullable=True
    )
    postal_code: Mapped[str | None] = mapped_column(String(20), nullable=True)

    # Financial
    default_currency: Mapped[str] = mapped_column(
        String(3), default="IDR", nullable=False
    )
    payment_terms_days: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    payment_methods: Mapped[str | None] = mapped_column(
        String(255), nullable=True
    )  # BANK_TRANSFER, CASH, etc.
    bank_account: Mapped[str | None] = mapped_column(String(50), nullable=True)
    bank_name: Mapped[str | None] = mapped_column(String(120), nullable=True)
    ap_control_account_id: Mapped[int | None] = mapped_column(
        ForeignKey("fin_coa_accounts.id"), nullable=True
    )
    tax_withholding_pct: Mapped[float | None] = mapped_column(
        Numeric(5, 2), nullable=True
    )

    # Control
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False, index=True
    )
    is_blacklist: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
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
    ap_control_account: Mapped["COAAccount | None"] = relationship(
        foreign_keys=[ap_control_account_id],
        lazy="selectin",
    )
