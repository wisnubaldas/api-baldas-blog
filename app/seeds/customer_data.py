"""Master Customer data seeding module.

This module handles creation of sample customer/client data with:
- Identity (code, legal_name, entity_type, tax info)
- Billing & Shipping Address information
- Credit Limit for receivables management
- AR Control Account integration
- Tax Classification
"""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import COAAccount, Customer


def _get_or_create_customer(
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
    billing_street: str | None = None,
    billing_city: str | None = None,
    billing_province: str | None = None,
    billing_country: str = "Indonesia",
    billing_postal_code: str | None = None,
    shipping_street: str | None = None,
    shipping_city: str | None = None,
    shipping_province: str | None = None,
    shipping_country: str | None = None,
    shipping_postal_code: str | None = None,
    credit_limit: float = 0,
    payment_terms_days: int = 0,
    ar_control_account_code: str | None = None,
    tax_classification: str | None = None,
    notes: str | None = None,
) -> Customer:
    """Get existing customer or create a new one."""
    customer = db.scalar(select(Customer).where(Customer.code == code))
    if customer:
        return customer

    ar_control_account_id = None
    if ar_control_account_code:
        account = db.scalar(
            select(COAAccount).where(COAAccount.code == ar_control_account_code)
        )
        if account:
            ar_control_account_id = account.id

    customer = Customer(
        code=code,
        legal_name=legal_name,
        entity_type=entity_type,
        tax_id=tax_id,
        is_pkp=is_pkp,
        contact_person=contact_person,
        email=email,
        phone=phone,
        website=website,
        billing_street=billing_street,
        billing_city=billing_city,
        billing_province=billing_province,
        billing_country=billing_country,
        billing_postal_code=billing_postal_code,
        shipping_street=shipping_street,
        shipping_city=shipping_city,
        shipping_province=shipping_province,
        shipping_country=shipping_country,
        shipping_postal_code=shipping_postal_code,
        credit_limit=credit_limit,
        payment_terms_days=payment_terms_days,
        ar_control_account_id=ar_control_account_id,
        tax_classification=tax_classification,
        notes=notes,
        is_active=True,
    )
    db.add(customer)
    db.flush()
    return customer


def _seed_customers(db: Session) -> None:
    """Seed sample customer data - Minimum Viable Set.

    Including:
    - Code & Legal Name (identity)
    - Entity Type & Tax Info (compliance)
    - Contact Person & Email (communication)
    - Billing Address (invoicing)
    - Shipping Address (delivery)
    - Credit Limit (receivables control)
    - Payment Terms & AR Control Account (financial)
    - Tax Classification (tax compliance)
    """
    # Customer 1 - PT Retail Maju
    _get_or_create_customer(
        db,
        code="CUST-001",
        legal_name="PT Retail Maju Indonesia",
        entity_type="COMPANY",
        tax_id="11.222.333.4-555.666",
        is_pkp=True,
        contact_person="Rina Wijaya",
        email="rina.wijaya@retailmaju.co.id",
        phone="+62-21-8888-1001",
        website="https://retailmaju.co.id",
        billing_street="Jl. Sudirman No. 555",
        billing_city="Jakarta",
        billing_province="Jakarta",
        billing_country="Indonesia",
        billing_postal_code="12000",
        shipping_street="Jl. Gatot Subroto No. 666",
        shipping_city="Tangerang",
        shipping_province="Banten",
        shipping_country="Indonesia",
        shipping_postal_code="15000",
        credit_limit=500000000.00,
        payment_terms_days=30,
        ar_control_account_code="1200",
        tax_classification="PKP",
        notes="Major retail customer",
    )

    # Customer 2 - CV Toko Eceran Maju
    _get_or_create_customer(
        db,
        code="CUST-002",
        legal_name="CV Toko Eceran Maju",
        entity_type="COMPANY",
        contact_person="Bambang Sutrisno",
        email="bambang@tokoeceran.id",
        phone="+62-32-6666-2002",
        billing_street="Jl. Diponegoro No. 222",
        billing_city="Bandung",
        billing_province="Jawa Barat",
        billing_country="Indonesia",
        billing_postal_code="40100",
        credit_limit=200000000.00,
        payment_terms_days=14,
        ar_control_account_code="1200",
        notes="Regional distributor",
    )

    # Customer 3 - Toko Kelontong Pak Haji
    _get_or_create_customer(
        db,
        code="CUST-003",
        legal_name="Toko Kelontong Pak Haji",
        entity_type="INDIVIDUAL",
        contact_person="Haji Muhktar",
        email="pakhaji@tokoku.id",
        phone="+62-274-3333-3003",
        billing_street="Jl. Malioboro No. 1000",
        billing_city="Yogyakarta",
        billing_province="DI Yogyakarta",
        billing_country="Indonesia",
        billing_postal_code="55000",
        credit_limit=50000000.00,
        payment_terms_days=0,
        ar_control_account_code="1200",
        notes="Small retailer, cash & credit",
    )

    # Customer 4 - PT Cafe Kopiko
    _get_or_create_customer(
        db,
        code="CUST-004",
        legal_name="PT Cafe Kopiko Nusantara",
        entity_type="COMPANY",
        tax_id="22.333.444.5-666.777",
        is_pkp=True,
        contact_person="Dewi Lestari",
        email="dewi@cafekopiko.com",
        phone="+62-81-1111-4004",
        website="https://cafekopiko.com",
        billing_street="Jl. Jend. Sudirman No. 888",
        billing_city="Medan",
        billing_province="Sumatera Utara",
        billing_country="Indonesia",
        billing_postal_code="20000",
        shipping_street="Jl. Wr. Supratman No. 333",
        shipping_city="Medan",
        shipping_province="Sumatera Utara",
        shipping_country="Indonesia",
        shipping_postal_code="20100",
        credit_limit=300000000.00,
        payment_terms_days=21,
        ar_control_account_code="1200",
        tax_classification="PKP",
        notes="Cafe chain with multiple branches",
    )


def run_customer_seed(db: Session) -> None:
    """Run customer seeding."""
    _seed_customers(db)
    db.commit()
