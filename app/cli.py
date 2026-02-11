import os

import uvicorn


def _port() -> int:
    return int(os.getenv("PORT", "8000"))


def dev() -> None:
    uvicorn.run("app.main:app", host="127.0.0.1", port=_port(), reload=True)


def prod() -> None:
    uvicorn.run("app.main:app", host="0.0.0.0", port=_port(), reload=False)
