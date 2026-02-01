from uuid import UUID

from fastapi import Depends
from starlette import status

from src.api.v1.tasks.dependencies import get_task_service
from src.api.v1.tasks.get_list.request import GetTaskListRequest
from src.api.v1.tasks.get_list.response import TaskResponse
from src.auth import get_current_user_id
from src.tasks.services import TaskService


async def get_all_tasks(
    search_params: GetTaskListRequest = Depends(),
    service: TaskService = Depends(get_task_service),
    user_id: UUID = Depends(get_current_user_id),
) -> list[TaskResponse]:
    """
    Получить все задачи текущего пользователя.

    Args:
        search_params: Параметры поиска
        service: Сервис для работы с задачами
        user_id: ID текущего пользователя из JWT токена

    Returns:
        Список всех задач пользователя

    Raises:
        HTTPException 401: Если токен невалидный или отсутствует
    """
    tasks = await service.get_all_tasks(search_params=search_params, user_id=user_id)
    return tasks


ENDPOINT_CONFIG = {
    "path": "/",
    "methods": ["GET"],
    "name": "Get all tasks",
    "response_model": list[TaskResponse],
    "status_code": status.HTTP_200_OK,
    "summary": "Получить все задачи",
    "description": "Возвращает список всех задач текущего пользователя",
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
