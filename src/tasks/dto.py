from dataclasses import dataclass
from datetime import date, datetime
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


@dataclass
class TaskReadDTO:
    id: UUID
    title: str
    description: str | None
    is_done: bool
    created_at: datetime
    updated_at: datetime


@dataclass
class TaskStatsDTO:
    total: int
    completed: int
    pending: int
    completion_percentage: float


@dataclass
class TasksByDayDTO:
    date: date
    count: int


@dataclass
class ActiveUserDTO:
    user_id: UUID
    username: str
    pending_tasks_count: int
