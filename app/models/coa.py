"""Chart of Accounts (COA) models."""

from datetime import datetime

from pydantic import BaseModel, Field
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class COAAccount(Base):
    """Chart of Accounts - master data untuk akun/rekening."""

    __tablename__ = "fin_coa_accounts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    account_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    category: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    parent_id: Mapped[int | None] = mapped_column(
        ForeignKey("fin_coa_accounts.id", ondelete="RESTRICT"),
        nullable=True,
        index=True,
    )
    level: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    path: Mapped[str | None] = mapped_column(String(500), nullable=True)
    is_postable: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    normal_balance: Mapped[str] = mapped_column(String(20), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
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

    settings: Mapped["COAAccountSettings | None"] = relationship(
        back_populates="account",
        uselist=False,
        lazy="selectin",
        cascade="all, delete-orphan",
    )


class COADimension(Base):
    """COA Dimensions - Cost Center, Project, Branch, etc."""

    __tablename__ = "fin_coa_dimensions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    dimension_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class COAAccountSettings(Base):
    """Account Settings - persyaratan tambahan untuk posting ke akun tertentu."""

    __tablename__ = "fin_coa_account_settings"

    account_id: Mapped[int] = mapped_column(
        ForeignKey("fin_coa_accounts.id", ondelete="CASCADE"), primary_key=True
    )
    require_cost_center: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    require_vendor: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    require_customer: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )

    account: Mapped[COAAccount] = relationship(back_populates="settings")


class COAAccountResponse(BaseModel):
    """Representasi account COA untuk response API."""

    id: int
    code: str
    name: str
    account_type: str
    category: str
    parent_id: int | None = None
    level: int
    path: str | None = None
    is_postable: bool
    normal_balance: str
    is_active: bool
    notes: str | None = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class COAAccountTreeNode(COAAccountResponse):
    """Node tree COA untuk file-tree frontend."""

    children: list["COAAccountTreeNode"] = Field(default_factory=list)


COAAccountTreeNode.update_forward_refs()
