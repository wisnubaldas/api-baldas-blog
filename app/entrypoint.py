import os

import uvicorn

from app.bootstrap import init_db


def main() -> None:
    init_db()
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=False)


if __name__ == "__main__":
    main()

