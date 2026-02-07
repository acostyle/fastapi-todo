import asyncio
from datetime import datetime, timezone
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock
from uuid import uuid4

from src.tasks.dto import TaskCreateDTO, TaskFilterDTO, TaskReadDTO, TaskUpdateDTO
from src.tasks.services import TaskService


def _run_async(coro):
    return asyncio.run(coro)


def _make_task(user_id):
    now = datetime.now(timezone.utc)
    return SimpleNamespace(
        id=uuid4(),
        title="Task title",
        description="Task description",
        is_done=False,
        created_at=now,
        updated_at=now,
        user_id=user_id,
    )


def test_get_all_tasks_returns_cached_value():
    user_id = uuid4()
    search_params = TaskFilterDTO(user_id=user_id)
    cached_tasks = [
        TaskReadDTO(
            id=uuid4(),
            title="Cached",
            description=None,
            is_done=False,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
    ]

    repository = Mock()
    repository.get_filtered_tasks = AsyncMock()

    cache = Mock()
    cache.get_tasks = AsyncMock(return_value=cached_tasks)
    cache.set_tasks = AsyncMock()
    cache.invalidate_user = AsyncMock()

    service = TaskService(repository=repository, task_list_cache=cache)
    result = _run_async(service.get_all_tasks(search_params=search_params))

    assert result == cached_tasks
    repository.get_filtered_tasks.assert_not_called()
    cache.set_tasks.assert_not_called()


def test_get_all_tasks_populates_cache_on_miss():
    user_id = uuid4()
    search_params = TaskFilterDTO(user_id=user_id)
    model_task = _make_task(user_id)

    repository = Mock()
    repository.get_filtered_tasks = AsyncMock(return_value=[model_task])

    cache = Mock()
    cache.get_tasks = AsyncMock(return_value=None)
    cache.set_tasks = AsyncMock()
    cache.invalidate_user = AsyncMock()

    service = TaskService(repository=repository, task_list_cache=cache)
    result = _run_async(service.get_all_tasks(search_params=search_params))

    assert len(result) == 1
    assert result[0].id == model_task.id
    cache.set_tasks.assert_awaited_once()


def test_create_task_invalidates_cache():
    user_id = uuid4()
    model_task = _make_task(user_id)

    repository = Mock()
    repository.create = AsyncMock(return_value=model_task)

    cache = Mock()
    cache.get_tasks = AsyncMock()
    cache.set_tasks = AsyncMock()
    cache.invalidate_user = AsyncMock()

    service = TaskService(repository=repository, task_list_cache=cache)
    payload = TaskCreateDTO(title="New task", description=None, user_id=user_id)
    _run_async(service.create_task(task_data=payload))

    cache.invalidate_user.assert_awaited_once_with(user_id)


def test_update_task_invalidates_cache():
    user_id = uuid4()
    task = _make_task(user_id)

    repository = Mock()
    repository.get_by_id_and_user = AsyncMock(return_value=task)
    repository.save = AsyncMock(return_value=task)

    cache = Mock()
    cache.get_tasks = AsyncMock()
    cache.set_tasks = AsyncMock()
    cache.invalidate_user = AsyncMock()

    service = TaskService(repository=repository, task_list_cache=cache)
    payload = TaskUpdateDTO(title="Updated title")
    _run_async(service.update_task(task_id=task.id, task_data=payload, user_id=user_id))

    cache.invalidate_user.assert_awaited_once_with(user_id)


def test_delete_task_invalidates_cache():
    user_id = uuid4()
    task = _make_task(user_id)

    repository = Mock()
    repository.get_by_id_and_user = AsyncMock(return_value=task)
    repository.delete = AsyncMock()

    cache = Mock()
    cache.get_tasks = AsyncMock()
    cache.set_tasks = AsyncMock()
    cache.invalidate_user = AsyncMock()

    service = TaskService(repository=repository, task_list_cache=cache)
    _run_async(service.delete_task(task_id=task.id, user_id=user_id))

    cache.invalidate_user.assert_awaited_once_with(user_id)
