SHELL := /bin/sh

.PHONY: help env up up-d down down-v restart logs ps \
	local-setup sync migrate run test lint format

help:
	@echo "Common commands:"
	@echo "  make env          - create .env from .env.example (if missing)"
	@echo "  make up           - docker compose up --build"
	@echo "  make up-d         - docker compose up --build -d"
	@echo "  make down         - docker compose down"
	@echo "  make down-v       - docker compose down -v"
	@echo "  make restart      - restart app service"
	@echo "  make logs         - follow app logs"
	@echo "  make ps           - show containers"
	@echo "  make local-setup  - env + sync + migrate"
	@echo "  make sync         - install deps via uv"
	@echo "  make migrate      - run alembic migrations"
	@echo "  make run          - start uvicorn locally"
	@echo "  make test         - run tests"
	@echo "  make lint         - ruff check"
	@echo "  make format       - ruff format"

env:
	@test -f .env || cp .env.example .env

up:
	docker compose up --build

up-d:
	docker compose up --build -d

down:
	docker compose down

down-v:
	docker compose down -v

restart:
	docker compose restart app

logs:
	docker compose logs -f app

ps:
	docker compose ps

local-setup: env sync migrate

sync:
	uv sync

migrate:
	uv run alembic upgrade head

run:
	uv run uvicorn src.main:app --reload

test:
	.venv/bin/pytest -q

lint:
	.venv/bin/ruff check .

format:
	.venv/bin/ruff format .
