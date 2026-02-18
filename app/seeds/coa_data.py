"""
Chart of Accounts (COA) and Dimensions seeding module.

This module handles the creation of sample COA accounts, dimensions,
and account settings using ORM models.
"""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import COAAccount, COAAccountSettings, COADimension


def _get_or_create_account(
    db: Session,
    *,
    code: str,
    name: str,
    account_type: str,
    category: str,
    level: int,
    path: str,
    is_postable: bool,
    normal_balance: str,
    notes: str | None = None,
    parent_code: str | None = None,
) -> COAAccount:
    """Get existing account or create a new one."""
    account = db.scalar(select(COAAccount).where(COAAccount.code == code))
    if account:
        return account

    parent_id = None
    if parent_code:
        parent = db.scalar(select(COAAccount).where(COAAccount.code == parent_code))
        if parent:
            parent_id = parent.id

    account = COAAccount(
        code=code,
        name=name,
        account_type=account_type,
        category=category,
        parent_id=parent_id,
        level=level,
        path=path,
        is_postable=is_postable,
        normal_balance=normal_balance,
        notes=notes,
        is_active=True,
    )
    db.add(account)
    db.flush()
    return account


def _get_or_create_dimension(
    db: Session,
    *,
    code: str,
    name: str,
    dimension_type: str,
) -> COADimension:
    """Get existing dimension or create a new one."""
    dimension = db.scalar(select(COADimension).where(COADimension.code == code))
    if dimension:
        return dimension

    dimension = COADimension(
        code=code,
        name=name,
        dimension_type=dimension_type,
        is_active=True,
    )
    db.add(dimension)
    db.flush()
    return dimension


def _seed_coa_accounts(db: Session) -> None:
    """Seed chart of accounts data."""
    # Header accounts
    _get_or_create_account(
        db,
        code="1000",
        name="Assets",
        account_type="ASSET",
        category="ASSET",
        level=0,
        path="1000",
        is_postable=False,
        normal_balance="DEBIT",
    )
    _get_or_create_account(
        db,
        code="2000",
        name="Liabilities",
        account_type="LIABILITY",
        category="LIABILITY",
        level=0,
        path="2000",
        is_postable=False,
        normal_balance="CREDIT",
    )
    _get_or_create_account(
        db,
        code="3000",
        name="Equity",
        account_type="EQUITY",
        category="EQUITY",
        level=0,
        path="3000",
        is_postable=False,
        normal_balance="CREDIT",
    )
    _get_or_create_account(
        db,
        code="4000",
        name="Revenue",
        account_type="REVENUE",
        category="REVENUE",
        level=0,
        path="4000",
        is_postable=False,
        normal_balance="CREDIT",
    )
    _get_or_create_account(
        db,
        code="5000",
        name="Expenses",
        account_type="EXPENSE",
        category="EXPENSE",
        level=0,
        path="5000",
        is_postable=False,
        normal_balance="DEBIT",
    )

    # Assets
    _get_or_create_account(
        db,
        code="1100",
        name="Cash and Cash Equivalent",
        account_type="ASSET",
        category="CASH",
        parent_code="1000",
        level=1,
        path="1000/1100",
        is_postable=False,
        normal_balance="DEBIT",
    )
    _get_or_create_account(
        db,
        code="1110",
        name="Cash on Hand",
        account_type="ASSET",
        category="CASH",
        parent_code="1100",
        level=2,
        path="1000/1100/1110",
        is_postable=True,
        normal_balance="DEBIT",
    )
    _get_or_create_account(
        db,
        code="1120",
        name="Bank BCA",
        account_type="ASSET",
        category="BANK",
        parent_code="1100",
        level=2,
        path="1000/1100/1120",
        is_postable=True,
        normal_balance="DEBIT",
    )
    _get_or_create_account(
        db,
        code="1200",
        name="Accounts Receivable",
        account_type="ASSET",
        category="AR",
        parent_code="1000",
        level=1,
        path="1000/1200",
        is_postable=True,
        normal_balance="DEBIT",
        notes="Control account for customer receivables",
    )
    _get_or_create_account(
        db,
        code="1300",
        name="Inventory",
        account_type="ASSET",
        category="INVENTORY",
        parent_code="1000",
        level=1,
        path="1000/1300",
        is_postable=True,
        normal_balance="DEBIT",
    )

    # Liabilities
    _get_or_create_account(
        db,
        code="2100",
        name="Accounts Payable",
        account_type="LIABILITY",
        category="AP",
        parent_code="2000",
        level=1,
        path="2000/2100",
        is_postable=True,
        normal_balance="CREDIT",
        notes="Control account for vendor payables",
    )
    _get_or_create_account(
        db,
        code="2200",
        name="Tax Payable",
        account_type="LIABILITY",
        category="TAX",
        parent_code="2000",
        level=1,
        path="2000/2200",
        is_postable=True,
        normal_balance="CREDIT",
    )

    # Equity
    _get_or_create_account(
        db,
        code="3100",
        name="Owner Capital",
        account_type="EQUITY",
        category="CAPITAL",
        parent_code="3000",
        level=1,
        path="3000/3100",
        is_postable=True,
        normal_balance="CREDIT",
    )
    _get_or_create_account(
        db,
        code="3200",
        name="Retained Earnings",
        account_type="EQUITY",
        category="RETAINED_EARNINGS",
        parent_code="3000",
        level=1,
        path="3000/3200",
        is_postable=True,
        normal_balance="CREDIT",
    )

    # Revenue
    _get_or_create_account(
        db,
        code="4100",
        name="Sales Revenue",
        account_type="REVENUE",
        category="OPERATING_REVENUE",
        parent_code="4000",
        level=1,
        path="4000/4100",
        is_postable=True,
        normal_balance="CREDIT",
    )

    # Expenses
    _get_or_create_account(
        db,
        code="5100",
        name="Cost of Goods Sold",
        account_type="EXPENSE",
        category="COGS",
        parent_code="5000",
        level=1,
        path="5000/5100",
        is_postable=True,
        normal_balance="DEBIT",
    )
    _get_or_create_account(
        db,
        code="5200",
        name="Operating Expense",
        account_type="EXPENSE",
        category="OPEX",
        parent_code="5000",
        level=1,
        path="5000/5200",
        is_postable=True,
        normal_balance="DEBIT",
    )
    _get_or_create_account(
        db,
        code="5300",
        name="Tax Expense",
        account_type="EXPENSE",
        category="TAX",
        parent_code="5000",
        level=1,
        path="5000/5300",
        is_postable=True,
        normal_balance="DEBIT",
    )


def _seed_dimensions(db: Session) -> None:
    """Seed dimensions data."""
    _get_or_create_dimension(
        db,
        code="CC-HQ",
        name="Head Office",
        dimension_type="COST_CENTER",
    )
    _get_or_create_dimension(
        db,
        code="CC-OPS",
        name="Operations",
        dimension_type="COST_CENTER",
    )
    _get_or_create_dimension(
        db,
        code="PRJ-001",
        name="Internal Project 001",
        dimension_type="PROJECT",
    )
    _get_or_create_dimension(
        db,
        code="BR-JKT",
        name="Jakarta Branch",
        dimension_type="BRANCH",
    )


def _seed_account_settings(db: Session) -> None:
    """Seed account settings."""
    # Accounts Receivable - require customer
    ar_account = db.scalar(select(COAAccount).where(COAAccount.code == "1200"))
    if ar_account and not db.scalar(
        select(COAAccountSettings).where(COAAccountSettings.account_id == ar_account.id)
    ):
        ar_settings = COAAccountSettings(
            account_id=ar_account.id,
            require_cost_center=False,
            require_vendor=False,
            require_customer=True,
        )
        db.add(ar_settings)

    # Accounts Payable - require vendor
    ap_account = db.scalar(select(COAAccount).where(COAAccount.code == "2100"))
    if ap_account and not db.scalar(
        select(COAAccountSettings).where(COAAccountSettings.account_id == ap_account.id)
    ):
        ap_settings = COAAccountSettings(
            account_id=ap_account.id,
            require_cost_center=False,
            require_vendor=True,
            require_customer=False,
        )
        db.add(ap_settings)

    # COGS - require cost center
    cogs_account = db.scalar(select(COAAccount).where(COAAccount.code == "5100"))
    if cogs_account and not db.scalar(
        select(COAAccountSettings).where(
            COAAccountSettings.account_id == cogs_account.id
        )
    ):
        cogs_settings = COAAccountSettings(
            account_id=cogs_account.id,
            require_cost_center=True,
            require_vendor=False,
            require_customer=False,
        )
        db.add(cogs_settings)

    # Operating Expense - require cost center
    opex_account = db.scalar(select(COAAccount).where(COAAccount.code == "5200"))
    if opex_account and not db.scalar(
        select(COAAccountSettings).where(
            COAAccountSettings.account_id == opex_account.id
        )
    ):
        opex_settings = COAAccountSettings(
            account_id=opex_account.id,
            require_cost_center=True,
            require_vendor=False,
            require_customer=False,
        )
        db.add(opex_settings)

    db.flush()


def run_coa_seed(db: Session) -> None:
    """Run all COA seeding functions."""
    _seed_coa_accounts(db)
    _seed_dimensions(db)
    _seed_account_settings(db)
    db.commit()
