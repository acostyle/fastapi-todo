from uuid import UUID

from fastapi import Depends
from starlette import status

from src.api.v1.tasks.dependencies import get_task_service
from src.api.v1.tasks.stats_total.response import TaskStatsResponse
from src.auth import get_current_user_id
from src.tasks.services import TaskService


async def get_task_stats(
    service: TaskService = Depends(get_task_service),
    user_id: UUID = Depends(get_current_user_id),
) -> TaskStatsResponse:
    """
    Получить статистику по задачам текущего пользователя.

    Args:
        service: Сервис для работы с задачами
        user_id: ID текущего пользователя из JWT токена

    Returns:
        Статистика: всего задач, выполнено, невыполнено, процент завершения

    Raises:
        HTTPException 401: Если токен невалидный или отсутствует
    """
    return await service.get_task_stats(user_id=user_id)


ENDPOINT_CONFIG = {
    "path": "/stats/total",
    "methods": ["GET"],
    "name": "Get task statistics",
    "response_model": TaskStatsResponse,
    "status_code": status.HTTP_200_OK,
    "summary": "Получить статистику по задачам",
    "description": "Возвращает общую статистику задач пользователя: количество выполненных/невыполненных, процент завершения",
    "responses": {
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Неавторизован - невалидный или отсутствующий токен"
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Внутренняя ошибка сервера"
        },
    },
    "tags": ["Tasks"],
}
