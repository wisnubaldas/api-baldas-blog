"""Financial Settings data seeding module.

This module handles initialization of the global financial settings singleton
with AR/AP control account mappings for automatic journal posting.
"""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import COAAccount, FinancialSettings


def _seed_financial_settings(db: Session) -> None:
    """Seed financial settings with AR/AP control accounts - Singleton.

    Minimum Viable:
    - AR Control Account (1200 - Accounts Receivable)
    - AP Control Account (2100 - Accounts Payable)
    - Default Currency (IDR)
    - Default Payment Terms Days (30)

    Note: Only one record should exist. This function is idempotent.
    """
    # Check if settings already exists
    settings = db.scalar(select(FinancialSettings))
    if settings:
        return

    # Get AR and AP control accounts from COA
    ar_account = db.scalar(select(COAAccount).where(COAAccount.code == "1200"))
    ap_account = db.scalar(select(COAAccount).where(COAAccount.code == "2100"))

    settings = FinancialSettings(
        ar_control_account_id=ar_account.id if ar_account else None,
        ap_control_account_id=ap_account.id if ap_account else None,
        default_currency="IDR",
        default_payment_terms_days=30,
        notes="Global finance settings for AR/AP operations - DO NOT DELETE THIS RECORD",
    )
    db.add(settings)
    db.flush()


def run_fin_settings_seed(db: Session) -> None:
    """Run financial settings seeding."""
    _seed_financial_settings(db)
    db.commit()
