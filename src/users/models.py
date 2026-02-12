import uuid
from datetime import date
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import String, Date
from sqlalchemy.orm import mapped_column, Mapped, relationship, validates

from src.database import Base
from src.common.mixins import TimestampMixin
from src.users.constants import (
    USERNAME_MAX_LENGTH,
    EMAIL_MAX_LENGTH,
    FIRST_NAME_MAX_LENGTH,
    LAST_NAME_MAX_LENGTH,
)

if TYPE_CHECKING:
    from src.tasks.models import Task


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    username: Mapped[str] = mapped_column(String(USERNAME_MAX_LENGTH), unique=True)
    email: Mapped[str] = mapped_column(String(EMAIL_MAX_LENGTH), unique=True)
    first_name: Mapped[str | None] = mapped_column(String(FIRST_NAME_MAX_LENGTH))
    last_name: Mapped[str | None] = mapped_column(String(LAST_NAME_MAX_LENGTH))
    birthdate: Mapped[date | None] = mapped_column(Date, nullable=True)
    hashed_password: Mapped[str] = mapped_column(String(1024))
    is_active: Mapped[bool] = mapped_column(default=True)

    tasks: Mapped[list["Task"]] = relationship(
        back_populates="owner", cascade="all, delete-orphan"
    )

    @validates("birthdate")
    def validate_birthdate(self, key, value):
        if value and value > date.today():
            raise ValueError("Birthdate cannot be in the future")
        return value
