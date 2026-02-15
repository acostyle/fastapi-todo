from uuid import UUID

from src.tasks.cache import TaskListCacheBackend
from src.tasks.dto import (
    ActiveUserDTO,
    TaskCreateDTO,
    TaskFilterDTO,
    TaskReadDTO,
    TaskStatsDTO,
    TasksByDayDTO,
    TaskUpdateDTO,
)
from src.tasks.exceptions import TaskNotFoundError
from src.tasks.models import Task
from src.tasks.repository import TaskRepository


class TaskService:
    def __init__(
        self,
        repository: TaskRepository,
        task_list_cache: TaskListCacheBackend,
    ):
        self.repository = repository
        self.task_list_cache = task_list_cache

    async def create_task(self, task_data: TaskCreateDTO) -> TaskReadDTO:
        task_model = await self.repository.create(task_data)
        await self.task_list_cache.invalidate_user(task_data.user_id)
        return self._to_task_read_dto(task_model)

    async def get_task_by_id(self, task_id: UUID, user_id: UUID) -> TaskReadDTO:
        task = await self._get_task_or_raise(task_id=task_id, user_id=user_id)
        return self._to_task_read_dto(task)

    async def get_all_tasks(self, search_params: TaskFilterDTO) -> list[TaskReadDTO]:
        self._validate_filters(search_params)
        cached_tasks = await self.task_list_cache.get_tasks(
            user_id=search_params.user_id, search_params=search_params
        )
        if cached_tasks is not None:
            return cached_tasks

        tasks = await self.repository.get_filtered_tasks(search_params)
        task_responses = [self._to_task_read_dto(task) for task in tasks]
        await self.task_list_cache.set_tasks(
            user_id=search_params.user_id,
            search_params=search_params,
            tasks=task_responses,
        )
        return task_responses

    async def update_task(
        self, task_id: UUID, task_data: TaskUpdateDTO, user_id: UUID
    ) -> TaskReadDTO:
        task = await self._get_task_or_raise(task_id=task_id, user_id=user_id)
        self._apply_task_updates(task=task, task_data=task_data)

        updated_task = await self.repository.save(task)
        await self.task_list_cache.invalidate_user(user_id)
        return self._to_task_read_dto(updated_task)

    async def delete_task(self, task_id: UUID, user_id: UUID) -> None:
        task = await self._get_task_or_raise(task_id=task_id, user_id=user_id)
        await self.repository.delete(task_id=task.id)
        await self.task_list_cache.invalidate_user(user_id)

    async def _get_task_or_raise(self, task_id: UUID, user_id: UUID) -> Task:
        task = await self.repository.get_by_id_and_user(
            task_id=task_id, user_id=user_id
        )
        if not task:
            raise TaskNotFoundError(
                task_id=task_id,
            )

        return task

    async def get_task_stats(self, user_id: UUID) -> TaskStatsDTO:
        stats = await self.repository.get_task_stats(user_id)

        completion_percentage = (
            (stats["completed"] / stats["total"] * 100) if stats["total"] > 0 else 0.0
        )

        return TaskStatsDTO(
            total=stats["total"],
            completed=stats["completed"],
            pending=stats["pending"],
            completion_percentage=round(completion_percentage, 2),
        )

    async def get_tasks_by_day(self, user_id: UUID) -> list[TasksByDayDTO]:
        tasks_by_day = await self.repository.get_tasks_by_day(user_id)
        return [TasksByDayDTO(date=item["date"], count=item["count"]) for item in tasks_by_day]

    async def get_active_users(self, limit: int = 10) -> list[ActiveUserDTO]:
        active_users = await self.repository.get_active_users(limit)
        return [
            ActiveUserDTO(
                user_id=item["user_id"],
                username=item["username"],
                pending_tasks_count=item["pending_tasks_count"],
            )
            for item in active_users
        ]

    @staticmethod
    def _apply_task_updates(task: Task, task_data: TaskUpdateDTO) -> None:
        # Обновляем только те поля, которые реально пришли в PATCH/PUT:
        # значение `...` означает "поле не передано", его не трогаем.
        for field_name in ("title", "description", "is_done"):
            field_value = getattr(task_data, field_name)
            if field_value is not ...:
                setattr(task, field_name, field_value)

    @staticmethod
    def _validate_filters(search_params: TaskFilterDTO) -> None:
        if not 1 <= search_params.limit <= 100:
            raise ValueError("limit must be between 1 and 100")
        if search_params.offset < 0:
            raise ValueError("offset must be >= 0")
        if (
            search_params.created_from
            and search_params.created_to
            and search_params.created_from > search_params.created_to
        ):
            raise ValueError("created_from must be <= created_to")

    @staticmethod
    def _to_task_read_dto(task: Task) -> TaskReadDTO:
        return TaskReadDTO(
            id=task.id,
            title=task.title,
            description=task.description,
            is_done=task.is_done,
            created_at=task.created_at,
            updated_at=task.updated_at,
        )
