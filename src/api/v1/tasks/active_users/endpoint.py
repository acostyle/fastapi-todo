from fastapi import Depends, Query
from starlette import status

from src.api.v1.tasks.dependencies import get_task_service
from src.api.v1.tasks.active_users.response import ActiveUserResponse
from src.tasks.services import TaskService


async def get_active_users(
    limit: int = Query(10, ge=1, le=100, description="Количество пользователей в топе"),
    service: TaskService = Depends(get_task_service),
) -> list[ActiveUserResponse]:
    users = await service.get_active_users(limit=limit)
    return [ActiveUserResponse.model_validate(user) for user in users]


ENDPOINT_CONFIG = {
    "path": "/active-users",
    "methods": ["GET"],
    "name": "Get active users",
    "response_model": list[ActiveUserResponse],
    "status_code": status.HTTP_200_OK,
    "summary": "Топ активных пользователей",
    "description": "Возвращает топ пользователей по количеству невыполненных задач",
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
