"""Master Vendor data seeding module.

This module handles creation of sample vendor/supplier data with:
- Identity (code, legal_name, entity_type, tax info)
- Contact & Address information
- Financial configuration (payment terms, bank details)
- AP Control Account integration
"""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import COAAccount, Vendor


def _get_or_create_vendor(
    db: Session,
    *,
    code: str,
    legal_name: str,
    entity_type: str = "COMPANY",
    tax_id: str | None = None,
    is_pkp: bool = False,
    contact_person: str | None = None,
    email: str | None = None,
    phone: str | None = None,
    website: str | None = None,
    street_address: str | None = None,
    city: str | None = None,
    province: str | None = None,
    country: str = "Indonesia",
    postal_code: str | None = None,
    payment_terms_days: int = 0,
    payment_methods: str | None = None,
    bank_account: str | None = None,
    bank_name: str | None = None,
    ap_control_account_code: str | None = None,
    tax_withholding_pct: float | None = None,
    notes: str | None = None,
) -> Vendor:
    """Get existing vendor or create a new one."""
    vendor = db.scalar(select(Vendor).where(Vendor.code == code))
    if vendor:
        return vendor

    ap_control_account_id = None
    if ap_control_account_code:
        account = db.scalar(
            select(COAAccount).where(COAAccount.code == ap_control_account_code)
        )
        if account:
            ap_control_account_id = account.id

    vendor = Vendor(
        code=code,
        legal_name=legal_name,
        entity_type=entity_type,
        tax_id=tax_id,
        is_pkp=is_pkp,
        contact_person=contact_person,
        email=email,
        phone=phone,
        website=website,
        street_address=street_address,
        city=city,
        province=province,
        country=country,
        postal_code=postal_code,
        payment_terms_days=payment_terms_days,
        payment_methods=payment_methods,
        bank_account=bank_account,
        bank_name=bank_name,
        ap_control_account_id=ap_control_account_id,
        tax_withholding_pct=tax_withholding_pct,
        notes=notes,
        is_active=True,
    )
    db.add(vendor)
    db.flush()
    return vendor


def _seed_vendors(db: Session) -> None:
    """Seed sample vendor data - Minimum Viable Set.

    Including:
    - Code & Legal Name (identity)
    - Entity Type & Tax Info (compliance)
    - Contact Person & Email (communication)
    - Billing Address (procurement)
    - Payment Terms & Methods (financial)
    - AP Control Account (accounting integration)
    """
    # Vendor 1 - PT Supplier Indonesia
    _get_or_create_vendor(
        db,
        code="VND-001",
        legal_name="PT Supplier Indonesia Jaya",
        entity_type="COMPANY",
        tax_id="12.345.678.9-012.345",
        is_pkp=True,
        contact_person="Budi Santoso",
        email="budi.santoso@supplier-ij.com",
        phone="+62-21-5555-1001",
        website="https://supplier-ij.com",
        street_address="Jl. Merdeka No. 123",
        city="Jakarta",
        province="Jakarta",
        country="Indonesia",
        postal_code="12345",
        payment_terms_days=30,
        payment_methods="BANK_TRANSFER,CASH",
        bank_account="1234567890",
        bank_name="Bank BCA",
        ap_control_account_code="2100",
        tax_withholding_pct=2.0,
        notes="Main supplier for raw materials",
    )

    # Vendor 2 - CV Toko Umum
    _get_or_create_vendor(
        db,
        code="VND-002",
        legal_name="CV Toko Umum Makmur",
        entity_type="COMPANY",
        tax_id="98.765.432.1-543.210",
        is_pkp=True,
        contact_person="Siti Nurhaliza",
        email="siti@tokomakmur.id",
        phone="+62-31-7777-2002",
        website="https://tokomakmur.id",
        street_address="Jl. Ahmad Yani No. 456",
        city="Surabaya",
        province="Jawa Timur",
        country="Indonesia",
        postal_code="60000",
        payment_terms_days=14,
        payment_methods="BANK_TRANSFER",
        bank_account="9876543210",
        bank_name="Bank Mandiri",
        ap_control_account_code="2100",
        tax_withholding_pct=1.5,
        notes="Supplier untuk spare parts",
    )

    # Vendor 3 - Distributor Bandung Raya
    _get_or_create_vendor(
        db,
        code="VND-003",
        legal_name="Distributor Bandung Raya",
        entity_type="INDIVIDUAL",
        contact_person="Ahmad Hidayat",
        email="ahmad@distributorbandung.com",
        phone="+62-274-9999-3003",
        street_address="Jl. Gatot Subroto No. 789",
        city="Bandung",
        province="Jawa Barat",
        country="Indonesia",
        postal_code="40000",
        payment_terms_days=7,
        payment_methods="CASH",
        ap_control_account_code="2100",
        notes="Small supplier, cash basis",
    )


def run_vendor_seed(db: Session) -> None:
    """Run vendor seeding."""
    _seed_vendors(db)
    db.commit()
