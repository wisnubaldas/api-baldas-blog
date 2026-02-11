# API Baldas Blog

Starter project FastAPI dengan Poetry, siap deploy ke Render dan Koyeb.

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

## Deploy ke Koyeb

### Opsi 1 (direkomendasikan): Dockerfile deployment

Project ini sudah punya `Dockerfile` dan `.dockerignore`.

1. Push repository ini ke GitHub.
2. Di Koyeb, pilih **Create App** -> **GitHub**.
3. Pilih repository ini, lalu pilih metode deploy **Dockerfile**.
4. Deploy langsung (Koyeb akan membaca `Dockerfile`).

### Opsi 2: Buildpack deployment

Project ini juga menyertakan `Procfile`:

`web: uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}`

Jika memakai buildpack Python Koyeb, `Procfile` ini dipakai untuk run command.
