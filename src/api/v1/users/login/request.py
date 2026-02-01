from pydantic import Field

from src.common.constants import PASSWORD_MIN_LENGTH
from src.common.schemas import BaseSchema
from src.users.constants import USERNAME_MAX_LENGTH


class LoginRequest(BaseSchema):
    username: str = Field(min_length=1, max_length=USERNAME_MAX_LENGTH)
    password: str = Field(min_length=PASSWORD_MIN_LENGTH)
