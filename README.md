# Task Tracker API (FastAPI)

Небольшой REST API для задач и пользователей. Асинхронный FastAPI + SQLAlchemy,
JWT-авторизация, миграции Alembic. Основная среда запуска - PostgreSQL в Docker.

## Возможности

- регистрация и логин пользователей (JWT)
- CRUD задач
- статистика по задачам (общая, по дням, активные пользователи)
- асинхронная БД, миграции Alembic
- кэширование списка задач в Redis с инвалидацией при create/update/delete
- линтинг и форматирование через Ruff

## Быстрый старт (Docker + PostgreSQL)

1. Скопируй `.env`:

```bash
cp .env.example .env
```

2. Задай `SECURITY__SECRET_KEY` длиной минимум 32 символа.

3. Запусти контейнеры:

```bash
docker compose up --build
```

Приложение стартует с `alembic upgrade head`, после этого запускается Gunicorn.
Swagger-документация: `http://localhost:8000/docs`

## Локальный запуск (без Docker)

1. Нужен Python 3.13+
2. Установи зависимости через `uv`:

```bash
uv sync
```

3. Примени миграции:

```bash
uv run alembic upgrade head
```

4. Запусти сервер:

```bash
uv run uvicorn src.main:app --reload
```

Для production-запуска с Gunicorn и несколькими воркерами:

```bash
GUNICORN_WORKERS=4 uv run gunicorn -c gunicorn.conf.py src.main:app
```

## Конфигурация

Обязательное:

- `SECURITY__SECRET_KEY` — секрет для JWT (>= 32 символов)

Часто используемые:

- `APP__NAME`, `APP__DEBUG`, `APP__ENVIRONMENT`
- `APP_PORT` — внешний порт приложения в docker compose
- `DATABASE__URL` — URL БД (по умолчанию указывает на PostgreSQL в docker compose)
- `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB` — параметры контейнера Postgres
- `REDIS__URL` — URL Redis для кэша списка задач
- `REDIS__TASK_LIST_TTL_SECONDS` — TTL кэша списка задач в секундах
- `GUNICORN_WORKERS`, `GUNICORN_TIMEOUT`, `GUNICORN_LOG_LEVEL`
- `DATABASE__DRIVER`, `DATABASE__PATH`, `DATABASE__NAME`, `DATABASE__ECHO`

Пример значений смотри в `.env.example`.

## API

Базовый префикс: `/api/v1`

Группы:

- `/users` — регистрация, логин (`POST /api/v1/users/login`), получение пользователя по id
- `/tasks` — список, получить по id, создать, обновить, удалить
- статистика задач: `stats_total`, `stats_by_day`, `active_users` (см. Swagger)

## Тесты

```bash
pytest
```

## Линтинг и форматирование

```bash
ruff check .
ruff format .
```
