from uuid import UUID

from pydantic import Field

from src.common.schemas import BaseResponseSchema


class ActiveUserResponse(BaseResponseSchema):
    user_id: UUID = Field(description="ID пользователя")
    username: str = Field(description="Имя пользователя")
    pending_tasks_count: int = Field(description="Количество невыполненных задач")
