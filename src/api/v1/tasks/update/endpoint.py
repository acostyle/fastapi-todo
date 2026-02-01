from uuid import UUID

from fastapi import Depends
from starlette import status

from src.api.v1.tasks.dependencies import get_task_service
from src.api.v1.tasks.update.request import UpdateTaskRequest
from src.api.v1.tasks.update.response import UpdateTaskResponse
from src.auth import get_current_user_id
from src.tasks.services import TaskService


async def update_task(
    task_id: UUID,
    task_data: UpdateTaskRequest,
    service: TaskService = Depends(get_task_service),
    user_id: UUID = Depends(get_current_user_id),
) -> UpdateTaskResponse:
    """
    Обновить задачу.

    Поддерживает частичное обновление - можно обновить только некоторые поля.
    Не переданные поля остаются без изменений.
    Чтобы очистить description, передайте null.

    Args:
        task_id: UUID задачи
        task_data: Данные для обновления
        service: Сервис для работы с задачами
        user_id: ID текущего пользователя из JWT токена

    Returns:
        Обновленная задача

    Raises:
        HTTPException 401: Если токен невалидный
        HTTPException 404: Если задача не найдена
        HTTPException 400: Если данные невалидны
    """
    task = await service.update_task(
        task_id=task_id, task_data=task_data, user_id=user_id
    )
    return task


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
