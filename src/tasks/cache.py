import json
import logging
from datetime import datetime
from hashlib import sha256
from typing import Any, Protocol
from uuid import UUID

from fastapi import Request
from redis.asyncio import Redis
from redis.exceptions import RedisError

from src.config import settings
from src.tasks.dto import TaskFilterDTO, TaskReadDTO

TASK_LIST_CACHE_PREFIX = "tasks:list"
TASK_LIST_VERSION_PREFIX = "tasks:list:version"

logger = logging.getLogger("app.tasks.cache")


class TaskListCacheBackend(Protocol):
    async def get_tasks(
        self, user_id: UUID, search_params: TaskFilterDTO
    ) -> list[TaskReadDTO] | None: ...

    async def set_tasks(
        self,
        user_id: UUID,
        search_params: TaskFilterDTO,
        tasks: list[TaskReadDTO],
    ) -> None: ...

    async def invalidate_user(self, user_id: UUID) -> None: ...

    async def close(self) -> None: ...


class RedisTaskListCache:
    def __init__(self, client: Redis, ttl_seconds: int):
        self.client = client
        self.ttl_seconds = ttl_seconds

    async def get_tasks(
        self, user_id: UUID, search_params: TaskFilterDTO
    ) -> list[TaskReadDTO] | None:
        try:
            version = await self._get_user_version(user_id)
            cache_key = self._build_cache_key(user_id, search_params, version)
            raw_payload = await self.client.get(cache_key)
            if raw_payload is None:
                return None

            payload = json.loads(raw_payload)
            if not isinstance(payload, list):
                return None

            tasks: list[TaskReadDTO] = []
            for task_data in payload:
                if not isinstance(task_data, dict):
                    return None
                tasks.append(self._deserialize_task(task_data))
            return tasks
        except (RedisError, TypeError, ValueError, KeyError) as exc:
            logger.warning("Failed to read task list cache: %s", exc)
            return None

    async def set_tasks(
        self,
        user_id: UUID,
        search_params: TaskFilterDTO,
        tasks: list[TaskReadDTO],
    ) -> None:
        try:
            version = await self._get_user_version(user_id)
            cache_key = self._build_cache_key(user_id, search_params, version)
            payload = [self._serialize_task(task) for task in tasks]
            await self.client.set(
                cache_key, json.dumps(payload, ensure_ascii=True), ex=self.ttl_seconds
            )
        except RedisError as exc:
            logger.warning("Failed to write task list cache: %s", exc)

    async def invalidate_user(self, user_id: UUID) -> None:
        try:
            await self.client.incr(self._version_key(user_id))
        except RedisError as exc:
            logger.warning("Failed to invalidate task list cache: %s", exc)

    async def close(self) -> None:
        try:
            await self.client.aclose()
        except RedisError as exc:
            logger.warning("Failed to close redis client: %s", exc)

    async def _get_user_version(self, user_id: UUID) -> int:
        raw_version = await self.client.get(self._version_key(user_id))
        if raw_version is None:
            return 0
        try:
            return int(raw_version)
        except (TypeError, ValueError):
            return 0

    @staticmethod
    def _version_key(user_id: UUID) -> str:
        return f"{TASK_LIST_VERSION_PREFIX}:{user_id}"

    @staticmethod
    def _build_cache_key(
        user_id: UUID, search_params: TaskFilterDTO, version: int
    ) -> str:
        params_payload = RedisTaskListCache._serialize_filter(search_params)
        params_json = json.dumps(
            params_payload, sort_keys=True, ensure_ascii=True, separators=(",", ":")
        )
        params_hash = sha256(params_json.encode("utf-8")).hexdigest()
        return f"{TASK_LIST_CACHE_PREFIX}:{user_id}:v{version}:{params_hash}"

    @staticmethod
    def _serialize_filter(search_params: TaskFilterDTO) -> dict[str, Any]:
        payload = {
            "is_done": search_params.is_done,
            "created_from": (
                search_params.created_from.isoformat()
                if search_params.created_from
                else None
            ),
            "created_to": (
                search_params.created_to.isoformat() if search_params.created_to else None
            ),
            "query": search_params.query,
            "order_by": search_params.order_by.value,
            "direction": search_params.direction.value,
            "limit": search_params.limit,
            "offset": search_params.offset,
        }
        return {key: value for key, value in payload.items() if value is not None}

    @staticmethod
    def _serialize_task(task: TaskReadDTO) -> dict[str, Any]:
        return {
            "id": str(task.id),
            "title": task.title,
            "description": task.description,
            "is_done": task.is_done,
            "created_at": task.created_at.isoformat(),
            "updated_at": task.updated_at.isoformat(),
        }

    @staticmethod
    def _deserialize_task(payload: dict[str, Any]) -> TaskReadDTO:
        return TaskReadDTO(
            id=UUID(payload["id"]),
            title=payload["title"],
            description=payload.get("description"),
            is_done=bool(payload["is_done"]),
            created_at=datetime.fromisoformat(payload["created_at"]),
            updated_at=datetime.fromisoformat(payload["updated_at"]),
        )


def create_task_list_cache() -> TaskListCacheBackend:
    client = Redis.from_url(
        settings.redis.url,
        encoding="utf-8",
        decode_responses=True,
    )
    return RedisTaskListCache(
        client=client,
        ttl_seconds=settings.redis.task_list_ttl_seconds,
    )


def get_task_list_cache(request: Request) -> TaskListCacheBackend:
    task_list_cache = getattr(request.app.state, "task_list_cache", None)
    if task_list_cache is None:
        task_list_cache = create_task_list_cache()
        request.app.state.task_list_cache = task_list_cache
    return task_list_cache
