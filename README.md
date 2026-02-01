# Task Tracker API (FastAPI)

Небольшой REST API для задач и пользователей. Асинхронный FastAPI + SQLAlchemy,
JWT-авторизация, миграции Alembic. По умолчанию используется SQLite.

## Возможности

- регистрация и логин пользователей (JWT)
- CRUD задач
- статистика по задачам (общая, по дням, активные пользователи)
- асинхронная БД, миграции Alembic

## Быстрый старт (SQLite)

1. Нужен Python 3.13+
2. Скопируй и настрой `.env`:

```bash
cp .env.example .env
```

Задай `SECURITY__SECRET_KEY` длиной минимум 32 символа.

3. Установи зависимости через `uv`:

```bash
uv sync
```

4. Примени миграции:

```bash
uv run alembic upgrade head
```

5. Запусти сервер:

```bash
uv run uvicorn src.main:app --reload
```

Swagger-документация: `http://localhost:8000/docs`

## Конфигурация

Обязательное:

- `SECURITY__SECRET_KEY` — секрет для JWT (>= 32 символов)

Часто используемые:

- `APP__NAME`, `APP__DEBUG`, `APP__ENVIRONMENT`
- `DATABASE__URL` — если указано, используется вместо SQLite
- `DATABASE__DRIVER`, `DATABASE__PATH`, `DATABASE__NAME`, `DATABASE__ECHO`

Пример значений смотри в `.env.example`.

## API

Базовый префикс: `/api/v1`

Группы:

- `/users` — регистрация, логин, получение пользователя по id
- `/tasks` — список, получить по id, создать, обновить, удалить
- статистика задач: `stats_total`, `stats_by_day`, `active_users` (см. Swagger)

## Тесты

```bash
pytest
```
