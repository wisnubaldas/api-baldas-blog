# API Baldas Blog

Starter project FastAPI + Poetry dengan RBAC schema (users, roles, permissions) dan JWT auth.

## Setup Lokal

```bash
poetry install
```

Optional environment variable:

```bash
DATABASE_URL=sqlite:///./baldas_blog.db
JWT_SECRET_KEY=super-secret-key
JWT_ALGORITHM=HS256
JWT_ACCESS_EXPIRES=3600
JWT_REFRESH_EXPIRES=86400
```

## Migrasi Database (Alembic)

```bash
poetry run alembic upgrade head
```

Rollback 1 revisi:

```bash
poetry run alembic downgrade -1
```

## Seed Data Sample

```bash
poetry run seed
```

Seed ini membuat data sample:

- Roles: `admin`, `editor`, `writer`
- Permissions: `posts.read`, `posts.create`, `posts.update`, `posts.delete`, `users.manage`
- Users:
- `admin@baldas.dev` / `admin123`
- `editor@baldas.dev` / `editor123`
- `writer@baldas.dev` / `writer123`

## Menjalankan API

Mode development:

```bash
poetry run dev
```

Mode production:

```bash
poetry run prod
```

API aktif di `http://127.0.0.1:8000`.

## Dokumentasi Endpoint

Swagger UI: `http://127.0.0.1:8000/docs`

Basic endpoint:

- `GET /`
- `GET /health`

Auth endpoint:

- `POST /auth/register`
- `POST /auth/login`
- `POST /auth/refresh`
- `GET /auth/me`

## Contoh Auth Flow

1. Login

```bash
curl -X POST "http://127.0.0.1:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"admin@baldas.dev\",\"password\":\"admin123\"}"
```

2. Gunakan `access_token` untuk endpoint protected

```bash
curl "http://127.0.0.1:8000/auth/me" \
  -H "Authorization: Bearer <access_token>"
```

3. Refresh access token

```bash
curl -X POST "http://127.0.0.1:8000/auth/refresh" \
  -H "Authorization: Bearer <refresh_token>"
```

## Deploy ke Render

Project ini sudah menyertakan `render.yaml`.

1. Push repository ini ke GitHub.
2. Di Render, pilih **New +** -> **Blueprint**.
3. Hubungkan repository ini, Render akan membaca `render.yaml` otomatis.

Build command: `pip install poetry && poetry install --no-root`
Start command: `poetry run uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-10000}`

## Deploy ke Koyeb

### Opsi 1: Dockerfile deployment

1. Push repository ini ke GitHub.
2. Di Koyeb, pilih **Create App** -> **GitHub**.
3. Pilih repository ini, lalu pilih metode deploy **Dockerfile**.

Saat container start di Koyeb, aplikasi otomatis menjalankan:

- `alembic upgrade head`
- seed data sample (`poetry run seed`)

Setelah itu API dijalankan.

### Opsi 2: Buildpack deployment

Project ini menyertakan `Procfile`:

`web: poetry run start`
