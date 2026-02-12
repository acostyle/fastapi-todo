from fastapi import APIRouter

from src.api.v1.tasks.router import tasks_router
from src.api.v1.users.router import users_router

router = APIRouter()

router.include_router(tasks_router, prefix="/tasks", tags=["Tasks"])
router.include_router(users_router, prefix="/users", tags=["Users"])
