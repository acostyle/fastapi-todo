from uuid import UUID

from fastapi import Depends
from starlette import status

from src.api.v1.tasks.dependencies import get_task_service
from src.auth import get_current_user_id
from src.tasks.services import TaskService


async def delete_task(
    task_id: UUID,
    service: TaskService = Depends(get_task_service),
    user_id: UUID = Depends(get_current_user_id),
) -> None:
    """
    Удалить задачу.

    Args:
        task_id: UUID задачи
        service: Сервис для работы с задачами
        user_id: ID текущего пользователя из JWT токена

    Returns:
        None (HTTP 204 No Content)

    Raises:
        HTTPException 401: Если токен невалидный
        HTTPException 404: Если задача не найдена
    """
    await service.delete_task(task_id=task_id, user_id=user_id)


ENDPOINT_CONFIG = {
    "path": "/{task_id}",
    "methods": ["DELETE"],
    "name": "Delete task",
    "status_code": status.HTTP_204_NO_CONTENT,
    "summary": "Удалить задачу",
    "description": "Удаляет задачу безвозвратно",
    "responses": {
        status.HTTP_401_UNAUTHORIZED: {"description": "Неавторизован"},
        status.HTTP_404_NOT_FOUND: {"description": "Задача не найдена"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Внутренняя ошибка сервера"
        },
    },
    "tags": ["Tasks"],
}
