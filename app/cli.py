import os

import uvicorn

from app.bootstrap import init_db
from app.core.database import SessionLocal
from app.seeds.coa_data import run_coa_seed
from app.seeds.customer_data import run_customer_seed
from app.seeds.fin_settings_data import run_fin_settings_seed
from app.seeds.sample_data import run_seed
from app.seeds.vendor_data import run_vendor_seed


def _port() -> int:
    return int(os.getenv("PORT", "8000"))


def dev() -> None:
    uvicorn.run("app.main:app", host="127.0.0.1", port=_port(), reload=True)


def prod() -> None:
    init_db()
    uvicorn.run("app.main:app", host="0.0.0.0", port=_port(), reload=False)


def seed() -> None:
    db = SessionLocal()
    try:
        run_seed(db)
        run_coa_seed(db)
        run_vendor_seed(db)
        run_customer_seed(db)
        run_fin_settings_seed(db)
    finally:
        db.close()
