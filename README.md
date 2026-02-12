# Task Tracker API (FastAPI)

Простое API для задач и пользователей: FastAPI + SQLAlchemy + JWT + Redis + Alembic.

## Запуск через Docker

1. Подготовь env:

```bash
cp .env.example .env
```

2. Открой `.env` и задай `SECURITY__SECRET_KEY` (минимум 32 символа).

3. Запусти проект:

```bash
make up
```

4. Открой Swagger:

`http://localhost:8000/docs`

Это все. База и Redis поднимутся автоматически, миграции применятся при старте app.

## Остановка и сброс

Остановить контейнеры:

```bash
make down
```

Остановить и удалить данные БД/Redis:

```bash
make down-v
```

## Локальный запуск (без Docker)

Требования:
- Python 3.13+
- `uv`
- PostgreSQL и Redis (или скорректируй `.env` под свой запуск)

Команды:

```bash
make local-setup
make run
```

Swagger:
`http://localhost:8000/docs`

## Что внутри

- регистрация и логин пользователей (JWT)
- CRUD задач
- статистика задач (`stats_total`, `stats_by_day`, `active_users`)
- кэш списка задач в Redis

## Основные настройки (`.env`)

Обязательное:
- `SECURITY__SECRET_KEY`

## Частые проблемы

`SECURITY__SECRET_KEY must be at least 32 characters`:
- задай более длинный ключ в `.env`.

Порт 8000 занят:
- поменяй `APP_PORT` в `.env`.

Не получается тестировать через curl/Postman:
- в проекте включена блокировка некоторых User-Agent.
- используй Swagger UI в браузере (`/docs`) или другой клиент.

## Тесты и линтинг

```bash
make test
make lint
```

## Полезные make-команды

```bash
make help
make up-d
make logs
make ps
```
