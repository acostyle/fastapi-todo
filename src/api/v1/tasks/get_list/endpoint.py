from uuid import UUID

from fastapi import Depends
from starlette import status

from src.api.v1.tasks.dependencies import get_task_service
from src.api.v1.tasks.get_list.request import GetTaskListRequest
from src.api.v1.tasks.get_list.response import TaskResponse
from src.auth import get_current_user_id
from src.tasks.dto import TaskFilterDTO
from src.tasks.services import TaskService


async def get_all_tasks(
    search_params: GetTaskListRequest = Depends(),
    service: TaskService = Depends(get_task_service),
    user_id: UUID = Depends(get_current_user_id),
) -> list[TaskResponse]:
    filter_dto = TaskFilterDTO(
        user_id=user_id,
        is_done=search_params.is_done,
        created_from=search_params.created_from,
        created_to=search_params.created_to,
        query=search_params.query,
        order_by=search_params.order_by,
        direction=search_params.direction,
        limit=search_params.limit,
        offset=search_params.offset,
    )
    tasks = await service.get_all_tasks(search_params=filter_dto)
    return [TaskResponse.model_validate(task) for task in tasks]


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
