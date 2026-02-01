from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_session
from src.tasks.repository import TaskRepository
from src.tasks.services import TaskService


def get_task_repository(session: AsyncSession = Depends(get_session)) -> TaskRepository:
    return TaskRepository(session)


def get_task_service(
    repository: TaskRepository = Depends(get_task_repository),
) -> TaskService:
    return TaskService(repository)
