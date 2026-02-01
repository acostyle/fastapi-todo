from fastapi import Depends
from starlette import status

from src.api.v1.users.dependencies import get_user_service
from src.api.v1.users.register.request import RegisterRequest
from src.api.v1.users.register.response import RegisterResponse
from src.users.services import UserService


async def register_user(
    user_data: RegisterRequest,
    service: UserService = Depends(get_user_service),
) -> RegisterResponse:
    result = await service.create_user(user_data)
    return result


ENDPOINT_CONFIG = {
    "path": "/register",
    "methods": ["POST"],
    "name": "Register user",
    "response_model": RegisterResponse,
    "status_code": status.HTTP_201_CREATED,
    "summary": "Зарегистрировать пользователя",
    "description": "Создает новую учетную запись пользователя",
    "responses": {
        status.HTTP_400_BAD_REQUEST: {
            "description": "Пользователь уже существует или данные невалидны"
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Внутренняя ошибка сервера"
        },
    },
    "tags": ["Users"],
}
