from uuid import UUID

from fastapi import Depends
from starlette import status

from src.api.v1.tasks.dependencies import get_task_service
from src.api.v1.tasks.create.request import CreateTaskRequest
from src.api.v1.tasks.create.response import CreateTaskResponse
from src.auth import get_current_user_id
from src.tasks.dto import TaskCreateDTO
from src.tasks.services import TaskService


async def create_task(
    task_data: CreateTaskRequest,
    service: TaskService = Depends(get_task_service),
    user_id: UUID = Depends(get_current_user_id),
) -> CreateTaskResponse:
    task_dto = TaskCreateDTO(
        title=task_data.title,
        description=task_data.description,
        user_id=user_id,
    )
    task = await service.create_task(task_data=task_dto)
    return CreateTaskResponse.model_validate(task)


ENDPOINT_CONFIG = {
    "path": "/",
    "methods": ["POST"],
    "name": "Create task",
    "response_model": CreateTaskResponse,
    "status_code": status.HTTP_201_CREATED,
    "summary": "Создать задачу",
    "description": "Создает новую задачу для текущего пользователя",
    "responses": {
        status.HTTP_401_UNAUTHORIZED: {"description": "Неавторизован"},
        status.HTTP_400_BAD_REQUEST: {"description": "Невалидные данные запроса"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Внутренняя ошибка сервера"
        },
    },
    "tags": ["Tasks"],
}
