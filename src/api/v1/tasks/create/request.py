from pydantic import Field

from src.common.schemas import BaseSchema
from src.tasks.constants import TASK_TITLE_MAX_LENGTH


class CreateTaskRequest(BaseSchema):
    title: str = Field(
        min_length=1,
        max_length=TASK_TITLE_MAX_LENGTH,
        description="Название задачи",
        examples=["Купить молоко"],
    )
    description: str | None = Field(
        default=None,
        description="Описание задачи (опционально)",
        examples=["Купить 2 литра молока в магазине на углу"],
    )
