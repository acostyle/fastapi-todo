from uuid import UUID

from fastapi import Depends
from starlette import status

from src.api.v1.tasks.dependencies import get_task_service
from src.api.v1.tasks.create.request import CreateTaskRequest
from src.api.v1.tasks.create.response import CreateTaskResponse
from src.auth import get_current_user_id
from src.tasks.services import TaskService


async def create_task(
    task_data: CreateTaskRequest,
    service: TaskService = Depends(get_task_service),
    user_id: UUID = Depends(get_current_user_id),
) -> CreateTaskResponse:
    """
    Создать новую задачу.

    Args:
        task_data: Данные для создания задачи
        service: Сервис для работы с задачами
        user_id: ID текущего пользователя из JWT токена

    Returns:
        Созданная задача

    Raises:
        HTTPException 401: Если токен невалидный
        HTTPException 400: Если данные невалидны
    """
    task = await service.create_task(task_data=task_data, user_id=user_id)
    return task


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
