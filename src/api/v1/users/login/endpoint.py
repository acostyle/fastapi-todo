from fastapi import Depends
from starlette import status

from src.api.v1.users.dependencies import get_user_service
from src.api.v1.users.login.request import LoginRequest
from src.api.v1.users.login.response import LoginResponse
from src.users.services import UserService


async def login_user(
    credentials: LoginRequest,
    service: UserService = Depends(get_user_service),
) -> LoginResponse:
    token = await service.login(
        username=credentials.username,
        password=credentials.password,
    )
    return LoginResponse(access_token=token, token_type="bearer")


ENDPOINT_CONFIG = {
    "path": "/login",
    "methods": ["POST"],
    "name": "Login user",
    "response_model": LoginResponse,
    "status_code": status.HTTP_200_OK,
    "summary": "Войти",
    "description": "Аутентифицирует пользователя и возвращает access token",
    "responses": {
        status.HTTP_401_UNAUTHORIZED: {"description": "Неверные учетные данные"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Внутренняя ошибка сервера"
        },
    },
    "tags": ["Users"],
}
