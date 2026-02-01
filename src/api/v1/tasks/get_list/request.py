from datetime import datetime

from pydantic import Field

from src.common.schemas import BaseSchema
from src.tasks.dto import TaskOrderBy, SortDirection


class GetTaskListRequest(BaseSchema):
    is_done: bool | None = Field(None, description="Фильтр по статусу выполнения")
    created_from: datetime | None = Field(
        None, description="Начало диапазона даты создания"
    )
    created_to: datetime | None = Field(
        None, description="Конец диапазона даты создания"
    )
    query: str | None = Field(None, description="Поиск по названию")

    order_by: TaskOrderBy = Field(
        TaskOrderBy.CREATED_AT, description="Поле для сортировки"
    )
    direction: SortDirection = Field(
        SortDirection.DESC, description="Направление (asc/desc)"
    )

    limit: int = Field(10, ge=1, le=100)
    offset: int = Field(0, ge=0)
