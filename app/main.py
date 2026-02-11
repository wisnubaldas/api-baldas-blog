from fastapi import FastAPI

app = FastAPI(title="API Baldas Blog")


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "API Baldas Blog is running"}


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
