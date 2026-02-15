from fastapi import Depends
from starlette import status

from src.api.v1.users.dependencies import get_user_service
from src.api.v1.users.register.request import RegisterRequest
from src.api.v1.users.register.response import RegisterResponse
from src.users.dto import UserCreateDTO
from src.users.services import UserService


async def register_user(
    user_data: RegisterRequest,
    service: UserService = Depends(get_user_service),
) -> RegisterResponse:
    user_dto = UserCreateDTO(
        username=user_data.username,
        email=str(user_data.email),
        password=user_data.password.get_secret_value(),
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        birthdate=user_data.birthdate,
    )
    result = await service.create_user(user_dto)
    return RegisterResponse.model_validate(result)


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
