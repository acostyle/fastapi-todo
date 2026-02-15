from datetime import date, datetime
from uuid import UUID

from pydantic import EmailStr, Field

from src.common.schemas import BaseResponseSchema


class RegisterResponse(BaseResponseSchema):
    id: UUID
    username: str
    email: EmailStr
    first_name: str | None
    last_name: str | None
    birthdate: date | None
    created_at: datetime = Field(description="Дата создания пользователя")
    updated_at: datetime = Field(description="Дата последнего обновления пользователя")
