"""Master Customer model."""

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


class Customer(Base):
    """Master data untuk customer/pelanggan - Minimum Viable:

    - code (unique identifier)
    - legal_name (business name)
    - entity_type (COMPANY/INDIVIDUAL)
    - tax_id & is_pkp (tax compliance)
    - contact_person, email, phone (primary contact)
    - billing_street, billing_city, billing_province, billing_country, billing_postal_code
    - shipping_street, shipping_city, shipping_province, shipping_country, shipping_postal_code (optional)
    - credit_limit (receivables management)
    - payment_terms_days (payment config)
    - ar_control_account_id (AR integration)
    - tax_classification & is_active (status)
    """

    __tablename__ = "fin_customers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False, index=True
    )
    legal_name: Mapped[str] = mapped_column(String(255), nullable=False)
    entity_type: Mapped[str] = mapped_column(
        Enum("COMPANY", "INDIVIDUAL", name="customer_entity_type"),
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

    # Billing Address (main)
    billing_street: Mapped[str | None] = mapped_column(String(255), nullable=True)
    billing_city: Mapped[str | None] = mapped_column(String(100), nullable=True)
    billing_province: Mapped[str | None] = mapped_column(String(100), nullable=True)
    billing_country: Mapped[str | None] = mapped_column(
        String(100), default="Indonesia", nullable=True
    )
    billing_postal_code: Mapped[str | None] = mapped_column(String(20), nullable=True)

    # Shipping Address (optional, defaults to billing if not set)
    shipping_street: Mapped[str | None] = mapped_column(String(255), nullable=True)
    shipping_city: Mapped[str | None] = mapped_column(String(100), nullable=True)
    shipping_province: Mapped[str | None] = mapped_column(String(100), nullable=True)
    shipping_country: Mapped[str | None] = mapped_column(String(100), nullable=True)
    shipping_postal_code: Mapped[str | None] = mapped_column(String(20), nullable=True)

    # Financial
    default_currency: Mapped[str] = mapped_column(
        String(3), default="IDR", nullable=False
    )
    credit_limit: Mapped[float] = mapped_column(
        Numeric(15, 2), default=0, nullable=False
    )
    payment_terms_days: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    ar_control_account_id: Mapped[int | None] = mapped_column(
        ForeignKey("fin_coa_accounts.id"), nullable=True
    )

    # Tax & Control
    tax_classification: Mapped[str | None] = mapped_column(
        String(50), nullable=True
    )  # PKP, NON_PKP, etc.
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
    ar_control_account: Mapped["COAAccount | None"] = relationship(
        foreign_keys=[ar_control_account_id],
        lazy="selectin",
    )
