# API Baldas Blog

Starter project FastAPI dengan Poetry dan siap deploy ke Render.

## Menjalankan di lokal

```bash
poetry install
poetry run dev
```

Aplikasi akan aktif di `http://127.0.0.1:8000`.

## Menjalankan mode production

```bash
poetry run prod
```

## Endpoint

- `GET /` - informasi API
- `GET /health` - health check

## Deploy ke Render

Project ini sudah menyertakan `render.yaml`.

1. Push repository ini ke GitHub.
2. Di Render, pilih **New +** -> **Blueprint**.
3. Hubungkan repository ini, Render akan membaca `render.yaml` otomatis.

Build command: `pip install poetry && poetry install --no-root`
Start command: `poetry run uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-10000}`
