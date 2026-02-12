from datetime import date

from pydantic import EmailStr, Field

from src.common.constants import PASSWORD_MIN_LENGTH
from src.common.schemas import BaseSchema
from src.users.constants import (
    USERNAME_MAX_LENGTH,
    EMAIL_MAX_LENGTH,
    FIRST_NAME_MAX_LENGTH,
    LAST_NAME_MAX_LENGTH,
)


class RegisterRequest(BaseSchema):
    username: str = Field(min_length=1, max_length=USERNAME_MAX_LENGTH)
    email: EmailStr = Field(max_length=EMAIL_MAX_LENGTH)
    password: str = Field(min_length=PASSWORD_MIN_LENGTH)
    first_name: str | None = Field(
        default=None, min_length=1, max_length=FIRST_NAME_MAX_LENGTH
    )
    last_name: str | None = Field(
        default=None, min_length=1, max_length=LAST_NAME_MAX_LENGTH
    )
    birthdate: date | None = None
