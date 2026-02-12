from uuid import UUID

from sqlalchemy import select, func, Integer
from sqlalchemy.ext.asyncio import AsyncSession

from src.tasks.dto import TaskCreateDTO, TaskFilterDTO
from src.tasks.models import Task
from src.users.models import User


class TaskRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, task_dto: TaskCreateDTO) -> Task:
        task = Task(
            title=task_dto.title,
            description=task_dto.description,
            user_id=task_dto.user_id,
        )
        self.session.add(task)
        await self.session.commit()
        await self.session.refresh(task)
        return task

    async def get_by_id_and_user(self, task_id: UUID, user_id: UUID) -> Task | None:
        query = select(Task).where((Task.id == task_id) & (Task.user_id == user_id))
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_all_by_user(self, user_id: UUID) -> list[Task]:
        query = select(Task).where(Task.user_id == user_id)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def get_filtered_tasks(self, filters: TaskFilterDTO) -> list[Task]:
        query = select(Task).where(Task.user_id == filters.user_id)

        if filters.is_done is not None:
            query = query.where(Task.is_done == filters.is_done)

        if filters.created_from:
            query = query.where(Task.created_at >= filters.created_from)

        if filters.created_to:
            query = query.where(Task.created_at <= filters.created_to)

        if filters.query:
            query = query.where(Task.title.ilike(f"%{filters.query}%"))

        # Сортировка
        order_field_map = {
            "created_at": Task.created_at,
            "title": Task.title,
            "is_done": Task.is_done,
        }
        order_field = order_field_map[filters.order_by.value]

        if filters.direction.value == "desc":
            query = query.order_by(order_field.desc())
        else:
            query = query.order_by(order_field.asc())

        query = query.limit(filters.limit).offset(filters.offset)

        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def save(self, task: Task) -> Task:
        self.session.add(task)
        await self.session.commit()
        await self.session.refresh(task)
        return task

    async def delete(self, task_id: UUID) -> None:
        task = await self.session.get(Task, task_id)
        if task:
            await self.session.delete(task)
            await self.session.commit()

    async def get_task_stats(self, user_id: UUID) -> dict:
        query = select(
            func.count(Task.id).label("total"),
            func.sum(func.cast(Task.is_done, Integer)).label("completed"),
        ).where(Task.user_id == user_id)

        result = await self.session.execute(query)
        row = result.first()

        total = row.total if row and row.total else 0
        completed = row.completed if row and row.completed else 0
        pending = total - completed

        return {
            "total": total,
            "completed": completed,
            "pending": pending,
        }

    async def get_tasks_by_day(self, user_id: UUID) -> list[dict]:
        query = (
            select(
                func.date(Task.created_at).label("date"),
                func.count(Task.id).label("count"),
            )
            .where(Task.user_id == user_id)
            .group_by(func.date(Task.created_at))
            .order_by(func.date(Task.created_at).desc())
        )

        result = await self.session.execute(query)
        return [{"date": row.date, "count": row.count} for row in result]

    async def get_active_users(self, limit: int = 10) -> list[dict]:
        query = (
            select(
                User.id.label("user_id"),
                User.username,
                func.count(Task.id).label("pending_tasks_count"),
            )
            .join(Task, Task.user_id == User.id)
            .where(Task.is_done.is_(False))
            .group_by(User.id, User.username)
            .order_by(func.count(Task.id).desc())
            .limit(limit)
        )

        result = await self.session.execute(query)
        return [
            {
                "user_id": row.user_id,
                "username": row.username,
                "pending_tasks_count": row.pending_tasks_count,
            }
            for row in result
        ]
