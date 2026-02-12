from pathlib import Path

from alembic import command
from alembic.config import Config

from app.core.database import SessionLocal
from app.seeds.sample_data import run_seed


def init_db() -> None:
    project_root = Path(__file__).resolve().parents[1]
    alembic_cfg = Config(str(project_root / "alembic.ini"))
    alembic_cfg.set_main_option("script_location", str(project_root / "alembic"))
    command.upgrade(alembic_cfg, "head")

    db = SessionLocal()
    try:
        run_seed(db)
    finally:
        db.close()
