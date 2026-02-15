from datetime import date

from pydantic import EmailStr, Field, SecretStr, field_validator

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
    password: SecretStr
    first_name: str | None = Field(
        default=None, min_length=1, max_length=FIRST_NAME_MAX_LENGTH
    )
    last_name: str | None = Field(
        default=None, min_length=1, max_length=LAST_NAME_MAX_LENGTH
    )
    birthdate: date | None = None

    @field_validator("password")
    @classmethod
    def validate_password_length(cls, value: SecretStr) -> SecretStr:
        if len(value.get_secret_value()) < PASSWORD_MIN_LENGTH:
            raise ValueError(
                f"Password must be at least {PASSWORD_MIN_LENGTH} characters long"
            )
        return value

    @field_validator("birthdate")
    @classmethod
    def validate_birthdate(cls, value: date | None) -> date | None:
        if value and value > date.today():
            raise ValueError("Birthdate cannot be in the future")
        return value
