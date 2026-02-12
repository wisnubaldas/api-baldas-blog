from alembic import command
from alembic.config import Config

from app.core.database import SessionLocal
from app.seeds.sample_data import run_seed


def init_db() -> None:
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")

    db = SessionLocal()
    try:
        run_seed(db)
    finally:
        db.close()

