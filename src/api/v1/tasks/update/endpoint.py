from uuid import UUID

from fastapi import Depends
from starlette import status

from src.api.v1.tasks.dependencies import get_task_service
from src.api.v1.tasks.update.request import UpdateTaskRequest
from src.api.v1.tasks.update.response import UpdateTaskResponse
from src.auth import get_current_user_id
from src.tasks.dto import TaskUpdateDTO
from src.tasks.services import TaskService


async def update_task(
    task_id: UUID,
    task_data: UpdateTaskRequest,
    service: TaskService = Depends(get_task_service),
    user_id: UUID = Depends(get_current_user_id),
) -> UpdateTaskResponse:
    update_dict = task_data.model_dump(exclude_unset=True)
    task_dto = TaskUpdateDTO(
        title=update_dict.get("title", ...),
        description=update_dict.get("description", ...),
        is_done=update_dict.get("is_done", ...),
    )
    task = await service.update_task(task_id=task_id, task_data=task_dto, user_id=user_id)
    return UpdateTaskResponse.model_validate(task)


ENDPOINT_CONFIG = {
    "path": "/{task_id}",
    "methods": ["PUT", "PATCH"],
    "name": "Update task",
    "response_model": UpdateTaskResponse,
    "status_code": status.HTTP_200_OK,
    "summary": "Обновить задачу",
    "description": "Обновляет задачу (частичное обновление поддерживается)",
    "responses": {
        status.HTTP_401_UNAUTHORIZED: {"description": "Неавторизован"},
        status.HTTP_404_NOT_FOUND: {"description": "Задача не найдена"},
        status.HTTP_400_BAD_REQUEST: {"description": "Невалидные данные"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Внутренняя ошибка сервера"
        },
    },
    "tags": ["Tasks"],
}
