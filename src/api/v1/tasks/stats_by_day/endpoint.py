from uuid import UUID

from fastapi import Depends
from starlette import status

from src.api.v1.tasks.dependencies import get_task_service
from src.api.v1.tasks.stats_by_day.response import TasksByDayResponse
from src.auth import get_current_user_id
from src.tasks.services import TaskService


async def get_tasks_by_day(
    service: TaskService = Depends(get_task_service),
    user_id: UUID = Depends(get_current_user_id),
) -> list[TasksByDayResponse]:
    tasks_by_day = await service.get_tasks_by_day(user_id=user_id)
    return [TasksByDayResponse.model_validate(item) for item in tasks_by_day]


ENDPOINT_CONFIG = {
    "path": "/stats/by-day",
    "methods": ["GET"],
    "name": "Get tasks by day",
    "response_model": list[TasksByDayResponse],
    "status_code": status.HTTP_200_OK,
    "summary": "Группировка задач по датам",
    "description": "Возвращает количество задач, сгруппированных по дате создания",
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
