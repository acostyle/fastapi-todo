import uuid
from typing import TYPE_CHECKING

from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base
from src.common.mixins import TimestampMixin
from src.tasks.constants import TASK_TITLE_MAX_LENGTH

if TYPE_CHECKING:
    from src.users.models import User


class Task(Base, TimestampMixin):
    __tablename__ = "tasks"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    title: Mapped[str] = mapped_column(String(TASK_TITLE_MAX_LENGTH))
    description: Mapped[str | None] = mapped_column(Text(), nullable=True)
    is_done: Mapped[bool] = mapped_column(default=False)

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))  # on_delete?
    owner: Mapped["User"] = relationship(back_populates="tasks")
