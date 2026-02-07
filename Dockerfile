ARG PYTHON_IMAGE=python:3.13.5-slim-bookworm
ARG UV_VERSION=0.7.12

FROM ${PYTHON_IMAGE} AS builder
ARG UV_VERSION

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install --no-cache-dir "uv==${UV_VERSION}"

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

FROM ${PYTHON_IMAGE} AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH" \
    PYTHONPATH=/app

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv
COPY src ./src
COPY alembic ./alembic
COPY alembic.ini ./
COPY gunicorn.conf.py ./

EXPOSE 8000

CMD ["gunicorn", "-c", "gunicorn.conf.py", "src.main:app"]
