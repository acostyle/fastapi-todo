from datetime import datetime
from uuid import UUID

from pydantic import Field

from src.common.schemas import BaseResponseSchema


class UpdateTaskResponse(BaseResponseSchema):
    id: UUID = Field(description="Уникальный идентификатор задачи")
    title: str = Field(description="Название задачи")
    description: str | None = Field(default=None, description="Описание задачи")
    is_done: bool = Field(description="Статус выполнения")
    created_at: datetime = Field(description="Дата создания")
    updated_at: datetime = Field(description="Дата последнего обновления (обновлена)")
