from uuid import UUID

from src.api.v1.tasks.create.request import CreateTaskRequest as TaskCreateSchema
from src.api.v1.tasks.create.response import CreateTaskResponse
from src.api.v1.tasks.get_by_id.response import TaskDetailResponse
from src.api.v1.tasks.get_list.request import GetTaskListRequest
from src.api.v1.tasks.get_list.response import TaskResponse
from src.api.v1.tasks.update.request import UpdateTaskRequest as TaskUpdateSchema
from src.api.v1.tasks.update.response import UpdateTaskResponse
from src.api.v1.tasks.stats_total.response import TaskStatsResponse
from src.api.v1.tasks.stats_by_day.response import TasksByDayResponse
from src.api.v1.tasks.active_users.response import ActiveUserResponse
from src.tasks.models import Task
from src.tasks.dto import TaskCreateDTO, TaskUpdateDTO, TaskFilterDTO
from src.tasks.exceptions import TaskNotFoundError
from src.tasks.repository import TaskRepository


class TaskService:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    async def create_task(
        self, task_data: TaskCreateSchema, user_id: UUID
    ) -> CreateTaskResponse:
        task_dto = TaskCreateDTO(
            title=task_data.title,
            description=task_data.description,
            user_id=user_id,
        )

        task_model = await self.repository.create(task_dto)
        return CreateTaskResponse.model_validate(task_model)

    async def get_task_by_id(self, task_id: UUID, user_id: UUID) -> TaskDetailResponse:
        task = await self._get_task_or_raise(task_id=task_id, user_id=user_id)
        return TaskDetailResponse.model_validate(task)

    async def get_all_tasks(
        self, search_params: GetTaskListRequest, user_id: UUID
    ) -> list[TaskResponse]:
        filter_dto = TaskFilterDTO(
            user_id=user_id,
            is_done=search_params.is_done,
            created_from=search_params.created_from,
            created_to=search_params.created_to,
            query=search_params.query,
            order_by=search_params.order_by,
            direction=search_params.direction,
            limit=search_params.limit,
            offset=search_params.offset,
        )

        tasks = await self.repository.get_filtered_tasks(filter_dto)
        return [TaskResponse.model_validate(task) for task in tasks]

    async def update_task(
        self, task_id: UUID, task_data: TaskUpdateSchema, user_id: UUID
    ) -> UpdateTaskResponse:
        task = await self._get_task_or_raise(task_id=task_id, user_id=user_id)

        update_dict = task_data.model_dump(exclude_unset=True)

        task_dto = TaskUpdateDTO(
            title=update_dict.get("title", ...),
            description=update_dict.get("description", ...),
            is_done=update_dict.get("is_done", ...),
        )

        if task_dto.title is not ...:
            task.title = task_dto.title
        if task_dto.description is not ...:
            task.description = task_dto.description
        if task_dto.is_done is not ...:
            task.is_done = task_dto.is_done

        updated_task = await self.repository.save(task)
        return UpdateTaskResponse.model_validate(updated_task)

    async def delete_task(self, task_id: UUID, user_id: UUID) -> None:
        task = await self._get_task_or_raise(task_id=task_id, user_id=user_id)
        await self.repository.delete(task_id=task.id)

    async def _get_task_or_raise(self, task_id: UUID, user_id: UUID) -> Task:
        task = await self.repository.get_by_id_and_user(
            task_id=task_id, user_id=user_id
        )
        if not task:
            raise TaskNotFoundError(
                task_id=task_id,
            )

        return task

    async def get_task_stats(self, user_id: UUID) -> TaskStatsResponse:
        stats = await self.repository.get_task_stats(user_id)

        completion_percentage = (
            (stats["completed"] / stats["total"] * 100) if stats["total"] > 0 else 0.0
        )

        return TaskStatsResponse(
            total=stats["total"],
            completed=stats["completed"],
            pending=stats["pending"],
            completion_percentage=round(completion_percentage, 2),
        )

    async def get_tasks_by_day(self, user_id: UUID) -> list[TasksByDayResponse]:
        tasks_by_day = await self.repository.get_tasks_by_day(user_id)
        return [
            TasksByDayResponse(date=item["date"], count=item["count"])
            for item in tasks_by_day
        ]

    async def get_active_users(self, limit: int = 10) -> list[ActiveUserResponse]:
        active_users = await self.repository.get_active_users(limit)
        return [
            ActiveUserResponse(
                user_id=item["user_id"],
                username=item["username"],
                pending_tasks_count=item["pending_tasks_count"],
            )
            for item in active_users
        ]
