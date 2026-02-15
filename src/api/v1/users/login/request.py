from pydantic import Field, SecretStr, field_validator

from src.common.constants import PASSWORD_MIN_LENGTH
from src.common.schemas import BaseSchema
from src.users.constants import USERNAME_MAX_LENGTH


class LoginRequest(BaseSchema):
    username: str = Field(min_length=1, max_length=USERNAME_MAX_LENGTH)
    password: SecretStr

    @field_validator("password")
    @classmethod
    def validate_password_length(cls, value: SecretStr) -> SecretStr:
        if len(value.get_secret_value()) < PASSWORD_MIN_LENGTH:
            raise ValueError(
                f"Password must be at least {PASSWORD_MIN_LENGTH} characters long"
            )
        return value
