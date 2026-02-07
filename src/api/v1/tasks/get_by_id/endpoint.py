from uuid import UUID

from fastapi import Depends
from starlette import status

from src.api.v1.tasks.dependencies import get_task_service
from src.api.v1.tasks.get_by_id.response import TaskDetailResponse
from src.auth import get_current_user_id
from src.tasks.services import TaskService


async def get_task_by_id(
    task_id: UUID,
    service: TaskService = Depends(get_task_service),
    user_id: UUID = Depends(get_current_user_id),
) -> TaskDetailResponse:
    task = await service.get_task_by_id(task_id=task_id, user_id=user_id)
    return TaskDetailResponse.model_validate(task)


ENDPOINT_CONFIG = {
    "path": "/{task_id}",
    "methods": ["GET"],
    "name": "Get task by ID",
    "response_model": TaskDetailResponse,
    "status_code": status.HTTP_200_OK,
    "summary": "Получить задачу по ID",
    "description": "Возвращает детальную информацию о задаче",
    "responses": {
        status.HTTP_401_UNAUTHORIZED: {"description": "Неавторизован"},
        status.HTTP_404_NOT_FOUND: {"description": "Задача не найдена"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Внутренняя ошибка сервера"
        },
    },
    "tags": ["Tasks"],
}
