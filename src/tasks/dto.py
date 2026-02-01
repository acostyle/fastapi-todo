from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from uuid import UUID


class TaskOrderBy(str, Enum):
    CREATED_AT = "created_at"
    TITLE = "title"
    IS_DONE = "is_done"


class SortDirection(str, Enum):
    ASC = "asc"
    DESC = "desc"


@dataclass
class TaskCreateDTO:
    title: str
    user_id: UUID
    description: str | None = None


@dataclass
class TaskUpdateDTO:
    title: str | None | type[Ellipsis] = ...
    description: str | None | type[Ellipsis] = ...
    is_done: bool | None | type[Ellipsis] = ...


@dataclass
class TaskFilterDTO:
    user_id: UUID
    is_done: bool | None = None
    created_from: datetime | None = None
    created_to: datetime | None = None
    query: str | None = None
    order_by: TaskOrderBy = TaskOrderBy.CREATED_AT
    direction: SortDirection = SortDirection.DESC
    limit: int = 10
    offset: int = 0

    def __post_init__(self):
        if self.limit < 1 or self.limit > 100:
            raise ValueError("limit must be between 1 and 100")
        if self.offset < 0:
            raise ValueError("offset must be >= 0")
        if (
            self.created_from
            and self.created_to
            and self.created_from > self.created_to
        ):
            raise ValueError("created_from must be <= created_to")
