import asyncio
import os
import shutil
import tempfile
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

_TEST_DB_DIR = Path(tempfile.mkdtemp(prefix="fastapi_test_db_"))
_TEST_DB_PATH = _TEST_DB_DIR / "test.db"

os.environ.setdefault("APP__ENVIRONMENT", "testing")
os.environ.setdefault("DATABASE__URL", f"sqlite+aiosqlite:///{_TEST_DB_PATH}")
os.environ.setdefault(
    "SECURITY__SECRET_KEY",
    "test-secret-key-please-change-1234567890abcdef",
)

from src.database import Base, async_session_maker, engine, get_session  # noqa: E402
from src.main import app


def _run_async(coro):
    asyncio.run(coro)


async def _init_models() -> None:
    import src.tasks.models  # noqa: F401
    import src.users.models  # noqa: F401

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def _drop_models() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="session", autouse=True)
def _prepare_database():
    _run_async(_init_models())
    yield
    _run_async(_drop_models())
    _run_async(engine.dispose())
    shutil.rmtree(_TEST_DB_DIR, ignore_errors=True)


@pytest.fixture()
def client():
    async def override_get_session():
        async with async_session_maker() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise

    app.dependency_overrides[get_session] = override_get_session

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
