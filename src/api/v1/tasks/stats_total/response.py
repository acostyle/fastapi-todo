from pydantic import Field

from src.common.schemas import BaseResponseSchema


class TaskStatsResponse(BaseResponseSchema):
    total: int = Field(description="Общее количество задач")
    completed: int = Field(description="Количество выполненных задач")
    pending: int = Field(description="Количество невыполненных задач")
    completion_percentage: float = Field(description="Процент завершенных задач")
