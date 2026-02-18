"""Finance Master Data Architecture - Minimum Viable Implementation

# STRUKTUR DATA MASTER FINANCE

Setiap master data diorganisir dalam 3 layer:

1. MODEL (app/models/\*.py) - ORM definitions dengan relationships
2. MIGRATION (alembic/versions/\*.py) - SQL schema dengan indexes
3. SEEDER (app/seeds/\*\_data.py) - Sample data dengan business logic

═══════════════════════════════════════════════════════════════════════════════

1. MASTER COA (Chart of Accounts)
   ──────────────────────────────────────────────────────────────────────────────

Model: app/models/coa.py
Migration: alembic/versions/20260218_0003_create_master_coa_tables.py
Seeder: app/seeds/coa_data.py

✓ CHECKLIST MINIMUM VIABLE - COA:
✓ Code (unique identifier)
✓ Name (account name)
✓ Account Type (ASSET/LIABILITY/EQUITY/REVENUE/EXPENSE)
✓ Category (grouping: CASH, BANK, AR, AP, COGS, TAX, etc.)
✓ Parent ID + Level + Path (hierarchy structure)
✓ Is Postable (only leaf accounts for journals)
✓ Normal Balance (DEBIT/CREDIT)
✓ Is Active (status control)
✓ Account Settings (require_cost_center, require_vendor, require_customer)
✓ Dimensions (COST_CENTER, PROJECT, BRANCH)

Sample Data:
• 1000: Assets (header)
• 1100: Cash and Cash Equivalent
• 1110: Cash on Hand (postable)
• 1120: Bank BCA (postable)
• 1200: Accounts Receivable (AR Control)
• 1300: Inventory
• 2000: Liabilities (header)
• 2100: Accounts Payable (AP Control)
• 2200: Tax Payable
• 3000: Equity, 4000: Revenue, 5000: Expenses (similar structure)

═══════════════════════════════════════════════════════════════════════════════

2. MASTER VENDOR (Supplier)
   ──────────────────────────────────────────────────────────────────────────────

Model: app/models/vendor.py
Migration: alembic/versions/20260219_0004_create_master_vendor_table.py
Seeder: app/seeds/vendor_data.py

✓ CHECKLIST MINIMUM VIABLE - VENDOR:
✓ Code (unique identifier)
✓ Legal Name (business name)
✓ Entity Type (COMPANY/INDIVIDUAL)
✓ Tax ID (optional, unique if provided)
✓ Is PKP (tax registration status)
✓ Contact Person (name)
✓ Email (primary contact)
✓ Phone (contact number)
✓ Website (optional)
✓ Street Address (billing address)
✓ City, Province, Country, Postal Code
✓ Default Currency (IDR)
✓ Payment Terms Days (credit period)
✓ Payment Methods (BANK_TRANSFER, CASH, etc.)
✓ Bank Account & Bank Name
✓ AP Control Account ID (FK to COA 2100)
✓ Tax Withholding Percentage
✓ Is Active (status control)
✓ Is Blacklist (vendor blocking)
✓ Notes (additional info)

Sample Data (3 vendors):
• VND-001: PT Supplier Indonesia Jaya (Company, PKP, Jakarta)
• VND-002: CV Toko Umum Makmur (Company, PKP, Surabaya)
• VND-003: Distributor Bandung Raya (Individual, Bandung)

═══════════════════════════════════════════════════════════════════════════════

3. MASTER CUSTOMER (Client)
   ──────────────────────────────────────────────────────────────────────────────

Model: app/models/customer.py
Migration: alembic/versions/20260219_0005_create_master_customer_table.py
Seeder: app/seeds/customer_data.py

✓ CHECKLIST MINIMUM VIABLE - CUSTOMER:
✓ Code (unique identifier)
✓ Legal Name (business name)
✓ Entity Type (COMPANY/INDIVIDUAL)
✓ Tax ID (optional, unique if provided)
✓ Is PKP (tax registration status)
✓ Contact Person (name)
✓ Email (primary contact)
✓ Phone (contact number)
✓ Website (optional)
✓ Billing Street, City, Province, Country, Postal Code
✓ Shipping Street, City, Province, Country, Postal Code (optional)
✓ Default Currency (IDR)
✓ Credit Limit (receivables control)
✓ Payment Terms Days (credit period)
✓ AR Control Account ID (FK to COA 1200)
✓ Tax Classification (PKP/NON_PKP, etc.)
✓ Is Active (status control)
✓ Is Blacklist (customer blocking)
✓ Notes (additional info)

Sample Data (4 customers):
• CUST-001: PT Retail Maju Indonesia (Company, PKP, Jakarta, Limit: 500M)
• CUST-002: CV Toko Eceran Maju (Company, Bandung, Limit: 200M)
• CUST-003: Toko Kelontong Pak Haji (Individual, Yogyakarta, Limit: 50M)
• CUST-004: PT Cafe Kopiko Nusantara (Company, PKP, Medan, Limit: 300M)

═══════════════════════════════════════════════════════════════════════════════

4. FINANCIAL SETTINGS (Global Configuration)
   ──────────────────────────────────────────────────────────────────────────────

Model: app/models/fin_settings.py
Migration: alembic/versions/20260219_0006_create_financial_settings_table.py
Seeder: app/seeds/fin_settings_data.py

✓ CHECKLIST MINIMUM VIABLE - FINANCIAL SETTINGS:
✓ ID (primary key)
✓ AR Control Account ID (FK to COA 1200 - Accounts Receivable)
✓ AP Control Account ID (FK to COA 2100 - Accounts Payable)
✓ Default Currency (IDR)
✓ Default Payment Terms Days (30 days)
✓ Notes (configuration info)

Note: Singleton pattern - Only ONE record should exist in this table.
Use: settings = db.query(FinancialSettings).first()

═══════════════════════════════════════════════════════════════════════════════

RELATIONSHIPS & INTEGRATION
───────────────────────────────────────────────────────────────────────────────

                        ╔═════════════════════╗
                        ║  COAAccount (1200)  ║
                        ║ Accounts Receivable ║
                        ╚═════════════════════╝
                              ▲        ▲
                              │        │
                    ┌─────────┘        └─────────┐
                    │                            │
            ╔═══════════════╗        ╔═══════════════════╗
            ║   Customer    ║        ║ FinancialSettings ║
            ║ ar_control_id ║        ║  ar_control_id    ║
            ╚═══════════════╝        ╚═══════════════════╝
                                           │
                                           │
                        ╔═════════════════════╗
                        ║  COAAccount (2100)  ║
                        ║ Accounts Payable    ║
                        ╚═════════════════════╝
                              ▲        ▲
                              │        │
                    ┌─────────┘        └─────────┐
                    │                            │
            ╔═══════════════╗        ╔═══════════════════╗
            ║   Vendor      ║        ║ FinancialSettings ║
            ║ ap_control_id ║        ║  ap_control_id    ║
            ╚═══════════════╝        ╚═══════════════════╝

═══════════════════════════════════════════════════════════════════════════════

EXECUTION ORDER IN BOOTSTRAP & CLI
────────────────────────────────────────────────────────────────────────────

bootstrap.py::init_db() dan cli.py::seed()

1. run_seed(db) → RBAC & Menu (base authentication)
2. run_coa_seed(db) → Chart of Accounts + Dimensions
3. run_vendor_seed(db) → Vendor data (references COA)
4. run_customer_seed(db) → Customer data (references COA)
5. run_fin_settings_seed(db) → Financial Settings (references COA)

Order is CRITICAL: COA must be seeded first as it's referenced by all others!

═══════════════════════════════════════════════════════════════════════════════

FILES KESELURUHAN STRUKTUR
──────────────────────────

app/models/
├── **init**.py (centralized exports)
├── rbac.py (User, Role, Permission, Menu)
├── coa.py (COAAccount, COADimension, COAAccountSettings)
├── vendor.py (Vendor) ← NEW
├── customer.py (Customer) ← NEW
└── fin_settings.py (FinancialSettings) ← NEW

alembic/versions/
├── 20260212_0001_create_rbac_tables.py
├── 20260212_0002_create_menus_table.py
├── 20260218_0003_create_master_coa_tables.py
├── 20260219_0004_create_master_vendor_table.py ← NEW
├── 20260219_0005_create_master_customer_table.py ← NEW
└── 20260219_0006_create_financial_settings_table.py ← NEW

app/seeds/
├── **init**.py
├── sample_data.py (RBAC & Menu data)
├── coa_data.py (COA data)
├── vendor_data.py (Vendor data) ← NEW
├── customer_data.py (Customer data) ← NEW
└── fin_settings_data.py (Financial Settings data) ← NEW

═══════════════════════════════════════════════════════════════════════════════

TESTING CHECKLIST
─────────────────────────────────────────────────────────────────────────────

□ Migration runs without error: alembic upgrade head
□ All tables created with correct relationships
□ Seed data inserted successfully
□ Foreign keys working: Vendor.ap_control_account references COA 2100
□ Foreign keys working: Customer.ar_control_account references COA 1200
□ Indexes created: fin_vendors_code, fin_vendors_is_active, fin_vendors_email
□ Indexes created: fin_customers_code, fin_customers_is_active, fin_customers_email
□ FinancialSettings singleton pattern verified
□ Sample data counts: 3 vendors, 4 customers, 1 settings record

═══════════════════════════════════════════════════════════════════════════════
"""
