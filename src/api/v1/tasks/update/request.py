from pydantic import Field

from src.common.schemas import BaseSchema
from src.tasks.constants import TASK_TITLE_MAX_LENGTH


class UpdateTaskRequest(BaseSchema):
    title: str | None = Field(
        default=None,
        max_length=TASK_TITLE_MAX_LENGTH,
        description="Название задачи (опционально)",
        examples=["Купить хлеб"],
    )
    description: str | None = Field(
        default=None,
        description="Описание задачи (опционально, можно установить null для очистки)",
        examples=["Купить свежий хлеб в пекарне"],
    )
    is_done: bool | None = Field(
        default=None,
        description="Статус выполнения (опционально)",
        examples=[True],
    )
