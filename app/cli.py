import os

import uvicorn

from app.bootstrap import init_db
from app.core.database import SessionLocal
from app.seeds.sample_data import run_seed


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
    finally:
        db.close()
