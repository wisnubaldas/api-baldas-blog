"""
Chart of Accounts (COA) and Dimensions seeding module.

This module handles the creation of sample COA accounts, dimensions,
and account settings using ORM models.
"""

import json
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import COAAccount, COAAccountSettings, COADimension

_DEFAULT_MASTER_COA_PATH = (
    Path(__file__).resolve().parent / "data" / "coa_isak335_full_master_level1-5.json"
)


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


def _load_master_coa_data() -> list[dict]:
    """Load master COA JSON payload from local seed data folder."""
    if not _DEFAULT_MASTER_COA_PATH.exists():
        raise FileNotFoundError(
            f"Master COA file not found: {_DEFAULT_MASTER_COA_PATH}"
        )

    with _DEFAULT_MASTER_COA_PATH.open("r", encoding="utf-8") as fp:
        payload = json.load(fp)

    if not isinstance(payload, list):
        raise ValueError("Master COA JSON must be a list of account objects.")

    return payload


def _extract_parent_code(path: str, code: str) -> str | None:
    """Extract parent account code from slash-delimited account path."""
    segments = [segment.strip() for segment in path.split("/") if segment.strip()]
    if len(segments) <= 1:
        return None
    if segments[-1] != code:
        return segments[-2]
    return segments[-2]


def _seed_coa_accounts(db: Session) -> None:
    """Seed chart of accounts data from the master COA JSON file."""
    master_accounts = _load_master_coa_data()
    ordered_accounts = sorted(
        master_accounts,
        key=lambda account: (
            int(account.get("level", 0)),
            str(account.get("path", "")),
            str(account.get("code", "")),
        ),
    )

    for account in ordered_accounts:
        code = str(account["code"]).strip()
        path = str(account["path"]).strip()
        parent_code = _extract_parent_code(path, code)

        _get_or_create_account(
            db,
            code=code,
            name=str(account["name"]).strip(),
            account_type=str(account["account_type"]).strip(),
            category=str(account["category"]).strip(),
            parent_code=parent_code,
            level=int(account["level"]),
            path=path,
            is_postable=bool(account["is_postable"]),
            normal_balance=str(account["normal_balance"]).strip(),
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
