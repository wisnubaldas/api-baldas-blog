from pathlib import Path

from alembic import command
from alembic.config import Config

from app.core.database import SessionLocal
from app.seeds.coa_data import run_coa_seed
from app.seeds.customer_data import run_customer_seed
from app.seeds.fin_settings_data import run_fin_settings_seed
from app.seeds.sample_data import run_seed
from app.seeds.vendor_data import run_vendor_seed


def init_db() -> None:
    project_root = Path(__file__).resolve().parents[1]
    alembic_cfg = Config(str(project_root / "alembic.ini"))
    alembic_cfg.set_main_option("script_location", str(project_root / "alembic"))
    command.upgrade(alembic_cfg, "head")

    db = SessionLocal()
    try:
        run_seed(db)
        run_coa_seed(db)
        run_vendor_seed(db)
        run_customer_seed(db)
        run_fin_settings_seed(db)
    finally:
        db.close()
