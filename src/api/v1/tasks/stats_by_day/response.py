from datetime import date as DateType

from pydantic import Field

from src.common.schemas import BaseResponseSchema


class TasksByDayResponse(BaseResponseSchema):
    date: DateType = Field(description="Дата создания задач")
    count: int = Field(description="Количество задач, созданных в эту дату")
