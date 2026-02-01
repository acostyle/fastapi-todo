from uuid import UUID

from fastapi import Depends
from starlette import status

from src.api.v1.users.dependencies import get_user_service
from src.api.v1.users.get_by_id.response import GetUserResponse
from src.users.services import UserService


async def get_user_by_id(
    user_id: UUID,
    service: UserService = Depends(get_user_service),
) -> GetUserResponse:
    return await service.get_user(user_id=user_id)


ENDPOINT_CONFIG = {
    "path": "/{user_id}",
    "methods": ["GET"],
    "name": "Get user by ID",
    "response_model": GetUserResponse,
    "status_code": status.HTTP_200_OK,
    "summary": "Получить пользователя по ID",
    "description": "Возвращает данные пользователя по user_id",
    "responses": {
        status.HTTP_404_NOT_FOUND: {"description": "Пользователь не найден"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Внутренняя ошибка сервера"
        },
    },
    "tags": ["Users"],
}
